# -*- coding: utf-8 -*-
__author__ = 'peter'

from flask import Blueprint, request, Response
from decorators import signature_verified
from models import Channel, Conversation, Bot
import choir
import intepreter
import logging

qq = Blueprint('qq', __name__, template_folder='templates')

@qq.route('/<string:channel>/weixin', methods=['GET', 'POST'])
@signature_verified
def listen(channel):
    remark = intepreter.process(request.data)
    q=Conversation.gql("WHERE channel = :1 AND user = :2", channel, remark['fromUser'])
    c=q.get()
    if c:
        c.messages.append(request.data.decode('utf-8'))
    else:
        c=Conversation(channel=channel, user=remark['fromUser'], messages=[request.data.decode('utf-8')])
    c.put()
    retort=choir.chant(remark)
    c.messages.append(retort)
    c.put()
    return Response(retort, content_type='application/xml;charset=utf-8')


@qq.route('/weixin/populate', methods=['GET'])
def populate():
    return 'populated.'
