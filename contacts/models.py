from django.db import models
import re
import cPickle as pickle
import django.contrib.auth.models as auth

class Widget(object):
  def __init__(self):
    self.uuid = None
      
  def render_generic(self):
    return "<span>%s</span>" % self.name()

  def name(self):
    return self.__class__.__name__
    
  def create(self, *args, **kargs):
    return self.__class__(*args, **kargs)

  def render(self, uuid=None):
    assert (uuid is None) is not (self.uuid is None), "No UUID or two UUID's defined: %s, %s" % (self.uuid, uuid)
    if uuid is None:
      uuid = self.uuid
      
    return self.template("id=%s" % uuid)

class Long(Widget):
  def __init__(self, data=''):
    self.data = data
    Widget.__init__(self)
    
  def template(self, id):
    return '''
    <textarea %s class="control" rows="5">%s</textarea>
    '''.strip() % (id, self.data)
  
class Short(Widget):
  def __init__(self, data=''):
    self.data = data
    Widget.__init__(self)
    
  def template(self, id):
    return '''
    <input %s class="control" type="text" rows="5" value="%s" />
    '''.strip() % (id, self.data)

class Comment(Widget):
  def __init__(self, who, when, data):
    self.who = who.strip()
    self.date = when.strip()
    self.entry = data
    Widget.__init__(self)
    
widgets = dict(short=Short(), long=Long())

def getOrCreate(model, **query):
  count = len(model.objects.filter(**query))
  assert count in [0, 1], "Query results didn't make sense: %s (%s)" % (query, count)
  if count is 0:
    return model(**query), True
  else:
    return model.objects.get(**query), False
    
# keep fields an order of magnitude larger than the largest input expected
class Contact(models.Model):
  name = models.CharField(max_length=200)
  uuid = models.SlugField()
  sortName = models.CharField(max_length=200)
  summary = models.TextField()
  
  def setDetail(self, uuid, data):
    '''
      Set the detail 'uuid' on this contact.
      Returns:
      * True if detail didn't exist
      * None if value if detail is updated
      * False if value is deleted or not created
    '''
    detail, created = getOrCreate(Detail, uuid=uuid, contact=self)
    if not data:
      if created:
        return None #Deleting a non-existing item==no-op
    
      detail.delete()
      return False
      
    detail.munch(data)
    detail.save()
    return created or None

  def addComment(self, uuid, data):
    '''
      Set the detail 'uuid' on this contact.
      Returns:
      * True if detail didn't exist
      * None if value if detail is updated
      * False if value is deleted or not created
    '''
    if not data:
      return False
    
      
#    entry = models.Entry(contact=contact, date="2008-10-10") #todo, uuid
#    entries = entry.entry
#    entries += contents
#    entry.entry = entries
#    print "Resulting %s" % entry.entry
#    entry.save()
#    assert entry.entry is not None

      
    comment, created = getOrCreate(Entry, uuid=uuid, contact=self)
    
    if not comment.date:
      comment.date = "2008-10-10"
    
    comment.munchAndAppend(data)
    comment.save()
    return comment

  @property 
  def details(self):
    details = list(Detail.objects.filter(contact=self))
    return [detail.get() for detail in details]
  
  @property
  def comments(self):
    return Entry.objects.filter(contact=self)
  
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
  
  def munch(self, data):
    self.detail = data
  
  def put(self, obj):
    self.data = pickle.dumps(obj)
  def get(self):
    class Unicode_(unicode):
      pass
    obj = Unicode_(pickle.loads(str(self.data)))
      
    obj.id = self.id
    obj.uuid = self.uuid
    return obj
  detail = property(get, put)
    
class Entry(models.Model):
  contact = models.ForeignKey(Contact)
  uuid = models.SlugField()
  date = models.DateField()
  who = models.ForeignKey('auth.User', null=True)
  data = models.TextField()

  def munchAndAppend(self, data):
    entry = self.entry
    entry += data
    self.entry = entry
  
  def put(self, obj):
    self.data = pickle.dumps(obj)
  
  def get(self):
    if not self.data:
      return []
      
    obj = pickle.loads(str(self.data))
    return obj
  entry = property(get, put)
  
classes = [Contact, Detail, Entry]
