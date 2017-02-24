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
 mhcvam_library.py

 Contains commonly-used classes and methods
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
import csv

"""
0  INDICATOR_CODE
1  INDICATOR_NAME
2  AGENCY
3  CATEGORY
4  LOW_LOWER
5  LOW_UPPER
6  MEDIUM_LOWER
7  MEDIUM_UPPER
8  HIGH_LOWER
9  HIGH_UPPER
"""

indicators_path = os.path.dirname(__file__) + '/indicators.csv'

class Indicators():

    def __init__(self):
        self.unicef_indicators_list = self.get_unicef_indicators_list()
        self.unique_agencies = self.get_unique_agencies()
        self.agencies_with_indicators_list = self.get_agencies_with_indicators_list()
        self.agencies_list = [a[0] for a in self.agencies_with_indicators_list]
        self.unique_categories = self.get_unique_categories()
        self.categories_with_indicators_list = self.get_categories_with_indicators_list()
        self.categories_list = [c[0] for c in self.categories_with_indicators_list]
        self.color_dict = self.get_indicators_color_dict()

    def get_unicef_indicators_list(self):
        with open(indicators_path, 'rb') as f:
            reader = csv.reader(f)
            return list(reader)[1:]

    def get_indicator_codes(self):

        return [i[0] for i in self.unicef_indicators_list]

    def get_unique_agencies(self):
        agencies = [a[2] for a in self.unicef_indicators_list]
        return sorted(list(set(agencies)))

    def get_agencies_with_indicators(self):
        agencies = self.unique_agencies
        agencies_with_indicators = []
        for a in agencies:
            for i in self.unicef_indicators_list:
                n = [i[0] for i in self.unicef_indicators_list if i[2] == a]
            agencies_with_indicators.append([a, n])

        return agencies_with_indicators

    def get_agencies_with_indicators_list(self):
        a = self.get_agencies_with_indicators()
        a.insert(0, ["Select Agency", ("","")])

        return a

    def get_unique_categories(self):
        categories = [a[3] for a in self.unicef_indicators_list]
        return sorted(list(set(categories)))

    def get_categories_with_indicators(self):
        categories = self.unique_categories
        categories_with_indicators = []
        for c in categories:
            for i in self.unicef_indicators_list:
                n = [i[0] for i in self.unicef_indicators_list if i[3] == c]
            categories_with_indicators.append([c, n])

        return categories_with_indicators

    def get_categories_with_indicators_list(self):
        c = self.get_categories_with_indicators()
        c.insert(0, ["Select Category", ["",""]])

        return c

    def get_indicators_color_dict(self):
        indicators = self.unicef_indicators_list
        color_dict = {}
        for i in indicators:
            color_dict[i[0]] = (("Low", float(i[4]), float(i[5]),"cyan"),
                                ("Medium", float(i[6]), float(i[7]),"orange"),
                                ("High", float(i[8]), float(i[9]),"red"))

        return color_dict

    def get_indicator_name(self, indicator_code):
        for i in self.unicef_indicators_list:
            if i[0] == indicator_code:
                return i[1]


def get_field(layer, fieldName):

    return [f for f in layer.fields().toList() if f.name() == fieldName][0]


def get_list_of_fields(layer, fields):

    fieldsList = []
    features = layer.getFeatures()
    for f in features:
        attr = f.attributes()
        fList = []
        for field in fields:
            fList.append(f[layer.fieldNameIndex(field)])

        fieldsList.append(fList)

    return fieldsList


def copy_vector_layer(layer, outputname):
    features = [f for f in layer.getFeatures()]

    copylayer = QgsVectorLayer("Polygon?crs={}".format(layer.crs().authid().lower()), outputname, "memory")

    data = copylayer.dataProvider()
    attr = layer.dataProvider().fields().toList()
    data.addAttributes(attr)
    copylayer.updateFields()
    data.addFeatures(features)

    QgsMapLayerRegistry.instance().addMapLayer(copylayer)


# def add_stat_to_layer(layer, stat, statIndex, summIndex, statDict):
#
#     if stat == "PERCENTAGE":
#         sumDict = {}
#         total = 0
#         features = layer.getFeatures()
#         for f in features:
#             attr = f.attributes()
#             sumDict[attr[summIndex]] = sum(statDict[attr[summIndex]])
#             total += sum(statDict[attr[summIndex]])
#
#         features2 = layer.getFeatures()
#         for f in features2:
#             layer.startEditing()
#             attr = f.attributes()
#             f[statIndex] = round(100.0*sumDict[attr[summIndex]]/total, 2)
#             layer.updateFeature(f)
#
#     else:
#         features = layer.getFeatures()
#         for f in features:
#             try:
#                 layer.startEditing()
#                 attr = f.attributes()
#
#                 if stat == "SUM":
#                     f[statIndex] = sum(statDict[attr[summIndex]])
#                 if stat == "MEAN":
#                     f[statIndex] = 1.0*sum(statDict[attr[summIndex]])/len(statDict[attr[summIndex]])
#                 if stat == "MIN":
#                     f[statIndex] = min(statDict[attr[summIndex]])
#                 if stat == "MAX":
#                     f[statIndex] = max(statDict[attr[summIndex]])
#
#                 layer.updateFeature()
#
#             except:
#                 pass
#
#             layer.commitChanges()


def add_labels(layer, stat):

    symbol = layer.rendererV2().symbols()[0]
    symbol.setColor(QColor(243,226,138))
    layer.triggerRepaint()

    palayer = QgsPalLayerSettings()
    palayer.readFromLayer(layer)
    palayer.enabled = True

    palayer.fieldName = stat

    palayer.placement = QgsPalLayerSettings.OverPoint
    palayer.fontSizeInMapUnits = False
    palayer.textFont.setPointSize(10)
    palayer.textColor = QColor(0,0,0)
    palayer.writeToLayer(layer)
