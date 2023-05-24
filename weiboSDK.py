import json
import hashlib
import urllib.parse
from flask import request

# Documents: https://open.weibo.com/wiki/%E6%8E%A5%E6%94%B6%E6%99%AE%E9%80%9A%E6%B6%88%E6%81%AF
class FansMessage:
    def __init__(self):
        self.app_secret = "" # store app_secret

    # set your app_secret, see https://open.weibo.com/
    def setAppSecret(self, app_secret):
        self.app_secret = app_secret

    # Get contents from the message posted by WEIBO server.
    # You have to use request.data to analyze the message
    def getPostMsgStr(self):
        return json.loads(request.data)

    # Verify the server signature
    # Generate a SHA1 Hash by the combination of "app_secret, timestamp and nonce", and compare the Hash value to signature.
    # See Documents of https://open.weibo.com/
    def checkSignature(self, signature, timestamp, nonce):
        tmpArr = [self.app_secret, timestamp, nonce]
        tmpArr.sort()
        tmpStr = hashlib.sha1("".join(tmpArr).encode('utf-8')).hexdigest()

        if tmpStr == signature:
            return True
        else:
            return False

    # construct the message to return
    def buildReplyMsg(self, receiver_id, sender_id, data, type):
        msg = {
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "type": type,
            # Note: data need the urlencode
            "data": urllib.parse.quote(json.dumps(data))
        }
        return msg

    # Generate text type message
    def textData(self, text):
        data = {"text": text}
        return data

    # Generate article type message
    def articleData(self, articles):
        data = {"articles": articles}
        return data

    # Generate position type message
    def positionData(self, longitude, latitude):
        data = {
            "longitude": longitude,
            "latitude": latitude
        }
        return data
