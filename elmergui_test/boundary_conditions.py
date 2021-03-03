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
            data = {"MeshDB": 0,
                    "Include path": 0,
                    "results directory": 0,
                    "Free text": 0}
            print('test equation')
        print('test equation')
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
            print('Tabs test equations')
            print(type(self.tabs[tab]), tab)
            self.solver_tabs.addTab(self.tabs[tab], tab)

        #self.setLayout(self.layout)
        #self.setGeometry(300, 300, 250, 150)
        self.element_settings.setText('Edit solver settings')
        self.setWindowTitle('General settings')
        self.exec()

    def applyChanges(self):
        """Apply button hit"""
        # Hide window, but keep contents in memory
        self.hide()


    def heat_equation_tabUI(self):

        title_font = QFont()
        title_font.setBold(True)
        title_font.setUnderline(True)

        layout_heat_equation_tab = QGridLayout()
        label_dirichlet_set = QLabel("Dirichlet Conditions")
        label_dirichlet_set.setFont(title_font)
        layout_heat_equation_tab.addWidget(label_dirichlet_set, 0, 0)

        label_temperature = QLabel("Temperature")
        lineedit_temperature = QLineEdit()
        layout_heat_equation_tab.addWidget(label_temperature, 1, 0)
        layout_heat_equation_tab.addWidget(lineedit_temperature, 1, 1)

        label_temperature_cond = QLabel("Temperature Condition")
        checkbox_temperature_cond = QLineEdit()
        layout_heat_equation_tab.addWidget(label_temperature_cond, 2, 0)
        layout_heat_equation_tab.addWidget(checkbox_temperature_cond, 2, 1)

        label_heat_flux_set = QLabel("Heat Flux Conditions")
        label_heat_flux_set.setFont(title_font)
        layout_heat_equation_tab.addWidget(label_heat_flux_set, 3, 0)

        label_temperature = QLabel("Heat Flux")
        lineedit_temperature = QLineEdit()
        layout_heat_equation_tab.addWidget(label_temperature, 4, 0)
        layout_heat_equation_tab.addWidget(lineedit_temperature, 4, 1)

        label_temperature_cond = QLabel("Heat Transfer Coefficient")
        checkbox_temperature_cond = QLineEdit()
        layout_heat_equation_tab.addWidget(label_temperature_cond, 5, 0)
        layout_heat_equation_tab.addWidget(checkbox_temperature_cond, 5, 1)

        label_ext_temperature_cond = QLabel("External temperature")
        checkbox_ext_temperature_cond = QLineEdit()
        layout_heat_equation_tab.addWidget(label_ext_temperature_cond, 6, 0)
        layout_heat_equation_tab.addWidget(checkbox_ext_temperature_cond, 6, 1)

        label_latent_heat_set = QLabel("Latent Heat of Phase Change")
        label_latent_heat_set.setFont(title_font)
        layout_heat_equation_tab.addWidget(label_latent_heat_set, 7, 0)

        label_phase_change = QLabel("Phase Change")
        checkbox_phase_change = QCheckBox()
        layout_heat_equation_tab.addWidget(label_phase_change, 8, 0)
        layout_heat_equation_tab.addWidget(checkbox_phase_change, 8, 1)

        label_heat_gap = QLabel("Heat Gap")
        label_heat_gap.setFont(title_font)
        layout_heat_equation_tab.addWidget(label_heat_gap, 9, 0)

        label_phase_change = QLabel("Phase Change")
        checkbox_phase_change = QCheckBox()
        layout_heat_equation_tab.addWidget(label_phase_change, 10, 0)
        layout_heat_equation_tab.addWidget(checkbox_phase_change, 10, 1)

        self.heat_equation_tab.setLayout(layout_heat_equation_tab)
