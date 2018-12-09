from view_base import ViewBase
from PyQt5 import QtWidgets, QtCore
from model import Endpoint


class ViewEndpoints(ViewBase):
    def __init__(self, ep_window, eps):
        super().__init__(self)

        self.window = ep_window
        self.window_size = 1000, 258
        self.window_name = 'Endpoints'

        self.model = eps

        self.tables = None

        self.table_names = {'table_name': 'Requests',
                            'rows': ['URI {}'.format(num) for num in range(10)],
                            'columns': ['URI','Headers', 'Body']}

        self.widget_config_1 = {'tables':  {'Requests':      (0, 0, 1, 3)},
                                'buttons': {'button_add':    (1, 0, 1, 1),
                                            'button_delete': (1, 1, 1, 1),
                                            'button_apply':  (1, 2, 1, 1),
                                            },
                                }
        self.button_names = {'apply': self.window.close,
                             'add': self.add_row,
                             'delete': self.delete_selected_row,
                             }

        self.grid_names = ['Layout_1']

        self.configure()

    def __str__(self):
        return  self.__class__.__name__

    def configure(self):
        window = self.window_configuration(self.window, self.window_size, self.window_name)
        self.table = self.create_table(names=self.table_names, parent=window)
        buttons = self.buttons_create(self.button_names, parent=window)
        grid_1 = self.grids_create([self.grid_names[0]], parent=window)
        self.grids_configure(grid=grid_1, widget_config=self.widget_config_1,
                             tables=[self.table], buttons=buttons)
        QtCore.QMetaObject.connectSlotsByName(window)

if __name__ == "__main__":
    from model import Endpoints
    class TestDtb:
        def __init__(self,*data):
            ...
        def read(self, *data):
            return ''

        def write(self, *data):
            ...
    app = QtWidgets.QApplication([])
    dialog = QtWidgets.QDialog()
    endpoint_view = ViewEndpoints(dialog, Endpoints(TestDtb('ololo', 'trololo')))
    dialog.show()
    app.exec_()

