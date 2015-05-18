__author__ = 'Laurent Dumont'
__name__ = 'Steam Skin Swapper'

import os
import psutil
import win32security
import urllib
import zipfile
import getpass

from _winreg import *


SKIN_PATH = os.getenv('APPDATA')
STEAM_PROC_NAME = "Steam.exe"

# Create a skin object with @skin_url and @skin_name


class skin:

    def __init__(self, skin_url, skin_name, skin_archive_name):
        self.skin_url = skin_url
        self.skin_name = skin_name
        self.skin_archive_name = skin_archive_name


#Download the skin @skin_array
def download_skin(skins_array,skin_id):

    for skin in skins_array:
        print "Downloading Skin " + skin.skin_name
        urllib.urlretrieve(skin.skin_url, skin.skin_name)

        with zipfile.ZipFile(skin.skin_name, "r") as skin_archive:
            if not os.path.exists(SKIN_PATH + "\\" + "SteamSkins" + "\\" + skin.skin_name):
                os.makedirs(SKIN_PATH + "\\" + "SteamSkins" + "\\" + skin.skin_name)
            skin_archive.extractall(SKIN_PATH + "\\" + "SteamSkins" + "\\" + skin.skin_name)


def find_steam_path():

    w7_path = "C:\\Program Files (x86)\\Steam\\skins"
    xp_path = "C:\\Program Files\\Steam\skins"
    global win_ver

    if os.path.exists(w7_path):
        win_ver = 'w7'

    if os.path.exists(xp_path):
        win_ver = 'xp'


def edit_selected_skin():

    user_name = getpass.getuser()
    sid = win32security.LookupAccountName(None, user_name)[0]
    sidstr = win32security.ConvertSidToStringSid(sid)

    connectRegistry = ConnectRegistry(None, HKEY_USERS)
    skin_key = OpenKey(connectRegistry, sidstr + "\Software\Valve\Steam", 0, KEY_WRITE)
    try:
        SetValueEx(skin_key, 'SkinV4', 0, REG_SZ, "air")
    except EnvironmentError:
        print "Cannot change Registry key"

    CloseKey(connectRegistry)
    CloseKey(skin_key)


def kill_steam():

    for process in psutil.process_iter():
        try:
            if process.name() == STEAM_PROC_NAME:
                try:
                    process.kill()
                except (os.Error):
                    print ('Cannot kill the Steam process. Please restart Steam manually')
        except (psutil.AccessDenied):
            print ('Cannot access process information')


def create_skin_objets():

    #Create the global variables containing the skins.
    global steamCompact
    global steamEnhanced
    global steamAir
    global skin_list

    skin_list = []
    steamCompact = skin("http://sss.coldnorthadmin.com/skins/compact/SteamCompact_1.5.27.zip", "compact", "compact.zip")
    steamEnhanced = skin("http://sss.coldnorthadmin.com/skins/enhanced/enhanced.zip", "enhanced", "enhanced.zip")
    steamAir = skin("http://sss.coldnorthadmin.com/skins/air/air.zip", "air", "air.zip")
    skin_list.append(steamEnhanced)
    skin_list.append(steamCompact)
    skin_list.append(steamAir)


def prompt_skin_choice(skins_array):

    for skin in skins_array:
        print "%s" % skin.skin_name

    try:
        skin_id = int(raw_input("Please enter the skin number"))
    except ValueError:
        print "Please select a correct skin number"

#Main function
def main():

    create_skin_objets()
    #download_skin(skin_list)
    prompt_skin_choice(skin_list)

#MAIN PROCESS
main()