import sys
from PyQt5.QtWidgets import (QInputDialog, QLineEdit, QDialog,
                             QApplication, QWidget, QLabel,
                             QApplication, QHBoxLayout, QMainWindow,
                             QCheckBox, QPushButton, QHBoxLayout,
                             QVBoxLayout)
from PyQt5.QtCore import QProcess
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

        #self.about.clicked.connect(self.onAbout)
        #self.reader.clicked.connect(self.onReadSif)
        #self.general.clicked.connect(self.onGeneralSetup)
        #self.eq.clicked.connect(self.onShowEquations)
        #self.mat.clicked.connect(self.onShowMaterials)
        #self.bf.clicked.connect(self.onShowBodyForces)
        #self.bc.clicked.connect(self.onShowBoundaryConditions)
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

def main():

    app = QApplication(sys.argv)
    ex = ElmerGui()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
