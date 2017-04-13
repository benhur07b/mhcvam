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

 Contains the logic for the Barangay-level Hazard and Vulnerability Analysis
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

indicators_path_brgy = os.path.dirname(__file__) + '/indicators_barangay.csv'

indicators = Indicators(indicators_path_brgy)


# try to solve UnicodeEncodeError in WIN
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')


class MHCVAMBarangayDialog(QDialog, Ui_MHCVAMBarangayDialog):

    def __init__(self, parent=None, iface=None):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        self.setWindowTitle(self.tr('Barangay-level Hazard and Vulnerability Analysis'))
        self.iface = iface

        QObject.connect(self.queryBrgyButtonBox, SIGNAL("accepted()"), self.run_query)
        QObject.connect(self.queryBrgyButtonBox.button(QDialogButtonBox.Reset), SIGNAL("clicked()"), self.reset_selection)
        QObject.connect(self.queryFieldAdd, SIGNAL("clicked()"), self.add_field_to_query)
        QObject.connect(self.uniqueValuesButton, SIGNAL("clicked()"), self.get_unique_field_values)
        QObject.connect(self.queryValueAdd, SIGNAL("clicked()"), self.add_value_to_query)
        QObject.connect(self.queryFunctionAdd, SIGNAL("clicked()"), self.add_function_to_query)
        QObject.connect(self.summBrgyButtonBox, SIGNAL("accepted()"), self.run_summary)


        self.agencyComboBox.addItems(indicators.agencies_list)
        self.queryAgencyComboBox.addItems(indicators.agencies_list)

        # Uncomment below if you need Limit by Category (Must Edit GUI)
        # self.categoryComboBox.addItems(indicators.categories_list)
        # self.queryCategoryComboBox.addItems(indicators.categories_list)

        QObject.connect(self.queryBrgyComboBox,
                        SIGNAL("currentIndexChanged(QString)"),
                        self.change_brgy_layer_query)

        QObject.connect(self.summBrgyComboBox,
                        SIGNAL("currentIndexChanged(QString)"),
                        self.set_muni_summary)

        QObject.connect(self.agencyComboBox,
                        SIGNAL("currentIndexChanged(QString)"),
                        self.set_fields_from_agency)

        QObject.connect(self.queryAgencyComboBox,
                        SIGNAL("currentIndexChanged(QString)"),
                        self.set_fields_from_agency_query)


        # Uncomment below if you need Limit by Category (Must Edit GUI)
        # QObject.connect(self.categoryComboBox,
        #                 SIGNAL("currentIndexChanged(QString)"),
        #                 self.set_fields_from_category)

        # QObject.connect(self.queryCategoryComboBox,
        #                 SIGNAL("currentIndexChanged(QString)"),
        #                 self.set_fields_from_category_query)

        self.set_muni_summary()


    def set_muni_summary(self):
        lyr = QgsMapLayerRegistry.instance().mapLayersByName(self.summBrgyComboBox.currentText())[0]
        self.muniFieldComboBox.setLayer(lyr)


    def set_fields_from_agency(self):

        self.fieldComboBox.clear()
        self.uniqueValuesListWidget.clear()

        selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.summBrgyComboBox.currentText())[0]
        layerFields = [field.name() for field in selectedLayer.fields().toList()]
        agencyFields = indicators.agencies_with_indicators_list[self.agencyComboBox.currentIndex()][1]

        fields = list(set(layerFields).intersection(agencyFields))
        fieldnames = [indicators.get_indicator_name_from_code(f) for f in fields]
        self.fieldComboBox.addItems(fieldnames)
        # self.categoryComboBox.setCurrentIndex(0)


    def set_fields_from_agency_query(self):

        self.queryFieldComboBox.clear()
        self.uniqueValuesListWidget.clear()

        selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.queryBrgyComboBox.currentText())[0]
        layerFields = [field.name() for field in selectedLayer.fields().toList()]
        agencyFields = indicators.agencies_with_indicators_list[self.queryAgencyComboBox.currentIndex()][1]

        fields = list(set(layerFields).intersection(agencyFields))
        fieldnames = [indicators.get_indicator_name_from_code(f) for f in fields]
        self.queryFieldComboBox.addItems(fieldnames)
        # self.queryCategoryComboBox.setCurrentIndex(0)


    # Uncomment below if you need Limit by Category (Must Edit GUI)
    # def set_fields_from_category(self):
    #
    #     self.fieldComboBox.clear()
    #
    #     selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.summBrgyComboBox.currentText())[0]
    #     layerFields = [field.name() for field in selectedLayer.fields().toList()]
    #     categoryFields = indicators.categories_with_indicators_list[self.categoryComboBox.currentIndex()][1]
    #
    #     fields = list(set(layerFields).intersection(categoryFields))
    #     fieldnames = [indicators.get_indicator_name_from_code(f) for f in fields]
    #     self.fieldComboBox.addItems(fieldnames)
    #     self.agencyComboBox.setCurrentIndex(0)


    # def set_fields_from_category_query(self):
    #
    #     self.queryFieldComboBox.clear()
    #
    #     selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.queryBrgyComboBox.currentText())[0]
    #     layerFields = [field.name() for field in selectedLayer.fields().toList()]
    #     categoryFields = indicators.categories_with_indicators_list[self.queryCategoryComboBox.currentIndex()][1]
    #
    #     fields = list(set(layerFields).intersection(categoryFields))
    #     fieldnames = [indicators.get_indicator_name_from_code(f) for f in fields]
    #     self.queryFieldComboBox.addItems(fieldnames)
    #     self.queryAgencyComboBox.setCurrentIndex(0)


    def change_brgy_layer_query(self):

        # self.reset_selection()
        self.queryFieldComboBox.clear()
        self.queryAgencyComboBox.setCurrentIndex(0)
        self.queryFunctionComboBox.setCurrentIndex(0)
        self.queryTextEdit.clear()
        self.uniqueValuesListWidget.clear()


    def add_field_to_query(self):

        # self.queryTextEdit.insertPlainText(' "{}" '.format(indicators.get_indicator_name_from_code(self.queryFieldComboBox.currentText())))
        self.queryTextEdit.insertPlainText(' "{}" '.format(self.queryFieldComboBox.currentText()))


    def get_unique_field_values(self):

        self.uniqueValuesListWidget.clear()

        brgy = QgsMapLayerRegistry.instance().mapLayersByName(self.queryBrgyComboBox.currentText())[0]
        fieldName = self.queryFieldComboBox.currentText()
        fieldCode = indicators.get_indicator_code_from_name(fieldName)
        fieldIndex = brgy.fieldNameIndex(fieldCode)
        fields = []

        features = brgy.getFeatures()
        for f in features:
            attr = f.attributes()
            fields.append(attr[fieldIndex])

        ufields = list(set([str(f) for f in fields]))
        ufields.sort()
        self.uniqueValuesListWidget.addItems(ufields)


    def add_value_to_query(self):

        self.queryTextEdit.insertPlainText(' {} '.format(self.uniqueValuesListWidget.currentItem().text()))


    def add_function_to_query(self):

        self.queryTextEdit.insertPlainText(' {} '.format(self.queryFunctionComboBox.currentText()))


    def reset_selection(self):

        # Only resets the selection of the current layer in the Barangay ComboBox
        brgy = QgsMapLayerRegistry.instance().mapLayersByName(self.queryBrgyComboBox.currentText())[0]
        brgy.removeSelection()
        brgy.setSubsetString('')    # remove feature filter
        self.queryFieldComboBox.clear()
        self.queryAgencyComboBox.setCurrentIndex(0)
        self.queryFunctionComboBox.setCurrentIndex(0)
        self.queryTextEdit.clear()
        self.uniqueValuesListWidget.clear()


    def run_query(self):
        """This version performs a feature filter before selection"""

        brgy = QgsMapLayerRegistry.instance().mapLayersByName(self.queryBrgyComboBox.currentText())[0]
        text = self.queryTextEdit.toPlainText()
        q = indicators.convert_to_query(text)
        query = unicode(q)
        brgy.setSubsetString(query)     # apply feature filter
        r = QgsFeatureRequest().setFilterExpression(query)
        sel = brgy.getFeatures(r)
        brgy.setSelectedFeatures([f.id() for f in sel])


    # def run_query(self):
    #
    #     brgy = QgsMapLayerRegistry.instance().mapLayersByName(self.queryBrgyComboBox.currentText())[0]
    #     text = self.queryTextEdit.toPlainText()
    #     q = indicators.convert_to_query(text)
    #     query = unicode(q)
    #     r = QgsFeatureRequest().setFilterExpression(query)
    #     sel = brgy.getFeatures(r)
    #     brgy.setSelectedFeatures([f.id() for f in sel])


    # def convert_to_query(self, text):
    #
    #     text.replace("greater than or equal to", ">=")
    #     text.replace("less than or equal to", "<=")
    #     text.replace("not equal to", "!=")
    #     text.replace("equal to", "=")
    #     text.replace("greater than", ">")
    #     text.replace("less than", "<")
    #
    #     text = text.replace("equal to", "=")
    #     text = text.replace(" or ", "")
    #     text = text.replace("not ", "!")
    #     text = text.replace("greater than", ">")
    #     text = text.replace("less than", "<")
    #
    #     return text


    def run_summary(self):

        brgy = QgsMapLayerRegistry.instance().mapLayersByName(self.summBrgyComboBox.currentText())[0]
        muniField = self.muniFieldComboBox.currentText()
        statFieldName = self.fieldComboBox.currentText()
        statField = indicators.get_indicator_code_from_name(statFieldName)
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
        out2.setLayerName("{} ({})".format(stat, statFieldName))
        QgsMapLayerRegistry.instance().removeMapLayers([out1.id()])

        if self.labelCheckBox.isChecked():
            add_labels(out2, stat)

        if self.symCheckBox.isChecked():
            pass
