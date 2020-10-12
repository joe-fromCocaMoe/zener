from tkinter import Canvas,Frame,Button,Label,Tk,IntVar
from random import shuffle, random, choice
from tkinter.messagebox import *
from tkinter.simpledialog import askstring
import logging, sys
from time import time,sleep
from PIL.ImageTk import PhotoImage, Image
from functools import partial
logging.basicConfig(level= logging.DEBUG)
#logging.disable(logging.CRITICAL)

class Zener_Test(Frame):
    def __init__(self, parent=None):
        self.parent= parent
        Frame.__init__(self, self.parent)
        self.pack(expand='yes', fill='both')
        self.canvas= Canvas(self)
        self.canvas.config(width= 1000, height= 880, bg='skyblue')
        self.canvas.pack(expand='yes', fill='both')
        self.btn= Button(self.canvas, text='start', command= self.get_entry)
        self.btn.place(x=800,y=60)
        self.bind_all('<Key>', self.key)
        self.zener_deck_base= ['Yellow Circle','Red Plus','Blue Waves',
                               'Black Square','Green Star']
        self.zener_pics= ['Yellow_Circle.png','Red_Plus.png',
                          'Blue_Waves.png','Black_Square.png',
                          'Green_Star.png']
        self.photo_path= 'zener/'
        self.image_ref= []
        self.image_ref2= []
        self.zener_buttons= []
        self.my_font=('arial',26,'bold')
        self.circle_count= IntVar(value=0)
        self.circle_lbl= Label(self.canvas, textvariable=self.circle_count,
                               font= self.my_font, bg='skyblue')
        self.circle_lbl.place(x=100,y=240)
        self.plus_count= IntVar(value=0)
        self.plus_lbl= Label(self.canvas, textvariable=self.plus_count,
                             font=self.my_font, bg='skyblue')
        self.plus_lbl.place(x=230,y=240)
        self.wave_count= IntVar(value=0)
        self.wave_lbl= Label(self.canvas, textvariable=self.wave_count,
                             font=self.my_font, bg='skyblue')
        self.wave_lbl.place(x=370,y=240)
        self.square_count= IntVar(value=0)
        self.square_lbl= Label(self.canvas, textvariable=self.square_count,
                               font=self.my_font, bg='skyblue')
        self.square_lbl.place(x=500,y=240)
        self.star_count= IntVar(value=0)
        self.star_lbl= Label(self.canvas, textvariable=self.star_count,
                             font=self.my_font, bg='skyblue')
        self.star_lbl.place(x=630,y=240)
        img= Image.open('zener/blank_card.png')
        image_= PhotoImage(img)
        self.guess_card= Label(self.canvas, image=image_,
                               width=360,height=600,bg='skyblue')
        self.guess_card.place(x=300,y=280)
        self.image_ref2.append(image_)
        self.card_count= IntVar(value=25)
        self.cards_left= Label(self.canvas, textvariable=self.card_count,
                               font=self.my_font,bg='skyblue')
        self.cards_left.place(x=140,y=600)
        self.deck= self.zener_deck_base * 5
        self.current_card= 0
        self.win= 0
        self.loss= 0
        self.outcome_answer= {}
        self.g_count=0
    def make_deck(self):
        shuffle(self.deck)
        front= self.deck[:12]
        back= self.deck[12:]
        shuffle(front)
        shuffle(back)
        final_deck= front + back
        return final_deck
        
    def key(self, event):
        self.g_count +=1
        message= 'count:{0} key:{1} num:{2} state:{3}'.format(self.g_count,
                                                 event.keysym,event.keysym_num,
                                       event.state)
        logging.debug(message)
    def make_card_buttons(self):
        x2= 50
        y2= 40
        img_dir= self.photo_path
        for pic in self.zener_pics:
            img_obj= Image.open( img_dir + pic)
            image= PhotoImage(img_obj)
            self.zener_buttons.append(Button(self.canvas, image= image,
                                             width=120,height=180,bg='skyblue',
                                      command= partial(self.check_guess, pic)))
            self.zener_buttons[-1].place(x=x2,y=y2)
            x2+=130
            self.image_ref.append(image)
    def compare_card(self,btn_str, card_):
        if btn_str == card_:
            self.win +=1
            self.current_card +=1            
            val_= self.card_count.get()
            val_ -=1
            self.card_count.set(val_)
            win= {val_:('yes',card_,None)}
            self.outcome_answer.update(win)
        else:
            self.loss +=1
            self.current_card +=1            
            val_= self.card_count.get()
            val_ -=1
            self.card_count.set(val_)            
            loss= {val_:('no',card_,btn_str)}
            self.outcome_answer.update(loss)
        if val_ == 0:
            
            self.guess_card.place_forget()
            self.cards_left.place_forget()
            txt_win_loss= 'Correct: {} Wrong: {}'.format(self.win, self.loss)
            percentage= 'Percentage correct: {:.2%}'.format(self.win/25)
            self.canvas.create_text(400,600,text=txt_win_loss,
                                    font=self.my_font, tag='end_game')
            self.canvas.create_text(400,670,text=percentage,
                                    font=self.my_font,tag='end_game')
            self.print_result()
    def print_result(self):
        print("key y/n actual your guess")
        for key in self.outcome_answer:
            val= self.outcome_answer[key]
            if val[0] == 'yes':
                print(key,val[0],val[1])
            else:
                print(key,val[0], val[1],val[2])
        
    def check_guess(self, picname):
        pn= picname.strip('.png')
        p_n= pn.replace('_',' ')        
        guess_card= self.working_deck[self.current_card]        
        if pn == 'Yellow_Circle':
            val=self.circle_count.get()
            val +=1
            self.circle_count.set(val)
                  
            if val == 5:
                self.zener_buttons[0].config(state='disabled')
            self.compare_card(p_n,guess_card)                  
            
        elif pn == 'Red_Plus':
            val= self.plus_count.get()
            val +=1
            self.plus_count.set(val)
            if val == 5:
                self.zener_buttons[1].config(state='disabled')
            self.compare_card(p_n,guess_card)  
            
        elif pn == 'Blue_Waves':
            val= self.wave_count.get()
            val +=1
            self.wave_count.set(val)
            if val == 5:
                self.zener_buttons[2].config(state='disabled')
            self.compare_card(p_n,guess_card)  
            
        elif pn == 'Black_Square':
            val= self.square_count.get()
            val +=1
            self.square_count.set(val)
            if val == 5:
                self.zener_buttons[3].config(state='disabled')
            self.compare_card(p_n,guess_card)  
            
        elif pn == 'Green_Star':
            val= self.star_count.get()
            val +=1
            self.star_count.set(val)
            if val == 5:
                self.zener_buttons[4].config(state='disabled')
            self.compare_card(p_n,guess_card)  
           
    def get_entry(self):
        self.btn.config(state='disabled')
        self.working_deck= self.make_deck()
        self.make_card_buttons()
        
if __name__ == '__main__':
    root= Tk()
    Zener_Test(root)
    root.mainloop()
