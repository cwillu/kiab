import models

from django.contrib import admin

from django import forms
from django.forms.widgets import *
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.html import escape 

import re
import json
from itertools import chain

admin.site.register(models.classes)
