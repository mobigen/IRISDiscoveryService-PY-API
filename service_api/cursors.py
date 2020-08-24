#!/usr/bin/env python
# coding=UTF-8

from http.client import HTTPConnection
import json


class ApiError(Exception):
    pass


class Cursor(object):

    def __init__(self, token):

        self.http_conn = None
        self.token = token
        self.sid = None
        self.response = None
        self.fetchall_data = []

    def execute(self, q=None, size=None, save=None):
        """
        파라미터
        -------------
        :param q: 모델의 정보
        :param size: 해당 모델의 한번에 보여줄 행의 사이즈
        :param save: 저장 유무
        :return: 모델의 정보를 이용하여 가공한 데이터
        """

        if q is None:
            q = " "
        if size is None:
            size = 10
        if save is None:
            save = True

        self.headers["Accept"] = "application/json"
        self.headers["Content-Type"] = "application/json"
        self.headers["Authorization"] = "Angora %s" % self.token

        self.parameters['q'] = q
        self.parameters['size'] = size
        self.parameters['save'] = save

        body = json.dumps(self.parameters)

        self.http_conn.request("POST", "/angora/query/jobs", body=body, headers=self.headers)
        r = json.load(self.http_conn.getresponse())

        try:
            self.sid = r["sid"]
        except KeyError as err:
            raise ApiError("no search sid")

    def response_data(self):

        self.http_conn.request(
            "GET",
            "/angora/query/jobs/%s" % self.sid,
            headers=self.headers)
        self.response = json.loads(self.http_conn.getresponse().read())

        return self.response

    def fetchall(self):

        response = self.response_data()
        try:
            self.fetchall_data = response['results']

        except KeyError:
            return

        return self.fetchall_data

    def description(self):
        """
        # description result column format
        [ name, type, display_size, internal_size, precision, scale, null_ok ]
        """

        response = self.response_data()
        try:
            for fields_data in response['fields']:
                self.description_data.append([fields_data['name'], fields_data['type'], None, None, None, None, None])
                self.description_data_name.append([fields_data['name'], None, None, None, None, None, None])
                self.description_data_type.append([None, fields_data['type'], None, None, None, None, None])

        except KeyError:
            return ""

        return self.description_data_name

    def close(self):

        conn = self.http_conn
        if conn is None:
            pass
        else:
            self.http_conn = None
            print('cursor close')
