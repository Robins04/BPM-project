#Display driver 

#Made from library using 
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


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



