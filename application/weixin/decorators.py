__author__ = 'peter'

from flask import request, redirect
from models import Channel, Message, Bot
from hashlib import sha1
from functools import wraps

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
