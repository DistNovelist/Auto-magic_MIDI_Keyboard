import pygame.midi as m
import time
import keyboard as key
import threading
import tkinter
notename = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
def gui():
    tk = tkinter.Tk()
    tk.geometry("600x200")
    tk.title("Auto-magic MIDI Keyboard")

    tk.mainloop()

def keyprocess():
    while True:
        if key.on_press

def main():
    print("Auto-magic MIDI Keyboard v0.1 by DIST_NOVELIST")
    m.init()
    print(str(m.get_default_output_id())+"/input:"+str(m.get_default_input_id()))
    i_num = m.get_count()
    for i in range(i_num):
        print(i)
        print(m.get_device_info(i))
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
            going = False
    midiout = m.Output(1)
    midiout.note_on(60,100)
    time.sleep(1)
    midiout.note_off(60)
    midiout.note_on(64,100)
    time.sleep(1)
    midiout.note_off(64)
    midiout.note_on(67,100)
    time.sleep(1)
    midiout.note_off(67)
    time.sleep(1)
    midiout.note_on(60,100)
    midiout.note_on(64,100)
    midiout.note_on(67,100)
    time.sleep(1)
    midiout.note_off(60,100)
    midiout.note_off(64,100)
    midiout.note_off(67,100)
    time.sleep(1)
    midiout.note_off(60)
    time.sleep(1)
    midiout.note_off(64)
    time.sleep(1)
    midiout.note_off(67)"""
    #i.close()

    guiTh = threading.Thread(target=gui)
    keyTh = threading.Thread(target=keyprocess)
    guiTh.start()
    keyTh.start()

    guiTh.join()
    keyTh.join()

    midiout = m.Output(1)
    midiout.close()
    m.quit()
    exit()

if __name__=="__main__":
    main()