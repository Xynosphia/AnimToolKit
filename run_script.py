import math
import os
import sys
import builtins
import importlib
import functools
from functools import partial

import maya.cmds as cmds
import maya.OpenMayaUI as omui


# Project paths and imports

# Get the directory containing this script
script_root = os.path.dirname(os.path.abspath(__file__))

# Add project directory to sys.path if necessary
if script_root not in sys.path:
    sys.path.insert(0, script_root)
    print(f'Added to sys.path: {script_root}')
else:
    print('Already in sys.path')


# Import project utilities and data from utilities.py
from utilities import get_selected_cam, get_selected_geo, ui_file, get_scene_cam, get_scene_geo, get_memory, get_distance_to_active_camera


# Maya version and Qt imports
version = int(cmds.about(version=True)[:4])
print(f'Maya version: {version}')

if version >= 2025:
    from PySide6 import QtWidgets as QW
    from PySide6 import QtCore as QC
    from PySide6 import QtGui as QG
    from PySide6 import QtUiTools as QTU
    import shiboken6

    from shiboken6 import wrapInstance

    print('Using PySide6')

else:
    from PySide2 import QtWidgets as QW
    from PySide2 import QtCore as QC
    from PySide2 import QtGui as QG
    from PySide2 import QtUiTools as QTU
    import shiboken2

    from shiboken2 import wrapInstance

    print('Using PySide2')


# Get Maya main window
def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QW.QWidget)


# Main UI class
class AnimToolKit():

    def __init__(self):

        # Create UI loader
        self.loader = QTU.QUiLoader()

        # Create QFile object
        self.ui_file = QC.QFile(ui_file)

        # Open UI file
        if not self.ui_file.open(QC.QIODevice.ReadOnly):
            print(
                f'Could not open UI file: '
                f'{self.ui_file.errorString()}'
            )

            return

        # Load UI and parent to Maya
        self.ui = self.loader.load(self.ui_file, maya_main_window())

        self.ui_file.close()

        # Check UI loaded successfully
        if self.ui is None:
            print('QUiLoader failed to load UI')
            return

        print('UI loaded successfully')

        # Set window properties
        self.ui.setWindowFlags(QC.Qt.Window)
        self.ui.setWindowTitle('AnimToolKit')

        # Connect buttons to class method and imported function from utilities.py

        # Selection comboboxes
        cam_list = get_scene_cam()
        sub_list = get_scene_geo()
        self.ui.Camera_List.addItems(cam_list)
        self.ui.Subject_List.addItems(sub_list)

        # Focus Box
        self.ui.camfocus_button.clicked.connect(self.focus_on_selected_subject)



        #viewport 
        # https://blog.lidia-martinez.com/embed-maya-native-ui-objects-in-pyside2-maya-2017

        #HELP ME!!!!!!
        cam_name = self.ui.Camera_List.currentData()
        if cam_name:
            current_cam = cam_name
        else:
            current_cam = "perspShape"

        # set the parent layout to the viewport window
        cmds.setParent("Viewport_Window")
        camViewport = cmds.paneLayout()
        # make a model panel
        modelPanel = cmds.modelPanel("embeddedModelPanel#", camera=current_cam, menuBarVisible=False)
        # find the pointer to the panel layout
        ptr = omui.MQtUtil.findControl(camViewport)
        # wrap the pointer to a QWidget, long changed to int
        self.viewport_widget = wrapInstance(int(ptr), QW.QWidget)
        # Use a Qt layout owned by the UI's viewport container
        self.ui.Viewport_Window.layout().addWidget(self.viewport_widget)

        # memoryPressur_bar
        memoryData = get_memory()
        max_memory = memoryData[1]
        current_memory = memoryData[0]
        self.ui.memory_bar.setValue(current_memory)
        self.ui.memory_bar.setMaximum(max_memory)

    # Class methods
    def focus_on_selected_subject(self):
        # Get selected object
        sel_subj = self.Subject_List.currentData() 
        if subj = sel_subj:
            continue
        else:
            subj = get_selected_geo()

        #Get selected camera
        sel_cam = self.Camera_List.currentData()

        # get world space position of the selected subject and camera
        subj_pos = cmds.xform(sel_subj, query=True, worldSpace=True, rotatePivot=True)
        cam_pos = cmds.xform(sel_cam, query=True, worldSpace=True, rotatePivot=True)

        # adjust camera focal distance to the selected subject
        distance = math.dist(cam_pos, subj_pos)
        focus = cmds.camera(sel_cam, depthOfField=True, focusDistance=distance)
        return focus

         


    





# Launch UI



# Create new instance
builtins.my_window = AnimToolKit()

# Check UI exists before displaying
if hasattr(builtins.my_window, 'ui'):

    builtins.my_window.ui.show()
    builtins.my_window.ui.raise_()
    builtins.my_window.ui.activateWindow()
    print('Window created and displayed')

else:
    print('Window could not be created')
     
        

