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
        l.setVerticalSpacing(5)
        self.setLayout(l)

        splashLabel = QLabel()
        splashLabel.setPixmap(QPixmap(":/plugins/UserManual/splash.png"))
        l.addWidget(splashLabel, l.rowCount(), 0, 1, 2)

        versionLabel = QLabel(self.tr("<b>Version</b>: %s") % (QGis.QGIS_BUILD_DATE))
        versionLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        l.addWidget(versionLabel, l.rowCount(), 0, 1, 1)

        licenseLabel = QLabel(self.tr("This software is released under the <a href=\"http://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html\">GNU Public License (GPL) Version 2</a>"))
        licenseLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        licenseLabel.setOpenExternalLinks(True)
        licenseLabel.setWordWrap(True)
        l.addWidget(licenseLabel, l.rowCount(), 0, 1, 1)
        mssLabel = QLabel(self.tr("The MSS/MilX components are property of <a href=\"http://www.gs-soft.com/\">gs-soft AG</a>"))
        mssLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        mssLabel.setOpenExternalLinks(True)
        mssLabel.setWordWrap(True)
        l.addWidget(mssLabel, l.rowCount(), 0, 1, 1)

        adminLogo = QLabel()
        adminLogo.setPixmap(QPixmap(":/plugins/UserManual/adminch.png"))
        adminLogo.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        l.addWidget(adminLogo, 2, 1, 3, 1)

        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        l.addWidget(hline, l.rowCount(), 0, 1, 1)

        hline2 = QFrame()
        hline2.setFrameShape(QFrame.HLine)
        hline2.setFrameShadow(QFrame.Sunken)
        l.addWidget(hline2, l.rowCount() - 1, 1, 1, 1)

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
        swisstopoDataTermsLink.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        swisstopoDataTermsLink.setOpenExternalLinks(True)
        l.addWidget(swisstopoDataTermsLink, l.rowCount(), 0, 1, 1)

        swissGDIdataTermsLink = QLabel("<a href=\"http://www.toposhop.admin.ch/%s/shop/terms/use/geodata_business\">%s</a>" % (locale, self.tr("Terms of use for Swiss GDI geodata")))
        swissGDIdataTermsLink.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        swissGDIdataTermsLink.setOpenExternalLinks(True)
        l.addWidget(swissGDIdataTermsLink, l.rowCount(), 0, 1, 1)

        dataContactLink = QLabel("<a href=\"http://www.geo.admin.ch/internet/geoportal/%s/home/geoadmin/contact.htm\">%s<a>" % (locale, self.tr("Data management and controller contacts")))
        dataContactLink.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        dataContactLink.setOpenExternalLinks(True)
        l.addWidget(dataContactLink, l.rowCount(), 0, 1, 1)

        disclaimerLinkMap = {"en" : "https://www.admin.ch/gov/en/start/terms-and-conditions.html",
                             "de" : "https://www.admin.ch/gov/de/start/rechtliches.html",
                             "it" : "https://www.admin.ch/gov/it/pagina-iniziale/basi-legali.html",
                             "fr" : "https://www.admin.ch/gov/fr/accueil/conditions-utilisation.html"}
        disclaimerLink = QLabel("<a href=\"%s\">%s<a>" % (disclaimerLinkMap[locale], self.tr("Data usage liability disclaimer")))
        disclaimerLink.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        disclaimerLink.setOpenExternalLinks(True)
        l.addWidget(disclaimerLink, l.rowCount(), 0, 1, 1)

        addressLabel = QLabel(self.tr("<b>Swiss Army<br />Mil Geo Info D<br />VZ VBS<br />3003 Bern</b>"))
        addressLabel.setAlignment(Qt.AlignLeft)
        addressLabel.setIndent(38)
        l.addWidget(addressLabel, 6, 1, 4, 1)

        bbox = QDialogButtonBox(QDialogButtonBox.Close)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        l.addWidget(bbox, l.rowCount(), 0, 1, 2)

        self.setFixedSize(self.sizeHint())
