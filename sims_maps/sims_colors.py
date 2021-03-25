from qgis.core import QgsColorScheme
from PyQt5.QtGui import QColor


class QgsSimsColorScheme(QgsColorScheme):

    def __init__(self, parent=None):
        QgsColorScheme.__init__(self)


    def schemeName(self):
        return 'SIMS Colors'


    def fetchColors(self,context='', basecolor=QColor()):
        return [[QColor('#e32219'),'Go 485C'],
                    [QColor('#f63440'),'Go RED032 (IFRC?)'],
                    [QColor('#7a1600'),'Go 483C 100%'], # brown
                    [QColor('#c3ada9'),'Go 483C 60%'],
                    [QColor('#e1d6d4'),'Go 483C 20%'],
                    [QColor('#786a65'),'Go 410C 100%'], # grey
                    [QColor('#c9c3c1'),'Go 410C 60%'],
                    [QColor('#e4e1e0'),'Go 410C 20%'],
                    [QColor('#ffd200'),'Go 109C 100%'], # yellow
                    [QColor('#ffe466'),'Go 109C 60%'],
                    [QColor('#fff6cc'),'Go 109C 20%'],
                    [QColor('#ff5014'),'Go 1655C 100%'], # orange
                    [QColor('#ff9966'),'Go 1655C 60%'],
                    [QColor('#ffdcd0'),'Go 1655C 20%'],
                    [QColor('#00a0dc'),'Go PR.CYAN 100%'],# cyan
                    [QColor('#99d9f1'),'Go PR.CYAN 60%'],
                    [QColor('#ccecf8'),'Go PR.CYAN 20%'],
                    [QColor('#d20073'),'Go 226C 100%'], # magenta
                    [QColor('#ed99c7'),'Go 226C 60%'],
                    [QColor('#f6cce3'),'Go 226C 20%'],
                    [QColor('#8cd200'),'Go 376C 100%'], # green
                    [QColor('#bae466'),'Go 376C 60%'],
                    [QColor('#e8f6cc'),'Go 376C 20%'],
                    [QColor('#003246'),'Go 303C 100%'], # dark blue
                    [QColor('#99adb5'),'Go 303C 60%'],
                    [QColor('#ccd6da'),'Go 303C 20%'],
                    [QColor('#5a325f'),'Go 519C 100%'], # dark purple
                    [QColor('#bdadbf'),'Go 519C 60%'],
                    [QColor('#ded6df'),'Go 519C 20%'],
                    [QColor('#555f1e'),'Go 378C 100%'], # dark green
                    [QColor('#999f78'),'Go 378C 60%'],
                    [QColor('#dddfd2'),'Go 378C 20%'],
                    [QColor('#ee3224'),'IFRC red']]


    def flags(self):
        return QgsColorScheme.ShowInAllContexts


    def clone(self):
        return QgsSimsColorScheme()
