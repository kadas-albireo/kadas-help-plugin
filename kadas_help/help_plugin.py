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

from qgis.core import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
try:
    from PyQt5.QtWebKitWidgets import QWebView
    HAVE_WEBKIT = True
except Exception as e:
    QMessageBox.information(None, "Debug", str(e))
    HAVE_WEBKIT = False
from kadas.kadascore import *
from kadas.kadasgui import *


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
        self.iface.mainWindowClosed.connect(self.closeHelpWindow)

        self.server = KadasFileServer(docdir, "127.0.0.1")
        QgsLogger.debug("Help server running on {host}:{port}".format(host=self.server.getHost(), port=self.server.getPort()))
        self.helpAction = self.iface.findAction("mActionHelp")
        self.helpAction.triggered.connect(self.showHelp)

        if os.path.isdir(os.path.join(docdir, self.locale)):
            self.lang = self.locale
        else:
            self.lang = 'en'

    def unload(self):
        self.helpWidget = None
        self.helpAction = None

    def showHelp(self):
        docdir = os.path.join(self.plugin_dir, "html")


        url = QUrl("http:///{host}:{port}/{lang}/".format(
            host=self.server.getHost(), port=self.server.getPort(), lang=self.lang))

        if not HAVE_WEBKIT:
            QDesktopServices.openUrl(url)
        else:
            if not self.helpWidget:
                self.helpWidget = QWebView()
                self.helpWidget.setWindowTitle(self.tr('KADAS User Manual'))
                self.helpWidget.resize(1024, 768)
                self.timer = QTimer()
                self.timer.setInterval(250)
                self.timer.setSingleShot(True)
                self.timer.timeout.connect(self.raiseHelpWindow)
            self.helpWidget.load(url)
            self.timer.start()

    def raiseHelpWindow(self):
            self.helpWidget.show()
            self.helpWidget.raise_()

    def closeHelpWindow(self):
        if self.helpWidget:
            self.helpWidget.close()
