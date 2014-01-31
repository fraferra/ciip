from django.db import models
from datetime import date
from django import forms
from django.contrib.auth.models import User,UserManager, AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.db.models.signals import post_save

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
            UserProfile.objects.create(user=instance) 

class Profile(models.Model):
    user=models.ForeignKey(User, unique=True)
    #first_name = models.CharField(max_length=20, null=True)
    #last_name= models.CharField(max_length = 20, null=True)
    #university=models.ForeignKey(University, null=False)

    class Meta:
        abstract = True


# Create your models here.

post_save.connect(create_user_profile, sender=User)


class UserProfile(Profile):
    #user = models.OneToOneField(User)
    #user=models.ForeignKey(User, unique=True)
    #user=models.CharField(max_length=20, null=True)

    # profile = models.ForeignKey('Profile')

    COUNTRIES = (
    ('AD', _('Andorra')),
    ('AE', _('United Arab Emirates')),
    ('AF', _('Afghanistan')),
    ('AG', _('Antigua & Barbuda')),
    ('AI', _('Anguilla')),
    ('AL', _('Albania')),
    ('AM', _('Armenia')),
    ('AN', _('Netherlands Antilles')),
    ('AO', _('Angola')),
    ('AQ', _('Antarctica')),
    ('AR', _('Argentina')),
    ('AS', _('American Samoa')),
    ('AT', _('Austria')),
    ('AU', _('Australia')),
    ('AW', _('Aruba')),
    ('AZ', _('Azerbaijan')),
    ('BA', _('Bosnia and Herzegovina')),
    ('BB', _('Barbados')),
    ('BD', _('Bangladesh')),
    ('BE', _('Belgium')),
    ('BF', _('Burkina Faso')),
    ('BG', _('Bulgaria')),
    ('BH', _('Bahrain')),
    ('BI', _('Burundi')),
    ('BJ', _('Benin')),
    ('BM', _('Bermuda')),
    ('BN', _('Brunei Darussalam')),
    ('BO', _('Bolivia')),
    ('BR', _('Brazil')),
    ('BS', _('Bahama')),
    ('BT', _('Bhutan')),
    ('BV', _('Bouvet Island')),
    ('BW', _('Botswana')),
    ('BY', _('Belarus')),
    ('BZ', _('Belize')),
    ('CA', _('Canada')),
    ('CC', _('Cocos (Keeling) Islands')),
    ('CF', _('Central African Republic')),
    ('CG', _('Congo')),
    ('CH', _('Switzerland')),
    ('CI', _('Ivory Coast')),
    ('CK', _('Cook Iislands')),
    ('CL', _('Chile')),
    ('CM', _('Cameroon')),
    ('CN', _('China')),
    ('CO', _('Colombia')),
    ('CR', _('Costa Rica')),
    ('CU', _('Cuba')),
    ('CV', _('Cape Verde')),
    ('CX', _('Christmas Island')),
    ('CY', _('Cyprus')),
    ('CZ', _('Czech Republic')),
    ('DE', _('Germany')),
    ('DJ', _('Djibouti')),
    ('DK', _('Denmark')),
    ('DM', _('Dominica')),
    ('DO', _('Dominican Republic')),
    ('DZ', _('Algeria')),
    ('EC', _('Ecuador')),
    ('EE', _('Estonia')),
    ('EG', _('Egypt')),
    ('EH', _('Western Sahara')),
    ('ER', _('Eritrea')),
    ('ES', _('Spain')),
    ('ET', _('Ethiopia')),
    ('FI', _('Finland')),
    ('FJ', _('Fiji')),
    ('FK', _('Falkland Islands (Malvinas)')),
    ('FM', _('Micronesia')),
    ('FO', _('Faroe Islands')),
    ('FR', _('France')),
    ('FX', _('France, Metropolitan')),
    ('GA', _('Gabon')),
    ('GB', _('United Kingdom (Great Britain)')),
    ('GD', _('Grenada')),
    ('GE', _('Georgia')),
    ('GF', _('French Guiana')),
    ('GH', _('Ghana')),
    ('GI', _('Gibraltar')),
    ('GL', _('Greenland')),
    ('GM', _('Gambia')),
    ('GN', _('Guinea')),
    ('GP', _('Guadeloupe')),
    ('GQ', _('Equatorial Guinea')),
    ('GR', _('Greece')),
    ('GS', _('South Georgia and the South Sandwich Islands')),
    ('GT', _('Guatemala')),
    ('GU', _('Guam')),
    ('GW', _('Guinea-Bissau')),
    ('GY', _('Guyana')),
    ('HK', _('Hong Kong')),
    ('HM', _('Heard & McDonald Islands')),
    ('HN', _('Honduras')),
    ('HR', _('Croatia')),
    ('HT', _('Haiti')),
    ('HU', _('Hungary')),
    ('ID', _('Indonesia')),
    ('IE', _('Ireland')),
    ('IL', _('Israel')),
    ('IN', _('India')),
    ('IO', _('British Indian Ocean Territory')),
    ('IQ', _('Iraq')),
    ('IR', _('Islamic Republic of Iran')),
    ('IS', _('Iceland')),
    ('IT', _('Italy')),
    ('JM', _('Jamaica')),
    ('JO', _('Jordan')),
    ('JP', _('Japan')),
    ('KE', _('Kenya')),
    ('KG', _('Kyrgyzstan')),
    ('KH', _('Cambodia')),
    ('KI', _('Kiribati')),
    ('KM', _('Comoros')),
    ('KN', _('St. Kitts and Nevis')),
    ('KP', _('Korea, Democratic People\'s Republic of')),
    ('KR', _('Korea, Republic of')),
    ('KW', _('Kuwait')),
    ('KY', _('Cayman Islands')),
    ('KZ', _('Kazakhstan')),
    ('KS', _('Kosovo')),
    ('LA', _('Lao People\'s Democratic Republic')),
    ('LB', _('Lebanon')),
    ('LC', _('Saint Lucia')),
    ('LI', _('Liechtenstein')),
    ('LK', _('Sri Lanka')),
    ('LR', _('Liberia')),
    ('LS', _('Lesotho')),
    ('LT', _('Lithuania')),
    ('LU', _('Luxembourg')),
    ('LV', _('Latvia')),
    ('LY', _('Libyan Arab Jamahiriya')),
    ('MA', _('Morocco')),
    ('MC', _('Monaco')),
    ('MD', _('Moldova, Republic of')),
    ('MG', _('Madagascar')),
    ('MH', _('Marshall Islands')),
    ('ML', _('Mali')),
    ('MN', _('Mongolia')),
    ('MM', _('Myanmar')),
    ('MO', _('Macau')),
    ('MP', _('Northern Mariana Islands')),
    ('MQ', _('Martinique')),
    ('MR', _('Mauritania')),
    ('MS', _('Monserrat')),
    ('MT', _('Malta')),
    ('MU', _('Mauritius')),
    ('MV', _('Maldives')),
    ('MW', _('Malawi')),
    ('MX', _('Mexico')),
    ('MY', _('Malaysia')),
    ('MZ', _('Mozambique')),
    ('NA', _('Namibia')),
    ('NC', _('New Caledonia')),
    ('NE', _('Niger')),
    ('NF', _('Norfolk Island')),
    ('NG', _('Nigeria')),
    ('NI', _('Nicaragua')),
    ('NL', _('Netherlands')),
    ('NO', _('Norway')),
    ('NP', _('Nepal')),
    ('NR', _('Nauru')),
    ('NU', _('Niue')),
    ('NZ', _('New Zealand')),
    ('OM', _('Oman')),
    ('PA', _('Panama')),
    ('PE', _('Peru')),
    ('PF', _('French Polynesia')),
    ('PG', _('Papua New Guinea')),
    ('PH', _('Philippines')),
    ('PK', _('Pakistan')),
    ('PL', _('Poland')),
    ('PM', _('St. Pierre & Miquelon')),
    ('PN', _('Pitcairn')),
    ('PR', _('Puerto Rico')),
    ('PT', _('Portugal')),
    ('PW', _('Palau')),
    ('PY', _('Paraguay')),
    ('QA', _('Qatar')),
    ('RE', _('Reunion')),
    ('RO', _('Romania')),
    ('RU', _('Russian Federation')),
    ('RW', _('Rwanda')),
    ('SA', _('Saudi Arabia')),
    ('SB', _('Solomon Islands')),
    ('SC', _('Seychelles')),
    ('SD', _('Sudan')),
    ('SE', _('Sweden')),
    ('SG', _('Singapore')),
    ('SH', _('St. Helena')),
    ('SI', _('Slovenia')),
    ('SJ', _('Svalbard & Jan Mayen Islands')),
    ('SK', _('Slovakia')),
    ('SL', _('Sierra Leone')),
    ('SM', _('San Marino')),
    ('SN', _('Senegal')),
    ('SO', _('Somalia')),
    ('SR', _('Suriname')),
    ('ST', _('Sao Tome & Principe')),
    ('SV', _('El Salvador')),
    ('SY', _('Syrian Arab Republic')),
    ('SZ', _('Swaziland')),
    ('TC', _('Turks & Caicos Islands')),
    ('TD', _('Chad')),
    ('TF', _('French Southern Territories')),
    ('TG', _('Togo')),
    ('TH', _('Thailand')),
    ('TJ', _('Tajikistan')),
    ('TK', _('Tokelau')),
    ('TM', _('Turkmenistan')),
    ('TN', _('Tunisia')),
    ('TO', _('Tonga')),
    ('TP', _('East Timor')),
    ('TR', _('Turkey')),
    ('TT', _('Trinidad & Tobago')),
    ('TV', _('Tuvalu')),
    ('TW', _('Taiwan, Province of China')),
    ('TZ', _('Tanzania, United Republic of')),
    ('UA', _('Ukraine')),
    ('UG', _('Uganda')),
    ('UM', _('United States Minor Outlying Islands')),
    ('US', _('United States of America')),
    ('UY', _('Uruguay')),
    ('UZ', _('Uzbekistan')),
    ('VA', _('Vatican City State (Holy See)')),
    ('VC', _('St. Vincent & the Grenadines')),
    ('VE', _('Venezuela')),
    ('VG', _('British Virgin Islands')),
    ('VI', _('United States Virgin Islands')),
    ('VN', _('Viet Nam')),
    ('VU', _('Vanuatu')),
    ('WF', _('Wallis & Futuna Islands')),
    ('WS', _('Samoa')),
    ('YE', _('Yemen')),
    ('YT', _('Mayotte')),
    ('YU', _('Yugoslavia')),
    ('ZA', _('South Africa')),
    ('ZM', _('Zambia')),
    ('ZR', _('Zaire')),
    ('ZW', _('Zimbabwe')),
    ('ZZ', _('Unknown or unspecified country')),
)

    UNIVERSITY_ENDORSEMENT = (
          ('Strongly recommended','Strongly recommended'),
          ('Recommended','Recommended'),
          ('Not recommended','Not recommended'),
         


        )

    university_endorsement=models.CharField(max_length=20, choices=UNIVERSITY_ENDORSEMENT, null=True)
    UNIVERSITY_ROLE = (
       ('Tutor', 'Tutor'),
       ('Mentor','Mentor'),
       ('University Professor', 'University Professor'),
       ('Employeer', 'Employeer'),
      )
    university_role=models.CharField(max_length=100, choices= UNIVERSITY_ROLE,  null=True)
    university_role_name=models.CharField(max_length=100, null=True)

    STATUS_UPDATES = (
       ('In consideration', 'In consideration'),
       ('First Interview Scheduled','First Interview Scheduled'),
       ('First Interview Passed', 'First Interview Passed'),
       ('Interview with Manager Scheduled', 'Interview with Manager Scheduled'),
       ('On Hold', 'On Hold'),
      )
    status=models.CharField(max_length=100, choices= STATUS_UPDATES, default='In consideration', null=True)
    

    INTERVIEW_RESPONSE=(
       ('Tutor', 'Tutor'),
       ('Mentor','Mentor'),
       ('University Professor', 'University Professor'),
       ('Employeer', 'Employeer'),
      )
    webex_link = models.TextField(max_length=200, null=True)

    interview_response = models.CharField(max_length=100,
                                            choices=INTERVIEW_RESPONSE,
                                            default='None', null=True)
    interviewer_comment = models.TextField(max_length=1000, null=True, default=None)
    interviewer_name = models.CharField(max_length=100, null=True, default=None)
    

    GENDER= (('male', 'male'),('female','female'),)
    gender=models.CharField(max_length=6, choices=GENDER, default='male', null=True)
   
    PASSPORT= (
         ('Yes', 'Yes'),
         ('No','No'),
        )
    good_university=models.CharField(max_length=3, choices=PASSPORT, default='Yes',null=True)
    passport=models.CharField(max_length=3, choices=PASSPORT, default='Yes',null=True)
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
    country_issued=models.CharField(max_length=2, choices=COUNTRIES,
                             default='ZZ', null=True)

    date_issued=models.DateField(_("Date"), default=date.today)

    date_expiration=models.DateField(_("Date"), default=date.today)

# http://xml.coverpages.org/country3166.html


    country=models.CharField(max_length=2, choices=COUNTRIES,
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



    UNIVERSITY_CHOICES = (
        ('UCL', 'UCL'),
        ('Kent', 'Kent'),
        ('EPFL', 'EPFL'),
        ('Keio','Keio'),
        ('ZJU', 'ZJU'),
        ('BMSTU','BMSTU'),
        ('CTU', 'CTU'),
        ('Tsinghua', 'Tsinghua'),
        ('UNSW', 'UNSW'),
        ('Ottawa','Ottawa'),
    )
    university = models.CharField(max_length=20,
                                      choices=UNIVERSITY_CHOICES,
                                      default = 'UCL', null=True)
    YEAR_OF_GRADUATION=(('2014','2014'),('2015','2015'),('2016','2016'),('2017','2017'),)
    year_of_graduation=models.CharField(max_length=4, choices=YEAR_OF_GRADUATION, default='2014', null=True)
    #year_of_graduation=models.DateField(auto_now=False, auto_now_add=False)
    degree=models.CharField(max_length=60, null=True)
    average=models.CharField(max_length=2, null=True)
    #average=models.DecimalField(max_digits=2, decimal_places=0, null=True)

    SKILL_LEVEL=(
      ('Advanced','Advanced'),
      ('Intermediate','Intermediate'),
      ('Beginner','Beginner'),
      ('None','None'),

    )
    skill_1=models.CharField(max_length=60, null=True)
    skill_level_1=models.CharField(max_length=30,
                                       choices=SKILL_LEVEL,
                                       default='None', null=True)
    skill_2=models.CharField(max_length=60, null=True)
    skill_level_2=models.CharField(max_length=30,
                                       choices=SKILL_LEVEL,
                                       default='None', null=True)
    skill_3=models.CharField(max_length=60, null=True)
    skill_level_3=models.CharField(max_length=30,
                                       choices=SKILL_LEVEL,
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
    

    #image = models.ImageField(upload_to='images/%Y/%m/%d')


    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.last_name) or u''
    






class UniversityAdmin(Profile):
    #user=models.ForeignKey(User, unique=True)
    UNIVERSITY_CHOICES = (
        ('UCL', 'UCL'),
        ('Kent', 'Kent'),
        ('EPFL', 'EPFL'),
        ('Keio','Keio'),
        ('ZJU', 'ZJU'),
        ('BMSTU','BMSTU'),
        ('CTU', 'CTU'),
        ('Tsinghua', 'Tsinghua'),
        ('UNSW', 'UNSW'),
        ('Ottawa','Ottawa'),
    )
    university = models.CharField(max_length=20,
                                      choices=UNIVERSITY_CHOICES,
                                      default = 'UCL', null=True)
    first_name = models.CharField(max_length=20, null=True)
    last_name= models.CharField(max_length = 20, null=True)
    #university=models.ForeignKey(University, null=True)
    #uni_admin=models.CharField(max_length=20, null=True)
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.first_name) or u''















