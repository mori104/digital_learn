#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 22:54:17 2019

@author: moritote
"""

import tkinter
from PIL import Image, ImageDraw
import numpy as np


class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('tkinter canvas trial')
        self.pack()
        self.create_widgets()
        self.setup()

    def create_widgets(self):
        #画面クリアボタンの配置、設定
        self.clear_button = tkinter.Button(self, text='clear all', command=self.clear_canvas)
        self.clear_button.grid(row=0, column=0)
        
        #セーブボタンの配置、設定
        self.save_button = tkinter.Button(self, text='save', command=self.save_canvas)
        self.save_button.grid(row=0, column=1)
        
        #現在の座標表示テキストの配置、設定
        self.geo_label = tkinter.Label(self)
        self.geo_label.grid(row=0, column=2)

        #文字記入画面の配置、設定
        self.test_canvas = tkinter.Canvas(self, bg='white', width=512, height=512)
        self.test_canvas.grid(row=1, column=0, columnspan=3)
        self.test_canvas.bind('<B1-Motion>', self.paint)
        self.test_canvas.bind('<ButtonRelease-1>', self.reset)

    def setup(self):
        #各種パラメータの初期化
        self.old_x = None
        self.old_y = None
        self.color = 'black'
        self.eraser_on = False
        self.im = Image.new('RGB', (512, 512), 'white')
        self.draw = ImageDraw.Draw(self.im)
        
        #筆跡記憶配列　３次元配列ver
        #np.full(((線の本数、描画数、x・y)))
        self.data = np.full(((100,1000,2)),-100)
        self.n = 0
        self.plot_size = 0

    def clear_canvas(self):
        #画面クリアボタン押下時呼び出し関数
        self.test_canvas.delete(tkinter.ALL)
        self.im = Image.new('RGB', (512, 512), 'white')
        self.draw = ImageDraw.Draw(self.im)
        self.data = np.full(((100,1000,2)),-100)
        self.plot_size=0
        self.n=0
        #print ("clear")

    def save_canvas(self):
        #セーブボタン押下時呼び出し関数
        
        #デバッグ用
        #self.test_canvas.postscript(file='out.ps', colormode='color')
        #self.data0=self.data[0:self.n,:,:] 
        #print(self.data0)
        #print("save")
        
        self.path_w = input('filename=> ')
        
        #配列を軽くしてからnumpy形式で保存
        self.data0=self.data[0:self.n,:,:]
        np.save(self.path_w, self.data0)
        
         #画像ファイルを保存(32x32に変換)
        filename = "temp.jpg"
        self.im1 = self.im.resize((512,512),Image.ANTIALIAS)
        self.im1.save(filename)
        
        print(self.data0)
        print ("write: ",self.path_w)

    def paint(self, event):
        #マウスクリック時呼び出し関数
        paint_color = 'black'
        if self.old_x and self.old_y:
            self.test_canvas.create_line(self.old_x, self.old_y, event.x, event.y, width=5.0, fill=paint_color, capstyle=tkinter.ROUND, smooth=tkinter.TRUE, splinesteps=36)
            self.draw.line((self.old_x, self.old_y, event.x, event.y), fill=paint_color, width=5)
            self.geo_label["text"] = "{" + str(event.x) + ","+ str(event.y) + "}"
            self.old_x_norm = int(self.old_x*100/512)
            self.old_y_norm = int(self.old_y*100/512)
            self.event_x_norm = int(event.x*100/512)
            self.event_y_norm = int(event.y*100/512)
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