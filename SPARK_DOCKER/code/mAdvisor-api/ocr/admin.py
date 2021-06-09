"""
OCR AdminSite Settings
"""
from django.contrib import admin

# Register your models here.
from ocr.models import OCRImage, OCRImageset, OCRUserProfile, Template, Project

# -------------------------------------------------------------------------------
# pylint: disable=too-few-public-methods
# pylint: disable=no-member
# pylint: disable=too-many-return-statements
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=unused-argument
# pylint: disable=line-too-long
# -------------------------------------------------------------------------------


class OCRImageAdmin(admin.ModelAdmin):
    """
    Model: OCRImage
    """
    icon = '<i class="material-icons">cloud_done</i>'
    search_fields = ["name", "slug"]
    list_display = ["name", "slug", "status", "created_by", "assignee", "deleted"]
    list_filter = ["status", "deleted", "created_by", 'is_L1assigned', 'is_L2assigned', 'is_recognized']
    readonly_fields = ["created_at", "created_by", "slug", "imageset", 'modified_at']

    def get_queryset(self, request):
        queryset = super(OCRImageAdmin, self).get_queryset(request)
        queryset = queryset.order_by('-created_at')
        return queryset


class OCRImagesetAdmin(admin.ModelAdmin):
    """
    Model: OCRImageset
    """
    icon = '<i class="material-icons">cloud_done</i>'
    search_fields = ["name"]
    list_display = ["name", "status", "created_by"]
    list_filter = ["status", "created_by"]
    readonly_fields = ["slug", "imagepath", "created_by"]

    def get_queryset(self, request):
        queryset = super(OCRImagesetAdmin, self).get_queryset(request)
        queryset = queryset.order_by('-created_at')
        return queryset

class OCRUserProfileAdmin(admin.ModelAdmin):
    """
    Model: OCRUserProfile
    """
    icon = '<i class="material-icons">cloud_done</i>'
    search_fields = ["slug"]
    list_display = ["slug", "is_active"]
    list_filter = ["is_active"]
    readonly_fields = ["slug"]

    def get_queryset(self, request):
        queryset = super(OCRUserProfileAdmin, self).get_queryset(request)
        #queryset = queryset.order_by('-created_at')
        return queryset

class TemplateAdmin(admin.ModelAdmin):
    """
    Model: Template
    """
    icon = '<i class="material-icons">cloud_done</i>'
    #search_fields = ["slug"]
    list_display = ["id", "template_classification", "modified_at"]
    #list_filter = ["is_active"]
    #readonly_fields = ["slug"]

    def get_queryset(self, request):
        queryset = super(TemplateAdmin, self).get_queryset(request)
        #queryset = queryset.order_by('-created_at')
        return queryset

class ProjectAdmin(admin.ModelAdmin):
    """
    Model: Project
    """
    icon = '<i class="material-icons">cloud_done</i>'
    search_fields = ["slug", "name"]
    list_display = ["name", "slug", "deleted"]
    #list_filter = ["slug", "name"]
    readonly_fields = ["slug"]

    def get_queryset(self, request):
        queryset = super(ProjectAdmin, self).get_queryset(request)
        queryset = queryset.order_by('-created_at')
        return queryset


admin.site.register(OCRImage, OCRImageAdmin)
admin.site.register(OCRImageset, OCRImagesetAdmin)
admin.site.register(OCRUserProfile, OCRUserProfileAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(Project, ProjectAdmin)
