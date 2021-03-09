from PyQt5.QtWidgets import (QInputDialog, QLineEdit, QDialog,
                             QApplication, QWidget, QLabel,
                             QHBoxLayout, QMainWindow, QCheckBox,
                             QPushButton, QVBoxLayout, QMessageBox,
                             QFileDialog, QStackedWidget, QGroupBox,
                             QGridLayout, QComboBox)
from PyQt5.QtGui import QFont
from base_sif import BaseSIF
from functools import partial

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
            self.data = {}
            print('test equation')
        print('test equation')
        self.general_tab = QWidget()
        self.general_tabUI()
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

        self.list_of_elements.itemClicked.connect(self.update_tabs)
        self.apply_element.clicked.connect(partial(self.on_apply, self.list_of_elements, self.data))
        self.new_element.clicked.connect(partial(self.on_new, self.list_of_elements, self.data))
        self.ok_element.clicked.connect(partial(self.on_ok, self.list_of_elements, self.data))
        self.delete_element.clicked.connect(partial(self.on_delete, self.list_of_elements, self.data))
        #self.setLayout(self.layout)
        #self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Materials')
        self.update_name("Material")
        self.element_settings.setText("Show Material Library")

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
        self.dynamic_widgets[label_heat_conductivity] = lineedit_heat_conductivity
        layout_heat_equation_tab.addWidget(label_properties_set, 0, 0)
        layout_heat_equation_tab.addWidget(label_heat_conductivity, 1, 0)
        layout_heat_equation_tab.addWidget(lineedit_heat_conductivity, 1, 1)

        label_heat_conductivity_model = QLabel("Heat Conductivity Model")
        lineedit_heat_conductivity_model = QLineEdit()
        self.dynamic_widgets[label_heat_conductivity_model] = lineedit_heat_conductivity_model
        layout_heat_equation_tab.addWidget(label_heat_conductivity_model, 2, 0)
        layout_heat_equation_tab.addWidget(lineedit_heat_conductivity_model, 2, 1)

        label_emissivity = QLabel("Emissivity")
        lineedit_emissivity = QLineEdit()
        self.dynamic_widgets[label_emissivity] = lineedit_emissivity
        layout_heat_equation_tab.addWidget(label_emissivity, 3, 0)
        layout_heat_equation_tab.addWidget(lineedit_emissivity, 3, 1)

        label_prandtl = QLabel("Turlbulent Prandtl Number")
        lineedit_prandtl = QLineEdit("0.85")
        self.dynamic_widgets[label_prandtl] = lineedit_prandtl
        layout_heat_equation_tab.addWidget(label_prandtl, 4, 0)
        layout_heat_equation_tab.addWidget(lineedit_prandtl, 4, 1)

        label_enthalpy = QLabel("Enthalpy")
        lineedit_enthalpy = QLineEdit()
        self.dynamic_widgets[label_enthalpy] = lineedit_enthalpy
        layout_heat_equation_tab.addWidget(label_enthalpy, 5, 0)
        layout_heat_equation_tab.addWidget(lineedit_enthalpy, 5, 1)

        label_specific_enthalpy = QLabel("Specific Enthalpy")
        lineedit_specific_enthalpy = QLineEdit()
        self.dynamic_widgets[label_specific_enthalpy] = lineedit_specific_enthalpy
        layout_heat_equation_tab.addWidget(label_specific_enthalpy, 6, 0)
        layout_heat_equation_tab.addWidget(lineedit_specific_enthalpy, 6, 1)

        label_pressure_coefficient = QLabel("Pressure Coefficient")
        lineedit_pressure_coefficient = QLineEdit()
        self.dynamic_widgets[label_pressure_coefficient] = lineedit_pressure_coefficient
        layout_heat_equation_tab.addWidget(label_pressure_coefficient, 7, 0)
        layout_heat_equation_tab.addWidget(lineedit_pressure_coefficient, 7, 1)

        self.heat_equation_tab.setLayout(layout_heat_equation_tab)

    def general_tabUI(self):

        title_font = QFont()
        title_font.setBold(True)
        title_font.setUnderline(True)

        layout_general = QGridLayout()

        label_properties_set = QLabel("Properties")
        label_properties_set.setFont(title_font)
        label_density = QLabel("Density")
        lineedit_density = QLineEdit()
        self.dynamic_widgets[label_density] = lineedit_density
        layout_general.addWidget(label_properties_set, 0, 0)
        layout_general.addWidget(label_density, 1, 0)
        layout_general.addWidget(lineedit_density, 1, 1)

        label_heat_capacity = QLabel("Heat Capacity")
        lineedit_heat_capacity = QLineEdit()
        self.dynamic_widgets[label_heat_capacity] = lineedit_heat_capacity
        layout_general.addWidget(label_heat_capacity, 2, 0)
        layout_general.addWidget(lineedit_heat_capacity, 2, 1)

        label_shr = QLabel("Specific Heat Ratio")
        lineedit_shr = QLineEdit()
        self.dynamic_widgets[label_shr] = lineedit_shr
        layout_general.addWidget(label_shr, 3, 0)
        layout_general.addWidget(lineedit_shr, 3, 1)

        label_ref_temp = QLabel("Reference Temperature")
        lineedit_ref_temp = QLineEdit()
        self.dynamic_widgets[label_ref_temp] = lineedit_ref_temp
        layout_general.addWidget(label_ref_temp, 4, 0)
        layout_general.addWidget(lineedit_ref_temp, 4, 1)

        label_ref_pressure = QLabel("Reference Pressure")
        lineedit_ref_pressure = QLineEdit()
        self.dynamic_widgets[label_ref_pressure] = lineedit_ref_pressure
        layout_general.addWidget(label_ref_pressure, 5, 0)
        layout_general.addWidget(lineedit_ref_pressure, 5, 1)

        label_hec = QLabel("Heat Expansion Coefficient")
        lineedit_hec = QLineEdit()
        self.dynamic_widgets[label_hec] = lineedit_hec
        layout_general.addWidget(label_hec, 6, 0)
        layout_general.addWidget(lineedit_hec, 6, 1)

        self.general_tab.setLayout(layout_general)
