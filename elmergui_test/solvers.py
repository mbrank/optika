from PyQt5.QtWidgets import (QInputDialog, QLineEdit, QDialog,
                             QApplication, QWidget, QLabel,
                             QHBoxLayout, QMainWindow, QCheckBox,
                             QPushButton, QVBoxLayout, QMessageBox,
                             QFileDialog, QStackedWidget, QGroupBox,
                             QGridLayout, QComboBox, QRadioButton)
from PyQt5.QtGui import QFont
from base_sif import BaseSIF

class Solvers(BaseSIF):
    """Class that provides the General setup dialog and its functionality"""

    def __init__(self, data, parent=None):
        """Constructor.

        Args:
        -----
        path_forms: str
            String containing the path to the ui-files defining the look of the
            window.
        """
        super(Solvers, self).__init__(parent)
        #uic.loadUi(path_forms + "generalsetup.ui", self)
        #self.simulationFreeTextEdit.setText("Use Mesh Names = Logical True")
        #self.acceptButton.clicked.connect(self.applyChanges)
        self.data = data
        if not self.data:
            self.data = {}
            print('test equation')
        print('test equation')
        self.ss_options_tab =  QWidget()
        self.ss_options_tabUI()
        self.general_tab = QWidget()
        self.general_tabUI()
        self.steady_state_tab = QWidget()
        self.steady_state_tabUI()
        self.nlin_system_tab = QWidget()
        self.nlin_system_tabUI()
        self.lin_system_tab = QWidget()
        self.lin_system_tabUI()
        self.parallel_tab = QWidget()
        self.parallel_tabUI()
        self.adaptive_tab = QWidget()
        self.adaptive_tabUI()
        self.multigrid_tab = QWidget()
        self.multigrid_tabUI()
        self.tabs = {'Solver specific options': self.ss_options_tab,
                     'General': self.general_tab,
                     'Steady state': self.steady_state_tab,
                     'Nonlinear system': self.nlin_system_tab,
                     'Linear system': self.lin_system_tab,
                     'Parallel': self.parallel_tab,
                     'Adaptive': self.adaptive_tab,
                     'Multigrid': self.multigrid_tab}

        for tab in self.tabs:
            print('Tabs test equations')
            print(type(self.tabs[tab]), tab)
            self.solver_tabs.addTab(self.tabs[tab], tab)

        self.list_of_elements.hide()
        #self.setLayout(self.layout)
        #self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Solvers')
        self.element_settings.hide()  # setText("Show Material Library")

    def applyChanges(self):
        """Apply button hit"""
        # Hide window, but keep contents in memory
        self.hide()

    def ss_options_tabUI(self):
        title_font = QFont()
        title_font.setBold(True)
        title_font.setUnderline(True)

        layout_ss_options_tab = QGridLayout()

        label_solv_procedure = QLabel("Procedure")
        lineedit_solv_procedure = QLineEdit('"MeshSolve" "MeshSolver"')
        self.dynamic_widgets[label_solv_procedure] = lineedit_solv_procedure
        layout_ss_options_tab.addWidget(label_solv_procedure, 0, 0)
        layout_ss_options_tab.addWidget(lineedit_solv_procedure, 0, 1)
        
        label_solv_variable = QLabel("Variable")
        lineedit_solv_variable = QLineEdit("Mesh Update(cdim)")
        self.dynamic_widgets[label_solv_variable] = lineedit_solv_variable
        layout_ss_options_tab.addWidget(label_solv_variable, 1, 0)
        layout_ss_options_tab.addWidget(lineedit_solv_variable, 1, 1)

        label_solv_add_var = QLabel("Additional Variables")
        label_solv_add_var.setFont(title_font)
        layout_ss_options_tab.addWidget(label_solv_add_var, 2, 0)
        label_solv_exp_var = QLabel("Exported Variable 1")
        lineedit_solv_exp_var = QLineEdit()
        self.dynamic_widgets[label_solv_exp_var] = lineedit_solv_exp_var
        layout_ss_options_tab.addWidget(label_solv_exp_var, 3, 0)
        layout_ss_options_tab.addWidget(lineedit_solv_exp_var, 3, 1)

        label_solv_misc_opt = QLabel("Miscellaneous options")
        label_solv_misc_opt.setFont(title_font)
        layout_ss_options_tab.addWidget(label_solv_misc_opt, 4, 0)
        label_solv_calc_load = QLabel("Calculate Loads")
        checkbox_solv_calc_load = QCheckBox()
        self.dynamic_widgets[label_solv_calc_load] = checkbox_solv_calc_load
        layout_ss_options_tab.addWidget(label_solv_calc_load, 5, 0)
        layout_ss_options_tab.addWidget(checkbox_solv_calc_load, 5, 1)

        self.ss_options_tab.setLayout(layout_ss_options_tab)

    def steady_state_tabUI(self):
        title_font = QFont()
        title_font.setBold(True)
        title_font.setUnderline(True)

        layout_ss = QVBoxLayout()
        # Execute solver
        solv_ss_gen_box = QGroupBox('General')
        solv_ss_gen_layout = QGridLayout()
        solv_ss_gen_box.setLayout(solv_ss_gen_layout)

        label_solv_cnv_tol = QLabel("Convergence tolerance")
        lineedit_solv_cnv_tol = QLineEdit('1.0e-5')
        self.dynamic_widgets[label_solv_cnv_tol] = lineedit_solv_cnv_tol
        solv_ss_gen_layout.addWidget(label_solv_cnv_tol, 0, 0)
        solv_ss_gen_layout.addWidget(lineedit_solv_cnv_tol, 0, 1)
        layout_ss.addWidget(solv_ss_gen_box)

        label_solv_ss_meas = QLabel("Measure")
        combobox_solv_ss_meas = QComboBox()
        combobox_solv_ss_meas.addItem("Norm")
        combobox_solv_ss_meas.addItem("Solution")
        combobox_solv_ss_meas.addItem("Residual")
        combobox_solv_ss_meas.itemText(0)
        solv_ss_gen_layout.addWidget(label_solv_ss_meas, 1, 0)
        solv_ss_gen_layout.addWidget(combobox_solv_ss_meas, 1, 1)
        self.steady_state_tab.setLayout(layout_ss)
        #rd_button_solv_exec = QRadioButton("Execute solver")
        #exec_solver_layout.addWidget(rd_button_solv_exec)

        
        #ss_solv_always = QRadioButton("Always")
        #rd_button_solv_always.setChecked(True)
        #exec_solver_layout.addWidget(rd_button_solv_always)

    def nlin_system_tabUI(self):
        title_font = QFont()
        title_font.setBold(True)
        title_font.setUnderline(True)

        layout_nls = QVBoxLayout()

        # General
        solv_nls_gen_box = QGroupBox('General')
        solv_nls_gen_layout = QGridLayout()
        solv_nls_gen_box.setLayout(solv_nls_gen_layout)

        label_solv_cnv_tol = QLabel("Convergence tolerance")
        lineedit_solv_cnv_tol = QLineEdit('1.0e-7')
        self.dynamic_widgets[label_solv_cnv_tol] = lineedit_solv_cnv_tol
        solv_nls_gen_layout.addWidget(label_solv_cnv_tol, 0, 0)
        solv_nls_gen_layout.addWidget(lineedit_solv_cnv_tol, 0, 1)

        label_solv_cnv_max_iter = QLabel("Max. iterations")
        lineedit_solv_cnv_max_iter = QLineEdit('20')
        self.dynamic_widgets[label_solv_cnv_max_iter] = lineedit_solv_cnv_max_iter
        solv_nls_gen_layout.addWidget(label_solv_cnv_max_iter, 1, 0)
        solv_nls_gen_layout.addWidget(lineedit_solv_cnv_max_iter, 1, 1)

        label_solv_cnv_rel_fac = QLabel("Relaxation factor")
        lineedit_solv_cnv_rel_fac = QLineEdit('1')
        self.dynamic_widgets[label_solv_cnv_rel_fac] = lineedit_solv_cnv_rel_fac
        solv_nls_gen_layout.addWidget(label_solv_cnv_rel_fac, 2, 0)
        solv_nls_gen_layout.addWidget(lineedit_solv_cnv_rel_fac, 2, 1)

        label_solv_nls_meas = QLabel("Measure")
        combobox_solv_nls_meas = QComboBox()
        combobox_solv_nls_meas.addItem("Norm")
        combobox_solv_nls_meas.addItem("Solution")
        combobox_solv_nls_meas.addItem("Residual")
        combobox_solv_nls_meas.itemText(0)
        self.dynamic_widgets[label_solv_nls_meas] = combobox_solv_nls_meas
        solv_nls_gen_layout.addWidget(label_solv_nls_meas, 3, 0)
        solv_nls_gen_layout.addWidget(combobox_solv_nls_meas, 3, 1)

        layout_nls.addWidget(solv_nls_gen_box)
        self.nlin_system_tab.setLayout(layout_nls)

        # Execute solver
        solv_nls_gen_box = QGroupBox('Newton')
        solv_nls_gen_layout = QGridLayout()
        solv_nls_gen_box.setLayout(solv_nls_gen_layout)

        label_solv_nls_n_ai = QLabel("After iterations")
        lineedit_solv_nls_n_ai = QLineEdit('3')
        self.dynamic_widgets[label_solv_nls_n_ai] = lineedit_solv_nls_n_ai
        solv_nls_gen_layout.addWidget(label_solv_cnv_tol, 0, 0)
        solv_nls_gen_layout.addWidget(lineedit_solv_cnv_tol, 0, 1)

        label_solv_cnv_max_iter = QLabel("After tolerance")
        lineedit_solv_cnv_max_iter = QLineEdit('1.0e-3')
        self.dynamic_widgets[label_solv_cnv_max_iter] = lineedit_solv_cnv_max_iter
        solv_nls_gen_layout.addWidget(label_solv_cnv_max_iter, 1, 0)
        solv_nls_gen_layout.addWidget(lineedit_solv_cnv_max_iter, 1, 1)

        layout_nls.addWidget(solv_nls_gen_box)
        self.nlin_system_tab.setLayout(layout_nls)

    def lin_system_tabUI(self):
        layout_ls = QVBoxLayout()

        # Method
        solv_ls_method_box = QGroupBox('Method')
        solv_ls_method_layout = QGridLayout()
        solv_ls_method_box.setLayout(solv_ls_method_layout)

        rd_button_solv_ls_direct = QRadioButton("Direct")
        combobox_solv_ls_direct = QComboBox()
        combobox_solv_ls_direct.addItems(["Banded", "Umfpack", "MUMPS"])
        solv_ls_method_layout.addWidget(rd_button_solv_ls_direct, 0, 0)
        solv_ls_method_layout.addWidget(combobox_solv_ls_direct, 0, 1)

        rd_button_solv_ls_iter = QRadioButton("Iterative")
        rd_button_solv_ls_iter.setChecked(True)
        combobox_solv_ls_iter = QComboBox()
        combobox_solv_ls_iter.addItems(["BiCGStab", "BiCGStabl", "TFQMR",
                                        "GCR", "GCS", "CG", "GMRES"])
        solv_ls_method_layout.addWidget(rd_button_solv_ls_iter, 1, 0)
        solv_ls_method_layout.addWidget(combobox_solv_ls_iter, 1, 1)

        rd_button_solv_mltgrd = QRadioButton("Multigrid")
        rd_button_solv_ls_iter.setChecked(True)
        combobox_solv_ls_mltgrd = QComboBox()
        combobox_solv_ls_mltgrd.addItems(["Jacobi", "CG", "BiCGStab"])
        solv_ls_method_layout.addWidget(rd_button_solv_mltgrd, 2, 0)
        solv_ls_method_layout.addWidget(combobox_solv_ls_mltgrd, 2, 1)
        layout_ls.addWidget(solv_ls_method_box)

        # Control
        solv_ls_cntr_box = QGroupBox('Control')
        solv_ls_cntr_layout = QGridLayout()
        solv_ls_cntr_box.setLayout(solv_ls_cntr_layout)

        label_solv_ls_cntr_max_iter = QLabel("Max. iterations")
        lineedit_solv_ls_cntr_max_iter = QLineEdit('500')
        self.dynamic_widgets[label_solv_ls_cntr_max_iter] = lineedit_solv_ls_cntr_max_iter
        solv_ls_cntr_layout.addWidget(label_solv_ls_cntr_max_iter, 0, 0)
        solv_ls_cntr_layout.addWidget(lineedit_solv_ls_cntr_max_iter, 0, 1)

        label_solv_ls_cntr_cnv_tol = QLabel("Convergence tol.")
        lineedit_solv_ls_cntr_cnv_tol = QLineEdit('1.0e-10')
        self.dynamic_widgets[label_solv_ls_cntr_cnv_tol] = lineedit_solv_ls_cntr_cnv_tol
        solv_ls_cntr_layout.addWidget(label_solv_ls_cntr_cnv_tol, 1, 0)
        solv_ls_cntr_layout.addWidget(lineedit_solv_ls_cntr_cnv_tol, 1, 1)

        label_solv_ls_prcon = QLabel("Preconditioning")
        combobox_solv_ls_prcon = QComboBox()
        combobox_solv_ls_prcon.addItems(["Diagonal", "Multigrid",
                                         "ILU0","ILU1","ILU2","ILU3",
                                         "ILU4","ILU5","ILU6","ILU7",
                                         "ILU8", "ILUT9", "vanka"])
        combobox_solv_ls_prcon.itemText(0)
        self.dynamic_widgets[label_solv_ls_prcon] = combobox_solv_ls_prcon
        solv_ls_cntr_layout.addWidget(label_solv_ls_prcon, 2, 0)
        solv_ls_cntr_layout.addWidget(combobox_solv_ls_prcon, 2, 1)

        label_solv_ls_ilt_tol = QLabel("ILUT tolerance")
        lineedit_solv_ls_ilt_tol = QLineEdit('1.0e-3')
        self.dynamic_widgets[label_solv_ls_ilt_tol] = lineedit_solv_ls_ilt_tol
        solv_ls_cntr_layout.addWidget(label_solv_ls_ilt_tol, 3, 0)
        solv_ls_cntr_layout.addWidget(lineedit_solv_ls_ilt_tol, 3, 1)

        label_solv_ls_res_out = QLabel("Residual output")
        lineedit_solv_ls_res_out = QLineEdit('1')
        self.dynamic_widgets[label_solv_ls_res_out] = lineedit_solv_ls_res_out
        solv_ls_cntr_layout.addWidget(label_solv_ls_res_out, 4, 0)
        solv_ls_cntr_layout.addWidget(lineedit_solv_ls_res_out, 4, 1)

        label_solv_ls_prcrec = QLabel("Prec. recomupute")
        lineedit_solv_ls_prcrec = QLineEdit('1')
        self.dynamic_widgets[label_solv_ls_prcrec] = lineedit_solv_ls_prcrec
        solv_ls_cntr_layout.addWidget(label_solv_ls_prcrec, 5, 0)
        solv_ls_cntr_layout.addWidget(lineedit_solv_ls_prcrec, 5, 1)

        label_solv_ls_bcgord = QLabel("BiCGStabl order")
        lineedit_solv_ls_bcgord = QLineEdit('2')
        self.dynamic_widgets[label_solv_ls_bcgord] = lineedit_solv_ls_bcgord
        solv_ls_cntr_layout.addWidget(label_solv_ls_bcgord, 6, 0)
        solv_ls_cntr_layout.addWidget(lineedit_solv_ls_bcgord, 6, 1)

        checkbox_solv_ls_abrt = QCheckBox("Abort if solution did not converge")
        layout_ls.addWidget(solv_ls_cntr_box)
        layout_ls.addWidget(checkbox_solv_ls_abrt)
        self.lin_system_tab.setLayout(layout_ls)
        # old
        #label_solv_cnv_max_iter = QLabel("Max. iterations")
        #lineedit_solv_cnv_max_iter = QLineEdit('20')
        #self.dynamic_widgets[label_solv_cnv_max_iter] = lineedit_solv_cnv_max_iter
        #solv_ls_cntr_layout.addWidget(label_solv_cnv_max_iter, 1, 0)
        #solv_ls_cntr_layout.addWidget(lineedit_solv_cnv_max_iter, 1, 1)
        #label_solv_cnv_rel_fac = QLabel("Relaxation factor")
        #lineedit_solv_cnv_rel_fac = QLineEdit('1')
        #self.dynamic_widgets[label_solv_cnv_rel_fac] = lineedit_solv_cnv_rel_fac
        #solv_ls_cntr_layout.addWidget(label_solv_cnv_rel_fac, 2, 0)
        #solv_ls_cntr_layout.addWidget(lineedit_solv_cnv_rel_fac, 2, 1)
        #label_solv_ls_meas = QLabel("Measure")
        #combobox_solv_ls_meas = QComboBox()
        #combobox_solv_ls_meas.addItem("Norm")
        #combobox_solv_ls_meas.addItem("Solution")
        #combobox_solv_ls_meas.addItem("Residual")
        #combobox_solv_ls_meas.itemText(0)
        #self.dynamic_widgets[label_solv_ls_meas] = combobox_solv_ls_meas
        #solv_ls_cntr_layout.addWidget(label_solv_ls_meas, 3, 0)
        #solv_ls_cntr_layout.addWidget(combobox_solv_ls_meas, 3, 1)


        #rd_button_solv_before_sim = QRadioButton("Before simulation")
        #exec_solver_layout.addWidget(rd_button_solv_before_sim)
        #rd_button_solv_after_sim = QRadioButton("After simulation")
        #exec_solver_layout.addWidget(rd_button_solv_after_sim)
        #label_solv_cnv_tol = QLabel("Convergence tolerance")
        #lineedit_solv_cnv_tol = QLineEdit('1.0e-7')
        #self.dynamic_widgets[label_solv_cnv_tol] = lineedit_solv_cnv_tol
        #solv_ls_gen_layout.addWidget(label_solv_cnv_tol, 0, 0)
        #solv_ls_gen_layout.addWidget(lineedit_solv_cnv_tol, 0, 1)
        #label_solv_cnv_max_iter = QLabel("Max. iterations")
        #lineedit_solv_cnv_max_iter = QLineEdit('20')
        #self.dynamic_widgets[label_solv_cnv_max_iter] = lineedit_solv_cnv_max_iter
        #solv_ls_gen_layout.addWidget(label_solv_cnv_max_iter, 1, 0)
        #solv_ls_gen_layout.addWidget(lineedit_solv_cnv_max_iter, 1, 1)
        #label_solv_cnv_rel_fac = QLabel("Relaxation factor")
        #lineedit_solv_cnv_rel_fac = QLineEdit('1')
        #self.dynamic_widgets[label_solv_cnv_rel_fac] = lineedit_solv_cnv_rel_fac
        #solv_ls_gen_layout.addWidget(label_solv_cnv_rel_fac, 2, 0)
        #solv_ls_gen_layout.addWidget(lineedit_solv_cnv_rel_fac, 2, 1)
        #label_solv_ls_meas = QLabel("Measure")
        #combobox_solv_ls_meas = QComboBox()
        #combobox_solv_ls_meas.addItem("Norm")
        #combobox_solv_ls_meas.addItem("Solution")
        #combobox_solv_ls_meas.addItem("Residual")
        #combobox_solv_ls_meas.itemText(0)
        #self.dynamic_widgets[label_solv_ls_meas] = combobox_solv_ls_meas
        #solv_ls_gen_layout.addWidget(label_solv_ls_meas, 3, 0)
        #solv_ls_gen_layout.addWidget(combobox_solv_ls_meas, 3, 1)
        #layout_ls.addWidget(solv_ls_gen_box)
        #self.lin_system_tab.setLayout(layout_ls)
        # Execute solver
        #solv_ls_gen_box = QGroupBox('Newton')
        #solv_ls_gen_layout = QGridLayout()
        #solv_ls_gen_box.setLayout(solv_ls_gen_layout)
        #label_solv_ls_n_ai = QLabel("After iterations")
        #lineedit_solv_ls_n_ai = QLineEdit('3')
        #self.dynamic_widgets[label_solv_ls_n_ai] = lineedit_solv_ls_n_ai
        #solv_ls_gen_layout.addWidget(label_solv_cnv_tol, 0, 0)
        #solv_ls_gen_layout.addWidget(lineedit_solv_cnv_tol, 0, 1)
        #label_solv_cnv_max_iter = QLabel("After tolerance")
        #lineedit_solv_cnv_max_iter = QLineEdit('1.0e-3')
        #self.dynamic_widgets[label_solv_cnv_max_iter] = lineedit_solv_cnv_max_iter
        #solv_ls_gen_layout.addWidget(label_solv_cnv_max_iter, 1, 0)
        #solv_ls_gen_layout.addWidget(lineedit_solv_cnv_max_iter, 1, 1)
        

    def parallel_tabUI(self):
        pass
    def adaptive_tabUI(self):
        pass
    def multigrid_tabUI(self):
        pass

                     
    def heat_equation_tabUI(self):

        title_font = QFont()
        title_font.setBold(True)
        title_font.setUnderline(True)

        layout_heat_equation_tab = QGridLayout()

        label_add_var_set = QLabel("Properties")
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

        layout_general = QVBoxLayout()
        # Execute solver
        exec_solver_box = QGroupBox('Execute solver')
        exec_solver_layout = QGridLayout()
        exec_solver_box.setLayout(exec_solver_layout)
        layout_general.addWidget(exec_solver_box)

        #rd_button_solv_exec = QRadioButton("Execute solver")
        #exec_solver_layout.addWidget(rd_button_solv_exec)
        rd_button_solv_always = QRadioButton("Always")
        rd_button_solv_always.setChecked(True)
        exec_solver_layout.addWidget(rd_button_solv_always)
        rd_button_solv_before_sim = QRadioButton("Before simulation")
        exec_solver_layout.addWidget(rd_button_solv_before_sim)
        rd_button_solv_after_sim = QRadioButton("After simulation")
        exec_solver_layout.addWidget(rd_button_solv_after_sim)
        rd_button_solv_bef_timestep = QRadioButton("Before timestep")
        exec_solver_layout.addWidget(rd_button_solv_bef_timestep)
        rd_button_solv_after_timestep = QRadioButton("After timestep")
        exec_solver_layout.addWidget(rd_button_solv_after_timestep)
        rd_button_solv_after_all = QRadioButton("After all")
        exec_solver_layout.addWidget(rd_button_solv_after_all)
        rd_button_solv_never = QRadioButton("Never")
        exec_solver_layout.addWidget(rd_button_solv_never)

        # Numerical techniques
        num_tech_solver_box = QGroupBox('Header')
        num_tech_solver_layout = QGridLayout()
        num_tech_solver_box.setLayout(num_tech_solver_layout)
        layout_general.addWidget(num_tech_solver_box)

        checkbox_solv_stab = QCheckBox("Stabilize")
        checkbox_solv_stab.setChecked(True)
        num_tech_solver_layout.addWidget(checkbox_solv_stab)
        checkbox_solv_bub = QCheckBox("Bubbles")
        num_tech_solver_layout.addWidget(checkbox_solv_bub)
        checkbox_solv_lmp_mass = QCheckBox("Lumped mass")
        num_tech_solver_layout.addWidget(checkbox_solv_lmp_mass)
        checkbox_solv_opt_bndw = QCheckBox("Optimized Bandwidth")
        checkbox_solv_opt_bndw.setChecked(True)
        num_tech_solver_layout.addWidget(checkbox_solv_opt_bndw)

        '''
        layout_general.addWidget(rd_button_solv_exec, 0, 0)
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
        '''
        self.general_tab.setLayout(layout_general)
