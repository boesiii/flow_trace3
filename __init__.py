# -*- coding: utf-8 -*-
"""
/***************************************************************************
 flowTrace
                                 A QGIS plugin
 Select line segments upstream of a selected line segment
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2019-01-18
        copyright            : (C) 2019 by Ed B
        email                : boesiii@yahoo.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load flowTrace class from file flowTrace.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .flow_trace import flowTrace
    return flowTrace(iface)