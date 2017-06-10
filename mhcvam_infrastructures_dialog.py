# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Multi-Hazard Child Vulnerability Analysis and Mapping Plugin

 A QGIS plugin that performs Multi-Hazard Child Vulnerability Analysis
 and Mapping using Different Indicators

        begin                   : 2017-01-03
        copyright               : (C) 2017 by Ben Hur S. Pintor
        email                   : bhs.pintor@gmail.com
        git sha                 : $Format:%H$
***************************************************************************/

/***************************************************************************
 mhcvam_infrastructures_dialog.py

 Contains the logic for the infrastructures risk analysis
***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 """

__author__ = 'Ben Hur S. Pintor <bhs.pintor@gmail.com>'
__date__ = '01/03/2017'

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from qgis.core import *
import os
import processing

from mhcvam_infrastructures_dialog_form import Ui_MHCVAMInfrastructuresDialog

# try to solve UnicodeEncodeError in WIN
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MHCVAMInfrastructuresDialog(QDialog, Ui_MHCVAMInfrastructuresDialog):

    def __init__(self, parent=None, iface=None):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        self.setWindowTitle(self.tr('Infrastructures Risk Analysis'))
        self.iface = iface

        # Set the response of the OK buttons
        QObject.connect(self.infraInHazardButtonBox, SIGNAL("accepted()"), self.run_infra)
        QObject.connect(self.infraInBrgyButtonBox, SIGNAL("accepted()"), self.run_brgy)

        self.set_hazard()
        self.set_infra_hazard()
        self.set_brgy()

        # If the selected layer changes, change the options for the fields too
        QObject.connect(self.hazardLayerComboBox,
                        SIGNAL("currentIndexChanged(QString)"),
                        self.set_hazard)

        QObject.connect(self.infraWithHazardComboBox,
                        SIGNAL("currentIndexChanged(QString)"),
                        self.set_infra_hazard)

        QObject.connect(self.brgyLayerComboBox,
                        SIGNAL("currentIndexChanged(QString)"),
                        self.set_brgy)


    def set_hazard(self):

        selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.hazardLayerComboBox.currentText())[0]
        self.hazardTypeComboBox.setLayer(selectedLayer)


    def set_infra_hazard(self):

        selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.infraWithHazardComboBox.currentText())[0]
        self.hazardTypeComboBox_2.setLayer(selectedLayer)


    def set_brgy(self):

        selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.brgyLayerComboBox.currentText())[0]
        self.brgyNamesComboBox.setLayer(selectedLayer)


    def run_infra(self):

        #Get Layers and Values in ComboBoxes
        infra = QgsMapLayerRegistry.instance().mapLayersByName(self.infraLayerComboBox.currentText())[0]
        hazard = QgsMapLayerRegistry.instance().mapLayersByName(self.hazardLayerComboBox.currentText())[0]
        hazardType = self.hazardTypeComboBox.currentText()
        hazardLevel = self.hazardLevelComboBox.currentText()
        outputname = self.outputNameLineEdit.text()
        summary = self.summaryCheckBox.isChecked()

        outlayer = ""

        if infra.geometryType() == 1:
            processing.runandload("qgis:multiparttosingleparts", infra, "memory:")
            outlayer0 = QgsMapLayerRegistry.instance().mapLayersByName("Single parts")[0]
            processing.runandload("qgis:intersection", outlayer0, hazard, False, "memory:")
            outlayer = QgsMapLayerRegistry.instance().mapLayersByName("Intersection")[0]
            outlayer.setLayerName(outputname)

            QgsMapLayerRegistry.instance().removeMapLayers([outlayer0.id()])

        else:
            processing.runandload("qgis:joinattributesbylocation", infra, hazard, u"intersects", 0.00000, 0, "mean", 0, "memory:")
            outlayer = QgsMapLayerRegistry.instance().mapLayersByName("Joined layer")[0]
            outlayer.setLayerName(outputname)

        hazardLevels = []

        if hazardLevel.capitalize() == "Low":
            hazardLevels = [("Low", "Low", "cyan")]

        elif hazardLevel.capitalize() == "Medium":
            hazardLevels = [("Medium", "Medium", "orange")]

        elif hazardLevel.capitalize() == "High":
            hazardLevels = [("High", "High", "red")]

        else:
            hazardLevels = [("Low", "Low", "cyan"),
                            ("Medium", "Medium", "orange"),
                            ("High", "High", "red")]

        categories = []

        for h, label, color in hazardLevels:

            sym = QgsSymbolV2.defaultSymbol(outlayer.geometryType())
            sym.setColor(QColor(color))
            cats = QgsRendererCategoryV2(h, sym, "{} ({})".format(label, hazardType))
            categories.append(cats)

        renderer = QgsCategorizedSymbolRendererV2(hazardType, categories)

        outlayer.setRendererV2(renderer)

        outlayer.triggerRepaint()

        if self.summaryCheckBox.isChecked():
            hazardLevelCount = []
            features = outlayer.getFeatures()
            for f in features:
                attr = f.attributes()
                hazardLevelCount.append(attr[outlayer.fieldNameIndex(hazardType)])

            numlows = hazardLevelCount.count("Low")
            nummeds = hazardLevelCount.count("Medium")
            numhigh = hazardLevelCount.count("High")

            infra_per_hazard = "Infrastructures per Hazard Level\nLow: {}\nMedium: {}\nHigh: {}".format(numlows, nummeds, numhigh)
            msg = infra_per_hazard
            QMessageBox.information(self.iface.mainWindow(), "SUMMARY REPORT", msg)


    def run_brgy(self):

        #Get Layers and Values in ComboBoxes
        infraWithHazard = QgsMapLayerRegistry.instance().mapLayersByName(self.infraWithHazardComboBox.currentText())[0]
        brgy = QgsMapLayerRegistry.instance().mapLayersByName(self.brgyLayerComboBox.currentText())[0]
        hazardType = self.hazardTypeComboBox_2.currentText()
        brgyNames = self.brgyNamesComboBox.currentText()
        outputname = self.brgyOutputNameLineEdit.text()
        toLabel = self.hazardLeveltoLabelComboBox.currentText()

        #Get intersection of infra-hazard with barangays
        self.add_hazard_count_to_brgy(infraWithHazard, brgy, brgyNames, hazardType, outputname)

        outLayer = QgsMapLayerRegistry.instance().mapLayersByName(outputname)[0]

        if self.labelCheckBox.isChecked():
            self.add_labels(outLayer, toLabel)

        if self.symCheckBox.isChecked():
            field = ""
            if toLabel == "Low":
                field = "NUM_LOW"
            elif toLabel == "Medium":
                field = "NUM_MED"
            elif toLabel == "High":
                field = "NUM_HIGH"
            else:
                field = "NUM_TOTAL"

            indicator = [("0", 0, 0, "white"),
                         ("1 to 5", 1, 5, "cyan"),
                         ("6 to 10", 6, 10, "orange"),
                         ("Greater than 10", 11, 999999, "red")]

            ranges = []

            for label, lower, upper, color in indicator:

                sym = QgsSymbolV2.defaultSymbol(outLayer.geometryType())
                sym.setColor(QColor(color))
                rng = QgsRendererRangeV2(lower, upper, sym, "{} ({})".format(label, toLabel))
                ranges.append(rng)

            renderer = QgsGraduatedSymbolRendererV2(field, ranges)

            outLayer.setRendererV2(renderer)

            outLayer.triggerRepaint()


    def count_hazard_level_per_barangay(self, infraWithHazard, brgy, brgyNames, hazardType):

        names0 = []
        brgyDict = {}

        processing.runandload("qgis:joinattributesbylocation", infraWithHazard, brgy, u"intersects", 0.00000, 0, "max", 1, "memory:")
        out1 = QgsMapLayerRegistry.instance().mapLayersByName("Joined layer")[0]

        brgyNameIndex = out1.fieldNameIndex(brgyNames)
        hazardTypeIndex = out1.fieldNameIndex(hazardType)

        features = out1.getFeatures()
        for f in features:
            try:
                attr = f.attributes()
                names0.append(str(attr[brgyNameIndex]))

            except IndexError:
                pass

        names = list(set(names0))

        for n in names:
            brgyDict[n] = [0,0,0]

        features2 = out1.getFeatures()
        for f in features2:
            try:
                attr = f.attributes()
                brgyName = str(attr[brgyNameIndex])
                hazardLevel = str(attr[hazardTypeIndex])

                if hazardlevel.capitalize() == "Low":
                    brgyDict[brgyName][0] += 1

                elif hazardlevel.capitalize() == "Medium":
                    brgyDict[brgyName][1] += 1

                elif hazardlevel.capitalize() == "High":
                    brgyDict[brgyName][2] += 1

            except IndexError:
                pass

        #toRemove = QgsMapLayerRegistry.instance().mapLayersByName("Joined layer")[0]
        QgsMapLayerRegistry.instance().removeMapLayers([out1.id()])

        return brgyDict


    def add_hazard_count_to_brgy(self, infraWithHazard, brgy, brgyNames, hazardType, outputname):

        brgyDict = self.count_hazard_level_per_barangay(infraWithHazard, brgy, brgyNames, hazardType)

        self.copy_vector_layer(brgy, outputname)
        inter = QgsMapLayerRegistry.instance().mapLayersByName(outputname)[0]
        numfields = len(brgy.fields().toList())

        res = inter.dataProvider().addAttributes([QgsField("NUM_LOW", QVariant.Int),
                                                  QgsField("NUM_MED", QVariant.Int),
                                                  QgsField("NUM_HIGH", QVariant.Int),
                                                  QgsField("NUM_TOTAL", QVariant.Int)])

        inter.updateFields()

        brgyNameIndex = inter.fieldNameIndex(brgyNames)
        numLowIndex = inter.fieldNameIndex("NUM_LOW")
        numMedIndex = inter.fieldNameIndex("NUM_MED")
        numHighIndex = inter.fieldNameIndex("NUM_HIGH")
        numTotalIndex = inter.fieldNameIndex("NUM_TOTAL")

        features = inter.getFeatures()
        for f in features:
            inter.startEditing()
            attr = f.attributes()
            try:
                brgyName = str(attr[brgyNameIndex])
                f[numLowIndex] = brgyDict[brgyName][0]
                f[numMedIndex] = brgyDict[brgyName][1]
                f[numHighIndex] = brgyDict[brgyName][2]
                f[numTotalIndex] = brgyDict[brgyName][0] + brgyDict[brgyName][1] + brgyDict[brgyName][2]
                inter.updateFeature(f)

            except KeyError:
                f[numLowIndex] = 0
                f[numMedIndex] = 0
                f[numHighIndex] = 0
                f[numTotalIndex] = 0
                inter.updateFeature(f)

        inter.commitChanges()


    def add_labels(self, lyr, toLabel):

        symbol = lyr.rendererV2().symbols()[0]
        symbol.setColor(QColor(243,226,138))
        lyr.triggerRepaint()

        palyr = QgsPalLayerSettings()
        palyr.readFromLayer(lyr)
        palyr.enabled = True

        if toLabel == "Low":
            palyr.fieldName = 'NUM_LOW'

        elif toLabel == "Medium":
            palyr.fieldName = 'NUM_MED'

        elif toLabel == "High":
            palyr.fieldName = 'NUM_HIGH'

        else:
            palyr.fieldName = 'NUM_TOTAL'

        palyr.placement = QgsPalLayerSettings.OverPoint
        palyr.fontSizeInMapUnits = False
        palyr.textFont.setPointSize(10)
        palyr.textColor = QColor(0,0,0)
        palyr.writeToLayer(lyr)


    def copy_vector_layer(self, inlyr, outputname):
        features = [f for f in inlyr.getFeatures()]

        copylyr = QgsVectorLayer("Polygon?crs={}".format(inlyr.crs().authid().lower()), outputname, "memory")

        data = copylyr.dataProvider()
        attr = inlyr.dataProvider().fields().toList()
        data.addAttributes(attr)
        copylyr.updateFields()
        data.addFeatures(features)

        QgsMapLayerRegistry.instance().addMapLayer(copylyr)
