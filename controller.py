from view import Ui_MainWindow
from model import Requests
from persistent_model import FileInt

from PyQt5 import QtCore, QtWidgets, QtGui


class Controller:
    def __init__(self, requests ):
        self.app = QtWidgets.QApplication([])
        self.main_window = QtWidgets.QMainWindow()
        self.window = Ui_MainWindow()

        self.requests = requests

        self.window.setupUi(self.main_window)
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
            self.window.lineEdit_request_name.setText(name_item.text())
        self.window.stackedWidget.setCurrentWidget(self.window.config)

    def button_add_request_action(self,*x):
        #self.requests
        self.window.stackedWidget.setCurrentWidget(self.window.config)

    def test_filled_tables(self, *tables):
        for table in tables:
            rows = table.rowCount()
            columns = table.columnCount()
            failed_items = []
            for column in range(columns):
                for row in range(rows):
                    item = table.item(row, column)
                    if not hasattr(item,'text') or item.background().color().getRgb() == (100,100,150,255) or not item.text():
                        table.setItem(row, column, QtWidgets.QTableWidgetItem())
                        table.item(row, column).setBackground(QtGui.QColor(100, 100, 150))
                        failed_items += (row, column)

        return False if failed_items else True

    def button_apply_config_action(self, *x):
        result = self.test_filled_tables(self.window.tableWidget_header_config, self.window.tableWidget_body_config)

        # self.add_row(self.window.tableWidget_request, self.requests)
        #get info
        if result:
            self.window.stackedWidget.setCurrentWidget(self.window.request)

    def table_update(self, table, item, update=True):
        if item.text():
            item.setBackground(QtGui.QColor(255, 255, 255))


    def configure_callbacks(self, window):
        # request window buttons
        window.button_edit_request.clicked.connect(self.button_edit_request_action)
        window.button_add_request.clicked.connect(self.button_add_request_action)
        window.button_delete_request.clicked.connect(lambda *x: self.del_row(window.tableWidget_request, self.requests))

        # main menu buttons
        window.actionEdit_URI.triggered.connect(lambda *x: window.stackedWidget.setCurrentWidget(window.uri))

        # config window buttons
        window.button_body_add.clicked.connect(lambda *x: self.add_row(window.tableWidget_body_config))
        window.button_body_delete.clicked.connect(lambda *x: self.del_row(window.tableWidget_body_config))

        window.button_header_add.clicked.connect(lambda *x: self.add_row(window.tableWidget_header_config))
        window.button_header_delete.clicked.connect(lambda *x: self.del_row(window.tableWidget_header_config))

        window.button_apply_config.clicked.connect(self.button_apply_config_action)

        window.tableWidget_header_config.itemChanged.connect(lambda item: self.table_update(window.tableWidget_header_config, item))
        window.tableWidget_body_config.itemChanged.connect(lambda item: self.table_update(window.tableWidget_body_config,item))

    def start_app(self):
        self.main_window.show()
        self.app.exec()

if __name__ == "__main__":
    requests = Requests(FileInt('URI_DBS', str(Requests.name)))
    Controller(requests)
