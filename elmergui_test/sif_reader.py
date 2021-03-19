# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 07:51:36 2017

@author: rainer.jacob

Sif reader class
"""
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QComboBox, QCheckBox
import collections
import re
import os
from PyQt5 import QtCore

class SifReader():
    """SifReader"""

    def __init__(self, _elmer_gui):
        """Constructor

        Args:
        -----
        ewh: ElmerWindowHandler class
            current instance of the ElmerWindowHandler class
            containing all data
        """

        self._elmer_gui = _elmer_gui
        #self._solvIds = {}
        self._eq_data = {}
        self._sifIds = {}
        self.errormsg = ''

    def readSif(self, sifdata):
        """Read a given sif-file and create data and objects in the main class
        of the module

        Args:
        -----
        sifdata: str
            Either path to the sif-file or the siffile string itself
        """

        # read file
        try:
            if os.path.exists(sifdata):
                with open(sifdata) as f:
                    data = f.read()
            else:
                data = sifdata
        except Exception:
            self.errormsg = "Error reading sif file"  # + path
            raise

        # remove all comments
        comments = re.findall(r'\![ ]*.*\n', data)
        for line in comments:
            data = data.replace(line, '')
        # and extract the blocks
        blocks = data.split('End')
        blocks = [x.strip() for x in blocks]
        blocks.sort()

        # collect block types
        bodies_blocks = []
        boundaries_blocks = []
        equations_blocks = []
        general_blocks = []
        initial_blocks = []
        materials_blocks = []
        solvers_blocks = []
        bforces_blocks = []

        for block in blocks:
            if block.startswith('Body Force'):
                bforces_blocks.append(block)
            elif block.startswith('Body'):
                bodies_blocks.append(block)
            elif block.startswith('Boundary'):
                boundaries_blocks.append(block)
            elif block.startswith('Equation'):
                equations_blocks.append(block)
            elif block.startswith('Header'):
                general_blocks.append(block)
            elif block.startswith('Simulation'):
                general_blocks.append(block)
            elif block.startswith('Constants'):
                general_blocks.append(block)
            elif block.startswith('Material'):
                materials_blocks.append(block)
            elif block.startswith('Initial'):
                initial_blocks.append(block)
            elif block.startswith('Solver'):
                solvers_blocks.append(block)

        # apply general settings
        #for block in general_blocks:
        #    self._general(block)

        for block in enumerate(equations_blocks):
            self._equation(block)

        for block in enumerate(boundaries_blocks):
            self._bcondition(block)

        for block in enumerate(materials_blocks):
            self._materials(block)

        for block in enumerate(solvers_blocks):
            self._solvers(block)

    def _bcondition(self, block):
        """Change settings for a new boundary condition

        Args:
        -----
        block: str
            String containing the settings of the given boundary condition
        """

        #bc_nr = block[0] # not needed
        block = block[1]
        ui = self._elmer_gui.boundary_conditions
        data = block.split('\n')
        bc_id = int(data.pop(0).split(' ')[2])
        # set name
        bc_block_data = {}
        name = data.pop(0).split('=')[1].strip().replace('"', '')
        self.check_name_in_qlist(ui, name)
        bc_block_data["Name".lower()] = name

        #ui.list_of_elements.addItem(name.replace('"', ''))
        while data:
            if '=' in data[0]:
                parameter, setting = data.pop(0).split('=')
                bc_block_data[parameter.strip().lower()] = setting

        ui.data[name] = bc_block_data
        print("ui.data", ui.data)

    def _equation(self, block):
        '''Change settings of the equation
        Args:
        ----
        block: str
            String containing the settings of the given equation        
        '''

        eq_nr = block[0]  # not needed, delete it!
        block = block[1]
        ui = self._elmer_gui.equations
        data = block.split('\n')
        # get equation set
        eq_id = int(data.pop(0).split(' ')[1])
        # set name
        eq_block_data = {}
        name = data.pop(0).split('=')[1].strip().replace('"', '')
        self.check_name_in_qlist(ui, name)
        eq_block_data["name"] = name
        #ui.list_of_elements.addItem(name.replace('"', ''))
        print('eq test 1')
        self.check_name_in_qlist(ui, name)
        # set active solver
        print('eq test 2')
        while data:
            parameter, setting = data.pop(0).split('=')
            parameter = parameter.strip().lower()
            setting = setting.strip()
            #if 'Active Solvers'.lower() in parameter:
            #    setting = setting.split(' ')
            #    if setting and int(parameter[-2]) == len(setting):
            eq_block_data[parameter[:-3]] = setting
            #    else:
            #        print("Error! Numbers of active solvers do not match")
        print('eq test 3')
        #self._eq_data[eq_id] = eq_block_data  # self._eq_data not needed. Delete it!

        # ui.data = self._eq_data # Delete all previous equations
        ui.data[name] = eq_block_data # Instead of creating
                                       # completely new set of
                                       # equations, consisting only of
                                       # ones from imported sif file,
                                       # we append new equations to
                                       # existing ones and pass them
                                       # to Equations object to update
                                       # its GUI elements


    def _materials(self, block):
        """Change settings for a new material

        Args:
        -----
        block: str
            String containing the settings of the given material
        """
        mat_nr = block[0] # not needed
        block = block[1]
        ui = self._elmer_gui.materials
        data = block.split('\n')
        mat_id = int(data.pop(0).split(' ')[1])
        # set name
        mat_block_data = {}
        name = data.pop(0).split('=')[1].strip().replace('"', '')
        # Delete name from QListWidget if it exists and replace with new
        self.check_name_in_qlist(ui, name)

        mat_block_data["Name".lower()] = name

        #self._set_element_name(ui, name)
        while data:
            if '=' in data[0]:
                parameter, setting = data.pop(0).split('=')
                mat_block_data[parameter.strip().lower()] = setting

        ui.data[name] = mat_block_data

        print("testing materials", ui.data)
        # check if element in qlistwidget already exists. If it does,
        # remove it and replace it with new

    def _solvers(self, block):
        """Change settings of the solver.

        Args:
        -----
        block: str
            String containing the settings of the given solver
        """

        solv_nr = block[0]  # not needed, delete it!
        block = block[1]
        ui = self._elmer_gui.solvers
        data = block.split('\n')
        # get equation set
        solv_id = int(data.pop(0).split(' ')[1])
        # set name
        solv_block_data = {}
        #name = data.pop(0).split('=')[1].strip()
        #solv_block_data["Equation".lower()] = name.replace('"', '')
        #ui.list_of_elements.addItem(name.replace('"', ''))

        #ui.list_of_elements.addItem(str(solv_id).replace('"', ''))
        while data:
            parameter, setting = data.pop(0).split('=')
            parameter = parameter.strip()
            setting = setting.strip()
            solv_block_data[parameter.lower()] = setting
            #if 'Procedure' in parameter:
            #    pass
            #else:
            #    setting = setting.split(' ')
            #    if setting and int(parameter[-2]) == len(setting):
            #    else:

        #if 'Name' not in solv_block_data:
        name = str(solv_id)
        self.check_name_in_qlist(ui, name)
        solv_block_data['name'] = str(solv_id)
        #self._eq_data[solv_id] = solv_block_data  # self._solv_data not needed. Delete it!

            
        # ui.data = self._solv_data # Delete all previous solvers
        ui.data[str(solv_id)] = solv_block_data # Instead of creating
                                                # completely new set of
                                                # solvers, consisting only of
                                                # ones from imported sif file,
                                                # we append new equations to
                                                # existing ones and pass them
                                                # to Equations object to update
                                                # its GUI elements
        ##self.check_name_in_qlist(ui, name)
        #print("material name", name)
        #current_item = ui.list_of_elements.findItems(name,
        #                                             QtCore.Qt.MatchExactly)
        #print("len(current_item)", len(current_item))
        #if current_item:
        #    print("current item")
        #    current_item = current_item[0].setSelected(True)
        #    ui.on_delete(ui.list_of_elements, ui.data)
        #ui.list_of_elements.addItem(name)

    def _general(self, block):
        """Change settings in the general setup of the Elmer module

        Args:
        -----
        block: str
            String containing the settings of the general setup
        """

        # get the general setups window
        ui = self._elmer_gui.general_setup
        self._elmer_gui.general_setup.coordinate_mapping_lineedit.setText("tresarsdamsdv")

        # split rows
        data = block.split('\n')
        title = data.pop(0)
        if title == 'Header':
            if 'CHECK KEYWORDS' in data[0]:
                ui.checkWarning.setChecked(True)
                data.pop(0)
            ui.checkWarning.setChecked(False)
            a, b = data.pop(0).strip().split(' ')[2:]
            ui.meshDB_lineedit1.setText(a.replace('"', ''))
            ui.meshDB_lineedit2.setText(b.replace('"', ''))
            a = data.pop(0).strip().split(' ')[2:][0]
            ui.includePath_lineedit.setText(a.replace('"', ''))
            a = data.pop(0).strip().split(' ')[2:][0]
            ui.resultsDir_lineedit.setText(a.replace('"', ''))
            text = '\n'.join(data)
            #ui.headerFreeTextEdit.setText(text.replace('"', ''))

        if title == 'Simulation':
            while data:
                key, val = data.pop(0).split('=')
                key = key.strip()
                val = val.strip()
                if key.lower() == "Max Output Level".lower():
                    idx = ui.max_output_level_combobox.findText(val)
                    ui.max_output_level_combobox.setCurrentIndex(idx)
                if key.lower() == "Coordinate System".lower():
                    idx = ui.coordinate_system_combobox.findText(val)
                    ui.coordinate_system_combobox.setCurrentIndex(idx)
                if key.lower() == "Coordinate Mapping(3)".lower():
                    ui.coordinate_mapping_lineedit.setText(val)
                if key.lower() == "Simulation Type".lower():
                    idx = ui.simulation_type_combobox.findText(val)
                    ui.simulation_type_combobox.setCurrentIndex(idx)
                if key.lower() == "Steady State Max Iterations".lower():
                    ui.steady_state_max_iter_lineedit.setText(val)
                if key.lower() == "Output intervals".lower():
                    ui.output_intervals_lineedit.setText(val)
                if key.lower() == "Timestepping Method".lower():
                    ui.timestepping_method_combobox.findText(val)
                    ui.timestepping_method_combobox.setCurrentIndex(idx)
                if key.lower() == "BDF Order".lower():
                    idx = ui.bdf_order_combobox.findText(val)
                    ui.bdf_order_combobox.setCurrentIndex(idx)
                if key.lower() == "Timestep intervals".lower():
                    ui.timestep_intervals_lineedit.setText(val)
                if key.lower() == "Timestep sizes".lower():
                    ui.timestep_sizes_lineedit.setText(val)
                if key.lower() == "Use Mesh Names".lower():
                    ui.mesh_names_lineedit.setText(val)
                if key.lower() == "Solver input file".lower():
                    ui.solver_input_file_lineedit.setText(val)
                if key.lower() == "Post file".lower():
                    ui.post_file_lineedit.setText(val)

        if title == 'Constants':
            a = data.pop(0).split('=')[1].strip()
            idx = ui.gravity_lineedit.setText(a)
            a = data.pop(0).split('=')[1].strip()
            idx = ui.stefan_boltzmann_lineedit.setText(a)
            a = data.pop(0).split('=')[1].strip()
            idx = ui.vacuum_permittivity_lineedit.setText(a)
            a = data.pop(0).split('=')[1].strip()
            idx = ui.boltzmann_lineedit.setText(a)
            a = data.pop(0).split('=')[1].strip()
            idx = ui.unit_change_lineedit.setText(a)
            text = '\n'.join(data)
            #ui.constantsFreeTextEdit.setText(text)

    def check_name_in_qlist(self, ui, name):
        '''check if element in qlistwidget already exists. If it does, remove
         it and replace it with new

        '''
        
        current_item = ui.list_of_elements.findItems(name,
                                                     QtCore.Qt.MatchExactly)
        if current_item:
            print("check_name_in_qlist", name)
            current_item = current_item[0].setSelected(True)
            print("current data of current item", ui.data)
            ui.on_delete(ui.list_of_elements, ui.data)
        ui.list_of_elements.addItem(name)
