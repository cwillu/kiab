from django.db import models
import re
import cPickle as pickle
import django.contrib.auth.models as auth

class Widget(object):
  @classmethod
  def render_generic(self):
    return "<span>%s</span>" % str(self.__name__)

class Address(Widget):
  def __init__(self, data):
    self.data = data
    
  def render(self):
    return '''
    <textarea rows="5">%s</textarea>
    '''.strip() % self.data
  
class Phone(Widget):
  def __init__(self, data):
    self.data = data
  def render(self):
    return '''
    <input type="text" rows="5" value="%s" />
    '''.strip() % self.data

class Email(Widget):
  def __init__(self, data):
    self.data = data
  def render(self):
    return '''
    <input type="text" rows="5" value="%s" />
    '''.strip() % self.data

class Comment(Widget):
  def __init__(self, who, when, data):
    self.who = who.strip()
    self.when = when.strip()
    self.data = map(str.strip, data.splitlines())
    
  def render(self):
    return '''
    <div class="comment">
      <span class="name">%s</span>
      <span class="date">%s</span>
      <span class="content">%s</span>
    </div>
    '''.strip() % (self.who, self.when, self.data)
  
  
widgets = dict(address=Address, phone=Phone, email=Email)


# keep fields an order of magnitude larger than the largest input expected
class Contact(models.Model):
  name = models.CharField(max_length=200)
  sortName = models.CharField(max_length=200)
  summary = models.TextField()
    
  def save(self, force_insert=False, force_update=False):
    pieces = re.findall(r'\w+', self.name)
    self.sortName = ' '.join(pieces[-1:] + pieces[:-1]) if pieces else ''
    super(Contact, self).save(force_insert, force_update)

  class Meta:
    ordering = ["sortName"]
    
  def __unicode__(self):
    return self.name 

class Detail(models.Model):
  contact = models.ForeignKey(Contact)
  position = models.IntegerField()
  detailType = models.CharField(max_length=200, verbose_name="type")
  data = models.TextField()
  
  def put(self, obj):
    self.data = pickle.dumps(obj)
  
  def get(self):
    obj = pickle.loads(self.data)
    obj.id = self.id
    return obj
    
class Entry(models.Model):
  contact = models.ForeignKey(Contact)
  date = models.DateField()
  who = models.ForeignKey('auth.User')
  entry = models.TextField()
  
classes = [Contact, Detail, Entry]
