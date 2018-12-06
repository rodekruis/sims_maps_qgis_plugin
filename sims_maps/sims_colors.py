from qgis.core import QgsColorScheme
from PyQt5.QtGui import QColor


class QgsSimsColorScheme(QgsColorScheme):

    def __init__(self, parent=None):
        QgsColorScheme.__init__(self)


    def schemeName(self):
        return "SIMS Colors"


    def fetchColors(self,context='', basecolor=QColor()):
        return [[QColor('#bc220e'),'Go red'],
                    [QColor('#2a2a2a'),'Go black'],
                    [QColor('#003045'),'Go blue'],
                    [QColor('#426b69'),'Go green'],
                    [QColor('#2e294e'),'Go purple'],
                    [QColor('#c02c2d'),'Go red?'],
                    [QColor('#fafafa'),'Go white'],
                    [QColor('#ffba49'),'Go yellow'],
                    [QColor('#ee3224'),'IFRC red']]


    def flags(self):
        return QgsColorScheme.ShowInAllContexts


    def clone(self):
        return QgsSimsColorScheme()
