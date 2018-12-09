from PyQt5 import QtCore, QtWidgets, Qt
from view_base import ViewBase
from model import Request


class ViewRequests(ViewBase):
    def __init__(self, main_window,  show_window, requests, ep_model):
        super().__init__(self)
        self.model = requests
        self.ep_model = ep_model
        self.model_element = Request
        self.main_window = main_window
        self.show_window = show_window
        self.main_window_size = 1000, 258
        self.tables = None
        self.ep_model.added.connect(self.on_endpoint_added)
        self.ep_model.updated.connect(self.on_endpoint_updated)
        self.ep_model.deleted.connect(self.on_endpoint_deleted)

        self.main_window_name = 'Requests'

        # self.menu_structure = {'Options':
        #                            {'Edit URI': self.show_window.show,
        #                             'Exit': lambda: QtWidgets.qApp.exit(0)
        #                             },
        #                        }

        self.button_names = {'add': self.add_row,
                             'edit uri': self.show_window.show,
                             'delete': self.delete_selected_row,
                             'send': lambda: print('send_fuc'),
                             }

        self.checkboxes_names = ["show Log",
                                 "show JWT/UUIDs"]

        self.grid_names = ['Layout_1',
                           'Layout_2']

        self.table_names = {'table_name': 'Requests',
                            'columns': ['URI', 'Headers', 'Request Body']}

        self.widget_config_1 = {'tables':  {'Requests':        (0, 0, 1, 3)},
                                'buttons': {'button_send':     (1, 0, 1, 3),
                                            'button_add':      (2, 0, 1, 1),
                                            'button_edit uri': (2, 1, 1, 1),
                                            'button_delete':   (2, 2, 1, 1),
                                            },
                                'grids':   {'grid_Layout_2':   (4, 0, 1, 1, {'alignment': Qt.Qt.AlignLeft})}
                                }

        self.widget_config_2 = {'checkboxes': {'checkBox_showLog':       (4, 0, 1, 1),
                                               'checkBox_showJWT/UUIDs': (4, 1, 1, 1)}
                                }
        self.configure()

    def __str__(self):
        return  self.__class__.__name__

    @QtCore.pyqtSlot(object)
    def on_endpoint_added(self, endpoint):

        for row in range(self.table.rowCount()):
            combo_box = self.table.cellWidget(row, 0)
            combo_box.addItem(endpoint.uri)

    @QtCore.pyqtSlot(object)
    def on_endpoint_updated(self, data):

        for row in range(self.table.rowCount()):
            combo_box = self.table.cellWidget(row, 0)
            combo_box.setItemText(data['row'], data['value'])

    @QtCore.pyqtSlot(object)
    def on_endpoint_deleted(self, number):

        for row in range(self.table.rowCount()):
            combo_box = self.table.cellWidget(row, 0)
            index = combo_box.currentIndex()
            if index == number:
                combo_box.setCurrentIndex(-1)
            combo_box.removeItem(number)

    def add_row(self):
        row_pos = self.table.rowCount()
        column_num = self.table.columnCount()

        #  Create blank data for Database
        blank_data = ['' for _ in range(column_num - 1)]
        combo_box = self.create_combobox(row_pos)


        # Add row and fill it
        self.table.insertRow(row_pos)
        self.table.setCellWidget(row_pos, 0, combo_box)

        self.model.add(self.model_element(* [combo_box.currentIndex()] + blank_data))

    def table_field_configure(self, table_widget, names):
        for column in range(0, len(self.model.item.index_to_key_map.keys())):
            table_widget.setHorizontalHeaderItem(column, QtWidgets.QTableWidgetItem(names['columns'][column]))

            for row in range(0, len(self.model)):

                if column == 0:
                    dropdown_index = self.model[row][column]
                    combobox_index = int(dropdown_index) if str(dropdown_index) else -1
                    combo_box = self.create_combobox(row, combobox_index)
                    table_widget.setCellWidget(row, column, combo_box)

                else:
                    cell_data = self.model[row][column]
                    table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(cell_data))

        self.set_header_size(table_widget)
        table_widget.verticalHeader().hide()
        # table_widget.setSortingEnabled(False)
        return table_widget

    def create_combobox(self, row, index=-1):
        combo_box = QtWidgets.QComboBox()

        for endpoint in self.ep_model:
            combo_box.addItem(endpoint.uri)
        combo_box.setCurrentIndex(index)
        combo_box.currentIndexChanged.connect(lambda data, row_=row: self.model.update(row_, 0, data))


        return combo_box

    def combobox_saver(self, index):
        row = self.table.currentRow()
        self.model.update(row, 0, index)

    def configure(self):
        central_widget = self.main_window_configuration(self.main_window_size, self.main_window_name)
        # menu, submenus = self.create_main_window_menu(self.menu_structure, parent=self.main_window)
        # self.main_window.setMenuBar(menu)
        self.table = self.create_table(names=self.table_names, parent=central_widget)
        buttons = self.buttons_create(self.button_names, parent=central_widget)
        checkboxes = self.checkboxes_create(self.checkboxes_names, parent=central_widget)
        grid_1 = self.grids_create([self.grid_names[0]], parent=central_widget)
        grid_2 = self.grids_create([self.grid_names[-1]], parent=None)
        self.grids_configure(checkboxes=checkboxes,
                             grid=grid_2, widget_config=self.widget_config_2)
        self.grids_configure(tables=[self.table], buttons=buttons, grids=[grid_2],
                             grid=grid_1, widget_config=self.widget_config_1)
        QtCore.QMetaObject.connectSlotsByName(self.main_window)




