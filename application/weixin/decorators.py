__author__ = 'peter'

from flask import request, redirect, render_template
from models import Channel, Message, Bot
from hashlib import sha1
from functools import wraps
import time
import re
import logging

from google.appengine.api import memcache

def signature_verified(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        signature=request.args.get('signature')
        timestamp=request.args.get('timestamp')
        nonce=request.args.get('nonce')
        echostr=request.args.get('echostr')
        channel=kwargs['channel']
        q=Channel.gql("WHERE id = :1", channel)
        c=q.get()
        if q:
            kwargs['channel']=c
            token=c.token
            if sha1(''.join(sorted([token, timestamp, nonce]))).hexdigest()==signature:
                if request.method=='GET':
                    return echostr
                else:
                    return func(*args, **kwargs)
        return func(*args, **kwargs)
    return decorated_view

def channel_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        channel=kwargs['channel']
        q=Channel.gql("WHERE id = :1", channel)
        c=q.get()
        if q:
            kwargs['channel']=c
            return func(*args, **kwargs)
        return func(*args, **kwargs)
    return decorated_view

def bot_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        bot=kwargs['bot']
        q=Bot.gql("WHERE name = :1", bot)
        b=q.get()
        if q:
            kwargs['bot']=b
            return func(*args, **kwargs)
        return func(*args, **kwargs)
    return decorated_view

def cache_key(remark):
    message=re.sub(r'\s','',remark['message'])
    key=re.sub(r'^<xml><ToUserName>.*</ToUserName><FromUserName>.*</FromUserName><CreateTime>.*</CreateTime>(.*)<MsgId>.*</MsgId></xml>$', r'\1', message)
    return key

def parrot(retort, remark):
    retort['toUser']=remark['fromUser']
    retort['fromUser']=remark['toUser']
    retort['createTime']=int(time.time())
    retort['message']=render_template('message.xml', message=retort)
    return retort

def cached(timeout=300):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            remark=args[0]
            key = cache_key(remark)
            logging.info(key)
            retort = memcache.get(key)
            if retort:
                logging.info('cache hit: {0}'.format(key))
                return parrot(retort, remark)
            retort = f(*args, **kwargs)
            memcache.set(key, retort, time=timeout)
            return retort
        return decorated_function
    return decorator

def invalidate_cache(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        memcache.flush_all()
        return func(*args, **kwargs)
    return decorated_function
