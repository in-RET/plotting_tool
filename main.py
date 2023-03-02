import os
import sys

from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QVBoxLayout, QFileDialog, QCheckBox, QProgressBar

from plotter.processing.sankey import buildSankeyDiagram
from plotter.processing.stackedplot import PlotStacked


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
        hbox = QVBoxLayout()

        button_load_data = QPushButton("Daten-Ordner auswählen", self)
        button_load_data.clicked.connect(self.GetFolderName)
        button_load_data.setObjectName("load")
        hbox.addWidget(button_load_data)

        hbox.addSpacing(25)

        self.checkbox_plots = QCheckBox("Zeige Plot-Ausgabe")
        hbox.addWidget(self.checkbox_plots)

        self.checkbox_sankey = QCheckBox("Zeige Sankey-Ausgabe")
        hbox.addWidget(self.checkbox_sankey)

        self.button_plot = QPushButton("Erstelle Diagramme", self)
        self.button_plot.clicked.connect(self.GoPlot)
        self.button_plot.setObjectName("go")
        self.button_plot.setEnabled(False)
        hbox.addWidget(self.button_plot)

        self.progressbar = QProgressBar()
        hbox.addWidget(self.progressbar)

        hbox.addSpacing(15)

        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QApplication.instance().quit)

        hbox.addWidget(qbtn)

        self.setLayout(hbox)

        self.move(300, 300)
        self.setWindowTitle('Plot Tool')
        self.show()

    def GetFolderName(self):
        filedialog = QFileDialog
        path = filedialog.getExistingDirectory(self, 'Ordner öffnen')

        self.path_load = path
        self.path_save = os.path.join(path, "../plots")

        if not os.path.exists(self.path_save):
            os.makedirs(self.path_save)

        self.button_plot.setEnabled(True)

        # print("Laden:", self.path_load)
        # print("Speichern:", self.path_save)

    def GoPlot(self):
        print("Erstelle Plots")

        if self.path_save is not None and self.path_load is not None:
            wpath = self.path_load
            spath = self.path_save

            datafolders = []

            for (root, dirs, files) in os.walk(wpath, topdown=True):
                if len(dirs) == 0 and len(files) > 0:
                    datafolders.append(root)

            self.progressbar.setRange(0, len(datafolders))
            self.progressbar.setEnabled(True)
            self.progressbar.setValue(0)

            for ddir in datafolders:
                pdir = os.path.join(spath, os.path.relpath(ddir, wpath))

                if not os.path.exists(pdir):
                    os.makedirs(pdir)

                SankeyDiagramme(ddir=ddir, pdir=pdir, output=self.checkbox_sankey.isChecked())
                PlotStacked(ddir=ddir, pdir=pdir, output=self.checkbox_plots.isChecked())

                self.progressbar.setValue(self.progressbar.value() + 1)
                self.parent.processEvents()

            print("Fin.")


def SankeyDiagramme(ddir, pdir, output=False):
    picture = buildSankeyDiagram(ddir, "Energieflussdiagramm", output=output)

    file = open(os.path.join(pdir, "energieflussdiagramm_" + os.path.basename(ddir) + ".html"), 'wt')
    file.write(picture)
    file.close()


def StartGui():
    app = QApplication(sys.argv)
    window = MainWindow(parent=app)
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    StartGui()
