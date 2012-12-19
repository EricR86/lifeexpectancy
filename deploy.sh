#!/bin/bash
cp -u -v -r . /usr/local/django/lifeleft | grep -v \.git
rm -r /usr/local/django/lifeleft/.git
rm /usr/local/django/lifeleft/.gitignore
touch /usr/local/django/lifeleft/apache/django.wsgi
