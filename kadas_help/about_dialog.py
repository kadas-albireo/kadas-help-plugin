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
        splashLabel.setPixmap(QPixmap(":/plugins/UserManual/splash.jpg"))
        l.addWidget(splashLabel, l.rowCount(), 0, 1, 2)

        versionLabel = QLabel(self.tr("<b>Version</b>: %s (%s)") % (QGis.QGIS_RELEASE_VERSION, QGis.QGIS_BUILD_DATE))
        versionLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        l.addWidget(versionLabel, l.rowCount(), 0, 1, 1)

        licenseLabel = QLabel(self.tr("This software is released under the <a href=\"http://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html\">GNU Public License (GPL) Version 2</a>"))
        licenseLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        licenseLabel.setOpenExternalLinks(True)
        licenseLabel.setWordWrap(True)
        l.addWidget(licenseLabel, l.rowCount(), 0, 1, 1)
        mssLabel = QLabel(self.tr("The MSS/MilX components are property of gs-soft AG"))
        mssLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
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

        swisstopoDataTermsLink = QLabel(
            "<a href=\"file:///%s\">%s</a>" % (
                pdfpath % lang, self.tr("Terms of use for swisstopo geodata")))
        swisstopoDataTermsLink.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        swisstopoDataTermsLink.setOpenExternalLinks(True)
        l.addWidget(swisstopoDataTermsLink, l.rowCount(), 0, 1, 1)

        gdiTermsLinkMap = {"en": "https://www.geo.admin.ch/en/about-swiss-geoportal/responsabilities-and-contacts.html",
                           "de": "https://www.geo.admin.ch/de/ueber-geo-admin/impressum.html",
                           "it": "https://www.geo.admin.ch/it/geo-admin-ch/colophon.html",
                           "fr": "https://www.geo.admin.ch/fr/geo-admin-ch/impressum.html"}
        swissGDIdataTermsLink = QLabel("<a href=\"%s\">%s</a>" % (gdiTermsLinkMap[locale], self.tr("Terms of use for Swiss GDI geodata")))
        swissGDIdataTermsLink.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        swissGDIdataTermsLink.setOpenExternalLinks(True)
        l.addWidget(swissGDIdataTermsLink, l.rowCount(), 0, 1, 1)

        dataContactLink = QLabel("<a href=\"mailto:GeoSupport.OP@vtg.admin.ch\">%s<a>" % (self.tr("Data management and controller contact")))
        dataContactLink.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        dataContactLink.setOpenExternalLinks(True)
        l.addWidget(dataContactLink, l.rowCount(), 0, 1, 1)

        disclaimerLinkMap = {"en": "https://www.admin.ch/gov/en/start/terms-and-conditions.html",
                             "de": "https://www.admin.ch/gov/de/start/rechtliches.html",
                             "it": "https://www.admin.ch/gov/it/pagina-iniziale/basi-legali.html",
                             "fr": "https://www.admin.ch/gov/fr/accueil/conditions-utilisation.html"}
        disclaimerLink = QLabel("<a href=\"%s\">%s<a>" % (disclaimerLinkMap[locale], self.tr("Data usage liability disclaimer")))
        disclaimerLink.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        disclaimerLink.setOpenExternalLinks(True)
        l.addWidget(disclaimerLink, l.rowCount(), 0, 1, 1)

        addressLabel = QLabel(self.tr("<b>Swiss Armed Forces<br />Mil Geo Info D<br />VZ VBS<br />3003 Bern</b>"))
        addressLabel.setAlignment(Qt.AlignLeft)
        addressLabel.setIndent(38)
        l.addWidget(addressLabel, 6, 1, 4, 1)

        bbox = QDialogButtonBox(QDialogButtonBox.Close)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        l.addWidget(bbox, l.rowCount(), 0, 1, 2)

        self.setFixedSize(self.sizeHint())
