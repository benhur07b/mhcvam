# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mhcvam_unicef_indicators_dialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_MHCVAMUnicefIndicatorsDialog(object):
    def setupUi(self, MHCVAMUnicefIndicatorsDialog):
        MHCVAMUnicefIndicatorsDialog.setObjectName(_fromUtf8("MHCVAMUnicefIndicatorsDialog"))
        MHCVAMUnicefIndicatorsDialog.resize(804, 396)
        MHCVAMUnicefIndicatorsDialog.setMinimumSize(QtCore.QSize(804, 318))
        MHCVAMUnicefIndicatorsDialog.setMaximumSize(QtCore.QSize(804, 396))
        self.buttonBox = QtGui.QDialogButtonBox(MHCVAMUnicefIndicatorsDialog)
        self.buttonBox.setGeometry(QtCore.QRect(520, 270, 271, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.layerComboBox = gui.QgsMapLayerComboBox(MHCVAMUnicefIndicatorsDialog)
        self.layerComboBox.setGeometry(QtCore.QRect(180, 20, 621, 27))
        self.layerComboBox.setFilters(gui.QgsMapLayerProxyModel.HasGeometry)
        self.layerComboBox.setObjectName(_fromUtf8("layerComboBox"))
        self.layerLabel = QtGui.QLabel(MHCVAMUnicefIndicatorsDialog)
        self.layerLabel.setGeometry(QtCore.QRect(10, 20, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.layerLabel.setFont(font)
        self.layerLabel.setAutoFillBackground(False)
        self.layerLabel.setFrameShape(QtGui.QFrame.NoFrame)
        self.layerLabel.setFrameShadow(QtGui.QFrame.Plain)
        self.layerLabel.setWordWrap(True)
        self.layerLabel.setObjectName(_fromUtf8("layerLabel"))
        self.fieldLabel = QtGui.QLabel(MHCVAMUnicefIndicatorsDialog)
        self.fieldLabel.setGeometry(QtCore.QRect(10, 140, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fieldLabel.setFont(font)
        self.fieldLabel.setAutoFillBackground(False)
        self.fieldLabel.setFrameShape(QtGui.QFrame.NoFrame)
        self.fieldLabel.setFrameShadow(QtGui.QFrame.Plain)
        self.fieldLabel.setWordWrap(True)
        self.fieldLabel.setObjectName(_fromUtf8("fieldLabel"))
        self.fieldComboBox = QtGui.QComboBox(MHCVAMUnicefIndicatorsDialog)
        self.fieldComboBox.setGeometry(QtCore.QRect(180, 140, 621, 27))
        self.fieldComboBox.setObjectName(_fromUtf8("fieldComboBox"))
        self.agencyLabel = QtGui.QLabel(MHCVAMUnicefIndicatorsDialog)
        self.agencyLabel.setGeometry(QtCore.QRect(10, 60, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.agencyLabel.setFont(font)
        self.agencyLabel.setAutoFillBackground(False)
        self.agencyLabel.setFrameShape(QtGui.QFrame.NoFrame)
        self.agencyLabel.setFrameShadow(QtGui.QFrame.Plain)
        self.agencyLabel.setWordWrap(True)
        self.agencyLabel.setObjectName(_fromUtf8("agencyLabel"))
        self.orLabel = QtGui.QLabel(MHCVAMUnicefIndicatorsDialog)
        self.orLabel.setGeometry(QtCore.QRect(10, 80, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.orLabel.setFont(font)
        self.orLabel.setAutoFillBackground(False)
        self.orLabel.setFrameShape(QtGui.QFrame.NoFrame)
        self.orLabel.setFrameShadow(QtGui.QFrame.Plain)
        self.orLabel.setWordWrap(True)
        self.orLabel.setObjectName(_fromUtf8("orLabel"))
        self.categoryLabel = QtGui.QLabel(MHCVAMUnicefIndicatorsDialog)
        self.categoryLabel.setGeometry(QtCore.QRect(10, 100, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.categoryLabel.setFont(font)
        self.categoryLabel.setAutoFillBackground(False)
        self.categoryLabel.setFrameShape(QtGui.QFrame.NoFrame)
        self.categoryLabel.setFrameShadow(QtGui.QFrame.Plain)
        self.categoryLabel.setWordWrap(True)
        self.categoryLabel.setObjectName(_fromUtf8("categoryLabel"))
        self.agencyComboBox = QtGui.QComboBox(MHCVAMUnicefIndicatorsDialog)
        self.agencyComboBox.setGeometry(QtCore.QRect(180, 60, 621, 27))
        self.agencyComboBox.setObjectName(_fromUtf8("agencyComboBox"))
        self.categoryComboBox = QtGui.QComboBox(MHCVAMUnicefIndicatorsDialog)
        self.categoryComboBox.setGeometry(QtCore.QRect(180, 100, 621, 27))
        self.categoryComboBox.setObjectName(_fromUtf8("categoryComboBox"))
        self.lowLower = QtGui.QLineEdit(MHCVAMUnicefIndicatorsDialog)
        self.lowLower.setGeometry(QtCore.QRect(250, 220, 91, 21))
        self.lowLower.setObjectName(_fromUtf8("lowLower"))
        self.lowLabel = QtGui.QLabel(MHCVAMUnicefIndicatorsDialog)
        self.lowLabel.setGeometry(QtCore.QRect(180, 220, 58, 21))
        self.lowLabel.setObjectName(_fromUtf8("lowLabel"))
        self.lowTo = QtGui.QLabel(MHCVAMUnicefIndicatorsDialog)
        self.lowTo.setGeometry(QtCore.QRect(340, 220, 31, 21))
        self.lowTo.setAlignment(QtCore.Qt.AlignCenter)
        self.lowTo.setObjectName(_fromUtf8("lowTo"))
        self.lowUpper = QtGui.QLineEdit(MHCVAMUnicefIndicatorsDialog)
        self.lowUpper.setGeometry(QtCore.QRect(370, 220, 91, 21))
        self.lowUpper.setObjectName(_fromUtf8("lowUpper"))
        self.cutoffLabel = QtGui.QLabel(MHCVAMUnicefIndicatorsDialog)
        self.cutoffLabel.setGeometry(QtCore.QRect(190, 190, 271, 17))
        self.cutoffLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.cutoffLabel.setObjectName(_fromUtf8("cutoffLabel"))
        self.mediumLower = QtGui.QLineEdit(MHCVAMUnicefIndicatorsDialog)
        self.mediumLower.setGeometry(QtCore.QRect(250, 250, 91, 21))
        self.mediumLower.setObjectName(_fromUtf8("mediumLower"))
        self.mediumLabel = QtGui.QLabel(MHCVAMUnicefIndicatorsDialog)
        self.mediumLabel.setGeometry(QtCore.QRect(180, 250, 58, 21))
        self.mediumLabel.setObjectName(_fromUtf8("mediumLabel"))
        self.mediumUpper = QtGui.QLineEdit(MHCVAMUnicefIndicatorsDialog)
        self.mediumUpper.setGeometry(QtCore.QRect(370, 250, 91, 21))
        self.mediumUpper.setObjectName(_fromUtf8("mediumUpper"))
        self.mediumTo = QtGui.QLabel(MHCVAMUnicefIndicatorsDialog)
        self.mediumTo.setGeometry(QtCore.QRect(340, 250, 31, 21))
        self.mediumTo.setAlignment(QtCore.Qt.AlignCenter)
        self.mediumTo.setObjectName(_fromUtf8("mediumTo"))
        self.highLower = QtGui.QLineEdit(MHCVAMUnicefIndicatorsDialog)
        self.highLower.setGeometry(QtCore.QRect(250, 280, 91, 21))
        self.highLower.setObjectName(_fromUtf8("highLower"))
        self.highLabel = QtGui.QLabel(MHCVAMUnicefIndicatorsDialog)
        self.highLabel.setGeometry(QtCore.QRect(180, 280, 58, 21))
        self.highLabel.setObjectName(_fromUtf8("highLabel"))
        self.highUpper = QtGui.QLineEdit(MHCVAMUnicefIndicatorsDialog)
        self.highUpper.setGeometry(QtCore.QRect(370, 280, 91, 21))
        self.highUpper.setObjectName(_fromUtf8("highUpper"))
        self.highTo = QtGui.QLabel(MHCVAMUnicefIndicatorsDialog)
        self.highTo.setGeometry(QtCore.QRect(340, 280, 31, 21))
        self.highTo.setAlignment(QtCore.Qt.AlignCenter)
        self.highTo.setObjectName(_fromUtf8("highTo"))
        self.label = QtGui.QLabel(MHCVAMUnicefIndicatorsDialog)
        self.label.setGeometry(QtCore.QRect(600, 340, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(5)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.logopgs = QtGui.QLabel(MHCVAMUnicefIndicatorsDialog)
        self.logopgs.setGeometry(QtCore.QRect(220, 340, 51, 51))
        self.logopgs.setText(_fromUtf8(""))
        self.logopgs.setPixmap(QtGui.QPixmap(_fromUtf8("img/logos/pgs-logo.png")))
        self.logopgs.setObjectName(_fromUtf8("logopgs"))
        self.logounicef = QtGui.QLabel(MHCVAMUnicefIndicatorsDialog)
        self.logounicef.setGeometry(QtCore.QRect(10, 340, 201, 51))
        self.logounicef.setText(_fromUtf8(""))
        self.logounicef.setPixmap(QtGui.QPixmap(_fromUtf8("img/logos/unicef-logo.png")))
        self.logounicef.setObjectName(_fromUtf8("logounicef"))

        self.retranslateUi(MHCVAMUnicefIndicatorsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MHCVAMUnicefIndicatorsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MHCVAMUnicefIndicatorsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(MHCVAMUnicefIndicatorsDialog)

    def retranslateUi(self, MHCVAMUnicefIndicatorsDialog):
        MHCVAMUnicefIndicatorsDialog.setWindowTitle(_translate("MHCVAMUnicefIndicatorsDialog", "MHCVAM using UNICEF Indicators (BARANGAY)", None))
        self.layerLabel.setText(_translate("MHCVAMUnicefIndicatorsDialog", "Barangay Layer with UNICEF Indicators", None))
        self.fieldLabel.setText(_translate("MHCVAMUnicefIndicatorsDialog", "UNICEF Indicator", None))
        self.agencyLabel.setText(_translate("MHCVAMUnicefIndicatorsDialog", "Limit By Agency", None))
        self.orLabel.setText(_translate("MHCVAMUnicefIndicatorsDialog", "or", None))
        self.categoryLabel.setText(_translate("MHCVAMUnicefIndicatorsDialog", "Limit By Category", None))
        self.lowLabel.setText(_translate("MHCVAMUnicefIndicatorsDialog", "Low", None))
        self.lowTo.setText(_translate("MHCVAMUnicefIndicatorsDialog", "to", None))
        self.cutoffLabel.setText(_translate("MHCVAMUnicefIndicatorsDialog", "INDICATOR CUT-OFFS", None))
        self.mediumLabel.setText(_translate("MHCVAMUnicefIndicatorsDialog", "Medium", None))
        self.mediumTo.setText(_translate("MHCVAMUnicefIndicatorsDialog", "to", None))
        self.highLabel.setText(_translate("MHCVAMUnicefIndicatorsDialog", "High", None))
        self.highTo.setText(_translate("MHCVAMUnicefIndicatorsDialog", "to", None))
        self.label.setText(_translate("MHCVAMUnicefIndicatorsDialog", "This plugin was made possible due to the efforts of the United Nations Children\'s Fund (UNICEF) and the Philippine Geographical Society (PGS).", None))

from qgis import gui
