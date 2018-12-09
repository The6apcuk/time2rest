from PyQt5 import QtCore, QtWidgets, Qt


class ViewBase(QtCore.QObject):
    def __init__(self, main_window):
        super().__init__()
        self.window = main_window
        self.saver_data = list()
        self.dbs_name = str(self)

    def window_configuration(self, window, size, name):
        window.setObjectName("MainWindow")
        window.resize(*size)
        window.setStyleSheet("")
        window.setWindowTitle(name)
        return window

    def initialize_central_widget(self, window):
        centralwidget = QtWidgets.QWidget(window)
        centralwidget.setObjectName("centralwidget")
        self.window.setCentralWidget(centralwidget)
        return centralwidget

    def create_window_menu(self, menu_structure, parent):
        menuBar = QtWidgets.QMenuBar(parent)
        menuBar.setGeometry(QtCore.QRect(0, 0, 411, 25))
        menuBar.setObjectName("menuBar")
        submenus = []
        for menu, action in self.add_menu_items(menu_structure, parent=menuBar):
            menuBar.addMenu(menu)
            submenus += [menu, action]
        return menuBar, submenus

    def add_menu_items(self, menu_items, parent):
        for menu_name, submenus_names in menu_items.items():
            menu = QtWidgets.QMenu(parent)
            menu.setObjectName("menu{}".format(menu_name))
            menu.setTitle(menu_name)
            menu_actions = []
            for submenu_name, func in submenus_names.items():
                action = self.add_submenu_items(submenu_name, func)
                menu.addAction(*action)
                menu_actions += action
            yield menu, menu_actions

    def add_submenu_items(self, submenu_name, func):
        action = QtWidgets.QAction(self.window)
        action.setText(submenu_name)
        action.setObjectName("action{}".format(submenu_name))
        # noinspection PyUnresolvedReferences
        action.triggered.connect(func)
        return [action]

    def create_table(self, names, parent):
        columns = len(self.model.item.index_to_key_map.keys())
        rows = len(self.model)
        table_widget = QtWidgets.QTableWidget(rows, columns, parent)
        table_widget.setObjectName(names['table_name'])
        table = self.table_field_configure(table_widget, names)
        table_widget.itemChanged.connect(self.table_saver)
        return table

    def table_saver(self, item):
        column = item.column()
        row = item.row()
        data = item.data(0)
        self.model.update(row, column, data)

    def add_row(self):
        row_pos = self.table.rowCount()
        column_num = self.table.columnCount()

        #  Create blank data for Database
        blank_data = ('' for _ in range(column_num))

        # Add row and fill it
        self.table.insertRow(row_pos)
        self.model.add(self.model.item(*blank_data))

    def delete_selected_row(self):
        cur_row = self.table.currentRow()
        self.table.removeRow(cur_row)

        self.model.delete(cur_row)

    def table_field_configure(self, table_widget, names):
        for column in range(0, len(self.model.item.index_to_key_map.keys())):
            table_widget.setHorizontalHeaderItem(column, QtWidgets.QTableWidgetItem(names['columns'][column]))

            for row in range(0, len(self.model)):
                cell_data = self.model[row][column] if self.model[row][column] else ''
                table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(cell_data))

        self.set_header_size(table_widget)
        table_widget.verticalHeader().hide()
        return table_widget

    def recreate_dbs(self, columns):
        self.dbs.write([[list() for _ in range(columns)]], type_ = self.dbs_name)

    @staticmethod
    def set_header_size(table_widget):
        table_widget.horizontalHeader().setStretchLastSection(True)

    @staticmethod
    def buttons_create(names, parent):
        for name, func in names.items():
            button = QtWidgets.QPushButton(parent)
            button.setObjectName("button_{}".format(name))
            button.setText(name.capitalize())
            # noinspection PyUnresolvedReferences
            button.clicked.connect(func)
            yield button

    # @staticmethod
    def create_combobox(self, names, parent, index=-1):
        for name, func in names.items():
            combo_box = QtWidgets.QComboBox(parent)
            combo_box.setObjectName("combobox_{}".format(name))
            combo_box.setCurrentIndex(index)
            combo_box.currentIndexChanged.connect(func)
            yield combo_box

    @staticmethod
    def modal_func(func):
        func.setWindowModality(Qt.Qt.ApplicationModal)
        return func.show

    @staticmethod
    def checkboxes_create(names, parent):
        for name in names:
            checkbox = QtWidgets.QCheckBox(parent)
            checkbox.setObjectName("checkBox_{}".format(name.replace(' ', '')))
            checkbox.setText(name.capitalize())
            yield checkbox

    @staticmethod
    def grids_create(names, parent):
        for name in names:
            grid = QtWidgets.QGridLayout(parent)
            grid.setObjectName("grid_{}".format(name.replace(' ', '')))
            return grid

    @staticmethod
    def grids_configure(widget_config, grid, **widget_types):
        for widget_name, widget_type in widget_types.items():
            for widget in widget_type:
                if widget_name in widget_config:
                    if widget_name == 'grids':
                        *num, alignment = widget_config[widget_name][widget.objectName()]
                        grid.addLayout(widget, *num, **alignment)
                    else:
                        grid.addWidget(widget, *widget_config[widget_name][widget.objectName()])