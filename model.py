

class Request:
    def __init__(self, name, headers, bodies):
        self.name = name
        self.headers = headers[self.name]
        self.bodies = bodies[self.name]


class Requests:
    name = 'Requests'
    def __init__(self, dtb):
        self.dtb = dtb
        self.collection = {}
        self.get_data()

    def __len__(self):
        return len(self.collection)

    def __getitem__(self, item):
        return self.collection[item]

    def __str__(self):
        return self.__class__.__name__

    def get_data(self):
        for request in self.dtb.read(self.name):
            self.add(request)

    def add(self, request):
        self.collection[request.name] = request
        self.dtb.write(self.collection, self.name)
        print(self.collection)

    def delete(self, name):
        if not name:
            print('doing nothing')
            return
        self.collection.pop(name)
        self.dtb.write(self.collection, self.name)

    def update(self, row, column, value):

        #self.collection[row].update(column, value)
        #self.dtb.update(self.name, row, self.collection[row])
        pass

