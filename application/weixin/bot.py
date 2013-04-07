# -*- coding: utf-8 -*-
__author__ = 'peter'

import logging
from application.weixin.decorators import history_aware, context_aware
from application.weixin.fuzzy import decide

MSG_TYPE_TEXT = u'text'
MSG_TYPE_ARTICLE = u'news'
MSG_TYPE_LOCATION = u'location'
MSG_TYPE_IMAGE = u'image'
MSG_TYPE_LINK = u'link'
MSG_TYPE_EVENT = u'event'
MSG_TYPE_MUSIC = u'music'

def subscription(**kwargs):
    article={'title':u'欢迎关注方鸿渐和唐晓芙的微信公众号！', 'url':'http://qrcache.com', 'description':u"""我们的婚礼定于2013年4月1日（星期日）于上海市徐家汇圣依纳爵主教座堂举行，真诚邀请各位亲朋好友参加！

关注我们的微信号，可以：
1）及时收到动态提醒——会于婚礼/答谢宴前及时推送提醒给大家，也会发布现场情况
2）查询婚礼/答谢宴的地址及时间——回复“查询”
3）查看我们的结婚照——回复“照片”。如需查看单人照，回复“方鸿渐”(或“新郎”)或“唐晓芙(或“新娘”)”
4）查询婚礼日程——回复“日程”
5）了解我们的恋爱史——回复“八卦”
6）无聊调戏我们一下——随便问问题试试，比如“家里谁说了算”？，不定期回复哦

如想再次看到本帮助消息，请回复“帮助”。"""}
    return [article]

def photos(**kwargs):
    pics=['http://pic.yupoo.com/qrcache/CLM3rdrK/medish.jpg', 'http://pic.yupoo.com/qrcache/CLM3qg0x/medish.jpg', 'http://pic.yupoo.com/qrcache/CLNkDZb0/medish.jpg']
    history=kwargs['history']
    newpics=pics
    if history.content:
        try:
            newpics=[pic for pic in pics if pic not in history.content['photos']]
        except KeyError:
            pass
    else:
        history.content={'photos':[], 'bride':[], 'groom':[]}
    if len(newpics)==0:
        article={'title':u'您已看过我们所有的照片，再看一次？', 'picUrl':pics[0]}
        history.content['photos']=[pics[0]]
    else:
        article={'picUrl':newpics[0]}
        history.content['photos'].append(newpics[0])
    history.put()
    return [article]

def schedule(**kwargs):
    article={'title':u'我们的婚礼', 'description':u'定于2013年4月1日（星期日）于上海市徐家汇圣依纳爵主教座堂举行，真诚邀请各位亲朋好友参加！'}
    return [article]

def gossip(**kwargs):
    article={'title':u'我们的婚礼', 'description':u'定于2013年4月1日（星期日）于上海市徐家汇圣依纳爵主教座堂举行，真诚邀请各位亲朋好友参加！'}
    return [article]

def bride(**kwargs):
    pics=['http://pic.yupoo.com/qrcache/CLM3qg0x/medish.jpg', 'http://pic.yupoo.com/qrcache/CLNkDZb0/medish.jpg']
    history=kwargs['history']
    newpics=pics
    if history.content:
        try:
            newpics=[pic for pic in pics if pic not in history.content['bride']]
        except KeyError:
            pass
    else:
        history.content={'photos':[], 'bride':[], 'groom':[]}
    if len(newpics)==0:
        article={'title':u'您已看过新娘唐晓芙所有的照片，再看一次？', 'picUrl':pics[0]}
        history.content['bride']=[pics[0]]
    else:
        article={'picUrl':newpics[0]}
        history.content['bride'].append(newpics[0])
    history.put()
    return [article]

def groom(**kwargs):
    pics=['http://pic.yupoo.com/qrcache/CLMzfJBi/medish.jpg']
    history=kwargs['history']
    newpics=pics
    if history.content:
        try:
            newpics=[pic for pic in pics if pic not in history.content['groom']]
        except KeyError:
            pass
    else:
        history.content={'photos':[], 'bride':[], 'groom':[]}
    if len(newpics)==0:
        article={'title':u'您已看过新郎方鸿渐所有的照片，再看一次？', 'picUrl':pics[0]}
        history.content['groom']=[pics[0]]
    else:
        article={'picUrl':newpics[0]}
        history.content['groom'].append(newpics[0])
    history.put()
    return [article]

@history_aware
def process_text(remark, retort, **kwargs):
    articles=decide({u'帮助':subscription, u'照片':photos, u'日程':schedule, u'八卦':gossip, u'唐晓芙':bride, u'方鸿渐':groom, u'新娘':bride, u'新郎':groom}, remark['content'])(history=kwargs['history'])
    retort['articles']=articles
    retort['articleCount']=len(articles)
    retort['msgType']=MSG_TYPE_ARTICLE
    retort['funcFlag']=0
    return retort

def process_location(remark, retort, **kwargs):
    return retort

def process_image(remark, retort, **kwargs):
    return retort

def process_link(remark, retort, **kwargs):
    return retort

def process_event(remark, retort, **kwargs):
    if remark['event']=='subscribe':
        articles=subscription()
        retort['articles']=articles
        retort['articleCount']=len(articles)
        retort['msgType']=MSG_TYPE_ARTICLE
    if remark['event']=='unsubscribe':
        retort['content']='Unsubscribed!'
        retort['msgType']=MSG_TYPE_TEXT
    if remark['event']=='CLICK':
        retort['content']=remark['eventkey']+' clicked!'
        retort['msgType']=MSG_TYPE_TEXT
    retort['funcFlag']=0
    return retort