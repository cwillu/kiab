from django.db import models
import re
import cPickle as pickle
import django.contrib.auth.models as auth
from django.db import transaction

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
    ob
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


class SearchIndexQueue(models.Model):
  contact = models.ForeignKey(Contact)

class SearchIndex(models.Model):
  piece = models.CharField()
  contacts = models.ManyToManyField(Contact)

  @transaction.commit_manually
  def touch(self, contact):
    try:
      getOrCreate(SearchIndexQueue, contact=contact).save() 
      contact.searchindex_set.delete()
    except:
      transaction.rollback()
      raise
    else:
      transaction.commit()
  
  def search(self, query):
  
    #    jQuery.query = function (query) {
    #      var tokens = query.toLowerCase().split(/\s+/g);  
    #
    #      var bitmap = $.map(new Array(index[0].length), function (value, index) { return index; });
    #      $.each(tokens, function (i, token) {
    #        var hits = [];
    #        if (token) {
    #          $.each(index[1], function (key, value) {
    #            if (key.substr(0, token.length) === token) {
    #              hits = hits.concat(value);
    #            }
    #          });
    #        }    
    #        hits = $.unique(hits);
    #        bitmap = $.grep(bitmap, function (val, _) {
    #          return $.inArray(val, hits) >= 0;
    #        });
    #      });
    #      
    #      return $.map(bitmap, function(v, i) {
    #        return [index[0][v]];
    #      });
    #    } 
  
classes = [Contact, Detail, Entry]















