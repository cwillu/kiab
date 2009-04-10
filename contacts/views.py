# -*- coding: utf-8 -*-

from django.http import HttpResponse
from contacts import models
from django.conf import settings
from django.template import Context, loader, libraries
from django.contrib.auth import decorators as auth

from jinja2 import Environment, FileSystemLoader
jinja = Environment(loader=FileSystemLoader(settings.TEMPLATE_DIRS))

import locale
locale.setlocale(locale.LC_ALL, "en_CA.UTF-8")

import django.forms.widgets as widgets

import models

testDetails = [
  models.Address('''1115 Cairns Ave\nSaskatoon, SK\nS7H 4G3'''.strip()),
  models.Phone('306-251-0744'),
  models.Phone('306-373-0552'),
  models.Email('cwillu@cwillu.com'),
  models.Email('cwillu@gmail.com'),
]

testComments = [
  models.Comment('Kai Mast', '2009-01-27', 'I can confirm this with AMD64 and Ubuntu Jaunty'),
  models.Comment('Niclas L', '2009-01-29', ' I have experienced some issues with EXT4 and data losses too, but more extreme than you all describe. I installed jaunty alpha 3 two days ago and have all the updates installed. Since the install 2 days ago I have lost data on 3 occations. The most strange losses is:\n\n* the computer wiped out a whole network share mounted in fstab\n* the computer one time also removed ~/.icons when I empty the trash\n\nThe data losses never happened after a crasch or power failure.'),
  models.Comment('Christoph Korn', '2009-03-03', '* data loss in jaunty (full upgraded) (307.6 KiB, image/png)\n\nI can confirm this data loss in jaunty.\nI installed all updates before trying the script in this comment:\nhttps://bugs.launchpad.net/ubuntu/jaunty/+source/linux/+bug/317781/comments/29\n\nI am testing jaunty in virtualbox.\n\nI have put the script on the desktop. I started it and turned the virtual machine off after some seconds.\n\nAfter reboot all files (also the script itself) are 0Byte and I cannot even open them with gedit.'),
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
  
def update(request, contactId):
  contact = models.Contact.objects.get(id=int(contactId))

  detailId = request.POST.get('update', None)
#  detailType = request.POST['type']
  detailConstructor = models.widgets[detailType]
  detailPosition = 0 #request.detailPosition
  detailData = request.POST['detail']
  
  if detailId:
    detail = models.Detail.objects.get(id=detailId, contact=contact, detailType=detailType)    
  else:    
    detail = models.Detail(contact=contact, detailType=detailType)    
        
  detail.position = detailPosition #insert how?
  detail.put(detailConstructor(detailData))
  detail.save()  

def comment(request, contactId):
  contact = models.Contact.objects.get(id=int(contactId))
  if not contact:
    return
    
  entry = models.Entry(contact=contact, who=None, when=None)
  #entry.entry = request.?
  
  
  
  
  
  
  
  
  
  
  
  
  
  
