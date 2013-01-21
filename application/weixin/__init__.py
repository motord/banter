# -*- coding: utf-8 -*-
__author__ = 'peter'

from flask import Blueprint, request, Response, render_template, flash, redirect, url_for
from decorators import signature_verified, channel_required, bot_required
from models import Channel, Message, Bot
import choir
import intepreter
import logging
from application.decorators import admin_required
from forms import ChannelForm
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

qq = Blueprint('qq', __name__, template_folder='templates')

@qq.route('/<string:channel>/weixin', methods=['GET', 'POST'])
@signature_verified
def listen(channel):
    remark = intepreter.parse(request.data)
    message=Message(channel=channel.key, from_user=remark['fromUser'],
        to_user=remark['toUser'], create_time=remark['createTime'],
        message_type=remark['msgType'], message=remark['message'])
    message.put()
    remark['channel']=channel
    retort=choir.chant(remark)
    message=Message(channel=channel.key, from_user=retort['fromUser'],
        to_user=retort['toUser'], create_time=retort['createTime'],
        message_type=retort['msgType'], message=retort['message'])
    message.put()
    return Response(retort['message'], content_type='application/xml;charset=utf-8')


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
    bot=Bot(name=u'spawn', code=code, channel=channel.key)
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
    try:
        channel.key.delete()
        flash(u'Channel %s successfully deleted.' % channel.name, 'success')
        return redirect(url_for('qq.list_channels'))
    except CapabilityDisabledError:
        flash(u'App Engine Datastore is currently in read-only mode.', 'info')
        return redirect(url_for('qq.list_channels.html'))

@admin_required
@qq.route('/new/<string:channel>', methods=['GET', 'POST'])
@channel_required
def new_bot(channel):
    return render_template('new_bot.html', channel=channel)

@admin_required
@qq.route('/edit/<string:channel>/<string:bot>', methods=['GET', 'POST'])
@channel_required
@bot_required
def edit_bot(channel, bot):
    return render_template('edit_bot.html', channel=channel, bot=bot)

@admin_required
@qq.route('/delete/<string:channel>/<string:bot>', methods=['GET', 'POST'])
@channel_required
@bot_required
def delete_bot(channel, bot):
    try:
        bot.key.delete()
        flash(u'Bot %s successfully deleted.' % bot.name, 'success')
        return redirect(url_for('qq.list_bots', channel=channel.id))
    except CapabilityDisabledError:
        flash(u'App Engine Datastore is currently in read-only mode.', 'info')
        return redirect(url_for('qq.list_bots.html', channel=channel.id))

@qq.route('/channels', methods=['GET', 'POST'])
def list_channels():
    """List all channels"""
    channels = Channel.query()
    form = ChannelForm()
    if form.validate_on_submit():
        channel = Channel(
            id = form.id.data,
            name = form.name.data,
            token = form.token.data,
        )
        try:
            channel.put()
            flash(u'Channel %s successfully saved.' % channel.id, 'success')
            return redirect(url_for('list_channels'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_channels'))
    return render_template('list_channels.html', channels=channels, form=form)

@qq.route('/bots/<string:channel>', methods=['GET'])
@channel_required
def list_bots(channel):
    """List channel bots"""
    bots = Bot.query(Bot.channel==channel.key)
    return render_template('list_bots.html', channel=channel, bots = bots)
