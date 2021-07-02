#!/usr/bin/env python
# coding=UTF-8
import json

from http.client import HTTPConnection


class Connection(object):

    def __init__(self, host=None, port=None, user_id=None, user_passwd=None):
        self.host = host
        self.port = port
        self.user_id = user_id
        self.user_passwd = user_passwd
        self.token = None

    def cursor(self):
        if self.token is not None:
            return self
        else:
            raise SyntaxError("no token")

    def connect(self, host=None, port=None, user_id=None, user_passwd=None):
        if host is None:
            host = ""
        if port is None:
            port = 6036
        if user_id is None:
            user_id = "root"
        if user_passwd is None:
            user_passwd = ''

        self.http_conn = HTTPConnection(host, port)

        self.http_conn.request(
            "POST",
            "/angora/auth",
            json.dumps({"id": user_id, "password": user_passwd}))

        self.token = json.load(self.http_conn.getresponse())["token"]

        return self
