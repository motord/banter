__author__ = 'peter'

from flask import render_template
from application import settings
import logging

MSG_TYPE_TEXT = u'text'
MSG_TYPE_LOCATION = u'location'
MSG_TYPE_IMAGE = u'image'

def process(remark, retort):
    if remark['msgType'] == MSG_TYPE_TEXT:
        if settings.DEBUG_MODE:
            logging.info('text message from %s', remark['fromUser'])
        if remark['content']:
            retort['content']=remark['content']
        retort['msgType']=MSG_TYPE_TEXT
        retort['funcFlag']=0
        retort=render_template('message.xml', message=retort)
        logging.info(retort)
        if settings.DEBUG_MODE:
            logging.info('Replied to %s with "%s"', remark['fromUser'], remark)
    elif remark['msgType'] == MSG_TYPE_LOCATION:
        if settings.DEBUG_MODE:
            logging.info('location message from %s', remark['fromUser'])
    elif remark['msgType'] == MSG_TYPE_IMAGE:
        if settings.DEBUG_MODE:
            logging.info('image message  from %s', remark['fromUser'])
    else:
        logging.info('message type unknown')
    return retort