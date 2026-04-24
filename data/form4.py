from tkinter import Toplevel,PhotoImage,Label,Frame
import webbrowser

class Form4(object):
	def __init__(self,parent,callback,icon,args="open"):
		self.callback=callback
		self.parent=parent
		self.ctl=Toplevel(
			self.parent,
			bg="white"
		)
		self.ctl.iconphoto(False, icon)
		self.ctl.title("About")
		w=500
		h=188
		x=(self.ctl.winfo_screenwidth()-w)//2
		y=(self.ctl.winfo_screenheight()-h)//2
		self.ctl.geometry(str(w)+"x"+str(h)+"+"+str(x)+"+"+str(y))
		self.ctl.resizable(False, False)
		self.ctl.transient(self.parent)
		self.ctl.grab_set()
		
		self.img=PhotoImage(file="data/img/py.png")
		l1=Label(
			self.ctl,
			image=self.img,
			bg="white"
		)
		l1.place(x=0,y=0)
		l2=Label(
			self.ctl,
			text="Text editor with file encription capability.",
			bg="white",
			justify="center"
		)
		l2.place(x=190,y=50,width=310)
		l3=Label(
			self.ctl,
			text="by Serж",
			bg="white",
			justify="center"
		)
		l3.place(x=190,y=80,width=310)
		f1=Frame(
			self.ctl,
			bg="white"
		)
		f1.place(x=190,y=110,width=310)
		l4=Label(
			f1,
			text="github.com/I-found-a-computer/PyNotepad",
			bg="white",
			justify="center",
			fg="blue",
			cursor="hand2"
		)
		l4.pack()
		l4.bind("<Button-1>",self.mail)
		self.ctl.focus()
		self.parent.wait_window(self.ctl)
		
	def mail(self,event=None):
		webbrowser.open_new("https://github.com/I-found-a-computer/PyNotepad")
