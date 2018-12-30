from view_base import ViewBase
from PyQt5 import QtWidgets, QtCore
from model import Endpoint


class ViewRequestConfig(ViewBase):
    def __init__(self, request_config_window, requests):
        super().__init__(self)

        self.window = request_config_window
        self.window_size = 1000, 258
        self.window_name = 'Request Config'

        self.model = requests

        self.headers_table = None
        self.bodies_table = None

        self.headers_table_name = {'table_name': 'Headers',
                                   'columns': ['Header name', 'Header value']}

        self.bodies_table_name = {'table_name': 'Bodies',
                                  'columns': ['Body name', 'Body value']}

        self.widget_config_1 = {'combobox': {'combobox_endpoints': (0, 0, 1, 3),},
                                'tables':  {'Headers':             (1, 0, 1, 3),
                                            'Bodies':              (2, 0, 1, 3)},
                                'buttons': {'button_add':          (3, 0, 1, 1),
                                            'button_delete':       (3, 1, 1, 1),
                                            'button_apply':        (3, 2, 1, 1),
                                            },

                                }

        self.button_names = {'apply': self.window.close,
                             'add': self.add_row,
                             'delete': self.delete_selected_row}


        self.combobox_names = {'endpoints': lambda: print('Endpoint selected')}

        self.grid_names = ['Layout_1']

        self.configure()

    def __str__(self):
        return  self.__class__.__name__

    def create_table(self, names, parent, columns = None, rows = None):
        # columns = len(self.model.item.index_to_key_map.keys())
        # rows = len(self.model)
        table_widget = QtWidgets.QTableWidget(rows, columns, parent)
        table_widget.setObjectName(names['table_name'])
        table = self.table_field_configure(table_widget, names, columns=columns, rows=rows)
        table_widget.itemChanged.connect(self.table_saver)
        return table

    def table_field_configure(self, table_widget, names, columns, rows):
        for column in range(0, columns):
            table_widget.setHorizontalHeaderItem(column, QtWidgets.QTableWidgetItem(names['columns'][column]))

            for row in range(0, rows):
                #cell_data = self.model[row][column] if self.model[row][column] else ''
                cell_data =  ''
                table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(cell_data))

        self.set_header_size(table_widget)
        table_widget.verticalHeader().hide()
        return table_widget

    def configure(self):
        window = self.window_configuration(self.window, self.window_size, self.window_name)
        self.headers_table = self.create_table(names=self.headers_table_name, parent=window, columns=2, rows=2)
        self.bodies_table = self.create_table(names=self.bodies_table_name, parent=window, columns=2, rows=2 )
        buttons = self.buttons_create(self.button_names, parent=window)
        combobox = self.create_combobox(self.combobox_names, parent=window)
        grid_1 = self.grids_create([self.grid_names[0]], parent=window)
        self.grids_configure(grid=grid_1, widget_config=self.widget_config_1,
                             tables=[self.headers_table, self.bodies_table], buttons=buttons, combobox=combobox)
        QtCore.QMetaObject.connectSlotsByName(window)

if __name__ == "__main__":
    from model import Requests
    class TestDtb:
        def __init__(self,*data):
            ...
        def read(self, *data):
            return ''

        def write(self, *data):
            ...
    app = QtWidgets.QApplication([])
    dialog = QtWidgets.QDialog()
    endpoint_view = ViewRequestConfig(dialog, Requests(TestDtb('ololo', 'trololo')))
    dialog.show()
    app.exec_()

