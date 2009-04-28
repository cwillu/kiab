# -*- coding: utf-8 -*-

from django.http import HttpResponse
from contacts import models
from django.conf import settings
from django.template import Context, loader, libraries
from django.contrib.auth import decorators as auth
from django.contrib.webdesign import lorem_ipsum
from django import http
from django.core.urlresolvers import reverse
from jinja2 import Environment, FileSystemLoader
jinja = Environment(loader=FileSystemLoader(settings.TEMPLATE_DIRS))

from uuid import uuid4 as uuid

import locale
locale.setlocale(locale.LC_ALL, "en_CA.UTF-8")

import django.forms.widgets as widgets

import models

class Widget(object):
  def render_generic(self):
    return "<span>%s</span>" % self.name()

  def name(self):
    return self.__class__.__name__
    
  def create(self, *args, **kargs):
    return self.__class__(*args, **kargs)

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

testDetails = [
  models.Long('''1115 Cairns Ave\nSaskatoon, SK\nS7H 4G3'''.strip()),
  models.Short('306-251-0744'),
  models.Short('306-373-0552'),
  models.Short('cwillu@cwillu.com'),
  models.Short('cwillu@gmail.com'),
]

def makeName():
  words = lorem_ipsum.words(3, 0).title().split()
  words[1] = words[1][0]
  return ' '.join(words)
  

testComments = [
  models.Comment(makeName(), '2009-01-27', lorem_ipsum.paragraphs(1)),
  models.Comment(makeName(), '2009-01-29', lorem_ipsum.paragraphs(3)),
  models.Comment(makeName(), '2009-03-03', lorem_ipsum.paragraphs(1)),
]

def blankContact(request):
  template = jinja.get_template('contacts/contact.html')
  context = {
    'contact': models.Contact(),
    'uuid': uuid(),
    'available': models.widgets.values(),
  }
  return HttpResponse(template.render(**context))

def showContact(request, contactId):
  contact = models.Contact.objects.get(id=int(contactId))
  
  template = jinja.get_template('contacts/contact.html')
  context = {
    'uuid': contact.uuid,
    'contact': contact,
    'available': models.widgets.values(),
  }
  return HttpResponse(template.render(**context))

def updateName(request, contactId):
  contact_uuid = request.POST['uuid']
  name = request.POST.get('name', '').strip()
  print "name", name
  print "id", contactId
  
  if contactId == 'create':
    print models.Contact.objects.filter(uuid=contact_uuid)
    assert not models.Contact.objects.filter(uuid=contact_uuid), contact_uuid
    contact = models.Contact(uuid=contact_uuid)    
  elif contactId is not None:
    contact = models.Contact.objects.get(id=int(contactId), uuid=contact_uuid)

  print "contact", contact

  contact.name = name
  contact.save()
  if contactId == 'create':
    response = HttpResponse(status=201)
    response['x-location'] = reverse(showContact, args=[contact.id])
    response['x-contact'] = contact.id
    return response
  else:
    return HttpResponse(status=204)
    
def getOrCreateContact(request, contactId):
  response = None
  if contactId == 'create':
    response = updateName(request, contactId)
    contactId = response['contact']

  contact = models.Contact.objects.get(id=int(contactId))

  print "contact", contact

  return contact, response

def updateDetail(request, contactId):
  contact, response = getOrCreateContact(request, contactId)

  detailId = request.POST.get('update', None)
  detailData = request.POST['detail'].strip()

  print "id", detailId
  print "detail", detailData

  if contact.setDetail(detailId, detailData) is not False:
    return response or HttpResponse(status=205)

  if not detailData:
    assert not response, "Wait, we just created this contact, how was this detail already there? %s, %s" % (contact, detail)

  return HttpResponse(status=204)

def addComment(request, contactId):
  contact, response = getOrCreateContact(request, contactId)

  comment = request.POST['comment']
  if not comment:
    return HttpResponse(status=204)
    
  print comment
  entry = models.Entry(contact=contact, date="2008-10-10") #todo, uuid
  entries = entry.entry
  entries.append(comment)
  entry.entry = entries
  print entry.entry
  entry.save()
  assert entry.entry is not None
  if False:  #existing entry
    return HttpResponse(status=201)
  else:
    return response or HttpResponse(status=205)
    
#  class Entry(models.Model):
#    contact = models.ForeignKey(Contact)
#    date = models.DateField()
#    who = models.ForeignKey('auth.User')
#    entry = models.TextField()

def comment(request, contactId):
  contact = models.Contact.objects.get(id=int(contactId))
  if not contact:
    return
    
  entry = models.Entry(contact=contact, who=None, when="10/10/2010")
  #entry.entry = request.?
  
  
  
  
  
  
  
  
  
  
  
  
  
  
