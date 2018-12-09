from view_base import ViewBase
from PyQt5 import QtWidgets, QtCore
from model import Endpoint


class ViewEndpoints(ViewBase):
    def __init__(self, main_window, eps):
        super().__init__(self)
        self.model = eps
        self.model_element = Endpoint
        self.main_window = main_window
        self.tables = None
        self.main_window_size = 1000, 258

        self.main_window_name = 'End points'

        self.table_names = {'table_name': 'Requests',
                            'rows': ['URI {}'.format(num) for num in range(10)],
                            'columns': ['URI','Headers', 'Body']}

        self.widget_config_1 = {'tables':  {'Requests':      (0, 0, 1, 3)},
                                'buttons': {'button_add':    (1, 0, 1, 1),
                                            'button_delete': (1, 1, 1, 1),
                                            'button_apply':  (1, 2, 1, 1),
                                            },
                                }
        self.button_names = {'apply': self.main_window.close,
                             'add': self.add_row,
                             'delete': self.delete_selected_row,
                             }

        self.grid_names = ['Layout_1']

        self.configure()

    def __str__(self):
        return  self.__class__.__name__

    def configure(self):
        central_widget = self.main_window_configuration(self.main_window_size, self.main_window_name)
        self.table = self.create_table(names=self.table_names, parent=central_widget)
        buttons = self.buttons_create(self.button_names, parent=central_widget)
        grid_1 = self.grids_create([self.grid_names[0]], parent=central_widget)
        self.grids_configure(grid=grid_1, widget_config=self.widget_config_1,
                             tables=[self.table], buttons=buttons)
        QtCore.QMetaObject.connectSlotsByName(self.main_window)

