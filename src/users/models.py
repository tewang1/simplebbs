from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from mongoengine import (
    Document,
    EmbeddedDocument,
    IntField,
    URLField,
    ListField,
    EmailField,
    StringField,
    BooleanField,
    DateTimeField,
    ReferenceField,
    EmbeddedDocumentField,
    CASCADE,
    OperationError,
)

from utils.security import (
    Allow,
    Deny,
    EveryOne,
    Owner,
    Authenticated,
)


class User(Document):

    username = StringField(max_length=30, required=True, unique=True)
    password = StringField(max_length=100, required=True)
    email = EmailField(required=True, unique=True)
    avatar = URLField()
    groups = ListField(StringField(max_length=30), default=lambda: ['group:user'])
    is_confirm = BooleanField(required=True, default=False)
    is_active = BooleanField(required=True, default=True)
    joined_time = DateTimeField(default=timezone.now())
    last_login = DateTimeField()

    __object_name__ = 'User'
    __acl__ = [
        (Allow, EveryOne, 'add'),
        (Allow, Owner, 'change'),
        (Allow, 'group:admin', 'delete'),
    ]

    @classmethod
    def is_owner(cls, request, authenticated_username, slug=None, instance=None):
        if slug:
            return slug == authenticated_username
        if instance:
            return instance.username == authenticated_username
        return False

    @classmethod
    def create_user(cls, username, password, email):
        return cls(username=username, password=password, email=email)

    @classmethod
    def check_password(cls, username, password):
        if cls.objects(username=username, password=password).first():
            return True
        return False

    @classmethod
    def check_email(cls, username, email):
        if cls.objects(username=username, email=email):
            return True
        return False

    @classmethod
    def is_username_exist(cls, username):
        if cls.objects(username=username).first():
            return True
        return False

    @classmethod
    def is_email_exist(cls, email):
        if cls.objects(email=email).first():
            return True
        return False

    @classmethod
    def mail_to_user(cls, username, email, subject, message):
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

