# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mhcvam_unicef_indicators_household_dialog.ui'
#
# Created: Mon Mar 20 13:23:08 2017
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MHCVAMUnicefIndicatorsHouseholdDialog(object):
    def setupUi(self, MHCVAMUnicefIndicatorsHouseholdDialog):
        MHCVAMUnicefIndicatorsHouseholdDialog.setObjectName(_fromUtf8("MHCVAMUnicefIndicatorsHouseholdDialog"))
        MHCVAMUnicefIndicatorsHouseholdDialog.resize(576, 515)
        MHCVAMUnicefIndicatorsHouseholdDialog.setMinimumSize(QtCore.QSize(576, 515))
        MHCVAMUnicefIndicatorsHouseholdDialog.setMaximumSize(QtCore.QSize(576, 515))
        self.buttonBox = QtGui.QDialogButtonBox(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 480, 561, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.selectHHComboBox = gui.QgsMapLayerComboBox(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.selectHHComboBox.setGeometry(QtCore.QRect(150, 20, 421, 27))
        self.selectHHComboBox.setFilters(gui.QgsMapLayerProxyModel.HasGeometry)
        self.selectHHComboBox.setObjectName(_fromUtf8("selectHHComboBox"))
        self.selectHHLabel = QtGui.QLabel(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.selectHHLabel.setGeometry(QtCore.QRect(10, 20, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.selectHHLabel.setFont(font)
        self.selectHHLabel.setAutoFillBackground(False)
        self.selectHHLabel.setFrameShape(QtGui.QFrame.NoFrame)
        self.selectHHLabel.setFrameShadow(QtGui.QFrame.Plain)
        self.selectHHLabel.setWordWrap(True)
        self.selectHHLabel.setObjectName(_fromUtf8("selectHHLabel"))
        self.listWidget = QtGui.QListWidget(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.listWidget.setGeometry(QtCore.QRect(10, 140, 561, 271))
        self.listWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.selectIndicatorLabel = QtGui.QLabel(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.selectIndicatorLabel.setGeometry(QtCore.QRect(10, 110, 301, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.selectIndicatorLabel.setFont(font)
        self.selectIndicatorLabel.setAutoFillBackground(False)
        self.selectIndicatorLabel.setFrameShape(QtGui.QFrame.NoFrame)
        self.selectIndicatorLabel.setFrameShadow(QtGui.QFrame.Plain)
        self.selectIndicatorLabel.setWordWrap(True)
        self.selectIndicatorLabel.setObjectName(_fromUtf8("selectIndicatorLabel"))
        self.selectAllBtn = QtGui.QPushButton(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.selectAllBtn.setGeometry(QtCore.QRect(10, 430, 101, 27))
        self.selectAllBtn.setObjectName(_fromUtf8("selectAllBtn"))
        self.deselectAllBtn = QtGui.QPushButton(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.deselectAllBtn.setGeometry(QtCore.QRect(120, 430, 101, 27))
        self.deselectAllBtn.setObjectName(_fromUtf8("deselectAllBtn"))
        self.resultFieldNameLabel = QtGui.QLabel(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.resultFieldNameLabel.setGeometry(QtCore.QRect(10, 60, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.resultFieldNameLabel.setFont(font)
        self.resultFieldNameLabel.setAutoFillBackground(False)
        self.resultFieldNameLabel.setFrameShape(QtGui.QFrame.NoFrame)
        self.resultFieldNameLabel.setFrameShadow(QtGui.QFrame.Plain)
        self.resultFieldNameLabel.setWordWrap(True)
        self.resultFieldNameLabel.setObjectName(_fromUtf8("resultFieldNameLabel"))
        self.resultFieldNameLineEdit = QtGui.QLineEdit(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.resultFieldNameLineEdit.setGeometry(QtCore.QRect(150, 60, 421, 27))
        self.resultFieldNameLineEdit.setObjectName(_fromUtf8("resultFieldNameLineEdit"))

        self.retranslateUi(MHCVAMUnicefIndicatorsHouseholdDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MHCVAMUnicefIndicatorsHouseholdDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MHCVAMUnicefIndicatorsHouseholdDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(MHCVAMUnicefIndicatorsHouseholdDialog)

    def retranslateUi(self, MHCVAMUnicefIndicatorsHouseholdDialog):
        MHCVAMUnicefIndicatorsHouseholdDialog.setWindowTitle(_translate("MHCVAMUnicefIndicatorsHouseholdDialog", "MHCVAM using UNICEF Indicators (HOUSEHOLD)", None))
        self.selectHHLabel.setText(_translate("MHCVAMUnicefIndicatorsHouseholdDialog", "Household Layer", None))
        self.selectIndicatorLabel.setText(_translate("MHCVAMUnicefIndicatorsHouseholdDialog", "Select Indicators to Add", None))
        self.selectAllBtn.setText(_translate("MHCVAMUnicefIndicatorsHouseholdDialog", "Select All", None))
        self.deselectAllBtn.setText(_translate("MHCVAMUnicefIndicatorsHouseholdDialog", "Deselect All", None))
        self.resultFieldNameLabel.setText(_translate("MHCVAMUnicefIndicatorsHouseholdDialog", "Resulting Field Name (max 10 chars)", None))

from qgis import gui
