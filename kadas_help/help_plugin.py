# -*- coding: utf-8 -*-
"""
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os


from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
try:
    from PyQt5.QtWebKitWidgets import QWebView
    HAVE_WEBKIT = True
except Exception as e:
    QMessageBox.information(None, "Debug", str(e))
    HAVE_WEBKIT = False
from kadas.kadasgui import *

from .http_server import HttpServer


class HelpPlugin:

    def __init__(self, iface):
        self.iface = KadasPluginInterface.cast(iface)
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        self.locale = QSettings().value('locale/userLocale', 'en')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'KadasHelp_{}.qm'.format(self.locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        self.helpWidget = None
        self.helpAction = None

    def tr(self, message):
        return QCoreApplication.translate('UserManual', message)

    def initGui(self):
        docdir = os.path.join(self.plugin_dir, "html")
        if os.path.isdir(os.path.join(docdir, self.locale)):
            lang = self.locale
        else:
            lang = 'en'
        docdir = os.path.join(docdir, lang)

        self.server = HttpServer(docdir, "127.0.0.1")
        self.helpAction = self.iface.findAction("mActionHelp")
        self.helpAction.triggered.connect(self.showHelp)
        self.server.start()

    def unload(self):
        self.server.shutdown()
        self.helpWidget = None
        self.helpAction = None

    def showHelp(self):
        url = QUrl("http:///{host}:{port}/".format(
            host=self.server.host, port=self.server.port))

        if not HAVE_WEBKIT:
            QDesktopServices.openUrl(url)
        else:
            if self.helpWidget is None:
                # Create the widget (after translation) and keep reference
                self.helpWidget = QWebView()
                self.helpWidget.setWindowTitle(self.tr('KADAS User Manual'))
                self.helpWidget.resize(1024, 768)
                self.helpWidget.load(url)

            self.helpWidget.show()
            self.helpWidget.raise_()
