from view import Ui_MainWindow
from model import Requests, Endpoints
from persistent_model import FileInt

from PyQt5 import QtCore, QtWidgets, QtGui


class Colors:
    red = (255, 0, 0)
    white = (255, 255, 255)


class Controller:
    def __init__(self, requests, eps):
        self.app = QtWidgets.QApplication([])
        self.main_window = QtWidgets.QMainWindow()
        self.window = Ui_MainWindow()

        self.models = {}
        self.models['requests'] = requests
        self.models['eps'] = eps
        self.table_names_to_model_mapping = {"header_config": '',
                                             "body_config": '',
                                             "uri": self.models['eps'],
                                             "request": self.models['requests']}

        self.window.setupUi(self.main_window)
        self.fill_tables_from_model()
        self.config_tables = self.window.tableWidget_header_config, self.window.tableWidget_body_config
        self.configure_callbacks(self.window)
        self.start_app()

    @staticmethod
    def add_row(table, row_pos=None):
        if not row_pos:
            row_pos = table.rowCount()
        # Add row
        table.insertRow(row_pos)

    @staticmethod
    def del_row(table):
        cur_row = table.currentRow()
        table.removeRow(cur_row)

        # model.delete(cur_row)

    def fill_tables_from_model(self):
        print(Requests)
        model_data = self.models['eps']
        for row, ep in enumerate(model_data):
            self.add_row(table=self.window.tableWidget_uri, row_pos=row)
            self.fill_table_rows(self.window.tableWidget_uri, row, ep)
            # self.window.tableWidget_uri.

    def fill_table_rows(self, table, row, data):
        for column, element in enumerate(data):
            # cell_data = getattr(data, element)
            table.setItem(row, column, QtWidgets.QTableWidgetItem(element))

            # print(element)
            # table.

    def button_edit_request_action(self, *x):
        # add filling of the config table
        # self.requests
        row = self.window.tableWidget_request.currentRow()
        column = self.window.tableWidget_request.currentColumn()

        name_item = self.window.tableWidget_request.item(row, 0)
        if hasattr(name_item, 'text'):
            # try to get information from dbs and fill all tables in config window
            self.window.lineEdit_request_name_config.setText(name_item.text())
        self.window.stackedWidget.setCurrentWidget(self.window.config)

    def button_add_request_action(self, *x):
        # self.requests
        self.window.stackedWidget.setCurrentWidget(self.window.config)

    def clear_tables_content(self, *tables):
        for table in tables:
            # table.clearContents()
            rows = table.rowCount()
            columns = table.columnCount()
            for row in range(rows):
                table.removeRow(row)

                # for column in range(columns):
                #     item = table.item(row, column)
                #     if item:
                #         table.setItem(row, column, QtWidgets.QTableWidgetItem())
                #         table.item(row, column).setBackground(QtGui.QColor(*Colors.white))

        self.window.stackedWidget.setCurrentWidget(self.window.request)

    def blank_cells_to_red_cells(self, row, column, item, table):
        # if no item, create an item
        if not item:
            item = QtWidgets.QTableWidgetItem()
            table.setItem(row, column, item)

        # if the cell is blank or is not read, fill with red
        if not item.text():
            table.item(row, column).setBackground(QtGui.QColor(*Colors.red))
            return row, column, item.text()

    def make_model_data(self, data, result_items):
        if isinstance(result_items, list):
            result_items = {}
        if data[0] in result_items.keys():
            result_items[data[0]].update(data[1])
        else:
            result_items[data[0]] = data[1]
        return result_items

    def check_cells(self, table, columns, rows, handler):
        result_items = []
        for column in range(columns):
            for row in range(rows):
                item = table.item(row, column)
                res = handler(row, column, item, table)
                if res:
                    if len(res) == 2:
                        result_items = self.make_model_data(res, result_items)
                    elif res:
                        result_items.append(res)
        return result_items

    def handle_tables(self, *tables, handler):
        table_result = {}
        for table in tables:
            rows = table.rowCount()
            columns = table.columnCount()
            action_result = self.check_cells(table, columns, rows, handler)
            if action_result:
                table_result[table] = action_result
        return table_result

    def button_apply_config_action(self, *x):
        result = self.handle_tables(*self.config_tables, handler=self.blank_cells_to_red_cells)

        if self.config_tables in result:
            final_result = []
            for table in self.config_tables:
                final_result += result[table]
            result = final_result

        # self.add_row(self.window.tableWidget_request, self.requests)
        if not result:
            self.clear_tables_content(*self.config_tables)
            self.window.stackedWidget.setCurrentWidget(self.window.request)

    def table_update(self, item):
        # column = item.column()
        # row = item.row()
        # data = item.data(0)
        # model.update(row, column, data)

        if hasattr(item, 'text') and item.text() and item.background().color().red():
            item.setBackground(QtGui.QColor(*Colors.white))

    def read_cell(self, row, column, item, table):
        item_type = table.objectName()[len('tableWidget_'):]
        item_model = self.table_names_to_model_mapping[item_type]
        column_names = [column_name for num, column_name in sorted(item_model.item.index_to_key_map.items())]

        if not item:
            item = QtWidgets.QTableWidgetItem()
            table.setItem(row, column, item)
        name_value = {column_names[column]: item.text()}
        return row, name_value

    # @staticmethod
    # def convert_cell2model_data(cell_data):
    #     model_data = {key: dict() for key in set(cell[0] for cell in cell_data)}
    #     for cell in cell_data:
    #         ep_index = cell[0]
    #         ep_properties = cell[1]
    #         ep_data = cell[2]
    #         column_names = ['uri', 'header_names', 'body_names']
    #
    #         ep_named_properties = column_names[ep_properties]
    #
    #         model_data[ep_index][ep_named_properties] = ep_data
    #     return model_data

    def button_apply_uri_action(self):
        view_table_data = self.handle_tables(self.window.tableWidget_uri, handler=self.read_cell)


        for table, elements in view_table_data.items():
            table_row_number = range(table.columnCount())
            self.clear_tables_content(table)

            for row in table_row_number:

                if row in elements.keys():
                    for id_, element in sorted(elements.items()):

                        if id_ in range(len(self.models['eps'])):
                            self.models['eps'].update(id_, element)
                        else:
                            self.models['eps'].add(Endpoints.item(**element))
                else:
                    self.models['eps'].delete(id_)

        # self.window.stackedWidget.setCurrentWidget(self.window.request)

    def edit_uri_action(self, window):
        self.fill_tables_from_model()
        window.stackedWidget.setCurrentWidget(window.uri)

    def configure_callbacks(self, window):
        # request window buttons
        window.button_edit_request.clicked.connect(self.button_edit_request_action)
        window.button_add_request.clicked.connect(self.button_add_request_action)
        window.button_delete_request.clicked.connect(lambda *x: self.del_row(window.tableWidget_request, self.requests))

        # main menu buttons
        window.actionEdit_URI.triggered.connect(lambda *x: self.edit_uri_action(self.window))

        # config window buttons
        window.button_body_add_config.clicked.connect(
            lambda *x: self.add_row(window.tableWidget_body_config, 'requests'))
        window.button_body_delete_config.clicked.connect(
            lambda *x: self.del_row(window.tableWidget_body_config, 'requests'))

        window.button_header_add_config.clicked.connect(
            lambda *x: self.add_row(window.tableWidget_header_config, 'requests'))
        window.button_header_delete_config.clicked.connect(
            lambda *x: self.del_row(window.tableWidget_header_config, 'requests'))

        window.button_apply_config.clicked.connect(self.button_apply_config_action)
        window.button_cancel_config.clicked.connect(lambda *x: self.clear_tables_content(*self.config_tables))

        window.tableWidget_header_config.itemChanged.connect(
            lambda item: self.table_update(item))  # window.tableWidget_header_config
        window.tableWidget_body_config.itemChanged.connect(
            lambda item: self.table_update(item))  # window.tableWidget_body_config

        # uri window
        window.button_add_uri.clicked.connect(lambda *x: self.add_row(window.tableWidget_uri))
        window.button_delete_uri.clicked.connect(lambda *x: self.del_row(window.tableWidget_uri))
        window.button_apply_uri.clicked.connect(self.button_apply_uri_action)

        # window.tableWidget_uri.clearContents()
        # window.tableWidget_uri.itemChanged.connect(lambda item: self.table_update(item, self.eps))

    def start_app(self):
        self.main_window.show()
        self.app.exec()


if __name__ == "__main__":
    requests = Requests(FileInt('URI_DBS', str(Requests.name)))
    eps = Endpoints(FileInt('URI_DBS', str(Endpoints.name)))
    Controller(requests, eps)
