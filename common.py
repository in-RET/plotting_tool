import os
#import threading
import multiprocessing
from PySide6.QtCore import QProcess

from plotter.processing.sankey import buildSankeyDiagram
from plotter.processing.stackedplot import buildStackedPlot

def plots(wpath, spath, window, plotSankey, plotStacked, pyqt=False):
    print("Erstelle Plots")
    if pyqt:
        window.AddLogLine("Erstelle Plots")

    datafolder = []

    for (root, dirs, files) in os.walk(wpath, topdown=True):
        if len(dirs) == 0 and len(files) > 0:
            datafolder.append(root)

    for ddir in datafolder:
        pdir = os.path.join(spath, os.path.relpath(ddir, wpath))

        if not os.path.exists(pdir):
            os.makedirs(pdir)
        
        ## First Attempt       
        #t_sankey = threading.Thread(target=sankeyDiagramme, args=(ddir, pdir, out_sankey))
        #t_stacked = threading.Thread(target=buildStackedPlot, args=(ddir, pdir))
        
        ## Second Attempt
        if plotSankey:
            t_sankey = multiprocessing.Process(target=sankeyDiagramme, args=(ddir, pdir))
            t_sankey.start()

        if plotStacked:
            t_stacked = multiprocessing.Process(target=buildStackedPlot, args=(ddir, pdir))
            t_stacked.start()

        ## Third Attempt
        #process = QProcess()
        #process.setProcessChannelMode(QProcess.MergedChannels)
        #process.start( "program_name", [ "arguments" ] )
        #process.readyReadStandardOutput.connect( aFunction )

        # then in the function...
        #outputBytes = process.readAll().data()
        #outputUnicode = outputBytes.decode( 'utf-8' )
        #messageWidget.append( outputUnicode )


    if pyqt:
        window.AddLogLine("Generation started...")

def sankeyDiagramme(ddir, pdir, output=False):
    picture = buildSankeyDiagram(ddir, "Energieflussdiagramm", output=output)

    file = open(os.path.join(pdir, "energieflussdiagramm_" + os.path.basename(ddir) + ".html"), 'wt', encoding="utf8")
    file.write(picture)
    file.close()