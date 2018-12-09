# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './URI configuration menu .ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets




class Ui_Form(object):
    def __init__(self, form):

        form.setObjectName("Form")
        form.resize(303, 146)

        self.gridLayout = QtWidgets.QGridLayout(form)
        self.gridLayout.setObjectName("gridLayout")

        self.label_uri1 = QtWidgets.QLabel(form)
        self.label_uri1.setObjectName("label_uri1")

        self.comboBox = QtWidgets.QComboBox(form)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")

        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.pushButton = QtWidgets.QPushButton(form)
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(form)
        self.pushButton_2.setObjectName("pushButton_2")

        self.lineEdit_2 = QtWidgets.QLineEdit(form)
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.label = QtWidgets.QLabel(form)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(form)
        self.label_2.setObjectName("label_2")

        self.lineEdit = QtWidgets.QLineEdit(form)
        self.lineEdit.setObjectName("lineEdit")

        self.gridLayout.addWidget(self.label_uri1,   0, 0, 1, 1)
        self.gridLayout.addWidget(self.comboBox,     0, 1, 1, 1)
        self.gridLayout.addWidget(self.label,        1, 0, 1, 1)
        self.gridLayout.addWidget(self.lineEdit,     1, 1, 1, 1)
        self.gridLayout.addWidget(self.label_2,      2, 0, 1, 1)
        self.gridLayout.addWidget(self.lineEdit_2,   2, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 3, 0, 1, 2)

        self.gridLayout_2.addWidget(self.pushButton,   0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.pushButton_2, 0, 1, 1, 1)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, Form):
        Form.setWindowTitle("URI configuration menu")
        self.label_uri1.setText("URI name")
        self.comboBox.setItemText(0, "/auth")
        self.pushButton.setText("Submit")
        self.pushButton_2.setText("Delete")
        self.lineEdit_2.setText("username;password")
        self.label.setText("Headers")
        self.label_2.setText("Body")
        self.lineEdit.setText("Authentication;Content-Type")

