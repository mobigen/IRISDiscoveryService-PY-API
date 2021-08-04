#!/usr/bin/env python
# coding=UTF-8

import json


class ApiError(Exception):
    pass


class Cursor(object):

    def __init__(self):

        self.http_conn = None
        self.token = None
        self.sid = None
        self.response = None
        self.fetchall_data = []
        self.headers = {}
        self.parameters = {}
        self.description_data = []
        self.description_data_name = []
        self.description_data_type = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def execute(self, q=None, size=None):
        """
        파라미터
        -------------
        :param q: 모델의 정보
        :param size: 해당 모델의 한번에 보여줄 행의 사이즈
        :return: 모델의 정보를 이용하여 가공한 데이터
        """

        if q is None:
            q = " "
        if size is None:
            size = 50

        self.headers["Accept"] = "application/json"
        self.headers["Content-Type"] = "application/json"
        self.headers["Authorization"] = "Angora %s" % self.token

        self.parameters['q'] = q
        self.parameters['size'] = size

        body = json.dumps(self.parameters)

        self.http_conn.request("POST", "/angora/query/jobs", body=body, headers=self.headers)

        try:
            r = json.load(self.http_conn.getresponse())
        except Exception as e:
            raise e

        self.sid = r["sid"]

    def response_data(self):

        self.http_conn.request(
            "GET",
            "/angora/query/jobs/%s" % self.sid,
            headers=self.headers)
        self.response = self.http_conn.getresponse()

        return self.response

    def fetchall(self):

        try:
            response = json.load(self.response_data())
        except Exception as e:
            raise e

        self.fetchall_data = response['results']

        return self.fetchall_data

    def description(self):
        """
        # description result column format
        [ name, type, display_size, internal_size, precision, scale, null_ok ]
        """

        try:
            response = self.response_data()
        except Exception as e:
            raise e

        for fields_data in response['fields']:
            self.description_data.append([fields_data['name'], fields_data['type'], None, None, None, None, None])
            self.description_data_name.append([fields_data['name'], None, None, None, None, None, None])
            self.description_data_type.append([None, fields_data['type'], None, None, None, None, None])

        return self.description_data_name

    def close(self):

        conn = self.http_conn
        if conn is None:
            pass
        else:
            self.http_conn = None
