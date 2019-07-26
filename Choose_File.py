import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

fileName = ""

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        fileName = self.openFileNameDialog()
          
    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Open", "","(*.txt)", options=options)
        if fileName:
            fileNamePull (fileName)
            
def fileNamePull (name):
    global fileName
    fileName = name

def main():
    app = QApplication(sys.argv)
    ex = App()
    return fileName

if __name__ == '__main__':
    main()
    
