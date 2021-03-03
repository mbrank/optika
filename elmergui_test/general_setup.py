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
                             QGridLayout, QComboBox)

class GeneralSetup(QDialog):
    """Class that provides the General setup dialog and its functionality"""

    def __init__(self, data, parent=None):
        """Constructor.

        Args:
        -----
        path_forms: str
            String containing the path to the ui-files defining the look of the
            window.
        """
        super(GeneralSetup, self).__init__(parent)
        #uic.loadUi(path_forms + "generalsetup.ui", self)
        #self.simulationFreeTextEdit.setText("Use Mesh Names = Logical True")
        #self.acceptButton.clicked.connect(self.applyChanges)
        self.data = data
        if not self.data:
            data = {"MeshDB": 0,
                    "Include path": 0,
                    "results directory": 0,
                    "Free text": 0}
            print('test')

        #self.initUI(self.data)

        #def initUI(self, data):
        layout = QGridLayout()
        # Header
        headerBox = QGroupBox('Header')
        headerLayout = QGridLayout()
        headerBox.setLayout(headerLayout)
        layout.addWidget(headerBox)
        # Simulation
        simulationBox = QGroupBox('Simulation')
        simulationLayout = QGridLayout()
        simulationBox.setLayout(simulationLayout)
        layout.addWidget(simulationBox)
        # Constants
        constantsBox = QGroupBox('Constants')
        constantsLayout = QGridLayout()
        constantsBox.setLayout(constantsLayout)
        layout.addWidget(constantsBox)

        # add widgets to Header group
        # checkbox
        checkWarning = QCheckBox("Check keywords warning")
        checkWarning.setChecked(True)
        headerLayout.addWidget(checkWarning, 0, 0)
        # meshDB
        header_grid_layout = QGridLayout()
        meshDB_label = QLabel("MeshDB")
        meshDB_lineedit1 = QLineEdit(".")
        meshDB_lineedit2 = QLineEdit(".")
        header_grid_layout.addWidget(meshDB_label, 0, 0)
        header_grid_layout.addWidget(meshDB_lineedit1, 0 ,1)
        header_grid_layout.addWidget(meshDB_lineedit2, 0, 2)
        # Include path widget
        includePath_label = QLabel("Include path")
        includePath_lineedit = QLineEdit()
        header_grid_layout.addWidget(includePath_label, 1, 0)
        header_grid_layout.addWidget(includePath_lineedit, 1, 1)
        # Include result directory widget
        resultsDir_layout = QHBoxLayout()
        resultsDir_label = QLabel("Results directory")
        resultsDir_lineedit = QLineEdit()
        header_grid_layout.addWidget(resultsDir_label, 2, 0)
        header_grid_layout.addWidget(resultsDir_lineedit, 2, 1)
        headerLayout.addLayout(header_grid_layout, 1, 0)

        # simulation
        max_output_level_label = QLabel("Max. output level")
        simulationLayout.addWidget(max_output_level_label, 0, 0)
        max_output_level_combobox = QComboBox()
        max_output_level_combobox.addItems(['1', '2', '3', '4', '5',
                                            '6', '7', '8', '9', '10'])
        max_output_level_combobox.setCurrentIndex(4)
        simulationLayout.addWidget(max_output_level_combobox, 0, 1)
        steady_state_max_iter_label = QLabel("Steady state max. iter")
        steady_state_max_iter_lineedit = QLineEdit()
        steady_state_max_iter_lineedit.setText("1")
        simulationLayout.addWidget(steady_state_max_iter_label, 0, 2)
        simulationLayout.addWidget(steady_state_max_iter_lineedit, 0, 3)
        
        coordinate_system_label = QLabel("Coordinate system")
        simulationLayout.addWidget(coordinate_system_label, 1, 0)
        coordinate_system_combobox = QComboBox()
        coordinate_system_combobox.addItems(['Cartesian',
                                             'Axisymmetric',
                                             'Cylindric symmetric'])
        coordinate_system_combobox.setCurrentIndex(0)
        simulationLayout.addWidget(coordinate_system_combobox, 1, 1)
        timestepping_method_label = QLabel("Time stepping method")
        simulationLayout.addWidget(timestepping_method_label, 1, 2)
        timestepping_method_combobox = QComboBox()
        timestepping_method_combobox.addItems(['BDF'])
        timestepping_method_combobox.setCurrentIndex(0)
        simulationLayout.addWidget(timestepping_method_combobox, 1, 3)

        coordinate_mapping_label = QLabel("Coordinate mapping")
        coordinate_mapping_lineedit = QLineEdit()
        coordinate_mapping_lineedit.setText("1 2 3")
        simulationLayout.addWidget(coordinate_mapping_label, 2, 0)
        simulationLayout.addWidget(coordinate_mapping_lineedit, 2, 1)
        bdf_order_label = QLabel("BDF order")
        simulationLayout.addWidget(bdf_order_label, 2, 2)
        bdf_order_combobox = QComboBox()
        bdf_order_combobox.addItems(['1',
                                     '2',
                                     '3', '4', '5'])
        bdf_order_combobox.setCurrentIndex(0)
        simulationLayout.addWidget(bdf_order_combobox, 2, 3)

        simulation_type_label = QLabel("Simulation type")
        simulationLayout.addWidget(simulation_type_label, 3, 0)
        simulation_type_combobox = QComboBox()
        simulation_type_combobox.addItems(['Steady state',
                                             'Transient',
                                             'Scanning'])
        simulation_type_combobox.setCurrentIndex(0)
        simulationLayout.addWidget(simulation_type_combobox, 3, 1)
        timestep_intervals_label = QLabel("Timestep intervals")
        timestep_intervals_lineedit = QLineEdit()
        simulationLayout.addWidget(timestep_intervals_label, 3, 2)
        simulationLayout.addWidget(timestep_intervals_lineedit, 3, 3)

        output_intervals_label = QLabel("Output intervals")
        output_intervals_lineedit = QLineEdit()
        output_intervals_lineedit.setText("1")
        simulationLayout.addWidget(output_intervals_label, 4, 0)
        simulationLayout.addWidget(output_intervals_lineedit, 4, 1)
        timestep_sizes_label = QLabel("Timestep sizes")
        timestep_sizes_lineedit = QLineEdit()
        simulationLayout.addWidget(timestep_sizes_label, 4, 2)
        simulationLayout.addWidget(timestep_sizes_lineedit, 4, 3)
        
        solver_input_file_label = QLabel("Solver input file")
        solver_input_file_lineedit = QLineEdit()
        solver_input_file_lineedit.setText("case.sif")
        simulationLayout.addWidget(solver_input_file_label, 5, 0)
        simulationLayout.addWidget(solver_input_file_lineedit, 5, 1)
        post_file_label = QLabel("Post file")
        post_file_lineedit = QLineEdit()
        post_file_lineedit.setText("case.vtu")
        simulationLayout.addWidget(post_file_label, 5, 2)
        simulationLayout.addWidget(post_file_lineedit, 5, 3)

        # constants
        gravity_label = QLabel("Gravity")
        gravity_lineedit = QLineEdit()
        gravity_lineedit.setText("0 -1 0 9.82")
        constantsLayout.addWidget(gravity_label, 0, 0)
        constantsLayout.addWidget(gravity_lineedit, 0, 1)

        boltzmann_label = QLabel("Boltzmann")
        boltzmann_lineedit = QLineEdit()
        boltzmann_lineedit.setText("1.3807e-23")
        constantsLayout.addWidget(boltzmann_label, 0, 2)
        constantsLayout.addWidget(boltzmann_lineedit, 0, 3)

        stefan_boltzmann_label = QLabel("Stefan-Boltzmann")
        stefan_boltzmann_lineedit = QLineEdit()
        stefan_boltzmann_lineedit.setText("5.67e-08")
        constantsLayout.addWidget(stefan_boltzmann_label, 1, 0)
        constantsLayout.addWidget(stefan_boltzmann_lineedit, 1, 1)

        unit_change_label = QLabel("Unit change")
        unit_change_lineedit = QLineEdit()
        unit_change_lineedit.setText("1.602e-19")
        constantsLayout.addWidget(unit_change_label, 1, 2)
        constantsLayout.addWidget(unit_change_lineedit, 1, 3)

        vacuum_permittivity_label = QLabel("Vacuum permittivity")
        vacuum_permittivity_lineedit = QLineEdit()
        vacuum_permittivity_lineedit.setText("1.602e-19")
        constantsLayout.addWidget(vacuum_permittivity_label, 2, 0)
        constantsLayout.addWidget(vacuum_permittivity_lineedit, 2, 1)

        self.setLayout(layout)
        # lbl1.move(15, 10)
        # lbl2 = QLabel('tutorials', self)
        # lbl2.move(35, 40)
        # lbl3 = QLabel('for programmers', self)
        # lbl3.move(55, 70)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('General settings')
        self.exec()



    def applyChanges(self):
        """Apply button hit"""
        # Hide window, but keep contents in memory
        self.hide()
