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

class BodyForces(BaseSIF):
    """Class that provides the General setup dialog and its functionality"""

    def __init__(self, data, parent=None):
        """Constructor.

        Args:
        -----
        path_forms: str
            String containing the path to the ui-files defining the look of the
            window.
        """
        super(BodyForces, self).__init__(parent)
        #uic.loadUi(path_forms + "generalsetup.ui", self)
        #self.simulationFreeTextEdit.setText("Use Mesh Names = Logical True")
        #self.acceptButton.clicked.connect(self.applyChanges)
        self.data = data
        if not self.data:
            self.data = {}
            #print('test equation')
        #print('test equation')
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
                     'Navier-Stokes': self.navier_stokes_tab}

        for tab in self.tabs:
            self.solver_tabs.addTab(self.tabs[tab], tab)

        self.list_of_elements.itemClicked.connect(self.update_tabs)
        self.apply_element.clicked.connect(partial(self.on_apply, self.list_of_elements, self.data))
        self.new_element.clicked.connect(partial(self.on_new, self.list_of_elements, self.data))
        self.ok_element.clicked.connect(partial(self.on_ok, self.list_of_elements, self.data))
        self.delete_element.clicked.connect(partial(self.on_delete, self.list_of_elements, self.data))

        #self.setLayout(self.layout)
        #self.setGeometry(300, 300, 250, 150)
        self.element_settings.setText('Edit solver settings')
        self.update_name("Body_Force")
        self.setWindowTitle('Body Forces')

    def applyChanges(self):
        """Apply button hit"""
        # Hide window, but keep contents in memory
        self.hide()


    def heat_equation_tabUI(self):

        title_font = QFont()
        title_font.setBold(True)
        title_font.setUnderline(True)

        layout_heat_equation_tab = QGridLayout()
        label_active_set = QLabel("Volume sources")
        label_active_set.setFont(title_font)
        layout_heat_equation_tab.addWidget(label_active_set, 0, 0)

        label_heat_source = QLabel("Heat Source")
        lineedit_heat_source = QLineEdit()
        layout_heat_equation_tab.addWidget(label_heat_source, 1, 0)
        layout_heat_equation_tab.addWidget(lineedit_heat_source, 1, 1)

        label_friction_heat = QLabel("Friction Heat")
        checkbox_friction_heat = QCheckBox()
        layout_heat_equation_tab.addWidget(label_friction_heat, 2, 0)
        layout_heat_equation_tab.addWidget(checkbox_friction_heat, 2, 1)

        label_joule_heat = QLabel("Joule Heat")
        checkbox_joule_heat = QCheckBox()
        layout_heat_equation_tab.addWidget(label_joule_heat, 3, 0)
        layout_heat_equation_tab.addWidget(checkbox_joule_heat, 3, 1)

        label_bdc_set = QLabel("Bodywise Dirichlet Conditions")
        label_bdc_set.setFont(title_font)
        layout_heat_equation_tab.addWidget(label_bdc_set, 4, 0)

        label_temperature = QLabel("Temperature")
        lineedit_temperature = QLineEdit()
        layout_heat_equation_tab.addWidget(label_temperature, 5, 0)
        layout_heat_equation_tab.addWidget(lineedit_temperature, 5, 1)

        label_temperature_cond = QLabel("Temperature Condition")
        lineedit_temperature_cond = QLineEdit()
        layout_heat_equation_tab.addWidget(label_temperature_cond, 6, 0)
        layout_heat_equation_tab.addWidget(lineedit_temperature_cond, 6, 1)

        label_bdc_set = QLabel("Perfusion")
        label_bdc_set.setFont(title_font)
        layout_heat_equation_tab.addWidget(label_bdc_set, 7, 0)

        label_temperature = QLabel("Perfusion Rate")
        lineedit_temperature = QLineEdit()
        layout_heat_equation_tab.addWidget(label_temperature, 8, 0)
        layout_heat_equation_tab.addWidget(lineedit_temperature, 8, 1)

        self.heat_equation_tab.setLayout(layout_heat_equation_tab)
