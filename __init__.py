# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QgisNM
                                 A QGIS plugin
 this plugin does noise stuff
                             -------------------
        begin                : 2017-08-10
        copyright            : (C) 2017 by tom
        email                : tomd@wilkinsonmurray.com.au
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
    """Load QgisNM class from file QgisNM.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .post_Processor import QgisNM
    return QgisNM(iface)
