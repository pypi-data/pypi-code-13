# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/grossmj/PycharmProjects/gns3-gui/gns3/modules/iou/ui/iou_device_wizard.ui'
#
# Created: Fri Jun 10 21:29:04 2016
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_IOUDeviceWizard(object):
    def setupUi(self, IOUDeviceWizard):
        IOUDeviceWizard.setObjectName("IOUDeviceWizard")
        IOUDeviceWizard.resize(586, 411)
        IOUDeviceWizard.setModal(True)
        self.uiServerWizardPage = QtWidgets.QWizardPage()
        self.uiServerWizardPage.setObjectName("uiServerWizardPage")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.uiServerWizardPage)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.uiServerTypeGroupBox = QtWidgets.QGroupBox(self.uiServerWizardPage)
        self.uiServerTypeGroupBox.setObjectName("uiServerTypeGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.uiServerTypeGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.uiRemoteRadioButton = QtWidgets.QRadioButton(self.uiServerTypeGroupBox)
        self.uiRemoteRadioButton.setChecked(True)
        self.uiRemoteRadioButton.setObjectName("uiRemoteRadioButton")
        self.verticalLayout.addWidget(self.uiRemoteRadioButton)
        self.uiVMRadioButton = QtWidgets.QRadioButton(self.uiServerTypeGroupBox)
        self.uiVMRadioButton.setObjectName("uiVMRadioButton")
        self.verticalLayout.addWidget(self.uiVMRadioButton)
        self.uiLocalRadioButton = QtWidgets.QRadioButton(self.uiServerTypeGroupBox)
        self.uiLocalRadioButton.setObjectName("uiLocalRadioButton")
        self.verticalLayout.addWidget(self.uiLocalRadioButton)
        self.gridLayout_2.addWidget(self.uiServerTypeGroupBox, 0, 0, 1, 1)
        self.uiRemoteServersGroupBox = QtWidgets.QGroupBox(self.uiServerWizardPage)
        self.uiRemoteServersGroupBox.setObjectName("uiRemoteServersGroupBox")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.uiRemoteServersGroupBox)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.uiRemoteServersLabel = QtWidgets.QLabel(self.uiRemoteServersGroupBox)
        self.uiRemoteServersLabel.setObjectName("uiRemoteServersLabel")
        self.gridLayout_7.addWidget(self.uiRemoteServersLabel, 0, 0, 1, 1)
        self.uiRemoteServersComboBox = QtWidgets.QComboBox(self.uiRemoteServersGroupBox)
        self.uiRemoteServersComboBox.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiRemoteServersComboBox.sizePolicy().hasHeightForWidth())
        self.uiRemoteServersComboBox.setSizePolicy(sizePolicy)
        self.uiRemoteServersComboBox.setObjectName("uiRemoteServersComboBox")
        self.gridLayout_7.addWidget(self.uiRemoteServersComboBox, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.uiRemoteServersGroupBox, 1, 0, 1, 1)
        IOUDeviceWizard.addPage(self.uiServerWizardPage)
        self.uiNameWizardPage = QtWidgets.QWizardPage()
        self.uiNameWizardPage.setObjectName("uiNameWizardPage")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.uiNameWizardPage)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout_7 = QtWidgets.QFormLayout()
        self.formLayout_7.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_7.setObjectName("formLayout_7")
        self.uiNameLabel = QtWidgets.QLabel(self.uiNameWizardPage)
        self.uiNameLabel.setObjectName("uiNameLabel")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.uiNameLabel)
        self.uiNameLineEdit = QtWidgets.QLineEdit(self.uiNameWizardPage)
        self.uiNameLineEdit.setObjectName("uiNameLineEdit")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.uiNameLineEdit)
        self.verticalLayout_2.addLayout(self.formLayout_7)
        self.groupBox = QtWidgets.QGroupBox(self.uiNameWizardPage)
        self.groupBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.groupBox.setAutoFillBackground(False)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.uiExistingImageRadioButton = QtWidgets.QRadioButton(self.groupBox)
        self.uiExistingImageRadioButton.setChecked(True)
        self.uiExistingImageRadioButton.setObjectName("uiExistingImageRadioButton")
        self.horizontalLayout_2.addWidget(self.uiExistingImageRadioButton)
        self.uiNewImageRadioButton = QtWidgets.QRadioButton(self.groupBox)
        self.uiNewImageRadioButton.setChecked(False)
        self.uiNewImageRadioButton.setObjectName("uiNewImageRadioButton")
        self.horizontalLayout_2.addWidget(self.uiNewImageRadioButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.formLayout_8 = QtWidgets.QFormLayout()
        self.formLayout_8.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_8.setObjectName("formLayout_8")
        self.uiTypeLabel = QtWidgets.QLabel(self.groupBox)
        self.uiTypeLabel.setObjectName("uiTypeLabel")
        self.formLayout_8.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.uiTypeLabel)
        self.uiTypeComboBox = QtWidgets.QComboBox(self.groupBox)
        self.uiTypeComboBox.setObjectName("uiTypeComboBox")
        self.formLayout_8.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.uiTypeComboBox)
        self.uiIOUImageLabel = QtWidgets.QLabel(self.groupBox)
        self.uiIOUImageLabel.setObjectName("uiIOUImageLabel")
        self.formLayout_8.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.uiIOUImageLabel)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.uiIOUImageListComboBox = QtWidgets.QComboBox(self.groupBox)
        self.uiIOUImageListComboBox.setObjectName("uiIOUImageListComboBox")
        self.horizontalLayout_5.addWidget(self.uiIOUImageListComboBox)
        self.uiIOUImageLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.uiIOUImageLineEdit.setObjectName("uiIOUImageLineEdit")
        self.horizontalLayout_5.addWidget(self.uiIOUImageLineEdit)
        self.uiIOUImageToolButton = QtWidgets.QToolButton(self.groupBox)
        self.uiIOUImageToolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.uiIOUImageToolButton.setObjectName("uiIOUImageToolButton")
        self.horizontalLayout_5.addWidget(self.uiIOUImageToolButton)
        self.formLayout_8.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.verticalLayout_3.addLayout(self.formLayout_8)
        self.verticalLayout_2.addWidget(self.groupBox)
        IOUDeviceWizard.addPage(self.uiNameWizardPage)

        self.retranslateUi(IOUDeviceWizard)
        QtCore.QMetaObject.connectSlotsByName(IOUDeviceWizard)

    def retranslateUi(self, IOUDeviceWizard):
        _translate = QtCore.QCoreApplication.translate
        IOUDeviceWizard.setWindowTitle(_translate("IOUDeviceWizard", "New IOU device template"))
        self.uiServerWizardPage.setTitle(_translate("IOUDeviceWizard", "Server"))
        self.uiServerWizardPage.setSubTitle(_translate("IOUDeviceWizard", "Please choose a server type to run your new IOU device."))
        self.uiServerTypeGroupBox.setTitle(_translate("IOUDeviceWizard", "Server type"))
        self.uiRemoteRadioButton.setText(_translate("IOUDeviceWizard", "Run the IOU on a remote computers"))
        self.uiVMRadioButton.setText(_translate("IOUDeviceWizard", "Run the IOU on the GNS3 VM"))
        self.uiLocalRadioButton.setText(_translate("IOUDeviceWizard", "Run the IOU on your local computer"))
        self.uiRemoteServersGroupBox.setTitle(_translate("IOUDeviceWizard", "Remote server"))
        self.uiRemoteServersLabel.setText(_translate("IOUDeviceWizard", "Run on:"))
        self.uiNameWizardPage.setTitle(_translate("IOUDeviceWizard", "Name and image"))
        self.uiNameWizardPage.setSubTitle(_translate("IOUDeviceWizard", "Please choose a descriptive name for the new IOU device and add an IOU image."))
        self.uiNameLabel.setText(_translate("IOUDeviceWizard", "Name:"))
        self.groupBox.setTitle(_translate("IOUDeviceWizard", "Image"))
        self.uiExistingImageRadioButton.setText(_translate("IOUDeviceWizard", "Existing image"))
        self.uiNewImageRadioButton.setText(_translate("IOUDeviceWizard", "New Image"))
        self.uiTypeLabel.setText(_translate("IOUDeviceWizard", "Type:"))
        self.uiIOUImageLabel.setText(_translate("IOUDeviceWizard", "IOU image:"))
        self.uiIOUImageToolButton.setText(_translate("IOUDeviceWizard", "&Browse..."))

