import requests
from flask import Flask, request, jsonify
import itchat
import itchat.content
import itchat.config
import farpush
import socket
import json
import _thread

app = Flask(__name__)


@app.route("/send", methods=['POST'])
def received():
    data = request.json
    username = data['username']
    nametype = data['type']
    content = data['content']
    if nametype == '0':
        send4nick(username, content)
    else:
        send(username, content)
    return 'ok'


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    print((msg.user.remarkName or msg.user.nickName) + " 说 : " + msg.text)
    farpush.mespush((msg.user.remarkName or msg.user.nickName), msg.text)


@itchat.msg_register(itchat.content.MEDIA_TYPE_MSG)
def text_media(msg):
    if msg.type in itchat.content.MESSAGE_TEXT:
        msgtext = itchat.content.MESSAGE_TEXT[msg.type]
    else:
        msgtext = '未定义类型'
    print((msg.user.remarkName or msg.user.nickName) + " 发送了 : " + msgtext)
    farpush.mespush((msg.user.remarkName or msg.user.nickName), msgtext)


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_reply(msg):
    farpush.mespush(msg.user.nickName, msg.text)


def send(username, content):
    itchat.send(content, toUserName=username)


def send4nick(nickname, content):
    friends = itchat.search_friends(name=nickname)
    if friends:
        author = friends[0]
        author.send(content)


def flask(ip, port):
    from waitress import serve
    serve(app, host=ip, port=port)


if __name__ == '__main__':
    _thread.start_new_thread(flask, ('0.0.0.0', 9091))
    itchat.check_login()
    itchat.auto_login(hotReload=True, enableCmdQR=2)
    itchat.run()
