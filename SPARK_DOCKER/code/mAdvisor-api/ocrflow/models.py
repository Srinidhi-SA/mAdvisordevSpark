from django.db import models

# Create your models here.
import random
import string
import datetime
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import(
    GenericForeignKey,
    GenericRelation
)
import simplejson as json
from ocr.models import OCRImage
from ocrflow.forms import ApprovalForm
from ocrflow import process
from singleton_model import SingletonModel

class OCRRules(models.Model):
    auto_assignmentL1 = models.BooleanField(default=False)
    auto_assignmentL2 = models.BooleanField(default=False)
    rulesL1 = models.TextField(max_length=3000, default={}, null=True, blank=True)
    rulesL2 = models.TextField(max_length=3000, default={}, null=True, blank=True)
    modified_at = models.DateTimeField(
        null=True,
        blank=True,
        auto_now_add=True
    )
    created_by = models.ForeignKey(User,blank=True, null=True)

    def __str__(self):
        return " : ".join(["{}".format(x) for x in ["OCRRule", self.created_by]])

    def save(self, *args, **kwargs):
        """Save OCRRules model"""
        super(OCRRules, self).save(*args, **kwargs)

class Task(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=100)
    assigned_group = models.ForeignKey(Group, related_name='tasks')
    assigned_user = models.ForeignKey(User,blank=True, null=True)
    is_closed = models.BooleanField(default=False)
    reviewed_on = models.DateTimeField(
        null=True,
        blank=True,
        auto_now_add=True
    )
    comments = models.TextField(blank=True, null=True)
    bad_scan = models.TextField(blank=True, null=True, max_length=100)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return " : ".join(["{}".format(x) for x in ["Task", self.name, self.slug]])

    def code(self):
        """Unique identifier of task"""
        return "{}-{}".format(self.slug, self.id)

    # def save(self, *args, **kwargs):
    #     """Save Task model"""
    #     self.generate_slug()
    #     super(Task, self).save(*args, **kwargs)

    # def generate_slug(self):
    #     """generate slug"""
    #     if not self.slug:
    #         self.slug = slugify(str(self.name) + '-' + ''.join(
    #             random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))

    @property
    def process_config(self):
        return self.content_object.PROCESS

    @property
    def state(self):
        return self.process_config[self.slug]

    @property
    def get_approval_form(self):
        return self.state.get('form', None) or ApprovalForm

    @property
    def next_transition(self):
        return self.state.get('next_transition', None)

    def submit(self, form, user):
        status = form.cleaned_data['status']
        comments = form.cleaned_data['remarks']
        self.comments = comments
        self.reviewed_on = datetime.datetime.now()
        self.is_closed = True
        self.save()

        # execute content object task action
        self.execute_task_actions(form, user)

        if self.next_transition:
            new_state = self.process_config[self.next_transition]
            new_user = self.assign_newuser(new_state)
            self.create_new_task(new_state)

    def assign_newuser(self, state):
        return User.objects.filter(
            groups__name=state['group'],
            is_active=True).order_by('?').first()

    def create_new_task(self, state):
        group = Group.objects.get(name=state['group'])
        newuser = self.assign_newuser(state)
        Task.objects.create(
            name=state['name'],
            slug=self.next_transition,
            assigned_group=group,
            assigned_user=newuser,
            content_type=self.content_type,
            object_id=self.content_object.id
        )

    def execute_task_actions(self, form, user):
        task_actions = self.state['on_completion']
        for action in task_actions:
            action(form, self.content_object, user)


class SimpleFlow(models.Model):
    tasks = GenericRelation(Task, related_name='tasks')

    class Meta:
        abstract = True

    def assigned_user(self, initial, state, rules, users=None):

        if users is None:
            Reviewers_queryset = User.objects.filter(
                groups__name=state['group'],
                is_active=True,
                ocruserprofile__supervisor=self.rule.created_by,
                ocruserprofile__is_active=True).order_by('?')
        else:
            Reviewers_queryset = User.objects.filter(
                username__in=users).order_by('?')

        for reviewer in Reviewers_queryset:
            isLimitReached = self.check_task_limit(rules, reviewer)
            if isLimitReached:
                if rules['auto']['active'] == "True":
                    if rules['auto']['remainaingDocsDistributionRule'] == 1:
                        return reviewer
                    else:
                        return None
                else:
                    if rules['custom']['remainaingDocsDistributionRule'] == 1:
                        return reviewer
                    else:
                        return None
            elif not isLimitReached:
                return reviewer
            else:
                return None

    def check_task_limit(self, rules, user):
        totalPendingTasks = len(Task.objects.filter(
            assigned_user=user,
            is_closed=False))
        if rules['auto']['active'] == "True":
            if totalPendingTasks >= rules['auto']['max_docs_per_reviewer']:
                return True
            else:
                return False
        else:
            if totalPendingTasks >= rules['custom']['max_docs_per_reviewer']:
                return True
            else:
                return False

    def start_simpleflow(self, initial_state=None):
        initial = initial_state or 'initial'
        state = self.PROCESS[initial]
        group = Group.objects.get(name=state['group'])
        content_type = ContentType.objects.get_for_model(self)

        #---------------------  Fetch OCR Rule ------------------------
        if initial == 'initial':
            rules = json.loads(self.rule.rulesL1)
        else:
            rules = json.loads(self.rule.rulesL2)
        #--------------------------------------------------------------

        #---------------   Check for reviewer availability ------------
        if rules['auto']['active'] == "True":
            reviewer = self.assigned_user(initial, state, rules)
        else:
            usersList = rules['custom']['selected_reviewers']
            reviewer = self.assigned_user(initial, state, rules, users=usersList)
        #--------------------------------------------------------------

        #------------------ Assignment based on doc_type --------------
        if self.doc_type == 'pdf':

            if reviewer is not None:
                pdfObject = OCRImage.objects.get(id=self.ocr_image.id)
                pages_queryset = OCRImage.objects.filter(
                    identifier=pdfObject.identifier,
                    doctype = 'pdf_page'
                )
                for page in pages_queryset:
                    object = ReviewRequest.objects.create(
                                ocr_image = page,
                                created_by = page.created_by,
                                rule = self.rule,
                                doc_type = 'pdf_page'
                            )
                    taskObj = Task.objects.create(
                                name=state['name'],
                                slug=initial,
                                assigned_group=group,
                                assigned_user=reviewer,
                                content_type=ContentType.objects.get_for_model(object),
                                object_id=object.id
                            )
                    if initial == 'initial':
                        #--------Update Review status--------
                        object.status='submitted_for_review(L1)'
                        #------Update OCR Image Object-------
                        page.is_L1assigned = True
                        page.status='ready_to_verify(L1)'
                        page.assignee=reviewer
                        page.l1_assignee=reviewer
                        #----------Save changes---------
                        object.save()
                        page.save()

                        print("Task assigned:  {0}  -  User:  {1}".format(page.name, taskObj.assigned_user))
                #-----------Update PDF OCR Object -----------
                pdfObject.is_L1assigned = True
                pdfObject.status='ready_to_verify(L1)'
                pdfObject.assignee=reviewer
                pdfObject.l1_assignee=reviewer
                self.status='submitted_for_review(L1)'
                #------ Save changes -------
                pdfObject.save()
                self.save()

            else:
                print("No Reviewers available. Moving to backlog")
                pass

        elif self.doc_type == 'pdf_page':
            if reviewer is not None:
                if initial == 'RL2_approval':
                    #Fetch OCRImage with PDF
                    pdfObject = OCRImage.objects.get(
                        identifier=self.ocr_image.identifier,
                        doctype='pdf')

                    if pdfObject.is_L2assigned == False:
                       pdfObject.assignee = reviewer
                       pdfObject.is_L2assigned = True
                       pdfObject.status='ready_to_verify(L2)'
                       pdfObject.save()
                       #Update PDF Review Object
                       revObject = ReviewRequest.objects.get(ocr_image=pdfObject)
                       revObject.status = 'submitted_for_review(L2)'
                       revObject.save()

                    Task.objects.create(
                        name=state['name'],
                        slug=initial,
                        assigned_group=group,
                        assigned_user=pdfObject.assignee,
                        content_type=content_type,
                        object_id=self.id
                    )
                    #Update Pdf_page and corresponding review object
                    imageObject=OCRImage.objects.get(id=self.ocr_image.id)
                    imageObject.is_L2assigned = True
                    imageObject.status='ready_to_verify(L2)'
                    imageObject.assignee=pdfObject.assignee
                    self.status='submitted_for_review(L2)'
                    imageObject.save()
                    self.save()
            else:
                print("No Reviewers available. Moving to backlog")
                pass
        else:
            if reviewer is not None:
                Task.objects.create(
                    name=state['name'],
                    slug=initial,
                    assigned_group=group,
                    assigned_user=reviewer,
                    content_type=content_type,
                    object_id=self.id
                )
                imageObject=OCRImage.objects.get(id=self.ocr_image.id)
                if initial == 'initial':
                    imageObject.is_L1assigned = True
                    imageObject.status='ready_to_verify(L1)'
                    imageObject.assignee=reviewer
                    imageObject.l1_assignee=reviewer
                    self.status='submitted_for_review(L1)'
                else:
                    imageObject.is_L2assigned = True
                    imageObject.status='ready_to_verify(L2)'
                    imageObject.assignee=reviewer
                    self.status='submitted_for_review(L2)'
                imageObject.save()
                self.save()
            else:
                print("No Reviewers available. Moving to backlog")
                pass

class ReviewRequest(SimpleFlow):
    # assign your process here
    PROCESS = process.AUTO_ASSIGNMENT
    slug = models.SlugField(null=False, blank=True, max_length=100)
    ocr_image = models.OneToOneField(
        OCRImage,
        blank=True,
        null=True,
        related_name='review_requests'
    )
    rule = models.ForeignKey(OCRRules, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='+'
    )
    modified_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='+'
    )
    status = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        choices=[
            ('created', 'Created'),
            ('submitted_for_review(L1)', 'Submitted for review(L1)'),
            ('submitted_for_review(L2)', 'Submitted for review(L2)'),
            ('reviewerL2_reviewed', 'ReviewerL2 Reviewed'),
            ('reviewerL2_rejected', 'ReviewerL2 Rejected'),
            ('reviewerL1_reviewed', 'ReviewerL1 Reviewed'),
            ('reviewerL1_rejected', 'ReviewerL1 Rejected'),
        ]
    )
    doc_type = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        choices=[
            ('pdf', 'PDF'),
            ('pdf_page', 'PDF PAGE'),
            ('image', 'IMAGE'),
        ],
    )
    def save(self, *args, **kwargs):
        """Save OCRUserProfile model"""
        self.generate_slug()
        super(ReviewRequest, self).save(*args, **kwargs)

    def generate_slug(self):
        """generate slug"""
        if not self.slug:
            self.slug = slugify("ITEREQ" + "-" + ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))

def submit_for_approval(sender, instance, created, **kwargs):
    if created:
        instance.status = "created"
        instance.save()
        instance.start_simpleflow()

post_save.connect(submit_for_approval, sender=ReviewRequest)
