import pyrise
from pyrise import *
from ciip.models import *
import re

Highrise.set_server('ciip')
Highrise.auth('e4fc52ecf013f5441c1c614fe50ee6e7')

students=UserProfile.objects.all()

for student in students:
	match=re.search('offered', student.offer_states.lower())
	if match:
         person=Person()
         person.first_name = student.first_name
         person.last_name = student.last_name
         person.contact_data = ContactData(
         	email_addresses=[
         	    EmailAddress(address=student.user.email, location='University'),
         	    EmailAddress(address=student.email, location='Personal'),
         	    ],
         	    phone_numbers=[PhoneNumber(number=student.phone, location='Personal')],
         	    )
         person.add_tag(student.university)
         person.add_tag('FY15')
         person.notes=student.interviewer_comment
         person.save()