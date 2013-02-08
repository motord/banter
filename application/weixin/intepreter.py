__author__ = 'peter'

from application import scrapemark
import re

def cdatarepl(matchobj):
    return matchobj.group(1)

def parse(message):
    pattern=scrapemark.compile("""
     <xml>
     <ToUserName>![CDATA[{{ message.toUser }}]]</ToUserName>
     <FromUserName>![CDATA[{{ message.fromUser }}]]</FromUserName>
     <CreateTime>{{ message.createTime }}</CreateTime>
     <MsgType>![CDATA[{{ message.msgType }}]]</MsgType>
     {*
     <Content>![CDATA[{{ message.content }}]]</Content>
     *}
     {*
     <Location_X>{{ message.locationX }}</Location_X>
     <Location_Y>{{ message.localtionY }}</Location_Y>
     <Scale>20</Scale>
     <Label>![CDATA[{{ message.label }}]]</Label>*}
     {*
     <PicUrl>![CDATA[{{ message.picUrl }}]]</PicUrl>
     *}
     {*
     <Title>![CDATA[{{ message.title }}]]</Title>
     <Description>![CDATA[{{ message.description }}]]</Description>
     <Url>![CDATA[{{ message.url }}]]</Url>
     *}
     {*
     <Event>![CDATA[{{ message.location }}]]</Event>
     <Latitude>{{ message.latitude }}</Latitude>
     <Longitude>{{ message.longtitude }}</Longitude>
     <Precision>{{ message.precision }}</Precision>
     *}
     {*
     <MsgId>{{ message.msgId }}</MsgId>
     *}
     </xml>
    """)
    msg=dict([(k,v) for (k,v) in pattern.scrape(html=re.sub('<(\!\[CDATA\[.*\]\])>', cdatarepl, message))['message'].items() if v])
    msg['message']=message
    msg['createTime']=int(msg['createTime'])
    return msg

