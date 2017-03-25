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

 Contains the logic for the MHCVAM using UNICEF Indicators (HOUSEHOLD)
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

indicators_path_unicef = os.path.dirname(__file__) + '/indicators_household.csv'

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
        self.setWindowTitle(self.tr('MHCVAM using UNICEF Indicators (HOUSEHOLD)'))
        self.iface = iface

        self.listWidget_cats = [self.listWidget_exp, self.listWidget_vul, self.listWidget_cap, self.listWidget_oth]

        # Set the response of the buttons
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.run)

        QObject.connect(self.selectAllBtn_exp, SIGNAL("clicked()"), self.listWidget_exp.selectAll)
        QObject.connect(self.deselectAllBtn_exp, SIGNAL("clicked()"), self.listWidget_exp.clearSelection)
        QObject.connect(self.selectAllBtn_vul, SIGNAL("clicked()"), self.listWidget_vul.selectAll)
        QObject.connect(self.deselectAllBtn_vul, SIGNAL("clicked()"), self.listWidget_vul.clearSelection)
        QObject.connect(self.selectAllBtn_cap, SIGNAL("clicked()"), self.listWidget_cap.selectAll)
        QObject.connect(self.deselectAllBtn_cap, SIGNAL("clicked()"), self.listWidget_cap.clearSelection)
        QObject.connect(self.selectAllBtn_oth, SIGNAL("clicked()"), self.listWidget_oth.selectAll)
        QObject.connect(self.deselectAllBtn_oth, SIGNAL("clicked()"), self.listWidget_oth.clearSelection)

        self.indicators_per_cats = indicators.get_indicators_per_catergory_dict()
        self.listWidget_exp.addItems(self.indicators_per_cats['Exposure'])
        self.listWidget_vul.addItems(self.indicators_per_cats['Vulnerability'])
        self.listWidget_cap.addItems(self.indicators_per_cats['Capacity'])
        self.listWidget_oth.addItems(self.indicators_per_cats['Others'])


    def get_indicators_to_add(self):

        # to_add = self.listWidget.selectedIndexes()
        # to_add_names = [str(x.data()) for x in to_add]
        # to_add_codes = [indicators.get_indicator_code_from_name(x) for x in to_add_names]
        # return to_add_codes

        to_add = [x.selectedIndexes() for x in self.listWidget_cats]
        to_add_names = [str(x.data()) for sublist in to_add for x in sublist]
        to_add_codes = [indicators.get_indicator_code_from_name(x) for x in to_add_names]
        return to_add_codes



    def run(self):

        hh = QgsMapLayerRegistry.instance().mapLayersByName(self.selectHHComboBox.currentText())[0]
        result_name = self.resultFieldNameLineEdit.text()
        res = hh.dataProvider().addAttributes([QgsField(result_name, QVariant.Double, 'double', 4, 2)])
        hh.updateFields()
        result_index = hh.fieldNameIndex(result_name)

        to_add_codes = self.get_indicators_to_add()

        features = hh.getFeatures()
        indices = [hh.fieldNameIndex(code) for code in to_add_codes]

        for f in features:
            hh.startEditing()
            attr = f.attributes()
            s = 0
            for i in indices:
                try:
                    s += float(attr[i])
                except ValueError:
                    s += 0

            f[result_index] = s
            # f[result_index] = sum(float(attr[i]) for i in indices)
            hh.updateFeature(f)

        hh.commitChanges()


        # Add Symbology

        high = len(to_add_codes)
        low = 0
        medium = high/2

        indicator = [("Low ({} - {})".format(low, medium - 1), low, medium - 1, "cyan"),
                     ("Medium ({} - {})".format(medium, high - 1), medium, high - 1, "orange"),
                     ("High (>={})".format(high), high, 9999999, "red")]

        ranges = []

        for label, lower, upper, color in indicator:

            sym = QgsSymbolV2.defaultSymbol(hh.geometryType())
            sym.setColor(QColor(color))
            rng = QgsRendererRangeV2(lower, upper, sym, "{}".format(label))
            ranges.append(rng)

        renderer = QgsGraduatedSymbolRendererV2(result_name, ranges)

        hh.setRendererV2(renderer)

        hh.triggerRepaint()

        msg = "{} added to  {}".format(result_name, self.selectHHComboBox.currentText())
        QMessageBox.information(self.iface.mainWindow(), "SUCCESS", msg)
