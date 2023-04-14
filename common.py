import os

from plotter.processing.sankey import buildSankeyDiagram
from plotter.processing.stackedplot import PlotStacked
from plotter.processing.radarplot import buildRadarPlot


def GoPlots(wpath, spath, out_plot, out_sankey, out_radar):
    print("Erstelle Plots")

    datafolders = []

    for (root, dirs, files) in os.walk(wpath, topdown=True):
        if len(dirs) == 0 and len(files) > 0:
            datafolders.append(root)

    for ddir in datafolders:
        pdir = os.path.join(spath, os.path.relpath(ddir, wpath))

        if not os.path.exists(pdir):
            os.makedirs(pdir)

        SankeyDiagramme(ddir=ddir, pdir=pdir, output=out_sankey)
        PlotStacked(ddir=ddir, pdir=pdir, output=out_plot)
        RadarPlots(ddir=ddir, pdir=pdir, output=out_radar)

    print("Fin.")

def RadarPlots(ddir, pdir, output=False):
    picture = buildRadarPlot(ddir, "Radarplot", output=output)
    file = open(os.path.join(pdir, "radarplot" + os.path.basename(ddir) + ".html"), 'wt')
    file.write(picture)
    file.close()

def SankeyDiagramme(ddir, pdir, output=False):
    picture = buildSankeyDiagram(ddir, "Energieflussdiagramm", output=output)

    file = open(os.path.join(pdir, "energieflussdiagramm_" + os.path.basename(ddir) + ".html"), 'wt')
    file.write(picture)
    file.close()