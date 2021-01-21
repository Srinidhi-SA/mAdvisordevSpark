from builtins import str
from builtins import range
from builtins import object
from django.db import models
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
import random
import string
from django.template.defaultfilters import slugify
from rest_framework import permissions


"""
Below are some permission classes that can be used to put permission before accessing
views.
"""

class DummyPermission(permissions.BasePermission):
    message = 'Adding Dummy not allowed.'

    def has_permission(self, request, view):
        user = request.user

        # if user is superadmin then allowed to access
        if user.is_superuser:
            return True
        else:
            # if user is not superadmin then it can only access SAFE METHODS which is GET
            if request.method in permissions.SAFE_METHODS:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        pass


class DummyPermissionTrue(permissions.BasePermission):
    message = 'Always True'

    def has_permission(self, request, view):
        user = request.user

        # Always true. Everyone is allowed to view
        return True

    def has_object_permission(self, request, view, obj):
        pass


class DummyPermissionFalse(permissions.BasePermission):
    message = 'Always False'

    def has_permission(self, request, view):
        user = request.user

        # Always False. No one is allowed to view
        return False

    def has_object_permission(self, request, view, obj):
        pass

class DummyPermissionGroup(permissions.BasePermission):
    message = 'Group related'

    def has_permission(self, request, view):
        user = request.user

        # If user has this particular group in its user-group-list
        if 'AllAccess' in user.groups.values_list('name', flat=True) or user.is_superuser:
            return True

    def has_object_permission(self, request, view, obj):
        pass


class DummyPermissionUsingHasObject(permissions.BasePermission):
    message = 'Using has_object_permissio.'

    def has_permission(self, request, view):
        return True

    # this method comes into picture when has_permission is already computed true.
    # this functions allows permission for object level
    def has_object_permission(self, request, view, obj):
        # Obj is actual instance. Like dataset's object.
        # one can develop further logic on the basis of obj instance details
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.created_by.id == request.user.id


class DummyPermissionModelPermission(permissions.DjangoModelPermissions):
    message = 'Using DjangoModelPermission.'

    def has_permission(self, request, view):

        #  First collect all the permission in model of this particular view.
        #  like can add dataset, can change dataset, can delete dataset .
        #  then compare it with user-permissions granted to user.
        perms = self.get_required_permissions(request.method, view.models)
        return request.user.has_perms(perms)


class Dummy(models.Model):
    job_type = models.CharField(max_length=300, null=False)
    object_id = models.CharField(max_length=300, null=False)
    name = models.CharField(max_length=300, null=False, default="")
    slug = models.SlugField(null=True, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(User, null=False)
    deleted = models.BooleanField(default=False)

    class Meta(object):
        permissions = (
            ('view_task', 'View task'),
        )

    def generate_slug(self):
        if not self.slug:
            self.slug = slugify(str(self.name) + "-" + ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))

    def save(self, *args, **kwargs):
        self.generate_slug()
        super(Dummy, self).save(*args, **kwargs)


class DummySerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Dummy
        exclude = ( 'id', 'updated_at')


class DummyView(viewsets.ModelViewSet):

    def get_queryset(self):
        queryset = Dummy.objects.filter(
            created_by=self.request.user,
            deleted=False
        )
        return queryset

    def get_object_from_all(self):
        return Dummy.objects.get(slug=self.kwargs.get('slug'))

    serializer_class = DummySerializer
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend,)


    # multiple permission objects in permission_class will be calculated with 'OR'

    # permission_classes = (DummyPermissionTrue, DummyPermissionFalse)
    # permission_classes = (DummyPermission, )
    # permission_classes = (DummyPermissionGroup, )
    # permission_classes = (DummyPermissionUsingHasObject, )
    permission_classes = (DummyPermissionModelPermission, )
    models = Dummy

    def create(self, request, *args, **kwargs):
        data = request.data
        data['created_by'] = request.user.id

        seriali = DummySerializer(data=data)
        if seriali.is_valid():
            instance = seriali.save()
            return JsonResponse(seriali.data)


# @api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
# def example_view(request, format=None):
#     content = {
#         'status': 'request was permitted'
#     }
#     return Response(content)