#!/usr/bin/env python
#!/usr/bin/python
#--------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#  lcd_i2c.py
#  LCD test script using I2C backpack.
#  Supports 16x2 and 20x4 screens.
#
# Author : Matt Hawkins
# Date   : 20/09/2015
#
# http://www.raspberrypi-spy.co.uk/
#
# Copyright 2015 Matt Hawkins
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#--------------------------------------
import smbus
import time
import RPi.GPIO as GPIO
import os
import vlc
from ftplib import FTP
def download():
    #download from /sw to /carol
    inner=0  
     
    ftp = FTP("192.168.0.105","root","raspberry")
    #ftp.retrlines("LIST")
     
    ftp.cwd("/sw")
    
    downlist=[]
     
    ftp.retrlines("LIST",downlist.append)
    print(downlist)
     
    while inner<len(downlist):
        word = downlist[inner].split(None,8)
        print(word)
        filename=word[-1].lstrip()
        print(filename)
        #ftp.pwd()
        local_filename = os.path.join("/home/pi/carol/" + filename)
        print(local_filename)
        If = open(local_filename,"wb")
        ftp.retrbinary("RETR "+filename, If.write, 1024)
        If.close()
        inner += 1
        print(downlist)
    return True

def download2():
    #download from /pop to /ballad
    inn=0  
     
    ftp = FTP("192.168.0.105","root","raspberry")
    #ftp.retrlines("LIST")
     
    ftp.cwd("/pop")
    
    downlist2=[]
     
    ftp.retrlines("LIST",downlist2.append)
    print(downlist2)
     
    while inn<len(downlist2):
        word2 = downlist2[inn].split(None,8)
        print(word2)
        filename2=word2[-1].lstrip()
        print(filename2)
        #ftp.pwd()
        local_filename2 = os.path.join("/home/pi/ballad/" + filename2)
        print(local_filename2)
        If = open(local_filename2,"wb")
        ftp.retrbinary("RETR "+filename2, If.write, 1024)
        If.close()
        inn += 1
        print(downlist2)
    return True
    

# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display
  

  message = message.rjust(LCD_WIDTH," ")
  

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def main():
  # file reading
  index = open('/home/pi/index2.txt','r')
  indexcontent = int(index.read())
  index.close()
  
  # Main program block
  playing = False

  lcd_string("    WELCOME!    ",LCD_LINE_1)
  lcd_string(" We Are Team 8! ",LCD_LINE_2)
  #download()
  #playing = download2()
  playing = True

  # Initialise display
  lcd_init()
  GPIO.setmode(GPIO.BCM)

  GPIO.setup(20, GPIO.IN)
  GPIO.setup(21, GPIO.IN)
  GPIO.setup(23, GPIO.IN)
  GPIO.setup(24, GPIO.IN)
  GPIO.setup(25, GPIO.IN)

  # folder reading
  folder = open('/home/pi/index.txt','r')
  foldername = folder.read()
  folder.close()
  
  mpath = "/home/pi/carol/"
  kpath = "/home/pi/ballad/"
  path = foldername
  klist = os.listdir("/home/pi/ballad/")
  mlist = os.listdir("/home/pi/carol/")
  alist = os.listdir(foldername)
  
  instance = vlc.Instance()
  player = instance.media_player_new()
  seq = indexcontent
  #txt STORAGE

  #txt file save

  media = instance.media_new(path + alist[seq])

  player.set_media(media)

  player.play()

  time.sleep(1)
     
  a = player.get_state()
  k = 0
  while playing:
      if(k == 12):
          k = 0
      a = player.get_state()

      k = k+1
      time.sleep(0.2)
      
      lcd_string(alist[seq]+ str(" ")*k,LCD_LINE_1)
      lcd_string(str(a)+ str(" ")*k,LCD_LINE_2)
      if a == 6:
          seq = seq + 1
          if seq == len(alist):
              seq = 0
          media = instance.media_new(path + alist[seq])
          player.set_media(media)
          lcd_string(alist[seq]+ str(" ")*k,LCD_LINE_1)
          lcd_string(str(a) + str(" ")*k,LCD_LINE_2)
          player.play()
          
          time.sleep(1)
          k = k+1
          
           
      if a == 5:
          break


      #BACK     
      if GPIO.input(21) == 0 :
         k = 0
         player.stop()
         seq = seq - 1
         if seq == -1:
             seq = len(alist)-1
         media = instance.media_new(path + alist[seq])

         player.set_media(media)

         player.play()
         lcd_string(alist[seq] + str(" ")*k ,LCD_LINE_1)
         lcd_string(str(a) + str(" ")*k ,LCD_LINE_2)
            
                 
         a = player.get_state()
         time.sleep(1)
         k = k+1


      #NEXT
      if GPIO.input(24) == 0 :
          k = 0
          player.stop()
          seq = seq + 1
          if seq == len(alist):
              seq = 0
          media = instance.media_new(path + alist[seq])
          player.set_media(media)
          player.play()
          lcd_string(alist[seq] + str(" ")*k,LCD_LINE_1)
          lcd_string(str(a) + str(" ")*k ,LCD_LINE_2)
          
          time.sleep(1)
          k = k+1


      #PAUSE
      if GPIO.input(20) == 0 :
          k = 0
          player.pause()
          a = player.get_state()
          lcd_string(alist[seq] + str(" ")*k ,LCD_LINE_1)
          lcd_string(str(a) + str(" ")*k ,LCD_LINE_2)
          
          time.sleep(1)
          k = k+1


      #Channel
      if GPIO.input(23) == 0 :
          k = 0
          player.stop()
         
          if path == "/home/pi/carol/":
              path = kpath
              alist = klist

          else:
              path = mpath
              alist = mlist
              
          
          media = instance.media_new(path + alist[seq])
          player.set_media(media)
          player.play()
          lcd_string(alist[seq] + str(" ")*k,LCD_LINE_1)
          lcd_string(str(a) + str(" ")*k ,LCD_LINE_2)
          
          time.sleep(1)
          k = k+1

          #media = instance.media_new(path + mlist[seq])

          #player.set_media(media)

          #player.play()
          #lcd_string(mlist[seq] + str(" ")*k ,LCD_LINE_1)
          #lcd_string(str(a) + str(" ")*k ,LCD_LINE_2)
            
                 
        #  a = player.get_state()
          #time.sleep(1)
          #k = k+1


      #SHUT DOWN
      if GPIO.input(25) == 0 :
          a = player.get_state()
          if a == 3:
              player.stop()
  indexnum=str(seq)
  index = open('index2.txt','w')
  index.write(indexnum)
  index.close()
  
  folder = open('index.txt','w')
  folder.write(path)
  folder.close()
   
   
    
if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)


