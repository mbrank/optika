class SifWriter():
    def __init__(self, _elmer_gui, file_to_save):
        """Constructor

        Args:
        -----
        ewh: ElmerWindowHandler class
            current instance of the ElmerWindowHandler class
            containing all data
        """

        self._elmer_gui = _elmer_gui
        self._eq_data = {}
        self._sifIds = {}
        self.errormsg = ''
        self.general_setup = self._elmer_gui.general_setup
        self.equations = self._elmer_gui.equations
        self.boundary_conditions = self._elmer_gui.boundary_conditions
        self.materials = self._elmer_gui.materials
        self.body_forces = self._elmer_gui.body_forces
        self.solvers = self._elmer_gui.solvers

        
        self.file_to_save = file_to_save
        self.file_string = ''
        
        #print(self.general_setup.data)
        #print(self.equations.data)
        #print(self.boundary_conditions.data)
        #print(self.materials.data)
        #print(self.body_forces.data)
        #print(self.solvers.data)

    def writeSif(self):

        # create dict to switch between equations and solvers
        solv_to_eq = {} # contains names of solvers and ints corresponding ID number
        # Collect all solvers 
        # collect all solvers from solvers:
        solvers_string = ''
        solv_id = 1
        for solv_nr in enumerate(self.solvers.data):
            solver = self.solvers.data[solv_nr[1]]
            #print('solver', solver)
            solvers_string += "\nSolver "+str(solv_nr[0]+1)+'\n'
            for sol in solver:
                ##print("sol", sol, sol)
                solv_id = solv_nr[0]+1
                if sol == "name":
                    solv_to_eq[solver[sol]] = solv_nr[0]+1
                    solvers_string += '  ' + sol+' = "'+solver[sol]+'"\n'
                else:
                    solvers_string += '  ' + sol+' = '+solver[sol]+'\n'
            solvers_string += "End\n"

        # collect all solvers from equations
        #print(solv_nr[0])
        for eq_nr in enumerate(self.equations.data):
            equation = self.equations.data[eq_nr[1]]
            print('equation', equation)
            if equation.get("solvers of eq"):
                #print("solvers of eq TRUE")
                solvers_string += "\nSolver "+str(solv_id+eq_nr[0]+1)+'\n'
                for solv_data in equation["solvers of eq"]:
                    if solv_data == "name":
                        print("test name of solvcer", equation["solvers of eq"][solv_data])
                        solv_to_eq[equation["solvers of eq"][solv_data]] = solv_id+eq_nr[0]+1
                        solvers_string += '  ' + solv_data+' = "'+equation["solvers of eq"][solv_data]+'"\n'
                    else:
                        solvers_string += '  ' + solv_data+' = '+equation["solvers of eq"][solv_data]+'\n'
                        

        print("solv_to_eq", solv_to_eq)
        ##print("self.materials", self.materials.data)
        for i in enumerate(self.equations.data):
            equation = self.equations.data[i[1]]
            self.file_string += "\nEquation "+str(i[0]+1)+'\n'
            ##print()
            for eq in equation:
                #print("eq", eq, equation[eq])
                if eq == 'active solvers':
                    self.file_string += '  ' + eq
                    eqs = equation[eq].split(' ')
                    print("EQS", eqs)
                    self.file_string +='('+str(len(eqs))+')'+' = '
                    for i in eqs:
                        if solv_to_eq.get(i):
                            self.file_string += str(solv_to_eq[i])+' '
                        else:
                            print('Error writing to Equation "'+equation['name']+'"! Solver "'+i+'" does not exist!!! Check active solvers in Equations and Solver names in Solvers!')
                    self.file_string += '\n'
                else:
                    if eq != 'solvers of eq':
                        self.file_string += '  ' + eq+' = '+equation[eq]+'\n'
            self.file_string += "End\n"

        for i in enumerate(self.materials.data):
            material = self.materials.data[i[1]]
            ##print("material", material)
            self.file_string += "\nMaterial "+str(i[0]+1)+'\n' # Numbering
                                                             # in
                                                             # Elmer
                                                             # starts
                                                             # from 1,
                                                             # not 0
            for mat in material:
                ##print("mat", mat, mat)
                if mat == "name":
                    self.file_string += '  ' +mat+' = "'+material[mat]+'"\n'
                else:
                    self.file_string += '  ' +mat+' = '+material[mat]+'\n'
            self.file_string += "End\n"

        #def write_block(self, data):
        ##print("self.materials", self.materials.data)
        for i in enumerate(self.body_forces.data):
            b_forces = self.body_forces.data[i[1]]
            self.file_string += "\nBody Force "+str(i[0]+1)+'\n'
            for bf in b_forces:
                ##print("bf", bf, bf)
                self.file_string += '  ' +bf+' = '+b_forces[bf]+'\n'
            self.file_string += "End\n"

        for i in enumerate(self.boundary_conditions.data):
            b_cond = self.boundary_conditions.data[i[1]]
            self.file_string += "\nBoundary Condition "+str(i[0]+1)+'\n'
            for bc in b_cond:
                ##print("bc", bc, bc)
                self.file_string += '  ' +bc+' = '+b_cond[bc]+'\n'
            self.file_string += "End\n"

        self.file_string = solvers_string + self.file_string
        f = open(self.file_to_save, 'w')
        f.write(self.file_string)  # .encode('utf-16'))
        f.close()

    def getGeneralSetup(self):
        pass

    
