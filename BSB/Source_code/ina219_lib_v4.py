import smbus
import math
import time


class ina219():
	def __init__ (self, _BUS=1, cal=4096):
		self.INA219_ADDR = 0x40
		self.INA219_CONFIG = 0x00
		self.INA219_SHUNT_V = 0x01
		self.INA219_BUS_V = 0x02
		self.INA219_POWER_REGISTER = 0x03
		self.INA219_CURRENT = 0x04
		self.INA219_CAL = 0x05
		self.config_val = 0x557	
		#self.config_val = 0x2557 #set for diff gain and FSR 


		self._CAL = cal
		self.bus = smbus.SMBus(_BUS)
		self.s_cal = 0
		self.currentlsb = 0
		self.powerlsb = 0
		
		self.set_cal_16V_3A() #Change name for the final product

	

	def _write_word(self, reg, data): #inspired by hrshoven
		data_bytes=[(data >> 8) & 0xFF, data & 0xFF]
		self.bus.write_i2c_block_data(self.INA219_ADDR, reg, data_bytes)

	def _read_word(self, reg): #inspired by hrshoven
		data_bytes=self.bus.read_i2c_block_data(self.INA219_ADDR, reg, 2) # ending with 2 because it is 16bit registers and it indicates that we want to extract 2 bytes of data
		data = (data_bytes[0] << 8) | data_bytes[1]
		return data



	def set_cal_16V_3A(self): #inspired by Dean Miller
		##CALCULATIONS
		#Vbus max = 32V
		VSHUNT_MAX = .04	#ASSUMES GAIN 8, +-320mV
		RSHUNT = 0.01

		"""
		1 max current 
		Max_I = VSHUNT/RSHUNT
		=4A
	
		2. max expected current 
		exc_max_I = 1A
	
		3. calc possible LSb range 
		minLSb = exc_max_I/32767
		minLSb = 0.000076   76µA
		maxLSb = exc_max_I/4096
		maxLSb = 0.000976   610µA


		4. choose an LSb between max and min
		want a roundish number near minLSb
		currentlsb = 76µA
		"""
		self.currentlsb = 0.085 #in mA
	
		#5. compute calibration register
		
		cal = math.trunc((0.04096)/(self.currentlsb*RSHUNT))
		#cal = 53
		
		#6. calc power lsb
		self.powerlsb= 20*self.currentlsb
		#print("POWLS", self.powerlsb)

		#push to calibration register 
		self.s_cal=cal
		#print("CAL: ", self.s_cal)
		self._write_word(self.INA219_CAL, self.s_cal)

		



	def _config(self):
		self._write_word(self.INA219_CONFIG, self.config_val)
		#print(self.config_val)
	

	def _get_bus_volt(self): #inspired by hrshoven 
		RAW_volt = self._read_word(self.INA219_BUS_V)
		#print("raW: ", RAW_volt)
		volt = round((RAW_volt >> 3)*4*0.001, 4)
		#print(volt)
		return volt

	def _get_shunt_volt(self): #inspired by hrshoven
		shunt_volt = self._read_word(self.INA219_SHUNT_V)
		if shunt_volt > 0x7FF:
			shunt_volt -= 0x10000		
		
		shunt_volt_1 = shunt_volt*0.00001		
		#print("shunt_raw: ",shunt_volt)
		#print("shunt_1: ",shunt_volt_1)
		return shunt_volt_1

	def _get_current(self): #inspired by hrshoven
		#print("s_cal: ", self.s_cal)
		self._write_word(self.INA219_CAL, self.s_cal)
		time.sleep(0.5)
		raw_curr = self._read_word(self.INA219_CURRENT)
		if raw_curr > 0x7FF:
			raw_curr-= 0X10000
		current = raw_curr*self.currentlsb*-1 #*1000 #multiply with 1000 for miliamp 
		return current


	def _get_power(self):
		raw_pow = self._read_word(self.INA219_POWER_REGISTER)
		raw_pow *= self.powerlsb*0.001
		BV = self._get_bus_volt()
		C = self._get_current()
		pow = round((C*BV),2)
		return pow







