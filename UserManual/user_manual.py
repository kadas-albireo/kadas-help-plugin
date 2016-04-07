# -*- coding: utf-8 -*-
"""
/***************************************************************************
 UserManual
                                 A QGIS plugin
 Integrated QGIS User Manual
                              -------------------
        begin                : 2016-04-06
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Sourcepole
        email                : pka@sourcepole.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt, QUrl
from PyQt4.QtGui import QAction, QIcon
from PyQt4.QtWebKit import QWebView
# Initialize Qt resources from file resources.py
import resources
import os.path

from about_dialog import AboutDialog


class UserManual:
    """QGIS Plugin Implementation."""

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
        self.locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'UserManual_{}.qm'.format(self.locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        self.helpWidget = None
        self.aboutWidget = None
        self.helpAction = None
        self.aboutAction = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('UserManual', message)

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self.helpAction = self.iface.findAction("mActionHelp")
        if not self.helpAction and self.iface.helpToolBar():
            self.helpAction = QAction(QIcon(":/plugins/UserManual/icon.png"), self.tr("Help"), self.iface.helpToolBar())
            self.iface.helpToolBar().addAction(self.helpAction)
        if self.helpAction:
            self.helpAction.triggered.connect(self.showHelp)

        self.aboutAction = self.iface.findAction("mActionAbout")
        if not self.aboutAction and self.iface.helpToolBar():
            self.aboutAction = QAction(QIcon(":/plugins/UserManual/about.png"), self.tr("About"), self.iface.helpToolBar())
            self.iface.helpToolBar().addAction(self.aboutAction)
        if self.aboutAction:
            self.aboutAction.triggered.connect(self.showAbout)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        if self.iface.helpToolBar():
            self.iface.helpToolBar().removeAction(self.helpAction)
        if self.helpAction:
            self.helpAction.triggered.disconnect(self.showHelp)
        if self.iface.helpToolBar():
            self.iface.helpToolBar().removeAction(self.aboutAction)
        if self.aboutAction:
            self.aboutAction.triggered.disconnect(self.showAbout)
        self.helpWidget = None
        self.helpAction = None
        self.aboutAction = None

    def showHelp(self):
        """Run method that loads and starts the plugin"""
        if self.helpWidget is None:
            # Create the widget (after translation) and keep reference
            self.helpWidget = QWebView()
            self.helpWidget.setWindowTitle(self.tr('User Manual'))
            self.helpWidget.resize(500, 600)

            docdir = os.path.join(self.plugin_dir, "html")
            if os.path.isdir(os.path.join(docdir, self.locale)):
                lang = self.locale
            else:
                lang = 'en'

            url = QUrl("file://{dir}/{lang}/docs/user_manual/index.html".format(
                dir=docdir, lang=lang))
            self.helpWidget.load(url)

        self.helpWidget.show()
        self.helpWidget.raise_()

    def showAbout(self):
        """Run method that loads and starts the plugin"""
        locale = self.locale
        if not locale in ['en', 'de', 'it', 'fr']:
            locale = 'en'
        if self.aboutWidget is None:
            self.aboutWidget = AboutDialog(locale, self.iface.mainWindow())
        self.aboutWidget.show()
        self.aboutWidget.raise_()
