class SifWriter():
    def __init__(self, _elmer_gui):
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
        

    def writeSif(self, dict_data):
        pass

    def getGeneralSetup(self):
        pass
