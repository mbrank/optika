# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 20:26:27 2016

@author: Rainer Jacob

General setup class
"""

from PyQt5.QtWidgets import (QInputDialog, QLineEdit, QDialog,
                             QApplication, QWidget, QLabel,
                             QHBoxLayout, QMainWindow, QCheckBox,
                             QPushButton, QVBoxLayout, QMessageBox,
                             QFileDialog, QStackedWidget, QGroupBox,
                             QGridLayout, QComboBox)
from PyQt5.QtGui import QFont
from base_sif import BaseSIF
from functools import partial

class Equations(BaseSIF):
    """Class that provides the General setup dialog and its functionality"""

    def __init__(self, data, parent=None):
        """Constructor.

        Args:
        -----
        path_forms: str
            String containing the path to the ui-files defining the look of the
            window.
        """
        super(Equations, self).__init__(parent)
        #uic.loadUi(path_forms + "generalsetup.ui", self)
        #self.simulationFreeTextEdit.setText("Use Mesh Names = Logical True")
        #self.acceptButton.clicked.connect(self.applyChanges)
        self.data = data
        print('eq data', self.data)
        if not self.data:
            data = {}
            #print('test equation')
        #print('test equation')
        self.element_name = 'Equation'
        self.electrostatics_tab = QWidget()
        self.mesh_update_tab = QWidget()
        self.heat_equation_tab = QWidget()
        self.heat_equation_tabUI()
        self.helmholtz_equation_tab = QWidget()
        self.result_output_tab = QWidget()
        self.navier_stokes_tab = QWidget()
        self.tabs = {'Electrostatics': self.electrostatics_tab,
                     'Mesh Update': self.mesh_update_tab,
                     'Heat Equation': self.heat_equation_tab,
                     'Helmholtz Equation': self.helmholtz_equation_tab,
                     'Result Output': self.result_output_tab,
                     'Navier-Stokes': self.navier_stokes_tab}

        for tab in self.tabs:
            #print('Tabs test equations')
            #print(type(self.tabs[tab]), tab)
            self.solver_tabs.addTab(self.tabs[tab], tab)

        #self.setLayout(self.layout)
        #self.setGeometry(300, 300, 250, 150)

        self.list_of_elements.itemClicked.connect(self.dict_to_widgets)
        self.apply_element.clicked.connect(partial(self.on_apply, self.list_of_elements, self.data))
        self.new_element.clicked.connect(partial(self.on_new, self.list_of_elements, self.data))
        self.ok_element.clicked.connect(partial(self.on_ok, self.list_of_elements, self.data))
        self.delete_element.clicked.connect(partial(self.on_delete, self.list_of_elements, self.data))

        items = []
        for i in range(self.list_of_elements.count()):
            items.append(self.list_of_elements.item(i))
        self.update_element_name(items, self.element_name)
 
        self.element_settings.setText('Create new solver')
        self.element_settings.hide()

        self.check_new_solver = QCheckBox("Create new solver")
        self.check_existing_solver = QCheckBox("Add existing solver")
        self.combobox_existing_solver = QComboBox()
        self.combobox_existing_solver.addItems(["1", "2", "3"])
        self.dynamic_widgets[self.check_new_solver] = self.check_new_solver
        self.solver_hlayout = QHBoxLayout()
        self.solver_hlayout.addWidget(self.check_existing_solver)
        self.solver_hlayout.addWidget(self.combobox_existing_solver)
        self.vertical_layout.addWidget(self.check_new_solver)
        self.vertical_layout.addLayout(self.solver_hlayout)
        self.update_element_name(items, "Equation")
        self.setWindowTitle('Equations')
        #self.exec()

    #def dict_to_widgets(self, item):
    #    #print("clicked item in list", item.text())
    #    #print("self.data", self.data)
    #    for eqs in self.data:
    #        #print("Comparison", self.data[eqs]["Name"], item.text())
    #        if self.data[eqs]["Name".lower()] == item.text():
    #            eq = self.data[eqs]
    #            #print('test equation show')
    #            self.lineedit_name_eq.setText(eq["Name"])
    #            break

        #self.checkbox_active = QCheckBox()
        #self.lineedit_priority = QLineEdit()
        #self.combobox_options = QComboBox()
        #self.combobox_convection = QComboBox()

    def applyChanges(self):
        """Apply button hit"""
        # Hide window, but keep contents in memory
        self.hide()

    def heat_equation_tabUI(self):

        title_font = QFont()
        title_font.setBold(True)
        title_font.setUnderline(True)

        layout_heat_equation_tab = QGridLayout()
        label_active_set = QLabel("Active for this equation set")
        label_active_set.setFont(title_font)
        label_active = QLabel("Active")
        self.checkbox_active = QCheckBox()
        self.label_active_solvers = QLabel("Active solvers")
        self.lineedit_active_solvers = QLineEdit()
        self.dynamic_widgets[label_active] = self.checkbox_active
        self.dynamic_widgets[self.label_active_solvers] = self.lineedit_active_solvers
        
        layout_heat_equation_tab.addWidget(label_active_set, 0, 0)
        layout_heat_equation_tab.addWidget(label_active, 1, 0)
        layout_heat_equation_tab.addWidget(self.checkbox_active, 1, 1)
        layout_heat_equation_tab.addWidget(self.label_active_solvers, 2, 0)
        layout_heat_equation_tab.addWidget(self.lineedit_active_solvers, 2, 1)

        label_priority_set = QLabel("Give Execution priority")
        label_priority_set.setFont(title_font)
        label_priority = QLabel("Priority")
        self.lineedit_priority = QLineEdit()
        layout_heat_equation_tab.addWidget(label_priority_set, 3, 0)
        layout_heat_equation_tab.addWidget(label_priority, 4, 0)
        layout_heat_equation_tab.addWidget(self.lineedit_priority, 4, 1)

        label_options_set = QLabel("Options")
        label_options_set.setFont(title_font)
        label_options = QLabel("Phase Change Model")
        self.combobox_options = QComboBox()
        self.combobox_options.addItem("None")
        self.combobox_options.addItem("Spatial 1")
        self.combobox_options.addItem("Spatial 2")
        self.combobox_options.addItem("Temporal")
        layout_heat_equation_tab.addWidget(label_options_set, 5, 0)
        layout_heat_equation_tab.addWidget(label_options, 6, 0)
        layout_heat_equation_tab.addWidget(self.combobox_options, 6, 1)
        self.dynamic_widgets[label_options] = self.combobox_options

        label_convection_set = QLabel("Convection")
        label_convection_set.setFont(title_font)
        label_convection = QLabel("Convection")
        self.combobox_convection = QComboBox()
        self.combobox_convection.addItem("None")
        self.combobox_convection.addItem("Constant")
        self.combobox_convection.addItem("Computed")
        layout_heat_equation_tab.addWidget(label_convection_set, 7, 0)
        layout_heat_equation_tab.addWidget(label_convection, 8, 0)
        layout_heat_equation_tab.addWidget(self.combobox_convection, 8, 1)
        self.dynamic_widgets[label_options] = self.combobox_options

        self.heat_equation_tab.setLayout(layout_heat_equation_tab)
