"""
OCR Validations
"""

# -------------------------------------------------------------------------------
# pylint: disable=too-many-ancestors
# pylint: disable=no-member
# pylint: disable=too-many-return-statements
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=unused-argument
# pylint: disable=line-too-long
# pylint: disable=inconsistent-return-statements
# -------------------------------------------------------------------------------
import re
import socket
from django.core.exceptions import ValidationError
from django.http import JsonResponse

# -------------------------------------------------------------------------------


def validate_host(host):
    """
    Validate Hostname/IP Address
    """
    # Remove leading zeroes in hostname (if provided)
    new_ip = ".".join([str(int(i)) for i in host.split(".")])
    try:
        socket.inet_aton(new_ip)
        return True
    except socket.error:
        return False


# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------


def validate_port(port):
    """
    Validate SSH Port for SFTP
    """
    if port == 22:
        return True
    if port in range(1024, 65535):
        return True

# -------------------------------------------------------------------------------

# Validation for OCR Image file extension, max_file_size and no of attachments

# -------------------------------------------------------------------------------


VALID_EXTENSIONS = ['jpg', 'png', 'jpeg', 'tif', 'pdf']
VALIDATION_ERROR_MESSAGE = 'Unsupported file extension.'

def validate_image_dimension(imagefile):
    """ METHOD:  To Validate max and min Dimension for OCRImage model FileField"""
    import PIL
    max_height = 10000
    max_width = 10000
    min_height = 50
    min_width = 50
    image = PIL.Image.open(imagefile.file)

    width, height = image.size

    if width > max_width or height > max_height:
        return 1
    elif width < min_width or height < min_height:
        return 0

def max_file_size(value):
    """ METHOD : To Validate max file size for OCRImage model FileField. """
    limit = 20 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 20 MB.')


def max_num_files(value):
    """ METHOD : To Validate max number of file upload for OCRImage model FileField. """
    if len(value) > 100:
        raise ValidationError("Can't upload more than 100 files")

def validate_phone_number(phone):
    """ METHOD : To Validate mobile number for OCRUserProfile model."""
    rule = re.compile(r'^\+?1?\d{9,15}$')

    if rule.search(phone):
        msg = u"Invalid Phone number. Format +91-<10 Digit Phone-No>"
        raise ValidationError(msg)

# ---------------------------------------------------------------------------------
