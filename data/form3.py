from tkinter import Toplevel,Label,LabelFrame,Spinbox,Checkbutton,Button,PhotoImage, \
	StringVar,IntVar,colorchooser
from data.mygui import TFontList,TText

class Form3(object):
	def __init__(self,parent,callback,icon,args="open"):
		self.callback=callback
		self.parent=parent
		self.config=args
		self.w=dict()
		self.w[0]=Toplevel(self.parent)
		self.w[0].iconphoto(False, icon)
		self.w[0].title("Settings")
		w=420+4
		h=437+4
		x=(self.w[0].winfo_screenwidth()-w)//2
		y=(self.w[0].winfo_screenheight()-h)//2
		self.w[0].geometry(str(w)+"x"+str(h)+"+"+str(x)+"+"+str(y))
		self.w[0].resizable(False, False)
		self.w[0].transient(self.parent)
		self.w[0].grab_set()
		self.w[0].update()#otherwise the form freezes while loading fonts
		#================================================================
		self.w[1]=LabelFrame(
			self.w[0],
			relief="groove",
			bd=2,
			text=" Font "
		)
		self.w[1].place(x=8,y=5,width=193,height=290)
		self.w[2]=Label(
			self.w[1],
			bg="white",
			relief="sunken",
			bd=2
		)
		self.w[2].place(x=8,y=5,width=173,height=27)
		self.w[3]=TFontList(self.w[1],self.onselect)
		self.w[3].place(x=8,y=40,width=173,height=225)
		#================================================================
		self.w[4]=LabelFrame(
			self.w[0],
			relief="groove",
			bd=2,
			text=" Size and style "
		)
		self.w[4].place(x=208,y=5,width=168+40,height=106)
		self.w[5]=Label(
			self.w[4],
			text="Font size",
			anchor="w"
		)
		self.w[5].place(x=8,y=8,width=90+40,height=20)
		self.s1_var=StringVar()
		self.w[6] = Spinbox(
			self.w[4],
			values=(8,9,10,11,12,14,16,18,20,22,24),
			textvariable=self.s1_var,
			command=self.update_text_config,
			highlightthickness=0,
			state="readonly"
		)
		self.w[6].place(x=80,y=8,width=70+40,height=20)
		self.c1_var=IntVar()
		self.w[7]=Checkbutton(
			self.w[4],
			text="Bold",
			anchor="w",
			variable=self.c1_var,
			command=self.update_text_config,
			highlightthickness=0
		)
		self.w[7].place(x=5,y=40,width=90+40,height=20)
		self.c2_var=IntVar()
		self.w[8]=Checkbutton(
			self.w[4],
			text="Italic",
			anchor="w",
			variable=self.c2_var,
			command=self.update_text_config,
			highlightthickness=0
		)
		self.w[8].place(x=5,y=60,width=90+40,height=20)
		#================================================================
		self.w[9]=LabelFrame(
			self.w[0],
			relief="groove",
			bd=2,
			text=" Colors "
		)
		self.w[9].place(x=208,y=115,width=168+40,height=128)
		#draw widgets for choosing colors
		lst=[
			("text_bgcolor","Window background"),
			("text_color","Window text"),
			("highlight_bgcolor","Highlight background"),
			("highlight_color","Highlight text")
		]
		
		cur_id=10; cur_y=6
		for s in lst:
			self.w[cur_id]=Label(
				self.w[9],
				text=s[1],
				anchor="w"
			)
			self.w[cur_id].place(x=5,y=cur_y,height=16)
			self.w[cur_id+1]=Label(
				self.w[9],
				bg="white",
				cursor="hand2"
			)
			self.w[cur_id+1].place(x=135+40,y=cur_y,height=16,width=16)
			self.w[cur_id+1].tag=s#remember the name of the property for the title of the dialog window
			self.w[cur_id+1].bind("<Button-1>",self.select_color)
			
			cur_id+=2
			cur_y+=25
		#================================================================
		self.w[30]=LabelFrame(
			self.w[0],
			relief="groove",
			bd=2,
			text=" Features "
		)
		self.w[30].place(x=208,y=247,width=168+40,height=48)
		self.c3_var=IntVar()
		self.w[31]=Checkbutton(
			self.w[30],
			text="Line numbers",
			anchor="w",
			variable=self.c3_var,
			command=self.update_text_config,
			highlightthickness=0
		)
		self.w[31].place(x=5,y=6,width=130+40,height=20)
		#================================================================
		self.w[32]=TText(self.w[0],8,304,366+40,93,self.passproc,self.passproc)
		self.w[32].text="0123456789 Aa Bb Cc Dd Ee Ff\n"+"next line..."
		self.w[32].enable=False
		#================================================================
		self.img1=PhotoImage(file="data/img/ok.png")
		self.img2=PhotoImage(file="data/img/cancel.png")
		self.w[33]=Button(
			self.w[0],
			text="  Ok",
			command=self.ok,
			image=self.img1,
			compound="left",
			anchor="center",
			padx=3
		)
		self.w[33].place(x=8,y=407,width=100,height=28)
		self.w[34]=Button(
			self.w[0],
			text="  Cancel",
			command=self.cancel,
			image=self.img2,
			compound="left",
			anchor="center",
			padx=3
		)
		self.w[34].place(x=277+40,y=407,width=100,height=28)
		#================================================================
		self.w[0].focus()
		self.load_config()
		self.update_text_config()
				
		self.parent.wait_window(self.w[0])
		
		
	def select_color(self,event=None):
		try:
			t=event.widget.tag #take the color name in config
		except: return
		
		c=event.widget["background"]	
		(rgb,col)=colorchooser.askcolor(color=c,title="Select color for "+t[1],parent=self.w[0])
		if rgb==None:return
		(r,g,b)=rgb
		c=self.rgbtohex(r,g,b)
		event.widget["background"]=c
		# some color has changed - everything needs to be redrawn
		self.update_text_config()
		
	def rgbtohex(self,r,g,b):
		r=int(r);g=int(g);b=int(b)
		if r>255:r=255
		if g>255:g=255
		if b>255:b=255
		return "#{0:0>2X}{1:0>2X}{2:0>2X}".format(r,g,b)
    
	def load_config(self):
		self.w[3].famyly=self.config["font_family"]
		self.w[2]["text"]=self.config["font_family"]
		self.s1_var.set(str(self.config["font_size"]))
		self.c1_var.set(self.config["font_bold"])
		self.c2_var.set(self.config["font_italic"])
		self.c3_var.set(self.config["show_numbers"])
		#load colors
		for i in range(4):
			self.w[(i*2)+11]["background"]=self.config[self.w[(i*2)+11].tag[0]]
		
	def onselect(self,family):
		self.w[2]["text"]=family
		self.update_text_config()
		
	def passproc(self,event=None):# stub for TText!
		pass
		
	def ok(self,event=None):
		self.config["font_family"]=self.w[32].font_family
		self.config["font_size"]=self.w[32].font_size
		self.config["font_bold"]=self.w[32].font_bold
		self.config["font_italic"]=self.w[32].font_italic
		self.config["show_numbers"]=self.w[32].show_numbers
		self.config["text_bgcolor"]=self.w[11]["background"]
		self.config["text_color"]=self.w[13]["background"]
		self.config["highlight_bgcolor"]=self.w[15]["background"]
		self.config["highlight_color"]=self.w[17]["background"]
		self.callback("form3",self.config)
		self.w[0].destroy()

	def cancel(self,event=None):
		self.w[0].destroy()

	def update_text_config(self,event=None):
		self.w[32].font_family=self.w[2]["text"]
		self.w[32].font_bold=self.c1_var.get()
		self.w[32].font_italic=self.c2_var.get()
		self.w[32].font_size=int(self.s1_var.get())
		self.w[32].show_numbers=self.c3_var.get()
		self.w[32].text_bgcolor=self.w[11]["background"]
		self.w[32].text_color=self.w[13]["background"]
		self.w[32].highlight_bgcolor=self.w[15]["background"]
		self.w[32].highlight_color=self.w[17]["background"]
		
