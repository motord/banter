__author__ = 'peter'

from google.appengine.ext import ndb
from flask import jsonify
from google.appengine.api import users

class Channel(ndb.Model):
    id = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    token = ndb.StringProperty(required=True)
    qrcode=ndb.BlobProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)

class Bot(ndb.Model):
    name = ndb.StringProperty(required=True)
    code = ndb.TextProperty(required=True)
    channel = ndb.ReferenceProperty(Channel, collection_name='bots')
    activated = ndb.BooleanProperty(required=True, default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)

class Message(ndb.Model):
    channel = ndb.ReferenceProperty(Channel, collection_name='messages')
    from_user = ndb.StringProperty(required=True)
    to_user = ndb.StringProperty(required=True)
    create_time = ndb.IntegerProperty(required=True)
    message_type = ndb.StringProperty(required=True)
    message=ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)