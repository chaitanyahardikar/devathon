# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from django.dispatch import receiver
# from .models import Profile

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
# 	name = kwargs.get('name',"default value")
# 	year = kwargs.get('year', 3)
# 	branch = kwargs.get('branch', '')
# 	image = kwargs.get('image', 'default.jpg')
	

# 	if created and not kwargs.get('raw', False):
# 		Profile.objects.create(user=instance, name=name, year=year, branch=branch, image=image)

# @receiver(post_save, sender=User)
# def save_profile(sender, instance, created, **kwargs):
# 	instance.profile.save()
