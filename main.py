from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
from Coder import Coder
import os
import timeit

toPackFilepath = ""
toUnpackFilepath = ""


# rezgion Pack slots
def selectFile2PacButton_clicked(self):
    global toPackFilepath
    form.packFactorLabel.setText(f'')
    form.packTimeLabel.setText(f'')
    toPackFilepath, _ = QFileDialog.getOpenFileName(None, 'Open File', './', "Any files (*)")
    form.selectedFile2PacLineEdit.setText(toPackFilepath)
    if toPackFilepath != "":
        form.toPackFileButton.setEnabled(True)
    else:
        form.toPackFileButton.setEnabled(False)


def toPackFileButton_clicked(self):
    coder = Coder()
    result_filename = toPackFilepath + ".2pack"
    print(result_filename)
    execution_time = timeit.timeit(lambda: coder.encode(filename=toPackFilepath, result_filename=result_filename), number=1)

    old_size = os.path.getsize(toPackFilepath)
    new_size = os.path.getsize(result_filename)
    difference = round(100 - (new_size * 100 / old_size), 2)
    if difference > 0.0:
        form.packFactorLabel.setText(f'Степень сжатия: <font color="green">{difference}%</font>')
    else:
        form.packFactorLabel.setText(f'Степень сжатия: <font color="red">{difference}%</font>')
    form.packTimeLabel.setText(f"Время сжатия: {execution_time:.2f} с")
    os.remove(toPackFilepath)

# endregion

# region Unpack slots
def selectFile2UnpackButton_clicked(self):
    global toUnpackFilepath
    form.unpackTimeLabel.setText(f'')
    toUnpackFilepath, _ = QFileDialog.getOpenFileName(None, 'Open File', './', "2packer File (*.2pack)")
    form.selectedFile2UnpackLineEdit.setText(toUnpackFilepath)
    if toUnpackFilepath != "":
        form.toUnpackFileButton.setEnabled(True)
    else:
        form.toUnpackFileButton.setEnabled(False)


def toUnpackFileButton_clicked(self):
    coder = Coder()
    result_filename = toUnpackFilepath[0: len(toUnpackFilepath) - 6]
    print(result_filename)
    execution_time = timeit.timeit(lambda: coder.decode(filename=toUnpackFilepath, result_filename=result_filename), number=1)
    form.unpackTimeLabel.setText(f"Время распаковки: {execution_time:.6f} с")
    os.remove(toUnpackFilepath)


# endregion
# подключаем файл, полученный в QtDesigner
Form, Window = uic.loadUiType("2packer.ui")

app = QApplication([])
window, form = Window(), Form()
form.setupUi(window)

window.show()

form.toPackFileButton.setEnabled(False)
form.toUnpackFileButton.setEnabled(False)
form.selectFile2PacButton.clicked.connect(selectFile2PacButton_clicked)
form.toPackFileButton.clicked.connect(toPackFileButton_clicked)
form.selectFile2UnpackButton.clicked.connect(selectFile2UnpackButton_clicked)
form.toUnpackFileButton.clicked.connect(toUnpackFileButton_clicked)

app.exec()
