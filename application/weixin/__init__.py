# -*- coding: utf-8 -*-
__author__ = 'peter'

from flask import Blueprint, request, Response, render_template
from decorators import signature_verified, channel_required, bot_required
from models import Channel, Message, Bot
import choir
import intepreter
import logging
from application.decorators import admin_required

qq = Blueprint('qq', __name__, template_folder='templates')

@qq.route('/<string:channel>/weixin', methods=['GET', 'POST'])
@signature_verified
def listen(channel):
    remark = intepreter.parse(request.data)
    message=Message(channel=channel, from_user=remark['fromUser'],
        to_user=remark['toUser'], create_time=remark['createTime'],
        message_type=remark['msgType'], message=remark['message'])
    message.put()
    remark['channel']=channel
    retort=choir.chant(remark)
    message=Message(channel=channel, from_user=retort['fromUser'],
        to_user=retort['toUser'], create_time=retort['createTime'],
        message_type=retort['msgType'], message=retort['message'])
    message.put()
    return Response(retort, content_type='application/xml;charset=utf-8')


@admin_required
@qq.route('/weixin/populate', methods=['GET'])
def populate():
    q=Channel.gql("WHERE id=:1", 'koan')
    channel=q.get()
    code="""
__author__ = 'peter'

from application import settings
import logging

MSG_TYPE_TEXT = u'text'
MSG_TYPE_LOCATION = u'location'
MSG_TYPE_IMAGE = u'image'

def process_text(remark, retort):
    if remark['content']:
        retort['content']='Bot Spawned!'
    retort['msgType']=MSG_TYPE_TEXT
    retort['funcFlag']=0
    return retort

def process_location(remark, retort):
    return retort

def process_image(remark, retort):
    return retort
    """
    bot=Bot(name=u'v2ex', code=code, channel=channel)
    bot.put()
    return 'populated.'

@admin_required
@qq.route('/create/<string:channel>')
@channel_required
def create_channel(channel):
    return render_template('new_channel.html', channel=channel)

@admin_required
@qq.route('/edit/<string:channel>/', methods=['GET', 'POST'])
@channel_required
def edit_channel(channel):
    return render_template('edit_channel.html', channel=channel)

@admin_required
@qq.route('/delete/<string:channel>/', methods=['GET', 'POST'])
@channel_required
def delete_channel(channel):
    return render_template('channel.html', channel=channel)

@admin_required
@qq.route('/create/<string:channel>/<string:bot>', methods=['GET', 'POST'])
@channel_required
@bot_required
def create_bot(channel, bot):
    return render_template('new_bot.html', channel=channel, bot=bot)

@admin_required
@qq.route('/edit/<string:channel>/<string:bot>', methods=['GET', 'POST'])
#@channel_required
#@bot_required
def edit_bot(channel, bot):
#    return render_template('edit_bot.html', channel=channel, bot=bot)
    return render_template('edit_bot.html')

@admin_required
@qq.route('/delete/<string:channel>/<string:bot>', methods=['GET', 'POST'])
@channel_required
@bot_required
def delete_bot(channel, bot):
    return render_template('bot.html', channel=channel, bot=bot)

