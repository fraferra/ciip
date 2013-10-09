from django.db import models
from django import forms
from django.contrib.auth.models import User,UserManager, AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.db.models.signals import post_save
# Create your models here.
class UserProfile(models.Model):
    #user = models.OneToOneField(User)
    user=models.ForeignKey(User, unique=True)
    #user=models.CharField(max_length=20, null=True)
    first_name = models.CharField(max_length=20, null=True)
    last_name= models.CharField(max_length = 20, null=True)
    email = models.EmailField(null=True)
    file_cv = models.FileField(upload_to='cvs/%Y/%m/%d')
    file_name = models.CharField(max_length=50, null=True)
    UNIVERSITY_CHOICES = (
        ('UCL', 'UCL'),
        ('Kent', 'Kent'),
        ('EPFL', 'EPFL'),
    )
    university = models.CharField(max_length=20,
                                      choices=UNIVERSITY_CHOICES,
                                      default = 'UCL', null=True)
   
    STATUS_UPDATES = (
       ('In consideration', 'In consideration'),
       ('First Interview Scheduled','First Interview Scheduled'),
       ('First Interview Passed', 'First Interview Passed'),
       ('Interview with Manager Scheduled', 'Interview with Manager Scheduled'),
       ('On Hold', 'On Hold'),
      )
    status=models.CharField(max_length=100, choices= STATUS_UPDATES, default='In consideration', null=True)
    objects=UserManager()
 
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)


    def __unicode__(self):  # Python 3: def __str__(self):
        return self.last_name



