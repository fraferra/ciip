import pyrise
from pyrise import *
from ciip.models import *
import re

Highrise.set_server('ciip')
Highrise.auth('e4fc52ecf013f5441c1c614fe50ee6e7')

students=UserProfile.objects.all()

for student in students:
    offer= student.offer_states
    if not offer is None:
        match=re.search('offer accepted', student.offer_states.lower())
        if match:
            person=Person()
            person.first_name = student.first_name
            person.last_name = student.last_name
            person.contact_data = ContactData(
            email_addresses=[
                 EmailAddress(address=student.user.email, location='Work'),
                 EmailAddress(address=student.email, location='Home'),
                 ],
            phone_numbers=[PhoneNumber(number=student.phone, location='Mobile')],
                 )
            
            person.save()
            person.add_note(student.interviewer_comment)
            person.add_tag(student.university)
            person.add_tag('FY15')
            
            