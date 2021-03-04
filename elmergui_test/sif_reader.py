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


class SifReader():
    """SifReader"""

    def __init__(self, _ewh):
        """Constructor

        Args:
        -----
        ewh: ElmerWindowHandler class
            current instance of the ElmerWindowHandler class
            containing all data
        """

        self._ewh = _ewh
        self._solvIds = {}
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
        bodies = []
        boundaries = []
        equations = []
        general = []
        initial = []
        materials = []
        solvers = []
        bforces = []

        for block in blocks:
            if block.startswith('Body Force'):
                bforces.append(block)
            elif block.startswith('Body'):
                bodies.append(block)
            elif block.startswith('Boundary'):
                boundaries.append(block)
            elif block.startswith('Equation'):
                equations.append(block)
            elif block.startswith('Header'):
                general.append(block)
            elif block.startswith('Simulation'):
                general.append(block)
            elif block.startswith('Constants'):
                general.append(block)
            elif block.startswith('Material'):
                materials.append(block)
            elif block.startswith('Initial'):
                initial.append(block)
            elif block.startswith('Solver'):
                solvers.append(block)
        print(solvers)

        # apply general settings
        for block in general:
            print("test 1")
            self._general(block)
            print("test 2")

        # make a new equations window and change settings of first equation
        # also creates the default solvers
        self._ewh.showAddEquation(visible=False)
        # get all solvers by name and index
        for idx, element in enumerate(self._ewh.solverParameterEditor):
            self._solvIds.update({element.solverName: idx})

        '''
        # apply settings
        for block in solvers:
            self._solvers(block)

        for block in equations:
            self._equation(block)

        for block in materials:
            self._materials(block)

        for block in bforces:
            self._bforces(block)

        for block in initial:
            self._icondition(block)

        for block in bodies:
            self._bproperties(block)

        bc = []

        # boundary conditions input has to be split in bcs first
        # extract bc settings and count the number of different settings
        for block in boundaries:
            lines = block.split('\n')[1:]
            line = '\n'.join(lines)
            bc.append(line)
        bc = dict(collections.Counter(bc))
        # create bcs
        count = 0
        for key, value in bc.items():
            self._bcondition(key)
            bc.update({key: count})
            count += 1
        # connect boundaries
        try:
            for block in boundaries:
                lines = block.split('\n')
                target = lines[1].split('=')[1].strip()
                editor = self._ewh.showBoundaryPropertyDefinition(
                    target, visible=False)
                editor.boundaryConditionCombo.setCurrentIndex(
                    editor.boundaryConditionCombo.findText(target[1:-1]))
                self._ewh.elementProperties.update({target[1:-1]: editor})
        except Exception:
            self.errormsg = "Possible mismatch in number of boundaries in" \
                " sif-file and number of boundary faces in study"
            raise
        '''

    def _changeSettings(self, parameter, value):
        """Change settings of hashed parameter in element.

        Args:
        -----
        parameter: obj
            obj of the parameter (e. g. the corresponding widget)
        value: str
            new value of the parameter
        """

        if isinstance(parameter, QLineEdit):
            parameter.setText(value.replace('"', ''))
        elif isinstance(parameter, QTextEdit):
            sifValue = parameter.toPlainText()
            if sifValue == '':
                sifValue = value.replace('"', '')
            else:
                sifValue = sifValue + '\n' + value.replace('"', '')
            parameter.setText(sifValue)
        elif isinstance(parameter, QComboBox):
            idx = parameter.findText(value)
            parameter.setCurrentIndex(idx)
        elif isinstance(parameter, QCheckBox):
            parameter.setChecked(value == 'True')

    def _bproperties(self, block):
        """Change settings for a new body properties

        Args:
        -----
        block: str
            String containing the settings of the given body property
        """

        data = block.split('\n')
        target = data[1].split('=')[1].strip()

        # create new window
        editor = self._ewh.showBodyPropertyDefinition(target, visible=False)
        for segment in data[1:]:
            name, idx = segment.split('=')
            if 'Equation' in name:
                editor.equationCombo.setCurrentIndex(int(idx.strip()))
            elif 'Material' in name:
                editor.materialCombo.setCurrentIndex(int(idx.strip()))
            elif 'orce' in name:
                editor.bodyForceCombo.setCurrentIndex(int(idx.strip()))
            elif 'Initial' in name:
                editor.initialConditionCombo.setCurrentIndex(int(idx.strip()))
        self._ewh.elementProperties.update({target[1:-1]: editor})

    def _bcondition(self, block):
        """Change settings for a new boundary condition

        Args:
        -----
        block: str
            String containing the settings of the given boundary condition
        """

        data = block.split('\n')
        # create boundary condition set
        count = len(self._ewh.boundaryConditionEditor)

        name = data.pop(0).split('=')[1].strip()
        if count == 0:
            self._ewh.showAddBoundaryCondition(visible=False)
            bc = self._ewh.boundaryConditionEditor[-1]
        else:
            flag = 1
            for i in self._ewh.boundaryConditionEditor:
                # If bc with same name exists, replace it, otherwise
                # create new
                if i.nameEdit.text() == name.replace('"', ''):
                    bc = self._ewh.boundaryConditionEditor[i.ID]
                    flag = 0
            if flag:
                self._ewh.boundaryConditionEditorFinishedSlot(3, count)
                bc = self._ewh.boundaryConditionEditor[-1]

        bc.nameEdit.setText(name.replace('"', ''))

        # set boundary condition data
        while data:
            if '=' not in data[0]:
                data.pop(0)
            parameter, setting = data.pop(0).split('=')
            parameter = parameter.strip()
            setting = setting.strip()
            freeText = True
            for key, value in bc.qhash.items():
                sifName = str(value.elem.firstChildElement(
                    'SifName').text()).strip()
                if sifName == '':
                    sifName = str(value.elem.firstChildElement(
                        'Name').text()).strip()
                if sifName == parameter:
                    self._changeSettings(value.widget, setting)
                    freeText = False
            if freeText:
                value = bc.qhash['/General/BoundaryCondition/Free text/{}'.format(
                    count)]
                self._changeSettings(value.widget, ' = '.join(
                    ['  {}'.format(parameter), setting]))
        bc.applyButton.click()

    def _icondition(self, block):
        """Change settings for a new initial condition

        Args:
        -----
        block: str
            String containing the settings of the given initial condition
        """

        data = block.split('\n')

        # get initial condition set
        sifID = int(data.pop(0).split(' ')[2])
        if len(self._ewh.initialConditionEditor) < sifID:
            if sifID == 1:
                self._ewh.showAddInitialCondition(visible=False)
            else:
                self._ewh.initialConditionEditorFinishedSlot(3, sifID - 1)
        ic = self._ewh.initialConditionEditor[sifID - 1]

        # set name
        name = data.pop(0).split('=')[1].strip()
        ic.nameEdit.setText(name.replace('"', ''))

        # set initial condition data
        while data:
            parameter, setting = data.pop(0).split('=')
            parameter = parameter.strip()
            setting = setting.strip()
            freeText = True
            for key, value in ic.qhash.items():
                sifName = str(value.elem.firstChildElement(
                    'SifName').text()).strip()
                if sifName == '':
                    sifName = str(value.elem.firstChildElement(
                        'Name').text()).strip()
                if sifName == parameter:
                    self._changeSettings(value.widget, setting)
                    freeText = False
            if freeText:
                for key in ic.qhash.keys():
                    if 'Free text' in key and 'input' not in key:
                        value = ic.qhash[key]
                        self._changeSettings(value.widget, ' = '.join(
                            ['  {}'.format(parameter), setting]))
                        break
        ic.applyButton.click()

    def _bforces(self, block):
        """Change settings for a new body force

        Args:
        -----
        block: str
            String containing the settings of the given body force
        """

        data = block.split('\n')

        # get body force set
        sifID = int(data.pop(0).split(' ')[2])
        if len(self._ewh.bodyForceEditor) < sifID:
            if sifID == 1:
                self._ewh.showAddBodyForce(visible=False)
            else:
                self._ewh.bodyForceEditorFinishedSlot(3, sifID - 1)
        bf = self._ewh.bodyForceEditor[sifID - 1]

        # set name
        name = data.pop(0).split('=')[1].strip()
        bf.nameEdit.setText(name.replace('"', ''))

        # set body force data
        while data:
            parameter, setting = data.pop(0).split('=')
            parameter = parameter.strip()
            setting = setting.strip()
            freeText = True
            for key, value in bf.qhash.items():
                sifName = str(value.elem.firstChildElement(
                    'SifName').text()).strip()
                if sifName == '':
                    sifName = str(value.elem.firstChildElement(
                        'Name').text()).strip()
                if sifName == parameter:
                    self._changeSettings(value.widget, setting)
                    freeText = False
            if freeText:
                for key in bf.qhash.keys():
                    if 'Free text' in key and 'input' not in key:
                        value = bf.qhash[key]
                        self._changeSettings(value.widget, ' = '.join(
                            ['  {}'.format(parameter), setting]))
                        break
        bf.applyButton.click()

    def _materials(self, block):
        """Change settings for a new material

        Args:
        -----
        block: str
            String containing the settings of the given material
        """

        data = block.split('\n')

        # get equation set
        sifID = int(data.pop(0).split(' ')[1])
        if len(self._ewh.materialEditor) < sifID:
            if sifID == 1:
                self._ewh.showAddMaterial(visible=False)
            else:
                self._ewh.matEditorFinishedSlot(3, sifID - 1)
        mat = self._ewh.materialEditor[sifID - 1]

        # set name
        name = data.pop(0).split('=')[1].strip()
        mat.nameEdit.setText(name.replace('"', ''))

        # set material data
        while data:
            parameter, setting = data.pop(0).split('=')
            parameter = parameter.strip()
            setting = setting.strip()
            freeText = True
            for key, value in mat.qhash.items():
                sifName = str(value.elem.firstChildElement(
                    'SifName').text()).strip()
                if sifName == '':
                    sifName = str(value.elem.firstChildElement(
                        'Name').text()).strip()
                if sifName == parameter:
                    self._changeSettings(value.widget, setting)
                    freeText = False
            if freeText:
                for key in mat.qhash.keys():
                    if 'Free text' in key and 'input' not in key:
                        value = mat.qhash[key]
                        self._changeSettings(value.widget, ' = '.join(
                            ['  {}'.format(parameter), setting]))
                        break
        mat.applyButton.click()

    def _equation(self, block):
        """Change settings of the equation

        Args:
        ----
        block: str
            String containing the settings of the given equation
        """

        data = block.split('\n')

        # get equation set
        sifID = int(data.pop(0).split(' ')[1])
        if len(self._ewh.equationEditor) < sifID:
            self._ewh.pdeEditorFinishedSlot(3, sifID - 1)
        eq = self._ewh.equationEditor[sifID - 1]

        # set name
        name = data.pop(0).split('=')[1].strip()
        eq.nameEdit.setText(name.replace('"', ''))

        # set active solver
        while data:
            parameter, setting = data.pop(0).split('=')
            parameter = parameter.strip()
            setting = setting.strip()
            if 'Active Solvers' in parameter:
                setting = setting.split(' ')
                for key in setting:
                    #########################################
                    if key == '':
                        pass
                    else:
                        ####################################
                        name = self._sifIds[key]
                        key = '/' + name + '/Equation/Active/' + str(eq.ID)
                        eq.qhash[key].widget.setChecked(True)
                break
            freeText = True
            for key, value in eq.qhash.items():
                sifName = str(value.elem.firstChildElement(
                    'SifName').text()).strip()
                if sifName == '':
                    sifName = str(value.elem.firstChildElement(
                        'Name').text()).strip()
                if sifName == parameter:
                    self._changeSettings(value.widget, setting)
                    freeText = False
            if freeText:
                for key in eq.qhash.keys():
                    if 'Free text' in key and 'input' not in key:
                        value = eq.qhash[key]
                        self._changeSettings(value.widget, ' = '.join(
                            ['  {}'.format(parameter), setting]))
                        break
        eq.applyButton.click()

    def _solvers(self, block):
        """Change settings of the solver.

        Args:
        -----
        block: str
            String containing the settings of the given solver
        """

        data = block.split('\n')

        # mapping of solver name and ID as in sif-file
        sifID = data.pop(0).split(' ')[1]
        name = data.pop(0).split('=')[1].strip()
        self._sifIds.update({sifID: name})

        # get the solver from the solver collection
        idx = self._solvIds[name]
        element = self._ewh.solverParameterEditor[idx]

        procedure = data.pop(0).split('=')[1].strip()
        variable = data.pop(0).split('=')[1].strip()

        # general options
        while data:
            key, value = data.pop(0).split('=')
            key = key.strip()
            value = value.strip()
            if 'Exec' in key:
                if value == 'Always':
                    element.execAlways.setChecked(True)
                if value == 'Before Simulation':
                    element.execBeforeSimulation.setChecked(True)
                if value == 'After Simulation':
                    element.execAfterSimulation.setChecked(True)
                if value == 'Before Timestep':
                    element.execBeforeTimestep.setChecked(True)
                if value == 'After Timestep':
                    element.execAfterTimestep.setChecked(True)
                if value == 'After All':
                    element.execAfterAll.setChecked(True)
                if value == 'Never':
                    element.execNever.setChecked(True)
                break
            key = '/{}/Solver/{}'.format(name, key)
            parameter = element.generalOptions.qhash[key]
            self._changeSettings(parameter.widget, value)

        if len(data) == 0:
            return

        keys = {'Stabilize': element.stabilizeCheck,
                'Bubbles': element.bubblesCheck,
                'Lumped Mass Matrix': element.lumpedMassCheck,
                'Optimize Bandwidth': element.optimizeBandwidthCheck,
                'Steady State Convergence Tolerance':
                element.steadyStateConvergenceToleranceEdit,
                'Steady State Convergence Measure':
                element.steadyStateConvergenceMeasureCombo,
                'Nonlinear System Convergence Tolerance':
                element.nonlinSystemConvergenceToleranceEdit,
                'Nonlinear System Max Iterations':
                element.nonlinSystemMaxIterationEdit,
                'Nonlinear System Relaxation Factor':
                element.nonlinSystemRelaxationFactorEdit,
                'Nonlinear System Convergence Measure':
                element.nonlinSystemConvergenceMeasureCombo,
                'Nonlinear System Newton After Iterations':
                element.nonlinSystemNewtonAfterIterEdit,
                'Nonlinear System Newton After Tolerance':
                element.nonlinSystemNewtonAfterTolEdit,
                'Linear System Direct Method':
                element.linearSystemDirectMethod,
                'Linear System Iterative Method':
                element.linearSystemIterativeMethod,
                'Linear System Max Iterations':
                element.linearSystemMaxIterationsEdit,
                'Linear System Convergence Tolerance':
                element.linearSystemConvergenceToleranceEdit,
                'BiCGstabl polynomial degree':
                element.linearSystemBiCGstablPolDeg,
                'Linear System Preconditioning':
                element.linearSystemPreconditioning,
                'Linear System ILUT Tolerance':
                element.linearSystemILUTToleranceEdit,
                'Linear System Abort Not Converged':
                element.linearSystemAbortWhenNotConvergedCheck,
                'Linear System Residual Output':
                element.linearSystemResidualOutputEdit,
                'Linear System Precondition Recompute':
                element.linearSystemPreconditionRecomputeEdit,
                'ParaSails Threshold': element.thresholdEdit,
                'ParaSails Filter': element.filterEdit,
                'ParaSails MaxLevel': element.maxLevelEdit,
                'ParaSails Symmetry': element.symmetryEdit,
                'BoomerAMG Relax Type': element.boomerRelaxation,
                'BoomerAMG Coarsen Type': element.boomerCoarsening,
                'BoomerAMG Num Sweeps': element.boomerSweeps,
                'BoomerAMG Max Levels': element.boomerMaxLevels,
                'BoomerAMG Interpolation': element.boomerInterpolation,
                'BoomerAMG Smooth Type': element.boomerSmoother,
                'BoomerAMG Cycle Type': element.boomerCycle,
                'Adaptive Mesh Refinement':
                element.adaptiveMeshRefinementCheck,
                'Adaptive Mesh Name': element.adaptiveMeshNameEdit,
                'Adaptive Remesh': element.adaptiveRemeshCheck,
                'Adaptive Save Mesh': element.adaptiveSaveMeshCheck,
                'Adaptive Coarsening': element.adaptiveCoarseningCheck,
                'Adaptive Error Limit': element.adaptiveErrorLimitEdit,
                'Adaptive Min H': element.adaptiveMinHEdit,
                'Adaptive Max H': element.adaptiveMaxHEdit,
                'Adaptive Max Change': element.adaptiveMaxChangeEdit}

        while data:
            key, value = data.pop(0).split('=')
            key = key.strip()
            value = value.strip()
            if key == 'Linear System Solver' and value == 'Direct':
                element.linearSystemSolverDirect.setChecked(True)
                continue
            if key == 'Linear System Solver' and value == 'Iterative':
                element.linearSystemSolverIterative.setChecked(True)
                continue
            if key == 'Linear System Solver' and value == 'MultiGrid':
                element.linearSystemSolverMultigrid.setChecked(True)
                continue
            if key == 'Linear System Use HYPRE' and value == 'True':
                element.useHypre.setChecked(True)
                continue
            if key == 'Linear System Preconditioning' and value == 'ParaSails':
                element.useParasails.setChecked(True)
                continue
            if key == 'Linear System Preconditioning' and value == 'BoomerAMG':
                element.useBoomerAMG.setChecked(True)
                continue
            if key == 'Adaptive Mesh Refinement':
                element.adaptiveMeshRefinement.setChecked(True)
                continue
            self._changeSettings(keys[key], value)

    def _general(self, block):
        """Change settings in the general setup of the Elmer module

        Args:
        -----
        block: str
            String containing the settings of the general setup
        """

        # get the general setups window
        ui = self._ewh.general_setup
        print('ui:-->', ui)
        self._ewh.general_setup.coordinate_mapping_lineedit.setText("tresarsdamsdv")
        print('test 4')

        # split rows
        data = block.split('\n')
        print('test 5')
        title = data.pop(0)
        print('test 6')
        if title == 'Header':
            if 'CHECK KEYWORDS' in data[0]:
                ui.checkWarning.setChecked(True)
                data.pop(0)
            print('test 6.1')
            ui.checkWarning.setChecked(False)
            print('test 6.2')
            a, b = data.pop(0).strip().split(' ')[2:]
            print('test 6.3')
            ui.meshDB_lineedit1.setText(a.replace('"', ''))
            print('test 6.4')
            ui.meshDB_lineedit2.setText(b.replace('"', ''))
            print('test 6.5')
            a = data.pop(0).strip().split(' ')[2:][0]
            print('test 6.6')
            ui.includePath_lineedit.setText(a.replace('"', ''))
            print('test 6.7')
            a = data.pop(0).strip().split(' ')[2:][0]
            print('test 6.8')
            ui.resultsDir_lineedit.setText(a.replace('"', ''))
            print('test 6.9')
            text = '\n'.join(data)
        print('test 7')
            #ui.headerFreeTextEdit.setText(text.replace('"', ''))
        
        if title == 'Simulation':
            print('test 7.0')
            a = data.pop(0).split('=')[1].strip()
            print('test 7.0.1')
            idx = ui.max_output_level_combobox.findText(a)
            print('test 7.1')
            ui.max_output_level_combobox.setCurrentIndex(idx)
            a = data.pop(0).split('=')[1].strip()
            idx = ui.coordinate_system_combobox.findText(a)
            print('test 7.1')
            ui.coordinate_system_combobox.setCurrentIndex(idx)
            a = data.pop(0).split('=')[1].strip()
            print('test 7.2')
            ui.coordinate_mapping_lineedit.setText(a)
            a = data.pop(0).split('=')[1].strip()
            idx = ui.simulation_type_combobox.findText(a)
            print('test 7.3')
            ui.simulation_type_combobox.setCurrentIndex(idx)
            a = data.pop(0).split('=')[1].strip()
            ui.steady_state_max_iter_lineedit.setText(a)
            print('test 7.4')
            a = data.pop(0).split('=')[1].strip()
            ui.output_intervals_lineedit.setText(a)
            a = data.pop(0).split('=')[1].strip()
            idx = ui.timestepping_method_combobox.findText(a)
            print('test 7.5')
            ui.timestepping_method_combobox.setCurrentIndex(idx)
            a = data.pop(0).split('=')[1].strip()
            idx = ui.bdf_order_combobox.findText(a)
            print('test 7.6')
            ui.bdf_order_combobox.setCurrentIndex(idx)
            a = data.pop(0).split('=')[1].strip()
            ui.solver_input_file_lineedit.setText(a)
            print('test 7.7')
            a = data.pop(0).split('=')[1].strip()
            ui.post_file_lineedit.setText(a)
            text = '\n'.join(data)
            #ui.simulationFreeTextEdit.setText(text)
        print('test 8')
        if title == 'Constants':
            a = data.pop(0).split('=')[1].strip()
            print('test 8.1', a)
            print(type(ui.gravity_lineedit))
            print('test 8.1.1')
            idx = ui.gravity_lineedit.setText(a)
            print('test 8.2')
            a = data.pop(0).split('=')[1].strip()
            print('test 8.3')
            idx = ui.stefan_boltzmann_lineedit.setText(a)
            print('test 8.4')
            a = data.pop(0).split('=')[1].strip()
            print('test 8.5')
            idx = ui.vacuum_permittivity_lineedit.setText(a)
            print('test 8.6')
            a = data.pop(0).split('=')[1].strip()
            print('test 8.7')
            idx = ui.boltzmann_lineedit.setText(a)
            print('test 8.8')
            a = data.pop(0).split('=')[1].strip()
            print('test 8.9')
            idx = ui.unit_change_lineedit.setText(a)
            print('test 8.10')
            text = '\n'.join(data)
            print('test 8.11')
            #ui.constantsFreeTextEdit.setText(text)
        print('test 9')
