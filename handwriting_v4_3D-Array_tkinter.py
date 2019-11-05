#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 22:54:17 2019

@author: moritote
"""

import os, tkinter, tkinter.filedialog
from PIL import Image, ImageDraw
import numpy as np



class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('tkinter canvas trial')
        self.master.minsize(420,335)
        self.master.configure(bg='black')
        self.pack()
        self.create_widgets()
        self.setup()
        self.hiragana = [chr(i) for i in range(12353, 12436)]
        #self.arg_num = 0

    def create_widgets(self):
        #フォルダ選択ボタンの配置、設定
        self.folder_button = tkinter.Button(self, text='select folder', command=self.folder_select)
        self.folder_button.grid(row=0, column=0)

        #選択されたフォルダテキストの配置、設定
        self.folder_label = tkinter.Label(self)
        self.folder_label.grid(row=0, column=1, columnspan=2)

        #記入文字支持テキストの配置、設定
        self.hiragana_label = tkinter.Label(self)
        self.hiragana_label.grid(row=1, column=0)

        #画面クリアボタンの配置、設定
        self.clear_button = tkinter.Button(self, text='clear all', command=self.clear_canvas)
        self.clear_button.grid(row=1, column=1)
        
        #セーブボタンの配置、設定
        self.save_button = tkinter.Button(self, text='save', command=self.save_canvas)
        self.save_button.grid(row=1, column=2)
        

        #文字記入画面の配置、設定
        self.test_canvas = tkinter.Canvas(self, bg='white', width=256, height=256)
        self.test_canvas.grid(row=2, column=0, columnspan=3)
        self.test_canvas.bind('<B1-Motion>', self.paint)
        self.test_canvas.bind('<ButtonRelease-1>', self.reset)

    def setup(self):
        #各種パラメータの初期化
        self.old_x = None
        self.old_y = None
        self.color = 'black'
        self.eraser_on = False
        self.im = Image.new('RGB', (256, 256), 'white')
        self.draw = ImageDraw.Draw(self.im)
        
        #筆跡記憶配列　３次元配列ver
        #np.full(((線の本数、描画数、x・y)))
        self.data = np.full(((100,1000,2)),-100)
        self.n = 0
        self.plot_size = 0

    def folder_select(self):
        #フォルダ選択ボタン押下時呼び出し関数
        self.iDir = os.path.abspath(os.path.dirname(__file__))
        self.dir = tkinter.filedialog.askdirectory(initialdir = self.iDir)
        self.folder_label["text"] = self.dir
        self.chk_path = self.dir + "/chk.npy"
        if os.path.exists(self.chk_path):
            self.arg_num = np.load(self.chk_path)
        else:
            self.arg_num = 0
        if self.arg_num < len(self.hiragana):
            self.hiragana_label["text"] = "「" + self.hiragana[self.arg_num] + "」を記入"
        else:
            self.hiragana_label["text"] = "完了！"
    
    def clear_canvas(self):
        #画面クリアボタン押下時呼び出し関数
        self.test_canvas.delete(tkinter.ALL)
        self.im = Image.new('RGB', (256, 256), 'white')
        self.draw = ImageDraw.Draw(self.im)
        self.data = np.full(((100,1000,2)),-100)
        self.plot_size=0
        self.n=0
        #print ("clear")

    def save_canvas(self):
        #セーブボタン押下時呼び出し関数
        self.path_w = self.dir + "/" + self.hiragana[self.arg_num] + ".npy"
        #配列を軽くしてからnumpy形式で保存
        self.data0=self.data[0:self.n,:,:]
        np.save(self.path_w, self.data0)
        
         #画像ファイルを保存
        filename = self.dir + "/" + self.hiragana[self.arg_num] + ".jpg"
        self.im1 = self.im.resize((256,256),Image.ANTIALIAS)
        self.im1.save(filename)
        #次書く文字を保存
        self.arg_num += 1
        np.save(self.chk_path, self.arg_num)
        if self.arg_num < len(self.hiragana):
            self.hiragana_label["text"] = "「" + self.hiragana[self.arg_num] + "」を記入"
        else:
            self.hiragana_label["text"] = "完了！"
        
        #画面の初期化
        self.test_canvas.delete(tkinter.ALL)
        self.im = Image.new('RGB', (256, 256), 'white')
        self.draw = ImageDraw.Draw(self.im)
        self.data = np.full(((100,1000,2)),-100)
        self.plot_size=0
        self.n=0
        #print(self.data0)
        print ("write: ",self.path_w)

    def paint(self, event):
        #マウスクリック時呼び出し関数
        paint_color = 'black'
        if event.x>=0 and event.x<=256 and event.y>=0 and event.y<=256:
            if self.old_x and self.old_y:
                self.test_canvas.create_line(self.old_x, self.old_y, event.x, event.y, width=5.0, fill=paint_color, capstyle=tkinter.ROUND, smooth=tkinter.TRUE, splinesteps=36)
                self.draw.line((self.old_x, self.old_y, event.x, event.y), fill=paint_color, width=5)
                #self.geo_label["text"] = "{" + str(event.x) + ","+ str(event.y) + "}"
                self.old_x_norm = int(self.old_x*100/256)
                self.old_y_norm = int(self.old_y*100/256)
                self.event_x_norm = int(event.x*100/256)
                self.event_y_norm = int(event.y*100/256)
                if self.old_x_norm != self.event_x_norm or self.old_y_norm != self.event_y_norm:
                    self.data[self.n,self.plot_size] = (self.event_x_norm, self.event_y_norm)
                    self.plot_size += 1        
            self.old_x = event.x
            self.old_y = event.y

    def reset(self, event):
        #マウスクリック終了時呼び出し関数
        self.old_x, self.old_y = None, None
        self.n+=1
        self.plot_size = 0

#メイン処理
root = tkinter.Tk()
app = Application(master=root)
app.mainloop()