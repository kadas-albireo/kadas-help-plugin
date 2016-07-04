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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import os
import resources


class AboutDialog(QDialog):
    def __init__(self, locale, parent):
        QDialog.__init__(self, parent)

        self.setWindowTitle(self.tr("About %s") % (QGis.QGIS_FULL_RELEASE_NAME))
        l = QGridLayout()
        self.setLayout(l)

        splashLabel = QLabel()
        splashLabel.setPixmap(QPixmap(":/plugins/UserManual/splash.png"))
        l.addWidget(splashLabel, l.rowCount(), 0, 1, 1)

        l.addWidget(QLabel(self.tr("<b>Version</b>: %s") % (QGis.QGIS_BUILD_DATE)))

        licenseLabel = QLabel(self.tr("This software is released under the <a href=\"http://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html\">GNU Public License (GPL) Version 2</a>"))
        licenseLabel.setOpenExternalLinks(True)
        l.addWidget(licenseLabel, l.rowCount(), 0, 1, 1)
        mssLabel = QLabel(self.tr("The MSS/MilX components are property of <a href=\"http://www.gs-soft.com/\">gs-soft AG</a>"))
        mssLabel.setOpenExternalLinks(True)
        l.addWidget(mssLabel, l.rowCount(), 0, 1, 1)

        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        l.addWidget(hline, l.rowCount(), 0, 1, 1)

        pdfpath = os.path.join(
            os.path.dirname(__file__), "doc",
            "Nutzungsbestimmungen_Daten_swisstopo_KADAS_Albireo_%s.pdf")
        if os.path.isfile(pdfpath % locale):
            lang = locale
        else:
            lang = 'de'
        print(pdfpath % locale)
        swisstopoDataTermsLink = QLabel(
            "<a href=\"file:///%s\">%s</a>" % (
                pdfpath % lang, self.tr("Terms of use for swisstopo geodata")))
        swisstopoDataTermsLink.setOpenExternalLinks(True)
        l.addWidget(swisstopoDataTermsLink, l.rowCount(), 0, 1, 1)

        swissGDIdataTermsLink = QLabel("<a href=\"http://www.toposhop.admin.ch/%s/shop/terms/use/geodata_business\">%s</a>" % (locale, self.tr("Terms of use for Swiss GDI geodata")))
        swissGDIdataTermsLink.setOpenExternalLinks(True)
        l.addWidget(swissGDIdataTermsLink, l.rowCount(), 0, 1, 1)

        dataContactLink = QLabel("<a href=\"http://www.geo.admin.ch/internet/geoportal/%s/home/geoadmin/contact.htm\">%s<a>" % (locale, self.tr("Data management and controller contacts")))
        dataContactLink.setOpenExternalLinks(True)
        l.addWidget(dataContactLink, l.rowCount(), 0, 1, 1)

        disclaimerLinkMap = {"en" : "https://www.admin.ch/gov/en/start/terms-and-conditions.html",
                             "de" : "https://www.admin.ch/gov/de/start/rechtliches.html",
                             "it" : "https://www.admin.ch/gov/it/pagina-iniziale/basi-legali.html",
                             "fr" : "https://www.admin.ch/gov/fr/accueil/conditions-utilisation.html"}
        disclaimerLink = QLabel("<a href=\"%s\">%s<a>" % (disclaimerLinkMap[locale], self.tr("Data usage liability disclaimer")))
        disclaimerLink.setOpenExternalLinks(True)
        l.addWidget(disclaimerLink, l.rowCount(), 0, 1, 1)

        bbox = QDialogButtonBox(QDialogButtonBox.Close)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        l.addWidget(bbox, l.rowCount(), 0, 1, 1)

        self.setFixedSize(self.sizeHint())
