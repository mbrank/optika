from PyQt5.QtWidgets import (QInputDialog, QLineEdit, QDialog,
                             QApplication, QWidget, QLabel,
                             QHBoxLayout, QMainWindow, QCheckBox,
                             QPushButton, QVBoxLayout, QMessageBox,
                             QFileDialog, QStackedWidget, QGroupBox,
                             QGridLayout, QComboBox)
from PyQt5.QtGui import QFont
from base_sif import BaseSIF

class InitialConditions(BaseSIF):
    """Class that provides the General setup dialog and its functionality"""

    def __init__(self, data, parent=None):
        """Constructor.

        Args:
        -----
        path_forms: str
            String containing the path to the ui-files defining the look of the
            window.
        """
        super(InitialConditions, self).__init__(parent)
        #uic.loadUi(path_forms + "generalsetup.ui", self)
        #self.simulationFreeTextEdit.setText("Use Mesh Names = Logical True")
        #self.acceptButton.clicked.connect(self.applyChanges)
        self.data = data
        if not self.data:
            self.data = {}
            print('test equation')
        print('test equation')
        self.general_tab = QWidget()
        self.electrostatics_tab = QWidget()
        self.mesh_update_tab = QWidget()
        self.heat_equation_tab = QWidget()
        self.heat_equation_tabUI()
        self.helmholtz_equation_tab = QWidget()
        self.navier_stokes_tab = QWidget()
        self.tabs = {'Electrostatics': self.electrostatics_tab,
                     'Mesh Update': self.mesh_update_tab,
                     'Heat Equation': self.heat_equation_tab,
                     'Helmholtz Equation': self.helmholtz_equation_tab,
                     'Navier-Stokes': self.navier_stokes_tab}

        for tab in self.tabs:
            print('Tabs test equations')
            print(type(self.tabs[tab]), tab)
            self.solver_tabs.addTab(self.tabs[tab], tab)

        self.list_of_elements.itemClicked.connect(self.update_tabs)
        #self.setLayout(self.layout)
        #self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Initial Conditions')
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

        label_variables_set = QLabel("Variables")
        label_variables_set.setFont(title_font)
        label_temperature_ic = QLabel("Heat Conductivity")
        lineedit_temperature_ic = QLineEdit()
        self.dynamic_widgets[label_temperature_ic] = lineedit_temperature_ic
        layout_heat_equation_tab.addWidget(label_variables_set, 0, 0)
        layout_heat_equation_tab.addWidget(label_temperature_ic, 1, 0)
        layout_heat_equation_tab.addWidget(lineedit_temperature_ic, 1, 1)

        self.heat_equation_tab.setLayout(layout_heat_equation_tab)
