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
 mhcvam_unicef_indicators_household_dialog.py

 Contains the logic for the MHCVAM using Child-centered Indicators (HOUSEHOLD)
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

from mhcvam_library import *

from mhcvam_unicef_indicators_household_dialog_form import Ui_MHCVAMUnicefIndicatorsHouseholdDialog

indicators_path_unicef = os.path.dirname(__file__) + '/indicators_unicef_household.csv'

indicators = Indicators(indicators_path_unicef)


# try to solve UnicodeEncodeError in WIN
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')


class MHCVAMUnicefIndicatorsHouseholdDialog(QDialog, Ui_MHCVAMUnicefIndicatorsHouseholdDialog):

    def __init__(self, parent=None, iface=None):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        self.setWindowTitle(self.tr('MHCVAM using Child-centered Indicators (HOUSEHOLD)'))
        self.iface = iface

        self.listWidget_cats = [self.listWidget_exp, self.listWidget_vul, self.listWidget_cap]

        # Set the response of the buttons
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.run)

        QObject.connect(self.selectAllBtn_exp, SIGNAL("clicked()"), self.listWidget_exp.selectAll)
        QObject.connect(self.deselectAllBtn_exp, SIGNAL("clicked()"), self.listWidget_exp.clearSelection)
        QObject.connect(self.selectAllBtn_vul, SIGNAL("clicked()"), self.listWidget_vul.selectAll)
        QObject.connect(self.deselectAllBtn_vul, SIGNAL("clicked()"), self.listWidget_vul.clearSelection)
        QObject.connect(self.selectAllBtn_cap, SIGNAL("clicked()"), self.listWidget_cap.selectAll)
        QObject.connect(self.deselectAllBtn_cap, SIGNAL("clicked()"), self.listWidget_cap.clearSelection)
        # QObject.connect(self.selectAllBtn_oth, SIGNAL("clicked()"), self.listWidget_oth.selectAll)
        # QObject.connect(self.deselectAllBtn_oth, SIGNAL("clicked()"), self.listWidget_oth.clearSelection)

        self.indicators_per_cats = indicators.get_indicators_per_catergory_dict()
        self.listWidget_exp.addItems(self.indicators_per_cats['Exposure'])
        self.listWidget_vul.addItems(self.indicators_per_cats['Vulnerability'])
        self.listWidget_cap.addItems(self.indicators_per_cats['Capacity'])
        # self.listWidget_oth.addItems(self.indicators_per_cats['Others'])


    def get_indicators_to_add(self):

        # to_add = self.listWidget.selectedIndexes()
        # to_add_names = [str(x.data()) for x in to_add]
        # to_add_codes = [indicators.get_indicator_code_from_name(x) for x in to_add_names]
        # return to_add_codes

        to_add = [x.selectedIndexes() for x in self.listWidget_cats]
        to_add_names = [str(x.data()) for sublist in to_add for x in sublist]
        to_add_codes = [indicators.get_indicator_code_from_name(x) for x in to_add_names]
        return to_add_codes


    def get_selected_indicators(self):

        sel_exp = self.listWidget_exp.selectedIndexes()
        sel_exp_names = [str(x.data()) for x in sel_exp]
        sel_exp_codes = [indicators.get_indicator_code_from_name(x) for x in sel_exp_names]

        sel_vul = self.listWidget_vul.selectedIndexes()
        sel_vul_names = [str(x.data()) for x in sel_vul]
        sel_vul_codes = [indicators.get_indicator_code_from_name(x) for x in sel_vul_names]

        sel_cap = self.listWidget_cap.selectedIndexes()
        sel_cap_names = [str(x.data()) for x in sel_cap]
        sel_cap_codes = [indicators.get_indicator_code_from_name(x) for x in sel_cap_names]

        return {'Exposure': sel_exp_codes,
                'Vulnerability': sel_vul_codes,
                'Capacity': sel_cap_codes
                }

        # sel_oth = self.listWidget_oth.selectedIndexes()
        # sel_oth_names = [str(x.data()) for x in sel_oth]
        # sel_oth_codes = [indicators.get_indicator_code_from_name(x) for x in sel_oth_names]

        # return {'Exposure': sel_exp_codes,
        #         'Vulnerability': sel_vul_codes,
        #         'Capacity': sel_cap_codes,
        #         'Others': sel_oth_codes}

    def run(self):

        hh = QgsMapLayerRegistry.instance().mapLayersByName(self.selectHHComboBox.currentText())[0]
        to_add_codes = self.get_indicators_to_add()
        selected_indicators = self.get_selected_indicators()

        exp_codes = selected_indicators['Exposure']
        vul_codes = selected_indicators['Vulnerability']
        cap_codes = selected_indicators['Capacity']
        # oth_codes = selected_indicators['Others']

        result_name = self.resultFieldNameLineEdit.text()
        exp_name = "{}_EXP".format(result_name)
        vul_name = "{}_VUL".format(result_name)
        cap_name = "{}_CAP".format(result_name)
        # oth_name = "{}_OTH".format(result_name)

        indices_exp = [hh.fieldNameIndex(code) for code in exp_codes]
        indices_vul = [hh.fieldNameIndex(code) for code in vul_codes]
        indices_cap = [hh.fieldNameIndex(code) for code in cap_codes]
        # indices_oth = [hh.fieldNameIndex(code) for code in oth_codes]

        if len(indices_exp) > 0:
            self.compute_risk(hh, exp_name, indices_exp, exp_codes, "exp")

        if len(indices_vul) > 0:
            self.compute_risk(hh, vul_name, indices_vul, vul_codes, "vul")

        if len(indices_cap) > 0:
            self.compute_risk(hh, cap_name, indices_cap, cap_codes, "cap")


    def compute_risk(self, hh, name, indices, codes, ind_type):

        # copy vector to new layer
        copy_vector_layer(hh, name, "Point")
        layer = QgsMapLayerRegistry.instance().mapLayersByName(name)[0]


        # add other fields
        res = layer.dataProvider().addAttributes([QgsField("TOTAL", QVariant.Double, 'double', 4, 2)])
        layer.updateFields()

        res = layer.dataProvider().addAttributes([QgsField("RISK", QVariant.String)])
        layer.updateFields()

        # add field to hold selected fields
        res = layer.dataProvider().addAttributes([QgsField("SELECTED", QVariant.String)])
        layer.updateFields()

        totfield = layer.fieldNameIndex("TOTAL")
        riskfield = layer.fieldNameIndex("RISK")
        selfield = layer.fieldNameIndex("SELECTED")

        layer_fields = layer.fields()

        # get max indicators
        mxs = []
        mx = 0

        features_max = layer.getFeatures()
        for f in features_max:

            attr = f.attributes()

            for i in indices:

                try:
                    # new (only include if main field by counting # of "_". main means less than 2 "_")
                    if layer_fields[i].name().count("_") < 2:
                        if float(attr[i]) >= 1:
                            if ind_type == "exp":
                                mx += float(attr[i])
                            else:
                                mx += 1

                        else:
                            pass

                    else:
                        pass

                except ValueError:
                    mx += 0

                mxs.append(mx)  # get list of number of indicators
            mx = 0  # reset number of indicators to zero for a new feature

        mx_i = max(mxs) # get max number of indicators in 1 feature

        # count values
        features = layer.getFeatures()
        for f in features:

            layer.startEditing()
            attr = f.attributes()

            s = 0

            for i in indices:

                try:
                    # new (only include if main field by counting # of "_". main means less than 2 "_")
                    if layer_fields[i].name().count("_") < 2:
                        # s += float(attr[i])
                        if float(attr[i]) >= 1:
                            if ind_type == "exp":
                                s += float(attr[i])
                            else:
                                s += 1

                        else:
                            pass

                    else:
                        pass

                except ValueError:
                    s += 0

            f[totfield] = s

            s_perc = 100.0 * (float(s)/mx_i)

            if s_perc < 33.33:
                f[riskfield] = "LOW"

            elif s_perc >= 33.33 and s_perc < 66.66:
                f[riskfield] = "MODERATE"

            else:
                f[riskfield] = "HIGH"

            # add selected fields
            f[selfield] = ", ".join(codes)

            layer.updateFeature(f)
        layer.commitChanges()


        # remove unwanted fields
        f = layer.fields().toList()
        fields = range(len(f))

        const = ["BRGY_HH_ID", "BARANGAY", "HOUSEHOLD", "STREET", "HH_HEAD", "TOTAL", "RISK", "SELECTED"]
        indices_constant = [layer.fieldNameIndex(code) for code in const]

        for c in indices_constant:
            fields.remove(c)

        res = layer.dataProvider().deleteAttributes(fields)
        layer.updateFields()

        # Add symbology
        risks = [("LOW", "cyan", "LOW"),
                 ("MODERATE", "orange", "MODERATE"),
                 ("HIGH", "red", "HIGH")]

        categories = []
        for risk, color, label in risks:
            sym = QgsSymbolV2.defaultSymbol(layer.geometryType())
            sym.setColor(QColor(color))
            cat = QgsRendererCategoryV2(risk, sym, label)
            categories.append(cat)

        renderer = QgsCategorizedSymbolRendererV2("RISK", categories)
        layer.setRendererV2(renderer)
        layer.triggerRepaint()



    # def run(self):
    #
    #     hh = QgsMapLayerRegistry.instance().mapLayersByName(self.selectHHComboBox.currentText())[0]
    #     to_add_codes = self.get_indicators_to_add()
    #     selected_indicators = self.get_selected_indicators()
    #     exp_codes = selected_indicators['Exposure']
    #     vul_codes = selected_indicators['Vulnerability']
    #     cap_codes = selected_indicators['Capacity']
    #     oth_codes = selected_indicators['Others']
    #
    #     result_name = self.resultFieldNameLineEdit.text()
    #
    #     exp_name = "{}_EXP".format(result_name)
    #     res = hh.dataProvider().addAttributes([QgsField(exp_name, QVariant.Double, 'double', 4, 2)])
    #     hh.updateFields()
    #     exp_index = hh.fieldNameIndex(exp_name)
    #
    #     vul_name = "{}_VUL".format(result_name)
    #     res = hh.dataProvider().addAttributes([QgsField(vul_name, QVariant.Double, 'double', 4, 2)])
    #     hh.updateFields()
    #     vul_index = hh.fieldNameIndex(vul_name)
    #
    #     cap_name = "{}_CAP".format(result_name)
    #     res = hh.dataProvider().addAttributes([QgsField(cap_name, QVariant.Double, 'double', 4, 2)])
    #     hh.updateFields()
    #     cap_index = hh.fieldNameIndex(cap_name)
    #
    #     oth_name = "{}_OTH".format(result_name)
    #     res = hh.dataProvider().addAttributes([QgsField(oth_name, QVariant.Double, 'double', 4, 2)])
    #     hh.updateFields()
    #     oth_index = hh.fieldNameIndex(oth_name)
    #
    #     res = hh.dataProvider().addAttributes([QgsField(result_name, QVariant.Double, 'double', 4, 2)])
    #     hh.updateFields()
    #     result_index = hh.fieldNameIndex(result_name)
    #
    #     features = hh.getFeatures()
    #     indices = [hh.fieldNameIndex(code) for code in to_add_codes]
    #     indices_exp = [hh.fieldNameIndex(code) for code in exp_codes]
    #     indices_vul = [hh.fieldNameIndex(code) for code in vul_codes]
    #     indices_cap = [hh.fieldNameIndex(code) for code in cap_codes]
    #     indices_oth = [hh.fieldNameIndex(code) for code in oth_codes]
    #
    #     for f in features:
    #         hh.startEditing()
    #         attr = f.attributes()
    #
    #         s = 0
    #         s_exp = 0
    #         s_vul = 0
    #         s_cap = 0
    #         s_oth = 0
    #
    #         for i in indices:
    #
    #             try:
    #                 s += float(attr[i])
    #             except ValueError:
    #                 s += 0
    #
    #             if i in indices_exp:
    #                 try:
    #                     s_exp += float(attr[i])
    #                 except ValueError:
    #                     s_exp += 0
    #
    #             if i in indices_vul:
    #                 try:
    #                     s_vul += float(attr[i])
    #                 except ValueError:
    #                     s_vul += 0
    #
    #             if i in indices_cap:
    #                 try:
    #                     s_cap += float(attr[i])
    #                 except ValueError:
    #                     s_cap += 0
    #
    #             if i in indices_oth:
    #                 try:
    #                     s_oth += float(attr[i])
    #                 except ValueError:
    #                     s_oth += 0
    #
    #         f[result_index] = s
    #         f[exp_index] = s_exp
    #         f[vul_index] = s_vul
    #         f[cap_index] = s_cap
    #         f[oth_index] = s_oth
    #         # f[result_index] = sum(float(attr[i]) for i in indices)
    #         hh.updateFeature(f)
    #
    #     hh.commitChanges()
    #
    #     # Add Symbology
    #     high = len(to_add_codes)
    #     low = 0
    #     medium = high/2
    #
    #     indicator = [("Low ({} - {})".format(low, medium - 1), low, medium - 1, "cyan"),
    #                  ("Medium ({} - {})".format(medium, high - 1), medium, high - 1, "orange"),
    #                  ("High (>={})".format(high), high, 9999999, "red")]
    #
    #     ranges = []
    #
    #     for label, lower, upper, color in indicator:
    #
    #         sym = QgsSymbolV2.defaultSymbol(hh.geometryType())
    #         sym.setColor(QColor(color))
    #         rng = QgsRendererRangeV2(lower, upper, sym, "{}".format(label))
    #         ranges.append(rng)
    #
    #     renderer = QgsGraduatedSymbolRendererV2(result_name, ranges)
    #
    #     hh.setRendererV2(renderer)
    #
    #     hh.triggerRepaint()
    #
    #     msg = "{} added to  {}".format(result_name, self.selectHHComboBox.currentText())
    #     QMessageBox.information(self.iface.mainWindow(), "SUCCESS", msg)
