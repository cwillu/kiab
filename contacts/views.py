# -*- coding: utf-8 -*-

from django.http import HttpResponse
from contacts import models
from django.conf import settings
from django.template import Context, loader, libraries
from django.contrib.auth import decorators as auth
from django.contrib.webdesign import lorem_ipsum
from django import http
from django.core.urlresolvers import reverse
from jinja2 import Environment, FileSystemLoader, Markup
jinja = Environment(loader=FileSystemLoader(settings.TEMPLATE_DIRS), autoescape=True)

from uuid import uuid4 as uuid

import locale
locale.setlocale(locale.LC_ALL, "en_CA.UTF-8")

import django.forms.widgets as widgets

import models

class Widget(object):
  def render_generic(self):
    return Markup(jinja.from_string("<span>{{ name }}</span>").render(name=self.name()))

  def name(self):
    return self.__class__.__name__
    
  def create(self, *args, **kargs):
    return self.__class__(*args, **kargs)

class Short(Widget):
  def __init__(self, data=''):
    self.data = data
  def render(self, id=None):
    return Markup(jinja.from_string('''
    <input {% if id %}id="{{id}}" {%endif -%} class="control" type="text" rows="5" value="{{value}}" />
    ''').render(id=id, value=self.data))

widgets = dict(short=Short())


def renderDetail(detail, id=None):
  if not id:
    id = detail.id
  print detail
  widget = Short(detail)
  print Markup(widget.render(id))
  return Markup(widget.render(id))

def blankContact(request):
  template = jinja.get_template('contacts/contact.html')
  context = {
    'contact': models.Contact(),
    'render': renderDetail,
    'uuid': uuid(),
    'available': widgets.values(),
  }
  return HttpResponse(template.render(**context))

commentTemplate = '''
<div class="comment">
  <div class="header">
    <span class="detail">{{ comment.who }}</span><span class="label">, on</span>
    <span class="detail">{{ comment.date }}</span><span class="label">:</span>
  </div>
  <div class="content">
  {% for line in comment.entry -%}
    <p>{{ line|wordwrap(80) }}</p>
  {%- endfor %}
  </div>
</div>
'''

def showContact(request, contactId):
  contact = models.Contact.objects.get(id=int(contactId))
  
  template = jinja.get_template('contacts/contact.html')
  context = {
    'uuid': contact.uuid,
    'render': renderDetail,
    'contact': contact,
    'commentTemplate': commentTemplate, 
    'available': widgets.values(),
  }
  return HttpResponse(template.render(**context))

def search(request, query):
  pass

def updateName(request, contactId):
  contact_uuid = request.POST['uuid']
  name = request.POST.get('name', '').strip()
  print "name", name
  print "id", contactId
  
  if contactId == 'create':
    while models.Contact.objects.filter(uuid=contact_uuid):
      #user hit the back button, or the nearly impossible happened
      contact_uuid = str(uuid())
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
    contactId = response['x-contact']

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

  print "removed detail"
  response = HttpResponse(status=204)
  snippet = autoComment(contact, ["[Removed detail]"], request)
  response.write(snippet)

  return response

def addComment(request, contactId):
  contact, response = getOrCreateContact(request, contactId)

  comment = request.POST['comment']
  if not comment:
    return HttpResponse(status=204)

  if False:  #existing entry
    response = HttpResponse(status=201)
  elif not response:
    response = HttpResponse(status=205)
  
  snippet = autoComment(contact, [comment], request)
  print snippet
  response.write(snippet)
  return response
  
    
#  class Entry(models.Model):
#    contact = models.ForeignKey(Contact)
#    date = models.DateField()
#    who = models.ForeignKey('auth.User')
#    entry = models.TextField()

def autoComment(contact, contents, request):
  print "Adding %s" % contents
  instance_uuid = request.POST['instance_uuid']
  assert instance_uuid

  comment = contact.addComment(instance_uuid, contents)

  template = jinja.get_template('contacts/comment.html')
  return template.render(comment=comment)
