# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 22:27:22 2021

Program to calculate Arknights DPS 
"""
import tkinter as tk
from tkinter import ttk
import numpy
#from PIL import Image, ImageTk

    
    
window = tk.Tk()
window.geometry('1600x700')
icon = tk.PhotoImage(master=window,file = "archet.png")
#window.rowconfigure([0,1], minsize=800, weight=1)
#window.columnconfigure([0,1,2], minsize=100, weight=1)
window.resizable(width= False, height= False)
window.title("Bable Calculation")
style = ttk.Style(window)


# Import the tcl file
window.tk.call('source', r'C:\\Users\\MSI\Desktop\\Arknights Babel Calc\\Azure-ttk-theme-main\\azure-dark.tcl')

# Set the theme with the theme_use method
style.theme_use('azure-dark')


""" this is the background image section 
background_lbl = tk.Label(window, image = icon)
background_lbl.place(x=0, y=0, relwidth=1, relheight=1)
background_lbl.grid(row=0,column=0)
"""
#storage varibles 

Button_limiter1 = 0 
Button_limiter2 = 0 
Button_limiter3 = 0  
Button_limiter4 = 0  
h = tk.BooleanVar()

Base_ATK_Buff = 0                   # Base Attack Buff
Sora_sk2 = tk.IntVar(value=0)
Sora_Buff = tk.IntVar(value=0)             # Sora Buff 
ATK_Multiplier_Buff = tk.IntVar(value=1)   # Attack Multiplier Buff
Base_Attack = tk.IntVar(value=1)           # Base Attack
Defence = tk.IntVar(value=0)               # Defence 
Physical_DMG_Taken = tk.IntVar(value=1)    # Physical DMG Taken 
Flat_Def_Down = tk.IntVar(value=0)
Scaling_Def_Down = tk.IntVar(value=1)


#Math is nesting here :

def ATK_M():
    global ATK_Multiplier_Buff
    m = []
    for entries in MBuffs_Lst:
       if entries.get().isdigit():
                m.append(int(entries.get()))
                
       else:
             print("Error: not a number")
    
    newm = [x / 100 for x in m]         #(x/100)
    ATK_Multiplier_Buff = numpy.prod(newm)  #(X1)*(X2)*(X3)*(Xn)
    print(m,newm)
    print("ATK Multiplier: ", ATK_Multiplier_Buff)        

def Sorask2():
    global Sora_sk2
    global ent_Sora_ATK
    global Sora_Buff
    s = []
    if ent_Sora_ATK.get().isdigit():
        s.append(int(ent_Sora_ATK.get()))
    else:
        print("Sora attack is not a number")
    Sora_Buff = int(s[0])*Sora_sk2.get() / 100
    
    


def OP_ATK():
    global Base_Attack
    global Defence
    if ent_Base_Attack.get().isdigit():
        Base_Attack = int(ent_Base_Attack.get())
    else:
            print("Base Attack is not a number")
    if ent_Defence.get().isdigit():
        Defence = int(ent_Defence.get())
    else:
        print("Defence is not a number")
   

def Phy_DMG_Taken():
    global Physical_DMG_Taken
    p =[]
    
    if ent_phs_tkn1.get().isdigit():
            p.append(int(ent_phs_tkn1.get()))
    if ent_phs_tkn2.get().isdigit():
            p.append(int(ent_phs_tkn2.get()))
    if ent_phs_tkn3.get().isdigit():
            p.append(int(ent_phs_tkn3.get()))  
    else:
        print("No Pyhsical dmg")
    newP = [ 1+x/100 for x in p]   
    Physical_DMG_Taken = numpy.prod(newP)
    
    

def Flat_Debuff():
    global Flat_Def_Down
    f = []
    for entries in Flat_Debuffs_Lst:
        if entries.get().isdigit():
            f.append(int(entries.get()))
        else:
            print("Flat debuff is not a number")
    Flat_Def_Down = sum(f)*-1
    print('list of flat debuff', f)
    

def Perc_Debuff():
    global Scaling_Def_Down
    s = []
    for entries in Perc_Debuffs_Lst:
        if entries.get().isdigit():
            s.append(int(entries.get()))
        else:
            print("Perc debuff is not a number")
    newS= [1-x/100 for x in s]
    Scaling_Def_Down = 1 - numpy.prod(newS)
    print("List of percentage debuffs ", newS)
    



def Final_Attack():
    OP_ATK()
    Sorask2()
    ATK_M()
    BaseATK_Buff()
    global Base_Attack, Sora_Buff, ATK_Multiplier_Buff, Base_ATK_Buff
    a = ((Base_Attack*(1+Base_ATK_Buff))+Sora_Buff)*ATK_Multiplier_Buff
    
    return a

def Physical_DMG_Formula():
    Flat_Debuff()
    Perc_Debuff()
    Phy_DMG_Taken()
    OP_ATK()
    global Defence, Flat_Def_Down, Physical_DMG_Taken, Scaling_Def_Down
   
    D = (Defence + Flat_Def_Down)
    if D<0:
        D=0
    result = (Final_Attack() - (D)*(1- Scaling_Def_Down))*Physical_DMG_Taken
    print("-"*30)
    print("D is ", D)
    print("Base Attack :",Base_Attack)
    print("Defence : ",Defence)
    print("Sora sk2 ", Sora_sk2.get())
    print("Sora Buff: ",Sora_Buff)
    print("Scaling def :", Scaling_Def_Down)
    print("Flat Def Down :", Flat_Def_Down)
    print("Phys DMG Take : ", Physical_DMG_Taken)
    print("Defence: ", Defence)
    print("Final Attack: ", Final_Attack())
    
    print("The result is : ",result)
    M = 0.05*Final_Attack()
    if result <= 0:
        result = M
        lbl_result.config(background="red",text="Total Physical DMG (minimum):")
    else:
        lbl_result.config(background="green")
    lbl_Base_Attack1.config(text=f'Base ATK Buff: {Base_ATK_Buff:.3f} ')
    lbl_ATKM_Buff.config(text=f'Multiplicative ATK Buff: {ATK_Multiplier_Buff:.3f} ')
    lbl_Def_FlatDebuff.config(text=f'Flat Defence Debuff: {Flat_Def_Down} ')
    lbl_Def_Scal.config(text=f'Scaling Defence Debuff: {Scaling_Def_Down:.3f} ')
    lbl_Sora.config(text=f'Sora SK2 Buff: {Sora_Buff:.3f} ')
    lbl_Final_ATK.config(text=f'Final Attack: {Final_Attack():.3f} ')
    ent_result.config(state='enabled')
    ent_result.delete(0,"end")
    ent_result.insert(0,f"{result:.3f}")
    ent_result.config(state='disabled')
    











#Stats section frame <------------------------------------------------------->
frm_Stats = ttk.LabelFrame(master=window, text='Stats', width=110, height=100)
frm_Stats.place(x=10, y=10)

    
#Base Attack
lbl_Base_Attack = ttk.Label(frm_Stats,text= "Opereator Attack: ")
ent_Base_Attack = ttk.Entry(frm_Stats)
lbl_Base_Attack.grid(row=0, column=0, padx=10, pady=10)
ent_Base_Attack.grid(row=0, column=1, padx=5, pady=10)

#Defence 
lbl_Defence = ttk.Label(frm_Stats, text= "Enemy Defence: ")
ent_Defence = ttk.Entry(frm_Stats)
lbl_Defence.grid(row=1, column=0, padx=10, pady=10)
ent_Defence.grid(row=1, column=1, padx=10, pady=10)
ent_Defence.insert(0,'0')

#Phy dmg taken
lbl_phs_tkn = ttk.Label(frm_Stats, text='Physical DMG Taken ')
ent_phs_tkn1 = ttk.Entry(frm_Stats)
ent_phs_tkn2 = ttk.Entry(frm_Stats)
ent_phs_tkn3 = ttk.Entry(frm_Stats)

lbl_phs_tkn.grid(row=3, column=0, padx=10, pady=10)
ent_phs_tkn1.grid(row=3, column=1, padx=10, pady=10)
ent_phs_tkn2.grid(row=4, column=1, padx=10, pady=10)
ent_phs_tkn3.grid(row=5, column=1, padx=10, pady=10)

#Buffs section frame <------------------------------------------->


List_buffs = [] #store all the buffs here 
        
def add_buff():
    print("Buff added")
    global Button_limiter1
    next_row = len(Additive_buffs)
    lab = ttk.Label(frm_Buffs, text=f"Additive Buff {next_row+1}")
    lab.grid(row=next_row+1, column=0, padx=5, pady=10)
    
    ent_buffs = ttk.Entry(frm_Buffs)
    ent_buffs.grid(row=next_row+1, column=1, padx=5, pady=10)
    Additive_buffs.append(ent_buffs)
    if Button_limiter1 < 5:
        Button_limiter1 = Button_limiter1 + 1
    else:
        btn_more_buffs.configure(state='disabled')
            
def BaseATK_Buff():
    global Base_ATK_Buff 
    v = []
    for entries in Additive_buffs:
        if entries.get().isdigit():
            v.append(int(entries.get()))   
        else:
             print("Error: not a number")
    Base_ATK_Buff = sum(v)/100
    print(v)
    print("Base ATK Buff: ",Base_ATK_Buff)
     

Additive_buffs = []  #list for additive buffs enterd  
frm_Buffs = ttk.Labelframe(master=window, text='Buffs - Additive Attack Buff', width=300, height=490)
frm_Buffs.place(x=310, y=10)


btn_more_buffs = ttk.Button(frm_Buffs, text="Add buff",command=add_buff)
btn_more_buffs.grid(row=0, column=0, sticky="n", padx=10, pady=20)


separator = ttk.Separator(frm_Stats,orient=tk.HORIZONTAL)
separator.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

#DeBuffs section frame <--------------------------------------------->
def add_debuff():
    print("deBuff added")
    global Button_limiter2
    next_row = len(Flat_Debuffs_Lst)
    lab = ttk.Label(frm_DeBuffs, text=f"Flat Defence deBuff {next_row+1}")
    lab.grid(row=next_row+1, column=0, padx=5, pady=10)
    
    ent_debuffs = ttk.Entry(frm_DeBuffs)
    ent_debuffs.grid(row=next_row+1, column=1, padx=5, pady=10)
    Flat_Debuffs_Lst.append(ent_debuffs)
    if Button_limiter2 < 5:
        Button_limiter2 = Button_limiter2 + 1
    else:
        btn_more_debuff.configure(state='disabled')
        
        
def add_debuffp():
    print("deBuff added")
    global Button_limiter3
    next_row = len(Perc_Debuffs_Lst)
    lab = ttk.Label(frm_DeBuffs, text=f"Percentage Defence deBuff {next_row+1}")
    lab.grid(row=next_row+1, column=2, padx=5, pady=10)
    
    ent_debuffsp = ttk.Entry(frm_DeBuffs)
    ent_debuffsp.grid(row=next_row+1, column=3, padx=5, pady=10)
    Perc_Debuffs_Lst.append(ent_debuffsp)
    if Button_limiter3 < 5:
        Button_limiter3 = Button_limiter3 + 1
    else:
        btn_more_debuffp.configure(state='disabled')        
     
Flat_Debuffs_Lst =[]     
Perc_Debuffs_Lst =[]   
frm_DeBuffs = ttk.Labelframe(master=window, text='Debuffs', width=680, height=370)
frm_DeBuffs.place(x=580,y=10)



btn_more_debuff = ttk.Button(frm_DeBuffs, text='Add Flat Defence Debuff',command=add_debuff)
btn_more_debuff.grid(row=0, column=0, padx=10, pady=10)

btn_more_debuffp = ttk.Button(frm_DeBuffs, text='Add Percentage Defence Debuff', command=add_debuffp)
btn_more_debuffp.grid(row=0, column=2, padx=10, pady=10)

#Sora Frame <------------------------------------------------------------>
frm_Sora = ttk.Labelframe(master=window, text='Sora Spectial Section ! ', width=440, height=120)
frm_Sora.place(x=10, y=420)

#Sora attack
lbl_Sora_ATK = ttk.Label(frm_Sora, text='Sora Attack : ')
ent_Sora_ATK = ttk.Entry(frm_Sora)
lbl_Sora_ATK.grid(row=0, column=0, padx=10, pady=20)
ent_Sora_ATK.grid(row=0, column=1, padx=10)
ent_Sora_ATK.insert(0,'0')

#Sora sk2 lvl 
lbl_Sora_sk2 = ttk.Label(frm_Sora, text='Sorra skill 2 buff % :')
rad1 = ttk.Radiobutton(frm_Sora, text='70%', variable=Sora_sk2, value=70)
rad2 = ttk.Radiobutton(frm_Sora, text='80%', variable=Sora_sk2, value=80)
rad3 = ttk.Radiobutton(frm_Sora, text='90%', variable=Sora_sk2, value=90)
rad4 = ttk.Radiobutton(frm_Sora, text='100%', variable=Sora_sk2, value=100)

lbl_Sora_sk2.grid(row=1, column=0, padx=10,)
rad1.grid(row=2, column=0, padx=10,)
rad2.grid(row=2, column=1, padx=10,)
rad3.grid(row=2, column=2, padx=10,)
rad4.grid(row=2, column=3, padx=10,)

#Attack Multiplier buff <----------------------------------------------------->
def add_Mbuff():
    print("M Buff added")
    global Button_limiter4
    next_row = len(MBuffs_Lst)
    next_col = len(MBuffs_Lst)
    lab = ttk.Label(frm_MBuffs, text=f"Attack Multiplier Buff {next_row+1}")
    lab.grid(row=1, column=next_col+1, padx=5, pady=10)
    
    ent_Mbuffs = ttk.Entry(frm_MBuffs)
    ent_Mbuffs.grid(row=0, column=next_col+1, padx=5, pady=10)
    MBuffs_Lst.append(ent_Mbuffs)
    if Button_limiter4 < 5:
        Button_limiter4 = Button_limiter4 + 1
    else:
        btn_atk_multi.configure(state='disabled') 
        






    
        
#Multiplire buff Frame



MBuffs_Lst =[]        
frm_MBuffs = ttk.Labelframe(master=window, text='Attack Multiplier Buff', width=1020, height=100)
frm_MBuffs.place(x=470, y=420)


btn_atk_multi = ttk.Button(frm_MBuffs, text='Add Multiplier Buff', command=add_Mbuff)
btn_atk_multi.grid(row=0,column=0, padx=10, pady=10)




# Notebook
notebook = ttk.Notebook(window)
#im = Image.open('C:\\Users\MSI\Desktop\Arknights Babel Calc\Patriot_sprite.png')
#Patriot_img = ImageTk.PhotoImage(im)
# Tab 1
notebookTab1 = ttk.Frame(notebook, width=318, height=382)
notebook.add(notebookTab1, text='🛈Tab 1',)
lbl_Tab1 = ttk.Label(notebookTab1,
                     text="General Instruction : \n① The program will ONLY accept integer numbers  Examples for non-acceptable entries :\n float '20.5'; letters '20t'; Space '  40' nor '40  ' \n\n② Don't use ' % nor -' \n\n③ Don't enter a decimal number  \n\n④ If you are using not using Sora just Disable it using the swtich \n\n⑤ Operator Attack is already added with (Trust ATK)   ",
                     wraplength=318,font=("Arial", 16), compound=tk.TOP)





lbl_Tab1.pack()
# Tab 2
notebookTab2 = ttk.Frame(notebook, width=318, height=382)
notebook.add(notebookTab2, text='Tab 2')
lbl_Tab2 = ttk.Label(notebookTab2,
                     text="➵Buffs - Additive Attack Buff Frame:\n\nHere you enter the Additive Buffs `basiclly buff with plus sign` (+⚔%ATK)\nExample : Warfrain s2 and Exusiai Talent.\n \n➵Attack Multiplier Buff Frame:\nMultiplicative buffs are WITH-OUT plus sign (ATK⚔%) Example: Schwarz s1 and Blemishine s1. ",
                     wraplength=320,font=("Arial", 16), compound=tk.TOP)
lbl_Tab2.pack()
# Tab 3
notebookTab3 = ttk.Frame(notebook, width=318, height=382)
notebook.add(notebookTab3, text='Tab 3')
lbl_Tab3 = ttk.Label(notebookTab3,
                     text="⩺Debuffs Frame:\n ⤿Flat Defence Debuff is any debuff with flat number (not %) Example ( -🛡 DEF): Ifrit s2 and Meteorite s2.\n\n⤿Percentage Defence Debuff is any debuff with percentage (-🛡% DEF) Example: Pramanix s2 and Schwarz Talent.",
                     wraplength=320,font=("Arial", 16), compound=tk.TOP)


lbl_Tab3.pack()
notebook.place(x=1270, y=10)

#Frame for the results : <.......................................................................>

frm_result = ttk.LabelFrame(master=window, text="The Results - Damage for physical attackers", width=660, height=111)
frm_result.place(x=470, y=530)

btn_clc = ttk.Button(frm_result, text="Calculate",style='AccentButton',command=Physical_DMG_Formula) #the test button to store all Entries into the list
btn_clc.grid(row=0, column=0, padx=20, pady=20)



lbl_result = ttk.Label(frm_result, text="Total Physical DMG :")
ent_result = ttk.Entry(frm_result,state='disabled')
lbl_result.grid(row=1, column=0, padx=5, pady=5)
ent_result.grid(row=1, column=1, padx=10, pady=10)

separator1 = ttk.Separator(frm_result,orient='vertical')
separator1.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky="ns")


lbl_Base_Attack1 = ttk.Label(frm_result, text="Base ATK Buff: --- ")
lbl_Base_Attack1.grid(row=0, column=3, padx=5, pady=10)

lbl_ATKM_Buff = ttk.Label(frm_result, text="Multiplicative ATK Buff: --- ")
lbl_ATKM_Buff.grid(row=1, column=3, padx=5, pady=10)

separator2 = ttk.Separator(frm_result,orient='vertical')
separator2.grid(row=0, column=4, rowspan=2, padx=10, pady=10, sticky="ns")

lbl_Def_FlatDebuff = ttk.Label(frm_result, text="Flat Defence Debuff: --- ")
lbl_Def_FlatDebuff.grid(row=0, column=5, padx=5, pady=10)

lbl_Def_Scal = ttk.Label(frm_result, text="Scaling Defence Debuff: --- ")
lbl_Def_Scal.grid(row=1, column=5, padx=5, pady=10)

separator3 = ttk.Separator(frm_result,orient='vertical')
separator3.grid(row=0, column=6, rowspan=2, padx=10, pady=10, sticky="ns")

lbl_Sora = ttk.Label(frm_result, text='Sora SK2 Buff: --- ')
lbl_Sora.grid(row=0, column=7, padx=5, pady=10)

lbl_Final_ATK = ttk.Label(frm_result, text='Final Attack: --- ')
lbl_Final_ATK.grid(row=1, column=7, padx=5, pady=10)


# Switch
switch = ttk.Checkbutton(frm_Sora , text='ON', style='Switch', variable=h)
switch.grid(row=0, column=2)
switch.invoke()

# Function for configure the Switch's text when switched
def switchFunction():
    if h.get():
        switch.config(text='ON')
        ent_Sora_ATK.config(state='enabled')
    else:
        switch.config(text='OFF')
        ent_Sora_ATK.delete(0,"end")
        ent_Sora_ATK.insert(0,'0')
        ent_Sora_ATK.config(state='disabled')
       
switch.config(command=switchFunction)

window.mainloop()
