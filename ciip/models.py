from django.db import models
from datetime import date
from django import forms
from django.contrib.auth.models import User,UserManager
from django.utils import timezone
from django.db.models.signals import post_save
import constants
from django.utils.translation import ugettext as _


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        #current_pk = request.user.pk
        #usertype = User.objects.get(pk=current_pk).usertype
        #usertype=ciip.views.usertype.profile
        try:
            user_type = instance.user_type
            if user_type == "University Admin": 
            #UniversityAdmin(user = instance).save()
                UniversityAdmin.objects.create(user=instance)   
            else:
            #UserProfile(user = instance).save()
                UserProfile.objects.create(user=instance) 
        except AttributeError:
            pass 

class Profile(models.Model):
    user=models.ForeignKey(User, unique=True)
    #first_name = models.CharField(max_length=20, null=True)
    #last_name= models.CharField(max_length = 20, null=True)
    #university=models.ForeignKey(University, null=False)

    class Meta:
        abstract = True


# Create your models here.

post_save.connect(create_user_profile, sender=User)
class ManagerProfile(Profile):
    coordinator=models.CharField(max_length=3, choices=constants.COORDINATOR, default='No', null=True)
    business_unit=models.CharField(max_length=100, choices=constants.PROJECTS, default=None ,null=True)
    first_name = models.CharField(max_length=20, null=True)
    last_name= models.CharField(max_length = 20, null=True)
    skill_1=models.CharField(max_length=60, null=True)
    skill_2=models.CharField(max_length=60, null=True)
    skill_3=models.CharField(max_length=60, null=True)
    interest_1=models.CharField(max_length=60, null=True)
    interest_2=models.CharField(max_length=60, null=True)
    interest_3=models.CharField(max_length=60, null=True)
    work_description=models.TextField(max_length=1000, null=True)

    job_title=models.CharField(max_length=50, null=True, default=None)
    degree=models.CharField(max_length=50, null=True, default=None)
    field=models.CharField(max_length=50, null=True, default=None)
    group=models.CharField(max_length=50, null=True, default=None)
    year_experience=models.CharField(max_length=20, null=True, default=None)
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.last_name) or u''



class UserProfile(Profile):
    #user = models.OneToOneField(User)
    #user=models.ForeignKey(User, unique=True)
    #user=models.CharField(max_length=20, null=True)

    # profile = models.ForeignKey('Profile')
    technical_resume_screen_selection =models.CharField(max_length=30, choices=constants.MANAGER_ENDORSEMENT,default='---', null=True)
    technical_resume_screen_comment=models.TextField(max_length=1000, null=True)
    technical_interview_screen_selection=models.CharField(max_length=30, choices=constants.MANAGER_ENDORSEMENT,default='---', null=True)
    technical_interview_screen_comment=models.TextField(max_length=1000, null=True)
    master_or_undergrad=models.CharField(max_length=30, choices=constants.MASTER_UNDER,default='---', null=True)
    university_endorsement=models.CharField(max_length=20, choices=constants.UNIVERSITY_ENDORSEMENT, null=True)

    university_role=models.CharField(max_length=100, choices= constants.UNIVERSITY_ROLE,  null=True)
    university_role_name=models.CharField(max_length=100, null=True)


    status=models.CharField(max_length=100, choices= constants.STATUS_UPDATES, default='In consideration', null=True)
    

    INTERVIEW_RESPONSE=(
       ('Tutor', 'Tutor'),
       ('Mentor','Mentor'),
       ('University Professor', 'University Professor'),
       ('Employeer', 'Employeer'),
      )
    webex_link = models.TextField(max_length=200, null=True)
    date_interview = models.DateTimeField( null=True)
    interview_response = models.CharField(max_length=100,
                                            default=None, null=True)
    OPTION=(
        ('Yes','Yes'),
        ('No','No')
        )
    leadership=models.CharField(max_length=3, null=True, default=None, choices=OPTION)
    initiative=models.CharField(max_length=3, null=True, default=None, choices=OPTION)
    innovation=models.CharField(max_length=3, null=True, default=None, choices=OPTION)
    adaptability=models.CharField(max_length=3, null=True, default=None, choices=OPTION)
    team_player=models.CharField(max_length=3, null=True, default=None, choices=OPTION)
    cisco_fit=models.CharField(max_length=3, null=True, default=None, choices=OPTION)
    technical_skill=models.CharField(max_length=3, null=True, default=None, choices=OPTION)
    motivation=models.CharField(max_length=3, null=True, default=None, choices=OPTION)
    interviewer_comment = models.TextField(max_length=1000, null=True, default=None)
    interviewer_name = models.CharField(max_length=100, null=True, default=None)
    position_suggested = models.CharField(max_length=100, null=True, choices=constants.PROJECTS, default=None)


    gender=models.CharField(max_length=6, choices=constants.GENDER, default='male', null=True)
   

    good_university=models.CharField(max_length=3, choices=constants.PASSPORT, default='Yes',null=True)
    passport=models.CharField(max_length=3, choices=constants.PASSPORT, default='Yes',null=True)
    birth_date_day=models.CharField(max_length=2, null=True)
    birth_date_month=models.CharField(max_length=2,null=True)
    birth_date_year=models.CharField(max_length=4,null=True)

    birth_date = models.DateField(_("Date"), default=date.today)


    first_name = models.CharField(max_length=20, null=True)
    last_name= models.CharField(max_length = 20, null=True)
    email = models.EmailField(null=True)
    phone=models.CharField(max_length=20, null=True, help_text="example: +44 7403 123456 ")
    #phone = models.DecimalField(max_digits=15, decimal_places=0, null=True)
    address_line1= models.CharField(max_length=100, null=True)
    address_line2=models.CharField(max_length=60, null=True)
    city=models.CharField(max_length=60, null=True)
    zip_code= models.CharField(max_length=20, null=True)

    passport_number=models.CharField(max_length=20, null=True)
    country_issued=models.CharField(max_length=2, choices=constants.COUNTRIES,
                             default='ZZ', null=True)

    date_issued=models.DateField(_("Date"), default=date.today)

    date_expiration=models.DateField(_("Date"), default=date.today)

# http://xml.coverpages.org/country3166.html


    country=models.CharField(max_length=2, choices=constants.COUNTRIES,
                             default='ZZ', null=True)

    objects=UserManager()
 

    full_name_emergency=models.CharField(max_length=100, null=True)
    relationship = models.CharField(max_length=60, null=True)
    phone_emergency=models.CharField(max_length=20, null=True, help_text="example: +44 7403 123456 ")
    email_emergency = models.EmailField(null=True)

    experience_1=models.TextField(max_length=1000, null=True)
    experience_2=models.TextField(max_length=1000, null=True)
    internship_1=models.TextField(max_length=1000, null=True)
    internship_2=models.TextField(max_length=1000, null=True)

    cover_letter=models.FileField(upload_to='media/%Y/%m/%d')



    university = models.CharField(max_length=20,
                                      choices=constants.UNIVERSITY_CHOICES,
                                      default = 'UCL', null=True)

    year_of_graduation=models.CharField(max_length=4, choices=constants.YEAR_OF_GRADUATION, default='2014', null=True)
    #year_of_graduation=models.DateField(auto_now=False, auto_now_add=False)
    degree=models.CharField(max_length=60, null=True)
    average=models.CharField(max_length=2, null=True)
    #average=models.DecimalField(max_digits=2, decimal_places=0, null=True)

    skill_1=models.CharField(max_length=60, null=True)
    skill_level_1=models.CharField(max_length=30,
                                       choices=constants.SKILL_LEVEL,
                                       default='None', null=True)
    skill_2=models.CharField(max_length=60, null=True)
    skill_level_2=models.CharField(max_length=30,
                                       choices=constants.SKILL_LEVEL,
                                       default='None', null=True)
    skill_3=models.CharField(max_length=60, null=True)
    skill_level_3=models.CharField(max_length=30,
                                       choices=constants.SKILL_LEVEL,
                                       default='None', null=True)
    interest_1=models.CharField(max_length=60, null=True)
    interest_2=models.CharField(max_length=60, null=True)
    interest_3=models.CharField(max_length=60, null=True)



    question_1=models.TextField(max_length=1000, null=True)
    question_2=models.TextField(max_length=1000, null=True)
    question_3=models.TextField(max_length=1000, null=True)
    #question_4=models.TextField(max_length=1000, null=True)

    uni_comment = models.TextField(max_length=500, null=True)
    
    file_cv = models.FileField(upload_to='media/%Y/%m/%d')
    file_name = models.CharField(max_length=50, null=True)
    offer_states=models.CharField(max_length=50, default=None,  null=True)
    manager_comment=models.TextField(max_length=1000, null=True, default=None)

    listed=models.TextField(max_length=50, choices=constants.LISTED, default='yes', null=True)


    #image = models.ImageField(upload_to='images/%Y/%m/%d')


    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.last_name) or u''
    






class UniversityAdmin(Profile):
    university = models.CharField(max_length=20,
                                      choices=constants.UNIVERSITY_CHOICES,
                                      default = 'UCL', null=True)
    first_name = models.CharField(max_length=20, null=True)
    last_name= models.CharField(max_length = 20, null=True)
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.first_name) or u''








class Interview(models.Model):
    date= models.DateTimeField( null=True)
    student=models.ForeignKey(UserProfile)
    manager=models.ForeignKey(ManagerProfile)
    delegated_to=models.ForeignKey(ManagerProfile, related_name='delegates', null=True, default=None)
    skype_name=models.CharField(max_length=100, null=True, default=None)
    interview_response = models.CharField(max_length=100,
                                            default=None, null=True)
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.manager) or u''


class Message(models.Model):
    text=models.TextField(max_length=1000, null=True)
    student=models.ForeignKey(UserProfile)
    manager=models.ForeignKey(ManagerProfile)
    sent_by=models.CharField(max_length=50, null=True)
    date_sent=models.DateTimeField( null=True)
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.student) or u''


class Search(models.Model):
    manager=models.ForeignKey(ManagerProfile)
    search=models.CharField(max_length=100, null=True, default=None)
    ranking=models.CharField(max_length=100, null=True, default=None)
    offer_status=models.CharField(max_length=100, null=True, default=None)
    university=models.CharField(max_length=100, null=True, default=None)
    date=models.DateTimeField( null=True)







