#!/usr/bin/env python
# coding=UTF-8

from cursors import *
from connections import *


class DiscoveryService(Cursor, Connection):

    def __init__(self):
        self.headers = {}
        self.parameters = {}
        self.description_data = []
        self.description_data_type = []
        self.description_data_name = []
        super(Connection, self).__init__()
        super(Cursor, self).__init__()


if __name__ == '__main__':

    sql_api = DiscoveryService()
    conn = sql_api.connect(host="", port=0, user_id=0, user_passwd="")

    cursor = conn.cursor()

    cursor.execute(
        q="",
        size=0, save=True)

    # print(cursor.fetchall())
    # cursor.close()
    # print(cursor.fetchall())
    print(cursor.description())
    print(cursor.description_data_name)
    # print(cursor.description_data_type)
    print(cursor.description())
    cursor.close()
