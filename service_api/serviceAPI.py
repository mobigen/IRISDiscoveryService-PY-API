#!/usr/bin/env python
# coding=UTF-8
import json
from http.client import HTTPConnection
import sys


class DiscoveryService:

    def __init__(self):
        self.headers = {}
        self.parameters = {}
        self.fetchall_data = []
        self.description_data = []
        self.description_data_type = []
        self.description_data_name = []

    def connect_data(self, addr=None, port=None):
        if addr is None:
            addr = ""
        if port is None:
            port = 6036

        self.addr = addr
        self.port = port

    def parameter(self, q=None, size=None, save=None):

        if q is None:
            q = " "
        if size is None:
            size = 10
        if save is None:
            save = True

        self.parameters['q'] = q
        self.parameters['size'] = size
        self.parameters['save'] = save

    def user_info(self, user_id=None, user_passwd=None):

        if user_id is None:
            user_id = "root"
        if user_passwd is None:
            user_passwd = ''

        self.user_id = user_id
        self.user_passwd = user_passwd

    def cursor(self):

        self.http_conn = HTTPConnection(self.addr, self.port)

        self.http_conn.request(
            "POST",
            "/angora/auth",
            json.dumps({"id": self.user_id, "password": self.user_passwd}))

        self.token = json.load(self.http_conn.getresponse())["token"]

        return self.token

    def execute(self, token):

        self.headers["Accept"] = "application/json"
        self.headers["Content-Type"] = "application/json"
        self.headers["Authorization"] = "Angora %s" % self.token
        body = json.dumps(self.parameters)

        self.http_conn.request("POST", "/angora/query/jobs", body=body, headers=self.headers)
        r = json.load(self.http_conn.getresponse())

        try:
            self.sid = r["sid"]
        except Exception as e:
            sys.exit()

    def fetchall(self):

        self.http_conn.request(
            "GET",
            "/angora/query/jobs/%s" % self.sid,
            headers=self.headers)
        self.response = json.loads(self.http_conn.getresponse().read())

        # try:
        #    for data in self.response['fields']:
        #        print(data)
        # except:
        #    pass

        self.fetchall_data = self.response['results']

        return self.fetchall_data

    def description(self):
        """
        # description result column format
        [ name, type, display_size, internal_size, precision, scale, null_ok ]
        """
        for fields_data in self.response['fields']:
            self.description_data.append([fields_data['name'], fields_data['type'], None, None, None, None, None])
            self.description_data_name.append([fields_data['name'], None, None, None, None, None, None])
            self.description_data_type.append([None, fields_data['type'], None, None, None, None, None])

        return self.description_data_name

    def close(self):
        self.http_conn.close()


if __name__ == '__main__':
    conn = DiscoveryService()
    conn.connect_data("192.168.100.180", 6036)
    conn.parameter("model name = 'syslog' model_owner = eva start_date = 20200820153500 end_date = 20200820153611", 10, True)
    conn.user_info("root", "biris.manse")
    cursor = conn.cursor()
    conn.execute(cursor)
    print(conn.fetchall())
    print(conn.description())
    print(conn.description_data_name)
    print(conn.description_data_type)
    conn.close()
