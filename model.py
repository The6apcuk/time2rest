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
        self.collection.pop(num)
        self.dtb.write(self.collection, self.name)
        print(self.collection)

    def update(self, row, column, value):
        self.collection[row].update(column, value)
        self.dtb.update(self.name, row, self.collection[row])


class ItemModel:

    def __repr__(self):
        return '{} {}'.format(self.__class__.__name__, self.__dict__)

    def __str__(self):
        return self.__class__.__name__

    def update(self, column, value):
        key = self.index_to_key_map[column]
        self.__setattr__(key, value)
        print('Updated key {} -> {}'.format(key, repr(self)))

        # for key, value in values.items():
        #     if self.__dict__.get(key):
        #         self.__setattr__(key, value)
        #         continue
        #     raise AttributeError('"{}" class has no attribute "{}"'.format(self.__class__.__name__, key))

    def dying(self):
        # emmit
        assert Exception, 'not implemented'

    def __getitem__(self, item):
        key = self.index_to_key_map[item]

        """Returns value from key/values of instance attributes"""
        return self.get_attributes()[key]

    def get_attributes(self):
        """Gets attributes, assuming that attributes are strings"""
        return {attr_name: attr_value for attr_name, attr_value in self.__dict__.items() if type(attr_value) in (str,int)}


class Endpoint(ItemModel):
    index_to_key_map = {0: 'uri', 1: 'header_names', 2: 'body_names'}

    def __init__(self, uri, header_names, body_names):
        self.uri = uri
        self.header_names = header_names
        self.body_names = body_names


class Request(ItemModel):
    index_to_key_map = {0: 'endpoint', 1: 'header_values', 2: 'body_values'}

    def __init__(self, endpoint, header_values, body_values):
        self.endpoint = endpoint
        self.header_values = header_values
        self.body_values = body_values


class Endpoints(CollectionModel):
    item = Endpoint
    name = 'Endpoints'

    added = QtCore.pyqtSignal(object)
    deleted = QtCore.pyqtSignal(object)
    updated = QtCore.pyqtSignal(object)

    def __init__(self, dtb):
        super().__init__(dtb)


    def add(self, request):
        super().add(request)
        self.added.emit(request)

    def delete(self, num):
        super().delete(num)
        self.deleted.emit(num)

    def update(self, row, column, value):
        super().update(row, column, value)
        if column == 0:
            self.updated.emit({'row': row, 'value': value})




class Requests(CollectionModel):
    item = Request
    name = 'Requests'

    def __init__(self, dtb):
        super().__init__(dtb)


if __name__ == '__main__':
    class TestDtb:
        def read(self, *data):
            return ''

        def write(self, *data):
            ...


    end_point = Endpoints(TestDtb())
    end_point.add(Endpoint('uri1', 'header1', 'body1'))
    end_point.add(Endpoint('uri2', 'header2', 'body2'))
    cur_value = ("[Endpoint {'uri': 'uri1', 'header': 'header1', 'body': 'body1'},"
                 " Endpoint {'uri': 'uri2', 'header': 'header2', 'body': 'body2'}]")

    assert str(end_point.collection) == cur_value, '\n{} != \n{}'.format(end_point.collection, cur_value)
    print(end_point.collection)

    end_point.delete(0)
    cur_value = "[Endpoint {'uri': 'uri2', 'header': 'header2', 'body': 'body2'}]"
    assert str(end_point.collection) == cur_value, '\n{} != \n{}'.format(end_point.collection, cur_value)
    print(end_point.collection)

    end_point[0].update(uri='uri3', header='header3', body='body3')
    cur_value = "[Endpoint {'uri': 'uri3', 'header': 'header3', 'body': 'body3'}]"
    assert str(end_point.collection) == cur_value, '\n{} != \n{}'.format(end_point.collection, cur_value)
    print(end_point.collection)

    # ______________________________________________________________________________________________________________________
    requests = Requests(TestDtb())
    requests.add(Request('uri1', 'body1'))
    requests.add(Request('uri2', 'body2'))
    cur_value = ("[Request {'uri': 'uri1', 'header': 'application/json, JWT ololo', 'body': 'body1'},"
                 " Request {'uri': 'uri2', 'header': 'application/json, JWT ololo', 'body': 'body2'}]")

    assert str(requests.collection) == cur_value, '\n{} != \n{}'.format(requests.collection, cur_value)
    print(requests.collection)

    requests.delete(0)
    cur_value = "[Request {'uri': 'uri2', 'header': 'application/json, JWT ololo', 'body': 'body2'}]"
    assert str(requests.collection) == cur_value, '\n{} != \n{}'.format(requests.collection, cur_value)
    print(requests.collection)

    requests[0].update(uri='uri3', body='body3')
    cur_value = "[Request {'uri': 'uri3', 'header': 'application/json, JWT ololo', 'body': 'body3'}]"
    assert str(requests.collection) == cur_value, '\n{} != \n{}'.format(requests.collection, cur_value)
    print(requests.collection)
