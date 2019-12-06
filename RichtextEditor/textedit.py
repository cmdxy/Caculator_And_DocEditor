# -*- coding: utf-8 -*-
from PyQt5.QtCore import QFile, QFileInfo, QIODevice, QTextStream, Qt
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTextEdit
#from zopyx.convert2 import Converter

class TextEdit(QTextEdit):
    NextId = 1

    def __init__(self, filename="", parent=None):
        super(TextEdit, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.filename = filename
        if self.filename == "":
            self.filename = "Untitled-{0}".format(TextEdit.NextId)
            TextEdit.NextId += 1
        self.document().setModified(False)
        self.windowName = QFileInfo(self.filename).fileName()
        self.setWindowTitle(self.windowName)
        #self.setWindowIcon(QIcon('images2/save.PNG'))
    




    def closeEvent(self, event):
        if self.document().isModified():
            dlg = QMessageBox.question(self, "Notepad", "是否保存对'{0}'的修改?".format(self.windowName),QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
            if dlg == QMessageBox.Yes:
                self.save()
            elif dlg == QMessageBox.No:
                self.close()
            else:
                event.ignore()


    def isModified(self):
        return self.document().isModified()


    def save(self):
        if self.filename.startswith("Untitled") or self.filename == '':
            self.filename = QFileDialog.getSaveFileName(self, "保存文件", self.filename,"Text files (*.txt);;HTML files (*.html)")[0]

        if self.filename == '':
            return
        self.windowName = QFileInfo(self.filename).fileName()
        with open(self.filename, 'w') as file_path:
            if 'html' in self.windowName:
                file_path.write(self.toHtml())
            if 'txt' in self.windowName:
                file_path.write(self.toPlainText())
        self.setWindowTitle(QFileInfo(self.filename).fileName())
        self.document().setModified(False)

    def load(self):
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError(str(fh.errorString()))
            stream = QTextStream(fh)
            #stream.setCodec("UTF-8")

            if 'html' in self.filename:
                self.setText(stream.readAll())
            elif 'txt' in self.filename:
                print("setPlainText")
                self.setPlainText(stream.readAll())

            self.document().setModified(False)
        except EnvironmentError as e:
            QMessageBox.warning(self,"加载错误"
                    "不能加载 {0}".format(self.filename))
        finally:
            if fh is not None:
                fh.close()
        self.setWindowTitle(QFileInfo(self.filename).fileName())

