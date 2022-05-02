from msilib.schema import ComboBox
import sys
from PyQt5.QtWidgets import QWidget, QCheckBox, QHBoxLayout, QVBoxLayout, QPushButton, QSplitter, QComboBox, QLabel, QSpinBox, QFileDialog
from PyQt5.QtGui import QPainter,QIcon, QPen, QPixmap, QPaintEvent, QMouseEvent, QColor
from PyQt5.QtCore import Qt, QPoint, QSize
from PaintBoard import PaintBoard

class MainWidget(QWidget):

    def __init__(self, Parent=None):

        super().__init__(Parent)

        self.__InitData()
        self.__InitView()

    def __InitData(self):
        self.paintBoard = PaintBoard(self)
        self.colorList = QColor.colorNames()

    def __InitView(self):

        main_layout = QHBoxLayout(self)

        main_layout.setSpacing(10)

        main_layout.addWidget(self.paintBoard)

        sub_layout = QVBoxLayout()

        sub_layout.setContentsMargins(10, 10, 10, 10)

        self.__btn_Clear = QPushButton("Clear Drawboard")
        self.__btn_Clear.setParent(self)

        self.__btn_Clear.clicked.connect(self.paintBoard.Clear)
        sub_layout.addWidget(self.__btn_Clear)

        self.__btn_Quit = QPushButton("Exit")
        self.__btn_Quit.setParent(self)
        self.__btn_Quit.clicked.connect(self.Quit)
        sub_layout.addWidget(self.__btn_Quit)

        self.__btn_Save = QPushButton("Save")
        self.__btn_Save.setParent(self)
        self.__btn_Save.clicked.connect(self.on_btn_Save_Clicked)
        sub_layout.addWidget(self.__btn_Save)

        self.__cbtn_Eraser = QCheckBox(" Eraser")
        self.__cbtn_Eraser.setParent(self)
        self.__cbtn_Eraser.clicked.connect(self.on_cbtn_Eraser_clicked)
        sub_layout.addWidget(self.__cbtn_Eraser)

        splitter = QSplitter(self)
        sub_layout.addWidget(splitter)

        self.__label_penThickness = QLabel(self)
        self.__label_penThickness.setText("Pen Thickness")
        self.__label_penThickness.setFixedHeight(20)
        sub_layout.addWidget(self.__label_penThickness)

        self.__spinBox_penThickness = QSpinBox(self)
        self.__spinBox_penThickness.setMaximum(20)
        self.__spinBox_penThickness.setMinimum(2)
        self.__spinBox_penThickness.setValue(10)
        self.__spinBox_penThickness.setSingleStep(2)
        self.__spinBox_penThickness.valueChanged.connect(self.on_PenThicknessChange)
        sub_layout.addWidget(self.__spinBox_penThickness)

        self.__label_penColor = QLabel(self)
        self.__label_penColor.setText("Pen Color")
        self.__label_penColor.setFixedHeight(20)
        sub_layout.addWidget(self.__label_penColor)

        self.__comboBox_penColor = QComboBox(self)
        self.__fillColorList(self.__comboBox_penColor)
        self.__comboBox_penColor.currentIndexChanged.connect(self.on_PenColorChange)
        sub_layout.addWidget(self.__comboBox_penColor)

        main_layout.addLayout(sub_layout)

    def __fillColorList(self, comboBox):

        index_black = 0
        index = 0
        for color in self.colorList:
            if color == "black":
                index_black = index
            index += 1
            pix = QPixmap(70,20)
            pix.fill(QColor(color))
            comboBox.addItem(QIcon(pix),None)
            comboBox.setIconSize(QSize(70,20))
            comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        comboBox.setCurrentIndex(index_black)

    def on_PenColorChange(self):
        color_index = self.__comboBox_penColor.currentIndex()
        color_str = self.colorList[color_index]
        self.paintBoard.ChangePenColor(color_str)

    def on_PenThicknessChange(self):
        penThickness = self.__spinBox_penThickness.value()
        self.paintBoard.ChangePenThickness(penThickness)



    def on_btn_Save_Clicked(self):
        savePath = QFileDialog.getSaveFileName(self, 'Save Your Paint', '.\\', '*.p')
        print(savePath)
        if savePath[0] == "":
            print("Save cancel")
            return
        file = self.paintBoard.ContentImage()
        file.save(savePath[0])

    

    def on_cbtn_Eraser_clicked(self):
        if self.__cbtn_Eraser.isChecked():
            self.paintBoard.Eraser = True
        else:
            self.paintBoard.Eraser = False

    def Quit(self):
        self.close()



