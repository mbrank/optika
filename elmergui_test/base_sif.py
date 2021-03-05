# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 20:26:27 2016

@author: Rainer Jacob

General setup class
"""
from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5.QtWidgets import (QInputDialog, QLineEdit, QDialog,
                             QApplication, QWidget, QLabel,
                             QHBoxLayout, QMainWindow, QCheckBox,
                             QPushButton, QVBoxLayout, QMessageBox,
                             QFileDialog, QStackedWidget, QGroupBox,
                             QGridLayout, QComboBox, QListWidget,
                             QFormLayout, QTabWidget)

class BaseSIF(QDialog):
    """Class that provides the General setup dialog and its functionality"""

    def __init__(self, data, parent=None):
        """Constructor.

        Args:
        -----
        path_forms: str
            String containing the path to the ui-files defining the look of the
            window.
        """
        super(BaseSIF, self).__init__(parent)
        #uic.loadUi(path_forms + "generalsetup.ui", self)
        #self.simulationFreeTextEdit.setText("Use Mesh Names = Logical True")
        #self.acceptButton.clicked.connect(self.applyChanges)

        self.data = data  # dictionary that contains set of blocks,
                          # i. e. set of equations, boundary conditions,
                          # initial_conditions

        self.dynamic_widgets = {} # dictionary that contains qwidgets
                                  # of different blocks,
                                  # i. e. equations, boundary
                                  # conditions, initial_conditions

        self.tab1 = QWidget()
        self.tabs = {'tab1': self.tab1}
        if not self.data:
            self.data = {}
            print('test')

        #self.initUI(self.data)

        #def initUI(self, data):
        self.layout = QHBoxLayout()
        self.list_of_elements = QListWidget()
        self.list_of_elements.insertItem(0, "Red")
        self.list_of_elements.insertItem(1, "Orange")
        self.list_of_elements.insertItem(2, "Blue")
        self.layout.addWidget(self.list_of_elements)

        self.vertical_layout = QVBoxLayout()
        self.solver_tabs = QTabWidget()

        #for tab in self.tabs:
        #    print('')
        #    print(type(self.tabs[tab]), tab)
        #    self.solver_tabs.addTab(self.tabs[tab], tab)

        self.element_settings = QPushButton()

        self.horizontal_layout_name = QHBoxLayout()
        self.label_name_eq = QLabel('Name')
        self.lineedit_name_eq = QLineEdit('Equation1')
        self.horizontal_layout_name.addWidget(self.label_name_eq)
        self.horizontal_layout_name.addWidget(self.lineedit_name_eq)
        self.horizontal_layout_buttons = QHBoxLayout()
        self.new_element = QPushButton('New')
        self.apply_element = QPushButton('Apply')
        self.ok_element = QPushButton('OK')
        self.delete_element = QPushButton('Delete')
        self.horizontal_layout_buttons.addWidget(self.new_element)
        self.horizontal_layout_buttons.addWidget(self.apply_element)
        self.horizontal_layout_buttons.addWidget(self.ok_element)
        self.horizontal_layout_buttons.addWidget(self.delete_element)

        self.vertical_layout.addWidget(self.solver_tabs)
        self.vertical_layout.addWidget(self.element_settings)
        self.vertical_layout.addLayout(self.horizontal_layout_name)
        self.vertical_layout.addLayout(self.horizontal_layout_buttons)
        self.layout.addLayout(self.vertical_layout)

        self.setLayout(self.layout)
        self.setGeometry(300, 300, 250, 150)
        #self.setWindowTitle('General settings')
        #self.exec()

    def update_tabs(self, item):
        """Virtual method of class BaseSIF. Only used in children of
        BaseSIF. It compares dictionaries self.data and self.dynamic_widgets
        and updates tabs according to parameters in self.data

            Input parameter: variable item of type QListWidget.item
        """

        print('---------------------------------------')
        print("clicked item in list", item.text())
        print("self.data", self.data)
        for bcs in self.data:
            print("Comparison", self.data[bcs]["Name"], item.text(), 'len self.data', self.data)
            if self.data[bcs]["Name"] == item.text():
                bc = self.data[bcs]
                print('test equation show')
                self.lineedit_name_eq.setText(bc["Name"])
                for label in self.dynamic_widgets:
                    setting = bc.get(label.text())
                    widget = self.dynamic_widgets[label]
                    widget_type = widget.metaObject().className()
                    if setting == None: # parameter not stored in bc block
                        if widget_type == "QLineEdit":
                            widget.setText("")
                        elif widget_type == "QCheckBox":
                            widget.setChecked(0)
                        elif widget_type == "QComboBox":
                            idx = widget.findText("None")
                            widget.setCurrentIndex(idx)

                    else:
                        if widget_type == "QLineEdit":
                            widget.setText(bc[label.text()])
                        elif widget_type == "QCheckBox":
                            if bc[label.text()] == 'Logical True'.lower():
                                widget.setChecked(1)
                            else:
                                widget.setChecked(0)
                        elif widget_type == "QComboBox":
                            try:
                                idx = widget.findText(bc[label.text()])
                                widget.setCurrentIndex(idx)
                            except:
                                print("QCombobox does not contain this parameter!")
                break
