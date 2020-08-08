from PySide2 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import mayautils

def maya_main_window():
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class SmartSave(QtWidgets.QDialog):

    def __init__(self):
        super(SmartSave, self).__init__(parent = maya_main_window())
        self.setWindowTitle('Smart Save')
        self.resize(450, 200)
        self.smartCore = mayautils.SceneFile()

        self.create_widgets()
        self.create_layout()
        self.establish_connections()

    def create_widgets(self):
        self.lbl_title = QtWidgets.QLabel("Smart Save")
        self.lbl_dir = QtWidgets.QLabel("Directory")
        self.lbl_descript = QtWidgets.QLabel("Descriptor")
        self.lbl_version = QtWidgets.QLabel("Version")
        self.lbl_ext = QtWidgets.QLabel("Extension")

        self.btn_browse = QtWidgets.QPushButton("Browse...")
        self.btn_increment = QtWidgets.QPushButton("Increment and Save")
        self.btn_save = QtWidgets.QPushButton("Save")
        self.btn_cancel = QtWidgets.QPushButton("Cancel")

        self.ln_dir = QtWidgets.QLineEdit()
        self.ln_dir.setText(self.smartCore.dir)
        self.ln_descript = QtWidgets.QLineEdit()
        self.ln_descript.setText(self.smartCore.descriptor)
        self.ln_ext = QtWidgets.QLineEdit()
        self.ln_ext.setText(self.smartCore.ext)

        self.spn_version = QtWidgets.QSpinBox()
        self.spn_version.setValue(self.smartCore.version)
        self.spn_version.setMinimum(self.smartCore.version)



    def create_layout(self):
        self.lay_main = QtWidgets.QVBoxLayout()
        self.setLayout(self.lay_main)
        self.lay_main.addWidget(self.lbl_title)

        self.lay_dir = QtWidgets.QHBoxLayout()
        self.lay_descript = QtWidgets.QHBoxLayout()
        self.lay_version = QtWidgets.QHBoxLayout()
        self.lay_ext = QtWidgets.QHBoxLayout()
        self.lay_confrim = QtWidgets.QHBoxLayout()

        self.lay_dir.addWidget(self.lbl_dir)
        self.lay_dir.addWidget(self.ln_dir)
        self.lay_dir.addWidget(self.btn_browse)

        self.lay_descript.addWidget(self.lbl_descript)
        self.lay_descript.addWidget(self.ln_descript)

        self.lay_version.addWidget(self.lbl_version)
        self.lay_version.addWidget(self.spn_version)

        self.lay_ext.addWidget(self.lbl_ext)
        self.lay_ext.addWidget(self.ln_ext)

        self.lay_confrim.addWidget(self.btn_increment)
        self.lay_confrim.addWidget(self.btn_save)
        self.lay_confrim.addWidget(self.btn_cancel)

        self.lay_main.addLayout(self.lay_dir)
        self.lay_main.addLayout(self.lay_descript)
        self.lay_main.addLayout(self.lay_version)
        self.lay_main.addLayout(self.lay_ext)
        self.lay_main.addStretch()
        self.lay_main.addLayout(self.lay_confrim)

    def establish_connections(self):
        self.btn_save.clicked.connect(self.onSave)
        self.btn_increment.clicked.connect(self.onIncrement_and_save)
        self.btn_browse.clicked.connect(self.onBrowse)
        self.btn_cancel.clicked.connect(self.onCancel)

        self.spn_version.valueChanged.connect(self.setVersion)

        self.ln_dir.editingFinished.connect(self.setDirectory)
        self.ln_ext.editingFinished.connect(self.setExtension)
        self.ln_descript.editingFinished.connect(self.setDescriptor)

    @QtCore.Slot()
    def setVersion(self, val):
        self.smartCore.version = val

    @QtCore.Slot()
    def setExtension(self):
        self.smartCore.ext = self.ln_ext.text()

    @QtCore.Slot()
    def setDirectory(self):
        self.smartCore.dir = self.ln_dir.text()

    @QtCore.Slot()
    def setDescriptor(self):
        self.smartCore.descriptor = self.ln_descript.text()
        self.spn_version.setMinimum(0)
        self.smartCore.version = 0

    @QtCore.Slot()
    def onIncrement_and_save(self):
        self.smartCore.increment_and_save()
        self.spn_version.setMinimum(self.smartCore.version + 1)

    @QtCore.Slot()
    def onSave(self):
        self.smartCore.save()
        self.spn_version.setMinimum(self.smartCore.version + 1)

    @QtCore.Slot()
    def onCancel(self):
        self.close()

    @QtCore.Slot()
    def onBrowse(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(
            parent = self,
            caption = "Select a Directory",
            dir = self.ln_dir.text(),
            options = QtWidgets.QFileDialog.ShowDirsOnly
             )
        self.ln_dir.setText(dir)
        self.smartCore.dir = dir