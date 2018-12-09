# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './uri_addition.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets, QtWidgets


class Ui_Form(object):
    def __init__(self, form):
        form.setObjectName("Form")
        form.resize(310, 146)
        self.gridLayout = QtWidgets.QGridLayout(form)
        self.gridLayout.setObjectName("gridLayout")
        self.label_uri1 = QtWidgets.QLabel(form)
        self.label_uri1.setObjectName("label_uri1")
        self.gridLayout.addWidget(self.label_uri1, 0, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(form)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(form)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(form)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 2, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(form)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 0, 1, 2)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, Form):
        Form.setWindowTitle("URI Addition menu")
        self.label_uri1.setText("URI name")
        self.lineEdit_3.setText("Name")
        self.label.setText("Headers")
        self.lineEdit.setText("Authentication;Content-Type")
        self.label_2.setText("Body")
        self.lineEdit_2.setText("username;password")
        self.pushButton.setText("Add")

