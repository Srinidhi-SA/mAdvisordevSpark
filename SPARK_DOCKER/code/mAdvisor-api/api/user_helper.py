from __future__ import print_function
from builtins import str
from builtins import range
from builtins import object
from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer
# from rest_framework_jwt.views import ObtainJSONWebToken
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import request, response
import uuid
from django.conf import settings

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
import random
import string
from django.http import JsonResponse
from api.helper import encrypt_for_kylo
from ocr.models import OCRUserProfile


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', primary_key=True, on_delete=models.CASCADE)
    photo = models.FileField(
        upload_to="profiles",
        max_length=255,
        null=True,
        blank=True
    )
    website = models.URLField(default='', blank=True)
    bio = models.TextField(default='', blank=True)
    phone = models.CharField(max_length=20, blank=True, default='')
    city = models.CharField(max_length=100, default='', blank=True)
    country = models.CharField(max_length=100, default='', blank=True)
    organization = models.CharField(max_length=100, default='', blank=True)
    slug = models.SlugField(null=True, max_length=300)

    def generate_slug(self):
        if not self.slug:
            self.slug = slugify(str(self.user.username) + "-" + ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(30)))

    def save(self, *args, **kwargs):
        self.generate_slug()
        super(Profile, self).save(*args, **kwargs)

    def get_image_url(self):
        image_url = settings.IMAGE_URL
        if not self.slug:
            return None

        try:
            image = self.photo.path
        except:
            return None

        return image_url + self.slug + "/"

    def json_serialized(self):


        user_profile = {
            "image_url": self.get_image_url(),
            "website": self.website,
            "bio": self.bio,
            "phone": self.phone,
            "kylo_password": encrypt_for_kylo(self.user.username, self.user.password)
        }

        # user_profile.update(self.user)
        return user_profile


class UserProfileSerializer(serializers.Serializer):

    class Meta(object):
        model = Profile
        field = ('photo', 'website', 'bio', 'phone', 'city', 'country', 'organization')

    def create(self, validated_data):  #
        userprofile_data = validated_data.pop('userprofile')
        user = User.objects.create(**validated_data)  # Create the user object instance before store in the DB
        user.set_password(validated_data['password'])  # Hash to the Password of the user instance
        user.save()  # Save the Hashed Password
        Profile.objects.create(user=user, **userprofile_data)

        if settings.ENABLE_KYLO:
            create_or_update_kylo_auth_file()
        return user  # Return user object

    # def update(self, instance, validated_data):
    #     instance.photo = validated_data.get('image', instance.photo)
    #     instance.website = validated_data.get('website', instance.website)
    #     instance.phone = validated_data.get('phone', instance.phone)
    #
    #     instance.save()
    #     return instance

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.website = validated_data.get('website', instance.website)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.city = validated_data.get('city', instance.city)
        instance.country = validated_data.get('country', instance.country)
        instance.organization = validated_data.get('organization', instance.organization)
        return instance


    def to_representation(self, instance):
        ret = super(UserProfileSerializer, self).to_representation(instance)
        try:
            ret['photo'] = instance.photo.path
        except:
            ret['photo'] = ""

        return ret


# class UserProfileView(generics.CreateAPIView, generics.UpdateAPIView):
#     serializer_class = UserProfileSerializer
#     queryset = User.objects.all()
#     lookup_field = 'slug'



class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ("username", "first_name", "last_name", "email", "date_joined", "last_login", "is_superuser", "is_staff")


def jwt_response_payload_handler(token, user=None, request=None):

    # print user.date_joined - datetime.datetime.now(tz=)
    # if  (timezone.now() - user.date_joined).days > 30:
    #     return {
    #         'error': "Subscription expired."
    #     }
    from api.utils import get_all_view_permission

    profile = Profile.objects.filter(user=user).first()
    if profile is None:
        profile = Profile(user=user)
        profile.save()
    #Adding OCR Profile details
    OCR_profile = OCRUserProfile.objects.filter(ocr_user=user).first()
    if OCR_profile is None:
        pass

    return {
        'token': "JWT " + token,
        'user': UserSerializer(user, context={'request': request}).data,
        'profile': profile.json_serialized() if profile is not None else None,
        'ocr_profile': OCR_profile.json_serialized() if OCR_profile is not None else None,
        'view_permission': get_all_view_permission(user)
    }


def return_user_using_token(token=None):

    try:
        from rest_framework_jwt.serializers import VerificationBaseSerializer
        from rest_framework_jwt.settings import api_settings
        vbs = VerificationBaseSerializer()
        payload = vbs._check_payload(token=token)
        user = vbs._check_user(payload=payload)
        return user
    except:
        return False


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = Profile(user=user)

        ocr_user_profile = OCRUserProfile(ocr_user=user)
        ocr_user_profile.save()
        #Loading all customapps for the user
        ########################################
        # from api.views import all_apps_for_users
        # all_apps_for_users(user)
        ########################################
        user_profile.save()

    if settings.ENABLE_KYLO:
        create_or_update_kylo_auth_file()

post_save.connect(create_profile, sender=User)


from rest_framework import viewsets, generics
from rest_framework.response import Response

from rest_framework.decorators import api_view

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['PUT'])
def upload_photo(request):
    user = request.user


    other_details = request.POST
    print(other_details.get('website'))

    data = dict()

    obj = Profile.objects.filter(user=user).first()

    if obj is None:
        obj = Profile(user=user)
        obj.save()

    if 'image' in request.FILES:
        image = request.FILES.get('image')
        data['image'] = image
        obj.photo = image

    if 'website' in other_details:
        data['website'] = other_details.get('website')
        obj.website = data['website']

    if 'bio' in other_details:
        data['bio'] = other_details.get('bio')
        obj.bio = data['bio']

    if 'phone' in other_details:
        data['phone'] = other_details.get('phone')
        obj.phone = data['phone']

    obj.save()

    return Response(obj.json_serialized())


@csrf_exempt
def get_profile_image(request, slug=None):

    profile = Profile.objects.filter(slug=slug).first()
    if profile is None:
        return Response({'message': 'No Image. Upload an image.'})
    import magic
    from django.http import HttpResponse
    import os

    try:
        image = profile.photo
        image_buffer = open(
            name=image.path,
            mode="rb"
        ).read()
        content_type = magic.from_buffer(image_buffer, mime=True)
        response = HttpResponse(image_buffer, content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(image.path)
        return response
    except Exception as err:
        return JsonResponse({'message': 'No Image. Upload an image.'})



import jwt

from calendar import timegm
from datetime import datetime, timedelta

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework_jwt.compat import Serializer

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.compat import get_username_field, PasswordField


User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class myJSONWebTokenSerializer(Serializer):
    """
    Serializer class used to validate a username and password.

    'username' is identified by the custom UserModel.USERNAME_FIELD.

    Returns a JSON Web Token that can be used to authenticate later calls.
    """
    def __init__(self, *args, **kwargs):
        """
        Dynamically add the USERNAME_FIELD to self.fields.
        """
        super(myJSONWebTokenSerializer, self).__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField(write_only=True)

    @property
    def username_field(self):
        return get_username_field()

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)

                # Update last login time for the current user
                user.last_login = timezone.now()
                user.save()
                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = _('You have entered a wrong username or password. Please retry!')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)


def create_or_update_kylo_auth_file():
    print("create_or_update_kylo_auth_file")
    if settings.ENABLE_KYLO is False:
        return True
    KYLO_SERVER_DETAILS = settings.KYLO_SERVER_DETAILS
    group_propertie_quote = KYLO_SERVER_DETAILS['group_propertie_quote']
    user_properties = ""
    groups_properties = ""
    all_users = User.objects.all()
    for user in all_users:
        user_properties += "{0}={1}\n\n".format(user.username, encrypt_for_kylo(user.username, user.password))
        groups_properties += "{0}={1}\n\n".format(user.username, group_propertie_quote)

    #add dladmin and default users of kylo
    user_properties +="dladmin=thinkbig"
    groups_properties += "dladmin=admin,user\n\nanalyst=analyst,user\n\ndesigner=designer,user\n\noperator=operations,user"


    with open('/tmp/users.properties', 'w') as fp:
        fp.write(user_properties)

    with open('/tmp/groups.properties', 'w') as fp:
        fp.write(groups_properties)

    ssh_command_users = "scp -i {0} /tmp/users.properties {1}@{2}:{3}".format(
        KYLO_SERVER_DETAILS['key_path'],
        KYLO_SERVER_DETAILS['user'],
        KYLO_SERVER_DETAILS['host'],
        KYLO_SERVER_DETAILS['kylo_file_path'],
    )

    ssh_command_groups = "scp -i {0} /tmp/groups.properties {1}@{2}:{3}".format(
        KYLO_SERVER_DETAILS['key_path'],
        KYLO_SERVER_DETAILS['user'],
        KYLO_SERVER_DETAILS['host'],
        KYLO_SERVER_DETAILS['kylo_file_path'],
    )

    print(ssh_command_users.split(' '))
    import subprocess
    subprocess.call(ssh_command_users.split(' '))
    subprocess.call(ssh_command_groups.split(' '))

    #call kylo api from admin user to create user from config group
    user=User.objects.last()
    grps=["madvisor"]
    displayName=user.first_name+" "+user.last_name
    user_data={"displayName": user.username,"email": user.email,"enabled": True,"groups":grps,"systemName": user.username}
    print("user_data: ")
    print(user_data)
    import json
    import requests
    import uuid
    import time
    user_data=json.dumps(user_data)
    print("user data after dump: ")
    print(user_data)
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    settings.KYLO_UI_URL
    url = settings.KYLO_UI_URL + "/proxy/v1/security/users"
    r=requests.post(url,data=user_data,auth=('dladmin','thinkbig'),headers=headers)
    print("response from kylo: ")
    print(r.text)
    #add personal category with Permissions
    cat_url = settings.KYLO_UI_URL + "/proxy/v1/feedmgr/categories"
    id=str(uuid.uuid4())
    millis = int(round(time.time() * 1000))
    print(millis)
    createDate=millis
    updateDate=millis
    cat_id=str(uuid.uuid4())
    owner=KYLO_OWNER
    allowedActions=KYLO_ALLOWED_ACTIONS
    feedRoleMemberships=KYLO_FEED_ROLE_MEMBERSHIPS
    roleMemberships=KYLO_ROLE_MEMBERSHIPS
    #cat_data=KYLO_CREATE_CATEGORY_TEMPLATE
    allowed_roles=["editor","feedCreator"]
    allowed_feed_roles=["editor","admin"]
    members=[{    "displayName": user.username,
                  "email": user.email,
                  "enabled": True,
                  "groups": ["madvisor"],
                  "systemName": user.username,
                  "name": user.username,
                  "title": user.username,
                  "type": "user",
                  "_lowername": user.username,
                  "_lowerSystemName":user.username,
                  "_lowerDisplayName": user.username
                }]

    for role in roleMemberships:
        if role["role"]["systemName"] in allowed_roles:
            role["users"]=[user.username]
            role["members"]=members
    for role in feedRoleMemberships:
        if role["role"]["systemName"] in allowed_feed_roles:
            role["users"]=[user.username]
            role["members"]=members

    cat_name=user.username+"_cat"
    cat_desc="for "+user.username+ " only"


    cat_data={
      "owner": owner,
      "allowedActions": allowedActions,
      "roleMemberships": roleMemberships,
      "feedRoleMemberships": feedRoleMemberships,
      "id": cat_id,
      "name": cat_name,
      "systemName": cat_name,
      "icon": "account_circle",
      "iconColor": "#80CBC4",
      "description": cat_desc,
      "allowIndexing": True,
      "securityGroups": [],
      "userFields": [],
      "userProperties": [],
      "relatedFeeds": 0,
      "createDate": createDate,
      "updateDate": updateDate,
      "_lowername": cat_name,
      "createFeed": True,
      "roleMembershipsUpdated": False
    }
    r=requests.post(cat_url,data=json.dumps(cat_data),auth=('dladmin','thinkbig'),headers=headers)
    print("rs from create/update category of kylo")
    print(r.text)



#for kylo category creation
## there will be two post calls
#kylo_cat_call1_template={"id":None,"name":"user1_cat","description":"for user 1 only","icon":"account_circle","iconColor":"#80CBC4","userFields":[],"userProperties":[],"relatedFeedSummaries":[],"securityGroups":[],"roleMemberships":[],"feedRoleMemberships":[],"owner":None,"allowIndexing":True,"systemName":"user1_cat"}

KYLO_ALLOWED_ACTIONS= {
        "actions": [{
          "systemName": "accessCategory",
          "actions": [{
            "systemName": "editCategorySummary"
          }, {
            "systemName": "accessCategoryDetails",
            "actions": [{
              "systemName": "editCategoryDetails"
            }, {
              "systemName": "deleteCategory"
            }]
          }, {
            "systemName": "createFeedUnderCategory"
          }, {
            "systemName": "changeCategoryPermissions"
          }]
        }]
}

KYLO_FEED_ROLE_MEMBERSHIPS= [{
"role": {
  "systemName": "editor",
  "title": "Editor",
  "description": "Allows a user to edit, enable/disable, start, delete and export feed. Allows access to job operations for feed. If role inherited via a category, allows these operations for feeds under that category.",
  "allowedActions": {
    "actions": [{
      "systemName": "accessFeed",
      "actions": [{
        "systemName": "accessFeedDetails",
        "actions": [{
          "systemName": "editFeedDetails",
          "title": "Edit Details",
          "description": "Allows editing of the details about the feed"
        }, {
          "systemName": "deleteFeed",
          "title": "Delete",
          "description": "Allows deleting the feed"
        }, {
          "systemName": "enableFeed",
          "title": "Enable/Disable",
          "description": "Allows enabling and disabling the feed"
        }, {
          "systemName": "startFeed",
          "title": "Start Feed",
          "description": "Allows manually triggering the start of a feed"
        }, {
          "systemName": "exportFeed",
          "title": "Export",
          "description": "Allows exporting the feed"
        }]
      }, {
        "systemName": "accessFeedOperations",
        "title": "Access Operations",
        "description": "Allows the ability to see the operational history of the feed"
      }]
    }]
  }
},
"users": ["user2"],
"groups": [],
"ui": {
  "members": {
    "selectedItem": None,
    "searchText": ""
  }
},
"members": [{
  "displayName": "user2",
  "email": "",
  "enabled": True,
  "groups": ["madvisor"],
  "systemName": "user2",
  "name": "user2",
  "title": "user2",
  "type": "user",
  "_lowername": "user2",
  "_lowerSystemName": "user2",
  "_lowerDisplayName": "user2"
}]
}, {
"role": {
  "systemName": "admin",
  "title": "Admin",
  "description": "All capabilities defined in the 'Editor' role along with the ability to change the permissions",
  "allowedActions": {
    "actions": [{
      "systemName": "accessFeed",
      "actions": [{
        "systemName": "accessFeedDetails",
        "actions": [{
          "systemName": "editFeedDetails",
          "title": "Edit Details",
          "description": "Allows editing of the details about the feed"
        }, {
          "systemName": "deleteFeed",
          "title": "Delete",
          "description": "Allows deleting the feed"
        }, {
          "systemName": "enableFeed",
          "title": "Enable/Disable",
          "description": "Allows enabling and disabling the feed"
        }, {
          "systemName": "startFeed",
          "title": "Start Feed",
          "description": "Allows manually triggering the start of a feed"
        }, {
          "systemName": "exportFeed",
          "title": "Export",
          "description": "Allows exporting the feed"
        }]
      }, {
        "systemName": "accessFeedOperations",
        "title": "Access Operations",
        "description": "Allows the ability to see the operational history of the feed"
      }, {
        "systemName": "changeFeedPermissions",
        "title": "Change Permissions",
        "description": "Allows editing of the permissions that grant access to the feed"
      }]
    }]
  }
},
"users": ["user2"],
"groups": [],
"ui": {
  "members": {
    "selectedItem": None,
    "searchText": ""
  }
},
"members": [{
  "displayName": "user2",
  "email": "",
  "enabled": True,
  "groups": ["madvisor"],
  "systemName": "user2",
  "name": "user2",
  "title": "user2",
  "type": "user",
  "_lowername": "user2",
  "_lowerSystemName": "user2",
  "_lowerDisplayName": "user2"
}]
}, {
"role": {
  "systemName": "readOnly",
  "title": "Read-Only",
  "description": "Allows a user to view the feed and access job operations",
  "allowedActions": {
    "actions": [{
      "systemName": "accessFeed",
      "actions": [{
        "systemName": "accessFeedDetails",
        "title": "Access Details",
        "description": "Allows viewing the full details about the feed"
      }, {
        "systemName": "accessFeedOperations",
        "title": "Access Operations",
        "description": "Allows the ability to see the operational history of the feed"
      }]
    }]
  }
},
"users": [],
"groups": [],
"ui": {
  "members": {
    "selectedItem": "",
    "searchText": ""
  }
},
"members": []
}]

KYLO_OWNER={
"displayName": "Data Lake Administrator",
"email": None,
"enabled": True,
"groups": ["admin", "user"],
"systemName": "dladmin"
}

KYLO_ROLE_MEMBERSHIPS= [{
    "role": {
      "systemName": "editor",
      "title": "Editor",
      "description": "Allows a user to edit, export and delete category. Allows creating feeds under the category",
      "allowedActions": {
        "actions": [{
          "systemName": "accessCategory",
          "title": "Access Category",
          "description": "Allows the ability to view the category and see basic summary information about it",
          "actions": [{
            "systemName": "accessCategoryDetails",
            "actions": [{
              "systemName": "editCategoryDetails",
              "title": "Edit Details",
              "description": "Allows editing of the details about the category"
            }, {
              "systemName": "deleteCategory",
              "title": "Delete",
              "description": "Allows deleting the category"
            }]
          }, {
            "systemName": "editCategorySummary",
            "title": "Edit Summary",
            "description": "Allows editing of the summary information about the category"
          }, {
            "systemName": "createFeedUnderCategory",
            "title": "Create Feed under Category",
            "description": "Allows creating feeds under this category"
          }]
        }]
      }
    },
    "users": ["user1"],
    "groups": [],
    "ui": {
      "members": {
        "selectedItem": None,
        "searchText": ""
      }
    },
    "members": [{
      "displayName": "user1",
      "email": "",
      "enabled": True,
      "groups": ["madvisor"],
      "systemName": "user1",
      "name": "user1",
      "title": "user1",
      "type": "user",
      "_lowername": "user1",
      "_lowerSystemName": "user1",
      "_lowerDisplayName": "user1"
    }]
  }, {
    "role": {
      "systemName": "admin",
      "title": "Admin",
      "description": "All capabilities defined in the 'Editor' role along with the ability to change the permissions",
      "allowedActions": {
        "actions": [{
          "systemName": "accessCategory",
          "title": "Access Category",
          "description": "Allows the ability to view the category and see basic summary information about it",
          "actions": [{
            "systemName": "accessCategoryDetails",
            "actions": [{
              "systemName": "editCategoryDetails",
              "title": "Edit Details",
              "description": "Allows editing of the details about the category"
            }, {
              "systemName": "deleteCategory",
              "title": "Delete",
              "description": "Allows deleting the category"
            }]
          }, {
            "systemName": "editCategorySummary",
            "title": "Edit Summary",
            "description": "Allows editing of the summary information about the category"
          }, {
            "systemName": "createFeedUnderCategory",
            "title": "Create Feed under Category",
            "description": "Allows creating feeds under this category"
          }, {
            "systemName": "changeCategoryPermissions",
            "title": "Change Permissions",
            "description": "Allows editing of the permissions that grant access to the category"
          }]
        }]
      }
    },
    "users": [],
    "groups": [],
    "ui": {
      "members": {
        "selectedItem": "",
        "searchText": ""
      }
    },
    "members": []
  }, {
    "role": {
      "systemName": "readOnly",
      "title": "Read-Only",
      "description": "Allows a user to view the category",
      "allowedActions": {
        "actions": [{
          "systemName": "accessCategory",
          "title": "Access Category",
          "description": "Allows the ability to view the category and see basic summary information about it"
        }]
      }
    },
    "users": [],
    "groups": [],
    "ui": {
      "members": {
        "selectedItem": "",
        "searchText": ""
      }
    },
    "members": []
  }, {
    "role": {
      "systemName": "feedCreator",
      "title": "Feed Creator",
      "description": "Allows a user to create a new feed using this category",
      "allowedActions": {
        "actions": [{
          "systemName": "accessCategory",
          "actions": [{
            "systemName": "accessCategoryDetails",
            "title": "Access Details",
            "description": "Allows viewing the full details about the category"
          }, {
            "systemName": "createFeedUnderCategory",
            "title": "Create Feed under Category",
            "description": "Allows creating feeds under this category"
          }]
        }]
      }
    },
    "users": ["user1"],
    "groups": [],
    "ui": {
      "members": {
        "selectedItem": None,
        "searchText": ""
      }
    },
    "members": [{
      "displayName": "user1",
      "email": "",
      "enabled": True,
      "groups": ["madvisor"],
      "systemName": "user1",
      "name": "user1",
      "title": "user1",
      "type": "user",
      "_lowername": "user1",
      "_lowerSystemName": "user1",
      "_lowerDisplayName": "user1"
    }]
  }]

KYLO_CREATE_CATEGORY_TEMPLATE={
  "owner": KYLO_OWNER,
  "allowedActions": KYLO_ALLOWED_ACTIONS,
  "roleMemberships": KYLO_ROLE_MEMBERSHIPS,
  "feedRoleMemberships": KYLO_FEED_ROLE_MEMBERSHIPS,
  "id": "fa893dda-5522-45a0-95d5-640bcf4797aa",
  "name": "user1_cat",
  "systemName": "user1_cat",
  "icon": "account_circle",
  "iconColor": "#80CBC4",
  "description": "for user 1 only",
  "allowIndexing": True,
  "securityGroups": [],
  "userFields": [],
  "userProperties": [],
  "relatedFeeds": 0,
  "createDate": 1530868419727,
  "updateDate": 1530868419727,
  "_lowername": "user1_cat",
  "createFeed": True,
  "roleMembershipsUpdated": False
}
