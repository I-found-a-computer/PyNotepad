from tkinter import Toplevel,Label,Entry,Button,PhotoImage,Checkbutton,IntVar

class Form5(object):
	def __init__(self,parent,callback,icon,args="open"):
		self.callback=callback
		self.parent=parent
		self.ctl=Toplevel(self.parent)
		self.ctl.iconphoto(False, icon)
		self.ctl.title("Find and replace")
		self.state=0
		w=538
		h=163
		x=(self.ctl.winfo_screenwidth()-w)//2
		y=(self.ctl.winfo_screenheight()-h)//2
		self.ctl.geometry(str(w)+"x"+str(h)+"+"+str(x)+"+"+str(y))
		self.ctl.resizable(False, False)
		self.ctl.transient(self.parent)
		self.img1=PhotoImage(file="data/img/search.png")
		self.img2=PhotoImage(file="data/img/cancel.png")
		self.img3=PhotoImage(file="data/img/search_next.png")
		self.img4=PhotoImage(file="data/img/replace.png")
		self.img5=PhotoImage(file="data/img/replace_all.png")
		#interface
		self.l1=Label(
			self.ctl,
			text="Find what",
			anchor="w"
		)
		self.l1.place(x=8,y=8)

		self.e1=Entry(
			self.ctl,
			highlightthickness=0,
			insertborderwidth=2
		)
		self.e1.place(x=100,y=8,width="432",height="24")

		self.l2=Label(
			self.ctl,
			text="Replace with",
			anchor="w"
		)
		self.l2.place(x=8,y=40)

		self.e2=Entry(
			self.ctl,
			highlightthickness=0
		)
		self.e2.place(x=100,y=40,width="432",height="24")

		self.c1_var=IntVar()
		self.c1=Checkbutton(
			self.ctl,
			text="Ignore case",
			variable=self.c1_var
		)
		self.c1.place(x=5,y=90,anchor="w")

		self.c2_var=IntVar()
		self.c2=Checkbutton(
			self.ctl,
			text="Use escape characters (\\n and \\t)",
			variable=self.c2_var
		)
		self.c2.place(x=5,y=110,anchor="w")

		self.b1=Button(
			self.ctl,
			text=" Find",
			image=self.img1,
			compound="left",
			command=self.find,
			anchor="center",
			padx=3
		)
		self.b1.place(x=5,y=130,width=100,height=28)

		self.b2=Button(
			self.ctl,
			text=" Find next",
			image=self.img3,
			compound="left",
			state="disabled",
			command=self.find_next,
			anchor="center",
			padx=3
		)
		self.b2.place(x=112,y=130,width=100,height=28)

		self.b3=Button(
			self.ctl,
			text=" Replace",
			image=self.img4,
			compound="left",
			command=self.replace,
			anchor="center",
			padx=3
		)
		self.b3.place(x=219,y=130,width=100,height=28)

		self.b4=Button(
			self.ctl,
			text=" Replace all",
			image=self.img5,
			compound="left",
			command=self.replace_all,
			anchor="center",
			padx=3
		)
		self.b4.place(x=326,y=130,width=100,height=28)

		self.b5=Button(
			self.ctl,
			text=" Cancel",
			image=self.img2,
			compound="left",
			command=self.cancel,
			anchor="center",
			padx=3
		)
		self.b5.place(x=433,y=130,width=100,height=28)		
		
		self.set_state(0)
		
		self.callback(
			"form5",
			("set_object",self,0,0,0)
		)
		self.e1.focus()
		self.parent.wait_window(self.ctl)
		
		
	def update(self):
		self.ctl.update()

	def cancel(self):
		oldstate=self.state
		self.callback(
			"form5",
			("cancel",0,0,0,0)
		)
		if self.state==0 and oldstate==0:
			self.ctl.destroy()

	def find(self):
		text1=self.e1.get()
		if text1!="":
			self.callback(
				"form5",
				("find",text1,0,self.c1_var.get(),self.c2_var.get())
			)
			
	def find_next(self):
		self.callback(
			"form5",
			("find_next",0,0,0,0)
		)
		
	def replace(self):
		text2=self.e2.get()
		self.callback(
			"form5",
			("replace",0,text2,0,0)
		)
			
	def replace_all(self):
		text2=self.e2.get()
		self.callback(
			"form5",
			("replace_all",0,text2,0,0)
		)
		
	def set_state(self,value):
		#zero state - when fields, checkboxes and the Find button are available;
		#Find next, replace, replace all - not available
		#--------------------------------------------------------------
		#first - the find field, checkboxes and the Find button are disabled, 
		#the replace field, Find next, replace, replace all - available
		#--------------------------------------------------------------
		#second - everything except cancel is unavailable
		self.state=value
		self.e1["state"]=("disabled","normal")[value==0]
		self.e2["state"]=("disabled","normal")[value==0 or value==1]
		self.b1["state"]=("disabled","normal")[value==0]
		self.c1["state"]=("disabled","normal")[value==0]
		self.c2["state"]=("disabled","normal")[value==0]
		self.b2["state"]=("disabled","normal")[value==1]
		self.b3["state"]=("disabled","normal")[value==1]
		self.b4["state"]=("disabled","normal")[value==1]
