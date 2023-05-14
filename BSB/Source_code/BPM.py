import time #used for sleep time
time.sleep(1)
import socket #used for getting IP Address
import psutil #used for getting ram and cpu 
from ina219_lib_v4 import ina219 #self made INA219 library 
from PIL import ImageFont, ImageDraw, Image #needed for OELD
import subprocess #used for shell commands
from Display_driver import display_i2c #display driver
display = 0  #used as a global var



#getting IP address
def IP_ADDR():
	ip = 0
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8",80)) 
		ip = "IP "+str(s.getsockname()[0])
		s.close()
	except Exception as ev: 
		ip = "Not connected"

	return ip
	

#getting ram 
def ram_u_per():
	mem_percent = psutil.virtual_memory().percent
	mem_round="RAM "+str(mem_percent)+"%"
	return mem_round
	

#getting CPU 
def cpu_u_per():
	cpu_ = psutil.cpu_percent(.05)
	CPU_int = "CPU "+str(cpu_)+"%"
	return CPU_int
	
#disk usage 
def disk_us():
	disk = psutil.disk_usage('.').percent
	disk_str = "disk "+str(disk)+"%"
	return disk_str


#power mode
def power_mode():
	
	target = subprocess.check_output("sudo nvpmodel -q '5W\|MAXN'", shell = True).decode('utf-8').strip('\n') #maybe needed: | grep -o 
	if target == "MAXN":
		target = "10W"
	else:
		target = "5W"
	
	#print("MODE")
	return target


#reading from INA

def read():
	
	volt=0
	current = 0	
	power = 0
	try:
		ina=ina219() #making shortcut for library		
		volt = ina._get_bus_volt()
		shunt = str(ina._get_shunt_volt())
		current = str(round(ina._get_current(), 2))
		power = str(ina._get_power())
		

	except (OSError, AttributeError) as ve:
		volt="0"
		current ="0"
		power="0"
	
	
	return 	volt, current, power
		
	
 
#method to get estimated battery level
 
def bat_lev(soc, dt, soc_init, BV, C):
	socList=[0]
	C = float(C)
	nomC = 2.5 #nominal currentin AH to be changed if battery have different nominal current
	numCell = 4 #number of battery cells (standard is 4)
	
	if C > 0.0:
		return "Charging"
	else:
		#used for fnding initial starting value of battery level
		while soc == 0: 
			if BV == 8.4:
				soc_init = 100
				break
			elif BV >= 7.6 and BV < 8.4:
				soc_init = 90
				break
			elif BV >= 7.5 and BV < 7.6:
				soc_init = 80
				break
			elif BV < 7.5 and BV >= 7.41:
				soc_init = 70
				break
			elif BV < 7.41 and BV > 7.38:
				soc_init = 60
				break
			elif BV <= 7.38 and BV > 7.35:
				soc_init = 50
				break
			elif BV <= 7.35 and BV > 7.3:
				soc_init = 40
				break
			elif BV <= 7.3 and BV > 7.2:
				soc_init = 30
				break
			elif BV <= 7.2 and BV > 6.9:
				soc_init = 20
				break
			elif BV <= 6.9 and BV > 5.8:
				soc_init = 10
				break
			elif BV > 5.75:
				soc_init = 5
				break
		if len(socList) == 10:
			soc = soc_init+(C*2*dt)/(nomC*numCell*36)	
			socList.append(soc)
			socList.pop(0)
			socP = sum(socList)/len(socList)
			return socP, soc_init
		else:
			soc = soc_init+(2*C*dt)/nomC*numCell*36)
			socList.append(soc)
			return soc, soc_init
		

	
	


def main():
	#declaring for important variables
	soc_init = 0
	soc = [0, 0]
	dt = 1
	ina =0
	i = 0
	
	CPU = addr=mem_round= disk_u= pow_1 = "0"
	bat_val = [0.2,"0","0"]
	display =0
	try :
		ina=ina219() #making shortcut for library
		ina._config()
		
		
	except (OSError, AttributeError) as ne:
		ina=0	
		
	while True: 
		
		try:		
			display=display_i2c()#shortcut to library
		except(OSError, AttributeError) as he:			
			display=0
			print("OLED is disconected")
		
		
		if ina == 0 and display == 0:

			time.sleep(2)
			dt += 2
			print("I2C disconnected")
			main()		

		if ina  == 0 and display != 0:
			#Check to see if ina219 disconnected			
			try:
				display.oled_refresh(10,10,"INA219 discoonnected")
				display.oled_print(10,10,"INA219 disconnected")
				display.oled_display()
				time.sleep(2)
				dt += 2.5
				main()
	
			except(AttributeError, OSError) as tr:
				time.sleep(2)
				dt += 2.5			
				main()
				
		else:
			try:
				display.oled_refresh(0,0, addr)
				display.oled_display()				
				addr = IP_ADDR()
				display.oled_print(0,0, addr)
				display.oled_display()
				display.oled_refresh(63,15,CPU)				
				CPU = cpu_u_per()
				display.oled_print(63,15, CPU)
				display.oled_display()
				display.oled_refresh(1,15, mem_round)
				mem_round = ram_u_per()
				display.oled_print(1,15, mem_round)
				display.oled_display()
				display.oled_refresh(60,45,disk_u)
				disk_u=disk_us()
				display.oled_print(60,45,disk_u)
				display.oled_display()
				display.oled_refresh(0, 45, pow_1)
				display.oled_display()
				pow_1=power_mode()
				display.oled_print(0, 45, pow_1)
				display.oled_display()				
				display.oled_refresh(0, 30, str(round(bat_val[0],1))+"V")
				display.oled_refresh(35, 30, bat_val[1]+"A")
				display.oled_refresh(80, 30, bat_val[2]+"W")
				display.oled_display()		
				bat_val = read()
				display.oled_print(0, 30, str(round(bat_val[0],1))+"V")
				display.oled_display()
				display.oled_print(35, 30, bat_val[1]+"A")
				display.oled_display()
				display.oled_print(80, 30, bat_val[2]+"W")
				display.oled_display()		
				display.oled_refresh(25, 45, str(round(soc[0]))+"%")
				display.oled_display()
				soc = bat_lev(soc[0], dt, soc_init, round(bat_val[0],1), bat_val[1])
				display.oled_print(25, 45, str(round(soc[0]))+"%")
				display.oled_display()
				time.sleep(2)
				soc_init = soc[1]
				dt += 5.5
				i +=1
				#print("antall: ", i)
				
				

			except Exception as e:
				#print(e)				
				time.sleep(2)
				main()
		
		
		
	
		

main()

