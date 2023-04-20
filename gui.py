import os
import sys
from common import GoPlots

try:
    from PyQt6.QtWidgets import QPushButton, QWidget, QApplication, QVBoxLayout, QFileDialog, QProgressBar, QTabWidget, QHBoxLayout, QLabel
    from PyQt6.QtGui import QPixmap
    from PyQt6.QtCore import QUrl
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    PYQT = True
except ModuleNotFoundError:
    PYQT = False
    print("Please install PyQt5 to start the application with a graphical user interface.")


if PYQT:
    class MainWindow(QWidget):
        path_load = None
        path_save = None

        def __init__(self, parent: QApplication):
            super().__init__()

            self.checkbox_plots = None
            self.checkbox_sankey = None
            self.button_plot = None
            self.progressbar = None
            self.parent = parent
            self.initUI()

        def initUI(self):
            hbox_input = QHBoxLayout()
            hbox_output = QHBoxLayout()
            vbox = QVBoxLayout()

            ### Input GUI
            button_load_data = QPushButton("Daten-Ordner auswählen", self)
            button_load_data.clicked.connect(self.GetFolderName)
            button_load_data.setObjectName("load")
            hbox_input.addWidget(button_load_data)

            hbox_input.addStretch()

            self.button_plot = QPushButton("Erstelle Diagramme", self)
            self.button_plot.clicked.connect(self.GoPlot)
            self.button_plot.setObjectName("go")
            self.button_plot.setEnabled(False)
            hbox_input.addWidget(self.button_plot)

            qbtn = QPushButton('Quit', self)
            qbtn.clicked.connect(QApplication.instance().quit)

            hbox_input.addWidget(qbtn)

            ### Output GUI
            self.tabs = QTabWidget()

            hbox_output.addWidget(self.tabs)

            vbox.addLayout(hbox_input)
            vbox.addLayout(hbox_output)

            self.setLayout(vbox)

            self.setGeometry(300, 300, 750, 550)
            self.setWindowTitle('Plot Tool')
            self.show()

        def GetFolderName(self):
            filedialog = QFileDialog
            path = filedialog.getExistingDirectory(self, 'Ordner öffnen')

            self.path_load = path
            self.path_save = os.path.abspath(os.path.join(path, "../plots"))

            if not os.path.exists(self.path_save):
                os.makedirs(self.path_save)

            self.button_plot.setEnabled(True)

            # print("Laden:", self.path_load)
            # print("Speichern:", self.path_save)

        def AddPlotTab(self):
            # der Pfad wo die Dateien liegen
            wdir = os.path.abspath(self.path_save)
            
            if wdir is not None:
                dirData = []
                for tmpDirData in os.walk(wdir):
                    #print(tmpDirData)
                    dirData.extend(tmpDirData)
                
                for file in dirData[2]:
                    filename = os.path.basename(file)
                    if str.find(filename, ".png") > 0:
                        #print("png")
                        tab = QWidget()

                        image = QPixmap(os.path.join(wdir, filename))
                        label = QLabel()
                        label.setPixmap(image)

                        vbox = QVBoxLayout()
                        vbox.addWidget(label)
                        tab.setLayout(vbox)

                        self.tabs.addTab(tab, filename)

                    elif str.find(filename, ".html") > 0:
                        #print("html")
                        tab = QWidget()

                        browser = QWebEngineView()
                        #browser.setHtml("<h1>Hello, world!</h1>")
                        browser.load(QUrl.fromLocalFile(os.path.join(wdir, filename)))

                        vbox = QVBoxLayout()
                        vbox.addWidget(browser)
                        tab.setLayout(vbox)
                        
                        self.tabs.addTab(tab, filename)

                    else:
                        print("Nicht Identifiziert")


        def GoPlot(self):
            GoPlots(self.path_load, self.path_save)
            self.AddPlotTab()
            self.button_plot.setEnabled(False)


    def StartGui():
        app = QApplication(sys.argv)
        window = MainWindow(parent=app)
        window.show()

        sys.exit(app.exec())