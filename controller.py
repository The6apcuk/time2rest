from view import Ui_MainWindow
from model import Requests, Endpoints
from persistent_model import FileInt

from PyQt5 import QtCore, QtWidgets, QtGui


class Colors:
    red = (255, 0, 0)
    white = (255, 255, 255)

class DictWithAttr(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.result = True


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

    @staticmethod
    def fill_table_rows(table, row, data):
        for column, element in enumerate(data):
            table.setItem(row, column, QtWidgets.QTableWidgetItem(element))

    def button_edit_request_action(self, *x):
        # add filling of the config table
        row = self.window.tableWidget_request.currentRow()
        column = self.window.tableWidget_request.currentColumn()

        name_item = self.window.tableWidget_request.item(row, 0)
        if hasattr(name_item, 'text'):
            # try to get information from dbs and fill all tables in config window
            self.window.lineEdit_request_name_config.setText(name_item.text())
        self.window.stackedWidget.setCurrentWidget(self.window.config)

    def button_add_request_action(self, *x):
        # self.requests
        self.window.comboBox_config.addItems(str(ep) for ep in self.models['eps'])
        self.window.comboBox_config.setCurrentIndex(0)
        # self.fill_config_tables()

    def fill_config_tables(self):
        header_val, body_val = self.models['eps'].default_eps(self.window.comboBox_config.currentText())
        self.fill_tables_from_model(self.window.tableWidget_header_config, model_data=header_val)
        self.fill_tables_from_model(self.window.tableWidget_body_config, model_data=body_val)
        self.window.stackedWidget.setCurrentWidget(self.window.config)

    @staticmethod
    def clear_tables_content(*tables):
        for table in tables:
            table.setRowCount(0)

    def blank_cells_to_red_cells(self, row, column, item, table):
        column_name = table.horizontalHeaderItem(column).text().lower().replace(' ','_')
        # if no item, create an item
        if not item:
            item = QtWidgets.QTableWidgetItem()
            table.setItem(row, column, item)

        name_value = DictWithAttr({column_name: item.text()})

        # if the cell is blank or is not read, fill with red
        if not item.text():
            table.item(row, column).setBackground(QtGui.QColor(*Colors.red))
            name_value.result = False
        return row, name_value

    @staticmethod
    def read_cells(row, column, item, table):
        column_name = table.horizontalHeaderItem(column).text().lower().replace(' ','_')
        # if no item, create an item
        if not item:
            item = QtWidgets.QTableWidgetItem()
            table.setItem(row, column, item)
        name_value = {column_name: item.text()}
        return row, name_value

    def make_model_data(self, data, result_items):
        # if isinstance(result_items, list):
        #     result_items = {}
        if data[0] in result_items.keys():
            result_items[data[0]].update(data[1])
        else:
            result_items[data[0]] = data[1]
        if hasattr(data[1], 'result') and not data[1].result:
            result_items.result = data[1].result
        return result_items

    def check_cells(self, table, columns, rows, handler):
        result_items = DictWithAttr()
        for column in range(columns):
            for row in range(rows):
                item = table.item(row, column)
                res = handler(row, column, item, table)
                if res:
                    result_items = self.make_model_data(res, result_items)
        return result_items

    def handle_tables(self, tables, handler):
        table_result = DictWithAttr({table: {} for table in tables})
        for table in tables:
            rows = table.rowCount()
            columns = table.columnCount()
            action_result = self.check_cells(table, columns, rows, handler)
            if action_result:
                table_result[table] = action_result
            if hasattr(action_result, 'result'):
                table_result.result = action_result.result
        return table_result

    def button_apply_config_action(self, *x):
        result = self.handle_tables(self.config_tables, handler=self.blank_cells_to_red_cells)

        if result.result:
            self.clear_tables_content(*self.config_tables)
            self.window.stackedWidget.setCurrentWidget(self.window.request)
            self.window.comboBox_config.clear()

    def table_update(self, item):
        # column = item.column()
        # row = item.row()
        # data = item.data(0)
        # model.update(row, column, data)

        if hasattr(item, 'text') and item.text() and item.background().color().red():
            item.setBackground(QtGui.QColor(*Colors.white))

    def button_apply_action(self, *tables, model):
        view_table_data = self.handle_tables(tables, handler=self.read_cells)

        for table, elements in view_table_data.items():
            self.clear_tables_content(table)
            if model:
                model.flush()

                # Iterate through data recieved from the table
                for id_, element in sorted(elements.items()):
                    model.add(Endpoints.item(**element))

        self.window.stackedWidget.setCurrentWidget(self.window.request)

    def edit_uri_action(self, window):
        if window.stackedWidget.currentWidget() != window.uri:
            self.fill_tables_from_model(self.window.tableWidget_uri, model_data=self.models['eps'])
            window.stackedWidget.setCurrentWidget(window.uri)

    def combobox_update(self, index_):
        self.clear_tables_content(*self.config_tables)
        if index_ != -1:
            self.fill_config_tables()

    def button_cancel_config_action(self, *x):
        self.button_apply_action(*self.config_tables, model=None)
        self.window.comboBox_config.clear()

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
        window.button_cancel_config.clicked.connect(lambda *x: self.button_cancel_config_action(*x))

        window.tableWidget_header_config.itemChanged.connect(lambda item: self.table_update(item))
        window.tableWidget_body_config.itemChanged.connect(lambda item: self.table_update(item))
        window.comboBox_config.currentIndexChanged.connect(lambda index_: self.combobox_update(index_))

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
