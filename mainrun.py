import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from design import *
import os
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog
import threading
import hashlib
import dialog_decrypt,dialog_encrypt


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self._encrypt)
        self.pushButton_2.clicked.connect(self._decrypt)
        self.action0.triggered.connect(lambda:os.startfile('https://github.com/lh11117/SHA512-encrypt'))
        self.action1.triggered.connect(lambda:QMessageBox.about(self,'关于','软件版本：v1.1'))
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
        dialog = encrypt_Window()
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.show()
        dialog.exec_()
    def _decrypt(self):
        dialog = decrypt_Window()
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.show()
        dialog.exec_()


class encrypt_Window(QDialog, dialog_encrypt.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self._encrypt)
        self.toolButton.clicked.connect(self.chooseFile)
    def chooseFile(self):
        fileName,fileType = QFileDialog.getOpenFileName(self, "选取文件", None, 
        "All Files(*);;Zip Files(*.zip);;RAR Files(*.rar);;SHA512-encrypt文件 (*.sha512-encrypt)")
        if fileName == "":
            return
        self.lineEdit.setText(fileName)
    def _encrypt(self):
        if self.lineEdit.text()=='':
            QMessageBox.critical(self, '错误', '密码不得为空', QMessageBox.Ok, QMessageBox.Ok)
        elif not os.path.isfile(self.lineEdit.text()):
            QMessageBox.critical(self, '错误', '文件不正确', QMessageBox.Ok, QMessageBox.Ok)
        else:
            fname, ftype = QFileDialog.getSaveFileName(self, '保存加密后的文件', None, "SHA512-encrypt文件 (*.sha512-encrypt)")
            if fname:
                self.setEnabled(False)
                threading.Thread(target=encrypt,args=(self.lineEdit.text(),fname,self.lineEdit_2.text(),self)).start()


class decrypt_Window(QDialog, dialog_decrypt.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self._decrypt)
        self.toolButton.clicked.connect(self.chooseFile)
    def chooseFile(self):
        fileName,fileType = QFileDialog.getOpenFileName(self, "选取文件", None, 
        "SHA512-encrypt文件 (*.sha512-encrypt)")
        if fileName == "":
            return
        self.lineEdit.setText(fileName)
    def _decrypt(self):
        if self.lineEdit.text()=='':
            QMessageBox.critical(self, '错误', '密码不得为空', QMessageBox.Ok, QMessageBox.Ok)
        elif not os.path.isfile(self.lineEdit.text()):
            QMessageBox.critical(self, '错误', '文件不正确', QMessageBox.Ok, QMessageBox.Ok)
        else:
            fname, ftype = QFileDialog.getSaveFileName(self, '保存解密后的文件', None, "所有文件 (*)")
            if fname:
                self.setEnabled(False)
                threading.Thread(target=decrypt,args=(self.lineEdit.text(),fname,self.lineEdit_2.text(),self)).start()


def encrypt(filepath,savepath,password,ui):
    ui.label_3.setText('正在读取文件')
    with open(filepath,"rb") as f:
        data = list("{:02X}".format(int(c)) for c in f.read())
    with open(savepath,'wb') as f:
        pasw = hashlib.sha512(password.encode('utf-8')).hexdigest()
        data_all_len = len(''.join(data))
        ui.label_3.setText('正在生成密钥')
        while len(pasw)<data_all_len:
            pasw += hashlib.sha512(pasw[-512:].encode('utf-8')).hexdigest()
        key = pasw[0:data_all_len]
        ui.label_3.setText('正在加密文件')
        for i in range(len(key)//2):
            f.write(bytes([(int(data[i], 16)+int(key[i*2:i*2+2], 16))%(int('ff',16)+1)])) 
    ui.setEnabled(True)
    ui.label_3.setText('全部完成！')

def decrypt(filepath,savepath,password,ui):
    ui.label_3.setText('正在读取文件')
    with open(filepath,"rb") as f:
        data = list("{:02X}".format(int(c)) for c in f.read())
    with open(savepath,'wb') as f:
        pasw = hashlib.sha512(password.encode('utf-8')).hexdigest()
        data_all_len = len(''.join(data))
        ui.label_3.setText('正在生成密钥')
        while len(pasw)<data_all_len:
            pasw += hashlib.sha512(pasw[-512:].encode('utf-8')).hexdigest()
        key = pasw[0:data_all_len]
        ui.label_3.setText('正在解密文件')
        for i in range(len(key)//2):
            f.write(bytes([(int(data[i], 16)-int(key[i*2:i*2+2], 16)+int('ff',16)+1) % (int('ff',16)+1)]))
    ui.setEnabled(True)
    ui.label_3.setText('全部完成！')



if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication([sys.argv[0]])
    mainWindow = Window()
    mainWindow.show()
    sys.exit(app.exec_())

