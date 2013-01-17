__author__ = 'peter'

from flask import render_template
from application import settings
import logging
from intepreter import MSG_TYPE_IMAGE, MSG_TYPE_LOCATION, MSG_TYPE_TEXT
import time

def chant(remark):
    retort={'toUser':remark['fromUser'], 'fromUser':remark['toUser'], 'createTime':int(time.time())}
    if remark['msgType'] == MSG_TYPE_TEXT:
        if settings.DEBUG_MODE:
            logging.info('text message from %s', remark['fromUser'])
        retort['content'] = '/'.join(remark['content'])
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