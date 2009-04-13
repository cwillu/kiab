# -*- coding: utf-8 -*-

from django.http import HttpResponse
from contacts import models
from django.conf import settings
from django.template import Context, loader, libraries
from django.contrib.auth import decorators as auth
from django.contrib.webdesign import lorem_ipsum

from jinja2 import Environment, FileSystemLoader
jinja = Environment(loader=FileSystemLoader(settings.TEMPLATE_DIRS))

import locale
locale.setlocale(locale.LC_ALL, "en_CA.UTF-8")

import django.forms.widgets as widgets

import models

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
  models.Comment(makeName(), '2009-01-27', lorem_ipsum.paragraph()),
  models.Comment(makeName(), '2009-01-29', *lorem_ipsum.paragraphs(3)),
  models.Comment(makeName(), '2009-03-03', lorem_ipsum.paragraph()),
]

def createContact(request):
  template = jinja.get_template('contacts/contact.html')
  context = {
    'available': models.widgets.values(),
    'details': [],
    'comments': [],
  }
  return HttpResponse(template.render(**context))

def contact(request, contactId):
  if contactId == 'test':
    contact = models.Contact(name="Carey Underwood")  
    details = testDetails
    comments = testComments
  else:
    contact = models.Contact.objects.get(id=int(contactId))
    
    details = list(models.Detail.objects.filter(contact=contact))
    details = [detail.get() for detail in details]
    
    comments = models.Entry.objects.filter(contact=contact)
  
  template = jinja.get_template('contacts/contact.html')
  context = {
    'contact': contact,
    'available': models.widgets.values(),
    'details': details,
    'comments': comments,
  }
  return HttpResponse(template.render(**context))

def updateName(request, contactId):
  if contactId == 'test':
    contact = models.Contact(name="Carey Underwood")
  else: 
    contact = models.Contact.objects.get(id=int(contactId))

  print "contact", contact

  name = request.POST['name'].strip()
  print "name", name 
  
  contact.name = name
  contact.save()
  
def update(request, contactId):
  if contactId == 'test':
    contact = models.Contact(name="Carey Underwood")
  else: 
    contact = models.Contact.objects.get(id=int(contactId))

  print "contact", contact

  detailId = request.POST.get('update', None)
#  detailType = request.POST['type']
  detailData = request.POST['detail'].strip()

  print "id", detailId
  print "detail", detailData
  
  if not detailData:
    raise "delete"
  elif '\n' in detailData:
    detailType = 'Long'
  else:
    detailType = 'Short'
  detailConstructor = models.widgets[detailType]

  print "type", detailType
  
  detail = models.Detail.objects.get(uuid=detailId, contact=contact, detailType=detailType)    
        
  detail.put(detailConstructor(detailData))
  detail.save()

def comment(request, contactId):
  contact = models.Contact.objects.get(id=int(contactId))
  if not contact:
    return
    
  entry = models.Entry(contact=contact, who=None, when=None)
  #entry.entry = request.?
  
  
  
  
  
  
  
  
  
  
  
  
  
  
