from django.db.models.signals import post_save
from django.dispatch import receiver
from tutor.models import LmsUser
import logging


logger = logging.getLogger('LMS')


@receiver(post_save, sender=LmsUser)
def user_registration(sender, instance, **kwargs):

	"""
		Send email on 
	"""

	logger.info("Email sent to user")