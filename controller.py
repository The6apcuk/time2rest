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
        self.models = {'requests': requests,
                       'eps': eps}
        self.table_names_to_model_mapping = {"header_config": '',
                                             "body_config": '',
                                             "uri": self.models['eps'],
                                             "request": self.models['requests']}

        self.window.setupUi(self.main_window)
        self.config_tables = self.window.tableWidget_header_config, self.window.tableWidget_body_config
        # self.fill_tables_from_model()
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

    def fill_tables_from_model(self, *tables, model_data):
        for table in tables:
            for row, ep in enumerate(model_data):
                self.add_row(table, row_pos=row)
                self.fill_table_rows(table, row, ep)

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
        self.window.comboBox_config.clear()# MOVE TO THE APPLY BUTTON
        self.window.comboBox_config.addItems(str(ep) for ep in self.models['eps'])
        self.window.comboBox_config.setCurrentIndex(0)
        header_val, body_val = self.models['eps'].default_eps(self.window.comboBox_config.currentText())
        self.fill_tables_from_model(self.window.tableWidget_header_config, model_data=header_val)
        self.fill_tables_from_model(self.window.tableWidget_body_config, model_data=body_val)

        self.window.stackedWidget.setCurrentWidget(self.window.config)

    def clear_tables_content(self, *tables):
        for table in tables:
            # table.clearContents()
            # rows = table.rowCount()
            # columns = table.columnCount()
            table.setRowCount(0)
            # for row in range(rows):
            #     table.removeRow(row)

                # for column in range(columns):
                #     item = table.item(row, column)
                #     if item:
                #         table.setItem(row, column, QtWidgets.QTableWidgetItem())
                #         table.item(row, column).setBackground(QtGui.QColor(*Colors.white))

        # self.window.stackedWidget.setCurrentWidget(self.window.request)

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

    def handle_tables(self, tables, handler):
        table_result = {table: {} for table in tables}
        for table in tables:
            rows = table.rowCount()
            columns = table.columnCount()
            action_result = self.check_cells(table, columns, rows, handler)
            if action_result:
                table_result[table] = action_result
        return table_result

    def button_apply_config_action(self, *x):
        result = self.handle_tables(self.config_tables, handler=self.blank_cells_to_red_cells)

        # if self.config_tables in result.keys():
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

    def button_apply_action(self, *tables, model, flush=True):
        view_table_data = self.handle_tables(tables, handler=self.read_cell)

        for table, elements in view_table_data.items():
            self.clear_tables_content(table)
            if flush:
                model.flush()

                # Iterate through data recieved from the table
                for id_, element in sorted(elements.items()):
                    model.add(Endpoints.item(**element))

        self.window.stackedWidget.setCurrentWidget(self.window.request)

    def edit_uri_action(self, window):
        if window.stackedWidget.currentWidget() != window.uri:
            self.fill_tables_from_model(self.window.tableWidget_uri, model_data=self.models['eps'])
            window.stackedWidget.setCurrentWidget(window.uri)

    def configure_callbacks(self, window):
        # request window buttons
        window.button_edit_request.clicked.connect(self.button_edit_request_action)
        window.button_add_request.clicked.connect(self.button_add_request_action)
        window.button_delete_request.clicked.connect(lambda *x: self.del_row(window.tableWidget_request))

        # main menu buttons
        window.actionEdit_URI.triggered.connect(lambda *x: self.edit_uri_action(self.window))

        # config window buttons
        window.button_body_add_config.clicked.connect(
            lambda *x: self.add_row(window.tableWidget_body_config))
        window.button_body_delete_config.clicked.connect(
            lambda *x: self.del_row(window.tableWidget_body_config))

        window.button_header_add_config.clicked.connect(
            lambda *x: self.add_row(window.tableWidget_header_config))
        window.button_header_delete_config.clicked.connect(
            lambda *x: self.del_row(window.tableWidget_header_config))

        window.button_apply_config.clicked.connect(lambda *x: self.button_apply_config_action(*x))
        window.button_cancel_config.clicked.connect(lambda *x: self.button_apply_action(*self.config_tables,
                                                                                        model=None,
                                                                                        flush=False))

        window.tableWidget_header_config.itemChanged.connect(
            lambda item: self.table_update(item))  # window.tableWidget_header_config
        window.tableWidget_body_config.itemChanged.connect(
            lambda item: self.table_update(item))  # window.tableWidget_body_config

        # uri window
        window.button_add_uri.clicked.connect(lambda *x: self.add_row(window.tableWidget_uri))
        window.button_delete_uri.clicked.connect(lambda *x: self.del_row(window.tableWidget_uri))
        window.button_apply_uri.clicked.connect(lambda *x: self.button_apply_action(self.window.tableWidget_uri,
                                                                                    model=self.models['eps']))

        # window.tableWidget_uri.clearContents()
        # window.tableWidget_uri.itemChanged.connect(lambda item: self.table_update(item, self.eps))

    def start_app(self):
        self.main_window.show()
        self.app.exec()


if __name__ == "__main__":
    requests = Requests(FileInt('URI_DBS', str(Requests.name)))
    eps = Endpoints(FileInt('URI_DBS', str(Endpoints.name)))
    Controller(requests, eps)
