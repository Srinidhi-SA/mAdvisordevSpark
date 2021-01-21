"""
Permissions module for OCRImage and OCRImageset models.
"""
from rest_framework import permissions


# -------------------------------------------------------------------------------
# pylint: disable=redefined-builtin
# pylint: disable=no-member
# pylint: disable=too-many-return-statements
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=inconsistent-return-statements
# pylint: disable=line-too-long
# -------------------------------------------------------------------------------

def get_permissions(user, model, type='retrieve'):
    """
    Defines the set of available permissions.
    """
    if model == 'ocrimage':
        if type == 'retrieve':
            return {
                'view_ocrimage': user.has_perm('ocr.view_ocrimage'),
                'rename_ocrimage': user.has_perm('ocr.rename_ocrimage'),
                'remove_ocrimage': user.has_perm('ocr.remove_ocrimage'),
                'create_ocrimage': user.has_perm('ocr.create_ocrimage'),
            }
        if type == 'list':
            return {
                'create_ocrimage': user.has_perm('ocr.create_ocrimage'),
                'view_ocrimage': user.has_perm('ocr.view_ocrimage'),
                'upload_from_file': user.has_perm('ocr.upload_from_file'),
                'upload_from_sftp': user.has_perm('ocr.upload_from_sftp'),
                'upload_from_s3': user.has_perm('ocr.upload_from_s3'),
            }

    return {}


class OCRImageRelatedPermission(permissions.BasePermission):
    """
    Class defining permissions for OCRImage model.
    """
    message = 'Permission for OCR.'

    def has_permission(self, request, view):
        user = request.user

        if request.method in ['GET']:
            return user.has_perm('ocr.view_ocr')

        if request.method in ['POST']:
            data = request.data
            datasource_type = data.get('datasource_type')
            if user.has_perm('ocr.create_ocr') and user.has_perm('ocr.view_ocr'):
                if datasource_type == 'fileUpload':
                    return user.has_perm('ocr.upload_from_file')
                if datasource_type == 'SFTP':
                    return user.has_perm('ocr.upload_from_sftp')
                if datasource_type == 'S3':
                    return user.has_perm('ocr.upload_from_s3')
                if datasource_type is None:
                    return user.has_perm('ocr.upload_from_file')

            return False

        if request.method in ['PUT']:
            data = request.data

            if 'deleted' in data:
                if data['deleted']:
                    return user.has_perm('ocr.remove_ocrimage')

            return user.has_perm('ocr.rename_ocrimage')

class IsOCRClientUser(permissions.BasePermission):
    """
    Allows access only to "ocr Admin role" users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Superuser').exists()
