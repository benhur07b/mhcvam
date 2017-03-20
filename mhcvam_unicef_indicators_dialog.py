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
 mhcvam_unicef_indicators_dialog.py

 Contains the logic for the MHCVAM using UNICEF Indicators (BARANGAY)
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

from mhcvam_unicef_indicators_dialog_form import Ui_MHCVAMUnicefIndicatorsDialog

indicators_path_unicef = os.path.dirname(__file__) + '/indicators_unicef.csv'

indicators = UNICEFBrgyIndicators(indicators_path_unicef)


# try to solve UnicodeEncodeError in WIN
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')


class MHCVAMUnicefIndicatorsDialog(QDialog, Ui_MHCVAMUnicefIndicatorsDialog):

    def __init__(self, parent=None, iface=None):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        self.setWindowTitle(self.tr('MHCVAM using UNICEF Indicators (BARANGAY)'))
        self.iface = iface

        # Set the response of the OK and Apply buttons
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.run)
        QObject.connect(self.buttonBox.button(QDialogButtonBox.Apply), SIGNAL("clicked()"), self.run)

        self.agencyComboBox.addItems(indicators.agencies_list)
        self.categoryComboBox.addItems(indicators.categories_list)

        # If the selected layer changes, change the options for the fields too
        QObject.connect(self.layerComboBox,
                        SIGNAL("currentIndexChanged(QString)"),
                        self.set_fields)

        QObject.connect(self.agencyComboBox,
                        SIGNAL("currentIndexChanged(QString)"),
                        self.set_fields_from_agency)

        QObject.connect(self.categoryComboBox,
                        SIGNAL("currentIndexChanged(QString)"),
                        self.set_fields_from_category)

        QObject.connect(self.fieldComboBox,
                        SIGNAL("currentIndexChanged(QString)"),
                        self.show_limits)


    def clear_limits(self):

        self.lowLower.clear()
        self.lowUpper.clear()
        self.mediumLower.clear()
        self.mediumUpper.clear()
        self.highLower.clear()
        self.highUpper.clear()


    def show_limits(self):

        if self.fieldComboBox.count() == 0:
            self.clear_limits()

        else:
            indicator = self.fieldComboBox.currentText()

            # If the current field is an indicator, show cutoffs. Else, don't.
            if indicator in indicators.get_indicator_names():
                i = [x for x in indicators.indicators_list if x[1] == indicator]
                self.lowLower.setText(i[0][4])
                self.lowUpper.setText(i[0][5])
                self.mediumLower.setText(i[0][6])
                self.mediumUpper.setText(i[0][7])
                self.highLower.setText(i[0][8])
                self.highUpper.setText(i[0][9])

            else:
                pass


    def set_fields_from_agency(self):

        self.fieldComboBox.clear()

        selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.layerComboBox.currentText())[0]
        layerFields = [field.name() for field in selectedLayer.fields().toList()]
        agencyFields = indicators.agencies_with_indicators_list[self.agencyComboBox.currentIndex()][1]

        fields = list(set(layerFields).intersection(agencyFields))
        fieldnames = [indicators.get_indicator_name_from_code(f) for f in fields]
        self.fieldComboBox.addItems(fieldnames)
        self.categoryComboBox.setCurrentIndex(0)
        self.show_limits()


    def set_fields_from_category(self):

        self.fieldComboBox.clear()

        selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.layerComboBox.currentText())[0]
        layerFields = [field.name() for field in selectedLayer.fields().toList()]
        categoryFields = indicators.categories_with_indicators_list[self.categoryComboBox.currentIndex()][1]

        fields = list(set(layerFields).intersection(categoryFields))
        fieldnames = [indicators.get_indicator_name_from_code(f) for f in fields]
        self.fieldComboBox.addItems(fieldnames)
        self.agencyComboBox.setCurrentIndex(0)
        self.show_limits()


    def set_fields(self):
        """Set the fields to be shown in the fieldComboBox according
        to the layer selected in the layerComboBox.
        """

        self.fieldComboBox.clear()
        self.categoryComboBox.setCurrentIndex(0)
        self.agencyComboBox.setCurrentIndex(0)
        selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.layerComboBox.currentText())[0]
        layerFields = [field.name() for field in selectedLayer.fields().toList()]
        indicatorFields = indicators.get_indicator_codes()

        fields = list(set(layerFields).intersection(indicatorFields))
        fieldnames = [indicators.get_indicator_name_from_code(f) for f in fields]
        self.fieldComboBox.addItems(fieldnames)
        self.show_limits()


    def check_cutoffs(self):
        """Checks if the cutoffs are valid"""

        cutoffs = [self.lowLower, self.lowUpper, self.mediumLower, self.mediumUpper, self.highLower, self.highUpper]

        tvs = [(len(str(c.text())) == 0) for c in cutoffs]

        # Returns True if there is a lower and upper value, or no values at all
        with_low = tvs[0] == tvs[1]
        with_med = tvs[2] == tvs[3]
        with_high = tvs[4] == tvs[5]

        # Returns True if the lower cutoff is <= the upper cutoff, if there are values
        # Returns False otherwise or if there is only 1 value
        try:
            nums_low = float(cutoffs[0].text()) <= float(cutoffs[1].text())
        except ValueError:
            if with_low:
                nums_low = True
            else:
                nums_low = False

        try:
            nums_med = float(cutoffs[2].text()) <= float(cutoffs[3].text())
        except ValueError:
            if with_med:
                nums_med = True
            else:
                nums_med = False

        try:
            nums_high = float(cutoffs[4].text()) <= float(cutoffs[5].text())
        except ValueError:
            if with_high:
                nums_high = True
            else:
                nums_high = False

        # Return True if ALL tests are are True
        low = with_low and nums_low
        med = with_med and nums_med
        high = with_high and nums_high

        return low and med and high


    def run(self):

        if self.check_cutoffs():

            layer = QgsMapLayerRegistry.instance().mapLayersByName(self.layerComboBox.currentText())[0]
            indicator_name = self.fieldComboBox.currentText()
            field = indicators.get_indicator_code_from_name(indicator_name)

            indicator = []

            # Add style values there are cutoffs for Low, Medium, or High. Otherwise, pass.
            try:
                indicator.append(("Low", float(self.lowLower.text()), float(self.lowUpper.text()), "cyan"))
            except ValueError:
                pass

            try:
                indicator.append(("Medium", float(self.mediumLower.text()), float(self.mediumUpper.text()), "orange"))
            except ValueError:
                pass

            try:
                indicator.append(("High", float(self.highLower.text()), float(self.highUpper.text()), "red"))
            except ValueError:
                pass

            ranges = []

            for label, lower, upper, color in indicator:

                sym = QgsSymbolV2.defaultSymbol(layer.geometryType())
                sym.setColor(QColor(color))
                rng = QgsRendererRangeV2(lower, upper, sym, "{} ({})".format(label, indicator_name))
                ranges.append(rng)

            renderer = QgsGraduatedSymbolRendererV2(field, ranges)

            layer.setRendererV2(renderer)

            layer.triggerRepaint()

        else:
            QMessageBox.critical(self.iface.mainWindow(), "WARNING", "INCORRECT CUTOFFS")
