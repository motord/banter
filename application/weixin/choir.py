__author__ = 'peter'

import logging
import time
import bot

def chant(remark):
    retort={'toUser':remark['fromUser'], 'fromUser':remark['toUser'], 'createTime':int(time.time())}
    return bot.process(remark, retort)
