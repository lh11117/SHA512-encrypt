import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from design import *
import os
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog
import threading
import hashlib


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.toolButton.clicked.connect(self.chooseFile)
        self.pushButton.clicked.connect(self._encrypt)
        self.pushButton_2.clicked.connect(self._decrypt)
        self.action0.triggered.connect(lambda:os.startfile('https://github.com/lh11117/SHA512-encrypt'))
        self.action1.triggered.connect(lambda:QMessageBox.about(self,'关于','SHA512-encrypt是一款加密和解密文件的软件，免费。'))
        self.action2.triggered.connect(lambda:QMessageBox.aboutQt(self,'关于Qt'))
        self.statusBar.showMessage('欢迎使用SHA512-encrypt',5000)
        try:
            if len(sys.argv) >= 2:
                if os.path.isfile(sys.argv[1]) and str(sys.argv[1].split('.')[-1]).lower() == 'sha512-encrypt':
                    self.lineEdit.setText(os.path.abspath(sys.argv[1]))
        except:
            pass
    def chooseFile(self):
        fileName,fileType = QFileDialog.getOpenFileName(self, "选取文件", None, 
        "All Files(*);;Zip Files(*.zip);;RAR Files(*.rar);;SHA512-encrypt文件 (*.sha512-encrypt)")
        if fileName == "":
            return
        self.lineEdit.setText(fileName)
    def _encrypt(self):
        if(os.path.isfile(self.lineEdit.text()) and self.lineEdit.text()!=''):
            fname, ftype = QFileDialog.getSaveFileName(self, '保存加密后的文件', None, "SHA512-encrypt文件 (*.sha512-encrypt)")
            if fname:
                self.setEnabled(False)
                threading.Thread(target=encrypt,args=(self.lineEdit.text(),fname,self.lineEdit_2.text(),self)).start()
        else:
            if self.lineEdit.text()=='':
                QMessageBox.critical(self, '错误', '密码不得为空', QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.critical(self, '错误', '文件不正确', QMessageBox.Ok, QMessageBox.Ok)
    def _decrypt(self):
        if(os.path.isfile(self.lineEdit.text()) and self.lineEdit.text()!=''):
            fname, ftype = QFileDialog.getSaveFileName(self, '保存解密后的文件', None, "所有文件 (*)")
            if fname:
                self.setEnabled(False)
                threading.Thread(target=decrypt,args=(self.lineEdit.text(),fname,self.lineEdit_2.text(),self)).start()
        else:
            if self.lineEdit.text()=='':
                QMessageBox.critical(self, '错误', '密码不得为空', QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.critical(self, '错误', '文件不正确', QMessageBox.Ok, QMessageBox.Ok)



def encrypt(filepath,savepath,password,ui):
    ui.statusBar.showMessage('请稍后……')
    f = open(filepath,"rb")
    data = list("{:02X}".format(int(c)) for c in f.read())
    f.close()
    f = open(savepath,'wb')
    pasw = []
    pasw.append(hashlib.sha512(password.encode('utf-8')).hexdigest())
    while len(''.join(pasw))<len(''.join(data)):
        pasw.append(hashlib.sha512(pasw[-1].encode('utf-8')).hexdigest())
    key = str(''.join(pasw))[0:len(''.join(data))]
    keys = []
    for i in range(len(key)//2):
        keys.append(key[i*2:i*2+2])
    for i in range(len(data)):
        f.write(bytes([(int(data[i], 16)+int(keys[i], 16))%(int('ff',16)+1)]))
    f.close()
    ui.setEnabled(True)
    ui.statusBar.showMessage('加密完成！')

def decrypt(filepath,savepath,password,ui):
    ui.statusBar.showMessage('请稍后……')
    f = open(filepath,"rb")
    data = list("{:02X}".format(int(c)) for c in f.read())
    f.close()
    f = open(savepath,'wb')
    pasw = []
    pasw.append(hashlib.sha512(password.encode('utf-8')).hexdigest())
    while len(''.join(pasw))<len(''.join(data)):
        pasw.append(hashlib.sha512(pasw[-1].encode('utf-8')).hexdigest())
    key = str(''.join(pasw))[0:len(''.join(data))]
    keys = []
    for i in range(len(key)//2):
        keys.append(key[i*2:i*2+2])
    for i in range(len(data)):
        f.write(bytes([(int(data[i], 16)-int(keys[i], 16)+int('ff',16)+1) % (int('ff',16)+1)]))
    f.close()
    ui.setEnabled(True)
    ui.statusBar.showMessage('解密完成！')



if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication([sys.argv[0]])
    mainWindow = Window()
    mainWindow.show()
    sys.exit(app.exec_())