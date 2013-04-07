__author__ = 'peter'

from flask import request, redirect, render_template, url_for
from models import Channel, Message, Bot, History, Context
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
        if c:
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
        channel=Channel.gql("WHERE id = :1", channel).get()
        if channel:
            kwargs['channel']=channel
            return func(*args, **kwargs)
        return redirect(url_for('qq.list_channels'))
    return decorated_view

def bot_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        channel=kwargs['channel']
        bot=kwargs['bot']
        bot=Bot.gql("WHERE name = :1", bot).get()
        if bot:
            kwargs['bot']=bot
            return func(*args, **kwargs)
        return redirect(url_for('qq.list_bots', channel=channel.id))
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
            channel=remark['channel']
            user=remark['fromUser']
            history_key='{0}::{1}'.format(channel.key.urlsafe(), user)
            hk=memcache.get(history_key)
            h=None
            if not hk:
                q=History.gql("WHERE channel = :1 AND user = :2", channel.key, user)
                h=q.get()
                if h:
                    hk=h.key
                    memcache.set(history_key, hk, time=timeout)
            key = cache_key(remark)
            if not hk:
                retort = memcache.get(key)
                if retort:
                    logging.info('cache hit: {0}'.format(key))
                    return parrot(retort, remark)
            else:
                logging.info('history disables cache')
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

def history_aware(func):
    @wraps(func)
    def decorated(remark, retort, **kwargs):
        channel=remark['channel']
        user=remark['fromUser']
        history_key='{0}::{1}'.format(channel.key.urlsafe(), user)
        hk=memcache.get(history_key)
        h=None
        if not hk:
            q=History.gql("WHERE channel = :1 AND user = :2", channel.key, user)
            h=q.get()
        if not h:
            h=History(channel=channel.key, user=user)
            hk=h.put()
        else:
            hk=h.key
        memcache.set(history_key, hk, time=300)
        kwargs['history']=h
        return func(remark, retort, **kwargs)
    return decorated

def context_aware(func):
    @wraps(func)
    def decorated(remark, retort, **kwargs):
        channel=remark['channel']
        user=remark['fromUser']
        q=Context.gql("WHERE channel = :1 AND user = :2", channel.key, user)
        c=q.get()
        if not c:
            c=Context(channel=channel.key, user=user)
            c.put()
        kwargs['context']=c
        return func(remark, retort, **kwargs)
    return decorated