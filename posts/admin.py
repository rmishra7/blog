# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Post, Comment, Like

models = [Post, Comment, Like]

admin.site.register(models)
