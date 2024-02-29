import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

from PySide6.QtWidgets import QLabel,QPushButton

class Mybutton(QPushButton):
    def __init__(self, text:str) -> None:
        super().__init__(text=text)

    def changeText(self, text:str):
        self.setText(text)


class MyWidget(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.hello = ["Hallo Welt", 'Hei Maailma', ' Hola mundo', "ereererddd"]
        self.button = QPushButton('click me')
        self.button = Mybutton('Click Me')
        self.text = QLabel('Hello World', alignment=QtCore.Qt.AlignCenter)

        self.board = QLabel('board gos here', alignment= QtCore.Qt.AlignCenter)
        self.valueChoices = [1,2,3,4,5,6,7]
        self.valueBtns = []
        self.choiceLayout = QtWidgets.QHBoxLayout()
        
        for i in self.valueChoices:
            btn = QPushButton(str(i),)
            self.valueBtns.append(btn)
            self.choiceLayout.addWidget(btn)
        

        self.statusDisplay = QLabel('STATUS UPDATER',alignment= QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.board)
        self.layout.addLayout(self.choiceLayout)
        self.layout.addWidget(self.statusDisplay)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.button.changeText(random.choice(self.hello))
        self.text.setText(random.choice(self.hello))




if __name__ == "__main__":
    app = QtWidgets.QApplication([])


    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())