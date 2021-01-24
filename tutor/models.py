from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, email, password, first_name=None, last_name=None, role='1'):

        """
            Creates and saves a User with the given email and password.
        """

        if not email:
            raise ValueError('Users must have an email address')

        if not first_name:
            raise ValueError('Users must have an first name')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.role = role
        user.save()
        return user

    def create_superuser(self, email, password, first_name=None, last_name='', role='2'):

        """
            Create Mentor
        """

        user = self.create_user(email, password, first_name, last_name, role)
        return user


class LmsUser(AbstractUser):

    ROLE_CHOICES = (
        ('1', 'User'),
        ('2', 'Mentor'),
    )
    username = None
    email = models.EmailField(_('Eail Address'), unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default='1')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

    def __str__(self):
        return str(self.id) + "-" + self.email


def user_query_directory_path(instance, filename):
    return 'user_query_documents/{0}/image/{1}'.format(instance.id, filename)


class Question(models.Model):

    from_user = models.ForeignKey('tutor.LmsUser', on_delete=models.SET_NULL,
                                  null=True, related_name='from_user')
    to_mentor = models.ForeignKey('tutor.LmsUser', on_delete=models.SET_NULL,
                                  null=True, related_name="to_mentor")
    question_text = models.TextField()
    document = models.FileField(upload_to=user_query_directory_path,
                                null=True, blank=True)


class Answer(models.Model):

    question = models.ForeignKey('tutor.Question', on_delete=models.CASCADE)
    answer_text = models.TextField()
