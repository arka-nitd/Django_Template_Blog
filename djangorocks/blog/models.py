from __future__ import unicode_literals

from django.db import models
from django.db.models import permalink
from django_auth_ldap.backend import populate_user
from django.contrib.auth.models import *

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField()
    posted = models.DateTimeField(db_index=True, auto_now_add=True)
    category = models.ForeignKey('blog.Category')

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('view_blog_post', None, { 'slug': self.slug })

#Comments
class Comment(models.Model):
    post = models.ForeignKey('Blog', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('view_blog_category', None, { 'slug': self.slug })

#def make_super(sender, user, **kwargs): 

#	user.is_superuser = True 

#populate_user.connect(make_super) 

def make_staff(sender, user, **kwargs):
    user.is_staff = True
    pl = Permission.objects.filter(codename__in=["add_comment", "change_comment", "delete_comment"])
    user.user_permissions.add(*pl)
populate_user.connect(make_staff)

