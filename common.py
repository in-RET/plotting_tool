import os

from plotter.processing.sankey import buildSankeyDiagram
from plotter.processing.stackedplot import buildStackedPlot


def plots(wpath, spath, out_sankey=False):
    print("Erstelle Plots")

    datafolder = []

    for (root, dirs, files) in os.walk(wpath, topdown=True):
        if len(dirs) == 0 and len(files) > 0:
            datafolder.append(root)

    for ddir in datafolder:
        pdir = os.path.join(spath, os.path.relpath(ddir, wpath))

        if not os.path.exists(pdir):
            os.makedirs(pdir)
        
        sankeyDiagramme(ddir=ddir, pdir=pdir, output=out_sankey)
        buildStackedPlot(ddir=ddir, pdir=pdir)

    print("Fin.")


def sankeyDiagramme(ddir, pdir, output=False):
    picture = buildSankeyDiagram(ddir, "Energieflussdiagramm", output=output)

    file = open(os.path.join(pdir, "energieflussdiagramm_" + os.path.basename(ddir) + ".html"), 'wt', encoding="utf8")
    file.write(picture)
    file.close()