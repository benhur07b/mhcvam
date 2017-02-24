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
 mhcvam.py

 Contains the logic that runs the plugin
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


class MHCVAM:
    """QGIS plugin implementation"""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'MHCVAM_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.action_mhcvam_unicef_indicators = None
        self.action_mhcvam_household = None
        self.action_mhcvam_barangay = None
        self.action_mhcvam_infrastructures = None
        self.actions = []
        self.menu = self.tr(u'&MHCVAM')

        # Create a dockable toolbar aside from the Menu in "Plugins"
        self.toolbar = self.iface.addToolBar(u'MHCVAM')
        self.toolbar.setObjectName(u'MHCVAM')


    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('MHCVAM', message)


    def add_action(self, action, add_to_toolbar=True):
        """Add the action to the MHCVAM toolbar

        :param action: The action that should be added to the toolbar.
        :type action: QAction

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the MHCVAM toolbar. Defaults to True.
        :type add_to_toolbar: bool

        """
        # store in the class list of actions for easy plugin unloading
        self.actions.append(action)
        self.iface.addPluginToMenu(self.tr('MHCVAM'), action)
        if add_to_toolbar:
            self.toolbar.addAction(action)


    def initGui(self):
        """Gui initialisation procedure (for QGIS plugin api).

        .. note:: Don't change the name of this method from initGui!

        This method is called by QGIS and should be used to set up
        any graphical user interface elements that should appear in QGIS by
        default (i.e. before the user performs any explicit action with the
        plugin).
        """

        # Create a dockable toolbar aside from the Menu in "Plugins"
        self.toolbar = self.iface.addToolBar('MHCVAM')
        self.toolbar.setObjectName('MHCVAMToolBar')

        # Create the Menu in "Plugins"
        self._create_mhcvam_unicef_indicators_action()
        self._create_mhcvam_household_action()
        self._create_mhcvam_barangay_action()
        self._create_mhcvam_infrastructures_action()


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&MHCVAM'),
                action)
            self.iface.removeToolBarIcon(action)
            self.iface.unregisterMainWindowAction(action)

        # remove the toolbar
        self.iface.mainWindow().removeToolBar(self.toolbar)


    '''UNICEF Indicators Methods'''
    def _create_mhcvam_unicef_indicators_action(self):
        """Create action for MHCVAM using UNICEF Indicators"""

        icon = os.path.dirname(__file__) + '/img/icons/icon-unicef-indicators.png'
        self.action_mhcvam_unicef_indicators = QAction(
            QIcon(icon),
            self.tr('MHCVAM using UNICEF Indicators'),
            self.iface.mainWindow())
        self.action_mhcvam_unicef_indicators.setStatusTip(
            self.tr('MHCVAM using UNICEF Indicators'))
        self.action_mhcvam_unicef_indicators.setWhatsThis(
            self.tr('Perform MHCVAM using UNICEF Indicators'))
        self.action_mhcvam_unicef_indicators.triggered.connect(
            self.mhcvam_unicef_indicators)
        self.add_action(
            self.action_mhcvam_unicef_indicators)


    def mhcvam_unicef_indicators(self):
        """Show dialog for MHCVAM using UNICEF Indicators"""

        from mhcvam_unicef_indicators_dialog import MHCVAMUnicefIndicatorsDialog

        # Run only if there are layers already loaded into QGIS
        if len(QgsMapLayerRegistry.instance().mapLayers()) > 0:
            dialog = MHCVAMUnicefIndicatorsDialog(
                self.iface.mainWindow(),
                self.iface)
            dialog.exec_()

        else:
            msg = "NO LAYERS FOUND.\n\nAdd layers first before running the plugin."
            QMessageBox.critical(self.iface.mainWindow(), "WARNING", msg)


    '''Household Methods'''
    def _create_mhcvam_household_action(self):
        """Create action for Household-level Analysis"""

        icon = os.path.dirname(__file__) + '/img/icons/icon-household.png'
        self.action_mhcvam_household = QAction(
            QIcon(icon),
            self.tr('Household-level Analysis'),
            self.iface.mainWindow())
        self.action_mhcvam_household.setStatusTip(
            self.tr('Household-level Analysis'))
        self.action_mhcvam_household.setWhatsThis(
            self.tr('Perform Household-level Analysis'))
        self.action_mhcvam_household.triggered.connect(
            self.mhcvam_household)
        self.add_action(
            self.action_mhcvam_household)


    def mhcvam_household(self):
        """Show dialog for Household-level Analysis"""

        from mhcvam_household_dialog import MHCVAMHouseholdDialog

        # Run only if there are layers already loaded into QGIS
        if len(QgsMapLayerRegistry.instance().mapLayers()) > 0:
            dialog = MHCVAMHouseholdDialog(
                self.iface.mainWindow(),
                self.iface)
            dialog.exec_()

        else:
            msg = "NO LAYERS FOUND.\n\nAdd layers first before running the plugin."
            QMessageBox.critical(self.iface.mainWindow(), "WARNING", msg)


    '''Barangay Methods'''
    def _create_mhcvam_barangay_action(self):
        """Create action for Barangay-level Analysis"""

        icon = os.path.dirname(__file__) + '/img/icons/icon-barangay.png'
        self.action_mhcvam_barangay = QAction(
            QIcon(icon),
            self.tr('Barangay-level Analysis'),
            self.iface.mainWindow())
        self.action_mhcvam_barangay.setStatusTip(
            self.tr('Barangay-level Analysis'))
        self.action_mhcvam_barangay.setWhatsThis(
            self.tr('Perform Barangay-level Analysis'))
        self.action_mhcvam_barangay.triggered.connect(
            self.mhcvam_barangay)
        self.add_action(
            self.action_mhcvam_barangay)


    def mhcvam_barangay(self):
        """Show dialog for Barangay-level Analysis"""

        from mhcvam_barangay_dialog import MHCVAMBarangayDialog

        # Run only if there are layers already loaded into QGIS
        if len(QgsMapLayerRegistry.instance().mapLayers()) > 0:
            dialog = MHCVAMBarangayDialog(
                self.iface.mainWindow(),
                self.iface)
            dialog.exec_()

        else:
            msg = "NO LAYERS FOUND.\n\nAdd layers first before running the plugin."
            QMessageBox.critical(self.iface.mainWindow(), "WARNING", msg)


    '''Infrastructures Methods'''
    def _create_mhcvam_infrastructures_action(self):
        """Create action for Infrastructures Risk Analysis"""

        icon = os.path.dirname(__file__) + '/img/icons/icon-infrastructures.png'
        self.action_mhcvam_infrastructures = QAction(
            QIcon(icon),
            self.tr('Infrastructures Hazard Analysis'),
            self.iface.mainWindow())
        self.action_mhcvam_infrastructures.setStatusTip(
            self.tr('Infrastructures Hazar Analysis'))
        self.action_mhcvam_infrastructures.setWhatsThis(
            self.tr('Perform Infrastructures Hazard Analysis'))
        self.action_mhcvam_infrastructures.triggered.connect(
            self.mhcvam_infrastructures)
        self.add_action(
            self.action_mhcvam_infrastructures)


    def mhcvam_infrastructures(self):
        """Show dialog for Infratructures Risk Analysis"""

        from mhcvam_infrastructures_dialog import MHCVAMInfrastructuresDialog

        # Run only if there are layers already loaded into QGIS
        if len(QgsMapLayerRegistry.instance().mapLayers()) > 0:
            dialog = MHCVAMInfrastructuresDialog(
                self.iface.mainWindow(),
                self.iface)
            dialog.exec_()

        else:
            msg = "NO LAYERS FOUND.\n\nAdd layers first before running the plugin."
            QMessageBox.critical(self.iface.mainWindow(), "WARNING", msg)
