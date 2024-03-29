# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Interview.skype_name'
        db.add_column('ciip_interview', 'skype_name',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Interview.skype_name'
        db.delete_column('ciip_interview', 'skype_name')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'ciip.interview': {
            'Meta': {'object_name': 'Interview'},
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interview_response': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ciip.ManagerProfile']"}),
            'skype_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ciip.UserProfile']"})
        },
        'ciip.managerprofile': {
            'Meta': {'object_name': 'ManagerProfile'},
            'business_unit': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest_1': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'interest_2': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'interest_3': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'skill_1': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'skill_2': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'skill_3': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'ciip.message': {
            'Meta': {'object_name': 'Message'},
            'date_sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ciip.ManagerProfile']"}),
            'sent_by': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ciip.UserProfile']"}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True'})
        },
        'ciip.universityadmin': {
            'Meta': {'object_name': 'UniversityAdmin'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'university': ('django.db.models.fields.CharField', [], {'default': "'UCL'", 'max_length': '20', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'ciip.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'adaptability': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '3', 'null': 'True'}),
            'address_line1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'address_line2': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'average': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'birth_date_day': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'birth_date_month': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'birth_date_year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'}),
            'cisco_fit': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '3', 'null': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'ZZ'", 'max_length': '2', 'null': 'True'}),
            'country_issued': ('django.db.models.fields.CharField', [], {'default': "'ZZ'", 'max_length': '2', 'null': 'True'}),
            'cover_letter': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'date_expiration': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'date_interview': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_issued': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'degree': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'email_emergency': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'experience_1': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True'}),
            'experience_2': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True'}),
            'file_cv': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'full_name_emergency': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'male'", 'max_length': '6', 'null': 'True'}),
            'good_university': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '3', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initiative': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '3', 'null': 'True'}),
            'innovation': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '3', 'null': 'True'}),
            'interest_1': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'interest_2': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'interest_3': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'internship_1': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True'}),
            'internship_2': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True'}),
            'interview_response': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'interviewer_comment': ('django.db.models.fields.TextField', [], {'default': 'None', 'max_length': '1000', 'null': 'True'}),
            'interviewer_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'leadership': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '3', 'null': 'True'}),
            'manager_comment': ('django.db.models.fields.TextField', [], {'default': 'None', 'max_length': '1000', 'null': 'True'}),
            'master_or_undergrad': ('django.db.models.fields.CharField', [], {'default': "'---'", 'max_length': '30', 'null': 'True'}),
            'motivation': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '3', 'null': 'True'}),
            'offer_states': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'}),
            'passport': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '3', 'null': 'True'}),
            'passport_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'phone_emergency': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'position_suggested': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'question_1': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True'}),
            'question_2': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True'}),
            'question_3': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'skill_1': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'skill_2': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'skill_3': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'skill_level_1': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '30', 'null': 'True'}),
            'skill_level_2': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '30', 'null': 'True'}),
            'skill_level_3': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '30', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'In consideration'", 'max_length': '100', 'null': 'True'}),
            'team_player': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '3', 'null': 'True'}),
            'technical_interview_screen_comment': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True'}),
            'technical_interview_screen_selection': ('django.db.models.fields.CharField', [], {'default': "'---'", 'max_length': '30', 'null': 'True'}),
            'technical_resume_screen_comment': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True'}),
            'technical_resume_screen_selection': ('django.db.models.fields.CharField', [], {'default': "'---'", 'max_length': '30', 'null': 'True'}),
            'technical_skill': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '3', 'null': 'True'}),
            'uni_comment': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True'}),
            'university': ('django.db.models.fields.CharField', [], {'default': "'UCL'", 'max_length': '20', 'null': 'True'}),
            'university_endorsement': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'university_role': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'university_role_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'webex_link': ('django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True'}),
            'year_of_graduation': ('django.db.models.fields.CharField', [], {'default': "'2014'", 'max_length': '4', 'null': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['ciip']