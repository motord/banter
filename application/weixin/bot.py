__author__ = 'peter'

from application import settings
import logging

MSG_TYPE_TEXT = u'text'
MSG_TYPE_LOCATION = u'location'
MSG_TYPE_IMAGE = u'image'

def process_text(remark, retort):
    if remark['content']:
        retort['content']=remark['content']
    retort['msgType']=MSG_TYPE_TEXT
    retort['funcFlag']=0
    return retort

def process_location(remark, retort):
    return retort

def process_image(remark, retort):
    return retort