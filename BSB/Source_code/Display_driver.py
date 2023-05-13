#Display driver 

#Made from library using 
# Substantially derived from code by (c) 2015 Richard Hull The MIT License (MIT)
# https://github.com/rm-hull/ssd1306:
#       "Permission is hereby granted, free of charge, to any person obtaining a copy
#       "of this software and associated documentation files (the "Software"), to deal
#       "in the Software without restriction, including without limitation the rights
#       "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#       "copies of the Software, and to permit persons to whom the Software is
#       "furnished to do so, subject to the following conditions:
#       "The above copyright notice and this permission notice shall be included in
#       "all copies or substantial portions of the Software."
#
# B Lavery 2015:
# This derivative "library" module is not installed to the python system as Hull's version was:
# it simply resides alongside your own python script.
# In this version, the I2C bus object needs to be handed in as a parameter from your user code.
# This makes this one same library file work with either Raspberry Pi or Virtual GPIO system.
# Hull's (clever) auto-displaying "canvas" is replaced by a persistent draw object
# which can be incrementally changed. This canvas needs coded "display()" calls to push to the hardware.


from lib_oled96 import ssd1306 #library for ssd1306 
import smbus #i2c library for python 


class display_i2c():
	def __init__(self, _BUS=1):
		self.i2c = smbus.SMBus(_BUS)
		self.oled = ssd1306(self.i2c) #creating object 


	def oled_print (self,x, y, value):
		#print("type value: ", value)
		#print("x: ", x)
		#print("y", y)
		self.oled.canvas.text((x,y), value, fill=1)

	
	def oled_display(self):
		self.oled.display()

	def oled_refresh(self, x,y,value):
		self.oled.canvas.text((x,y), value, fill=0)

	def oled_clear(self):
		self.oled.cls()



