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
                             QFormLayout, QTabWidget, QRadioButton)
from functools import partial
from PyQt5 import QtCore

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
        self.layout = QHBoxLayout()
        self.list_of_elements = QListWidget()
        self.layout.addWidget(self.list_of_elements)
        self.vertical_layout = QVBoxLayout()
        self.solver_tabs = QTabWidget()
        self.element_settings = QPushButton()
        self.horizontal_layout_name = QHBoxLayout()
        self.label_name_eq = QLabel('Name')
        self.lineedit_name_eq = QLineEdit()
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

    def on_delete(self, list_of_elements, data):
        list_items = list_of_elements.selectedItems()
        for item in list_items:
            for i in data:
                if data[i]['name'] == item.text().lower():
                    data.pop(i)
                    break
            break
        for item in list_items:
            list_of_elements.takeItem(list_of_elements.row(item))

    def on_ok(self, list_of_elements, data):
        pass

    def on_apply(self, list_of_elements, data):
        # update name in QListWidget
        new_name = self.lineedit_name_eq.text()
        sel_items = self.list_of_elements.currentItem()

        if not self.update_name(new_name):
            return None
        # Get selected block in dictionary based on selected item in QListWidget
        for i in data:
            if data[i]['name'] == list_of_elements.currentItem().text():
                data[i]['name'] = new_name # update new name in dictionary
                sel_items.setText(new_name) # update new name in QListWidget

                # Iterate over widgets, get their new info and update dictionary
                self.widgets_to_dict(self.dynamic_widgets, data, i)

                # set the new data and update tabs based on new data
                self.data = data
                self.update_tabs(list_of_elements.currentItem())
                break

    def update_tabs(self, item=None):
        """Virtual method of class BaseSIF. Only used in children of
        BaseSIF. It compares dictionaries self.data and self.dynamic_widgets
        and updates tabs according to parameters in self.data

            Input parameter: variable item of type QListWidget.item
        """

        for bcs in self.data:
            if item:
                if self.data[bcs]["Name".lower()] == item.text():
                    bc = self.data[bcs]
                    self.lineedit_name_eq.setText(bc["Name".lower()])
                else:
                    continue
            else:
                bc = self.data[bcs]
            for label in self.dynamic_widgets:
                setting = bc.get(label.text().lower())
                widget = self.dynamic_widgets[label]
                widget_type = widget.metaObject().className()
                if setting is None: # parameter not stored in bc block
                    if widget_type == "QLineEdit":
                        widget.setText("")
                    elif widget_type == "QCheckBox":
                        widget.setChecked(0)
                    elif widget_type == "QComboBox":
                        idx = widget.findText("None")
                        widget.setCurrentIndex(idx)
                    elif widget_type == "RadioComboGroup":
                        if widget.text().lower() == "Linear System Solver".lower():
                            combo_text = bc.get(str("Linear System "+str(setting)+" Method").lower())
                        elif widget.text().lower() == "Exec Solver".lower():
                            combo_text = None
                        widget.setSelected(setting, combo_text)
                else:
                    if widget_type == "QLineEdit":
                        widget.setText(bc[label.text().lower()])
                    elif widget_type == "QCheckBox":
                        true = ['Logical True'.lower(), 'True'.lower()]
                        if bc[label.text().lower()].lower() in true:
                            widget.setChecked(1)
                        else:
                            widget.setChecked(0)
                    elif widget_type == "QComboBox":
                        try:
                            idx = widget.findText(bc[label.text().lower()])
                            widget.setCurrentIndex(idx)
                        except:
                            print("QCombobox does not contain this parameter!")
                    elif widget_type == "RadioComboGroup":
                        if widget.text().lower() == "Linear System Solver".lower():
                            combo_text = bc.get(str("Linear System "+str(setting)+" Method").lower())
                        elif widget.text().lower() == "Exec Solver".lower():
                            combo_text = None
                        widget.setSelected(setting, combo_text)
            break

    def update_name(self, new_name=None):
        sel_item = self.list_of_elements.currentItem()
        items = []
        for i in range(self.list_of_elements.count()):
            if self.list_of_elements.item(i).text() == sel_item.text():
                pass
            else:
                items.append(self.list_of_elements.item(i))
        #exists = self.list_of_elements.findItems(update_name,
        #                                         QtCore.Qt.MatchRegExp)
        if self.list_of_elements.count() is 0:
            self.lineedit_name_eq.setText(new_name+"_1")

        if new_name:
            for i in items:
                if i.text() == new_name:
                    #print("Name already exists")
                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Information)
                    msgBox.setText("Element with this name already exists.")
                    msgBox.setWindowTitle("QMessageBox Example")
                    msgBox.setStandardButtons(QMessageBox.Ok)
                    msgBox.exec()
                    return False
        else:
            for i in range(self.list_of_elements.count()):
                update_name = new_name+"_"+str(i)
                print("update_name", update_name)
                exists = self.list_of_elements.findItems(new_name,
                                                    QtCore.Qt.MatchExactly)
                if len(exists) is 0:
                    self.lineedit_name_eq.setText(update_name)
                    return True

    def check_name(self, list_of_elements, new_name):
        element = list_of_elements.findItems(new_name,
                                             QtCore.Qt.MatchExactly)
        print("element", element)
        if len(element) is not 0:
            #print("Exists")
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Element with this name already exists.")
            msgBox.setWindowTitle("QMessageBox Example")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            #msgBox.buttonClicked.connect(msgButtonClick)
            return False
        return True

    def on_new(self, list_of_elements, data):
        # update name in QListWidget
        new_name = self.lineedit_name_eq.text()
        #sel_items = self.list_of_elements.currentItem()
        if not self.check_name(list_of_elements, new_name):
            return None
        # Get selected block in dictionary based on selected item in QListWidget
        len_data = len(data) # get current number of elements in data
        data[len_data+1] = {}
        data[len_data+1]['name'] = new_name
        self.list_of_elements.addItem(new_name)
        current_item = self.list_of_elements.findItems(new_name, QtCore.Qt.MatchExactly)[0]
        print("current_item", current_item)
        for i in data:
            if data[i]['name'] == current_item.text():
                data[i]['name'] = new_name # update new name in dictionary
                #sel_items.setText(new_name) # update new name in QListWidget
                self.widgets_to_dict(self.dynamic_widgets, data, i)
                self.data = data
                self.update_tabs(current_item)
                return None

    def widgets_to_dict(self, dynamic_widgets, data, i):
        self.dynamic_widgets = dynamic_widgets
        
        # Iterate over widgets, get their new info and update dictionary
        for widget in self.dynamic_widgets:
            parameter = widget
            setting = self.dynamic_widgets[widget]
            setting_type = setting.metaObject().className() 
            if setting_type == "QLineEdit":
                setting = setting.text().lower()
                parameter = parameter.text().lower()
                data[i][parameter] = setting
            elif setting_type == "QCheckBox":
                parameter = parameter.text().lower()
                if setting.isChecked():
                    data[i][parameter] = "Logical True"
                else:
                    data[i][parameter] = "Logical False"
            elif setting_type == "QComboBox":
                setting = setting.currentText()
                parameter = parameter.text()
                data[i][parameter] = setting
            elif setting_type == "RadioComboGroup":
                data_params = setting
                setting = setting.getSelected()
                print("setting", setting)
                if setting[1] != None:
                    parameter1 = "Linear System Solver"
                    setting1 = setting[0]
                    data[i][parameter1.lower()] = setting1
                    parameter2 = "Linear System "+setting[0]+" Method"
                    setting2 = setting[1]
                    data[i][parameter2.lower()] = setting2
                elif setting[1] == None:
                    parameter = data_params.text()
                    setting = setting[0]
                    data[i][parameter.lower()] = setting

                # set the new data and update tabs based on new data
                #self.data = data
                #self.update_tabs(list_of_elements.currentItem())
                #break
        pass

class RadioComboGroup(QWidget):
    """Documentation for RadioCombo

    """
    def __init__(self, title, radio_combo, parent=None):
        QWidget.__init__(self, parent=parent)
        self.parent = parent
        self.lbl_title = QLabel(title)
        self.radio_combo = radio_combo
        self.radio_combo_widgets = []
        layout = QVBoxLayout(self)
        layout.addWidget(self.lbl_title)
        grid_layout = QGridLayout(self)
        for item in enumerate(self.radio_combo):
            rd_button = QRadioButton(item[1][0])
            if item[1][1] != None:
                combobox = QComboBox()
                combobox.addItems(item[1][1])
                self.radio_combo_widgets.append([rd_button, combobox])
                grid_layout.addWidget(combobox, item[0], 1)
            else:
                self.radio_combo_widgets.append([rd_button, None])
            grid_layout.addWidget(rd_button, item[0], 0)
        layout.addLayout(grid_layout)

    def setText(self, text):
        self.lbl_title.setText(text)

    def getText(self):
        return self.lbl_title.text()

    def text(self):
        return self.lbl_title.text()

    def setSelected(self, radio, combo):
        for item in self.radio_combo_widgets:
            if item[0].text() == radio:
                item[0].setChecked(True)
                if item[1] != None:
                    idx = item[1].findText(combo)
                    item[1].setCurrentIndex(idx)
                return None
        print("Error setting radio and combo!!!")

    def getSelected(self):
        for item in self.radio_combo_widgets:
            if item[0].isChecked():
                if item[1] is not None:
                    setting = item[1].currentText()
                    return [item[0].text(), setting]
                return [item[0].text(), None]

