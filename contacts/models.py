from django.db import models
import re
import cPickle as pickle
import django.contrib.auth.models as auth

class Widget(object):
  def render_generic(self):
    return "<span>%s</span>" % self.name()

  def name(self):
    return self.__class__.__name__
    
  def create(self, *args, **kargs):
    return self.__class__(*args, **kargs)

class Long(Widget):
  def __init__(self, data=''):
    self.data = data
    
  def render(self, id=None):
    if id:
      id = "id=%s" % id
    else:
      id = ''
      
    return '''
    <textarea %s class="control" rows="5">%s</textarea>
    '''.strip() % (id, self.data)
  
class Short(Widget):
  def __init__(self, data=''):
    self.data = data
  def render(self, id=None):
    if id:
      id = "id=%s" % id
    else:
      id = ''
    return '''
    <input %s class="control" type="text" rows="5" value="%s" />
    '''.strip() % (id, self.data)

class Comment(Widget):
  def __init__(self, who, when, data):
    self.who = who.strip()
    self.date = when.strip()
    self.entry = data

    
widgets = dict(short=Short(), long=Long())


# keep fields an order of magnitude larger than the largest input expected
class Contact(models.Model):
  name = models.CharField(max_length=200)
  uuid = models.SlugField()
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
  uuid = models.CharField(max_length=36)
  contact = models.ForeignKey(Contact)
  detailType = models.CharField(max_length=200, verbose_name="type")
  data = models.TextField()
  
  def put(self, obj):
    self.data = pickle.dumps(obj)
  
  def get(self):
    obj = pickle.loads(str(self.data))
    obj.id = self.id
    obj.uuid = self.uuid
    return obj
  
  detail = property(get, put)
    
class Entry(models.Model):
  contact = models.ForeignKey(Contact)
  date = models.DateField()
  who = models.ForeignKey('auth.User', null=True)
  data = models.TextField()
  
  def put(self, obj):
    self.data = pickle.dumps(obj)
  
  def get(self):
    if not self.data:
      return []
      
    obj = pickle.loads(str(self.data))
    return obj
  entry = property(get, put)
  
classes = [Contact, Detail, Entry]
