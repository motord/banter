__author__ = 'peter'

from flask import render_template
import logging
import time
import bot
from models import  Bot
import sys
from google.appengine.ext import db
from decorators import cached, invalidate_cache

MSG_TYPE_TEXT = u'text'
MSG_TYPE_LOCATION = u'location'
MSG_TYPE_IMAGE = u'image'

def import_module(channel, bot):
        # Has this module already been loaded? If so, move on
        for mod in sys.modules.keys():
            if mod == bot.name:
                # module found
                logging.info('Module already loaded ({0})'.format(bot.name))
                return sys.modules[mod]
        bot_name=bot.name.encode('utf-8')
        channel_id=channel.id.encode('utf-8')
        module = sys.modules[bot_name] = type(sys)(bot_name)
        module.__dict__['__file__'] = '.'.join([channel_id, bot_name])
        bot_code=compile(bot.code, filename='.'.join([channel_id, bot_name]), mode='exec')
        try:
            exec bot_code in module.__dict__
        except:
            # Module failed to load? Unload it?
            logging.info('execute {0} error'.format(bot.name))
            del sys.modules[bot.name]
        return module

@invalidate_cache
def LoadBot(channel, bot):
    # Call the import function
    bot=import_module(channel, bot)
    return bot

@invalidate_cache
def ReloadBot(channel, bot):
    UnloadBot(bot)
    bot=LoadBot(bot)
    logging.info('Reload Bot ({0})'.format(bot.name))
    return bot

@invalidate_cache
def UnloadBot(channel, bot):
    if sys.modules.has_key(bot):
        logging.info('Remove Bot ({0})'.format(bot.name))
    del sys.modules[bot]

@invalidate_cache
def ReloadAllBots(channel, bot):
    # Get the list of modules from the database and load them all
    q=Bot.gql("WHERE channel = :1 AND activated = True", channel.key)
    for bot in q:
        ReloadBot(channel, bot)

@cached()
def chant(remark):
    retort={'toUser':remark['fromUser'], 'fromUser':remark['toUser'], 'createTime':int(time.time())}
    channel=remark['channel']
    q=Bot.gql("WHERE channel = :1 AND activated = True", channel.key)
    for bot in q:
        module=LoadBot(channel, bot)
        retort = {MSG_TYPE_TEXT: module.process_text,
                  MSG_TYPE_IMAGE: module.process_image,
                  MSG_TYPE_LOCATION: module.process_location}[remark['msgType']](remark, retort)
    retort['message']=render_template('message.xml', message=retort)
    logging.info(retort['message'])
    return retort