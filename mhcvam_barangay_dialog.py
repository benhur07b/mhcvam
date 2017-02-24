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
 mhcvam_barangay_dialog.py

 Contains the logic for the barangay-level analysis
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

from mhcvam_barangay_dialog_form import Ui_MHCVAMBarangayDialog

indicators = Indicators()

class MHCVAMBarangayDialog(QDialog, Ui_MHCVAMBarangayDialog):

    def __init__(self, parent=None, iface=None):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        self.setWindowTitle(self.tr('Barangay-level Analysis'))
        self.iface = iface

        QObject.connect(self.summBrgyButtonBox, SIGNAL("accepted()"), self.run_summary)

        self.agencyComboBox.addItems(indicators.agencies_list)
        self.categoryComboBox.addItems(indicators.categories_list)

        QObject.connect(self.summBrgyComboBox,
                        SIGNAL("currentIndexChanged(QString)"),
                        self.set_muni)

        QObject.connect(self.agencyComboBox,
                        SIGNAL("currentIndexChanged(QString)"),
                        self.set_fields_from_agency)

        QObject.connect(self.categoryComboBox,
                        SIGNAL("currentIndexChanged(QString)"),
                        self.set_fields_from_category)

        self.set_muni()


    def set_muni(self):
        lyr = QgsMapLayerRegistry.instance().mapLayersByName(self.summBrgyComboBox.currentText())[0]
        self.muniFieldComboBox.setLayer(lyr)


    def set_fields_from_agency(self):

        self.fieldComboBox.clear()

        selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.summBrgyComboBox.currentText())[0]
        layerFields = [field.name() for field in selectedLayer.fields().toList()]
        agencyFields = indicators.agencies_with_indicators_list[self.agencyComboBox.currentIndex()][1]

        fields = list(set(layerFields).intersection(agencyFields))
        self.fieldComboBox.addItems(fields)
        self.categoryComboBox.setCurrentIndex(0)


    def set_fields_from_category(self):

        self.fieldComboBox.clear()

        selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.summBrgyComboBox.currentText())[0]
        layerFields = [field.name() for field in selectedLayer.fields().toList()]
        categoryFields = indicators.categories_with_indicators_list[self.categoryComboBox.currentIndex()][1]

        fields = list(set(layerFields).intersection(categoryFields))
        self.fieldComboBox.addItems(fields)
        self.agencyComboBox.setCurrentIndex(0)


    def run_summary(self):

        brgy = QgsMapLayerRegistry.instance().mapLayersByName(self.summBrgyComboBox.currentText())[0]
        muniField = self.muniFieldComboBox.currentText()
        statField = self.fieldComboBox.currentText()
        statField0 = get_field(brgy, statField)
        dissolveField = get_field(brgy, muniField)
        stat = self.statComboBox.currentText()

        fieldList = get_list_of_fields(brgy, [muniField, statField])
        munis = list(set([m[0] for m in fieldList]))

        munisDict = {}

        for m in munis:
            munisDict[m] = []

        for f in fieldList:
            munisDict[f[0]].append(f[1])

        processing.runandload("qgis:dissolve", brgy, False, muniField, "memory:")
        out1 = QgsMapLayerRegistry.instance().mapLayersByName("Dissolved")[0]

        res = out1.dataProvider().addAttributes([QgsField(stat, statField0.type())])
        out1.updateFields()

        statIndex = out1.fieldNameIndex(stat)
        muniIndex = out1.fieldNameIndex(muniField)

        if stat == "SUM":
            features = out1.getFeatures()
            for f in features:
                out1.startEditing()
                attr = f.attributes()
                f[statIndex] = sum(munisDict[attr[muniIndex]])
                out1.updateFeature(f)

        if stat == "MEAN":
            features = out1.getFeatures()
            for f in features:
                out1.startEditing()
                attr = f.attributes()
                f[statIndex] = round(1.0*sum(munisDict[attr[muniIndex]])/len(munisDict[attr[muniIndex]]), 2)
                out1.updateFeature(f)

        if stat == "MIN":
            features = out1.getFeatures()
            for f in features:
                out1.startEditing()
                attr = f.attributes()
                f[statIndex] = min(munisDict[attr[muniIndex]])
                out1.updateFeature(f)

        if stat == "MAX":
            features = out1.getFeatures()
            for f in features:
                out1.startEditing()
                attr = f.attributes()
                f[statIndex] = min(munisDict[attr[muniIndex]])
                out1.updateFeature(f)

        if stat == "PERCENTAGE":
            sumDict = {}
            total = 0
            features = out1.getFeatures()
            for f in features:
                attr = f.attributes()
                sumDict[attr[muniIndex]] = sum(munisDict[attr[muniIndex]])
                total += sum(munisDict[attr[muniIndex]])

            features2 = out1.getFeatures()
            for f in features2:
                out1.startEditing()
                attr = f.attributes()
                f[statIndex] = round(100.0*sumDict[attr[muniIndex]]/total, 2)
                out1.updateFeature(f)

        out1.commitChanges()

        processing.runandload("qgis:deleteholes", out1, "memory:")
        out2 = QgsMapLayerRegistry.instance().mapLayersByName("Cleaned")[0]
        out2.setLayerName("{} ({})".format(stat, statField))
        QgsMapLayerRegistry.instance().removeMapLayers([out1.id()])

        if self.labelCheckBox.isChecked():
            add_labels(out2, stat)

        if self.symCheckBox.isChecked():
            pass
