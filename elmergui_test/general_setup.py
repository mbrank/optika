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
            data = {}
            #print('test')

        self.dynamic_widgets = {} # dictionary that contains qwidgets
                                  # of different blocks,
                                  # i. e. equations, boundary
                                  # conditions, initial_conditions

        #self.initUI(self.data)

        #def initUI(self, data):
        general_setup_layout = QGridLayout()
        # Header
        headerBox = QGroupBox('Header')
        headerLayout = QGridLayout()
        headerBox.setLayout(headerLayout)
        self.dynamic_widgets['Header'] = {}
        general_setup_layout.addWidget(headerBox)
        # Simulation
        simulationBox = QGroupBox('Simulation')
        simulationLayout = QGridLayout()
        simulationBox.setLayout(simulationLayout)
        self.dynamic_widgets['Simulation'] = {}
        general_setup_layout.addWidget(simulationBox)
        # Constants
        constantsBox = QGroupBox('Constants')
        constantsLayout = QGridLayout()
        constantsBox.setLayout(constantsLayout)
        self.dynamic_widgets['Constants'] = {}
        general_setup_layout.addWidget(constantsBox)

        # add widgets to Header group
        # checkbox
        self.checkWarning = QCheckBox("Check keywords warning")
        self.checkWarning.setChecked(True)
        headerLayout.addWidget(self.checkWarning, 0, 0)
        # meshDB
        header_grid_layout = QGridLayout()
        meshDB_label = QLabel("MeshDB")
        self.meshDB_lineedit1 = QLineEdit(".")
        self.meshDB_lineedit2 = QLineEdit(".")
        self.dynamic_widgets['Header']["MeshDB"] = [self.meshDB_lineedit1,
                                                    self.meshDB_lineedit2]
        header_grid_layout.addWidget(meshDB_label, 0, 0)
        header_grid_layout.addWidget(self.meshDB_lineedit1, 0 ,1)
        header_grid_layout.addWidget(self.meshDB_lineedit2, 0, 2)
        # Include path widget
        includePath_label = QLabel("Include path")
        self.includePath_lineedit = QLineEdit()
        self.dynamic_widgets['Header']["Include path"] = self.includePath_lineedit
        header_grid_layout.addWidget(includePath_label, 1, 0)
        header_grid_layout.addWidget(self.includePath_lineedit, 1, 1)
        # Include result directory widget
        resultsDir_layout = QHBoxLayout()
        resultsDir_label = QLabel("Results directory")
        self.resultsDir_lineedit = QLineEdit()
        self.dynamic_widgets['Header']["Results directory"] = self.resultsDir_lineedit
        header_grid_layout.addWidget(resultsDir_label, 2, 0)
        header_grid_layout.addWidget(self.resultsDir_lineedit, 2, 1)
        headerLayout.addLayout(header_grid_layout, 1, 0)

        # simulation
        max_output_level_label = QLabel("Max. output level")
        simulationLayout.addWidget(max_output_level_label, 0, 0)
        self.max_output_level_combobox = QComboBox()
        self.max_output_level_combobox.addItems(['1', '2', '3', '4', '5',
                                            '6', '7', '8', '9', '10'])
        self.max_output_level_combobox.setCurrentIndex(4)
        self.dynamic_widgets['Simulation']["Max. output level"] = self.max_output_level_combobox
        simulationLayout.addWidget(self.max_output_level_combobox, 0, 1)
        steady_state_max_iter_label = QLabel("Steady state max. iter")
        self.steady_state_max_iter_lineedit = QLineEdit()
        self.steady_state_max_iter_lineedit.setText("1")
        self.dynamic_widgets['Simulation']["Steady state max. iter"] = self.steady_state_max_iter_lineedit
        simulationLayout.addWidget(steady_state_max_iter_label, 0, 2)
        simulationLayout.addWidget(self.steady_state_max_iter_lineedit, 0, 3)
        
        coordinate_system_label = QLabel("Coordinate system")
        simulationLayout.addWidget(coordinate_system_label, 1, 0)
        self.coordinate_system_combobox = QComboBox()
        self.coordinate_system_combobox.addItems(['Cartesian',
                                             'Axi Symmetric',
                                             'Cylindric symmetric'])
        self.coordinate_system_combobox.setCurrentIndex(0)
        self.dynamic_widgets['Simulation']["Coordinate system"] = self.coordinate_system_combobox
        simulationLayout.addWidget(self.coordinate_system_combobox, 1, 1)
        timestepping_method_label = QLabel("Timestepping method")
        simulationLayout.addWidget(timestepping_method_label, 1, 2)
        self.timestepping_method_combobox = QComboBox()
        self.timestepping_method_combobox.addItems(['BDF'])
        self.timestepping_method_combobox.setCurrentIndex(0)
        self.dynamic_widgets['Simulation']["Timestepping method"] = self.timestepping_method_combobox
        simulationLayout.addWidget(self.timestepping_method_combobox, 1, 3)

        coordinate_mapping_label = QLabel("Coordinate mapping")
        self.coordinate_mapping_lineedit = QLineEdit()
        self.coordinate_mapping_lineedit.setText("1 2 3")
        self.dynamic_widgets['Simulation']["Coordinate mapping"] = self.coordinate_mapping_lineedit
        simulationLayout.addWidget(coordinate_mapping_label, 2, 0)
        simulationLayout.addWidget(self.coordinate_mapping_lineedit, 2, 1)
        bdf_order_label = QLabel("BDF order")
        simulationLayout.addWidget(bdf_order_label, 2, 2)
        self.bdf_order_combobox = QComboBox()
        self.bdf_order_combobox.addItems(['1',
                                     '2',
                                     '3', '4', '5'])
        self.bdf_order_combobox.setCurrentIndex(0)
        self.dynamic_widgets['Simulation']["BDF order"] = self.bdf_order_combobox
        simulationLayout.addWidget(self.bdf_order_combobox, 2, 3)

        simulation_type_label = QLabel("Simulation type")
        simulationLayout.addWidget(simulation_type_label, 3, 0)
        self.simulation_type_combobox = QComboBox()
        self.simulation_type_combobox.addItems(['Steady state',
                                             'Transient',
                                             'Scanning'])
        self.simulation_type_combobox.setCurrentIndex(0)
        self.dynamic_widgets['Simulation']["Simulation type"] = self.simulation_type_combobox
        simulationLayout.addWidget(self.simulation_type_combobox, 3, 1)
        timestep_intervals_label = QLabel("Timestep intervals")
        self.timestep_intervals_lineedit = QLineEdit()
        self.dynamic_widgets['Simulation']["Timestep intervals"] = self.timestep_intervals_lineedit
        simulationLayout.addWidget(timestep_intervals_label, 3, 2)
        simulationLayout.addWidget(self.timestep_intervals_lineedit, 3, 3)

        output_intervals_label = QLabel("Output intervals")
        self.output_intervals_lineedit = QLineEdit()
        self.output_intervals_lineedit.setText("1")
        self.dynamic_widgets['Simulation']["Output intervals"] = self.output_intervals_lineedit
        simulationLayout.addWidget(output_intervals_label, 4, 0)
        simulationLayout.addWidget(self.output_intervals_lineedit, 4, 1)
        timestep_sizes_label = QLabel("Timestep sizes")
        self.timestep_sizes_lineedit = QLineEdit()
        self.dynamic_widgets['Simulation']["Timestep sizes"] = self.timestep_sizes_lineedit
        simulationLayout.addWidget(timestep_sizes_label, 4, 2)
        simulationLayout.addWidget(self.timestep_sizes_lineedit, 4, 3)
        
        solver_input_file_label = QLabel("Solver input file")
        self.solver_input_file_lineedit = QLineEdit()
        self.solver_input_file_lineedit.setText("case.sif")
        self.dynamic_widgets['Simulation']["Solver input file"] = self.solver_input_file_lineedit
        simulationLayout.addWidget(solver_input_file_label, 5, 0)
        simulationLayout.addWidget(self.solver_input_file_lineedit, 5, 1)

        post_file_label = QLabel("Post file")
        self.post_file_lineedit = QLineEdit()
        self.post_file_lineedit.setText("case.vtu")
        self.dynamic_widgets['Simulation']["Post file"] = self.post_file_lineedit
        simulationLayout.addWidget(post_file_label, 5, 2)
        simulationLayout.addWidget(self.post_file_lineedit, 5, 3)

        mesh_names_label = QLabel("Use Mesh Names")
        self.mesh_names_lineedit = QLineEdit()
        self.mesh_names_lineedit.setText("Logical True")
        self.dynamic_widgets['Simulation']["Use Mesh Names"] = self.mesh_names_lineedit
        simulationLayout.addWidget(mesh_names_label, 6, 0)
        simulationLayout.addWidget(self.mesh_names_lineedit, 6, 1)

        
        # constants
        gravity_label = QLabel("Gravity")
        self.gravity_lineedit = QLineEdit()
        self.gravity_lineedit.setText("0 -1 0 9.82")
        self.dynamic_widgets['Constants']["Gravity"] = self.gravity_lineedit
        constantsLayout.addWidget(gravity_label, 0, 0)
        constantsLayout.addWidget(self.gravity_lineedit, 0, 1)

        boltzmann_label = QLabel("Boltzmann")
        self.boltzmann_lineedit = QLineEdit()
        self.boltzmann_lineedit.setText("1.3807e-23")
        self.dynamic_widgets['Constants']["Boltzmann"] = self.boltzmann_lineedit
        constantsLayout.addWidget(boltzmann_label, 0, 2)
        constantsLayout.addWidget(self.boltzmann_lineedit, 0, 3)

        stefan_boltzmann_label = QLabel("Stefan-Boltzmann")
        self.stefan_boltzmann_lineedit = QLineEdit()
        self.stefan_boltzmann_lineedit.setText("5.67e-08")
        self.dynamic_widgets['Constants']["Stefan-Boltzmann"] = self.stefan_boltzmann_lineedit
        constantsLayout.addWidget(stefan_boltzmann_label, 1, 0)
        constantsLayout.addWidget(self.stefan_boltzmann_lineedit, 1, 1)

        unit_change_label = QLabel("Unit change")
        self.unit_change_lineedit = QLineEdit()
        self.unit_change_lineedit.setText("1.602e-19")
        self.dynamic_widgets['Constants']["Unit change"] = self.unit_change_lineedit
        constantsLayout.addWidget(unit_change_label, 1, 2)
        constantsLayout.addWidget(self.unit_change_lineedit, 1, 3)

        vacuum_permittivity_label = QLabel("Vacuum permittivity")
        self.vacuum_permittivity_lineedit = QLineEdit()
        self.vacuum_permittivity_lineedit.setText("1.602e-19")
        self.dynamic_widgets['Constants']["Vacuum permittivity"] = self.vacuum_permittivity_lineedit
        constantsLayout.addWidget(vacuum_permittivity_label, 2, 0)
        constantsLayout.addWidget(self.vacuum_permittivity_lineedit, 2, 1)

        self.setLayout(general_setup_layout)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('General settings')
        #self.exec()

    def applyChanges(self):
        """Apply button hit"""
        # Hide window, but keep contents in memory
        self.hide()
