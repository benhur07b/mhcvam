# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mhcvam_unicef_indicators_household_dialog.ui'
#
# Created: Mon Mar 20 17:42:41 2017
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
        MHCVAMUnicefIndicatorsHouseholdDialog.resize(962, 531)
        MHCVAMUnicefIndicatorsHouseholdDialog.setMinimumSize(QtCore.QSize(962, 531))
        self.buttonBox = QtGui.QDialogButtonBox(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 490, 941, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.selectHHComboBox = gui.QgsMapLayerComboBox(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.selectHHComboBox.setGeometry(QtCore.QRect(160, 20, 311, 27))
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
        self.listWidget_exp = QtGui.QListWidget(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.listWidget_exp.setGeometry(QtCore.QRect(10, 170, 221, 271))
        self.listWidget_exp.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidget_exp.setObjectName(_fromUtf8("listWidget_exp"))
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
        self.selectAllBtn_exp = QtGui.QPushButton(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.selectAllBtn_exp.setGeometry(QtCore.QRect(10, 450, 81, 27))
        self.selectAllBtn_exp.setObjectName(_fromUtf8("selectAllBtn_exp"))
        self.deselectAllBtn_exp = QtGui.QPushButton(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.deselectAllBtn_exp.setGeometry(QtCore.QRect(100, 450, 81, 27))
        self.deselectAllBtn_exp.setObjectName(_fromUtf8("deselectAllBtn_exp"))
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
        self.resultFieldNameLineEdit.setGeometry(QtCore.QRect(160, 60, 311, 27))
        self.resultFieldNameLineEdit.setObjectName(_fromUtf8("resultFieldNameLineEdit"))
        self.listWidget_vul = QtGui.QListWidget(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.listWidget_vul.setGeometry(QtCore.QRect(250, 170, 221, 271))
        self.listWidget_vul.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidget_vul.setObjectName(_fromUtf8("listWidget_vul"))
        self.listWidget_cap = QtGui.QListWidget(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.listWidget_cap.setGeometry(QtCore.QRect(490, 170, 221, 271))
        self.listWidget_cap.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidget_cap.setObjectName(_fromUtf8("listWidget_cap"))
        self.listWidget_oth = QtGui.QListWidget(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.listWidget_oth.setGeometry(QtCore.QRect(730, 170, 221, 271))
        self.listWidget_oth.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidget_oth.setObjectName(_fromUtf8("listWidget_oth"))
        self.label_exp = QtGui.QLabel(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.label_exp.setGeometry(QtCore.QRect(20, 140, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_exp.setFont(font)
        self.label_exp.setAutoFillBackground(False)
        self.label_exp.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_exp.setFrameShadow(QtGui.QFrame.Plain)
        self.label_exp.setWordWrap(True)
        self.label_exp.setObjectName(_fromUtf8("label_exp"))
        self.label_vul = QtGui.QLabel(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.label_vul.setGeometry(QtCore.QRect(260, 140, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_vul.setFont(font)
        self.label_vul.setAutoFillBackground(False)
        self.label_vul.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_vul.setFrameShadow(QtGui.QFrame.Plain)
        self.label_vul.setWordWrap(True)
        self.label_vul.setObjectName(_fromUtf8("label_vul"))
        self.label_cap = QtGui.QLabel(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.label_cap.setGeometry(QtCore.QRect(500, 140, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_cap.setFont(font)
        self.label_cap.setAutoFillBackground(False)
        self.label_cap.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_cap.setFrameShadow(QtGui.QFrame.Plain)
        self.label_cap.setWordWrap(True)
        self.label_cap.setObjectName(_fromUtf8("label_cap"))
        self.label_oth = QtGui.QLabel(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.label_oth.setGeometry(QtCore.QRect(740, 140, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_oth.setFont(font)
        self.label_oth.setAutoFillBackground(False)
        self.label_oth.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_oth.setFrameShadow(QtGui.QFrame.Plain)
        self.label_oth.setWordWrap(True)
        self.label_oth.setObjectName(_fromUtf8("label_oth"))
        self.selectAllBtn_vul = QtGui.QPushButton(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.selectAllBtn_vul.setGeometry(QtCore.QRect(250, 450, 81, 27))
        self.selectAllBtn_vul.setObjectName(_fromUtf8("selectAllBtn_vul"))
        self.deselectAllBtn_vul = QtGui.QPushButton(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.deselectAllBtn_vul.setGeometry(QtCore.QRect(340, 450, 81, 27))
        self.deselectAllBtn_vul.setObjectName(_fromUtf8("deselectAllBtn_vul"))
        self.selectAllBtn_cap = QtGui.QPushButton(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.selectAllBtn_cap.setGeometry(QtCore.QRect(490, 450, 81, 27))
        self.selectAllBtn_cap.setObjectName(_fromUtf8("selectAllBtn_cap"))
        self.deselectAllBtn_cap = QtGui.QPushButton(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.deselectAllBtn_cap.setGeometry(QtCore.QRect(580, 450, 81, 27))
        self.deselectAllBtn_cap.setObjectName(_fromUtf8("deselectAllBtn_cap"))
        self.selectAllBtn_oth = QtGui.QPushButton(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.selectAllBtn_oth.setGeometry(QtCore.QRect(730, 450, 81, 27))
        self.selectAllBtn_oth.setObjectName(_fromUtf8("selectAllBtn_oth"))
        self.deselectAllBtn_oth = QtGui.QPushButton(MHCVAMUnicefIndicatorsHouseholdDialog)
        self.deselectAllBtn_oth.setGeometry(QtCore.QRect(820, 450, 81, 27))
        self.deselectAllBtn_oth.setObjectName(_fromUtf8("deselectAllBtn_oth"))

        self.retranslateUi(MHCVAMUnicefIndicatorsHouseholdDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MHCVAMUnicefIndicatorsHouseholdDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MHCVAMUnicefIndicatorsHouseholdDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(MHCVAMUnicefIndicatorsHouseholdDialog)

    def retranslateUi(self, MHCVAMUnicefIndicatorsHouseholdDialog):
        MHCVAMUnicefIndicatorsHouseholdDialog.setWindowTitle(_translate("MHCVAMUnicefIndicatorsHouseholdDialog", "MHCVAM using UNICEF Indicators (HOUSEHOLD)", None))
        self.selectHHLabel.setText(_translate("MHCVAMUnicefIndicatorsHouseholdDialog", "Household Layer", None))
        self.selectIndicatorLabel.setText(_translate("MHCVAMUnicefIndicatorsHouseholdDialog", "Select Indicators to Add", None))
        self.selectAllBtn_exp.setText(_translate("MHCVAMUnicefIndicatorsHouseholdDialog", "Select All", None))
        self.deselectAllBtn_exp.setText(_translate("MHCVAMUnicefIndicatorsHouseholdDialog", "Deselect All", None))
        self.resultFieldNameLabel.setText(_translate("MHCVAMUnicefIndicatorsHouseholdDialog", "Resulting Field Name (max 10 chars)", None))
        self.label_exp.setText(_translate("MHCVAMUnicefIndicatorsHouseholdDialog", "Exposure", None))
        self.label_vul.setText(_translate("MHCVAMUnicefIndicatorsHouseholdDialog", "Vulnerability", None))
        self.label_cap.setText(_translate("MHCVAMUnicefIndicatorsHouseholdDialog", "Capacity", None))
        self.label_oth.setText(_translate("MHCVAMUnicefIndicatorsHouseholdDialog", "Others", None))
        self.selectAllBtn_vul.setText(_translate("MHCVAMUnicefIndicatorsHouseholdDialog", "Select All", None))
        self.deselectAllBtn_vul.setText(_translate("MHCVAMUnicefIndicatorsHouseholdDialog", "Deselect All", None))
        self.selectAllBtn_cap.setText(_translate("MHCVAMUnicefIndicatorsHouseholdDialog", "Select All", None))
        self.deselectAllBtn_cap.setText(_translate("MHCVAMUnicefIndicatorsHouseholdDialog", "Deselect All", None))
        self.selectAllBtn_oth.setText(_translate("MHCVAMUnicefIndicatorsHouseholdDialog", "Select All", None))
        self.deselectAllBtn_oth.setText(_translate("MHCVAMUnicefIndicatorsHouseholdDialog", "Deselect All", None))

from qgis import gui
