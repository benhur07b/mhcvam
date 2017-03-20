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
import re

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

# indicators_path = os.path.dirname(__file__) + '/indicators.csv'

class Indicators():

    def __init__(self, indicators_path):
        self.indicators_path = indicators_path
        self.indicators_list = self.get_indicators_list()
        self.unique_agencies = self.get_unique_agencies()
        self.agencies_with_indicators_list = self.get_agencies_with_indicators_list()
        self.agencies_list = [a[0] for a in self.agencies_with_indicators_list]
        self.unique_categories = self.get_unique_categories()
        self.categories_with_indicators_list = self.get_categories_with_indicators_list()
        self.categories_list = [c[0] for c in self.categories_with_indicators_list]


    def get_indicators_list(self):
        with open(self.indicators_path, 'rb') as f:
            reader = csv.reader(f)
            return list(reader)[1:]

    def get_indicator_codes(self):

        return [i[0] for i in self.indicators_list]

    def get_indicator_names(self):

        return [i[1] for i in self.indicators_list]

    def get_indicator_name_from_code(self, indicator_code):

        if indicator_code in self.get_indicator_codes():
            for i in self.indicators_list:
                if i[0] == indicator_code:
                    return i[1]
        else:
            return indicator_code

    def get_indicator_code_from_name(self, indicator_name):

        if indicator_name in self.get_indicator_names():
            for i in self.indicators_list:
                if i[1] == indicator_name:
                    return i[0]
        else:
            return indicator_name


    def get_unique_agencies(self):
        agencies = [a[2] for a in self.indicators_list]
        return sorted(list(set(agencies)))

    def get_agencies_with_indicators(self):
        agencies = self.unique_agencies
        agencies_with_indicators = []
        for a in agencies:
            for i in self.indicators_list:
                n = [i[0] for i in self.indicators_list if i[2] == a]
            agencies_with_indicators.append([a, n])

        return agencies_with_indicators

    def get_agencies_with_indicators_list(self):
        a = self.get_agencies_with_indicators()
        a.insert(0, ["Select Agency", ("","")])

        return a

    def get_unique_categories(self):
        categories = [a[3] for a in self.indicators_list]
        return sorted(list(set(categories)))

    def get_categories_with_indicators(self):
        categories = self.unique_categories
        categories_with_indicators = []
        for c in categories:
            for i in self.indicators_list:
                n = [i[0] for i in self.indicators_list if i[3] == c]
            categories_with_indicators.append([c, n])

        return categories_with_indicators

    def get_categories_with_indicators_list(self):
        c = self.get_categories_with_indicators()
        c.insert(0, ["Select Category", ["",""]])

        return c

    def convert_to_query(self, text):

        split = splitter(text)
        split_codes = [self.get_indicator_code_from_name(s.replace('"', '')) for s in split]

        text = " ".join(split_codes)
        text = text.replace("equal to", "=")
        text = text.replace(" or ", "")
        text = text.replace("not ", "!")
        text = text.replace("greater than", ">")
        text = text.replace("less than", "<")

        return text


class UNICEFBrgyIndicators(Indicators):

    def __init__(self, indicators_path):
        Indicators.__init__(self, indicators_path)
        self.color_dict = self.get_indicators_color_dict()


    def get_indicators_color_dict(self):
        indicators = self.indicators_list
        color_dict = {}
        for i in indicators:
            color_dict[i[0]] = (("Low", get_value(i[4]), get_value(i[5]),"cyan"),
                                ("Medium", get_value(i[6]), get_value(i[7]),"orange"),
                                ("High", get_value(i[8]), get_value(i[9]),"red"))

        return color_dict


def get_value(num):
    try:
        return float(num)
    except ValueError:
        return num


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


# def convert_to_query(text):
#
#     text = text.replace("equal to", "=")
#     text = text.replace(" or ", "")
#     text = text.replace("not ", "!")
#     text = text.replace("greater than", ">")
#     text = text.replace("less than", "<")
#
#     return text


def splitter(s):

    def replacer(m):
        return m.group(0).replace(" ", "\x00")

    parts = re.sub('".+?"', replacer, s).split()
    parts = [p.replace("\x00", " ") for p in parts]
    return parts


def read_hazard_level(text):

    return text.capitalize()


def clear_all_layer_selection(self):

    lyrs = QgsMapLayerRegistry.instance().mapLayers()
    for lyr in lyrs:
        lyrs[lyr].clearSelection()


def clear_all_feature_filters(self):

    lyrs = QgsMapLayerRegistry.instance().mapLayers()
    for lyr in lyrs:
        lyrs[lyr].setSubsetString('')
