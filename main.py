import os
import time
import tkinter
from modules import modules
import threading
from PIL import ImageTk
from modules import _utils
from modules import _config
from tkinter import messagebox

version = '2.3'

if not os.path.isfile('./data/config.json'):
    messagebox.showerror('Error', message='config.jsonが見つかりません。\ndata/config.jsonを設定してください')

def reload_status(threading_counter_label, caches_counter_label, proxy_counter_label):
    while True:
        try:
            threading_counter_label['text'] = f'Active Threads: {threading.active_count()}'
        except RuntimeError:
            pass
        caches_counter_label['text'] = f'Caches: {len(_utils.caches)}'
        proxy_counter_label['text'] = f'Proxies: {len(_utils.proxies)}'
        time.sleep(1)

def change_module(event):
    if len(listbox.curselection()) != 0:
        module_number = listbox.curselection()[0]
        children = module_frame.winfo_children()
        for child in children:
            child.destroy()
        tkinter.Label(master=module_frame, text=modules[module_number].module['name'], font=(None, 20), foreground='#ffffff', background='#2c2f33').pack()
        tkinter.Label(master=module_frame, text=modules[module_number].module['description'], font=(None, 10), foreground='#ffffff', background='#2c2f33').pack()
        modules[module_number].draw_module(module_frame)

def config_menu():
    children = module_frame.winfo_children()
    for child in children:
        child.destroy()
    tkinter.Label(master=module_frame, text=_config.module['name'], font=(None, 20), foreground='#ffffff', background='#2c2f33').pack()
    _config.draw_module(module_frame)

def about_menu():
    children = module_frame.winfo_children()
    for child in children:
        child.destroy()
    tkinter.Label(master=module_frame, text=f'Thunder Raider v{version}', font=(None, 20), foreground='yellow', background='#2c2f33').pack()
    tkinter.Label(master=module_frame, image=icon).pack()
    tkinter.Label(master=module_frame, text='by Raizou', font=(None, 20), foreground='#ffffff', background='#2c2f33').pack()

print(f'Thunder v{version}')
print('by Raizou\n')

root = tkinter.Tk()
icon = ImageTk.PhotoImage(file=os.path.dirname(__file__)+'/icon.ico')  
root.iconphoto(False, icon)
root.title(f'Thunder v{version}')
root.geometry('800x500')
root.resizable(False, False)

header_frame = tkinter.Frame(master=root, width=200, height=500, background='#2c2f33')
header_frame.propagate(False)
module_frame = tkinter.Frame(master=root, width=600, height=500, background='#2c2f33')
module_frame.propagate(False)

tkinter.Label(master=header_frame, text='Thunder', font=(None, 30), foreground='yellow', background='#2c2f33').pack()
tkinter.Label(master=header_frame, text=f'Version:{version}', font=(None, 15), foreground='#ffffff', background='#2c2f33').pack()
tkinter.Label(master=header_frame, text='Modules', foreground='#ffffff', background='#2c2f33').pack()

listbox = tkinter.Listbox(master=header_frame, font=(None, 12), width=24, height=16, justify='center', foreground='#ffffff', background='#2c2f33')
listbox.bind('<<ListboxSelect>>', change_module)
for module in modules:
    listbox.insert(tkinter.END, module.module['name'])
listbox.pack()

threading_counter_label = tkinter.Label(master=header_frame, foreground='#ffffff', background='#2c2f33')
threading_counter_label.pack()
caches_counter_label = tkinter.Label(master=header_frame, foreground='#ffffff', background='#2c2f33')
caches_counter_label.pack()
proxy_counter_label = tkinter.Label(master=header_frame, foreground='#ffffff', background='#2c2f33')
proxy_counter_label.pack()

tkinter.Button(master=header_frame, text='Config Menu', foreground='#ffffff', background='#2c2f33', command=config_menu).pack()
tkinter.Button(master=header_frame, text='About Thunder', foreground='#ffffff', background='#2c2f33', command=about_menu).pack()

config_menu()

header_frame.pack(side=tkinter.LEFT)
module_frame.pack(side=tkinter.LEFT)

if len(_utils.caches) == 0:
    messagebox.showinfo('Information', message='caches.jsonにデータが入っていません\nConfig MenuからRefresh Cachesをしてください')

threading.Thread(target=reload_status, args=(threading_counter_label,caches_counter_label,proxy_counter_label)).start()
root.mainloop()