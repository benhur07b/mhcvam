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

        # Set the response of the buttons
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.run)
        QObject.connect(self.selectAllBtn, SIGNAL("clicked()"), self.listWidget.selectAll)
        QObject.connect(self.deselectAllBtn, SIGNAL("clicked()"), self.listWidget.clearSelection)

        self.listWidget.addItems(indicators.get_indicator_names())


    def run(self):

        pass
