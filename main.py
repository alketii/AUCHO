"""
Copyright (C) 2014  Alket Rexhepi

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

from PyQt4 import QtCore, QtGui
from os.path import expanduser
import sqlite3, hashlib, os , datetime, time, ftplib, shutil

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))

        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        self.comboBox_projects = QtGui.QComboBox(self.centralwidget)
        self.comboBox_projects.setObjectName(_fromUtf8("comboBox_projects"))
        self.comboBox_projects.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_projects, 0, 0, 1, 1)

        self.pushButton_compare = QtGui.QPushButton(self.centralwidget)
        self.pushButton_compare.setObjectName(_fromUtf8("pushButton_compare"))
        self.gridLayout.addWidget(self.pushButton_compare, 0, 1, 1, 1)

        self.pushButton_update = QtGui.QPushButton(self.centralwidget)
        self.pushButton_update.setObjectName(_fromUtf8("pushButton_update"))
        self.gridLayout.addWidget(self.pushButton_update, 0, 2, 1, 1)

        self.pushButton_edit = QtGui.QPushButton(self.centralwidget)
        self.pushButton_edit.setObjectName(_fromUtf8("pushButton_edit"))
        self.gridLayout.addWidget(self.pushButton_edit, 0, 3, 1, 1)
        self.pushButton_edit.setEnabled(False)

        self.pushButton_new = QtGui.QPushButton(self.centralwidget)
        self.pushButton_new.setObjectName(_fromUtf8("pushButton_new"))
        self.gridLayout.addWidget(self.pushButton_new, 0, 4, 1, 1)

        self.treeWidget = QtGui.QTreeWidget(self.centralwidget)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.gridLayout.addWidget(self.treeWidget, 1, 0, 1, 5)

        self.listWidget_log = QtGui.QListWidget(self.centralwidget)
        self.listWidget_log.setMinimumSize(QtCore.QSize(0, 100))
        self.listWidget_log.setMaximumSize(QtCore.QSize(16777215, 100))
        self.listWidget_log.setObjectName(_fromUtf8("listWidget_log"))
        self.gridLayout.addWidget(self.listWidget_log, 2, 0, 1, 5)

        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 5)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.progressBar.hide()

        MainWindow.setCentralWidget(self.centralwidget)

        self.actionNew_Project = QtGui.QAction(MainWindow)
        self.actionNew_Project.setObjectName(_fromUtf8("actionNew_Project"))
        self.actionEdit_Projects = QtGui.QAction(MainWindow)
        self.actionEdit_Projects.setObjectName(_fromUtf8("actionEdit_Projects"))

        self.pushButton_update.setEnabled(False)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #functions
        self.pushButton_new.clicked.connect(self.newProjectForm)
        self.pushButton_compare.clicked.connect(self.compareFiles)
        self.pushButton_update.clicked.connect(self.updateAndUpload)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "AUCHO", None))
        self.pushButton_compare.setText(_translate("MainWindow", "Compare", None))
        self.pushButton_update.setText(_translate("MainWindow", "Upload", None))
        self.pushButton_edit.setText(_translate("MainWindow", "Edit", None))
        self.pushButton_new.setText(_translate("MainWindow", "New", None))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "Upload", None))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "State", None))
        self.treeWidget.headerItem().setText(2, _translate("MainWindow", "File", None))
        self.actionNew_Project.setText(_translate("MainWindow", "New Project", None))
        self.actionEdit_Projects.setText(_translate("MainWindow", "Edit Projects", None))
        self.treeWidget.header().resizeSection(0,70)
        self.treeWidget.header().resizeSection(1,100)

    
    def logNew(self,msg):
        self.listWidget_log.insertItem(0,str(datetime.datetime.now().strftime("%H:%M:%S"))+" - "+msg)

    def newProjectForm(self):
        NewProject.show()

    def showProjects(self):
        self.comboBox_projects.clear()
        con = sqlite3.connect('data/main.sql')
        con.text_factory = str
        cur = con.cursor()
        cur.execute("SELECT * FROM main")
        rows = cur.fetchall()
        for row in rows:
            self.comboBox_projects.addItem(row[1])
        if len(rows) == 0:
            self.pushButton_compare.setEnabled(False)
        else:
            self.pushButton_compare.setEnabled(True)

    def getProject(self,index):
        con = sqlite3.connect('data/main.sql')
        con.text_factory = str
        cur = con.cursor()
        cur.execute("SELECT * FROM main")
        rows = cur.fetchall()
        return rows[index]

    def updateAndUpload(self):
        itemCount = self.treeWidget.topLevelItemCount()
        if itemCount > 0:
            index = self.comboBox_projects.currentIndex()
            project = self.getProject(index)
            projectId = project[0]
            projectDir = project[2]
            projectFTP_host = project[3]
            projectFTP_user = project[4]
            projectFTP_password = project[5]
            projectFTP_dir = project[7]

            self.pushButton_compare.setEnabled(False)
            self.pushButton_update.setEnabled(False)
            self.pushButton_new.setEnabled(False)
            self.treeWidget.setEnabled(False)
            self.comboBox_projects.setEnabled(False)

            everythingOk = False

            if projectFTP_password == "":
                password, button_ok = QtGui.QInputDialog.getText(None,"FTP Password","Please provide password for\n"+projectFTP_user+"@"+projectFTP_host,QtGui.QLineEdit.Password)
                if button_ok:
                    projectFTP_password = str(password)
                    everythingOk = True
                else:
                    everythingOk = False
            else:
                everythingOk = True

            if everythingOk:

                self.logNew("Trying to connect to FTP")
                ftp = ftplib.FTP(projectFTP_host)
                self.logNew(ftp.login(projectFTP_user,projectFTP_password))
                self.logNew(ftp.getwelcome())

                conLs = sqlite3.connect('data/last/'+projectId+'.sql')
                conLs.text_factory = str
                curLs = conLs.cursor()

                #create dirs
                for root, dirs, filenames in os.walk(projectDir):
                    remoteDir = projectFTP_dir+root[len(projectDir):]
                    if remoteDir != "":
                        try:
                            ftp.mkd(remoteDir)
                        except:
                            pass

                #upload files
                self.progressBar.setValue(0)
                self.progressBar.setMaximum(itemCount)
                self.progressBar.show()
                currentItem = 0
                while currentItem < itemCount:
                    item = self.treeWidget.topLevelItem(currentItem)
                    currentItem += 1
                    if item.checkState(0) == 2:
                        currentFile = projectDir+"/"+item.text(2)
                        remoteFile = projectFTP_dir+"/"+item.text(2)
                        cleanFile = str(item.text(2))
                        self.logNew(remoteFile+" : Uploading")
                        try:
                            self.logNew(remoteFile+" : "+ftp.storbinary('STOR '+str(remoteFile), open(str(currentFile), 'rb')))

                        except Exception,e:
                            self.logNew(remoteFile +" : "+str(e))

                        curLs.execute("SELECT * FROM project WHERE file=?",[cleanFile])
                        row = curLs.fetchone()
                        currentFileHash = hashlib.md5(open(currentFile).read()).hexdigest()
                        if row:
                            curLs.execute("UPDATE project SET hash=? WHERE file=?",[currentFileHash,cleanFile])
                        else:
                            curLs.execute("INSERT INTO project VALUES(?,?)",[cleanFile,currentFileHash])
                    self.progressBar.setValue(currentItem)

                self.logNew(ftp.quit())
                conLs.commit()
                self.treeWidget.clear()
                self.pushButton_update.setEnabled(False)
                self.progressBar.hide()
                self.logNew("Uploaded "+str(itemCount)+" Files.")
            else:
                self.logNew("No password provided")
        else:
            self.logNew("Nothing to upload.")

    def compareFiles(self):
        self.logNew("Comparing...")
        self.pushButton_compare.setEnabled(False)
        self.pushButton_update.setEnabled(False)
        self.pushButton_new.setEnabled(False)
        self.treeWidget.setEnabled(False)
        self.comboBox_projects.setEnabled(False)
        self.treeWidget.clear()

        index = self.comboBox_projects.currentIndex()
        project = self.getProject(index)
        projectId = project[0]
        projectDir = project[2]

        if not os.path.isfile('data/'+projectId+'.sql'): #check if project is new
            shutil.copy('data/template.sql','data/'+str(projectId)+'.sql')
            shutil.copy('data/template.sql','data/last/'+str(projectId)+'.sql')

        con = sqlite3.connect('data/'+projectId+'.sql')
        con.text_factory = str
        cur = con.cursor()
        conLs = sqlite3.connect('data/last/'+projectId+'.sql')
        conLs.text_factory = str
        curLs = conLs.cursor()
        totalFiles = 0
        for root, dirs, filenames in os.walk(projectDir):
            for f in filenames:
                totalFiles += 1

        self.progressBar.show()
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(totalFiles)
        currentProgress = 0

        for root, dirs, filenames in os.walk(projectDir):
            currentDir = root[len(projectDir)+1:]
            if currentDir != "":
                currentDir = currentDir+'/'
            for f in filenames:
                currentFile = currentDir+f
                variables = [currentFile]
                currentFileHash = hashlib.md5(open(root+'/'+f).read()).hexdigest()
                curLs.execute("SELECT * FROM project WHERE file=?",variables)
                row = curLs.fetchone()
                if row: #is it in Last sql ?
                    if currentFileHash != row[1]: #did it change ?                         
                        newVariables = [currentFileHash,currentFile]
                        cur.execute("UPDATE project SET hash=? WHERE file=?",newVariables)
                        self.addItemToTree("Modified",currentFile)

                else: #fil may be new ? if not update hash anyway
                    cur.execute("SELECT * FROM project WHERE file=?",variables)
                    row = cur.fetchone()
                    if row: # File exists , update hash
                        newVariables = [currentFileHash,currentFile]
                        cur.execute("UPDATE project SET hash=? WHERE file=?",newVariables)
                    else: # File is new
                        newVariables = [currentFile,currentFileHash]
                        cur.execute("INSERT INTO project VALUES(?,?)",newVariables)

                    self.addItemToTree("New",currentFile)

                currentProgress += 1
                self.progressBar.setValue(currentProgress)

        con.commit()
           
        self.pushButton_compare.setEnabled(True)
        if self.treeWidget.topLevelItemCount() > 0:
            self.logNew(str(self.treeWidget.topLevelItemCount())+" files to be uploaded.")
            self.pushButton_update.setEnabled(True)
        else:
            self.logNew("Nothing to upload.")

        self.pushButton_new.setEnabled(True)
        self.treeWidget.setEnabled(True)
        self.comboBox_projects.setEnabled(True)

        self.progressBar.hide()

    def addItemToTree(self,fileState,currentFile):
        item = QtGui.QTreeWidgetItem(["",fileState,currentFile])
        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        item.setCheckState(0,QtCore.Qt.Checked)
        currentExt = currentFile.split('.')
        currentExt = currentExt[len(currentExt)-1]
        icon = QtGui.QIcon()
        if currentExt == "html":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/text-html.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "css":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/text-css.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "bmp":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/image-bmp.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "jpg" or currentExt == "jpeg":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/image-jpeg.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "png":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/image-png.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "gif":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/image-gif.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "tga":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/image-tiff.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "ico":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/image-x-ico.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "xml":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/text-xml.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "wav":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/audio-x-generic.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "py" or currentExt == "pyc":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/text-x-python.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "psd":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/image-x-psd.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "avi" or currentExt == "mp4" or currentExt == "ogg" or currentExt == "ogv":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/video-x-generic.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "php":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/application-x-php.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "exe":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/application-x-ms-dos-executable.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "swf" or currentExt == "flv":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/application-x-flash-video.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "exe":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/application-x-ms-dos-executable.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "pdf":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/application-pdf.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "js":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/text-x-javascript.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "zip" or currentExt == "7z" or currentExt == "rar" or currentExt == ".gz":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/application-x-archive.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "tpl" or currentExt == "lng":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/text-x-generic-template")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "so" or currentExt == "bin" or currentExt == "sh":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/application-x-executable.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "xcf":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/gimp.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif currentExt == "svg" or currentExt == "ai":
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/inkscape.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        else:
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("data/icons/unknown.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        
        item.setIcon(2, icon)
        self.treeWidget.insertTopLevelItem(0,item)

    def newProjectAdd(self):
        title = ui_newProject.lineEdit_projectTitle.text()
        directory = ui_newProject.lineEdit_localDirectory.text()
        ftp_host = ui_newProject.lineEdit_ftpHost.text()
        ftp_user = ui_newProject.lineEdit_ftpUser.text()
        ftp_password = ui_newProject.lineEdit_ftpPassword.text()
        ftp_directory = ui_newProject.lineEdit_ftpDirectory.text()

        if title != "" and directory != "" and ftp_host != "" and ftp_user != "" and ftp_directory != "":
            con = sqlite3.connect('data/main.sql')
            con.text_factory = str
            cur = con.cursor()
            projectId = time.time()
            variables = [str(projectId),str(title),str(directory),str(ftp_host),str(ftp_user),str(ftp_password),"",str(ftp_directory),""]
            cur.execute("INSERT INTO main VALUES(?,?,?,?,?,?,?,?,?)",variables)
            con.commit()
            self.comboBox_projects.addItem(str(title)) #replace with the new one
            self.logNew("Created new project: "+str(title))
            self.showProjects()
            NewProject.hide()
        else:
            self.logNew("Please fill required fields.")

class Ui_formProjects(object):
    def setupUi(self, formProjects):
        formProjects.setObjectName(_fromUtf8("formProjects"))
        formProjects.resize(406, 220)
        formProjects.setMinimumSize(QtCore.QSize(406, 220))
        formProjects.setMaximumSize(QtCore.QSize(406, 220))

        self.widget = QtGui.QWidget(formProjects)
        self.widget.setGeometry(QtCore.QRect(10, 10, 385, 214))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        self.pushButton_addProject = QtGui.QPushButton(formProjects)
        self.pushButton_addProject.setGeometry(QtCore.QRect(157, 180, 94, 24))
        self.pushButton_addProject.setObjectName(_fromUtf8("pushButton_addProject"))

        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_projectTitle = QtGui.QLineEdit(self.widget)
        self.lineEdit_projectTitle.setObjectName(_fromUtf8("lineEdit_projectTitle"))
        self.gridLayout.addWidget(self.lineEdit_projectTitle, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_localDirectory = QtGui.QLineEdit(self.widget)
        self.lineEdit_localDirectory.setObjectName(_fromUtf8("lineEdit_localDirectory"))
        self.gridLayout.addWidget(self.lineEdit_localDirectory, 1, 1, 1, 1)

        self.pushButton_browse = QtGui.QPushButton(self.widget)
        self.pushButton_browse.setObjectName(_fromUtf8("pushButton_browse"))
        self.gridLayout.addWidget(self.pushButton_browse, 1, 2, 1, 1)

        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEdit_ftpHost = QtGui.QLineEdit(self.widget)
        self.lineEdit_ftpHost.setObjectName(_fromUtf8("lineEdit_ftpHost"))
        self.gridLayout.addWidget(self.lineEdit_ftpHost, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.widget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.lineEdit_ftpUser = QtGui.QLineEdit(self.widget)
        self.lineEdit_ftpUser.setObjectName(_fromUtf8("lineEdit_ftpUser"))
        self.gridLayout.addWidget(self.lineEdit_ftpUser, 3, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.widget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.lineEdit_ftpPassword = QtGui.QLineEdit(self.widget)
        self.lineEdit_ftpPassword.setObjectName(_fromUtf8("lineEdit_ftpPassword"))
        self.gridLayout.addWidget(self.lineEdit_ftpPassword, 4, 1, 1, 1)
       
        self.label_7 = QtGui.QLabel(self.widget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)
        self.lineEdit_ftpDirectory = QtGui.QLineEdit(self.widget)
        self.lineEdit_ftpDirectory.setObjectName(_fromUtf8("lineEdit_ftpDirectory"))
        self.gridLayout.addWidget(self.lineEdit_ftpDirectory, 6, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.widget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 7, 0, 1, 1)

        self.retranslateUi(formProjects)
        QtCore.QMetaObject.connectSlotsByName(formProjects)

        #functions

        self.pushButton_addProject.clicked.connect(ui.newProjectAdd)
        self.pushButton_browse.clicked.connect(self.selectDir)

    def retranslateUi(self, formProjects):
        formProjects.setWindowTitle(_translate("formProjects", "Create New Project", None))
        self.pushButton_addProject.setText(_translate("formProjects", "Add Project", None))
        self.pushButton_browse.setText(_translate("formProjects", "Browse", None))
        self.label.setText(_translate("formProjects", "Project Title", None))
        self.label_2.setText(_translate("formProjects", "Local Directory", None))
        self.label_3.setText(_translate("formProjects", "FTP Host", None))
        self.label_4.setText(_translate("formProjects", "FTP User", None))
        self.label_5.setText(_translate("formProjects", "FTP Password", None))
        self.label_7.setText(_translate("formProjects", "FTP Directory", None))

    def selectDir(self):
        dirname = QtGui.QFileDialog.getExistingDirectory(None,'Select directory of project',expanduser('~'))
        self.lineEdit_localDirectory.setText(dirname)



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.showProjects()
    MainWindow.show()

    NewProject = QtGui.QMainWindow(MainWindow)
    NewProject.setModal(True)
    ui_newProject = Ui_formProjects()
    ui_newProject.setupUi(NewProject)

    sys.exit(app.exec_())
