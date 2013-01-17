__author__ = 'peter'

from google.appengine.ext import db
from flask import jsonify
from google.appengine.api import users

class Channel(db.Model):
    id = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    token = db.StringProperty(required=True)
    qrcode=db.BlobProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)

class Bot(db.Model):
    code = db.StringProperty(required=True)
    channel = db.ReferenceProperty(Channel)
    published = db.BooleanProperty(required=True, default=False)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)

class Conversation(db.Model):
    channel = db.ReferenceProperty(Channel)
    user = db.StringProperty(required=True)
    messages=db.ListProperty(unicode)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)