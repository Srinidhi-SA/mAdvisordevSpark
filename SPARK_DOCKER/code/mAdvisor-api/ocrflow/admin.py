from django.contrib import admin

# Register your models here.
from ocrflow.models import Task, SimpleFlow, ReviewRequest, OCRRules

class TaskAdmin(admin.ModelAdmin):
    """
    Model: Task
    """
    icon = '<i class="material-icons">cloud_done</i>'
    search_fields = ["name"]
    list_display = ["name", "assigned_group", "assigned_user", "is_closed"]
    list_filter = ["assigned_group", "assigned_user", "is_closed"]
    #readonly_fields = ["slug"]

    def get_queryset(self, request):
        queryset = super(TaskAdmin, self).get_queryset(request)
        #queryset = queryset.order_by('-created_at')
        return queryset

class ReviewRequestAdmin(admin.ModelAdmin):
    #form = BugForm
    list_display = ('ocr_image', 'slug', 'status')

    def get_queryset(self, request):
        queryset = super(ReviewRequestAdmin, self).get_queryset(request)
        #queryset = queryset.order_by('-recorded_at')
        return queryset

class OCRRuleAdmin(admin.ModelAdmin):
    #form = BugForm
    readonly_fields = ["created_by",]

    def get_queryset(self, request):
        queryset = super(OCRRuleAdmin, self).get_queryset(request)
        #queryset = queryset.order_by('-recorded_at')
        return queryset

admin.site.register(ReviewRequest,ReviewRequestAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(OCRRules, OCRRuleAdmin)
