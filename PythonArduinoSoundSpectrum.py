import pyaudio
import numpy as np
import serial
import time
import warnings
warnings.simplefilter("ignore", DeprecationWarning)
from termcolor import colored as clr
val = 0

#redLed = board.get_pin('a:2:o')
#greenLed = board.get_pin('a:3:o')
#blueLed = board.get_pin('a:5:o')
temp = ''
highS = 0
CHUNK = 2**11
RATE = 44100
port = 'COM7'
old=0
light=serial.Serial(port,9600)
time.sleep(2)
light.write(('255,w'+'\r\n').encode())
#time.sleep(2)
p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK)
def Gmap( x,  in_min,  in_max, out_min, out_max):
  return int((x - in_min) * (out_max - out_min) / (in_max - in_min ) + out_min)
def delay(milli):
    time.sleep(milli/1000)
def cmd(t):
    print("")
   # print((t+'\r\n').encode())
    #print(t)
    #light.write((t+'\r\n').encode())
    #print("")
#for i in range(int(10*44100/1024)): #go for a few seconds
while True:
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    peak=(np.average(np.abs(data))*2)
    bars="#"*int(50*peak/2**16)
    if len(bars)<1:
          print("|")
    #bars = bars + "#"
    l=len(bars)
    val=Gmap(l,0,30,0,255)
    Sval=str(val)
    
    #print(clr(bars, 'cyan'))
    if l <2 and l>1:
       print(clr(bars, 'cyan')*2)
    elif l>=2 and l<4:
        print(clr(bars, 'blue')*2)
    elif l>=4 and l<6:
       print(clr(bars, 'green')*2)
    elif l >=6 and l<8:
      print(clr(bars, 'magenta')*2)
    elif l>=8:
      print(clr(bars, 'red'))
    elif l==1:
      print(bars)
    if l!=old:
        old=l
    light.write((Sval+'\r\n').encode())
stream.stop_stream()
stream.close()
p.terminate()