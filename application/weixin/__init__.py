# -*- coding: utf-8 -*-
__author__ = 'peter'

from flask import Blueprint, request, Response, render_template
from decorators import signature_verified, channel_required, bot_required
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

@qq.route('/create/<string:channel>')
@channel_required
def create_channel(channel):
    pass

@qq.route('/edit/<string:channel>/', methods=['GET', 'POST'])
@channel_required
def edit_channel(channel):
    return render_template('channel.html', channel=channel)

@qq.route('/delete/<string:channel>/', methods=['GET', 'POST'])
@channel_required
def delete_channel(channel):
    return render_template('channel.html', channel=channel)

@qq.route('/create/<string:channel>/<string:bot>', methods=['GET', 'POST'])
@channel_required
@bot_required
def create_bot(channel, bot):
    return render_template('bot.html', channel=channel, bot=bot)

@qq.route('/edit/<string:channel>/<string:bot>', methods=['GET', 'POST'])
@channel_required
@bot_required
def edit_bot(channel, bot):
    return render_template('bot.html', channel=channel, bot=bot)

@qq.route('/delete/<string:channel>/<string:bot>', methods=['GET', 'POST'])
@channel_required
@bot_required
def delete_bot(channel, bot):
    return render_template('bot.html', channel=channel, bot=bot)

