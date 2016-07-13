from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here

class Novel(models.Model):
	like = models.IntegerField(default=0)
	title = models.CharField(max_length=100, db_index=True)
	writer = models.ForeignKey(User, related_name='novel_set')
	pub_date = models.DateTimeField(auto_now_add=True)
        def __unicode__(self):
            return self.title

class Paragraph(models.Model):
	prev_paragraph = models.ForeignKey('Paragraph', related_name='next_paragraph_set', null=True)
	text = models.TextField()
	like = models.IntegerField(default=0)
	novel = models.ForeignKey(Novel, related_name='paragraph_set')
	writer = models.ForeignKey(User, related_name='paragraph_set')
	pub_date = models.DateTimeField(auto_now_add=True)
        is_first = models.BooleanField(default=False)
        is_userfirst = models.BooleanField(default=False)
        index = models.IntegerField(default=1)
	
        def __unicode__(self):
            return u"%s(%s)"%(self.novel.title,self.text[0:20])
