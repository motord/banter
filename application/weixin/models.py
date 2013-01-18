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
    name = db.StringProperty(required=True)
    code = db.TextProperty(required=True)
    channel = db.ReferenceProperty(Channel, collection_name='bots')
    published = db.BooleanProperty(required=True, default=False)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)

class Conversation(db.Model):
    channel = db.ReferenceProperty(Channel, collection_name='conversations')
    user = db.StringProperty(required=True)
    messages=db.ListProperty(unicode)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)