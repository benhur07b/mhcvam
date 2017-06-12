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

 Contains the logic for the Household-level Hazard and Vulnerability Analysis
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

indicators_path_hh = os.path.dirname(__file__) + '/indicators_household.csv'

indicators = Indicators(indicators_path_hh)


# try to solve UnicodeEncodeError in WIN
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')


class MHCVAMHouseholdDialog(QDialog, Ui_MHCVAMHouseholdDialog):

    def __init__(self, parent=None, iface=None):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        self.setWindowTitle(self.tr('Household-level Hazard and Vulnerability Analysis'))
        self.iface = iface

        QObject.connect(self.selectHHButtonBox, SIGNAL("accepted()"), self.run_select)
        QObject.connect(self.queryHHButtonBox, SIGNAL("accepted()"), self.run_query)
        QObject.connect(self.queryHHButtonBox.button(QDialogButtonBox.Reset), SIGNAL("clicked()"), self.reset_selection)
        QObject.connect(self.summHHButtonBox, SIGNAL("accepted()"), self.run_summary)
        QObject.connect(self.queryFieldAdd, SIGNAL("clicked()"), self.add_field_to_query)
        QObject.connect(self.uniqueValuesButton, SIGNAL("clicked()"), self.get_unique_field_values)
        QObject.connect(self.queryValueAdd, SIGNAL("clicked()"), self.add_value_to_query)
        QObject.connect(self.queryFunctionAdd, SIGNAL("clicked()"), self.add_function_to_query)

        self.agencyComboBox.addItems(indicators.agencies_list)
        self.queryAgencyComboBox.addItems(indicators.agencies_list)

        # Uncomment below if you need Limit by Category (Must Edit GUI)
        # self.categoryComboBox.addItems(indicators.categories_list)
        # self.queryCategoryComboBox.addItems(indicators.categories_list)

        QObject.connect(self.selectHazardComboBox,
                        SIGNAL("currentIndexChanged(QString)"),
                        self.set_hazard)

        QObject.connect(self.queryHHComboBox,
                        SIGNAL("currentIndexChanged(QString)"),
                        self.change_hh_layer_query)

        QObject.connect(self.summHHComboBox,
                        SIGNAL("currentIndexChanged(QString)"),
                        self.change_HH_summ)

        QObject.connect(self.summHHBrgyComboBox,
                        SIGNAL("currentIndexChanged(QString)"),
                        self.set_brgy)

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

        self.set_hazard()
        self.set_brgy()

    def change_HH_summ(self):
        self.set_brgy()
        self.set_fields_from_agency()

    def set_hazard(self):

        selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.selectHazardComboBox.currentText())[0]
        self.selectHazardTypeComboBox.setLayer(selectedLayer)


    def set_brgy(self):

        selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.summHHBrgyComboBox.currentText())[0]
        self.brgyFieldComboBox.setLayer(selectedLayer)


    def set_fields_from_agency(self):

        self.fieldComboBox.clear()
        self.uniqueValuesListWidget.clear()

        selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.summHHComboBox.currentText())[0]
        layerFields = [field.name() for field in selectedLayer.fields().toList()]
        agencyFields = indicators.agencies_with_indicators_list[self.agencyComboBox.currentIndex()][1]

        fields = list(set(layerFields).intersection(agencyFields))
        fieldnames = [indicators.get_indicator_name_from_code(f) for f in fields]
        self.fieldComboBox.addItems(fieldnames)
        # self.categoryComboBox.setCurrentIndex(0)


    def set_fields_from_agency_query(self):

        self.queryFieldComboBox.clear()
        self.uniqueValuesListWidget.clear()

        selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.queryHHComboBox.currentText())[0]
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
    #     selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.summHHComboBox.currentText())[0]
    #     layerFields = [field.name() for field in selectedLayer.fields().toList()]
    #     categoryFields = indicators.categories_with_indicators_list[self.categoryComboBox.currentIndex()][1]
    #
    #     fields = list(set(layerFields).intersection(categoryFields))
    #     fieldnames = [indicators.get_indicator_name_from_code(f) for f in fields]
    #     self.fieldComboBox.addItems(fieldnames)
    #     self.agencyComboBox.setCurrentIndex(0)

    # # Uncomment below if you need Limit by Category (Must Edit GUI)
    # def set_fields_from_category_query(self):
    #
    #     self.queryFieldComboBox.clear()
    #
    #     selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.queryHHComboBox.currentText())[0]
    #     layerFields = [field.name() for field in selectedLayer.fields().toList()]
    #     categoryFields = indicators.categories_with_indicators_list[self.queryCategoryComboBox.currentIndex()][1]
    #
    #     fields = list(set(layerFields).intersection(categoryFields))
    #     fieldnames = [indicators.get_indicator_name_from_code(f) for f in fields]
    #     self.queryFieldComboBox.addItems(fieldnames)
    #     self.queryAgencyComboBox.setCurrentIndex(0)


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

        if self.selectSummaryCheckBox.isChecked():
            hazardLevelCount = []
            features = outlayer.getFeatures()
            for f in features:
                attr = f.attributes()
                hazardLevelCount.append(attr[outlayer.fieldNameIndex(hazardType)].capitalize()) #set to Low, Medium, and High only

            numlows = hazardLevelCount.count("Low")
            nummeds = hazardLevelCount.count("Medium")
            numhigh = hazardLevelCount.count("High")

            hh_per_hazard = "Households in Hazard Level\nLow: {}\nMedium: {}\nHigh: {}".format(numlows, nummeds, numhigh)
            msg = hh_per_hazard
            QMessageBox.information(self.iface.mainWindow(), "SUMMARY REPORT", msg)

    def change_hh_layer_query(self):

        # self.reset_selection()
        self.queryFieldComboBox.clear()
        self.queryAgencyComboBox.setCurrentIndex(0)
        self.queryFunctionComboBox.setCurrentIndex(0)
        self.queryTextEdit.clear()
        self.uniqueValuesListWidget.clear()


    def add_field_to_query(self):

        self.queryTextEdit.insertPlainText(' "{}" '.format(indicators.get_indicator_name_from_code(self.queryFieldComboBox.currentText())))

    def get_unique_field_values(self):

        self.uniqueValuesListWidget.clear()

        brgy = QgsMapLayerRegistry.instance().mapLayersByName(self.queryHHComboBox.currentText())[0]
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

        # Only resets the selection of the current layer in the Household ComboBox
        hh = QgsMapLayerRegistry.instance().mapLayersByName(self.queryHHComboBox.currentText())[0]
        hh.removeSelection()
        hh.setSubsetString('')      # remove feature filter
        self.queryFieldComboBox.clear()
        self.queryAgencyComboBox.setCurrentIndex(0)
        self.queryFunctionComboBox.setCurrentIndex(0)
        self.queryTextEdit.clear()
        self.uniqueValuesListWidget.clear()

    # def run_query(self):
    #
    #     hh = QgsMapLayerRegistry.instance().mapLayersByName(self.queryHHComboBox.currentText())[0]
    #     text = self.queryTextEdit.toPlainText()
    #     q = indicators.convert_to_query(text)
    #     query = unicode(q)
    #     r = QgsFeatureRequest().setFilterExpression(query)
    #     sel = hh.getFeatures(r)
    #     hh.setSelectedFeatures([f.id() for f in sel])


    def run_query(self):
        """This version applies a feature filter before selection"""
        hh = QgsMapLayerRegistry.instance().mapLayersByName(self.queryHHComboBox.currentText())[0]
        text = self.queryTextEdit.toPlainText()
        q = indicators.convert_to_query(text)
        query = unicode(q)
        hh.setSubsetString(query)   # apply feature filter
        r = QgsFeatureRequest().setFilterExpression(query)
        sel = hh.getFeatures(r)
        hh.setSelectedFeatures([f.id() for f in sel])


    def run_summary(self):

        hh = QgsMapLayerRegistry.instance().mapLayersByName(self.summHHComboBox.currentText())[0]
        brgy = QgsMapLayerRegistry.instance().mapLayersByName(self.summHHBrgyComboBox.currentText())[0]
        brgyField = self.brgyFieldComboBox.currentText()
        statFieldName = self.fieldComboBox.currentText()
        statField = indicators.get_indicator_code_from_name(statFieldName)
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

        # copy_vector_layer(brgy, "{} ({})".format(stat, statFieldName), "Polygon")
        # out1 = QgsMapLayerRegistry.instance().mapLayersByName("{} ({})".format(stat, statFieldName))[0]
        #
        # res = out1.dataProvider().addAttributes([QgsField(stat, QVariant.Double, "double", 18, 2)])
        # out1.updateFields()
        #
        # statIndex = out1.fieldNameIndex(stat)
        # brgyIndex = out1.fieldNameIndex(brgyField)

        '''NEW'''

        if statFieldName in ["RISK", "Hazard Level"]:
            if stat in ["COUNT [LOW]", "COUNT [MEDIUM]", "COUNT [HIGH]"]:

                copy_vector_layer(brgy, "{} ({})".format(stat, statFieldName), "Polygon")
                out1 = QgsMapLayerRegistry.instance().mapLayersByName("{} ({})".format(stat, statFieldName))[0]

                res = out1.dataProvider().addAttributes([QgsField(stat, QVariant.Double, "double", 18, 2)])
                out1.updateFields()

                statIndex = out1.fieldNameIndex(stat)
                brgyIndex = out1.fieldNameIndex(brgyField)

                features = out1.getFeatures()
                for f in features:
                    try:
                        out1.startEditing()
                        attr = f.attributes()
                        f[statIndex] = brgyDict[attr[brgyIndex]].count(stat[7:-1])
                        out1.updateFeature(f)
                    except KeyError:
                        pass

                out1.commitChanges()

                if self.labelCheckBox.isChecked():
                    add_labels(out1, stat)

                if self.symCheckBox.isChecked():
                    pass

                remove_other_fields_summary(out1, brgyField)

            else:
                QMessageBox.warning(self.iface.mainWindow(), "WARNING", "ONLY COUNT CAN BE USED FOR RISKS")

        else:
            if stat in ["SUM", "MEAN", "MIN", "MAX", "PERCENTAGE"]:

                copy_vector_layer(brgy, "{} ({})".format(stat, statFieldName), "Polygon")
                out1 = QgsMapLayerRegistry.instance().mapLayersByName("{} ({})".format(stat, statFieldName))[0]

                res = out1.dataProvider().addAttributes([QgsField(stat, QVariant.Double, "double", 18, 2)])
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


                remove_other_fields_summary(out1, brgyField)

            else:
                QMessageBox.warning(self.iface.mainWindow(), "WARNING", "COUNT CAN ONLY BE USED FOR RISKS")




        '''NEW'''

        # if stat == "COUNT [LOW]":
        #     # res = out1.dataProvider().addAttributes([QgsField(stat, statField0.type())])
        #     # out1.updateFields()
        #
        #     if statFieldName == "RISK":
        #         # res = out1.dataProvider().addAttributes([QgsField("LOW", QVariant.Double, "double", 10, 2),
        #         #                                          QgsField("MEDIUM", QVariant.Double, "double", 10, 2),
        #         #                                          QgsField("HIGH", QVariant.Double, "double", 10, 2)])
        #         # out1.updateFields()
        #
        #         # res = out1.dataProvider().addAttributes([QgsField("MEDIUM", QVariant.Double, "double", 10, 2)])
        #         # out1.updateFields()
        #         #
        #         # res = out1.dataProvider().addAttributes([QgsField("HIGH", QVariant.Double, "double", 10, 2)])
        #         # out1.updateFields()
        #
        #         # lowIndex = out1.fieldNameIndex("LOW")
        #         # medIndex = out1.fieldNameIndex("MEDIUM")
        #         # highIndex = out1.fieldNameIndex("HIGH")
        #
        #         features = out1.getFeatures()
        #         for f in features:
        #             try:
        #                 out1.startEditing()
        #                 attr = f.attributes()
        #                 # f[statIndex] = len(brgyDict[attr[brgyIndex]])
        #                 f[statIndex] = brgyDict[attr[brgyIndex]].count("LOW")
        #                 # f[medIndex] = brgyDict[attr[brgyIndex]].count("MEDIUM")
        #                 # f[highIndex] = brgyDict[attr[brgyIndex]].count("HIGH")
        #                 out1.updateFeature(f)
        #             except KeyError:
        #                 pass
        #
        # if stat == "COUNT [MEDIUM]":
        #     # res = out1.dataProvider().addAttributes([QgsField(stat, statField0.type())])
        #     # out1.updateFields()
        #
        #     if statFieldName == "RISK":
        #
        #         features = out1.getFeatures()
        #         for f in features:
        #             try:
        #                 out1.startEditing()
        #                 attr = f.attributes()
        #                 # f[statIndex] = len(brgyDict[attr[brgyIndex]])
        #                 f[statIndex] = brgyDict[attr[brgyIndex]].count("MEDIUM")
        #                 # f[medIndex] = brgyDict[attr[brgyIndex]].count("MEDIUM")
        #                 # f[highIndex] = brgyDict[attr[brgyIndex]].count("HIGH")
        #                 out1.updateFeature(f)
        #             except KeyError:
        #                 pass
        #
        # if stat == "COUNT [HIGH]":
        #     # res = out1.dataProvider().addAttributes([QgsField(stat, statField0.type())])
        #     # out1.updateFields()
        #
        #     if statFieldName == "RISK":
        #
        #         features = out1.getFeatures()
        #         for f in features:
        #             try:
        #                 out1.startEditing()
        #                 attr = f.attributes()
        #                 # f[statIndex] = len(brgyDict[attr[brgyIndex]])
        #                 f[statIndex] = brgyDict[attr[brgyIndex]].count("HIGH")
        #                 # f[medIndex] = brgyDict[attr[brgyIndex]].count("MEDIUM")
        #                 # f[highIndex] = brgyDict[attr[brgyIndex]].count("HIGH")
        #                 out1.updateFeature(f)
        #             except KeyError:
        #                 pass
        #
        #
        # if stat == "SUM":
        #     # res = out1.dataProvider().addAttributes([QgsField(stat, QVariant.Double, "double", 10, 2)])
        #     # out1.updateFields()
        #     if statFieldName == "RISK":
        #         QMessageBox.warning(self.iface.mainWindow(), "WARNING", "SUM CAN'T BE USED ON RISK")
        #         pass
        #
        #     else:
        #         features = out1.getFeatures()
        #         for f in features:
        #             try:
        #                 out1.startEditing()
        #                 attr = f.attributes()
        #                 f[statIndex] = sum(brgyDict[attr[brgyIndex]])
        #                 out1.updateFeature(f)
        #             except KeyError:
        #                 pass
        #
        # if stat == "MEAN":
        #     # res = out1.dataProvider().addAttributes([QgsField(stat, QVariant.Double, "double", 10, 2)])
        #     # out1.updateFields()
        #
        #     if statFieldName == "RISK":
        #         pass
        #
        #     else:
        #         features = out1.getFeatures()
        #         for f in features:
        #             try:
        #                 out1.startEditing()
        #                 attr = f.attributes()
        #                 f[statIndex] = round(1.0*sum(brgyDict[attr[brgyIndex]])/len(brgyDict[attr[brgyIndex]]), 2)
        #                 out1.updateFeature(f)
        #             except KeyError:
        #                 pass
        #
        # if stat == "MIN":
        #     # res = out1.dataProvider().addAttributes([QgsField(stat, QVariant.Double, "double", 10, 2)])
        #     # out1.updateFields()
        #
        #     if statFieldName == "RISK":
        #         pass
        #
        #     else:
        #         features = out1.getFeatures()
        #         for f in features:
        #             try:
        #                 out1.startEditing()
        #                 attr = f.attributes()
        #                 f[statIndex] = min(brgyDict[attr[brgyIndex]])
        #                 out1.updateFeature(f)
        #             except KeyError:
        #                 pass
        #
        # if stat == "MAX":
        #     # res = out1.dataProvider().addAttributes([QgsField(stat, QVariant.Double, "double", 10, 2)])
        #     # out1.updateFields()
        #
        #     if statFieldName == "RISK":
        #         pass
        #
        #     else:
        #         features = out1.getFeatures()
        #         for f in features:
        #             try:
        #                 out1.startEditing()
        #                 attr = f.attributes()
        #                 f[statIndex] = max(brgyDict[attr[brgyIndex]])
        #                 out1.updateFeature(f)
        #             except KeyError:
        #                 pass
        #
        # if stat == "PERCENTAGE":
        #     # res = out1.dataProvider().addAttributes([QgsField(stat, QVariant.Double, "double", 10, 2)])
        #     # out1.updateFields()
        #
        #     if statFieldName == "RISK":
        #         pass
        #
        #     else:
        #         sumDict = {}
        #         total = 0
        #         features = out1.getFeatures()
        #         for f in features:
        #             try:
        #                 attr = f.attributes()
        #                 sumDict[attr[brgyIndex]] = sum(brgyDict[attr[brgyIndex]])
        #                 total += sum(brgyDict[attr[brgyIndex]])
        #             except KeyError:
        #                 pass
        #
        #         features2 = out1.getFeatures()
        #         for f in features2:
        #             try:
        #                 out1.startEditing()
        #                 attr = f.attributes()
        #                 f[statIndex] = round(100.0*sumDict[attr[brgyIndex]]/total, 2)
        #                 out1.updateFeature(f)
        #             except KeyError:
        #                 pass
        #
        # out1.commitChanges()
        #
        # if self.labelCheckBox.isChecked():
        #     add_labels(out1, stat)
        #
        # if self.symCheckBox.isChecked():
        #     pass
        #
        #
        # remove_other_fields_summary(out1, brgyField)
