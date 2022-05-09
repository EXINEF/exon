from django.db.models.signals import post_save
from django.contrib.auth.models import Group

from .models import Teacher


"""
	SIGNALS allow to do automatic actions inside the wep app,
	in this case we use it to automaticaly insert the new Created Teacher,
	inside Teacher Group
"""

def teacher_profile(sender, instance, created, **kwargs):
	"""
		If a Teacher is created from the Admin Panel,
		it will be automaticaly inserted in Teacher Group
	"""
	if created:
		teacher_group = Group.objects.get(name='teacher')
		teacher_group.user_set.add(instance.user)


post_save.connect(teacher_profile, sender=Teacher)
