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

        self.requests = requests
        self.eps = eps

        self.window.setupUi(self.main_window)
        self.config_tables = self.window.tableWidget_header_config, self.window.tableWidget_body_config
        self.configure_callbacks(self.window)
        self.start_app()

    @staticmethod
    def add_row( table, model):
        row_pos = table.rowCount()
        column_num = table.columnCount()

        #  Create blank data for Database
        blank_data = ('' for _ in range(column_num))

        # Add row and fill it
        table.insertRow(row_pos)
        model.add(model.item(*blank_data))

    @staticmethod
    def del_row(table, model):
        cur_row = table.currentRow()
        table.removeRow(cur_row)

        model.delete(cur_row)

    def button_edit_request_action(self,*x):
        # add filling of the config table
        # self.requests
        row = self.window.tableWidget_request.currentRow()
        column = self.window.tableWidget_request.currentColumn()

        name_item = self.window.tableWidget_request.item(row, 0)
        if hasattr(name_item, 'text'):
            # try to get information from dbs and fill all tables in config window
            self.window.lineEdit_request_name_config.setText(name_item.text())
        self.window.stackedWidget.setCurrentWidget(self.window.config)

    def button_add_request_action(self,*x):
        #self.requests
        self.window.stackedWidget.setCurrentWidget(self.window.config)

    def clear_config_tables_content(self, *tables):
        for table in tables:
            rows = table.rowCount()
            columns = table.columnCount()
            for column in range(columns):
                for row in range(rows):
                    item = table.item(row, column)
                    if item:
                        table.setItem(row, column, QtWidgets.QTableWidgetItem())
                        # table.item(row, column).setBackground(QtGui.QColor(*Colors.white))

        self.window.stackedWidget.setCurrentWidget(self.window.request)


    def test_filled_tables(self, *tables):
        for table in tables:
            rows = table.rowCount()
            columns = table.columnCount()
            failed_items = []
            for column in range(columns):
                for row in range(rows):
                    item = table.item(row, column)
                    if not (item and item.text()) or item.background().color().getRgb() == Colors.red:
                        table.setItem(row, column, QtWidgets.QTableWidgetItem())
                        table.item(row, column).setBackground(QtGui.QColor(*Colors.red))
                        failed_items += (row, column)

        return False if failed_items else True

    def button_apply_config_action(self, *x):
        result = self.test_filled_tables(*self.config_tables)

        # self.add_row(self.window.tableWidget_request, self.requests)
        #get info
        if result:
            self.clear_config_tables_content(*self.config_tables)
            self.window.stackedWidget.setCurrentWidget(self.window.request)

    def table_update(self, item, model):
        column = item.column()
        row = item.row()
        data = item.data(0)
        model.update(row, column, data)

        if hasattr(item, 'background'):
            item.setBackground(QtGui.QColor(*Colors.white))




    def configure_callbacks(self, window):
        # request window buttons
        window.button_edit_request.clicked.connect(self.button_edit_request_action)
        window.button_add_request.clicked.connect(self.button_add_request_action)
        window.button_delete_request.clicked.connect(lambda *x: self.del_row(window.tableWidget_request, self.requests))

        # main menu buttons
        window.actionEdit_URI.triggered.connect(lambda *x: window.stackedWidget.setCurrentWidget(window.uri))

        # config window buttons
        window.button_body_add_config.clicked.connect(lambda *x: self.add_row(window.tableWidget_body_config, 'requests'))
        window.button_body_delete_config.clicked.connect(lambda *x: self.del_row(window.tableWidget_body_config, 'requests'))

        window.button_header_add_config.clicked.connect(lambda *x: self.add_row(window.tableWidget_header_config, 'requests'))
        window.button_header_delete_config.clicked.connect(lambda *x: self.del_row(window.tableWidget_header_config, 'requests'))

        window.button_apply_config.clicked.connect(self.button_apply_config_action)
        window.button_cancel_config.clicked.connect(lambda *x: self.clear_config_tables_content(*self.config_tables))

        window.tableWidget_header_config.itemChanged.connect(lambda item: self.table_update(window.tableWidget_header_config, item))
        window.tableWidget_body_config.itemChanged.connect(lambda item: self.table_update(window.tableWidget_body_config,item))

        # uri window
        window.button_add_uri.clicked.connect(lambda *x: self.add_row(window.tableWidget_uri, eps))
        window.button_delete_uri.clicked.connect(lambda *x: self.del_row(window.tableWidget_uri, 'ep'))
        window.button_apply_uri.clicked.connect(lambda *x: window.stackedWidget.setCurrentWidget(window.request))

        window.tableWidget_uri.itemChanged.connect(lambda item: self.table_update(item, self.eps))

    def start_app(self):
        self.main_window.show()
        self.app.exec()

if __name__ == "__main__":
    requests = Requests(FileInt('URI_DBS', str(Requests.name)))
    eps = Endpoints(FileInt('URI_DBS', str(Endpoints.name)))
    Controller(requests, eps)
