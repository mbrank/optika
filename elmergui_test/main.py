import os
import sys
from PyQt5.QtWidgets import (QInputDialog, QLineEdit, QDialog,
                             QApplication, QWidget, QLabel,
                             QHBoxLayout, QMainWindow,
                             QCheckBox, QPushButton,
                             QVBoxLayout, QMessageBox, QFileDialog,
                             QStackedWidget, QCheckBox)
from PyQt5.QtCore import QProcess, pyqtSlot, QTimer
from sif_reader import SifReader
from general_setup import GeneralSetup
from base_sif import BaseSIF
from equations import Equations
from materials import Materials
from body_forces import BodyForces
from boundary_conditions import BoundaryConditions
#from PyQt5 import (QDialog, QPushButton, pyqtSlot, QVBoxLayout,
#                   QMessageBox, QProcess, QLineEdit,
#                   QLabel, QCheckBox, QComboBox)


class ElmerGui(QDialog):
    """Dialog for showing ELMER controls.
    """

    #def __init__(self, entry, sifstring, casedim, parent=None):
    def __init__(self):
        # global main
        super(ElmerGui, self).__init__()
        self.main = {}
        self.setWindowTitle('Elmer tools')
        self.process = QProcess()
        #self.entry = entry
        #self.casedim = casedim
        #if self.entry not in self.main:
        #    self.main[self.entry] = ElmerWindowHandler()
        # String that contains sif file
        #self.sifstring = sifstring
        #if self.sifstring:
        #    self.main[self.entry].sif_read(self.sifstring)
        self.initUi()

    def initUi(self):
        self.casename = QLabel('Case name')
        self.casename_lb = QLineEdit()
        self.caseDimension = QLabel('Select case type')
        self.dimension2 = QCheckBox('2D', self)
        self.dimension3 = QCheckBox('3D', self)
        #if self.casedim == 3:
        #    self._toggle = False
        #else:
        #    self._toggle = True
        #self.dimension2.setChecked(self._toggle)
        #self.dimension3.setChecked(not self._toggle)
        #self.dimension3.clicked.connect(self.toggle)
        #self.dimension2.clicked.connect(self.toggle)
        self.about = QPushButton('About')
        self.reader = QPushButton('Read sif file')
        self.general = QPushButton('General settings')
        self.eq = QPushButton('Equations')
        self.mat = QPushButton('Materials')
        self.bf = QPushButton('Body Forces')
        self.bc = QPushButton('Boundary conditions')
        self.ic = QPushButton('Initial conditions')
        self.meshselection = QLabel('Select mesh')
        #meshes = getListOfMeshes()
        #self.mesh = self.addDropDown("Select mesh", meshes)
        self.ep = QPushButton('Object properties')
        self.parallel = QPushButton('Parallel settings')
        self.savecase = QPushButton('Save case to ELMER study')

        self.about.clicked.connect(self.onAbout)
        self.reader.clicked.connect(self.onReadSif)
        self.general.clicked.connect(self.onGeneralSettings)
        self.eq.clicked.connect(self.onEquations)
        self.mat.clicked.connect(self.onMaterials)
        self.bf.clicked.connect(self.onBodyForces)
        self.bc.clicked.connect(self.onBoundaryConditions)
        #self.ic.clicked.connect(self.onShowInitialConditions)
        #self.ep.clicked.connect(self.onDefineElementProperties)
        #self.parallel.clicked.connect(self.onParallelSettings)
        #self.savecase.clicked.connect(self.onSaveCaseToELMERStudy)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.casename)
        self.layout.addWidget(self.casename_lb)
        self.layout.addWidget(self.caseDimension)
        self.layout.addWidget(self.dimension2)
        self.layout.addWidget(self.dimension3)
        self.layout.addWidget(self.about)
        self.layout.addWidget(self.reader)
        self.layout.addWidget(self.general)
        self.layout.addWidget(self.eq)
        self.layout.addWidget(self.mat)
        self.layout.addWidget(self.bf)
        self.layout.addWidget(self.bc)
        self.layout.addWidget(self.ic)
        self.layout.addWidget(self.meshselection)
        #self.layout.addWidget(self.mesh)
        self.layout.addWidget(self.ep)
        self.layout.addWidget(self.parallel)
        self.layout.addWidget(self.savecase)
        self.setLayout(self.layout)

        self.general_setup = GeneralSetup(0)

    @pyqtSlot()
    def onAbout(self):
        '''This method displays details about ELMER interface for SMTER

        '''

        title = "ELMER interface for SMITER editor"
        msg = "Interface that allows setup of an Elmer simulation with the " \
              "help of the Salome Mesh editor and generation of necessary " \
              "sif-file.\nThe mesh is exported as *.unv and converted with " \
              "ElmerGrid. ElmerSolver can be started in a single process or " \
              "using multiprocessing.\n\n"
        QMessageBox.about(None, title, msg)

    @pyqtSlot()
    def onReadSif(self, file=''):
        #self.main[self.entry].sif_read()
        # create new instance of SifReader-class
        sr = SifReader(self)
        if file == '':
            file = QFileDialog.getOpenFileName(parent=None,
                                               caption="Select sif-File",
                                               filter='*.sif')
            file = str(file[0])
        try:
            sr.readSif(file)
            self.sifFile = file
            self.meshDirectory = os.path.dirname(file)
        except Exception:
            QMessageBox.warning(None, 'Error', 'Error')

    @pyqtSlot()
    def onGeneralSettings(self, data=0):
        if not data:
            print('test')
            # load default data
            #app = QApplication(sys.argv)
            #ex = GeneralSetup(data)
            self.general_setup.exec()
            #ex.show()
            #sys.exit(app.exec_())
        else:
            # load dictionary into gui
            pass

    @pyqtSlot()
    def onEquations(self, data=0):
        if not data:
            print('test')
            # load default data
            #app = QApplication(sys.argv)
            ex = Equations(data)
            #sys.exit(app.exec_())
        else:
            # load dictionary into gui
            pass

    @pyqtSlot()
    def onMaterials(self, data=0):
        if not data:
            print('test')
            # load default data
            #app = QApplication(sys.argv)
            ex = Materials(data)
            #sys.exit(app.exec_())
        else:
            # load dictionary into gui
            pass

    @pyqtSlot()
    def onBodyForces(self, data=0):
        if not data:
            print('test')
            # load default data
            #app = QApplication(sys.argv)
            ex = BodyForces(data)
            #sys.exit(app.exec_())
        else:
            # load dictionary into gui
            pass

    @pyqtSlot()
    def onBoundaryConditions(self, data=0):
        if not data:
            print('test')
            # load default data
            #app = QApplication(sys.argv)
            ex = BoundaryConditions(data)
            #sys.exit(app.exec_())
        else:
            # load dictionary into gui
            pass


def main():

    app = QApplication(sys.argv)
    ex = ElmerGui()
    ex.show()

    # Purpose of timer
    #  |
    #  |
    #  V
    # https://machinekoder.com/how-to-not-shoot-yourself
    # -in-the-foot-using-python-qt/
    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
