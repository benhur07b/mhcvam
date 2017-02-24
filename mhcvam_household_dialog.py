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
 mhcvam_household_dialog.py

 Contains the logic for the household-level analysis
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

from mhcvam_library import *

from mhcvam_household_dialog_form import Ui_MHCVAMHouseholdDialog

indicators = Indicators()


class MHCVAMHouseholdDialog(QDialog, Ui_MHCVAMHouseholdDialog):

    def __init__(self, parent=None, iface=None):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        self.setWindowTitle(self.tr('Household-level Analysis'))
        self.iface = iface

        QObject.connect(self.selectHHButtonBox, SIGNAL("accepted()"), self.run_select)
        QObject.connect(self.summHHButtonBox, SIGNAL("accepted()"), self.run_summary)

        self.agencyComboBox.addItems(indicators.agencies_list)
        self.categoryComboBox.addItems(indicators.categories_list)

        QObject.connect(self.selectHazardComboBox,
                        SIGNAL("currentIndexChanged(QString)"),
                        self.set_hazard)

        QObject.connect(self.summHHComboBox,
                        SIGNAL("currentIndexChanged(QString)"),
                        self.set_brgy)

        QObject.connect(self.agencyComboBox,
                        SIGNAL("currentIndexChanged(QString)"),
                        self.set_fields_from_agency)

        QObject.connect(self.categoryComboBox,
                        SIGNAL("currentIndexChanged(QString)"),
                        self.set_fields_from_category)

        self.set_hazard()
        self.set_brgy()


    def set_hazard(self):

        selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.selectHazardComboBox.currentText())[0]
        self.selectHazardTypeComboBox.setLayer(selectedLayer)

    def set_brgy(self):
        lyr = QgsMapLayerRegistry.instance().mapLayersByName(self.summHHBrgyComboBox.currentText())[0]
        self.brgyFieldComboBox.setLayer(lyr)


    def set_fields_from_agency(self):

        self.fieldComboBox.clear()

        selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.summHHComboBox.currentText())[0]
        layerFields = [field.name() for field in selectedLayer.fields().toList()]
        agencyFields = indicators.agencies_with_indicators_list[self.agencyComboBox.currentIndex()][1]

        fields = list(set(layerFields).intersection(agencyFields))
        self.fieldComboBox.addItems(fields)
        self.categoryComboBox.setCurrentIndex(0)


    def set_fields_from_category(self):

        self.fieldComboBox.clear()

        selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.summHHComboBox.currentText())[0]
        layerFields = [field.name() for field in selectedLayer.fields().toList()]
        categoryFields = indicators.categories_with_indicators_list[self.categoryComboBox.currentIndex()][1]

        fields = list(set(layerFields).intersection(categoryFields))
        self.fieldComboBox.addItems(fields)
        self.agencyComboBox.setCurrentIndex(0)


    def run_select(self):

        hh = QgsMapLayerRegistry.instance().mapLayersByName(self.selectHHComboBox.currentText())[0]
        hazard = QgsMapLayerRegistry.instance().mapLayersByName(self.selectHazardComboBox.currentText())[0]
        hazardType = self.selectHazardTypeComboBox.currentText()
        hazardLevel = self.selectHazardLevelComboBox.currentText()
        outputname = self.selectOutputNameLineEdit.text()

        processing.runandload("qgis:joinattributesbylocation", hh, hazard, u"intersects", 0.00000, 0, "mean", 0, "memory:")
        outlayer = QgsMapLayerRegistry.instance().mapLayersByName("Joined layer")[0]

        outlayer.setLayerName(outputname)

        hazardLevels = []

        if hazardLevel == "Low":
            hazardLevels = [("Low", "Low", "cyan")]

        elif hazardLevel == "Medium":
            hazardLevels = [("Medium", "Medium", "orange")]

        elif hazardLevel == "High":
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

        if self.selectSummaryCheckBox.isChecked():
            hazardLevelCount = []
            features = outlayer.getFeatures()
            for f in features:
                attr = f.attributes()
                hazardLevelCount.append(attr[outlayer.fieldNameIndex(hazardType)])

            numlows = hazardLevelCount.count("Low")
            nummeds = hazardLevelCount.count("Medium")
            numhigh = hazardLevelCount.count("High")

            hh_per_hazard = "Households in Hazard Level\nLow: {}\nMedium: {}\nHigh: {}".format(numlows, nummeds, numhigh)
            msg = hh_per_hazard
            QMessageBox.information(self.iface.mainWindow(), "SUMMARY REPORT", msg)


    def run_summary(self):

        hh = QgsMapLayerRegistry.instance().mapLayersByName(self.summHHComboBox.currentText())[0]
        brgy = QgsMapLayerRegistry.instance().mapLayersByName(self.summHHBrgyComboBox.currentText())[0]
        brgyField = self.brgyFieldComboBox.currentText()
        statField = self.fieldComboBox.currentText()
        statField0 = get_field(hh, statField)
        stat = self.statComboBox.currentText()

        processing.runandload("qgis:joinattributesbylocation", hh, brgy, u"intersects", 0.00000, 0, "mean", 0, "memory:")
        hhbrgy = QgsMapLayerRegistry.instance().mapLayersByName("Joined layer")[0]
        hhbrgy.setLayerName("hhbrgy")

        fieldList = get_list_of_fields(hhbrgy, [brgyField, statField])
        brgys = list(set(b[0] for b in fieldList))

        brgyDict = {}

        for b in brgys:
            brgyDict[b] = []

        for f in fieldList:
            brgyDict[f[0]].append(f[1])

        QgsMapLayerRegistry.instance().removeMapLayers([hhbrgy.id()])

        copy_vector_layer(brgy, "{} ({})".format(stat, statField))
        out1 = QgsMapLayerRegistry.instance().mapLayersByName("{} ({})".format(stat, statField))[0]

        res = out1.dataProvider().addAttributes([QgsField(stat, statField0.type())])
        out1.updateFields()

        statIndex = out1.fieldNameIndex(stat)
        brgyIndex = out1.fieldNameIndex(brgyField)

        if stat == "SUM":
            features = out1.getFeatures()
            for f in features:
                try:
                    out1.startEditing()
                    attr = f.attributes()
                    f[statIndex] = sum(brgyDict[attr[brgyIndex]])
                    out1.updateFeature(f)
                except KeyError:
                    pass

        if stat == "MEAN":
            features = out1.getFeatures()
            for f in features:
                try:
                    out1.startEditing()
                    attr = f.attributes()
                    f[statIndex] = round(1.0*sum(brgyDict[attr[brgyIndex]])/len(brgyDict[attr[brgyIndex]]), 2)
                    out1.updateFeature(f)
                except KeyError:
                    pass

        if stat == "MIN":
            features = out1.getFeatures()
            for f in features:
                try:
                    out1.startEditing()
                    attr = f.attributes()
                    f[statIndex] = min(brgyDict[attr[brgyIndex]])
                    out1.updateFeature(f)
                except KeyError:
                    pass

        if stat == "MAX":
            features = out1.getFeatures()
            for f in features:
                try:
                    out1.startEditing()
                    attr = f.attributes()
                    f[statIndex] = max(brgyDict[attr[brgyIndex]])
                    out1.updateFeature(f)
                except KeyError:
                    pass

        if stat == "PERCENTAGE":
            sumDict = {}
            total = 0
            features = out1.getFeatures()
            for f in features:
                try:
                    attr = f.attributes()
                    sumDict[attr[brgyIndex]] = sum(brgyDict[attr[brgyIndex]])
                    total += sum(brgyDict[attr[brgyIndex]])
                except KeyError:
                    pass

            features2 = out1.getFeatures()
            for f in features2:
                try:
                    out1.startEditing()
                    attr = f.attributes()
                    f[statIndex] = round(100.0*sumDict[attr[brgyIndex]]/total, 2)
                    out1.updateFeature(f)
                except KeyError:
                    pass

        out1.commitChanges()

        if self.labelCheckBox.isChecked():
            add_labels(out1, stat)

        if self.symCheckBox.isChecked():
            pass
