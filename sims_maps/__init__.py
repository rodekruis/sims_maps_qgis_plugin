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

from PyQt5.QtWidgets import (QAction,
                             QMessageBox,
                             QLineEdit,
                             QCheckBox,
                             QToolButton)
from PyQt5.QtCore import (QFile,
                          Qt,
                          QSettings,
                          QCoreApplication,
                          QTranslator,
                          qVersion)
from PyQt5.QtXml import QDomDocument
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi
from qgis.gui import QgsLayoutDesignerInterface
from qgis.core import (QgsProject,
                       QgsPathResolver,
                       QgsPrintLayout,
                       QgsReadWriteContext,
                       QgsApplication,
                       QgsLayoutItemLabel,
                       QgsVectorLayer,
                       QgsCoordinateReferenceSystem,
                       QgsCoordinateTransform)
from .logos import RcLogos
from .layout_config import (simsLayoutConfiguration,
                            simsDisclamers,
                            simsLogoTexts,
                            simsIfrcLogos,
                            simsMonths)
from .sims_colors import QgsSimsColorScheme


def classFactory(iface):
    return SimsMaps(iface)


class SimsMaps:

    def __init__(self, iface):
        self.iface = iface
        self.pluginDir = os.path.dirname(__file__)
        self.dataPath = os.path.join(self.pluginDir, 'data')
        self.logos = RcLogos()
        self.logos.readFromCsv(os.path.join(self.dataPath, 'logos', 'logos.csv'))
        self.worldLayerPath = os.path.join(self.dataPath, u'sims_maps_resources.gpkg|layername=world_map')
        self.worldLayerName = 'SIMS_world_overview'
        self.worldLayerId = None
        self.layoutBaseName = 'sims_layout'

        self.addIconPath()
        self.colorScheme = QgsSimsColorScheme()
        #self.addColorScheme()
        self.pathPreprocessorId = QgsPathResolver.setPathPreprocessor(self.simsMapsPathPreprocessor)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        print(locale)
        locale_path = os.path.join(
            self.pluginDir,
            'i18n',
            'sims_maps_{}.qm'.format(locale))
        print(locale_path)

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


    def tr(self, message):
        return QCoreApplication.translate('SimsMaps', message)


    def initGui(self):
        print(self.tr('initGui'))

        #QgsApplication.colorSchemeRegistry().addColorScheme(self.colorscheme)
        self.addColorScheme()

        self.toolBar = self.iface.addToolBar('SIMS Maps')
        #self.toolButtonCreateLayout = QToolButton()
        #self.toolBar.addAction(self.toolButtonCreateLayout)
        icon = QIcon(os.path.join(self.pluginDir, 'create_layout_crystal.svg'))
        self.actionCreateLayout = QAction(icon, self.tr('Create SIMS Layout'), parent=self.iface.mainWindow())
        self.toolBar.addAction(self.actionCreateLayout)

        createLayoutUi = os.path.join(self.pluginDir, 'create_layout_dialog.ui')
        self.createLayoutDialog = loadUi(createLayoutUi)
        self.createLayoutDialog.buttonBox.accepted.connect(self.createLayout)

        # connections
        self.iface.layoutDesignerOpened.connect(self.designerOpened)
        self.iface.layoutDesignerClosed.connect(self.designerClosed)
        self.actionCreateLayout.triggered.connect(self.showLayoutDialog)
        self.createLayoutDialog.comboBoxNsLogo.currentIndexChanged.connect(self.updateLabelPreview)

        # TODO: loop existing designers to add connections and actions

        #print(u'initGui finished')


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
        if self.pathPreprocessorId is not None:
            QgsPathResolver.removePathPreprocessor(self.pathPreprocessorId)
        # remove toolBar
        self.iface.removeToolBarIcon(self.actionCreateLayout)
        self.iface.mainWindow().removeToolBar(self.toolBar)
        del self.toolBar

        self.removeIconPath()
        self.removeColorScheme()
        self.removeWorldLayer()

        # TODO: loop designers to remove connections and actions

    def simsMapsPathPreprocessor(self, path):
        print(u'simsMapsPathPreprocessor()')
        pluginParentPath, pluginFolder = os.path.split(self.pluginDir)

        if not os.path.isfile(path):
            allParts = []
            while 1:
                parts = os.path.split(path)
                if parts[0] == path:
                    allParts.insert(0, parts[0])
                    break
                elif parts[1] == path:
                    allParts.insert(0, parts[1])
                    break
                else:
                    path = parts[0]
                    allParts.insert(0, parts[1])

            if pluginFolder in allParts:
                path = os.path.join(pluginParentPath, *allParts[allParts.index(pluginFolder):])

        return path

    def addIconPath(self):
        print('addIconPath')
        iconsDir = os.path.join(self.dataPath, 'SIMS-Icons')
        paths = QgsApplication.svgPaths()
        if not iconsDir in paths:
            paths.append(iconsDir)
        QgsApplication.setDefaultSvgPaths(paths)


    def removeIconPath(self):
        print('removeIconPath')
        iconsDir = os.path.join(self.dataPath, 'SIMS-Icons')
        paths = QgsApplication.svgPaths()
        i = paths.index(iconsDir)
        if i >= 0:
            del paths[i]
        QgsApplication.setDefaultSvgPaths(paths)


    def addColorScheme(self):
        #print('add simsColorScheme')
        QgsApplication.colorSchemeRegistry().addColorScheme(self.colorScheme)


    def removeColorScheme(self):
        #print(u'remove simsColorScheme')
        schemesToRemove = []
        for cs in QgsApplication.colorSchemeRegistry().schemes():
            if cs.schemeName() in ['', 'SIMS Colors']:
                schemesToRemove.append(cs)
        for cs in schemesToRemove:
            QgsApplication.colorSchemeRegistry().removeColorScheme(cs)


    def getLayoutName(self):
        # returns a unique layout name for the project
        template = self.layoutBaseName + '_{0:0>3}'

        existingNames = []
        project = QgsProject.instance()
        layoutManager = project.layoutManager()
        for layout in layoutManager.layouts():
            existingNames.append(layout.name())

        for i in range(1, 1000):
            name = template.format(i)
            if not name in existingNames:
                break

        return name


    def showLayoutDialog(self):
        #print('showLayoutDialog()')

        # templates
        cb = self.createLayoutDialog.comboBoxTemplate
        while cb.count() > 0:
            cb.removeItem(0)

        # name
        self.createLayoutDialog.lineEditName.setText(self.getLayoutName())

        # templates
        for file in sorted(os.listdir(self.dataPath), reverse=True):
            if file.endswith(u'.qpt'):
                cb.addItem(file)

        # ns logos
        cb = self.createLayoutDialog.comboBoxNsLogo
        while cb.count() > 0:
            cb.removeItem(0)
        for fn in self.logos.getFileNames():
            cb.addItem(fn)

        # languages
        cb = self.createLayoutDialog.comboBoxLanguage
        while cb.count() > 0:
            cb.removeItem(0)
        for key in simsDisclamers.keys(): # using keys in disclamers here!
            cb.addItem(key)

        self.createLayoutDialog.show()
        #print(u'showLayoutDialog() finished')


    def addWorldLayer(self):
        if self.worldLayerId is not None:
             try:
                  layer = QgsProject.instance().mapLayers()[self.worldLayerId]
                  return layer
             except KeyError:
                 pass
                 #print('World Layer not present')

        worldGpkg = os.path.join(self.dataPath, 'sims_maps_resources.gpkg' + '|layername=world_map')
        layer = self.iface.addVectorLayer(worldGpkg, self.worldLayerName, 'ogr')
        # TODO: set layer down in background

        self.worldLayerId = layer.id()
        return layer


    def removeWorldLayer(self):
        if self.worldLayerId is not None:
             try:
                  QgsProject.instance().removeMapLayers([self.worldLayerId])
             except KeyError:
                 pass
                 #print(u'World Layer not present')


    def createLayout(self):
        #print('createLayout()')

        templateFile = self.createLayoutDialog.comboBoxTemplate.currentText()
        templateQpt = os.path.join(self.dataPath, templateFile)

        layoutName = self.createLayoutDialog.lineEditName.text()

        project = QgsProject.instance()
        layoutManager = project.layoutManager()

        oldLayout = layoutManager.layoutByName(layoutName)
        if oldLayout is not None:
            #print('removing: {}'.format(oldLayout))
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
        map = self.getItemById(layout, 'RC_map')
        if map is not None:
            #print(map.crs().description())
            map.zoomToExtent(self.iface.mapCanvas().extent())

        # set default label values
        for configurationItem in simsLayoutConfiguration:
            label = self.getItemById(layout, configurationItem['code'])
            if label is not None and isinstance(label, QgsLayoutItemLabel):
                if configurationItem['default'] is not None:
                    label.setText(configurationItem['default'])

        # set overview map
        map = self.getItemById(layout, 'RC_overview')
        if map is not None:
            worldLayer = self.addWorldLayer()
            map.setFollowVisibilityPreset(False)
            map.setKeepLayerSet(True)
            map.setLayers([worldLayer])

            overviewCrs = QgsCoordinateReferenceSystem("EPSG:54030")
            map.setCrs(overviewCrs)

            extent = worldLayer.extent()
            layerCrs = worldLayer.sourceCrs()
            if not layerCrs == overviewCrs:
                transform = QgsCoordinateTransform(layerCrs, overviewCrs, QgsProject.instance())
                extent = transform.transformBoundingBox(extent)
            map.zoomToExtent(extent)

            root = QgsProject.instance().layerTreeRoot()
            rl = root.findLayer(worldLayer.id())
            rl.setItemVisibilityChecked(False)

        # set disclamer
        languageChoice = self.createLayoutDialog.comboBoxLanguage.currentText()

        label = self.getItemById(layout, 'RC_disclaimer')
        if label is not None:
            label.setText(simsDisclamers[languageChoice])

        label = self.getItemById(layout, 'RC_logotext')
        if label is not None:
            label.setText(simsLogoTexts[languageChoice])

        # set title
        label = self.getItemById(layout, 'RC_title')
        if label is not None:
            label.setText(self.createLayoutDialog.lineEditName.text())

        # set Copyright
        # possibly dynamically: [%'© SIMS '  || year(now())%]
        '''
        label = self.getItemById(layout, 'COPYRIGHT')
        if label is not None:
            print(label)
            label.setText('© SIMS {0}'.format(datetime.now().year))

        # set filename
        label = self.getItemById(layout, 'FILENAME')
        if label is not None:
            print(label)
            filename = QgsProject.instance().fileName()
            if filename == '':
                filename = 'filename unknown, project not saved'
            label.setText(filename)
        '''

        # set NS logo
        picture = self.getItemById(layout, 'RC_logo1')
        if picture is not None:
            logoChoice = self.createLayoutDialog.comboBoxNsLogo.currentText()
            logoSvg = os.path.join(self.dataPath, 'logos', logoChoice)
            picture.setPicturePath(logoSvg)

        # set IFRC logo
        picture = self.getItemById(layout, 'RC_logo2')
        if picture is not None:
            logo = simsIfrcLogos[languageChoice]
            logoSvg = os.path.join(self.dataPath, 'img', logo)
            picture.setPicturePath(logoSvg)

        # set date
        label = self.getItemById(layout, 'RC_date')
        if label is not None:
            now = datetime.now()
            month = simsMonths[languageChoice][now.month]
            label.setText(now.strftime('%d {} %Y').format(month))

        # set North Arrow
        picture = self.getItemById(layout, 'RC_northarrow')
        if picture is not None:
            logoSvg = os.path.join(QgsApplication.pkgDataPath(), 'svg', 'arrows', 'NorthArrow_02.svg')
            picture.setPicturePath(logoSvg)

        # clear default label values

        # add to project and open designer window
        layoutManager.addLayout(layout)
        designer = self.iface.openLayoutDesigner(layout)


    def editTitleblock(self, designer):

        designer.titleblockDialog.buttonBox.accepted.connect(partial(self.updateDesigner, designer))
        # TODO: Find out if this needs to be disconnected, and when

        for configurationItem in simsLayoutConfiguration:
            #print(configurationItem)
            label = self.getTitleblockWidget(designer, configurationItem['label'])
            edit = self.getTitleblockWidget(designer, configurationItem['edit'])
            #edit.setClearButtonEnabled(True)

            layoutItem = self.getItemById(designer.layout(), configurationItem['code'])
            #print(layoutItem)
            if layoutItem is not None:
                if label is not None:
                    label.setEnabled(True)
                edit.setEnabled(True)
                if isinstance(edit, QLineEdit):
                    edit.setText(layoutItem.text())
                if isinstance(edit, QCheckBox):
                    edit.setChecked(layoutItem.isVisible())
            else:
                if label is not None:
                    label.setEnabled(False)
                edit.setEnabled(False)
                if isinstance(edit, QLineEdit):
                    edit.setText(u'')
                if isinstance(edit, QCheckBox):
                    edit.setChecked(False)

        designer.titleblockDialog.show()


    def getTitleblockWidget(self, designer, name):
            if name is not None:
                widget = eval('designer.titleblockDialog.{0}'.format(name))
            else:
                widget = None
            return widget


    def updateDesigner(self, designer):
        #print('updateDesigner')

        for configurationItem in simsLayoutConfiguration:
            label = self.getTitleblockWidget(designer, configurationItem['label'])
            edit = self.getTitleblockWidget(designer, configurationItem['edit'])
            if edit.isEnabled():
                layoutItem = self.getItemById(designer.layout(), configurationItem['code'])
                if layoutItem is not None:
                    if isinstance(edit, QLineEdit):
                        layoutItem.setText(edit.text())
                    if isinstance(edit, QCheckBox):
                        layoutItem.setVisibility(edit.isChecked())

        designer.layout().refresh()


    def designerOpened(self, designer):
        #print('opened')

        dialogFile = os.path.join(self.pluginDir, 'edit_layout_dialog.ui')
        designer.dialog = loadUi(dialogFile)
        designer.dialog.buttonBox.accepted.connect(partial(self.updateDesigner, designer))

        tb = designer.actionsToolbar()
        icon = QIcon(os.path.join(self.pluginDir, 'create_layout_crystal.svg'))
        action = QAction(icon, self.tr('Edit SIMS Layout'), parent=designer)
        action.triggered.connect(partial(self.editTitleblock, designer))
        tb.addAction(action)

        titleblockUi = os.path.join(self.pluginDir, 'edit_layout_dialog.ui')
        designer.titleblockDialog = loadUi(titleblockUi)

        #print(u'opened finished')

    def designerClosed(self):
        pass
        #print('closed')

    def getItemById(self, layout, itemId):
        item = layout.itemById(itemId)
        if item is None:
            #print('Layout does not contain item: \'{0}\''.format(itemId))
            return None
        return item

    def updateLabelPreview(self):
        #self.createLayoutDialog.labelImagePreview.setAlignment(Qt.AlignCenter)
        #milis_logo.setAlignment(Qt.AlignCenter)
        filename = self.createLayoutDialog.comboBoxNsLogo.currentText()
        filename = os.path.join(self.dataPath, 'logos', filename)
        #print(filename)
        pm = QPixmap(filename)
        w = self.createLayoutDialog.labelImagePreview.width()
        h = self.createLayoutDialog.labelImagePreview.height()
        self.createLayoutDialog.labelImagePreview.setPixmap(pm.scaled(w, h, Qt.KeepAspectRatio))
