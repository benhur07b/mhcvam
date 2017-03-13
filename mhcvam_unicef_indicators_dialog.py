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
 mhcvam_unicef_indicators.py

 Contains the logic for the MHCVAM using UNICEF Indicators
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

indicators = Indicators(indicators_path_unicef)

class MHCVAMUnicefIndicatorsDialog(QDialog, Ui_MHCVAMUnicefIndicatorsDialog):

    def __init__(self, parent=None, iface=None):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        self.setWindowTitle(self.tr('MHCVAM using UNICEF Indicators'))
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
            if indicator in indicators.get_indicator_codes():
                i = [x for x in indicators.unicef_indicators_list if x[0] == indicator]
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
        self.fieldComboBox.addItems(fields)
        self.categoryComboBox.setCurrentIndex(0)
        self.show_limits()


    def set_fields_from_category(self):

        self.fieldComboBox.clear()

        selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.layerComboBox.currentText())[0]
        layerFields = [field.name() for field in selectedLayer.fields().toList()]
        categoryFields = indicators.categories_with_indicators_list[self.categoryComboBox.currentIndex()][1]

        fields = list(set(layerFields).intersection(categoryFields))
        self.fieldComboBox.addItems(fields)
        self.agencyComboBox.setCurrentIndex(0)
        self.show_limits()


    def set_fields(self):
        """Set the fields to be shown in the fieldComboBox according
        to the layer selected in the layerComboBox.
        """

        self.fieldComboBox.clear()
        selectedLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.layerComboBox.currentText())[0]
        for field in selectedLayer.fields().toList():
            self.fieldComboBox.addItem(field.name())


    def missing_cutoffs(self):

        cutoffs = [self.lowLower, self.lowUpper, self.mediumLower, self.mediumUpper, self.highLower, self.highUpper]
        for c in cutoffs:
            if len(str(c.text())) == 0:
                return True

        return False


    def run(self):

        if self.missing_cutoffs():
            QMessageBox.critical(self.iface.mainWindow(), "WARNING", "CUT-OFF of {} NOT FOUND.".format(self.fieldComboBox.currentText()))

        else:
            try:
                assert float(self.lowLower.text()) < float(self.lowUpper.text()) < float(self.mediumLower.text()) < float(self.mediumUpper.text()) < float(self.highLower.text()) < float(self.highUpper.text())

                layer = QgsMapLayerRegistry.instance().mapLayersByName(self.layerComboBox.currentText())[0]
                field = self.fieldComboBox.currentText()
                indicator_name = [x[1] for x in indicators.unicef_indicators_list if x[0] ==  self.fieldComboBox.currentText()][0]
                indicator = [("Low", float(self.lowLower.text()), float(self.lowUpper.text()), "cyan"),
                             ("Medium", float(self.mediumLower.text()), float(self.mediumUpper.text()), "orange"),
                             ("High", float(self.highLower.text()), float(self.highUpper.text()), "red")]

                ranges = []

                for label, lower, upper, color in indicator:

                    sym = QgsSymbolV2.defaultSymbol(layer.geometryType())
                    sym.setColor(QColor(color))
                    rng = QgsRendererRangeV2(lower, upper, sym, "{} ({})".format(label, indicator_name))
                    ranges.append(rng)

                renderer = QgsGraduatedSymbolRendererV2(field, ranges)

                layer.setRendererV2(renderer)

                layer.triggerRepaint()

            except AssertionError as e:
                QMessageBox.critical(self.iface.mainWindow(), "WARNING", "CUT-OFF of {} INVALID.".format(self.fieldComboBox.currentText()))
