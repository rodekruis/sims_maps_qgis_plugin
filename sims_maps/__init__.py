# encoding: utf-8
#-----------------------------------------------------------
# Copyright (C) 510, The Netherlands Red Cross
# Aron Gergely
# Raymond Nijssen
#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------

import os
from datetime import datetime
from functools import partial

from PyQt5.QtWidgets import QAction, QMessageBox, QLineEdit, QCheckBox, QToolButton
from PyQt5.QtCore import QFile, Qt
from PyQt5.QtXml import QDomDocument
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi
from qgis.gui import QgsLayoutDesignerInterface
from qgis.core import (QgsProject,
                       QgsPrintLayout,
                       QgsReadWriteContext)
from .logos import RcLogos


def classFactory(iface):
    return SimsMaps(iface)


class SimsMaps:

    def __init__(self, iface):
        self.iface = iface
        self.pluginDir = os.path.dirname(__file__)
        self.dataPath = os.path.join(self.pluginDir, u'data')
        self.logos = RcLogos()
        self.logos.readFromCsv(os.path.join(self.dataPath, u'logos', u'logos.csv'))


    def initGui(self):
        print(u'initGui')

        self.toolBar = self.iface.addToolBar(u'SIMS')
        #self.toolButtonCreateLayout = QToolButton()
        #self.toolBar.addAction(self.toolButtonCreateLayout)
        icon = QIcon(os.path.join(self.pluginDir, u'create_layout_crystal.svg'))
        self.actionCreateLayout = QAction(icon, u'SIMS Maps Cross', parent=self.iface.mainWindow())
        self.toolBar.addAction(self.actionCreateLayout)
        '''
        w = self.toolBar.widgetForAction(self.actionCreateLayout)
        print(w)
        w.setPopupMode(QToolButton.MenuButtonPopup)
        self.toolButtonCreateLayout = self.toolBar.addAction(self.actionCreateLayout)
        print(self.actionCreateLayout)
        '''

        dialogFile = os.path.join(self.pluginDir, u'create_layout_dialog.ui')
        self.createLayoutDialog = loadUi(dialogFile)
        self.createLayoutDialog.buttonBox.accepted.connect(self.createLayout)

        # connections
        self.iface.layoutDesignerOpened.connect(self.designerOpened)
        self.iface.layoutDesignerClosed.connect(self.designerClosed)
        self.actionCreateLayout.triggered.connect(self.showLayoutDialog)
        self.createLayoutDialog.comboBoxNsLogo.currentIndexChanged.connect(self.updateLabelPreview)

        # TODO: loop existing designers to add connections and actions

        print(u'initGui finished')


    def unload(self):
        try:
            self.iface.layoutDesignerOpened.disconnect()
        except Exception:
            pass
        try:
            self.iface.layoutDesignerClosed.disconnect()
        except Exception:
            pass
        try:
            self.actionCreateLayout.triggered.disconnect()
        except Exception:
            pass

        # remove toolBar
        self.iface.removeToolBarIcon(self.actionCreateLayout)
        self.iface.mainWindow().removeToolBar(self.toolBar)
        del self.toolBar

        # TODO: loop designers to remove connections and actions


    def showLayoutDialog(self):
        print(u'createLayoutDialog()')

        cb = self.createLayoutDialog.comboBoxTemplate
        while cb.count() > 0:
            cb.removeItem(0)

        #cb.addItem('')
        for file in os.listdir(self.dataPath):
            if file.endswith(u'.qpt'):
                cb.addItem(file)

        # ns logos
        cb = self.createLayoutDialog.comboBoxNsLogo
        while cb.count() > 0:
            cb.removeItem(0)
        for fn in self.logos.getFileNames():
            cb.addItem(fn)

        #cb.addItem(u'croissant_rouge_tunisien.svg')
        #cb.addItem(u'Sierra Leone Red Cross.svg')


        self.createLayoutDialog.show()


    def createLayout(self):
        print(u'createLayout()')

        templateFile = self.createLayoutDialog.comboBoxTemplate.currentText()
        templateQpt = os.path.join(self.dataPath, templateFile)

        layoutName = self.createLayoutDialog.lineEditName.text()

        project = QgsProject.instance()
        layoutManager = project.layoutManager()

        oldLayout = layoutManager.layoutByName(layoutName)
        if oldLayout is not None:
            print(u'removing: {}'.format(oldLayout))
            layoutManager.removeLayout(oldLayout)

        # create new layout
        layout = QgsPrintLayout(project)

        # load layout template
        fl = QFile(templateQpt)
        doc = QDomDocument()
        doc.setContent(fl)
        layout.loadFromTemplate(doc, QgsReadWriteContext())

        # set name
        layout.setName(layoutName)

        # set map properties
        map = self.getItemById(layout, u'RC_map')
        if map is not None:
            #print(map.crs().description())
            map.zoomToExtent(self.iface.mapCanvas().extent())

        # set overview map
        # set scale
        # set page size

        # set Copyright
        # evt. automatisch: [%'© SIMS '  || year(now())%]
        '''
        label = self.getItemById(layout, u'COPYRIGHT')
        if label is not None:
            print(label)
            label.setText(u'© SIMS {0}'.format(datetime.now().year))

        # set filename
        label = self.getItemById(layout, u'FILENAME')
        if label is not None:
            print(label)
            filename = QgsProject.instance().fileName()
            if filename == u'':
                filename = u'filename unknown, project not saved'
            label.setText(filename)
        '''

        # set logo
        picture = self.getItemById(layout, u'RC_logo')
        if picture is not None:
            logoChoice = self.createLayoutDialog.comboBoxNsLogo.currentText()
            logoSvg = os.path.join(self.dataPath, u'logos', logoChoice)
            print(logoSvg)
            picture.setPicturePath(logoSvg)



        # clear default label values

        # add to project and open designer window
        layoutManager.addLayout(layout)
        self.d = self.iface.openLayoutDesigner(layout)


    def editTitleblock(self, designer):
        self.layoutConfiguration = [
            {u'code': u'RC_title', u'label': designer.dialog.labelRcTitle, u'edit': designer.dialog.lineEditRcTitle},

        ]

        for configurationItem in self.layoutConfiguration:
            #print(configurationItem)
            label = configurationItem[u'label']
            edit = configurationItem[u'edit']
            #edit.setClearButtonEnabled(True)

            layoutItem = self.getItemById(designer.layout(), configurationItem[u'code'])
            #print(layoutItem)
            if layoutItem is not None:
                if label is not None:
                    label.setEnabled(True)
                edit.setEnabled(True)
                if isinstance(edit, QLineEdit):
                    edit.setText(layoutItem.text())
                if isinstance(edit, QCheckBox):
                    #print(u'checkbox:', layoutItem.visible())
                    edit.setChecked(layoutItem.isVisible())
            else:
                if label is not None:
                    label.setEnabled(False)
                edit.setEnabled(False)
                if isinstance(edit, QLineEdit):
                    edit.setText(u'')
                if isinstance(edit, QCheckBox):
                    edit.setChecked(False)

        designer.dialog.show()


    def updateDesigner(self, designer):
        print(u'updateDesigner')

        for configurationItem in self.layoutConfiguration:
            label = configurationItem[u'label']
            print(label)
            edit = configurationItem[u'edit']
            print(edit)
            if edit.isEnabled():
                layoutItem = self.getItemById(designer.layout(), configurationItem['code'])
                if layoutItem is not None:
                    if isinstance(edit, QLineEdit):
                        layoutItem.setText(edit.text())
                    if isinstance(edit, QCheckBox):
                        layoutItem.setVisibility(edit.isChecked())

        designer.layout().refresh()


    def designerOpened(self, designer):
        print(u'opened')

        dialogFile = os.path.join(self.pluginDir, u'edit_layout_dialog.ui')
        designer.dialog = loadUi(dialogFile)
        designer.dialog.buttonBox.accepted.connect(partial(self.updateDesigner, designer))

        tb = designer.actionsToolbar()
        icon = QIcon(os.path.join(self.pluginDir, u'create_layout_crystal.svg'))
        action = QAction(icon, u'Edit SIMS map', parent=designer)
        action.triggered.connect(partial(self.editTitleblock, designer))

        tb.addAction(action)

        print(u'opened finished')


    def designerClosed(self):
        print(u'closed')


    def getItemById(self, layout, itemId):
        item = layout.itemById(itemId)
        if item is None:
            print(u'Layout does not contain item: \'{0}\''.format(itemId))
            return None
        return item

    def updateLabelPreview(self):
        #self.createLayoutDialog.labelImagePreview.setAlignment(Qt.AlignCenter)
        #milis_logo.setAlignment(Qt.AlignCenter)
        filename = self.createLayoutDialog.comboBoxNsLogo.currentText()
        filename = os.path.join(self.dataPath, u'logos', filename)
        print(filename)
        pm = QPixmap(filename)
        w = self.createLayoutDialog.labelImagePreview.width()
        h = self.createLayoutDialog.labelImagePreview.height()
        self.createLayoutDialog.labelImagePreview.setPixmap(pm.scaled(w, h, Qt.KeepAspectRatio))
