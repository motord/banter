# -*- coding: utf-8 -*-
__author__ = 'peter'

from application import scrapemark
import logging
import re

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
     </xml>
    """)

def cdatarepl(matchobj):
    return matchobj.group(1)

text="""<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>1348831860</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[this is a test]]></Content>
</xml>"""

location="""
<xml>
 <ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName>
 <CreateTime>1351776360</CreateTime>
 <MsgType><![CDATA[location]]></MsgType>
 <Location_X>23.134521</Location_X>
 <Location_Y>113.358803</Location_Y>
 <Scale>20</Scale>
 <Label><![CDATA[位置信息]]></Label>
 </xml>
"""
image="""
<xml>
 <ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName>
 <CreateTime>1348831860</CreateTime>
 <MsgType><![CDATA[image]]></MsgType>
 <PicUrl><![CDATA[this is a url]]></PicUrl>
 </xml>
"""

if __name__ == "__main__":
    logging.error(dict([(k,v) for (k,v) in pattern.scrape(html=re.sub('<(\!\[CDATA\[.*\]\])>', cdatarepl, text))['message'].items() if v]))
    logging.error(dict([(k,v) for (k,v) in pattern.scrape(html=re.sub('<(\!\[CDATA\[.*\]\])>', cdatarepl, location))['message'].items() if v]))
    logging.error(dict([(k,v) for (k,v) in pattern.scrape(html=re.sub('<(\!\[CDATA\[.*\]\])>', cdatarepl, image))['message'].items() if v]))
