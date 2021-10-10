import pygame.midi as m
import time
import keyboard as key
import threading
import tkinter
import tkinter.ttk as ttk
import os
notename = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
keynum2midinum = [0, 2, 4, 5, 7, 9, 11]
pressedMidiKey=[]
keyprocEndFlag = False
velocity = 100

def keypress(n,deltaOct):
    global velocity
    midikeypress(keynum2midinum[n]+12*deltaOct+60, velocity)
    """global pressedMidiKey
    global keynum2midinum
    note_n = keynum2midinum[n]+12*deltaOct+60
    if (note_n in pressedMidiKey) == False:
        global velocity
        midikeyrelease(note_n)
        midikeypress(note_n, velocity)
        pressedMidiKey.append(note_n)"""
def keyrelease(n,deltaOct):
    midikeyrelease(keynum2midinum[n]+12*deltaOct+60)
    """global pressedMidiKey
    global keynum2midinum
    note_n = keynum2midinum[n]+12*deltaOct+60
    if note_n in pressedMidiKey:
        midikeyrelease(note_n)
        pressedMidiKey.remove(note_n)"""
def keyprocess():
    global keyprocEndFlag
    global keynum2midinum
    key_list1 = ["z","x","c","v","b","n","m",",",".","/","_"]
    key_list2 = ["a","s","d","f","g","h","j","k","l",";",":","]"]
    key_list3 = ["q","w","e","r","t","y","u","i","o","p","@","["]
    global pressedMidiKey
    pressedMidiKey = []
    for k in key_list1:
        key.on_press_key(k, lambda c: keypress(key_list1.index(c.name)%len(keynum2midinum), key_list1.index(c.name)//len(keynum2midinum)))
        key.on_release_key(k, lambda c: keyrelease(key_list1.index(c.name)%len(keynum2midinum), key_list1.index(c.name)//len(keynum2midinum)))
    for k in key_list2:
        key.on_press_key(k, lambda c: keypress(key_list2.index(c.name)%len(keynum2midinum), key_list2.index(c.name)//len(keynum2midinum)+1))
        key.on_release_key(k, lambda c: keyrelease(key_list2.index(c.name)%len(keynum2midinum), key_list2.index(c.name)//len(keynum2midinum)+1))
    for k in key_list3:
        key.on_press_key(k, lambda c: keypress(key_list3.index(c.name)%len(keynum2midinum), key_list3.index(c.name)//len(keynum2midinum)+2))
        key.on_release_key(k, lambda c: keyrelease(key_list3.index(c.name)%len(keynum2midinum), key_list3.index(c.name)//len(keynum2midinum)+2))
    

def midikeypress(i,vel):
    if (i in pressedMidiKey) == False:
        global midiout
        midiout.note_on(i, vel)
        pressedMidiKey.append(i)

def midikeyrelease(i):
    if i in pressedMidiKey:
        global midiout
        midiout.note_off(i)
        pressedMidiKey.remove(i)

COLOR_TABLE = ("light gray","gray","white","gray15")
midiout = None
midi_devices = []
def main():
    global COLOR_TABLE
    global midi_devices
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
        #print(m.get_device_info(i))
        midi_devices.append(m.get_device_info(i)[1].decode())

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
    midiout = m.Output(1)

    keyTh = threading.Thread(target=keyprocess)
    keyTh.setDaemon(True)
    keyTh.start()

    #tkinter
    tk = tkinter.Tk()
    tk.geometry("723x200")
    tk.resizable(width=0,height=0)
    tk.title("Auto-magic MIDI Keyboard")
    tk.lift()
    tk.configure(bg=COLOR_TABLE[0])

    frame = tkinter.Frame(tk)
    frame.configure(bg=COLOR_TABLE[0])
    frame.grid()


    c = tkinter.Canvas(frame,width=723,height=100)
    c.configure(bg=COLOR_TABLE[1], highlightthickness=0)
    c.grid(row=0,column=0)

    pressing_key = 0
    def click(event):
        clicked = [
            obj for obj in c.find_overlapping(event.x-1, event.y+1,event.x+1,event.y-1)
        ]
        print(clicked)
        global pressing_key
        if clicked:
            pressing_key = int(c.gettags(clicked[0])[0])
            midikeypress(pressing_key,100)
            return
    def release(event):
        global pressing_key
        if pressing_key:
            midikeyrelease(pressing_key)
            pressing_key = 0



    black_keys = (1,3,6,8,10)
    for i in range(36):
        if i%12 in black_keys:
            k = c.create_rectangle(i*20+4,98,i*20+22,0, outline="", fill=COLOR_TABLE[3],tag=str(i+48))
        else:
            k = c.create_rectangle(i*20+4,98,i*20+22,0, outline="",fill=COLOR_TABLE[2],tag=str(i+48))
        #print(k)
        #print(c.gettags(k))
    c.bind('<Button-1>',click)
    c.bind('<ButtonRelease-1>',release)

    label1 = tkinter.Label(frame,text="Output Port")
    label1.grid(row=1,column=0)
    label2 = tkinter.Label(frame,text="Velocity")
    label2.grid(row=1,column=1)

    v=tkinter.StringVar()
    cb = ttk.Combobox(frame, textvariable=v, values=midi_devices, width=50)
    cb.set(midi_devices[0])
    cb.grid(row=2, column=0)
    vels = ttk.Scale(frame,variable=100,orient=tkinter.HORIZONTAL,length=200,from_=0,to=255)
    cb.grid(row=2, column=1)



    
    #tkinterメインループ
    tk.mainloop()

    keyTh.join()

    print("quit")
    midiout.close()
    m.quit()
    exit()

if __name__=="__main__":
    main()