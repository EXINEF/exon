from django.db.models.signals import post_save
from django.contrib.auth.models import Group

from .models import Teacher


def teacher_profile(sender, instance, created, **kwargs):
	if created:
		teacher_group = Group.objects.get(name='teacher')
		teacher_group.user_set.add(instance.user)


post_save.connect(teacher_profile, sender=Teacher)
