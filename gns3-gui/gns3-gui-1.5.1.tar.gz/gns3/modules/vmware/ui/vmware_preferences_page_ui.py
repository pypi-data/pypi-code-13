# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/grossmj/PycharmProjects/gns3-gui/gns3/modules/vmware/ui/vmware_preferences_page.ui'
#
# Created: Tue May 31 11:28:22 2016
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VMwarePreferencesPageWidget(object):
    def setupUi(self, VMwarePreferencesPageWidget):
        VMwarePreferencesPageWidget.setObjectName("VMwarePreferencesPageWidget")
        VMwarePreferencesPageWidget.resize(464, 255)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(VMwarePreferencesPageWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.uiTabWidget = QtWidgets.QTabWidget(VMwarePreferencesPageWidget)
        self.uiTabWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.uiTabWidget.setObjectName("uiTabWidget")
        self.uiGeneralSettingsTabWidget = QtWidgets.QWidget()
        self.uiGeneralSettingsTabWidget.setObjectName("uiGeneralSettingsTabWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.uiGeneralSettingsTabWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.uiUseLocalServercheckBox = QtWidgets.QCheckBox(self.uiGeneralSettingsTabWidget)
        self.uiUseLocalServercheckBox.setChecked(True)
        self.uiUseLocalServercheckBox.setObjectName("uiUseLocalServercheckBox")
        self.gridLayout_2.addWidget(self.uiUseLocalServercheckBox, 0, 0, 1, 1)
        self.uiVmrunPathLabel = QtWidgets.QLabel(self.uiGeneralSettingsTabWidget)
        self.uiVmrunPathLabel.setObjectName("uiVmrunPathLabel")
        self.gridLayout_2.addWidget(self.uiVmrunPathLabel, 1, 0, 1, 1)
        self.uiHostTypeLabel = QtWidgets.QLabel(self.uiGeneralSettingsTabWidget)
        self.uiHostTypeLabel.setObjectName("uiHostTypeLabel")
        self.gridLayout_2.addWidget(self.uiHostTypeLabel, 3, 0, 1, 1)
        self.uiHostTypeComboBox = QtWidgets.QComboBox(self.uiGeneralSettingsTabWidget)
        self.uiHostTypeComboBox.setObjectName("uiHostTypeComboBox")
        self.gridLayout_2.addWidget(self.uiHostTypeComboBox, 4, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 5, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.uiVmrunPathLineEdit = QtWidgets.QLineEdit(self.uiGeneralSettingsTabWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiVmrunPathLineEdit.sizePolicy().hasHeightForWidth())
        self.uiVmrunPathLineEdit.setSizePolicy(sizePolicy)
        self.uiVmrunPathLineEdit.setObjectName("uiVmrunPathLineEdit")
        self.horizontalLayout_5.addWidget(self.uiVmrunPathLineEdit)
        self.uiVmrunPathToolButton = QtWidgets.QToolButton(self.uiGeneralSettingsTabWidget)
        self.uiVmrunPathToolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.uiVmrunPathToolButton.setObjectName("uiVmrunPathToolButton")
        self.horizontalLayout_5.addWidget(self.uiVmrunPathToolButton)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 2, 0, 1, 1)
        self.uiTabWidget.addTab(self.uiGeneralSettingsTabWidget, "")
        self.uiNetworkTab = QtWidgets.QWidget()
        self.uiNetworkTab.setObjectName("uiNetworkTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.uiNetworkTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.uiManagedVMnetRangeGroupBox = QtWidgets.QGroupBox(self.uiNetworkTab)
        self.uiManagedVMnetRangeGroupBox.setObjectName("uiManagedVMnetRangeGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.uiManagedVMnetRangeGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.uiVMnetStartRangeSpinBox = QtWidgets.QSpinBox(self.uiManagedVMnetRangeGroupBox)
        self.uiVMnetStartRangeSpinBox.setMinimum(2)
        self.uiVMnetStartRangeSpinBox.setMaximum(19)
        self.uiVMnetStartRangeSpinBox.setObjectName("uiVMnetStartRangeSpinBox")
        self.horizontalLayout_3.addWidget(self.uiVMnetStartRangeSpinBox)
        self.uiToLabel = QtWidgets.QLabel(self.uiManagedVMnetRangeGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiToLabel.sizePolicy().hasHeightForWidth())
        self.uiToLabel.setSizePolicy(sizePolicy)
        self.uiToLabel.setObjectName("uiToLabel")
        self.horizontalLayout_3.addWidget(self.uiToLabel)
        self.uiVMnetEndRangeSpinBox = QtWidgets.QSpinBox(self.uiManagedVMnetRangeGroupBox)
        self.uiVMnetEndRangeSpinBox.setMinimum(2)
        self.uiVMnetEndRangeSpinBox.setMaximum(19)
        self.uiVMnetEndRangeSpinBox.setProperty("value", 19)
        self.uiVMnetEndRangeSpinBox.setObjectName("uiVMnetEndRangeSpinBox")
        self.horizontalLayout_3.addWidget(self.uiVMnetEndRangeSpinBox)
        self.uiConfigureVmnetPushButton = QtWidgets.QPushButton(self.uiManagedVMnetRangeGroupBox)
        self.uiConfigureVmnetPushButton.setObjectName("uiConfigureVmnetPushButton")
        self.horizontalLayout_3.addWidget(self.uiConfigureVmnetPushButton)
        self.uiResetVmnetPushButton = QtWidgets.QPushButton(self.uiManagedVMnetRangeGroupBox)
        self.uiResetVmnetPushButton.setObjectName("uiResetVmnetPushButton")
        self.horizontalLayout_3.addWidget(self.uiResetVmnetPushButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.uiBlockHostTrafficCheckBox = QtWidgets.QCheckBox(self.uiManagedVMnetRangeGroupBox)
        self.uiBlockHostTrafficCheckBox.setChecked(True)
        self.uiBlockHostTrafficCheckBox.setObjectName("uiBlockHostTrafficCheckBox")
        self.verticalLayout.addWidget(self.uiBlockHostTrafficCheckBox)
        self.verticalLayout_3.addWidget(self.uiManagedVMnetRangeGroupBox)
        spacerItem2 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.uiTabWidget.addTab(self.uiNetworkTab, "")
        self.verticalLayout_2.addWidget(self.uiTabWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(164, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.uiRestoreDefaultsPushButton = QtWidgets.QPushButton(VMwarePreferencesPageWidget)
        self.uiRestoreDefaultsPushButton.setObjectName("uiRestoreDefaultsPushButton")
        self.horizontalLayout_2.addWidget(self.uiRestoreDefaultsPushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(VMwarePreferencesPageWidget)
        self.uiTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(VMwarePreferencesPageWidget)

    def retranslateUi(self, VMwarePreferencesPageWidget):
        _translate = QtCore.QCoreApplication.translate
        VMwarePreferencesPageWidget.setWindowTitle(_translate("VMwarePreferencesPageWidget", "VMware"))
        self.uiUseLocalServercheckBox.setText(_translate("VMwarePreferencesPageWidget", "Use the local server"))
        self.uiVmrunPathLabel.setText(_translate("VMwarePreferencesPageWidget", "Path to vmrun:"))
        self.uiHostTypeLabel.setText(_translate("VMwarePreferencesPageWidget", "Host type:"))
        self.uiVmrunPathToolButton.setText(_translate("VMwarePreferencesPageWidget", "&Browse..."))
        self.uiTabWidget.setTabText(self.uiTabWidget.indexOf(self.uiGeneralSettingsTabWidget), _translate("VMwarePreferencesPageWidget", "General settings"))
        self.uiManagedVMnetRangeGroupBox.setTitle(_translate("VMwarePreferencesPageWidget", "Managed VMnet interfaces (VMnet8 excluded)"))
        self.uiVMnetStartRangeSpinBox.setPrefix(_translate("VMwarePreferencesPageWidget", "vmnet"))
        self.uiToLabel.setText(_translate("VMwarePreferencesPageWidget", "to"))
        self.uiVMnetEndRangeSpinBox.setPrefix(_translate("VMwarePreferencesPageWidget", "vmnet"))
        self.uiConfigureVmnetPushButton.setText(_translate("VMwarePreferencesPageWidget", "&Configure"))
        self.uiResetVmnetPushButton.setText(_translate("VMwarePreferencesPageWidget", "&Reset"))
        self.uiBlockHostTrafficCheckBox.setToolTip(_translate("VMwarePreferencesPageWidget", "Block network traffic originating from the host OS to be injected in vmnet interfaces. Currently supported on Windows only and is recommended."))
        self.uiBlockHostTrafficCheckBox.setText(_translate("VMwarePreferencesPageWidget", "Block network traffic originating from the host OS"))
        self.uiTabWidget.setTabText(self.uiTabWidget.indexOf(self.uiNetworkTab), _translate("VMwarePreferencesPageWidget", "Network"))
        self.uiRestoreDefaultsPushButton.setText(_translate("VMwarePreferencesPageWidget", "Restore defaults"))

