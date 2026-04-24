# coding=utf-8

##### IMPORT #####
from tkinter import Canvas,Button,PhotoImage,Tk,Text,Menu,Label,Frame,Entry,Scrollbar
from tkinter.ttk import Sizegrip
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Toplevel
import random
from tkinter import simpledialog
from tkinter import font
from data.mygui import TToolbarSeparator, TToolbarButton, TText, TToolTip
from data.form2 import Form2
from data.form3 import Form3
from data.form4 import Form4
from data.form5 import Form5
import sys
import json
import os
from functools import partial

##### GLOBAL #####
class App(object):
	def __init__(self):
		self.codepage="utf-8"
		self.line_end=chr(13)+chr(10)#lines ending in windows style, i.e. on \r\n
		# are displayed incorrectly. before displaying, you need to replace \r\n with \n,
		# and when writing a file, replace it back
		self.filename="New_file.txt"
		self.apptitle="PyNotepad"
		self.crypt_signature=(chr(0)+chr(1)+chr(2)+"KEY"+chr(2)+chr(1)+chr(0)).encode(self.codepage)
		self.password=""
		self.password_len=0
		self.form2_message=""
		self.file_encrypted=False
		self.command=""
		self.config=dict()
		self.old_win_width=0
		self.old_win_height=0
		
		self.find_index1="1.0"
		self.find_index2="end-1c"
		self.find_text=""#text to search
		self.find_replace_text=""#replacement text
		self.find_nocase=True
		self.find_use_escape_chars=False
		self.find_cancel=False
		
		self.form2=0
		self.form3=0
		self.form4=0
		self.form5=0
app=App()

##### PROCS #####

def callback(sender,message):#to receive data from other forms, sender is the sending form
	if sender=="form2":app.form2_message=message
	if sender=="form3":
		app.config.update(message)
		apply_text_config()
	if sender=="form5":
		need_update=False
		(command,arg1,arg2,arg3,arg4)=message
		win.focus()
		if command=="set_object":
			app.form5=arg1
		if command=="find":
			app.find_cancel=False
			app.find_text=arg1
			app.find_nocase=arg3
			app.find_use_escape_chars=arg4
			if app.find_use_escape_chars:
				app.find_text=replace_escape_chars(app.find_text)
			(app.find_index1,app.find_index2)=find(app.find_text,"1.0",app.find_nocase)
			need_update=True
		if command=="find_next":
			(app.find_index1,app.find_index2)=find(app.find_text,app.find_index2,app.find_nocase)
			need_update=True
		if command=="replace":
			app.find_replace_text=arg2
			if app.find_use_escape_chars:
				app.find_replace_text=replace_escape_chars(app.find_replace_text)
			(app.find_index1,app.find_index2)=replace()
			need_update=True
		if command=="replace_all":
			app.find_replace_text=arg2
			if app.find_use_escape_chars:
				app.find_replace_text=replace_escape_chars(app.find_replace_text)
			app.form5.set_state(2)#disable all controls except cancel
			(app.find_index1,app.find_index2)=replace_all()
			app.form5.set_state(1)
			need_update=True
		if command=="cancel":
			app.find_cancel=True#turn on the cancel flag
			if app.form5.state==1:
				app.form5.set_state(0)
		if need_update:
			if app.find_index2!="":
				app.form5.set_state(1)
			else:
				app.form5.set_state(0)
		
def find(text,index,nocase):
	t1.deselect_text()
	ind1 = t1.search(text, index, nocase=nocase, stopindex="end-1c")
	if ind1!="":
		ind2 = "%s+%dc" % (ind1, len(text))
		t1.select(ind1,ind2)
		return (ind1,ind2)
	else:
		return ("","")

def replace():
	(sel_start,sel_end)=t1.get_selection_range()
	t1.replace(sel_start,sel_end,app.find_replace_text)
	last_ind="%s+%dc" % (sel_start, len(app.find_replace_text))
	(ind1,ind2)=find(app.find_text,last_ind,app.find_nocase)
	return (ind1,ind2)
	
def replace_all():
	app.find_cancel=False#disable the cancel flag
	while True:
		(ind1,ind2)=replace()
		app.form5.update()
		if ind2=="" or app.find_cancel :break
	return (ind1,ind2)
	
def replace_escape_chars(text):
	s = text.replace("\\n","\n")
	s = s.replace("\\t","\t")
	return s

def end(event=None):
	ok=False#not okay yet
	if t1.save_ctl_enable:#if there is something unsaved in the textbox
		ret= confirm_erase_text(app.apptitle)#we warn you that the information will be erased if you close the program
		if ret==False:ok=True#if the user doesn't care, then okay
		if ret==True:#if you care
			ok=savefile()#we suggest saving
			#and okay
		if ret==None: ok=False#if the user clicked cancel - not okay
	else:#if there is nothing unsaved in the textbox
		ok=True#okay then
	if not ok: return
	win.update_idletasks()
	save_config()#save window sizes and coordinates
	win.destroy()
	win.quit()

def win_resize(event=None):
	win.update_idletasks()
	if event.widget is win:
		ww=win.winfo_width()
		wh=win.winfo_height()
		if (ww,wh)!=(app.old_win_width,app.old_win_height):#so that it only works when resizing
			app.old_win_width=ww
			app.old_win_height=wh
			#toolbar
			toolbar.place(x=0, y=0, width=ww, height=30)
			#button "Encrypt"
			bx=ww-30
			b1.place(x=bx,y=1)
			#large text field
			tx=1
			ty=31
			tw=ww-3
			th=wh-55
			t1.place(x=tx, y=ty, width=tw, height=th)
			#statusbar
			sy=ty+th+2
			sw=ww
			sh=wh-th-ty-2
			statusbar.place(x=0, y=sy, width=sw, height=sh)
			#inscryption on the status bar
			l1.place(x=2, y=2, width=sw-32, height=sh-4)
			#resize button (sizegreep)
			sg.place(x=sw-16, y=sh-16, width=16, height=16)
		app.config["x"]=win.winfo_rootx()
		app.config["y"]=win.winfo_rooty()
		app.config["width"]=ww
		app.config["height"]=wh

def new():
	ok=False#not okay yet
	if t1.save_ctl_enable:#if there is something unsaved in the textbox
		ret= confirm_erase_text(app.apptitle+": Creating a new file")#we warn you that the information will be erased,
		# if you create a new file
		if ret==False:ok=True#if the user doesn't care, then okay
		if ret==True:#if you care
			ok=savefile()#we suggest saving
			#and okay
		if ret==None: ok=False#if the user clicked cancel - not okay
	else:#if there is nothing unsaved in the textbox
		ok=True#okay then
	if ok:#if ok
		t1.text=""#clear the textbox
		app.filename="New_file.txt"#reset filename
		app.file_encrypted=False#reset the encryption flag
		app.codepage="utf-8"
		t1.reset_undoredo()#we convince the textbox that it does not need to be saved
		update_win_title()#update the window title

def get_lastdir():
	if os.path.isdir(app.config["lastdir"]):
		return app.config["lastdir"]
	else:
		return os.path.abspath((os.curdir))
		
def openfile(filepath="",cp="",bycommand=False):
	tcp=""#temporary code page
	if cp=="":
		tcp=app.codepage
	else:
		tcp=cp
	lastdir=get_lastdir()
	ok=False#not okay yet
	if t1.save_ctl_enable:#if the textbox wants to be saved
		ret= confirm_erase_text(app.apptitle+": Opening a file")#warn about loss of information
		if ret==False: ok=True#if the user doesn't care, then okay
		if ret==True:#if the user chose to save
			ok=savefile()#suggest saving
			#and after that it’s okay
		if ret==None: ok=False#if the user clicked cancel - not okay
	else:#if there is nothing unsaved in the textbox
		ok=True#okay then
	if ok:#if ok
		if filepath=="":#if this is not opening a file from Command when starting the program
			filepath = str(filedialog.askopenfilename(initialdir=lastdir))##request file name to open
		if filepath!="" and filepath!="()":#if the user entered something or there was already something there
			try:#trying is not torture
				file=open(filepath, "rb")#trying to open the file for reading
				if not bycommand:#if this is not opening a file from Command when starting the program
					lastdir=os.path.dirname(filepath)
					app.config["lastdir"]=lastdir
				t=file.read()#read bytes
				file.close()#close the file
				if is_text_encrypted(t):#if the file is encrypted
					app.form2=Form2(win,callback,appimg)#request password
					if app.form2_message==chr(0) or app.form2_message=="":#if the user refused or did not enter anything
						return#let's go out
					else:#if you haven't refused
						psw=app.form2_message.encode(tcp)#save his nonsense as a temporary password
						t=t[len(app.crypt_signature):]#cut off the signature of the encrypted file from the text
						t2=encrypt(t,psw)#decoding
						if is_correct_key(t2,psw):#if the user was able to guess the password
							t2=delete_key_from_text(t2,psw)#remove it from the text
							if cp=="":
								s=mydecode(t2,filepath)#detect encoding and decode
								if s==False: return#if an error occurred during decoding, exit
							else:
								try:
									s=t2.decode(tcp)
									app.codepage=tcp
								except:
									messagebox.showerror(app.apptitle, "Can't decode file "+filepath)#say it didn't work out
									return
							app.password=psw.decode(tcp)#remember like a real password for
							# save the file later
							app.file_encrypted=True#remember that we are working with an encrypted file
						else:#if the user didn't guess correctly
							messagebox.showerror(app.apptitle, "Password is incorrect")#tell him he was wrong
							return#let's go out
				else:#if the file was not encrypted
					if cp=="":
						s=mydecode(t,filepath)#detect encoding and decode
						if s==False: return#if an error occurred during decoding, exit
					else:
						try:
							s=t.decode(tcp)
							app.codepage=tcp
						except:
							messagebox.showerror(app.apptitle, "Can't decode file "+filepath)#say it didn't work out
							return
					app.file_encrypted=False#reset the encryption flag
				if "\r\n" in s:#if lines end in windows style
					app.line_end="\r\n"#remember this information
					s=s.replace("\r\n","\n")#change for a new one
				else:
					app.line_end="\n"
				t1.text=s#display text
				app.filename=filepath#write the address in filename
				t1.reset_undoredo()#tell the textbox that it saved everything and doesn’t want it anymore
				update_win_title()#update the window title
			except:#didn't work out
				messagebox.showerror(app.apptitle, "Can't open file "+filepath)#say it didn't work out

def mydecode(bytestring, filepath):
	try:
		t=bytestring.decode("utf-8")
		app.codepage="utf-8"
		return t
	except:
		try:
			t=bytestring.decode("unicode_internal")
			app.codepage="unicode"
			return t
		except:
			try:
				t=bytestring.decode("1251")
				app.codepage="1251"
				return t
			except:
				messagebox.showerror(app.apptitle, "Can't decode file "+filepath)#say it didn't work out
				return False

def savefile(saveas=False,cp=""):
	if cp=="":
		cp=app.codepage
	lastdir=get_lastdir()
	if app.filename=="New_file.txt" or saveas:#if the name has not yet been set or needs to be saved under a new name
		filepath = str(filedialog.asksaveasfilename(initialdir=lastdir))#request it
		if filepath!="" and filepath!="()":#if the user wrote something
			if len(filepath)>3:#if I wrote more than 3 characters
				ext=filepath[-4:].upper()#take the last 4 characters
				if ext!=".TXT": filepath=filepath+".txt"#if this is not .TXT, then add .txt at the end
			else:#if I wrote less than 4 characters
				filepath=filepath+".txt"#attribute .txt to them
		else:#if the user pressed cancel
			return False#return FALSE and exit
	else:#if the name is already set
		filepath=app.filename#copy it to filepath
	try:#trying is not torture
		file=open(filepath, "wb")#open the file
		s=t1.text#read the contents of the textbox
		if app.line_end=="\r\n":#if necessary
			s=s.replace("\n","\r\n")#restore the ends of lines
		if app.file_encrypted:#if we are working with an encrypted file
			try:
				t2=s.encode(cp)#convert text to bytes
			except:
				messagebox.showerror(app.apptitle, "Can't encode text with codepage "+app.codepage)#say it didn't work out
				file.close()
				return False
			psw=app.password.encode(cp)#and the password too
			t2=insert_key_in_text(t2,psw)#insert password into text
			t2=encrypt(t2,psw)#encrypt
			t2=app.crypt_signature+t2#add signature
			file.write(t2)#write to file
		else:#if the file is not encrypted
			try:
				t2=s.encode(cp)
			except:
				messagebox.showerror(app.apptitle, "Can't encode text with codepage "+cp)#say it didn't work out
				file.close()
				return False
			file.write(t2)#write to it from a variable
		file.close()#closing
		app.codepage=cp#update the code page
		app.filename=filepath#if there was nothing in filename, write from filepath
		t1.save_ctl_enable=False#tell the textbox that it saved everything and doesn’t want it anymore
		update_win_title()#update the window title
		controls_update()#updating the "save" button
		return True
	except:#didn't work out
		messagebox.showerror(app.apptitle, "Can't open file "+filepath)#say it didn't work out
		return False
		
def savefileas():
	savefile(True)

def confirm_erase_text(title_text="Confirmation"):
	ret = messagebox.askyesnocancel(title_text, "The editor contains unsaved text. Do you want to save it to disk?")
	return ret
	
def is_text_encrypted(text):
	return (False,True)[text[:9]==app.crypt_signature]

def is_correct_key(text,key):
	return (False,True)[key in text]
	
def insert_key_in_text(text,key):
	key_pos=text.find(key)#check whether the word that is the password is already in the text. well, suddenly)
	if key_pos==-1:#if not
		i=len(text)#we can insert the password anywhere in the text
	else:#if yes
		i=key_pos#we can insert before this found word
	random.seed()#random!!!
	r=random.randint(1,i+1)#choose a random position
	t=text[:r-1]+key+text[r-1:]#stick
	return t
	
def delete_key_from_text(text,key):
	key_pos=text.find(key)
	t=text[:key_pos]+text[key_pos+len(key):]
	return t

def set_encrypt_mode():
	if not app.file_encrypted:
		app.form2=Form2(win,callback,appimg,"new")
		if app.form2_message==chr(0) or app.form2_message=="":return
		app.password=app.form2_message
		app.password_len=len(app.password)
		app.file_encrypted=True
		t1.save_ctl_enable=True
	else:
		app.form2=Form2(win,callback,appimg,"remove")
		if app.form2_message==chr(0) or app.form2_message=="":return
		psw=app.form2_message
		if psw==app.password:
			app.password=""
			app.password_len=0
			app.file_encrypted=False
			t1.save_ctl_enable=True
	controls_update()

def controls_update(event=None):
	tb4.enable=t1.undo_enable
	tb5.enable=t1.redo_enable
	edit_menu.entryconfigure("Undo",state=("disabled","normal")[t1.undo_enable])
	edit_menu.entryconfigure("Redo",state=("disabled","normal")[t1.redo_enable])
	
	tb6.enable=t1.selection_ctl_enable
	tb7.enable=t1.selection_ctl_enable
	tb9.enable=t1.selection_ctl_enable
	edit_menu.entryconfigure("Cut",state=("disabled","normal")[t1.selection_ctl_enable])
	edit_menu.entryconfigure("Copy",state=("disabled","normal")[t1.selection_ctl_enable])
	edit_menu.entryconfigure("Delete",state=("disabled","normal")[t1.selection_ctl_enable])
	c_menu.entryconfigure("Cut",state=("disabled","normal")[t1.selection_ctl_enable])
	c_menu.entryconfigure("Copy",state=("disabled","normal")[t1.selection_ctl_enable])
	
	tb3.enable=t1.save_ctl_enable
	file_menu.entryconfigure("Save",state=("disabled","normal")[t1.save_ctl_enable])
	update_win_title()
	
	b1.img=(img4,img25)[app.file_encrypted]
	tooltip.set_text(b1.ctl,("Enable encryption","Disable encryption")[app.file_encrypted])
	l1["text"]=("Not encrypted","Encrypted")[app.file_encrypted]
	l1["text"]="Code page: "+app.codepage+"  "+l1["text"]
	l1["foreground"]=("red","green")[app.file_encrypted]

def update_win_title():
	s=("","*")[t1.save_ctl_enable]
	win.title(s+app.filename+" - "+app.apptitle)
	
def show_context_menu(event):
	c_menu.tk_popup(event.x_root, event.y_root)

def encrypt(text,key):#bytes in and bytes out. and encrypts and decrypts
	if len(key)==0:
		return text
	cur=0
	s=bytes()
	for i in range(0,len(text)):
		cur+=1
		n=256-(text[i]+key[cur-1])
		if n<0:n+=256
		if cur==len(key):cur=0
		s=s+bytes([n])
	return s

def show_settings(event=None):
	tconfig=app.config
	app.form3=Form3(win,callback,appimg,tconfig)
	
def show_search(event=None):
	app.form5=Form5(win,callback,appimg)
	
def show_about():
	app.form4=Form4(win,callback,appimg)

def load_config():
	r=dict()
	try:
		with open("config.json", "r") as f:
			r = json.load(f)
	except:
		r["x"]=100
		r["y"]=100
		r["width"]=640
		r["height"]=480
		r["font_family"]="font"
		r["font_size"]=10
		r["font_bold"]=0
		r["font_italic"]=0
		r["text_bgcolor"]="#ffffff"
		r["text_color"]="#000000"
		r["highlight_bgcolor"]="RoyalBlue"
		r["highlight_color"]="#ffffff"
		r["show_numbers"]=1
		r["lastdir"]=""
		r["dx"]=-1
		r["dy"]=-1
	return r
	
def save_config():
	with open("config.json", "w") as f:
		json.dump(app.config, f, indent=4,sort_keys=True)
	return
	
def apply_text_config():
	t1.font_family=app.config["font_family"]
	t1.font_size=app.config["font_size"]
	t1.font_bold=app.config["font_bold"]
	t1.font_italic=app.config["font_italic"]
	t1.show_numbers=app.config["show_numbers"]
	t1.text_color=app.config["text_color"]
	t1.text_bgcolor=app.config["text_bgcolor"]
	t1.highlight_color=app.config["highlight_color"]
	t1.highlight_bgcolor=app.config["highlight_bgcolor"]

def passproc(event=None):
	pass
	
##### MAIN WINDOW #####
win = Tk()
win.title("My Notepad")
try: app.command=sys.argv[1] #trying to get the command line
except: pass #it ​​didn’t work out, oh well
appimg=PhotoImage(file="data/img/note.png")
win.iconphoto(False, appimg)
app.config=load_config()#read the configuration

tooltip=TToolTip(win)

# ##### TEXTBOX AND SCROLLBARS #####
t1=TText(win,0,0,1,1,controls_update,show_context_menu)

# ##### IMAGE LOADING #####
img1 =  PhotoImage(file="data/img/page.png")
img2 =  PhotoImage(file="data/img/open.png")
img3 =  PhotoImage(file="data/img/save.png")
img4 =  PhotoImage(file="data/img/key.png")
img5 =  PhotoImage(file="data/img/undo.png")
img6 =  PhotoImage(file="data/img/redo.png")
img7 =  PhotoImage(file="data/img/cut.png")
img8 =  PhotoImage(file="data/img/copy.png")
img9 =  PhotoImage(file="data/img/paste.png")
img10 =  PhotoImage(file="data/img/delete.png")

img25=PhotoImage(file="data/img/key_del.png")
img26=PhotoImage(file="data/img/settings2.png")
img27=PhotoImage(file="data/img/search.png")

img31=PhotoImage(file="data/img/m_page.png")
img32=PhotoImage(file="data/img/m_open.png")
img33=PhotoImage(file="data/img/m_save.png")
img34=PhotoImage(file="data/img/m_save_as.png")
img35=PhotoImage(file="data/img/m_settings2.png")

img41=PhotoImage(file="data/img/m_paste.png")
img42=PhotoImage(file="data/img/m_cut.png")
img43=PhotoImage(file="data/img/m_copy.png")
img44=PhotoImage(file="data/img/m_undo.png")
img45=PhotoImage(file="data/img/m_redo.png")
img46=PhotoImage(file="data/img/m_search.png")
img47=PhotoImage(file="data/img/m_delete.png")

img50=PhotoImage(file="data/img/m_app.png")
# ##### MENU #####
main_menu = Menu(
	activebackground="RoyalBlue",
	activeforeground="white",
	activeborderwidth=0
)

menu_config={
	"tearoff":0,
	"activebackground":"RoyalBlue",
	"activeforeground":"white",
	"activeborderwidth":1,
	"background":"white",
	"foreground":"black",
	"relief":"flat",
	"borderwidth":3
}

encoding_menu1 = Menu(**menu_config)
encoding_menu2 = Menu(**menu_config)
popular_encs = ["utf-8","utf-8-sig","utf-16","utf-32","-",
				"ascii","cp1251","cp1252","-",
				"iso-8859-5","koi8-r","cp437","cp866","-",
				"mac_roman","mac_cyrillic"]

for enc in popular_encs:
	if enc!="-":
		encoding_menu1.add_command(
			label=enc, 
			command=partial(openfile,"",enc,False)
		)
		encoding_menu2.add_command(
			label=enc, 
			command=partial(savefile,True,enc)
		)
	else:
		encoding_menu1.add_separator()
		encoding_menu2.add_separator()

file_menu = Menu(**menu_config)

file_menu.add_command(
	label="New",
	image=img31,
	compound="left",
	accelerator="Ctrl+N",
	command=new
)
file_menu.add_command(
	label="Open",
	image=img32,
	compound="left",
	accelerator="Ctrl+O",
	command=openfile
)
file_menu.add_cascade(
	label="Open with encoding", 
	menu=encoding_menu1
)
file_menu.add_command(
	label="Save",
	image=img33,
	compound="left",
	accelerator="Ctrl+S",
	command=savefile
)
file_menu.add_command(
	label="Save as",
	image=img34,
	compound="left",
	command=savefileas
)
file_menu.add_cascade(
	label="Save with encoding", 
	menu=encoding_menu2
)
file_menu.add_separator()
file_menu.add_command(
	label="Settings",
	image=img35,
	compound="left",
	accelerator="Alt+F12",
	command=show_settings
)
file_menu.add_separator()
file_menu.add_command(
	label="Exit",
	compound="left",
	command=end
)

edit_menu = Menu(**menu_config)

edit_menu.add_command(
	label="Undo",
	image=img44,
	state="disabled",
	compound="left",
	accelerator="Ctrl+Z",
	command=t1.undo
)
edit_menu.add_command(
	label="Redo",
	image=img45,
	state="disabled",
	compound="left",
	accelerator="Ctrl+Y",
	command=t1.redo
)
edit_menu.add_separator()
edit_menu.add_command(
	label="Cut",
	image=img42,
	compound="left",
	accelerator="Ctrl+X",
	command=t1.cut
)
edit_menu.add_command(
	label="Copy",
	image=img43,
	compound="left",
	accelerator="Ctrl+C",
	command=t1.copy
)
edit_menu.add_command(
	label="Paste",
	image=img41,
	compound="left",
	accelerator="Ctrl+V",
	command=t1.paste
)
edit_menu.add_command(
	label="Delete",
	image=img47,
	compound="left",
	command=t1.delete
)
edit_menu.add_separator()
edit_menu.add_command(
	label="Search and replace",
	image=img46,
	compound="left",
	accelerator="Ctrl+F",
	command=show_search
)

help_menu = Menu(**menu_config)

help_menu.add_command(
	label="About",
	image=img50,
	compound="left",
	command=show_about
)

main_menu.add_cascade(label="File", menu=file_menu)
main_menu.add_cascade(label="Edit", menu=edit_menu)
main_menu.add_cascade(label="Help", menu=help_menu)

win.config(menu=main_menu)

if app.config["dx"]==-1 and app.config["dy"]==-1:
	win.geometry("640x480+0+0")
	win.update_idletasks()
	app.config["dx"]=win.winfo_rootx()
	app.config["dy"]=win.winfo_rooty()
win.geometry(
	str(app.config["width"])+
	"x"+
	str(app.config["height"])+
	"+"+
	str(app.config["x"]-app.config["dx"])+
	"+"+
	str(app.config["y"]-app.config["dy"])
)

win.update_idletasks()
apply_text_config()

##### CONTEXT MENU #####
c_menu=Menu(**menu_config)

c_menu.add_command(
	label="Cut",
	image=img42,
	compound="left",
	accelerator="Ctrl+X",
	command=t1.cut
)
c_menu.add_command(
	label="Copy",
	image=img43,
	compound="left",
	accelerator="Ctrl+C",
	command=t1.copy
)
c_menu.add_command(
	label="Paste",
	image=img41,
	compound="left",
	accelerator="Ctrl+V",
	command=t1.paste
)
c_menu.add_separator()
c_menu.add_command(
	label="Select all",
	accelerator="Ctrl+A",
	command=t1.select_all
)

##### TOOLBAR #####
toolbar = Frame(win)
cur=1
tb1=TToolbarButton(toolbar, cur,1,img1, new)
cur+=30
tb2=TToolbarButton(toolbar,cur,1, img2, openfile)
cur+=30
tb3=TToolbarButton(toolbar, cur,1,img3, savefile)
cur+=30
c1=TToolbarSeparator(toolbar,cur,7)
cur+=5
tb4=TToolbarButton(toolbar,cur,1, img5, t1.undo)
cur+=30
tb5=TToolbarButton(toolbar,cur,1, img6, t1.redo)
cur+=30
c2=TToolbarSeparator(toolbar,cur,7)
cur+=5
tb11=TToolbarButton(toolbar,cur,1, img27, show_search)
cur+=30
c4=TToolbarSeparator(toolbar,cur,7)
cur+=5
tb6=TToolbarButton(toolbar,cur,1, img7, t1.cut)
cur+=30
tb7=TToolbarButton(toolbar, cur,1,img8, t1.copy)
cur+=30
tb8=TToolbarButton(toolbar, cur,1,img9, t1.paste)
cur+=30
tb9=TToolbarButton(toolbar, cur,1,img10, t1.delete)
cur+=30
c3=TToolbarSeparator(toolbar,cur,7)
cur+=5
tb10=TToolbarButton(toolbar, cur,1,img26, show_settings)
b1=TToolbarButton(toolbar,400,1,img4,set_encrypt_mode)

tooltip.register_tooltip(tb1.ctl,"Create new file")
tooltip.register_tooltip(tb2.ctl,"Open file")
tooltip.register_tooltip(tb3.ctl,"Save file")
tooltip.register_tooltip(tb4.ctl,"Undo")
tooltip.register_tooltip(tb5.ctl,"Redo")
tooltip.register_tooltip(tb6.ctl,"Cut selected text to clipboard")
tooltip.register_tooltip(tb7.ctl,"Copy selected text to clipboard")
tooltip.register_tooltip(tb8.ctl,"Paste text from clipboard")
tooltip.register_tooltip(tb9.ctl,"Delete selected text")
tooltip.register_tooltip(tb10.ctl,"Settings")
tooltip.register_tooltip(tb11.ctl,"Find and replace")
tooltip.register_tooltip(b1.ctl,"text1")

##### STATUSBAR #####
statusbar = Frame(win)
l1=Label(statusbar,text="Ok",anchor="w")
sg=Sizegrip(statusbar)

##### EVENTS #####
win.bind("<Control-q>", end)
win.bind("<Configure>", win_resize)
win.bind("<Alt-F12>", show_settings)
win.bind("<Control-f>", show_search)

win.event_generate("<Configure>")
######################
if app.command!="":
	openfile(app.command,"",True)
else:
	new()
controls_update()

##### MAINLOOP #####
win.minsize(640, 480)
win.protocol('WM_DELETE_WINDOW', end)
win.mainloop()
