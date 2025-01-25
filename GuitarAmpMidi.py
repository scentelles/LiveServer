import mido
import time


#ports = mido.get_input_names()
#print(ports)

#ports = mido.get_output_names()
#print(ports)

try:
  midi_output = mido.open_output('MIDIMATE II:MIDIMATE II MIDI 2 24:1')
  print (output)
except:
  print("Midi output interface not found")


try:
  midi_input = mido.open_input('MIDIMATE II:MIDIMATE II MIDI 1 24:0')
  print (midi_input)
except:
  print("Midi input interface not found")

#output.send(mido.Message('note_on', note=60, velocity=64))

AMP_CHANNEL_CLEAN = 89
AMP_CHANNEL_BOOST = 90
AMP_CHANNEL_XLEAD = 91

def setAmpChannel(output, myAmpChannel):
    print("switching amp channel : ")
    print(myAmpChannel)
    output.send(mido.Message('program_change', channel=0, program=myAmpChannel))

def setGMajorProgram(output, myProgram):
    print("switching GMajor channel : ")
    print(myProgram)
    output.send(mido.Message('program_change', channel=1, program=myProgram-1))    

def setGMajorBoost(output, myValue):
    print("Boost GMajor channel : ")
    print(myValue)
    output.send(mido.Message('control_change', channel=1, control=85, value=127*myValue))    

def setGMajorDelay(output, myValue):
    print("Delay GMajor channel : ")
    print(myValue)
    output.send(mido.Message('control_change', channel=1, control=82, value=127*myValue))    

    
