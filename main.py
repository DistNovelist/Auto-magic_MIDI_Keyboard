import pygame.midi as m
import time
import keyboard as key
import threading
from tkinter import *
import tkinter.ttk as ttk
import os
import math
import copy
notename = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
noteoct = ["-1","0","1","2","3","4","5","6","7"]
keynum2midinum = [0, 2, 4, 5, 7, 9, 11]
scales =  {"Major":[0, 2, 4, 5, 7, 9, 11], 
"Natural Minor":[0, 2, 3, 5, 7, 8, 10], 
"All Notes":[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 
"Harmonic Minor":[0, 2, 3, 5, 7, 8, 11], 
"Melodic Minor":[0, 2, 3, 5, 7, 9, 11], 
"Major Penta Tonic(ヨナ抜き長音階)":[0, 2, 4, 7, 9],
"Major Blues":[0, 2, 3, 4, 7, 9]}
scaleNames=["Major", "Natural Minor", "All Notes", "Custom", "Harmonic Minor", "Melodic Minor", "Major Penta Tonic(ヨナ抜き長音階)", "Major Blues"]
pressedMidiKey=[]
keyprocEndFlag = False
midiOutChangeFlag = False
velocity = 100
baseNote = 60
c=None
black_keys = (1,3,6,8,10)
customizeMode=False

def keypress(n,deltaOct):
    global velocity
    global baseNote
    if len(keynum2midinum)>0:
        midikeypress(keynum2midinum[n]+12*deltaOct+baseNote, velocity)

def keyrelease(n,deltaOct):
    global baseNote
    if len(keynum2midinum)>0:
        midikeyrelease(keynum2midinum[n]+12*deltaOct+baseNote)

def keyprocess():
    global keyprocEndFlag
    global midiOutChangeFlag
    global midiout
    global keynum2midinum
    key_list1 = ["z","x","c","v","b","n","m",",",".","/","_"]
    key_list2 = ["a","s","d","f","g","h","j","k","l",";",":","]"]
    key_list3 = ["q","w","e","r","t","y","u","i","o","p","@","["]
    global pressedMidiKey
    pressedMidiKey = []
    for k in key_list1:
        key.on_press_key(k, lambda c: keypress(key_list1.index(c.name)%len(keynum2midinum), key_list1.index(c.name)//len(keynum2midinum)) if len(keynum2midinum) > 0 else None)
        key.on_release_key(k, lambda c: keyrelease(key_list1.index(c.name)%len(keynum2midinum), key_list1.index(c.name)//len(keynum2midinum)) if len(keynum2midinum) > 0 else None)
    for k in key_list2:
        key.on_press_key(k, lambda c: keypress(key_list2.index(c.name)%len(keynum2midinum), key_list2.index(c.name)//len(keynum2midinum)+1) if len(keynum2midinum) > 0 else None)
        key.on_release_key(k, lambda c: keyrelease(key_list2.index(c.name)%len(keynum2midinum), key_list2.index(c.name)//len(keynum2midinum)+1) if len(keynum2midinum) > 0 else None)
    for k in key_list3:
        key.on_press_key(k, lambda c: keypress(key_list3.index(c.name)%len(keynum2midinum), key_list3.index(c.name)//len(keynum2midinum)+2) if len(keynum2midinum) > 0 else None)
        key.on_release_key(k, lambda c: keyrelease(key_list3.index(c.name)%len(keynum2midinum), key_list3.index(c.name)//len(keynum2midinum)+2) if len(keynum2midinum) > 0 else None)
    while keyprocEndFlag == False:
        if midiOutChangeFlag and m.get_init() == False:
            global midioutID
            m.init()
            while m.get_init() == False and keyprocEndFlag == False:
                time.sleep(0.2)
                print("m.get_init():"+str(m.get_init()))
            midiout = None
            midiout = m.Output(midioutID)
            midiOutChangeFlag = False
            print(midiout)
        
            
    

def midikeypress(i,vel):
    global pressedMidiKey
    if (i in pressedMidiKey) == False and midiOutChangeFlag == False:
        global midiout
        midiout.note_on(i, vel)
        pressedMidiKey.append(i)
        if i - (baseNote//12)*12< 37 and i - (baseNote//12)*12> -1:
            global c
            global black_keys
            if i == baseNote+12:
                c.itemconfig(str(13+baseNote%12), fill=COLOR_TABLE[7])
            elif i % 12 in black_keys:
                c.itemconfig(str(i - (baseNote//12)*12+1),fill=COLOR_TABLE[5])
            else:
                c.itemconfig(str(i - (baseNote//12)*12+1),fill=COLOR_TABLE[4])


def midikeyrelease(i):
    global pressedMidiKey
    if i in pressedMidiKey and midiOutChangeFlag == False:
        global midiout
        midiout.note_off(i)
        pressedMidiKey.remove(i)
        if i - (baseNote//12)*12< 37 and i - (baseNote//12)*12> -1:
            global c
            global black_keys
            if i == baseNote+12:
                c.itemconfig(str(13+baseNote%12), fill=COLOR_TABLE[6])
            elif i % 12 in black_keys:
                c.itemconfig(str(i - (baseNote//12)*12+1),fill=COLOR_TABLE[3])
            else:
                c.itemconfig(str(i - (baseNote//12)*12+1),fill=COLOR_TABLE[2])

def allMidiKeyRelease():
    global pressedMidiKey
    i_num = m.get_count()
    for i in pressedMidiKey:
        midikeyrelease(i)

def changeMidiOutPort(portNum):
    i_num = m.get_count()
    for i in range(i_num):
        #print(i)
        #print(m.get_device_info(i))
        print(m.get_device_info(i))
    print("out→ "+str(portNum))
    global midiout
    global midioutID
    global midiOutChangeFlag
    global pressedMidiKey
    for i in pressedMidiKey:
        midikeyrelease(i)
    midiout.close()
    m.quit()
    midioutID = portNum
    midiOutChangeFlag = True

def setKeyOutline():
    global keynum2midinum
    global c
    global baseNote
    for i in range(1,37):
        if (i-baseNote-1)%12 in keynum2midinum:
            c.itemconfig(str(i), width=2, outline="red")
        else:
            c.itemconfig(str(i), width=0)
        if i == 13 + baseNote % 12:
            c.itemconfig(str(i), fill=COLOR_TABLE[6])
        elif (i-1) % 12 in black_keys:
            c.itemconfig(str(i),fill=COLOR_TABLE[3])
        else:
            c.itemconfig(str(i),fill=COLOR_TABLE[2])

COLOR_TABLE = ("light gray","gray","white","gray15","gray80","gray40","light salmon","brown")
midiout = None
midioutID = None
midi_devices = []
midi_inputdevices = []
midi_outputdevices = []
def main():
    global COLOR_TABLE
    global midi_devices
    global midi_inputdevices
    global midi_outputdevices
    print("Auto-magic MIDI Keyboard v0.1 by DIST_NOVELIST")
    # 実行UID(EUID)とUIDを確認し、
    # "0"(root)であれば管理者権限を持つ。
    if os.geteuid() == 0 and os.getuid() == 0 :
        print("管理者権限を持っています。")
    else:
        print("このスクリプトの実行には、管理者権限が必要です。")
    m.init()
    print(str(m.get_default_output_id())+"/input:"+str(m.get_default_input_id()))
    i_num = m.get_count()
    for i in range(i_num):
        #print(i)
        print(m.get_device_info(i))
        midi_devices.append(m.get_device_info(i)[1].decode()+"(input)"*m.get_device_info(i)[2]+"(output)"*m.get_device_info(i)[3])
        if m.get_device_info(i)[2]==1:
            midi_inputdevices.append(m.get_device_info(i)[1].decode()+"(input)")
        if m.get_device_info(i)[3]==1:
            midi_outputdevices.append(m.get_device_info(i)[1].decode()+"(output)")

    """input_id = m.get_default_input_id()
    print("input MIDI:%d" % input_id)
    i = m.Input(input_id)
    print ("starting")
    print ("full midi_events:[[[status,data1,data2,data3],timestamp],...]")

    going = True
    count = 0
    while going:
        if i.poll():
            midi_events = i.read(10)
            print ("full midi_events:" + str(midi_events) + ", note:" + notename[midi_events[0][0][1]%12] + str(midi_events[0][0][1]//12-2))
            count += 1
        if count >= 14:
            going = False"""
    #i.close()

    global midiout
    global midioutID
    midiout = m.Output(m.get_default_output_id())
    midioutID = m.get_default_output_id()
    keyTh = threading.Thread(target=keyprocess)
    keyTh.setDaemon(True)
    keyTh.start()

    #tkinter
    tk = Tk()
    tk.geometry("723x200")
    tk.resizable(width=0,height=0)
    tk.title("Auto-magic MIDI Keyboard")
    tk.lift()
    tk.configure(bg=COLOR_TABLE[0])

    frame = ttk.Frame(tk)
    frame.grid()

    global c
    c = Canvas(frame,width=723,height=50)
    c.configure(bg=COLOR_TABLE[1], highlightthickness=0)
    c.grid(columnspan=6,row=0,column=0)

    pressing_key = 0
    def click(event):
        clicked = [
            obj for obj in c.find_overlapping(event.x-1, event.y+1,event.x+1,event.y-1)
        ]
        print(clicked)
        global pressing_key
        global velocity
        if clicked:
            pressing_key = int(c.gettags(clicked[0])[0])+baseNote//12*12
            midikeypress(pressing_key,velocity)
            if customizeMode:
                global keynum2midinum
                if (int(c.gettags(clicked[0])[0])-baseNote)%12 in keynum2midinum:
                    keynum2midinum.remove((int(c.gettags(clicked[0])[0])-baseNote)%12)
                else:
                    keynum2midinum.append((int(c.gettags(clicked[0])[0])-baseNote)%12)
                    keynum2midinum.sort()
                setKeyOutline()

                    
            return
    def release(event):
        global pressing_key
        if pressing_key:
            midikeyrelease(pressing_key)
            pressing_key = 0

    global baseNote

    global black_keys
    for i in range(36):
        if i%12 in black_keys:
            k = c.create_rectangle(i*20+4,48,i*20+22,0, outline="", fill=COLOR_TABLE[3],tag=str(i))
        else:
            k = c.create_rectangle(i*20+4,48,i*20+22,0, outline="",fill=COLOR_TABLE[2],tag=str(i))
        #print(k)
        #print(c.gettags(k))
    c.bind('<Button-1>',click)
    c.bind('<ButtonRelease-1>',release)

    label1 = ttk.Label(frame, text="Output MIDI Port:")
    label1.grid(row=1,column=0)
    cb_v=StringVar()
    cb = ttk.Combobox(frame, textvariable=cb_v, values=midi_outputdevices, width=30, state="readonly")
    cb.set(midi_outputdevices[0])
    cb.bind('<<ComboboxSelected>>', lambda e: changeMidiOutPort(midi_devices.index(cb_v.get())))
    cb.grid(row=1, column=1, columnspan=2)

    label2 = ttk.Label(frame, text="Velocity:")
    label2.grid(row=1,column=3)

    global velocity
    velText = StringVar()
    label3 = ttk.Label(frame,textvariable=velText)
    velText.set(str(velocity))
    def SetVel(v):
        global velocity
        velocity = math.floor(float(v))
        velText.set(str(velocity))

    vels = ttk.Scale(frame,variable=velocity,value=velocity,orient=HORIZONTAL,length=127,from_=0,to=127,command=lambda v: SetVel(v))
    vels.grid(row=1, column=4)
    label3.grid(row=1,column=5)
    
    label4 = ttk.Label(frame, text="Base Note:")
    label4.grid(row=2,column=0)
    cbBN1_v=StringVar()
    cbBN1 = ttk.Combobox(frame, textvariable=cbBN1_v, values=notename, width=5, state="readonly")
    cbBN1.set(notename[0])
    cbBN2_v=StringVar()
    cbBN2 = ttk.Combobox(frame, textvariable=cbBN2_v, values=noteoct, width=5, state="readonly")
    cbBN2.set(noteoct[5])
    def setBN():
        allMidiKeyRelease()
        global baseNote
        baseNote = notename.index(cbBN1.get()) + 12*(int(cbBN2.get())+1)
        setKeyOutline()
    cbBN1.bind('<<ComboboxSelected>>', lambda e: setBN())
    cbBN2.bind('<<ComboboxSelected>>', lambda e: setBN())
    cbBN1.grid(row=2, column=1)
    cbBN2.grid(row=2, column=2)
    label5 = ttk.Label(frame, text="Scale:")
    label5.grid(row=2,column=3)
    global scaleNames
    cbSc_v=StringVar()
    cbSc = ttk.Combobox(frame, textvariable=cbSc_v, values=scaleNames, width=30, state="readonly")
    cbSc.set(scaleNames[0])
    def changeScale(scalename):
        allMidiKeyRelease()
        global keynum2midinum
        global customizeMode
        if scalename == "Custom":
            customizeMode = True
        else:
            customizeMode = False
            keynum2midinum = copy.copy(scales[scalename])
        setKeyOutline()
    changeScale(cbSc_v.get())
    cbSc.bind('<<ComboboxSelected>>', lambda e: changeScale(cbSc_v.get()))
    cbSc.grid(row=2, column=4,columnspan=2)



    
    #tkinterメインループ
    tk.mainloop()
    global keyprocEndFlag
    keyprocEndFlag=True
    keyTh.join()
    print("quit")
    midiout.close()
    m.quit()
    exit()

if __name__=="__main__":
    main()