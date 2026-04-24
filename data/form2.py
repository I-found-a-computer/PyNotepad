from tkinter import Toplevel,Label,Entry,Button,PhotoImage

class Form2(object):
	def __init__(self,parent,callback,icon,args="open"):
		self.callback=callback
		self.parent=parent
		self.ctl=Toplevel(self.parent)
		self.ctl.iconphoto(False, icon)
		self.ctl.title("Password")
		w=300
		h=120
		x=(self.ctl.winfo_screenwidth()-w)//2
		y=(self.ctl.winfo_screenheight()-h)//2
		self.ctl.geometry(str(w)+"x"+str(h)+"+"+str(x)+"+"+str(y))
		self.ctl.resizable(False, False)
		self.ctl.transient(self.parent)
		self.ctl.grab_set()
		self.img1=PhotoImage(file="data/img/ok.png")
		self.img2=PhotoImage(file="data/img/cancel.png")
		#interface
		if args=="new":
			lt="The file is not encrypted.\nEnter a password to encrypt"
		elif args=="open":
			lt="The file is encrypted.\nEnter the password to open the file"
		else:
			lt="The file is encrypted.\nEnter the correct password to disable encryption"
		self.l1=Label(self.ctl,text=lt)
		self.l1.place(width=w,height=48,x=0,y=0)
		self.e1=Entry(self.ctl,justify="center")
		self.e1.place(width=w-16,height=24,x=8,y=50)
		self.b1=Button(
			self.ctl,
			text="  Ok",
			command=self.ok,
			image=self.img1,
			compound="left",
			anchor="center",
			padx=3,
			activebackground="white",
			borderwidth="2"
		)
		self.b1.place(width=100,height=28,x=8,y=85)
		self.b2=Button(
			self.ctl,
			text="  Cancel",
			command=self.cancel,
			image=self.img2,
			compound="left",
			anchor="center",
			padx=3
		)
		self.b2.place(width=100,height=28,x=192,y=85)
		self.e1.focus()
		self.parent.wait_window(self.ctl)
		
	def ok(self):
		self.callback("form2",self.e1.get())
		self.ctl.destroy()
		
	def cancel(self):
		self.callback("form2",chr(0))
		self.ctl.destroy()
