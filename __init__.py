# -*- coding: utf-8 -*-
"""
/***************************************************************************
 UserManual
                                 A QGIS plugin
 Integrated QGIS User Manual
                             -------------------
        begin                : 2016-04-06
        copyright            : (C) 2016 by Sourcepole
        email                : pka@sourcepole.ch
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
    """Load UserManual class from file UserManual.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .user_manual import UserManual
    return UserManual(iface)
