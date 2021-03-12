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

class BoundaryConditions(BaseSIF):
    """Class that provides the General setup dialog and its functionality"""

    def __init__(self, data, parent=None):
        """Constructor.

        Args:
        -----
        path_forms: str
            String containing the path to the ui-files defining the look of the
            window.
        """
        super(BoundaryConditions, self).__init__(parent)
        #uic.loadUi(path_forms + "generalsetup.ui", self)
        #self.simulationFreeTextEdit.setText("Use Mesh Names = Logical True")
        #self.acceptButton.clicked.connect(self.applyChanges)
        self.data = data
        if not self.data:
            data = {"test":"test1"}
            #print('test equation')
        #print('test equation')
        self.element_name = 'Boundary_Condition'
        self.general_tab = QWidget()
        self.electrostatics_tab = QWidget()
        self.mesh_update_tab = QWidget()
        self.heat_equation_tab = QWidget()
        self.heat_equation_tabUI()
        self.helmholtz_equation_tab = QWidget()
        self.result_output_tab = QWidget()
        self.navier_stokes_tab = QWidget()
        self.tabs = {'General': self.general_tab,
                     'Electrostatics': self.electrostatics_tab,
                     'Mesh Update': self.mesh_update_tab,
                     'Heat Equation': self.heat_equation_tab,
                     'Helmholtz Equation': self.helmholtz_equation_tab,
                     'Navier-Stokes': self.navier_stokes_tab}

        for tab in self.tabs:
            #print('Tabs test equations')
            #print(type(self.tabs[tab]), tab)
            self.solver_tabs.addTab(self.tabs[tab], tab)

        self.list_of_elements.itemClicked.connect(self.dict_to_widgets)
        self.apply_element.clicked.connect(partial(self.on_apply, self.list_of_elements, self.data))
        self.new_element.clicked.connect(partial(self.on_new, self.list_of_elements, self.data))
        self.ok_element.clicked.connect(partial(self.on_ok, self.list_of_elements, self.data))
        self.delete_element.clicked.connect(partial(self.on_delete, self.list_of_elements, self.data))

        #self.setLayout(self.layout)
        #self.setGeometry(300, 300, 250, 150)
        items = []
        for i in range(self.list_of_elements.count()):
            items.append(self.list_of_elements.item(i))
        self.update_element_name(items, self.element_name)
        self.element_settings.setText('Edit solver settings')
        self.setWindowTitle('Boundary Conditions')


    #def applyChanges(self):
    #    """Apply button hit"""
    #    # Hide window, but keep contents in memory
    #    self.hide()


    def heat_equation_tabUI(self):

        title_font = QFont()
        title_font.setBold(True)
        title_font.setUnderline(True)

        layout_heat_equation_tab = QGridLayout()
        label_dirichlet_set = QLabel("Dirichlet Conditions")
        label_dirichlet_set.setFont(title_font)
        layout_heat_equation_tab.addWidget(label_dirichlet_set, 0, 0)

        self.label_temperature = QLabel("Temperature")
        self.lineedit_temperature = QLineEdit()
        self.dynamic_widgets[self.label_temperature] = self.lineedit_temperature
        layout_heat_equation_tab.addWidget(self.label_temperature, 1, 0)
        layout_heat_equation_tab.addWidget(self.lineedit_temperature, 1, 1)

        self.label_temperature_cond = QLabel("Temperature Condition")
        self.checkbox_temperature_cond = QLineEdit()
        self.dynamic_widgets[self.label_temperature_cond] = self.checkbox_temperature_cond
        layout_heat_equation_tab.addWidget(self.label_temperature_cond, 2, 0)
        layout_heat_equation_tab.addWidget(self.checkbox_temperature_cond, 2, 1)

        self.label_heat_flux_set = QLabel("Heat Flux Conditions")
        self.label_heat_flux_set.setFont(title_font)
        layout_heat_equation_tab.addWidget(self.label_heat_flux_set, 3, 0)

        self.label_heat_flux = QLabel("Heat Flux")
        self.lineedit_heat_flux = QLineEdit()
        self.dynamic_widgets[self.label_heat_flux] = self.lineedit_heat_flux
        layout_heat_equation_tab.addWidget(self.label_heat_flux, 4, 0)
        layout_heat_equation_tab.addWidget(self.lineedit_heat_flux, 4, 1)

        self.label_temperature_cond = QLabel("Heat Transfer Coefficient")
        self.checkbox_temperature_cond = QLineEdit()
        self.dynamic_widgets[self.label_temperature_cond] = self.checkbox_temperature_cond
        layout_heat_equation_tab.addWidget(self.label_temperature_cond, 5, 0)
        layout_heat_equation_tab.addWidget(self.checkbox_temperature_cond, 5, 1)

        self.label_ext_temperature_cond = QLabel("External temperature")
        self.checkbox_ext_temperature_cond = QLineEdit()
        self.dynamic_widgets[self.label_ext_temperature_cond] = self.checkbox_ext_temperature_cond
        layout_heat_equation_tab.addWidget(self.label_ext_temperature_cond, 6, 0)
        layout_heat_equation_tab.addWidget(self.checkbox_ext_temperature_cond, 6, 1)

        self.label_latent_heat_set = QLabel("Latent Heat of Phase Change")
        self.label_latent_heat_set.setFont(title_font)
        layout_heat_equation_tab.addWidget(self.label_latent_heat_set, 7, 0)

        self.label_phase_change = QLabel("Phase Change")
        self.checkbox_phase_change = QCheckBox()
        self.dynamic_widgets[self.label_phase_change] = self.checkbox_phase_change
        layout_heat_equation_tab.addWidget(self.label_phase_change, 8, 0)
        layout_heat_equation_tab.addWidget(self.checkbox_phase_change, 8, 1)

        self.label_heat_gapset = QLabel("Heat Gap")
        self.label_heat_gapset.setFont(title_font)
        layout_heat_equation_tab.addWidget(self.label_heat_gapset, 9, 0)

        self.label_heat_gap = QLabel("Heat Gap")
        self.checkbox_heat_gap = QCheckBox()
        self.dynamic_widgets[self.label_heat_gap] = self.checkbox_heat_gap
        layout_heat_equation_tab.addWidget(self.label_heat_gap, 10, 0)
        layout_heat_equation_tab.addWidget(self.checkbox_heat_gap, 10, 1)

        self.heat_equation_tab.setLayout(layout_heat_equation_tab)
