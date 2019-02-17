from distutils.command.config import config

from PyQt5 import QtCore

class CollectionModel(QtCore.QObject):
    def __init__(self, dtb):
        super().__init__()
        self.name = self.__class__.__name__
        self.dtb = dtb
        self.collection = []
        self.get_data()
        print(ItemModel)

    def __len__(self):
        return len(self.collection)

    def __getitem__(self, item):
            return self.collection[item]


    def __str__(self):
        return self.__class__.__name__

    def add(self, request):
        self.collection += [request]
        self.dtb.write(self.collection, self.name)
        print(self.collection)

    def get_data(self):
        for request in self.dtb.read(self.name):
            self.add(request)

    def delete(self, num):
        if num == -1:
            print('doing nothing')
            return
        self.collection.pop(num)
        self.dtb.write(self.collection, self.name)

    def update(self, row, element):
        self.collection[row].update(**element)
        self.dtb.update(self.name, row, self.collection[row])


class ItemModel:
    def __repr__(self):
        return '{} {}'.format(self.__class__.__name__, self.__dict__)

    def __str__(self):
        return self.__class__.__name__

    def update(self, **element):
        # key = self.index_to_key_map[column]
        for key, value in element.items():
            self.__setattr__(key, value)
            print('Updated key {} -> {}'.format(key, repr(self)))

        # for key, value in values.items():
        #     if self.__dict__.get(key):
        #         self.__setattr__(key, value)
        #         continue
        #     raise AttributeError('"{}" class has no attribute "{}"'.format(self.__class__.__name__, key))

    def __iter__(self):
        for key, element in self.get_attributes().items():
            yield element

    # def __next__(self, item):
    #     key = self.index_to_key_map[item]
    #
    #     """Returns value from key/values of instance attributes"""
    #     return self.get_attributes()[key]

    def get_attributes(self):
        """Gets attributes, assuming that attributes are strings"""
        return {attr_name: attr_value for attr_name, attr_value in self.__dict__.items() if type(attr_value) in (str, int)}


class Endpoint(ItemModel):
    index_to_key_map = {0: 'endpoint', 1: 'header_names', 2: 'body_names'}

    def __init__(self, endpoint, header_names, body_names):
        self.endpoint = endpoint
        self.header_names = header_names
        self.body_names = body_names

class Request(ItemModel):
    index_to_key_map = {0: 'uri', 1: 'header_names', 2: 'body_names'}

    def __init__(self, name, headers, bodies):
        self.name = name
        self.headers = headers[self.name]
        self.bodies = bodies[self.name]



class Endpoints(CollectionModel):
    item = Endpoint
    name = 'Endpoints'

    def __init__(self, dtb):
        CollectionModel.__init__(self, dtb)


class Requests(CollectionModel):
    name = 'Requests'
    def __init__(self, dtb):
        CollectionModel.__init__(self, dtb)


