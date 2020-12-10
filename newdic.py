#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os, sys
if sys.version_info[0] == 2:
    from Tkinter import *
    from tkFont import Font
    from ttk import *
    #Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
    from tkMessageBox import *
    #Usage:f=tkFileDialog.askopenfilename(initialdir='E:/Python')
    #import tkFileDialog
    #import tkSimpleDialog
else:  #Python 3.x
    from tkinter import *
    from tkinter.font import Font
    from tkinter.ttk import *
    from tkinter.messagebox import *
    #import tkinter.filedialog as tkFileDialog
    #import tkinter.simpledialog as tkSimpleDialog    #askstring()

import random
import time
from collections import Iterable
import mp3play
import requests
import threading

from contextlib import contextmanager
from os import chdir, getcwd, listdir, remove, makedirs
from os.path import isfile, exists, join, expanduser

def check_cache(f):
    def _wrapper(words,voicetype):
        if not isinstance(words, Iterable):
            words = (words)
        for word in words:
            if not isfile(word + '.mp3'):
                f([word],voicetype)
    return _wrapper


@check_cache
def download_audio(words, voicetype):
    for word in words:
        if voicetype=='y':                
            r = requests.get(
                url='http://dict.youdao.com/dictvoice?audio=' + word + '&type=1',
                stream=True)
            with open(word + '.mp3', 'wb+') as f:
                f.write(r.content)
        else:
            r = requests.get(
                url='http://dict.youdao.com/dictvoice?audio=' + word + '&type=0',
                stream=True)
            with open(word + '.mp3', 'wb+') as f:
                f.write(r.content)            
        
        #format_transfer(word, 'mp3', target_format, remove_ori=True)
@contextmanager
def change_dir(target_path):
    """A function assisting change working directory temporarily

    >>> import os
    >>> os.chdir(os.path.expanduser('~'))
    >>> os.getcwd() == os.path.expanduser('~')  # You're in your home directory now
    True
    >>> with change_dir('/usr/local'): # change working directory to '/usr/local'
    ...     print(os.getcwd())
    ...     pass # Anything you want to do in this directory
    ...
    /usr/local
    >>> os.getcwd() == os.path.expanduser('~') # You're back in your previous working directory
    True

    """
    current_path = getcwd()
    chdir(target_path)
    yield
    chdir(current_path)


def play_mp3(audio,jg):
    clip = mp3play.load(audio)
    clip.play()
    time.sleep(max(jg, clip.seconds()))
    clip.stop()

def thread_it(func, *args):
    t = threading.Thread(target=func,args=args)
    t.setDaemon(True)
    t.start()     

class Application_ui(Frame):
    #The class will create all widgets for UI.
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('小雨滴单词听写')
        self.master.geometry('529x258')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.Label1Var = StringVar(value='准备开始吧！')
        self.style.configure('TLabel1.TLabel', anchor='center', foreground='#0000FF', font=('Consolas',56))
        self.Label1 = Label(self.top, text='hello', textvariable=self.Label1Var, style='TLabel1.TLabel')
        self.Label1.setText = lambda x: self.Label1Var.set(x)
        self.Label1.text = lambda : self.Label1Var.get()
        self.Label1.place(relx=0.03, rely=0.093, relwidth=0.94, relheight=0.407)

        self.Command1Var = StringVar(value='开始听写')
        self.style.configure('TCommand1.TButton', font=('宋体',9))
        self.Command1 = Button(self.top, text='开始听写', textvariable=self.Command1Var, command=self.Command1_Cmd, style='TCommand1.TButton')
        self.Command1.setText = lambda x: self.Command1Var.set(x)
        self.Command1.text = lambda : self.Command1Var.get()
        self.Command1.place(relx=0.847, rely=0.558, relwidth=0.123, relheight=0.376)

        self.Command2Var = StringVar(value='增加单词')
        self.style.configure('TCommand2.TButton', font=('宋体',9))
        self.Command2 = Button(self.top, text='增加单词', textvariable=self.Command2Var, command=self.Command2_Cmd, style='TCommand2.TButton')
        self.Command2.setText = lambda x: self.Command2Var.set(x)
        self.Command2.text = lambda : self.Command2Var.get()
        self.Command2.place(relx=0.484, rely=0.775, relwidth=0.123, relheight=0.159)

        self.txtaddVar = StringVar(value='')
        self.txtadd = Entry(self.top, textvariable=self.txtaddVar, font=('宋体',24))
        self.txtadd.setText = lambda x: self.txtaddVar.set(x)
        self.txtadd.text = lambda : self.txtaddVar.get()
        self.txtadd.place(relx=0.06, rely=0.775, relwidth=0.376, relheight=0.159)

        self.Label2Var = StringVar(value='播报间隔（S）：')
        self.style.configure('TLabel2.TLabel', anchor='w', font=('宋体',9))
        self.Label2 = Label(self.top, text='播报间隔（S）：', textvariable=self.Label2Var, style='TLabel2.TLabel')
        self.Label2.setText = lambda x: self.Label2Var.set(x)
        self.Label2.text = lambda : self.Label2Var.get()
        self.Label2.place(relx=0.529, rely=0.589, relwidth=0.198, relheight=0.097)

        self.Command3Var = StringVar(value='预习浏览')
        self.style.configure('TCommand3.TButton', font=('宋体',9))
        self.Command3 = Button(self.top, text='预习浏览', textvariable=self.Command3Var, command=self.Command3_Cmd, style='TCommand3.TButton')
        self.Command3.setText = lambda x: self.Command3Var.set(x)
        self.Command3.text = lambda : self.Command3Var.get()
        self.Command3.place(relx=0.665, rely=0.775, relwidth=0.123, relheight=0.159)

        self.topRadioVar = StringVar()
        self.style.configure('TOption1.TRadiobutton', font=('宋体',9))
        self.Option1 = Radiobutton(self.top, text='美音', value='Option1', variable=self.topRadioVar, style='TOption1.TRadiobutton')
        self.Option1.setValue = lambda x: self.topRadioVar.set('Option1' if x else '')
        self.Option1.value = lambda : 1 if self.topRadioVar.get() == 'Option1' else 0
        self.Option1.setValue(1)
        self.Option1.place(relx=0.181, rely=0.558, relwidth=0.108, relheight=0.128)

        self.Label3Var = StringVar(value='发音：')
        self.style.configure('TLabel3.TLabel', anchor='w', font=('宋体',9))
        self.Label3 = Label(self.top, text='发音：', textvariable=self.Label3Var, style='TLabel3.TLabel')
        self.Label3.setText = lambda x: self.Label3Var.set(x)
        self.Label3.text = lambda : self.Label3Var.get()
        self.Label3.place(relx=0.076, rely=0.589, relwidth=0.078, relheight=0.097)

        self.style.configure('TOption2.TRadiobutton', font=('宋体',9))
        self.Option2 = Radiobutton(self.top, text='英音', value='Option2', variable=self.topRadioVar, style='TOption2.TRadiobutton')
        self.Option2.setValue = lambda x: self.topRadioVar.set('Option2' if x else '')
        self.Option2.value = lambda : 1 if self.topRadioVar.get() == 'Option2' else 0
        
        self.Option2.place(relx=0.318, rely=0.558, relwidth=0.108, relheight=0.128)

        self.txtjiangeVar = StringVar(value='5')
        self.txtjiange = Entry(self.top, textvariable=self.txtjiangeVar, font=('宋体',9))
        self.txtjiange.setText = lambda x: self.txtjiangeVar.set(x)
        self.txtjiange.text = lambda : self.txtjiangeVar.get()
        self.txtjiange.place(relx=0.726, rely=0.558, relwidth=0.062, relheight=0.097)


class Application(Application_ui):
    #The class will implement callback function for events and your logical code.
    def __init__(self, master=None):        
        Application_ui.__init__(self, master)

    def do_work(self,flag):        
        with open("words.txt") as f:
            lst = f.readlines()
            lst = (item.strip() for item in lst)
            lst = [item for item in lst if item != '']    
        #默认乱序
            random.shuffle(lst)       
        cache_directory = expanduser("cache")
        if not exists(cache_directory):
            makedirs(cache_directory)    
        with change_dir(cache_directory):
            if self.topRadioVar.get()=="Option1":                
                download_audio(lst,'m')
            else:
                download_audio(lst,'y')
            for item in [item + '.mp3' for item in lst]:
                if flag=="p":
                    #预习模式显示单词取消后面.mp3字符串
                    self.Label1Var.set(item[:-4])
                elif flag=="l":
                    self.Label1Var.set('听写中...')                
                play_mp3(item,int(self.txtjiangeVar.get()))       
    def Command1_Cmd(self, event=None):
        #TODO, Please finish the function here!
        thread_it(self.do_work,"l")      

    

    def Command2_Cmd(self, event=None):
        #TODO, Please finish the function here!
        if self.txtaddVar.get().strip() != "":
            with open('words.txt',"a") as file:   #”w"代表着每次运行都覆盖内容
                file.write(self.txtaddVar.get().strip() + " "+"\n") 
        self.txtaddVar.set('')
                

    def Command3_Cmd(self, event=None):
        thread_it(self.do_work,"p") 


if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()    



