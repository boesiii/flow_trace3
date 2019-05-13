# -*- coding: utf-8 -*-
"""
/***************************************************************************
 flowTrace
                                 A QGIS plugin
 Select line segments upstream of a selected line segment
                              -------------------
        begin                : 2014-02-20
        copyright            : (C) 2014 by Ed B
        email                : boesiii@yahoo.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from __future__ import print_function
# Import the PyQt and QGIS libraries
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
from builtins import str
from builtins import object
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from flowtracedialog import flowTraceDialog
import os.path
from qgis.gui import QgsMessageBar


class flowTrace(object):

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'flowtrace_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = flowTraceDialog()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/flowtrace/icon.png"),
            u"Flow Trace", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Flow Trace", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Flow Trace", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        QMessageBox.information(None, "Flow Trace", "Press Ok to start Flow Trace")
        #setup final selection list
        final_list = []
        #setup temporary selection list
        selection_list = []
        #add tolerance value
        tolerance = 1
        #get current layer
        clayer = self.iface.mapCanvas().currentLayer()
        
        if clayer is None:
            return 
        
        #get provider
        provider = clayer.dataProvider()
        
        #get selected features
        features = clayer.selectedFeatures()
        
        #if not clayer.selectedFeatures():
        #   QMessageBox.information(None, "Flow Trace", "No Features Selected")
        #   exit(0)
        
        # get crs for tolerance setting
        crs = self.iface.activeLayer().crs().authid()
        # fix_print_with_import
        # fix_print_with_import
print(crs)
        if crs == 'EPSG:4269':
            rec = .0001
            tolerance = .0001
        else:
            rec = 1
        #print tolerance
        
            
        
        #iterate thru features to add to lists
        for feature in features:            
            # add selected features to final list
            final_list.append(feature.id())
            # add selected features to selection list for while loop
            selection_list.append(feature.id())
            #get feature geometry
            geom = feature.geometry()
            if geom.type() != QGis.Line:
                # fix_print_with_import
                print("Geometry not allowed")
                QMessageBox.information(None, "Flow Trace", "Geometry not allowed, \nPlease select line geometry only.")
                return
            
        
        
        
        #loop thru selection list
        while selection_list:
        
            #get selected features
            request = QgsFeatureRequest().setFilterFid(selection_list[0])
            feature = next(clayer.getFeatures(request))            
            
            # get list of nodes
            nodes = feature.geometry().asPolyline()
            
            # get upstream node
            upstream_coord = nodes[0]
                        
            # select all features around upstream coordinate using a bounding box
            rectangle = QgsRectangle(upstream_coord.x() - rec, upstream_coord.y() - rec, upstream_coord.x() + rec, upstream_coord.y() + rec)
            request = QgsFeatureRequest().setFilterRect(rectangle)
            features = clayer.getFeatures(request)
                        
            #iterate thru requested features
            for feature in features:
            
                #get list of nodes
                #print feature.id()
                nodes = feature.geometry().asPolyline()
                
                #get downstream node
                downstream_coord = nodes[-1]
                
                #setup distance
                distance = QgsDistanceArea()
                
                #get distance from downstream node to upstream node
                dist = distance.measureLine(downstream_coord, upstream_coord)
                
                #Below is the distance rounded to 2 decimal places only needed during testing
                #dist = round (distance.measureLine(downstream_coord, upstream_coord), 2)
                
                if dist < tolerance:
                    #add feature to final list
                    final_list.append(feature.id())
                    
                    #add feature to selection list to keep selecting upstream line segments
                    #selection_list.append(feature.id())
                                        
                    if feature.id() not in selection_list:
                        #add feature to selection list
                        selection_list.append(feature.id())
                
            #remove feature from selection list
            selection_list.pop(0)
            
            
        #select features using final_list           
        clayer.setSelectedFeatures(final_list)
        
        #refresh the canvas
        self.iface.mapCanvas().refresh()
        QMessageBox.information(None, "Flow Trace Complete", "Total Features Selected: " + str(len(final_list)))