# ==========================================================
#   Export save selected shapes as SVG file plug-in v0.2 
# ==========================================================
# Copyright (C) 2024 L.Sumireneko.M
# This program is free software: you can redistribute it and/or modify it under the 
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#  without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>. 

from krita import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5 import QtCore

from io import StringIO
import re,os,time,copy,math



# ====================
# Utilities
# ====================

def message(mes):
    mb = QMessageBox()
    mb.setText(str(mes))
    mb.setWindowTitle('Message')
    mb.setStandardButtons(QMessageBox.Ok)
    ret = mb.exec()
    if ret == QMessageBox.Ok:
        pass # OK clicked


# create dialog  and show it
def notice_autoclose_dialog(message):
    app = Krita.instance()
    qwin = app.activeWindow().qwindow()
    qq = qwin.size()
    wpos = math.ceil(qq.width() * 0.45)
    hpos = math.ceil(qq.height() * 0.45)
    
    noticeDialog = QDialog() 
    noticeDialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    label = QLabel(message)
    hboxd = QHBoxLayout()
    hboxd.addWidget(label)
    noticeDialog.setLayout(hboxd)
    noticeDialog.setWindowTitle("Title") 
    
    noticeDialog.move(qwin.x()+wpos,qwin.y()+hpos)
    QtCore.QTimer.singleShot(1500, noticeDialog.close)
    noticeDialog.exec_() # show

# ====================
# Main
# ====================
def save_file(sdata):
    file = QFileDialog.getSaveFileName(None,'Set the name of save file(s)',os.path.expanduser('~' + '/Desktop'), filter = 'SVG (*.svg)')
    # print('Select file:'+file[0])
    if file[0] == '':print('No select to file for open');return

    file_path = file[0]
    full_path = os.path.expanduser(file_path)
    if full_path.endswith('.svg') == False:print('Not svg extension');return


    # mode w(overwrite) or x(not overwrite)
    for c in range(0,len(sdata)):
        mod_path = re.sub( r"(\.svg)$", r'{0}\1' , full_path)
        mod_path = mod_path.format(c)
        #print(f"- Save file: {mod_path}")
        
        try:
            with open(mod_path, mode='x', encoding='UTF-8') as f:
                f.write(sdata[c])
        except FileExistsError:
            pass

def main():
    global dir,svg_path,export_file
    app = Krita.instance()
    doc = app.activeDocument()
    lay = doc.activeNode()
    
    if lay.type() == 'vectorlayer':
    
        app.action('InteractionTool').trigger()# Select shape tool
        shapes = lay.shapes()
        #print(" "+str(len(shapes))+" shapes found in this active VectorLayer")
        
        selected_shapes = []
        #print("-- ↑ Front -- ") 
        
        # Get All shape info
        # Range = len()-1 .... 0 
        for i in range(len(shapes)-1,-1,-1):
            sp = shapes[i]
            #print(f'* Shape({i}), Name: {sp.name()}  ,Type: {sp.type()} , isSelected?: {sp.isSelected()} , ID :{sp} ')
    
            # Get the selected shape
            if sp.isSelected() == True:
                selected_shapes.append(sp)
        #print("-- ↓ Back -- ")
        
        #print(" ")
        #print(f" {len(selected_shapes)} / {len(shapes)} shapes selected")

        svg_parts=[]
        if len(selected_shapes) == 0:print("No files");return

        svg_attr= 'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"   xmlns:krita="http://krita.org/namespaces/svg/krita"  xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" preserveAspectRatio="none" '
        # Detail of the selected shapes
        for j in range(len(selected_shapes)-1,-1,-1):
            s = selected_shapes[j]
            name = s.name()
            type = s.type()

            # get bounding box
            [x,y,w,h] = s.boundingBox().getRect()
            wpt = w#*0.72
            hpt = h#*0.72

            #print(" ------------------ ")
            #print(f'* Shape({j}), Type:{type} , \n '+s.toSvg())
            containts = s.toSvg()
            fntmatrix = ""
            font_ofs = 0
            if type == 'KoSvgTextShapeID':
                # read one time only at match (before from the tag boundrady '>' )
                fs_srch = re.search(r'font-size:\s?(.*?);(?=.*?>)',containts);
                mat = s.transformation()
                q = [mat.m11(),mat.m12(),mat.m13(),mat.m21(),mat.m22(),mat.m23(),mat.m13(),mat.m32(),mat.m33()]
                fntmatrix=f' transform="matrix({q[0]} {q[1]} {q[3]} {q[4]} 0 0)"'

                if fs_srch:
                    font_ofs = float(fs_srch.group(1))*0.5

            wpt2 = wpt*0.375 + (font_ofs*2)
            hpt2 = hpt*0.375 + (font_ofs*2)


            containts = re.sub( r'translate\(.*?\)(?=.*?>)','translate(0,0)' , containts,1)

            containts = re.sub( r'(matrix\(.*?\s.*?\s.*?\s.*?\s)(.*?)(\))(?=.*?>)',r'\1 0 0\3' , containts,1)

            if type == 'KoSvgTextShapeID':
                containts = re.sub( r'<text', r'<text{}'.format(fntmatrix) , containts,1)


            svgdata = f'<svg {svg_attr} width="{wpt}pt" height="{hpt}pt" viewBox="-{wpt2} -{hpt2} {wpt*2} {hpt*2}">\n{containts}\n</svg>'
            svg_parts.append(svgdata)

        save_file(svg_parts)
        notice_autoclose_dialog("Saved selected shape(s) each svg file(s)!!")



class export_shapes(Extension):

    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)

    def setup(self):
        #This runs only once when app is installed
        pass

    def createActions(self, window):
        # optional location: "tools/scripts"
        action = window.createAction("export_shapes", "Save Selected Shapes as SVGs...", f"Layer/LayerImportExport")
        action.triggered.connect(main)

        pass

