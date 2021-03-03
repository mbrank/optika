from PyQt5.QtWidgets import (QInputDialog, QLineEdit, QDialog,
                             QApplication, QWidget, QLabel,
                             QHBoxLayout, QMainWindow, QCheckBox,
                             QPushButton, QVBoxLayout, QMessageBox,
                             QFileDialog, QStackedWidget, QGroupBox,
                             QGridLayout, QComboBox)
from PyQt5.QtGui import QFont
from base_sif import BaseSIF

class Materials(BaseSIF):
    """Class that provides the General setup dialog and its functionality"""

    def __init__(self, data, parent=None):
        """Constructor.

        Args:
        -----
        path_forms: str
            String containing the path to the ui-files defining the look of the
            window.
        """
        super(Materials, self).__init__(parent)
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
        self.setWindowTitle('General settings')
        self.element_settings.setText("Show Material Library")
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

        label_properties_set = QLabel("Properties")
        label_properties_set.setFont(title_font)
        label_heat_conductivity = QLabel("Heat Conductivity")
        lineedit_heat_conductivity = QLineEdit()
        layout_heat_equation_tab.addWidget(label_properties_set, 0, 0)
        layout_heat_equation_tab.addWidget(label_heat_conductivity, 1, 0)
        layout_heat_equation_tab.addWidget(lineedit_heat_conductivity, 1, 1)

        label_heat_conductivity_model = QLabel("Heat Conductivity Model")
        lineedit_heat_conductivity_model = QLineEdit()
        layout_heat_equation_tab.addWidget(label_heat_conductivity_model, 2, 0)
        layout_heat_equation_tab.addWidget(lineedit_heat_conductivity_model, 2, 1)

        label_emissivity = QLabel("Emissivity")
        lineedit_emissivity = QLineEdit()
        layout_heat_equation_tab.addWidget(label_emissivity, 3, 0)
        layout_heat_equation_tab.addWidget(lineedit_emissivity, 3, 1)

        label_prandtl = QLabel("Turlbulent Prandtl Number")
        lineedit_prandtl = QLineEdit("0.85")
        layout_heat_equation_tab.addWidget(label_prandtl, 4, 0)
        layout_heat_equation_tab.addWidget(lineedit_prandtl, 4, 1)

        label_enthalpy = QLabel("Enthalpy")
        lineedit_enthalpy = QLineEdit()
        layout_heat_equation_tab.addWidget(label_enthalpy, 5, 0)
        layout_heat_equation_tab.addWidget(lineedit_enthalpy, 5, 1)

        label_specific_enthalpy = QLabel("Specific Enthalpy")
        lineedit_specific_enthalpy = QLineEdit()
        layout_heat_equation_tab.addWidget(label_specific_enthalpy, 6, 0)
        layout_heat_equation_tab.addWidget(lineedit_specific_enthalpy, 6, 1)

        label_pressure_coefficient = QLabel("Pressure Coefficient")
        lineedit_pressure_coefficient = QLineEdit()
        layout_heat_equation_tab.addWidget(label_pressure_coefficient, 7, 0)
        layout_heat_equation_tab.addWidget(lineedit_pressure_coefficient, 7, 1)

        self.heat_equation_tab.setLayout(layout_heat_equation_tab)
