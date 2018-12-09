#!/usr/bin/python2
import shelve
import requests as req
import json
from time import sleep


class FileInt:
    def __init__(self, name, *dbs):
        self.file_name = name
        self.data = list()
        self.dbs = dbs
        self.check_dbs()

    def check_dbs(self):
        for db in self.dbs:
            dbs = self.open()
            try:
                dbs[db]
            except (KeyError,AttributeError):
                dbs[db] = []

    def read(self, db):
        dbs = self.open()
        data = list(dbs.items()) if db == 'all' else dbs[db]
        self.close(dbs)
        return data

    def write(self, data, table):
        dbs = self.open()
        # if type_ == 'jwts':
        #     self.dbs['jwts'] = data
        #     self.close()
        # elif type_ == 'uuids':
        #     self.dbs['uuids'] = data
        #     self.close()
        # else:
        dbs[table] = data
        self.close(dbs)

    def open(self):
        return shelve.open(self.file_name)

    @staticmethod
    def close(dbs):
        dbs.close()

    def update(self, table, row, data):
        dbs_data = self.read(table)
        dbs_data[row] = data
        self.write(dbs_data, table=table)

    # def append(self, data):
    #     self.open()
    #     if data:
    #         for element in data if isinstance(data, list) else [data]:
    #             uuids = self.dbs['uuids']
    #             if element not in uuids:
    #                 uuids.append(element)
    #                 self.dbs['uuids'] = uuids
    #         else:
    #             self.close()
    #     else:
    #         self.dbs['uuids'] = list()

    # def pop(self, index=None):
    #     self.open()
    #     uuids = self.dbs['uuids']
    #     if isinstance(index, int) and uuids:
    #         uuid = uuids.pop(index)
    #         self.write(uuids, 'uuids')
    #         self.close()
    #         return (i for i in [uuid])
    #     self.write(list(), 'uuids')
    #     self.close()
    #     return (i for i in uuids[::-1])
