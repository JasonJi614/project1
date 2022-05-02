from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QPixmap, QPaintEvent, QMouseEvent, QColor
from PyQt5.QtCore import Qt, QPoint, QSize


class PaintBoard(QWidget):

    def __init__(self, Parent=None):
        '''
        con
        '''

        super().__init__(Parent)
        self.__InitData()
        self.__InitView()
    
    def __InitData(self):

        self.QSize = QSize(480,460)
        self.PaintBoard = QPixmap(self.QSize)
        self.PaintBoard.fill()
        self.QPainter = QPainter()
        self.ifEmpty = True
        self.Eraser = False
        self.penThickness = 12
        self.penColor = QColor("black")
        self.colorList = QColor.colorNames()
        self.lastMousePosition = QPoint(0,0)
        self.currentMousePosition = QPoint(0,0)

    def __InitView(self):
        self.setFixedSize(self.QSize)

    def Clear(self):
        self.PaintBoard.fill()
        self.update()
        self.ifEmpty = True

    def ChangePenColor(self, color="black"):
        self.penColor = QColor(color)

    def ChangePenThickness(self, thinkness=10):
        self.penThickness = thinkness

    def IfEmpty(self):
        return self.ifEmpty 

    def ContentImage(self):
        file = self.PaintBoard.toImage()
        return file

    def paintEvent(self, QpaintEvent):
        self.QPainter.begin(self)
        self.QPainter.drawPixmap(0,0,self.PaintBoard)
        self.QPainter.end()

    def mousePressEvent(self, mouseEvent):
        self.currentMousePosition = mouseEvent.pos()
        self.lastMousePosition = self.currentMousePosition

    def mouseMoveEvent(self, mouseEvent):
        self.currentMousePosition = mouseEvent.pos()
        self.QPainter.begin(self.PaintBoard)

        if self.Eraser == True:
            self.QPainter.setPen(QPen(QColor("white"),10))
        else:
            self.QPainter.setPen(QPen(self.penColor,self.penThickness))

        self.QPainter.drawLine(self.lastMousePosition, self.currentMousePosition)
        self.QPainter.end()
        self.lastMousePosition = self.currentMousePosition

        self.update()

    def mouseReleaseEvent(self, QmouseEvent):
        self.ifEmpty = False