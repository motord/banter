import logging
from application.weixin.decorators import cached, history_aware, context_aware, paragraphical, musical
from application.weixin.fuzzy import decide

MSG_TYPE_TEXT = u'text'
MSG_TYPE_ARTICLE = u'news'
MSG_TYPE_LOCATION = u'location'
MSG_TYPE_IMAGE = u'image'
MSG_TYPE_LINK = u'link'
MSG_TYPE_EVENT = u'event'
MSG_TYPE_MUSIC = u'music'

@cached()
@paragraphical
def subscription(remark, retort, **kwargs):
    article={'title':u'欢迎关注方鸿渐和唐晓芙的微信公众号！', 'url':'http://qrcache.com', 'description':u"""我们的婚礼定于2013年4月1日（星期日）于上海市徐家汇圣依纳爵主教座堂举行，真诚邀请各位亲朋好友参加！

关注我们的微信号，可以：
1）及时收到动态提醒——会于婚礼/答谢宴前及时推送提醒给大家，也会发布现场情况
2）查询婚礼的地址及时间——回复“查询”
3）查看我们的结婚照——回复“照片”。如需查看单人照，回复“方鸿渐”(或“新郎”)或“唐晓芙(或“新娘”)”
4）查询婚礼日程——回复“日程”
5）了解我们的恋爱史——回复“八卦”
6）听一下我们的OST，回复“音乐”
7）无聊调戏我们一下——随便问问题试试，比如“家里谁说了算”？，不定期回复哦

如想再次看到本帮助消息，请回复“帮助”。"""}
    return [article]

@musical
@history_aware
def music(remark, retort, **kwargs):
    songs=[{'title': 'Come Away With Me', 'artist': 'Norah Jones', 'mp3': 'http://wedbliss.b0.upaiyun.com/ComeAwayWithMeNorahJones.mp3'},
           {'title': 'Marry Me', 'artist': 'Train', 'mp3': 'http://wedbliss.b0.upaiyun.com/MarryMeTrain.mp3'}]
    history=kwargs['history']
    newsongs=songs
    if history.content:
        try:
            newsongs=[song for song in songs if song not in history.content['music']]
        except KeyError:
            pass
    else:
        history.content={'photos':[], 'bride':[], 'groom':[], 'music':[]}
    if len(newsongs)==0:
        retort['title']=songs[0]['artist']
        retort['description']=songs[0]['title']
        retort['musicUrl']=songs[0]['mp3']
        retort['hQMusicUrl']=songs[0]['mp3']
        history.content['music']=[songs[0]]
    else:
        retort['title']=newsongs[0]['artist']
        retort['description']=newsongs[0]['title']
        retort['musicUrl']=newsongs[0]['mp3']
        retort['hQMusicUrl']=newsongs[0]['mp3']
        history.content['music'].append(newsongs[0])
    history.put()
    return retort

@paragraphical
@history_aware
def photos(remark, retort, **kwargs):
#    pics=['http://pic.yupoo.com/qrcache/CLM3rdrK/medish.jpg', 'http://pic.yupoo.com/qrcache/CLM3qg0x/medish.jpg', 'http://pic.yupoo.com/qrcache/CLNkDZb0/medish.jpg']
#    teddy
    pics=['http://pic.yupoo.com/qrcache/CLZw20O2/small.jpg', 'http://pic.yupoo.com/qrcache/CLZwo5ID/small.jpg', 'http://pic.yupoo.com/qrcache/CLZwnxuK/small.jpg']
    history=kwargs['history']
    newpics=pics
    if history.content:
        try:
            newpics=[pic for pic in pics if pic not in history.content['photos']]
        except KeyError:
            pass
    else:
        history.content={'photos':[], 'bride':[], 'groom':[], 'music':[]}
    if len(newpics)==0:
        article={'title':u'您已看过我们所有的照片，再看一次？', 'picUrl':pics[0]}
        history.content['photos']=[pics[0]]
    else:
        article={'picUrl':newpics[0]}
        history.content['photos'].append(newpics[0])
    history.put()
    return [article]

@cached()
@paragraphical
def schedule(remark, retort, **kwargs):
    article={'title':u'我们的婚礼', 'description':u'定于2013年4月1日（星期日）于上海市徐家汇圣依纳爵主教座堂举行，真诚邀请各位亲朋好友参加！'}
    return [article]

@cached()
@paragraphical
def gossip(remark, retort, **kwargs):
    article={'title':u'我们的婚礼', 'description':u'定于2013年4月1日（星期日）于上海市徐家汇圣依纳爵主教座堂举行，真诚邀请各位亲朋好友参加！'}
    return [article]

@paragraphical
@history_aware
def bride(remark, retort, **kwargs):
#    pics=['http://pic.yupoo.com/qrcache/CLM3qg0x/medish.jpg', 'http://pic.yupoo.com/qrcache/CLNkDZb0/medish.jpg']
#    teddy
    pics=['http://pic.yupoo.com/qrcache/CLZwpNda/small.jpg', 'http://pic.yupoo.com/qrcache/CLZyZ7wn/medish.jpg']
    history=kwargs['history']
    newpics=pics
    if history.content:
        try:
            newpics=[pic for pic in pics if pic not in history.content['bride']]
        except KeyError:
            pass
    else:
        history.content={'photos':[], 'bride':[], 'groom':[], 'music':[]}
    if len(newpics)==0:
        article={'title':u'您已看过新娘唐晓芙所有的照片，再看一次？', 'picUrl':pics[0]}
        history.content['bride']=[pics[0]]
    else:
        article={'picUrl':newpics[0]}
        history.content['bride'].append(newpics[0])
    history.put()
    return [article]

@paragraphical
@history_aware
def groom(remark, retort, **kwargs):
#    pics=['http://pic.yupoo.com/qrcache/CLMzfJBi/medish.jpg']
#    teddy
    pics=['http://pic.yupoo.com/qrcache/CLZwqrkc/medish.jpg', 'http://pic.yupoo.com/qrcache/CLZw31RG/medish.jpg']
    history=kwargs['history']
    newpics=pics
    if history.content:
        try:
            newpics=[pic for pic in pics if pic not in history.content['groom']]
        except KeyError:
            pass
    else:
        history.content={'photos':[], 'bride':[], 'groom':[], 'music':[]}
    if len(newpics)==0:
        article={'title':u'您已看过新郎方鸿渐所有的照片，再看一次？', 'picUrl':pics[0]}
        history.content['groom']=[pics[0]]
    else:
        article={'picUrl':newpics[0]}
        history.content['groom'].append(newpics[0])
    history.put()
    return [article]

def process_text(remark, retort, **kwargs):
    retort=decide({u'帮助':subscription, u'照片':photos, u'日程':schedule, u'八卦':gossip, u'唐晓芙':bride, u'方鸿渐':groom, u'新娘':bride, u'新郎':groom, u'音乐':music}, remark['content'])(remark, retort)
    return retort

def process_location(remark, retort, **kwargs):
    return retort

def process_image(remark, retort, **kwargs):
    return retort

def process_link(remark, retort, **kwargs):
    return retort

def process_event(remark, retort, **kwargs):
    if remark['event']=='subscribe':
        retort=subscription(remark, retort)
        return retort
    if remark['event']=='unsubscribe':
        retort['content']='Unsubscribed!'
        retort['msgType']=MSG_TYPE_TEXT
    if remark['event']=='CLICK':
        retort['content']=remark['eventkey']+' clicked!'
        retort['msgType']=MSG_TYPE_TEXT
    retort['funcFlag']=0
    return retort