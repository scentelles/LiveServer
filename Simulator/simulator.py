import sys  
sys.path.append("..")  

import tkinter as tk
from random import randint
import math

from PIL import ImageTk
from PIL import Image

import threading
import time

from pythonosc import udp_client
from pythonosc import osc_server
from pythonosc import dispatcher

from SmoothDefines import *  #TODO : used only for OBS. not smooth specific

import sys

from socket import (socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR,
                    SO_BROADCAST)
from struct import pack, unpack


from OSC_2_video_PC import *


#todo : use config file
clientVideoPC = udp_client.SimpleUDPClient("localhost", 5007)


class Stage:
    def __init__(self):
        self.fixtures = []
        self.u1_dmx_values = [ 0 for i in range(512)]
        self.u2_dmx_values = [ 0 for i in range(512)]
        self.u3_dmx_values = [ 0 for i in range(512)]
        self.u4_dmx_values = [ 0 for i in range(512)]
        self.universes = [self.u1_dmx_values, self.u2_dmx_values, self.u3_dmx_values, self.u4_dmx_values]
        
        
    def add_fixture(self, fixture):
        self.fixtures.append(fixture)
        
    def set_dmx(self, universe, channel, value):
        
        previous_value = self.universes[universe-1][channel-1]
        if(previous_value != value):
            self.universes[universe-1][channel-1] = value

            
            print("Universe " + str(universe), " : Setting channel " + str(channel) + " to value : " + str(value))
            for x in self.fixtures:
                #print("changing fixture color\n")
                if(x.universe == universe):
                    if((channel >= x.address - 1) and (channel <= x.address - 1 + x.range)):
                        x.set_dmx(self.universes[universe-1][x.address-1:x.address-1+x.range])
            




class Fixture:
    def __init__(self, label, xpos, ypos, size, universe, address, range=None, dimmer_index=None, R_index=None, G_index=None, B_index=None, W_index=None):
        self.xpos = xpos
        self.ypos = ypos
        self.size = size
        self.label = label
        self.address = address
        self.universe = universe
        self.range = range
        self.R_index = R_index
        self.G_index = G_index
        self.B_index = B_index
        self.W_index = W_index
        self.dimmer_index = dimmer_index
        
        
        self.drawItem()


    def drawItem(self):
        self.tkitem  = canvas.create_circle(self.xpos, self.ypos, self.size, fill="blue", outline="#DDD", width=2)
        self.tklabel = canvas.create_text(self.xpos,self.ypos + self.size + 10,fill="white",font="Times 10 italic bold", text=self.label)
        
    def render(self):
        canvas.itemconfig(item, fill = color)
    
    def calculate_RGBW_color(self, R,G,B,W, dimmer_value):
        return from_rgb((int(dimmer_value * min(R + W, 255)), int(dimmer_value * min(G + W, 255)), int(dimmer_value * min(B + W, 255))))
    
    def set_dmx(self, values):

        R_value = values[self.R_index - 1]
        G_value = values[self.G_index - 1]
        B_value = values[self.B_index - 1]
        if(self.W_index != None):
            W_value = values[self.W_index - 1]
        if(self.dimmer_index != None):
            dimmer_value = float(values[self.dimmer_index - 1])/255
        if((self.W_index != None) and (self.dimmer_index != None)):
            
            color = self.calculate_RGBW_color(R_value, G_value, B_value, W_value, dimmer_value)
        
        else:
            if((self.W_index == None) and (self.dimmer_index != None)):
                color = self.calculate_RGBW_color(R_value, G_value, B_value, 0, dimmer_value)
            else:
                color = self.calculate_RGBW_color(R_value, G_value, B_value, 0, 1)
                
        #print ("colorDMX : " + color + "\n")
        canvas.itemconfig(self.tkitem, fill = color)


class OBS(Fixture):
    def __init__(self, label, xpos, ypos, size, universe, address, range=None, dimmer_index=None, R_index=None, G_index=None, B_index=None, W_index=None):
        Fixture.__init__(self, label, xpos, ypos, size, universe, address, range=range, dimmer_index=dimmer_index, R_index=R_index, G_index=G_index, B_index=B_index, W_index=W_index)
        self.OBS_SCENE      = 0
        self.OBS_COLLECTION = 0
        
    def drawItem(self):
        return

    def set_dmx(self, values):
        

        new_OBS_SCENE = values[DMX_CHANNEL_OBS_SCENE - self.address]  
     
        if(self.OBS_SCENE != new_OBS_SCENE):
            self.OBS_SCENE = new_OBS_SCENE
            process_OSC_2_video_PC(clientVideoPC, DMX_CHANNEL_OBS_SCENE - 1, self.OBS_SCENE)

        new_OBS_COLLECTION = values[DMX_CHANNEL_OBS_COLLECTION - self.address]  
     
        if(self.OBS_COLLECTION != new_OBS_COLLECTION):
            self.OBS_COLLECTION = new_OBS_COLLECTION
            #Not implemented
            #process_OSC_2_video_PC(clientVideoPC, DMX_CHANNEL_OBS_COLLECTION - 1, self.OBS_COLLECTION)            
            
            
            
class Visualizer(Fixture):
    def __init__(self, label, xpos, ypos, size, universe, address, range=None, dimmer_index=None, R_index=None, G_index=None, B_index=None, W_index=None):
        Fixture.__init__(self, label, xpos, ypos, size, universe, address, range=range, dimmer_index=dimmer_index, R_index=R_index, G_index=G_index, B_index=B_index, W_index=W_index)
        self.VISUALIZER_PRESET = 0
     
    def drawItem(self):
        return

    def set_dmx(self, values):
        

        new_VISUALIZER_PRESET = values[DMX_CHANNEL_VISUALIZER_PRESET - self.address]  
     
        if(self.VISUALIZER_PRESET != new_VISUALIZER_PRESET):
            self.VISUALIZER_PRESET = new_VISUALIZER_PRESET
            process_OSC_2_video_PC(clientVideoPC, DMX_CHANNEL_VISUALIZER_PRESET - 1, self.VISUALIZER_PRESET)
            

        
class MegaScreen(Fixture):
    def __init__(self, label, xpos, ypos, size, universe, address, range=None, dimmer_index=None, R_index=None, G_index=None, B_index=None, W_index=None):
        Fixture.__init__(self, label, xpos, ypos, size, universe=universe, address=address, range=range, dimmer_index=dimmer_index, R_index=R_index, G_index=G_index, B_index=B_index, W_index=W_index)
     
    def drawItem(self):
        self.tkitem  = canvas.create_rectangle(self.xpos, self.ypos, self.xpos+self.size*2, self.ypos+self.size, fill="blue", outline="#DDD", width=4)
        self.tklabel = canvas.create_text(self.xpos + self.size,self.ypos + self.size + 10,fill="white",font="Times 10 italic bold", text=self.label)

    def set_dmx(self, values):
        print("Megascreen set value : ", values)
        R_value = values[self.R_index - 1]
        G_value = values[self.G_index - 1]
        B_value = values[self.B_index - 1]
        
       
            
        if(self.W_index != None):
            W_value = values[self.W_index - 1]
        if(self.dimmer_index != None):
            dimmer_value = float(values[self.dimmer_index - 1])/255
        if((self.W_index != None) and (self.dimmer_index != None)):
            
            color = self.calculate_RGBW_color(R_value, G_value, B_value, W_value, dimmer_value)
        
        else:
            if((self.W_index == None) and (self.dimmer_index != None)):
                color = self.calculate_RGBW_color(R_value, G_value, B_value, 0, dimmer_value)
            else:
                color = self.calculate_RGBW_color(R_value, G_value, B_value, 0, 1)
                
        #print ("colorDMX : " + color + "\n")
        canvas.itemconfig(self.tkitem, fill = color)



        
def from_rgb(rgb):
    #translates an rgb tuple of int to a tkinter friendly color code
    return "#%02x%02x%02x" % rgb  
    
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)


def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)


#canvas.create_circle(100, 120, 50, fill="blue", outline="#DDD", width=4)
#canvas.create_circle_arc(100, 120, 48, fill="green", outline="", start=45, end=140)
#canvas.create_circle_arc(100, 120, 48, fill="green", outline="", start=275, end=305)
#canvas.create_circle_arc(100, 120, 45, style="arc", outline="white", width=6, start=270-25, end=270+25)
#canvas.create_circle(150, 40, 20, fill="#BBB", outline="")



def print_qlc_handler(osc_address, args, message):
    print("received OSC message from QLC")
    print("address : " + osc_address)

    temp = osc_address.split("/")
    universe = int(temp[1]) + 1
    channel  = int(temp[3]) + 1  
    print("channel : " + str(channel))
    value = int(float(message) * 255)
    print(value)
    my_stage.set_dmx(universe, channel, value)
  
 # temp = osc_address.split("/")
 # note = int(temp[4])
 # print (note);
 
root = tk.Tk()
canvas = tk.Canvas(root, width=800, height=600, borderwidth=0, highlightthickness=0, bg="black")
canvas.pack()
my_stage = Stage()

dispatcher = dispatcher.Dispatcher()

def OSC_universe1_thread(name):

    dispatcher.map("/*", print_qlc_handler, "qlc_laserharp")

    server = osc_server.ThreadingOSCUDPServer(
        ("127.0.0.1", 9000), dispatcher)

    try:
        print("Entering main loop. Press Control-C to exit.")
        server.serve_forever()
    except KeyboardInterrupt:
        exit()

def OSC_universe2_thread(name):

    dispatcher.map("/*", print_qlc_handler, "qlc_laserharp")

    server = osc_server.ThreadingOSCUDPServer(
        ("127.0.0.1", 9001), dispatcher)

    try:
        print("Entering main loop. Press Control-C to exit.")
        server.serve_forever()
    except KeyboardInterrupt:
        exit()

def OSC_universe3_thread(name):

    dispatcher.map("/*", print_qlc_handler, "qlc_laserharp")

    server = osc_server.ThreadingOSCUDPServer(
        ("127.0.0.1", 9002), dispatcher)

    try:
        print("Entering main loop. Press Control-C to exit.")
        server.serve_forever()
    except KeyboardInterrupt:
        exit()

def OSC_universe4_thread(name):

    dispatcher.map("/*", print_qlc_handler, "qlc_laserharp")

    server = osc_server.ThreadingOSCUDPServer(
        ("127.0.0.1", 9003), dispatcher)

    try:
        print("Entering main loop. Press Control-C to exit.")
        server.serve_forever()
    except KeyboardInterrupt:
        exit()

        
        
def main():
    tk.Canvas.create_circle = _create_circle

    tk.Canvas.create_circle_arc = _create_circle_arc

    #PAR_FRONT=canvas.create_circle(100, 120, 20, fill="blue", outline="#DDD", width=2)
    #LYRE_CHRIS=canvas.create_circle(150, 120, 20, fill="blue", outline="#DDD", width=2)


    #Building the stage

    my_stage.add_fixture(Fixture("PAR_RL", 370,30,20, universe=1, address = 24, range = 8, R_index = 2, G_index = 3, B_index = 4, W_index = None, dimmer_index=1))
    my_stage.add_fixture(Fixture("PAR_RR", 430,30,20, universe=1, address = 24, range = 8, R_index = 2, G_index = 3, B_index = 4, W_index = None, dimmer_index=1))
    #my_stage.add_fixture(Fixture("LYRE_L", 300,100,25, universe=1, address = 40))
    #my_stage.add_fixture(Fixture("LYRE_R", 500,100,25, universe=1, address = 40))

    my_stage.add_fixture(Fixture("LYRE CHRIS" , 200,500,20, universe=2, address = 1, range = 14, R_index = 7, G_index = 8, B_index = 9, W_index = 10, dimmer_index=6 ))
    my_stage.add_fixture(Fixture("LYRE SLY"   , 400,500,20, universe=2, address = 15, range = 14, R_index = 7, G_index = 8, B_index = 9, W_index = 10, dimmer_index=6))
    my_stage.add_fixture(Fixture("LYRE GUI"   , 600,500,20, universe=2, address = 29, range = 14, R_index = 7, G_index = 8, B_index = 9, W_index = 10, dimmer_index=6))
#    my_stage.add_fixture(Fixture("BTLED CHRIS", 200,400,10, universe=3, address = 1, R_index = 1, G_index = 2, B_index = 3, W_index = None, dimmer_index=None))
    #btled_sly   = Fixture(400,400,20)
#    my_stage.add_fixture(Fixture("BTLED GUI", 600,400,10, universe=3, address = 7, R_index = 1, G_index = 2, B_index = 3, W_index = None, dimmer_index=None))
    my_stage.add_fixture(Fixture("PAR_FL", 50,550,25,  universe=1, address = 8, range = 8, R_index = 2, G_index = 3, B_index = 4, W_index = None, dimmer_index=1))
    my_stage.add_fixture(Fixture("PAR_FR", 750,550,25, universe=1, address = 8, range = 8, R_index = 2, G_index = 3, B_index = 4, W_index = None, dimmer_index=1))

    my_stage.add_fixture(MegaScreen("MEGASCREEN", 180,100,220, universe=3, address = 24, range = 5, R_index = 2, G_index = 3, B_index = 4, W_index = None, dimmer_index=1))
    my_stage.add_fixture(OBS("OBS", 0,0,0, universe=3, address = 20, range = 2))
    my_stage.add_fixture(Visualizer("VISUALIZER", 0,0,0, universe=3, address = 32, range = 3))



    U1 = threading.Thread(target=OSC_universe1_thread, args=(1,))
    U1.start()
    U2 = threading.Thread(target=OSC_universe2_thread, args=(1,))
    U2.start()
    U3 = threading.Thread(target=OSC_universe3_thread, args=(1,))
    U3.start()
    U4 = threading.Thread(target=OSC_universe4_thread, args=(1,))
    U4.start()
    
    
    root.wm_title("Circles and Arcs")
    root.mainloop()
    
    x.join()
    
    
exitapp = False
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exitapp = True
        raise
