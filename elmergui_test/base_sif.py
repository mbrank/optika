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
        #self.list_of_elements.insertItem(0, "Red")
        #self.list_of_elements.insertItem(1, "Orange")
        #self.list_of_elements.insertItem(2, "Blue")
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

        #self.apply_element.clicked.connect(partial(self.on_apply, self.list_of_elements))

        self.setLayout(self.layout)
        self.setGeometry(300, 300, 250, 150)
        #self.setWindowTitle('General settings')
        #self.exec()

    def on_apply(self, list_of_elements, data):
        print("Clicking on Apply!!!")
        print("item in Apply!!!")
        print(list_of_elements.currentItem().text())
        print(data)
        print("test 2")
        for i in data:
            print("test 3", data[i])
            print("test 4", data[i]['name'])
            if data[i]['name'] == list_of_elements.currentItem().text():
                print("test 4")
                for widget in self.dynamic_widgets:
                    print("test 3")
                    parameter = widget
                    setting = self.dynamic_widgets[widget]
                    setting_type = setting.metaObject().className() 
                    #print("parameter.text()", parameter.text())
                    #print("setting.text()", setting.text())
                    #data[i][parameter.text().lower()] = setting.text()
                    print("setting_type ", setting_type)
                    print("parameter_type ", setting_type)                    
                    if setting_type == "QLineEdit":
                        setting = setting.text().lower()
                        parameter = parameter.text().lower()
                        data[i][parameter] = setting
                    elif setting_type == "QCheckBox":
                        parameter = parameter.text().lower()
                        print('parameter----------------aa-------', parameter)
                        if setting.isChecked():
                            data[i][parameter] = "Logical True"
                        else:
                            data[i][parameter] = "Logical False"
                    elif setting_type == "QComboBox":
                        #idx = widget.findText("None")
                        #widget.setCurrentIndex(idx)
                        setting = setting.currentText()
                        parameter = parameter.text()
                        data[i][parameter] = setting
                    elif setting_type == "RadioComboGroup":
                        #print("RadioComboGroup --------------------------v")
                        #print("RadioComboGroup", bc.get("Linear System "+setting+" Method"))
                        #combo_text = bc.get("Linear System "+str(setting)+" Method")
                        #widget.setSelected(setting, combo_text)
                        data_params = setting
                        print('data_params', data_params)
                        setting = setting.getSelected()
                        print("setting.getSelected()----->>>>>>", setting)
                        if setting[1] != None:
                            parameter1 = "Linear System Solver"
                            setting1 = setting[0]
                            data[i][parameter1] = setting1
                            parameter2 = "Linear System "+setting[0]+"Method"
                            setting2 = setting[1]
                            data[i][parameter2] = setting2

                        elif setting[1] == None:
                            parameter = data_params.text()
                            setting = setting[0]
                            data[i][parameter] = setting
                            
                        #print("RadioComboGroup --------------------------v", widget.text().lower(), "Linear System Solver".lower())
                        #if widget.text().lower() == "Linear System Solver".lower():
                        #    combo_text = bc.get(str("Linear System "+str(setting)+" Method").lower())
                        #    print("Setting ------>", setting)
                        #elif widget.text().lower() == "Exec Solver".lower():
                        #    combo_text = None
                        #widget.setSelected(setting, combo_text)

                self.data = data
                self.update_tabs(list_of_elements.currentItem())
                break
        pass
   
    def update_tabs(self, item=None):
        """Virtual method of class BaseSIF. Only used in children of
        BaseSIF. It compares dictionaries self.data and self.dynamic_widgets
        and updates tabs according to parameters in self.data

            Input parameter: variable item of type QListWidget.item
        """

        print('---------------------------------------')
        if item == None:
            pass
        else:
            print("clicked item in list", item.text())
        print("self.data", self.data)
        for bcs in self.data:
            if item:
                print("Comparison", self.data[bcs]["Name".lower()], item.text(), 'self.data', self.data)
                if self.data[bcs]["Name".lower()] == item.text():
                    bc = self.data[bcs]
                    self.lineedit_name_eq.setText(bc["Name".lower()])
                else:
                    continue
            else:
                print('test equation show')
                bc = self.data[bcs]
            for label in self.dynamic_widgets:
                setting = bc.get(label.text().lower())
                widget = self.dynamic_widgets[label]
                widget_type = widget.metaObject().className()
                print("bc.get(label.text().lower()):", bc.get(label.text().lower()), "setting:", setting)
                if setting == None: # parameter not stored in bc block
                    if widget_type == "QLineEdit":
                        widget.setText("")
                    elif widget_type == "QCheckBox":
                        widget.setChecked(0)
                    elif widget_type == "QComboBox":
                        idx = widget.findText("None")
                        widget.setCurrentIndex(idx)
                    elif widget_type == "RadioComboGroup":
                        #print("RadioComboGroup --------------------------v")
                        #print("RadioComboGroup", bc.get("Linear System "+setting+" Method"))
                        #combo_text = bc.get("Linear System "+str(setting)+" Method")
                        #widget.setSelected(setting, combo_text)
                        print("RadioComboGroup --------------------------v", widget.text().lower(), "Linear System Solver".lower())
                        if widget.text().lower() == "Linear System Solver".lower():
                            combo_text = bc.get(str("Linear System "+str(setting)+" Method").lower())
                            print("Setting ------>", setting)
                        elif widget.text().lower() == "Exec Solver".lower():
                            combo_text = None
                        widget.setSelected(setting, combo_text)

                else:
                    if widget_type == "QLineEdit":
                        widget.setText(bc[label.text().lower()])
                    elif widget_type == "QCheckBox":
                        #print("Qcheckbox", label.text(), bc[label.text()].lower())
                        true = ['Logical True'.lower(), 'True'.lower()]
                        print("label.text().lower()", label.text().lower())
                        if bc[label.text().lower()].lower() in true:
                            widget.setChecked(1)
                        else:
                            widget.setChecked(0)
                    elif widget_type == "QComboBox":
                        try:
                            idx = widget.findText(bc[label.text().lower()])
                            widget.setCurrentIndex(idx)
                        except:
                            #print("QCombobox does not contain this parameter!")
                            pass
                    elif widget_type == "RadioComboGroup":
                        #print("RadioComboGroup", bc.get("Linear System "+str(setting)+" Method"))
                        print("RadioComboGroup --------------------------v", widget.text().lower(), "Linear System Solver".lower())
                        if widget.text().lower() == "Linear System Solver".lower():
                            combo_text = bc.get(str("Linear System "+str(setting)+" Method").lower())
                            print(bc)
                            print("Setting -- combo_text ---->", setting, combo_text)
                        elif widget.text().lower() == "Exec Solver".lower():
                            combo_text = None
                        widget.setSelected(setting, combo_text)
                        print("RadioComboGroup --------------------------v, combo_text", combo_text)
            break


        #if item:
        #    for bcs in self.data:
        #        print("Comparison", self.data[bcs]["Name".lower()], item.text(), 'self.data', self.data)
        #        if self.data[bcs]["Name".lower()] == item.text():
        #            bc = self.data[bcs]
        #            print('test equation show')
        #            self.lineedit_name_eq.setText(bc["Name".lower()])
        #            for label in self.dynamic_widgets:
        #                setting = bc.get(label.text().lower())
        #                widget = self.dynamic_widgets[label]
        #                widget_type = widget.metaObject().className()
        #                if setting == None: # parameter not stored in bc block
        #                    if widget_type == "QLineEdit":
        #                        widget.setText("")
        #                    elif widget_type == "QCheckBox":
        #                        widget.setChecked(0)
        #                    elif widget_type == "QComboBox":
        #                        idx = widget.findText("None")
        #                        widget.setCurrentIndex(idx)
        #                else:
        #                    if widget_type == "QLineEdit":
        #                        widget.setText(bc[label.text().lower()])
        #                    elif widget_type == "QCheckBox":
        #                        if bc[label.text()] == 'Logical True'.lower():
        #                            widget.setChecked(1)
        #                        else:
        #                            widget.setChecked(0)
        #                    elif widget_type == "QComboBox":
        #                        try:
        #                            idx = widget.findText(bc[label.text().lower()])
        #                            widget.setCurrentIndex(idx)
        #                        except:
        #                            print("QCombobox does not contain this parameter!")
        #            break
        #else:
        #    for bcs in self.data:
        #        #print("Comparison", self.data[bcs]["Name"], item.text(), 'self.data', self.data)
        #        #if self.data[bcs]["Name"] == item.text():
        #        bc = self.data[bcs]
        #        print('bc', bc)
        #        print('test equation show')
        #        #self.lineedit_name_eq.setText(bc["Name"])
        #        for label in self.dynamic_widgets:
        #            setting = bc.get(label.text().lower())
        #            widget = self.dynamic_widgets[label]
        #            widget_type = widget.metaObject().className()
        #            print('compare ', label.text(), setting, " ||| widget_type", widget_type)
        #            if setting == None: # parameter not stored in bc block
        #                if widget_type == "QLineEdit":
        #                    widget.setText("")
        #                elif widget_type == "QCheckBox":
        #                    widget.setChecked(0)
        #                elif widget_type == "QComboBox":
        #                    idx = widget.findText("None")
        #                    widget.setCurrentIndex(idx)
        #                elif widget_type == "QRadioButton":
        #                    #print("QRadioButton", widget.text(), self.dynamic_widgets[widget.text()])
        #                    pass
        #                elif widget_type == "RadioComboGroup":
        #                    print("RadioComboGroup --------------------------v")
        #                    print("RadioComboGroup", bc.get("Linear System "+setting+" Method"))
        #                    combo_text = bc.get("Linear System "+setting+" Method")
        #                    widget.setSelected(setting, combo_text)
        #            else:
        #                if widget_type == "QLineEdit":
        #                    widget.setText(bc[label.text()])
        #                elif widget_type == "QCheckBox":
        #                    #print("Qcheckbox", label.text(), bc[label.text()].lower())
        #                    true = ['Logical True'.lower(), 'True'.lower()]
        #                    if bc[label.text()].lower() in true:
        #                        widget.setChecked(1)
        #                    else:
        #                        widget.setChecked(0)
        #                elif widget_type == "QComboBox":
        #                    try:
        #                        idx = widget.findText(bc[label.text()])
        #                        widget.setCurrentIndex(idx)
        #                    except:
        #                        #print("QCombobox does not contain this parameter!")
        #                        pass
        #                elif widget_type == "RadioComboGroup":
        #                    print("RadioComboGroup --------------------------v")
        #                    print("RadioComboGroup", bc.get("Linear System "+setting+" Method"))
        #                    combo_text = bc.get("Linear System "+setting+" Method")
        #                    widget.setSelected(setting, combo_text)
        #        break


class RadioComboGroup(QWidget):
    """Documentation for RadioCombo

    """
    def __init__(self, title, radio_combo, parent=None):
        #super(RadioCombo, self).__init__(self, parent)
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

        #print(".metaObject().className()", self.metaObject().className())
        #rd_button_solv_ls_direct = QRadioButton("Direct")
        #combobox_solv_ls_direct = QComboBox()
        #combobox_solv_ls_direct.addItems(["Banded", "Umfpack", "MUMPS"])


        #rd_button_solv_ls_iter = QRadioButton("Iterative")
        #rd_button_solv_ls_iter.setChecked(True)
        #combobox_solv_ls_iter = QComboBox()
        #combobox_solv_ls_iter.addItems(["BiCGStab", "BiCGStabl", "TFQMR",
        #                                "GCR", "GCS", "CG", "GMRES"])

        #layout.addWidget(rd_button_solv_ls_iter, 1, 0)
        #layout.addWidget(combobox_solv_ls_iter, 1, 1)

        #rd_button_solv_ls_mltgrd = QRadioButton("Multigrid")
        #rd_button_solv_ls_iter.setChecked(True)
        #combobox_solv_ls_mltgrd = QComboBox()
        #combobox_solv_ls_mltgrd.addItems(["Jacobi", "CG", "BiCGStab"])

        #layout.addWidget(rd_button_solv_ls_mltgrd, 2, 0)
        #layout.addWidget(combobox_solv_ls_mltgrd, 2, 1)

    def setText(self, text):
        self.lbl_title.setText(text)

    def getText(self):
        return self.lbl_title.text()

    def text(self):
        return self.lbl_title.text()

    def setSelected(self, radio, combo):
        print("-------------------------------===============>", radio, combo, self.radio_combo_widgets)
        for item in self.radio_combo_widgets:
            print("item[0].text()---->", item[0].text(), radio, combo)
            if item[0].text() == radio:
                item[0].setChecked(True)
                if item[1] != None:
                    idx = item[1].findText(combo)
                    print("item[1].item---------->", combo, idx)
                    item[1].setCurrentIndex(idx)
                print('End\n---------------------------------')
                return None

        if True:
            print("Error setting radio and combo!!!")

    def getSelected(self):
        for item in self.radio_combo_widgets:
            if item[0].isChecked():
                if item[1] != None:
                    setting = item[1].currentText()
                    #print("item[1].item---------->", combo, idx)
                    return [item[0].text(), setting]
                else:
                    return [item[0].text(), None]
                break
