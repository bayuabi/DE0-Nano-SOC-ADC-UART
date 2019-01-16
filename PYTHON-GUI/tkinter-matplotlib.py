import serial
import serial.tools.list_ports
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style 
from matplotlib import animation

import tkinter as tk 
from tkinter import ttk 


noPort = True

ports = list(serial.tools.list_ports.comports())

if len(ports) > 0:
	noPort = False
	portlist = []
	for p in ports:
		dash = str(p).find('-')
		com = str(p)[0:dash-1]
		portlist.append(com)
else:
	noPort = True
	portlist = [""]



LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

channel = 1
port = ""
baudrate = 0
ser = None
pause = True

fig = Figure(figsize=(10,5), dpi=120)
a = fig.add_subplot(1,1,1)

xs = list(range(0,200))

ys = [[-1]*200, [-1]*200, [-1]*200, [-1]*200, [-1]*200, [-1]*200, [-1]*200, [-1]*200]

a.set_ylim([0,5])
a.set_xlim([0,200])
a.set_ylabel("Voltage (volt)")

# title_text = "Grafik ADC Channel " + str(channel)
# title = a.set_title(title_text)
line, = a.plot(xs,ys[channel], color="b")

# line, = a.plot([],[], color="b")
  
def getData():
	global pause

	try:
		# if not pause:
		line = ser.readline().decode('utf-8').split('\r\n')
		data = line[0].split(',')
		ch = []
		if data[0] == "A":
			for i in range(8):
				ch.append(float((int(data[i+1])*4.096)/4096))
				# ch.append(int(data[i+1]))
			return ch
	except:
		return [-1,-1,-1,-1,-1,-1,-1,-1]
		# print("Choose Port")


def animate(i, ys):
	global channel 
	global pause
	global title_text
	title_text = "Grafik ADC Channel " + str(channel)
	
	if not pause:
		allChannel = getData()
		# print(allChannel)
		for i in range(8):
			ys[i].append(allChannel[i])
			ys[i] = ys[i][-200:]
		line.set_ydata(ys[channel])
	else:
		for i in range (8):
			for a in range (200):
				ys[i].append(-1)
			ys[i] = ys[i][-200:]
		line.set_ydata(ys[channel]) 
	return line, 

def portPick(value):
	global port
	port = value

def baudratePick(value):
	global baudrate
	baudrate = value
	

class ADC_UART_FPGA_App(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		tk.Tk.iconbitmap(self, default="logolapan.ico")
		tk.Tk.wm_title(self, "ADC FPGA APP")

		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		# container.grid_rowconfigure(1, weight=1)
		# container.grid_columnconfigure(1, weight=1)

		self.frames = {}
			
		frame1 = homePage(container, self)
		self.frames[homePage] = frame1
		frame1.grid(row=0, column=0, sticky="nsew")

		self.show_frame(homePage)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

class homePage(tk.Frame):
	def __init__(self, parent, controller):
		global portlist
		global noPort
		tk.Frame.__init__(self, parent)

		title = tk.Label(self, text="ADC-FPGA to Serial USB", font=LARGE_FONT)
		title.grid(column=3, row = 0,rowspan=2, pady=10, padx = 10)

		channelTitle = ttk.Label(self, text="Grafik Channel 1", font=("Verdana", 12))
		channelTitle.grid(column=3, row=2, pady=5,padx=5)

		def channelChange(channelPick):
			global channel

			channel = channelPick

			text = "Grafik Channel " + str(channel+1)
			channelTitle.config(text=text)

		portLabel = ttk.Label(self, text="Port :")
		portLabel.grid(column=0,
					   row=0,
					   sticky="wns",
					   padx=5)
		baudrateLabel = ttk.Label(self, text="Baudrate :")
		baudrateLabel.grid(column=0,
					   row=1,
					   sticky="wns",
					   padx=5)


		portMenu = ttk.OptionMenu(self, tk.StringVar(), portlist[0], *portlist,
								  command=portPick)
		portMenu.grid(column=1,
					  row=0,
					  pady=5,
					  sticky="ewns")
		baudrateOptions = ['9600','19200','38400','115200']
		baudrateMenu = ttk.OptionMenu(self, tk.StringVar(), baudrateOptions[0], *baudrateOptions,
									  command=baudratePick)
		baudrateMenu.grid(column=1,
					  row=1,
					  pady=5,
					  sticky="ewns")
		def start():
			global port
			global baudrate
			global ser
			global pause

			baudrate = int(baudrate)
			# print(port) 
			# print(type(baudrate))
			
			if startButton.config('text')[-1] == 'START':
				startButton.config(text="STOP")
				ser = serial.Serial(port, baudrate)
				pause = False
			else:
				startButton.config(text="START")
				ser.close()
				pause = True

		startButton = ttk.Button(self, 
							   text="START",
							   command=start)
		startButton.grid(column = 0,
					   row = 2,
					   pady = 5,
					   columnspan=2)
		

		def startStop():
			if startButton.config('text')[-1] == 'START':
				startButton.config(text="STOP")
			else:
				startButton.config(text="START")

		ch1Button = ttk.Button(self, 
							   text="Channel 1",
							   command=lambda: channelChange(0))
		ch1Button.grid(column = 0,
					   row = 3,
					   pady = 20,
					   columnspan=2)

		ch2Button = ttk.Button(self, 
							   text="Channel 2",
							   command=lambda: channelChange(1))
		ch2Button.grid(column = 0,
					   row = 4,
					   pady = 20,
					   columnspan=2)
		ch3Button = ttk.Button(self, 
							   text="Channel 3",
							   command=lambda: channelChange(2))
		ch3Button.grid(column = 0,
					   row = 5,
					   pady = 20,
					   columnspan=2)
		ch4Button = ttk.Button(self, 
							   text="Channel 4",
							   command=lambda: channelChange(3))
		ch4Button.grid(column = 0,
					   row = 6,
					   pady = 20,
					   columnspan=2)
		ch5Button = ttk.Button(self, 
							   text="Channel 5",
							   command=lambda: channelChange(4))
		ch5Button.grid(column = 0,
					   row = 7,
					   pady = 20,
					   columnspan=2)
		ch6Button = ttk.Button(self, 
							   text="Channel 6",
							   command=lambda: channelChange(5))
		ch6Button.grid(column = 0,
					   row = 8,
					   pady = 20,
					   columnspan=2)
		ch7Button = ttk.Button(self, 
							   text="Channel 7",
							   command=lambda: channelChange(6))
		ch7Button.grid(column = 0,
					   row = 9,
					   pady = 20,
					   columnspan=2)
		ch8Button = ttk.Button(self, 
							   text="Channel 8",
							   command=lambda: channelChange(7))
		ch8Button.grid(column = 0,
					   row = 10,
					   pady = 20,
					   columnspan=2)


		canvas = FigureCanvasTkAgg(fig, self)
		canvas.show()
		canvas.get_tk_widget().grid(column=3, row=3, padx=50, rowspan=8)
		
		# toolbar = NavigationToolbar2TkAgg(canvas, self)
		# toolbar.update()
		# canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

app = ADC_UART_FPGA_App()
w, h = app.winfo_screenwidth(), app.winfo_screenheight()
app.geometry("%dx%d+0+0" % (w,h) )
# app.geometry("1920x1080")
ani = animation.FuncAnimation(fig, animate, fargs=(ys,), interval=10, blit=True)
ani.event_source.stop()
app.mainloop()