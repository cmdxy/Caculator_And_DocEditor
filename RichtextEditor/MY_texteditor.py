import sys
import textedit
import webbrowser
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon,QPalette,QTextCursor,QTextDocument
from PyQt5.QtCore import Qt,QMimeData,QFile, QFileInfo
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QMessageBox,\
                            QFontDialog, QColorDialog,QVBoxLayout,QWidget,QFileDialog, QMessageBox
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, \
    QHBoxLayout, QVBoxLayout




class Editor(QMainWindow,QWidget):
    
    def __init__(self):
        super(Editor, self).__init__()

        #用于search功能
        self.count = 0;
        self.sw_work = False
        #新建SearchBox控件
        self.SearchBox = QWidget()
        #设置控件模态显示
        self.SearchBox.setWindowModality(Qt.ApplicationModal)
        #搜索框UI
        self.SearchBox.setWindowTitle("搜索框")
        self.SearchBox.keyword_label = QLabel('关键字:', self)
        self.SearchBox.replace_label = QLabel('替换为:', self)
        self.SearchBox.keyword_line = QLineEdit(self)
        self.SearchBox.replace_line = QLineEdit(self)
        self.SearchBox.search_button = QPushButton('搜索', self)
        self.SearchBox.replace_button = QPushButton('替换', self)

        self.SearchBox.label_v_layout = QVBoxLayout()                      # 1
        self.SearchBox.line_v_layout = QVBoxLayout()                       # 2
        self.SearchBox.button_h_layout = QHBoxLayout()                     # 3
        self.SearchBox.label_line_h_layout = QHBoxLayout()                 # 4
        self.SearchBox.all_v_layout = QVBoxLayout()                        # 5

        self.SearchBox.label_v_layout.addWidget(self.SearchBox.keyword_label)           # 6
        self.SearchBox.label_v_layout.addWidget(self.SearchBox.replace_label)
        self.SearchBox.line_v_layout.addWidget(self.SearchBox.keyword_line)
        self.SearchBox.line_v_layout.addWidget(self.SearchBox.replace_line)
        self.SearchBox.button_h_layout.addWidget(self.SearchBox.search_button)
        self.SearchBox.button_h_layout.addWidget(self.SearchBox.replace_button)
        self.SearchBox.label_line_h_layout.addLayout(self.SearchBox.label_v_layout)  # 7
        self.SearchBox.label_line_h_layout.addLayout(self.SearchBox.line_v_layout)
        self.SearchBox.all_v_layout.addLayout(self.SearchBox.label_line_h_layout)
        self.SearchBox.all_v_layout.addLayout(self.SearchBox.button_h_layout)

        self.SearchBox.setLayout(self.SearchBox.all_v_layout)
        #SearchBox类的按钮连接Editor类的search_word函数和replace_word函数
        self.SearchBox.search_button.clicked.connect(self.search_word)
        self.SearchBox.replace_button.clicked.connect(self.replace_word)          



        #设置窗体标题/图标
        self.setWindowTitle(" Little NotePad ")
        self.setWindowIcon(QIcon('images2/记事本.PNG'))

        #设置多窗口控件
        self.mdiArea = QtWidgets.QMdiArea()
        
        
        #0-竖向，1-横向，2-重叠
        self.layout_type = 0;


        #窗体UI
        self.file_menu = self.menuBar().addMenu('文件(F)')
        self.edit_menu = self.menuBar().addMenu('编辑(E)')
        #new
        self.View_menu = self.menuBar().addMenu('视图(V)')
        self.help_menu = self.menuBar().addMenu('帮助(H)')
        

        self.file_toolbar = self.addToolBar('File')
        self.edit_toolbar = self.addToolBar('Edit')

        self.status_bar = self.statusBar()

        #new
        self.search_action = QAction('Search',self)
        self.new_action = QAction('New', self)
        self.open_action = QAction('Open', self)
        self.save_action = QAction('Save', self)
        self.save_as_action = QAction('Save As', self)
        

        self.cut_action = QAction('Cut', self)
        self.copy_action = QAction('Copy', self)
        self.paste_action = QAction('Paste', self)
        self.font_action = QAction('Font', self)
        self.color_action = QAction('Color', self)
        self.about_action = QAction('关于作者', self)

        
        self.actionHorizontal = QAction('Horizontal', self)
        self.actionVertical = QAction('Vertical', self)
        self.actionPile = QAction('Pile', self)
        self.actionLeft = QAction('Left', self)
        self.actionRight = QAction('Right', self)
        self.actionCenter = QAction('Center', self)


        self.actionDelete = QAction('Delete',self)
        self.actionRecover = QAction('Recover',self)

        #剪贴板功能相关
        self.mime_data = QMimeData()
        self.clipboard = QApplication.clipboard()

        #设置窗体大小
        self.setCentralWidget(self.mdiArea)
        self.resize(1200, 800)

        self.menu_init()
        self.toolbar_init()
        self.status_bar_init()
        self.action_init()


    def menu_init(self):
        self.file_menu.addAction(self.new_action)
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.save_as_action)
        self.file_menu.addSeparator()
        #self.file_menu.addAction(self.close_action)

        self.edit_menu.addAction(self.cut_action)
        self.edit_menu.addAction(self.copy_action)
        self.edit_menu.addAction(self.paste_action)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.font_action)
        self.edit_menu.addAction(self.color_action)
        #new
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.search_action)

        self.help_menu.addAction(self.about_action)

        #new
        self.View_menu.addAction(self.actionPile)
        self.View_menu.addAction(self.actionHorizontal)
        self.View_menu.addAction(self.actionVertical)

    def toolbar_init(self):
        self.file_toolbar.addAction(self.new_action)
        self.file_toolbar.addAction(self.open_action)
        self.file_toolbar.addAction(self.save_action)
        self.file_toolbar.addAction(self.save_as_action)

        self.edit_toolbar.addAction(self.font_action)
        self.edit_toolbar.addAction(self.color_action)

        self.edit_toolbar.addAction(self.actionDelete)
        self.edit_toolbar.addAction(self.actionRecover)

        self.edit_toolbar.addAction(self.actionLeft)
        self.edit_toolbar.addAction(self.actionCenter)
        self.edit_toolbar.addAction(self.actionRight)

        self.edit_toolbar.addAction(self.cut_action)
        self.edit_toolbar.addAction(self.copy_action)
        self.edit_toolbar.addAction(self.paste_action)
        
        #new
        self.edit_toolbar.addAction(self.search_action)

    def status_bar_init(self):
        self.status_bar.showMessage('Ready to compose')

    def action_init(self):
        self.new_action.setIcon(QIcon('images2/new.ico'))
        self.new_action.setShortcut('Ctrl+N')
        self.new_action.setToolTip('Create a new file')
        self.new_action.setStatusTip('Create a new file')
        self.new_action.triggered.connect(self.new_func)

        self.open_action.setIcon(QIcon('images2/open.PNG'))
        self.open_action.setShortcut('Ctrl+O')
        self.open_action.setToolTip('Open an existing file')
        self.open_action.setStatusTip('Open an existing file')
        self.open_action.triggered.connect(self.open_file_func)

        self.save_action.setIcon(QIcon('images2/save.ico'))
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.setToolTip('Save the file')
        self.save_action.setStatusTip('Save the file')
        self.save_action.triggered.connect(self.save_func)

        self.save_as_action.setIcon(QIcon('images2/save_as.ico'))
        self.save_as_action.setShortcut('Ctrl+A')
        self.save_as_action.setToolTip('Save the file to a specified location')
        self.save_as_action.setStatusTip('Save the file to a specified location')
        self.save_as_action.triggered.connect(self.save_as_func)


        self.cut_action.setIcon(QIcon('images2/cut.PNG'))
        self.cut_action.setShortcut('Ctrl+X')
        self.cut_action.setToolTip('Cut the text to clipboard')
        self.cut_action.setStatusTip('Cut the text')
        self.cut_action.triggered.connect(self.cut_func)

        self.copy_action.setIcon(QIcon('images2/copy.PNG'))
        self.copy_action.setShortcut('Ctrl+C')
        self.copy_action.setToolTip('Copy the text')
        self.copy_action.setStatusTip('Copy the text')
        self.copy_action.triggered.connect(self.copy_func)

        self.paste_action.setIcon(QIcon('images2/paste.PNG'))
        self.paste_action.setShortcut('Ctrl+V')
        self.paste_action.setToolTip('Paste the text')
        self.paste_action.setStatusTip('Paste the text')
        self.paste_action.triggered.connect(self.paste_func)

        self.font_action.setIcon(QIcon('images2/font.PNG'))
        self.font_action.setShortcut('Ctrl+T')
        self.font_action.setToolTip('Change the font')
        self.font_action.setStatusTip('Change the font')
        self.font_action.triggered.connect(self.font_func)

        self.color_action.setIcon(QIcon('images2/color.ico'))
        self.color_action.setShortcut('Ctrl+R')
        self.color_action.setToolTip('Change the color')
        self.color_action.setStatusTip('Change the color')
        self.color_action.triggered.connect(self.color_func)

        self.about_action.setIcon(QIcon('images2/作者.PNG'))
        self.about_action.setToolTip('About me')
        self.about_action.setStatusTip('About me')
        self.about_action.triggered.connect(self.about_func)

        #new
        self.search_action.setIcon(QIcon('images2/search.PNG'))
        self.search_action.setShortcut('Ctrl+F')
        self.search_action.setToolTip('Search key words')
        self.search_action.setStatusTip('Search key words')
        self.search_action.triggered.connect(self.search_func)

        #调试用,Editor类里的search_action（放在菜单栏）连接search_word()
        self.search_action.triggered.connect(self.search_word)


        #new
        self.actionPile.setIcon(QIcon('images2/平铺.PNG'))
        self.actionPile.setStatusTip('平铺布局')
        self.actionPile.triggered.connect(self.filePile)


        #new
        self.actionHorizontal.setIcon(QIcon('images2/横向布局.PNG'))
        self.actionHorizontal.setStatusTip('水平布局')
        self.actionHorizontal.triggered.connect(self.fileHorizontal)


        #new
        self.actionVertical.setIcon(QIcon('images2/竖向布局.PNG'))
        self.actionVertical.setStatusTip('垂直布局')
        self.actionVertical.triggered.connect(self.fileVertical)

        #new
        self.actionLeft.setIcon(QIcon('images2/左对齐.PNG'))
        self.actionLeft.setStatusTip('左对齐')
        self.actionLeft.triggered.connect(self.fileLeft)
        #new
        self.actionRight.setIcon(QIcon('images2/右对齐.PNG'))
        self.actionRight.setStatusTip('右对齐')
        self.actionRight.triggered.connect(self.fileRight)
        #new
        self.actionCenter.setIcon(QIcon('images2/居中.PNG'))
        self.actionCenter.setStatusTip('居中')
        self.actionCenter.triggered.connect(self.fileCenter)

        #new
        self.actionDelete.setIcon(QIcon('images2/undo.PNG'))
        self.actionDelete.triggered.connect(self.fileUndo)


        #new redo
        self.actionRecover.setIcon(QIcon('images2/redo.PNG'))
        self.actionRecover.triggered.connect(self.fileRedo)

  
    #new
    def filePile(self):
        self.layout_type = 2
        if len(self.mdiArea.subWindowList()) > 1:
            self.mdiArea.cascadeSubWindows()

    def fileHorizontal(self):
        self.layout_type = 1
        wList = self.mdiArea.subWindowList()
        size = len(wList)
        if size > 0:
            position = QtCore.QPoint(0, 0)
            for w in wList:
                rect = QtCore.QRect(0, 0,  self.mdiArea.width() / size,
                         self.mdiArea.height())
                w.setGeometry(rect)
                w.move(position)
                position.setX(position.x() + w.width())

    def fileVertical(self):
        self.layout_type = 0
        wList =  self.mdiArea.subWindowList()
        size = len(wList)
        if size > 0:
            position = QtCore.QPoint(0, 0)
            for w in wList:
                rect = QtCore.QRect(0, 0, self.mdiArea.width(),
                         self.mdiArea.height() / size)
                w.setGeometry(rect)
                w.move(position)
                position.setY(position.y() + w.height())

    #has update
    def new_func(self):
        tmpTextEdit = textedit.TextEdit()
        self.mdiArea.addSubWindow(tmpTextEdit)
        tmpTextEdit.show()
        if self.layout_type == 0:
            self.fileVertical()
        elif self.layout_type == 1:
            self.fileHorizontal()
        elif self.layout_type == 2:
            self.filePile()

    #has update
    def open_file_func(self):
        filename,filetype = QFileDialog.getOpenFileName(self,"打开文件","C:","Text files (*.txt);;HTML files (*html)")
        if filename:
            for window in self.mdiArea.subWindowList():
                textEdit=window.widget()
                if textEdit.filename == filename:
                    self.mdiArea.setActiveSubWindow(window)
                    print(textEdit.filename,filename) 
                    break
            else:
                self.loadFile(filename)
                if self.layout_type == 0:
                    self.fileVertical()
                elif self.layout_type == 1:
                    self.fileHorizontal()
                elif self.layout_type == 2:
                    self.filePile()

    #引入辅助open_file/有bug
    def loadFile(self, filename):
        tmpTextEdit = textedit.TextEdit(filename)
        tmpTextEdit.load()
        self.mdiArea.addSubWindow(tmpTextEdit)
        tmpTextEdit.show()

    #has update
    def save_func(self, text):
        if self.empty():
            return 
        tmpTextEdit = self.mdiArea.activeSubWindow()
        tmpTextEdit=tmpTextEdit.widget()
        if tmpTextEdit is None or not isinstance(tmpTextEdit, QTextEdit):
            return True
        tmpTextEdit.save()
    #/有bug
    def save_as_func(self):
        if self.empty():
            return 
        tmpTextEdit = self.mdiArea.activeSubWindow()
        tmpTextEdit = tmpTextEdit.widget()
        path, _ = QFileDialog.getSaveFileName(self, 'Save File', './', "Text files (*.txt);;HTML files (*.html)")
        #修复bug
        if path == '':
            return 
        with open(path, 'w') as file_path:
            if 'html' in tmpTextEdit.filename:
                file_path.write(tmpTextEdit.toHtml())
            if 'txt' in tmpTextEdit.filename:
                print("toPlainText")
                file_path.write(tmpTextEdit.toPlainText())
 
    #has update
    def closeEvent(self,event):
        unSaveFile = 0
        for window in self.mdiArea.subWindowList():
            textEdit = window.widget()
            if textEdit.isModified():
                unSaveFile += 1
        if unSaveFile != 0:
            dlg = QMessageBox.warning(self, "Notepad", "{0}个文档尚未保存，是否关闭？".format(unSaveFile), QMessageBox.Yes|QMessageBox.No)
            if dlg == QMessageBox.Yes:
                 QtCore.QCoreApplication.quit()
            elif dlg == QMessageBox.No:
                 event.ignore()

    #has update
    def cut_func(self):
        if self.empty():
            return 
        self.mdiArea.activeSubWindow().widget().cut()
    
    #has update
    def copy_func(self):
        if self.empty():
            return 
        self.mdiArea.activeSubWindow().widget().copy()
    
    #has update
    def paste_func(self):
        if self.empty():
            return 
        self.mdiArea.activeSubWindow().widget().paste()
    
    #has update
    def font_func(self):
        if self.empty():
            return 
        font, ok = QFontDialog.getFont()
        if ok:
            self.mdiArea.activeSubWindow().widget().setCurrentFont(font)
    #has update
    def color_func(self):
        if self.empty():
            return 
        color = QColorDialog.getColor()
        if color.isValid():
            self.mdiArea.activeSubWindow().widget().setTextColor(color)

    def about_func(self):
        try:
            webbrowser.get('chrome').open_new_tab('https://chzarles.github.io/about/')
        except Exception as e:
            webbrowser.open_new_tab('https://chzarles.github.io/about/')

    #new
    def search_func(self):
        if self.empty():
            return 

        sub = self.mdiArea.activeSubWindow().widget()
        sub.moveCursor(QTextCursor.Start)
        self.count = -1;
        self.SearchBox.show()
       
 
 
    #
    
    def search_word(self):

        pattern = self.SearchBox.keyword_line.text()
        if pattern == "":
            return ;
        sub = self.mdiArea.activeSubWindow().widget()
  
        if sub.find(pattern):
            #找到了才标记起作用
            self.sw_work = True
            #测试
            self.count = self.count + 1
        
            print("self.count",self.count)
            palette = sub.palette()
            palette.setColor(QPalette.Highlight, palette.color(QPalette.Active,QPalette.Highlight))
            sub.setPalette(palette)
        else:
            sub.moveCursor(QTextCursor.Start)
            self.count = -1;
            if sub.find(pattern):
                self.count = self.count + 1
                self.sw_work = True
                palette = sub.palette()
                palette.setColor(QPalette.Highlight, palette.color(QPalette.Active,QPalette.Highlight))
                sub.setPalette(palette)
            print("self.count",self.count)
                
        
        print("search_word self.count:" ,self.count)




    def replace_word(self):
        #确保被选中才能执行replace_word
        if not self.sw_work:
            return 
        else:
            self.sw_work = False

        pattern = self.SearchBox.keyword_line.text()
        sub = self.mdiArea.activeSubWindow().widget()


        tar = self.SearchBox.replace_line.text()
        text = sub.toPlainText()
        #待替换关键词的长度
        l = len(pattern)

        #开始搜索的索引
        start = 0
        backup = self.count     

        while(backup):
            print("循环里backup :",backup)
            idx = text.find(pattern,start)
            print("循环里idx :",idx)
            start = (idx+l)
            backup = backup - 1;
        idx = text.find(pattern,start)
        print("出来时start：",start)
        print("出来时：",backup)
        print("idx:" ,idx)
        h = text[0:idx]
        t = text[idx+l:]
        print("关键字长度：",l)
        print("前缀：",h)
        print("后缀：",t)
        print("self.count:" ,self.count)
        text = h + tar + t
        sub.setText(text)

        self.count -= 1
        bk = self.count
        sub.moveCursor(QTextCursor.Start)
        while bk!=-1:
            self.sw_work = True
            bk-=1
            sub.find(pattern)


        
    

    #new            
    def fileLeft(self):
        if self.empty():
            return 
        self.mdiArea.activeSubWindow().widget().setAlignment(Qt.AlignLeft)
        
    def fileRight(self):
        if self.empty():
            return 
        self.mdiArea.activeSubWindow().widget().setAlignment(Qt.AlignRight)
        
        
    def fileCenter(self):
        if self.empty():
            return 
        self.mdiArea.activeSubWindow().widget().setAlignment(Qt.AlignCenter)


    #修复bug用
    def empty(self):
        wList =  self.mdiArea.subWindowList()
        if len(wList) == 0:
            return True
        else :
            return False

    #new 撤销/反销撤
    def fileRedo(self):
        self.mdiArea.activeSubWindow().widget().redo()

    def fileUndo(self):
        self.mdiArea.activeSubWindow().widget().undo()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    test = Editor()
    test.show()
    sys.exit(app.exec_())
