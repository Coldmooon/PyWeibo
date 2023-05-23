import sys
import hashlib
import json
from flask import Flask, request

from weiboSDK import CallbackSDK

# set app_secret of your WEIBO application. See http://api.weibo.com
app_secret = "5fda2753c4af0e8c02fdb8afb92a8f0c"

# Initialize  weiboSDK
call_back_SDK = CallbackSDK()
call_back_SDK.setAppSecret(app_secret)

# Verify the signature of a message posted by WEIBO
def verify():
    signature = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")
    if not call_back_SDK.checkSignature(signature, timestamp, nonce):
        return "check signature error"

    # For the first URL verification, the message contains a "echostr" keyword.
    # You need to return the "echostr" back to the WEIBO server.
    if request.args.get("echostr"):
        return request.args.get("echostr")

    # Process the WEIBO message posted by WEIBO server.
    post_msg_str = call_back_SDK.getPostMsgStr()

    # Set the return string to empty
    # Note that the WEIBO server require UTF8 encode.
    # The WEIBO server determine "POST SUCCESS" if receiving a HTTP 200 status code.
    # or it will repost the message three times.
    str_return = ""

    if post_msg_str:
        text_received = post_msg_str["text"]
        
        # When return a message, the sender_id should be the receiver_id of the message posted by WEIBO server.
        sender_id = post_msg_str["receiver_id"]
        # Similarly, the receiver_id should be your weibo fans.
        receiver_id = post_msg_str["sender_id"]

        # There are multiple message type.
        # For "text" message example
        data_type = "text"
        data = call_back_SDK.textData("真不错啊！好看！")

        # For articles message:
        # data_type = "articles"
        # article_data = [
        #     {
        #         "display_name": "第一个故事",
        #         "summary": "今天讲两个故事，分享给你。谁是公司？谁又是中国人？",
        #         "image": "http://storage.mcp.weibo.cn/0JlIv.jpg",
        #         "url": "http://e.weibo.com/mediaprofile/article/detail?uid=1722052204&aid=983319"
        #     },
        #     {
        #         "display_name": "第二个故事",
        #         "summary": "今天讲两个故事，分享给你。谁是公司？谁又是中国人？",
        #         "image": "http://storage.mcp.weibo.cn/0JlIv.jpg",
        #         "url": "http://e.weibo.com/mediaprofile/article/detail?uid=1722052204&aid=983319"
        #     }
        # ]
        # data = call_back_SDK.articleData(article_data)

        # For position message:
        # data_type = "position"
        # longitude = "123.01"
        # latitude = "154.2"
        # data = call_back_SDK.positionData(longitude, latitude)
        
        str_return = call_back_SDK.buildReplyMsg(receiver_id, sender_id, data, data_type)

    return json.dumps(str_return)
