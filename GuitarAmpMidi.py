import mido
import time

output = mido.open_output('MIDIMATE II:MIDIMATE II MIDI 2 20:1')
print (output)
#output.send(mido.Message('note_on', note=60, velocity=64))

AMP_CHANNEL_CLEAN = 89
AMP_CHANNEL_BOOST = 90
AMP_CHANNEL_XLEAD = 91

def setAmpChannel(myAmpChannel):
    print("switching amp to clean channel")
    output.send(mido.Message('program_change', channel=0, program=myAmpChannel))

def setGMajorProgram(myProgram):
    print("switching GMajor channel : ")
    print(myProgram)
    output.send(mido.Message('program_change', channel=1, program=myProgram-1))    

def setGMajorBoost(myValue):
    print("Boost GMajor channel : ")
    print(myValue)
    output.send(mido.Message('control_change', channel=1, control=85, value=127*myValue))    

def setGMajorDelay(myValue):
    print("Delay GMajor channel : ")
    print(myValue)
    output.send(mido.Message('control_change', channel=1, control=82, value=127*myValue))    

