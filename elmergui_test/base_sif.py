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
import copy

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
        self.element_name = "BaseSIF" # overwritten by child class
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
        self.dict_to_widgets()
        self.setLayout(self.layout)
        self.setGeometry(300, 300, 250, 150)

    def on_delete(self, list_of_elements, data):
        list_items = list_of_elements.selectedItems()
        print('len(list_items)', len(list_items))
        for item in list_items:
            for i in data:
                print("item.text().lower() to delete", item.text().lower())
                if data[i]['name'].lower() == item.text().lower():
                    data.pop(i)
                    break
            break
        for item in list_items:
            list_of_elements.takeItem(list_of_elements.row(item))

    def on_ok(self, list_of_elements, data):
        #self.on_apply(list_of_elements, data)
        pass

    def on_new(self, list_of_elements, data):
        # update name in QListWidget
        new_name = self.lineedit_name_eq.text()
        #sel_items = self.list_of_elements.currentItem()

        items = [list_of_elements.item(i) for i in range(list_of_elements.count())]
        print("items len", len(items))
        new_name = self.update_element_name(items, new_name)
        if not new_name:
            return None
        # Get selected block in dictionary based on selected item in QListWidget
        len_data = len(data) # get current number of elements in data
        data[len_data+1] = {}
        data[len_data+1]['name'] = new_name
        self.list_of_elements.addItem(new_name)
        current_item = self.list_of_elements.findItems(new_name, QtCore.Qt.MatchExactly)[0]
        print("current_item", current_item)
        for i in data:
            print('data', data)
            print(i)
            if data[i]['name'] == current_item.text():
                data[i]['name'] = new_name # update new name in dictionary
                #sel_items.setText(new_name) # update new name in QListWidget
                self.widgets_to_dict(self.dynamic_widgets, data, i)
                self.data = data
                self.dict_to_widgets(current_item)
                current_item.setSelected(True)
                self.list_of_elements.setCurrentItem(current_item)
                print("current_item.setSelected(True)", current_item.text())
                print(self.list_of_elements.selectedItems())
                sel_items = self.list_of_elements.currentItem()
                print('sel_items.text()', sel_items.text())
                return None

    def on_apply(self, list_of_elements, data):
        # update name in QListWidget
        new_name = self.lineedit_name_eq.text()
        sel_items = self.list_of_elements.currentItem()

        # Create list of QListWidget elements (except the selected
        # one) to check if new name is allowed
        items = []
        for i in range(self.list_of_elements.count()):
            if not self.list_of_elements.item(i).text() == sel_items.text():
                items.append(self.list_of_elements.item(i))

        # Check if new name is possible
        if not self.update_element_name(items, new_name):
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
                self.dict_to_widgets(list_of_elements.currentItem())
                break

    def dict_to_widgets(self, item=None):
        """Virtual method of class BaseSIF. Only used in children of
        BaseSIF. It compares dictionaries self.data and self.dynamic_widgets
        and updates tabs according to parameters in self.data

            Input parameter: variable item of type QListWidget.item
        """

        for bcs in self.data:
            bc = self.data[bcs]
            bc =  {k.lower(): v for k, v in bc.items()}
            print("BCXCCCC", bc)
            if item:
                # set all keys to lower
                print("self.data[bcs]:", self.data[bcs])
                if bc["Name".lower()] == item.text():
                    #bc = self.data[bcs]
                    self.lineedit_name_eq.setText(bc["Name".lower()])
                else:
                    continue
            else:
                #bc = self.data[bcs]
                ## set all keys to lower
                #bc =  {k.lower(): v for k, v in bc.items()}
                pass
            for label in self.dynamic_widgets:
                if label.text() == "Create new solver":
                    print("CREATE NRE SOLCER")
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
                        #if label.text() == 'Active solvers':
                        #    _solvers = bc['active solvers'].split()
                        #    print('_SOLVERS', _solvers, bc["name"].replace(' ','_') + '_solver')
                        #    if bc["name"].replace(' ','_') + '_solver' in _solvers:
                        #        print("IS INSIDE")
                        #        self.check_new_solver.setChecked(1)
                        #        if self.check_new_solver.isChecked():
                        #            print("IS CHECKED CHECKED")
                        #            #     widget.setText(widget.text()+' '+bc['solvers of eq']['name'].replace(' ', '_'))
                    elif widget_type == "QCheckBox":
                        true = ['Logical True'.lower(), 'True'.lower()]
                        print("widget.TEXT()", label.text())
                        if bc[label.text().lower()].lower() in true:
                            widget.setChecked(1)
                            #if widget.text() == "Create new solver":
                            #    print("CREATE NEW SOLVER INSIDE")
                            #    if bc["solvers of eq"].get("name"):
                            #        #and widget.isChecked():
                            #        print("CREATE NEW SOLVER CHECKED")
                            #        # pass new solver to active solvers
                            #        for active_solvers_label in self.dynamic_widgets:
                            #            if active_solvers_label.text() == "Active solvers":
                            #                active_solvers = self.dynamic_widgets[active_solvers_label]
                            #                current_solvers = active_solvers.text()
                            #                updated_solvers = current_solvers +" "+bc['solvers of eq']['name']
                            #                active_solvers.setText(updated_solvers)
                        else:
                            print("LABEL TEXT SET()", label.text())
                            if label.text() != 'Create new solver':
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

        # check QLineEdit for Active solvers and update CheckBox for new solver
        for active_solvers_label in self.dynamic_widgets:
            if active_solvers_label.text() == "Active solvers":
                print("ACTIVE SOLVERS")
                active_solvers = self.dynamic_widgets[active_solvers_label]
                current_solvers = active_solvers.text().split()
                if bc["name"].replace(' ','_') + '_solver' in current_solvers:
                    self.check_new_solver.setChecked(1)

    def update_element_name(self, items, new_name):
        """Check if new element name already exists in QListWidget.

        """
        if new_name != '':
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
            return new_name
        else:
            if self.list_of_elements.count() == 0:
                new_name = self.element_name+"_"+str(0)
                return new_name

            for i in range(0, self.list_of_elements.count()+1):
                new_name = self.element_name+"_"+str(i)
                exists = self.list_of_elements.findItems(new_name,
                                                         QtCore.Qt.MatchExactly)
                if len(exists) == 0:
                    return new_name
            return False

    def widgets_to_dict(self, dynamic_widgets, data, i):
        self.dynamic_widgets = dynamic_widgets
        #print("widgets_to_dict test", data)
        # Iterate over widgets, get their new info and update dictionary
        print(i)
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
                print("setting.text()", setting.text())
                if setting.text() == "Create new solver":
                    #print('testing active solvers')
                    if setting.isChecked():
                        from constants import DEFAULT_SOLVER
                        df_solver = copy.deepcopy(DEFAULT_SOLVER)
                        df_solver['name'] = data[i]['name'].replace(' ','_') + '_solver'
                        #print('DFSOLVER', data[i]['name'].replace(' ','_') + '_solver', df_solver)
                        data[i]["solvers of eq"] = df_solver
                        if not df_solver['name'] in data[i]['active solvers']:
                            data[i]['active solvers'] = data[i]['active solvers']+' '+df_solver['name']
                        setting.setChecked(1)
                        print("setting.ISCHECKED()", setting.text())
                else:
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
                #self.dict_to_widgets(list_of_elements.currentItem())
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
        #print("Error setting radio and combo!!!")

    def getSelected(self):
        for item in self.radio_combo_widgets:
            if item[0].isChecked():
                if item[1] is not None:
                    setting = item[1].currentText()
                    return [item[0].text(), setting]
                return [item[0].text(), None]
        return [None, None]

