
#===============================================================================
# SET THE HOME PATH AS FIRST OPTION TO IMPORT MODULES
#===============================================================================

import sys
import os

try:    
    # ...works on at least windows and linux. 
    # In windows it points to the user's folder 
    #  (the one directly under Documents and Settings, not My Documents)


    # In windows, you can choose to care about local versus roaming profiles.
    # You can fetch the current user's through PyWin32.
    #
    # For example, to ask for the roaming 'Application Data' directory:
    #  (CSIDL_APPDATA asks for the roaming, CSIDL_LOCAL_APPDATA for the local one)
    from win32com.shell import shellcon, shell            
    HOME_PATH = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
 
except ImportError: 
   # quick semi-nasty fallback for non-windows/win32com case
    HOME_PATH = os.path.expanduser("~")

# SET THE IDE PATH ON USER DIRECTORY
HOME_NINJA_PATH = os.path.join(HOME_PATH, ".ninja_ide")


# CREATES IF NOT EXIST
if not os.path.isdir(HOME_NINJA_PATH):
        os.mkdir(HOME_NINJA_PATH)
        
# PATCH THE sys LIST
sys.path.insert(0, HOME_NINJA_PATH)


#===============================================================================
# START NINJA
#===============================================================================

import core
import resources

resources.HOME_PATH = HOME_PATH
resources.HOME_NINJA_PATH = HOME_NINJA_PATH

if __name__ == "__main__":
    core.run_ninja()
