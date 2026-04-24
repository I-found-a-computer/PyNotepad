from tkinter import Canvas,Button,Text,Scrollbar,Toplevel,Frame,font,ttk

class TToolbarSeparator(object):
	def __init__(self,container,x,y):
		self.ctl=Canvas(container, width=5,height=18,bd=0,highlightthickness=0)
		self.ctl.place(x=x,y=y,width=5,height=18)
		self.ctl.create_line(1,0,1,20,fill="white")
		self.ctl.create_line(2,0,2,20,fill="LightCyan3")

#================================================================================

class TToolbarButton(object):
	def __get_enable(self):
		return self._enable

	def __set_enable(self, new_value):
		self._enable = new_value
		self.ctl["state"]=("disabled","normal")[self._enable]
		if not self._enable: 
			self.on_leave(event=None)

	enable = property(__get_enable, __set_enable)
	
	def __get_img(self):
		return self.ctl["image"]

	def __set_img(self, new_img):
		self.ctl["image"] = new_img

	img = property(__get_img, __set_img)

	def on_enter(self,event=None):
		if self.ctl["relief"]=="groove" or not self.enable:return
		self.ctl["relief"]="groove"   
		

	def on_leave(self,event=None):
		if self.ctl["relief"]=="flat": return
		self.ctl["relief"]="flat"
		

	def place(self,**kwargs):
		self.ctl.place(kwargs)
		
	def __init__(self, container, x, y, img, command):
		self.ctl=Button(container)
		self._enable=True
		self.ctl["image"]=img
		self.ctl["relief"]="flat"
		self.ctl["anchor"]="center"
		self.ctl["command"]=command
		
		self.ctl["background"]=self.ctl.master.cget("background")
		
		self.ctl.bind('<Enter>', self.on_enter)
		self.ctl.bind('<Leave>', self.on_leave)
		self.ctl.place(x=x,y=y,width=29,height=29)

#================================================================================

class TText(Text):
	def place(self,**kwargs):
		yw=self._ys.winfo_width()
		xh=self._xs.winfo_height()
		self._ys.place(x=kwargs["x"]+kwargs["width"]-yw, y=kwargs["y"], height=kwargs["height"]-xh)
		self._xs.place(x=kwargs["x"],y=kwargs["y"]+kwargs["height"]-xh,width=kwargs["width"]-yw)
		self.ctl.place(
			x=kwargs["x"]+self.line_counter_width, 
			y=kwargs["y"], 
			width=kwargs["width"]-yw-self.line_counter_width, 
			height=kwargs["height"]-xh
		)
		self.line_counter.place(
			x=kwargs["x"], 
			y=kwargs["y"],
			height=kwargs["height"]-xh,
			width=self.line_counter_width
		)
		self.ctl.focus()
		
		self.line_counter_redraw()
		self._x=kwargs["x"]
		self._y=kwargs["y"]
		self._width=kwargs["width"]
		self._height=kwargs["height"]
	
	def __get_enable(self):
		return self.ctl_enable

	def __set_enable(self, new_value):
		self.ctl_enable = new_value
		self.ctl["state"]=("disabled","normal")[self.ctl_enable]

	enable = property(__get_enable, __set_enable)
	
	def __init__(self,container,x,y,width,height,controls_update_proc,context_menu_proc):
		self._x=x
		self._y=y
		self._width=width
		self._height=height
		self._container=container
		self.undo_enable=False
		self.redo_enable=False
		self.selection_ctl_enable=False
		self.save_ctl_enable=False
		self.controls_update_proc=controls_update_proc
		self.context_menu_proc=context_menu_proc
		self._text_color="#000000"
		self._text_bgcolor="#ffffff"
		self._highlight_color="#000000"
		self._highlight_bgcolor="#aaaaaa"
		self._font_family="courier"
		self._font_size=10
		self._font_bold=0
		self._font_italic=0
		self._font_string="courier 10"
		self._font=font.Font(family="courier", size=10, weight="normal",slant="roman")
		self.last_linenum=""
		self._show_numbers=1
		self.old_numbers=[]
		self.linenumber_widgets=[]
		self.char_width=1
		self.old_line_count=-1
		self.line_counter_width=1#calculate the width of the line number field
		self.line_counter=Canvas(container, width=self.line_counter_width,height=height,bd=0,\
			highlightthickness=0,cursor="right_ptr")
		self.ctl=Text(
			self._container,
			wrap="none",
			undo="false",
			font=self._font_family+" "+str(self._font_size),
			pady=3,
			padx=5,
			highlightthickness=0
		)
		self._orig = self.ctl._w + "_orig"
		self._container.tk.call("rename", self.ctl._w, self._orig)
		self._container.tk.createcommand(self.ctl._w, self._proxy)
		self._undo_stack = []
		self._redo_stack = []
		#events
		self.ctl.bind("<Control-z>",self.undo)
		self.ctl.bind("<Control-y>",self.redo)
		self.ctl.bind("<Control-v>",self.paste)
		self.ctl.bind("<Control-x>",self.cut)
		self.ctl.bind("<Control-a>", self.select_all)
		self.ctl.bind("<ButtonRelease-1>", self.check_selection)
		self.ctl.bind("<Button-3>", self.context_menu_proc)
		self.ctl.bind("<<TextModified>>",self.text_modified)
		self.ctl.bind("<<LineCountChange>>",self.line_counter_redraw)
		#scrollbars
		self._ys = ttk.Scrollbar(self._container,orient = "vertical", command = self.myscroll)
		self._xs = ttk.Scrollbar(self._container,orient = "horizontal", command = self.ctl.xview)		
		self.ctl.config(yscrollcommand=self.myset,xscrollcommand=self._xs.set)
		self._ys.place(x=0,y=0)
		self._xs.place(x=0,y=0)
		#line number field
		self.line_counter.bind("<B1-Motion>",self.select_lines)
		self.line_counter.bind("<Button-1>",self.begin_select)
		self.line_counter.bind("<ButtonRelease-1>",self.finish_select)
		#accommodation
		self.place(x=x,y=y,width=width,height=height)
		self.ctl_enable=True
		self.enable=self.ctl_enable
	
	def myscroll(self,proc,arg1,arg2=""):#for drawing line names
		if proc=="scroll":self.ctl.yview_scroll(arg1,arg2)
		if proc=="moveto":self.ctl.yview_moveto(arg1)
		self.line_counter_redraw()
		
	def myset(self,arg1,arg2):#for drawing line names
		self._ys.set(arg1,arg2)
		self.line_counter_redraw()
		
	def text_modified(self,event=None):
		self.save_ctl_enable=True
		self.update()
		
	def update(self,event=None):
		self.undo_enable=len(self._undo_stack)!=0
		self.redo_enable=len(self._redo_stack)!=0
		self.controls_update_proc()#procedure for updating the availability of external controls
		
	def check_selection(self,event=None):
		self.selection_ctl_enable=(len(self.ctl.tag_ranges("sel"))!=0)
		self.controls_update_proc()#procedure for updating the availability of external controls
		
	def _proxy(self, command, *args):
		modified=False;linecount_changed=False# preparing event indicators
		#handling calls that lead to an error, I don’t know where they come from :\
		if command == "get" and (args[0] == "sel.first" and args[1] == "sel.last") \
			and not self.ctl.tag_ranges('sel'): return
		if command == "delete" and (args[0] == "sel.first" and args[1] == "sel.last") \
			and not self.ctl.tag_ranges('sel'): return
		#undo redo subclassing
		if command in ["insert", "delete","replace"]:
			modified=True#we say that the text has changed anyway
			if args[0] == "end":#find the first index for all commands
				index = self.ctl.index("end-1c")
			else:
				index = self.ctl.index(args[0])
			if command == "insert":#always two arguments: index and character string
				s=args[1]#we pick out the line that needs to be inserted
				undo_args = ("delete", index, "{}+{}c".format(index, len(s)))#form undo
				redo_args=("insert", index, s)#forming redo
			if command=="delete":#can be one or two arguments
				if len(args)==1:#if there is only one argument, then only one character is removed
					i2=self.ctl.index(index+"+1c")#get its index
				else:#if two, then several characters are removed
					i2=self.ctl.index(args[1])#get the index of the symbol up to which they are removed
				s=self.ctl.get(index,i2)#get the line, cat. we will delete
				undo_args=("insert", index, s)#form undo
				redo_args=("delete", index,i2)#forming redo
			if command=="replace":#always three arguments: start index; index to which; and string
				i2=self.ctl.index(args[1])#get the second argument
				s=self.ctl.get(index,i2)#get the string
				undo_args=("replace",index,"{}+{}c".format(index,len(args[2])),s)#form undo
				redo_args=("replace",index,i2,args[2])#forming redo
				if "/n" in args[2]:linecount_changed=True#if the replacement string contains "ends of lines"
			if "\n" in s:linecount_changed=True#or the character being inserted or removed is "end of line"
			#or there were “ends of lines” in the line being replaced, which means you will need to redraw the line names
			self._redo_stack.clear()#clear the redo stack
			self._undo_stack.append((undo_args, redo_args))#add the undo stack
			if len(self._undo_stack)>64:self._undo_stack=self._undo_stack[1:]#if it's too long, shorten it
		#further processing and generation of events
		cmd = (self._orig, command) + args#forming a team
		result = self._container.tk.call(cmd)#carrying out
		if modified:self.ctl.event_generate("<<TextModified>>")#honk if necessary
		if linecount_changed:self.ctl.event_generate("<<LineCountChange>>")#and here
		return result
		
	def delete(self, event=None):
		self.ctl.delete("sel.first", "sel.last")
		return "break"
        
	def cut(self,event=None):
		self.ctl.event_generate("<<Cut>>")
		self.line_counter_redraw()
		return "break"

	def copy(self,event=None):
		self.ctl.event_generate("<<Copy>>")
		return "break"

	def paste(self,event=None):
		try:#if something has been selected, it must first be deleted and then pasted from the buffer
			(sel_start,sel_end)=self.get_selection_range()
			seltext=self.get(sel_start,sel_end)
			self.ctl.delete("sel.first", "sel.last")
		except:
			pass
			
		self.ctl.event_generate("<<Paste>>")
		self.ctl.see("insert")
		return "break"
		
	def select_all(self,event=None):
		self.ctl.tag_add("sel", "1.0", "end-1c")
		self.ctl.mark_set("insert", "1.0")
		self.ctl.see("insert")
		return "break"
	
	def undo(self,event=None):
		if not self._undo_stack:return
		undo_args, redo_args = self._undo_stack.pop()
		self._redo_stack.append((undo_args, redo_args))
		self.ctl.tk.call((self._orig,) + undo_args)
		self.ctl.event_generate("<<TextModified>>")
		self.line_counter_redraw()
		return "break"

	def redo(self,event=None):
		if not self._redo_stack:return
		undo_args, redo_args = self._redo_stack.pop()
		self._undo_stack.append((undo_args, redo_args))
		self.ctl.tk.call((self._orig,) + redo_args)
		self.ctl.event_generate("<<TextModified>>")
		self.line_counter_redraw()
		return "break"
		
	def __get_text(self):
		return self.ctl.get("1.0", "end-1c")
	
	def __set_text(self,new_text):
		self.ctl.delete("1.0", "end")
		self.ctl.insert("1.0", new_text)
		
	text = property(__get_text, __set_text)
	
	def reset_undoredo(self):
		self._redo_stack.clear()#clear the redo stack
		self._undo_stack.clear()#clear undo stack
		self.save_ctl_enable=False
		self.update()
			
	def linenumbers(self):
		ret=[]
		i=self.ctl.index("@0,0")
		while True :
			dline=self.ctl.dlineinfo(i)#take information about the string
			if dline is None: break#if the line is not visible - exit
			y = dline[1]#take the Y coordinate
			linenum = " "+str(i).split(".")[0]+" "#take the line number
			ret.append((linenum,y))
			i = self.ctl.index("%s+1line" % i)#take the next line
		return ret
		
	def line_counter_redraw(self,event=None):
		if not self._show_numbers:return
		chindren=self.line_counter.find_all()
		numbers=self.linenumbers()
		if numbers==self.old_numbers: return	
		last_linenum=numbers[len(numbers)-1][0]#last line number
		linenum_width=len(last_linenum)*self.char_width
		
		if linenum_width!=self.line_counter_width:#if the line counter width has changed
			self.last_linenum=last_linenum
			self.line_counter_width=linenum_width
			self.place(x=self._x,y=self._y,width=self._width,height=self._height)#apply
			
		if len(numbers)>len(chindren): #if the number of lines has changed upward
			i=len(numbers)-len(chindren)
			for j in range(i):
				self.line_counter.create_text(0,0,text="")#preparing widget for line number
			chindren=self.line_counter.find_all()

		for i in range(len(chindren)):
			if i<len(numbers):
				linenum=numbers[i][0]
				self.line_counter.coords(chindren[i], self.line_counter_width, numbers[i][1])
				self.line_counter.itemconfigure(
					chindren[i],
					anchor="ne",
					text=linenum,
					font=self._font_string,
					fill=self._highlight_color
				)
			else:
				self.line_counter.coords(chindren[i], 0, 0)
				self.line_counter.itemconfigure(
					chindren[i],
					anchor="nw",
					text=""
				)

		self.old_linenumbers=numbers
			
	def select_lines(self,event=None):
		y=event.y
		i=self.ctl.index("@0,%s" % y)#take the line, cat. located at the Y coordinate
		i=str(i).split(".")[0]#take the line number
		self.select_one_line(i)#highlight her
            
	def deselect_text(self,event=None):
		self.ctl.tag_remove("sel","1.0","end")#reset selection
    
	def select_one_line(self,line_index):#select a line
		self.ctl.tag_add("sel", line_index+".0", line_index+".0"+"+1line-1c")
		self.ctl.mark_set("insert", line_index+".0"+"+1line-1c")
	
	def begin_select(self,event=None):
		self.deselect_text()
		self.select_lines(event)
	
	def finish_select(self,event=None):
		self.ctl.focus()
		self.check_selection()
		
	def get_font_family(self):
		return self._font_family
		
	def set_font_family(self,new_family):
		self._font_family=new_family
		self.update_font()
		
	font_family=property(get_font_family,set_font_family)
	
	def get_font_size(self):
		return self._font_size
		
	def set_font_size(self,new_size):
		self._font_size=new_size
		self.update_font()
		
	font_size=property(get_font_size,set_font_size)
	
	def get_font_bold(self):
		return self._font_bold
		
	def set_font_bold(self,value):
		self._font_bold=(value!=0)
		self.update_font()
		
	font_bold=property(get_font_bold,set_font_bold)
	
	def get_font_italic(self):
		return self._font_italic
		
	def set_font_italic(self,value):
		self._font_italic=(value!=0)
		self.update_font()
		
	font_italic=property(get_font_italic,set_font_italic)
	
	def update_font(self):
		fs=(
			'"'+self._font_family+'" '+
			str(self._font_size)+
			(""," bold")[self._font_bold]+
			(""," italic")[self._font_italic]
		)
		self._font_string=fs
		self.ctl["font"]=fs
		del self._font
		self._font=font.Font(
			family=self._font_family, 
			size=self._font_size,
			weight=("normal","bold")[self._font_bold], 
			slant=("roman","italic")[self._font_italic]
		)
		self._container.update_idletasks()
		self._container.update()
		self.char_width=self._font.measure("_")
		self._container.update_idletasks()
		self.line_counter_redraw()
		
	def get_show_numbers(self):
		return self._show_numbers
		
	def set_show_numbers(self,value):
		self._show_numbers=(value!=0)
		if self._show_numbers:
			self.line_counter_width=self._font.measure(self.last_linenum)
		else:
			self.line_counter_width=0
		self.place(x=self._x,y=self._y,width=self._width,height=self._height)
		
	show_numbers=property(get_show_numbers,set_show_numbers)
	
	def get_text_color(self):
		return self._text_color
		
	def set_text_color(self,value):
		self._text_color=value
		self.ctl["foreground"]=self._text_color
		
	text_color=property(get_text_color,set_text_color)
	
	def get_text_bgcolor(self):
		return self._text_bgcolor
		
	def set_text_bgcolor(self,value):
		self._text_bgcolor=value
		self.ctl["bg"]=self._text_bgcolor
		
	text_bgcolor=property(get_text_bgcolor,set_text_bgcolor)
	
	def get_highlight_color(self):
		return self._highlight_color
		
	def set_highlight_color(self,value):
		self._highlight_color=value
		self.ctl.tag_config("sel", foreground=self._highlight_color)
		self.line_counter_redraw()
		
	highlight_color=property(get_highlight_color,set_highlight_color)
	
	def get_highlight_bgcolor(self):
		return self._highlight_bgcolor
		
	def set_highlight_bgcolor(self,value):
		self._highlight_bgcolor=value
		self.line_counter["bg"]=self._highlight_bgcolor
		self.ctl.tag_config("sel", background=self._highlight_bgcolor)
		
	highlight_bgcolor=property(get_highlight_bgcolor,set_highlight_bgcolor)
	
	def search(self,text,index="1.0",nocase=True,stopindex="end-1c"):
		return self.ctl.search(text,index,nocase=nocase,stopindex=stopindex)
		
	def select(self,index1,index2):
		self.ctl.focus()
		self.ctl.tag_add("sel", index1, index2)
		self.ctl.mark_set("insert",index2)
		self.ctl.see("insert")
	
	def replace(self,index1,index2,text):
		self.ctl.replace(index1,index2,text)
		
	def get_selection_range(self):
		return self.ctl.tag_ranges("sel")
		
	def get(self,ind1,ind2):
		return self.ctl.get(ind1,ind2)
#================================================================================
	
class TToolTip(object):
	def __init__(self,parent):
		self.parent=parent
		self.w_exists=False
		self.widgets=dict()
		self.text=""
		self.timer_id=None

	def show(self):
		if self.w_exists:self.w.destroy()#if the tooltip window exists, destroy it
		
		self.w=Toplevel()
		self.w.bg="honeydew"
		self.w.bd=0
		self.w.overrideredirect(True)
		self.ttc=Canvas(self.w,bg="honeydew",bd=0,highlightthickness=0)
		self.ttct=self.ttc.create_text(9, 5, anchor="nw", text=self.text,fill="black")
		bounds = self.ttc.bbox(self.ttct)  # returns a tuple like (x1, y1, x2, y2)
		ttctw = bounds[2] - bounds[0]
		ttcth = bounds[3] - bounds[1]
		self.ttcr1=self.ttc.create_rectangle(0,0,ttctw+18,ttcth+10,fill="RoyalBlue",width=0)
		self.ttcr2=self.ttc.create_rectangle(1,1,ttctw+17,ttcth+9,fill="LightCyan3",width=0)
		self.ttc.place(x=0,y=0,width=ttctw+18,height=ttcth+10)
		self.ttc.tag_raise(self.ttct)
		x=self.w.winfo_pointerx() - self.w.winfo_rootx()
		y=self.w.winfo_pointery() - self.w.winfo_rooty()
		if x>self.w.winfo_screenwidth()/2:
			x=x-ttctw-18-5
		else:
			x=x+5
		if y<self.w.winfo_screenheight()/2:
			y=y+ttcth
		else:
			y=y-ttcth*2
		self.w.geometry(str(ttctw+18)+"x"+str(ttcth+10)+"+"+str(x)+"+"+str(y))
		self.w_exists=True

	def hide(self):
		if self.w_exists:
			self.w.destroy()
			self.w_exists=False
			self.text=""

	def destroy(self):
		if self.w_exists:self.w.destroy()
		
	def register_tooltip(self,widget,text):
		widget.bind("<Enter>",self.on_enter,add="+")
		widget.bind("<Leave>",self.on_leave,add="+")
		self.widgets[widget.winfo_name]=text
		
	def set_text(self,widget,text):
		self.widgets[widget.winfo_name]=text
		
	def on_enter(self,event=None):
		t=self.widgets.get(event.widget.winfo_name)
		if t!=None:
			self.text=t
			self.timer_id=self.parent.after(1000,self.show)
		
	def on_leave(self,event=None):
		if self.timer_id!=None: self.parent.after_cancel(self.timer_id)
		self.hide()
		
#================================================================================

class TFontList(object):
	def __init__(self, container,onselect_proc):
		self.ctl=Frame(container,bd=2,relief="sunken",padx=0,pady=0,highlightthickness=0)
		self.cfg=dict()
		self.cfg["text_bgcolor"]="#ffffff"
		self.cfg["text_color"]="#000000"
		self.cfg["highlight_bgcolor"]="#000000"
		self.cfg["highlight_color"]="#ffffff"
		self.cnv=Canvas(self.ctl,bg=self.cfg["text_bgcolor"],highlightthickness=0)
		self.vs=ttk.Scrollbar(self.ctl,orient = "vertical",command=self.myscroll)
		self.container=container
		
		self.vs.place(x=0,y=0)#without this temporary placement self.vs.winfo_height() returns 1
		self.enable=True
		self.cnv_height=1#temporary canvas height
		self.line_height=20#line height canvas
		self.font_size=10
		self.onselect_proc=onselect_proc#callback
		self.cnv.bind("<Button-1>",self.select)#connect event (left mouse button)
		# Binding for Windows/macOS
		self.cnv.bind("<MouseWheel>", self.scroll_canvas)
		# Binding for Linux
		self.cnv.bind("<Button-4>", self.scroll_canvas)
		self.cnv.bind("<Button-5>", self.scroll_canvas)

		self.load_fonts()#download information about fonts
		self.line_count=len(self.fonts)#number of lines per canvas
		self.step=1#temporary step
		self.first_visible_line=0#first line of fonts visible on canvas
		self.old_first_visible_line=-1
		self.selected_line=-1#index of the selected row
		self.visible_line_count=1#number of lines per canvas
		self.container.update_idletasks()#without this self.vs.winfo_height() returns 1
		
	def load_fonts(self):
		self.fonts=[]#initialize the list
		for fam in font.families():#for each font in the list of system fonts
			d=dict()#initialize the dictionary
			if fam!="Noto Color Emoji":
				f=font.Font(family=fam, size=self.font_size, weight="normal",slant="roman")#download the font
				d["family"]=fam#enter the font name into the dictionary
				d["ascent"]=f.metrics("ascent")#lower the height to baseline
				del f#delete
				self.fonts.append(d)#add the dictionary as a list element
				del d
			
	def place(self,**kwargs):
		x=kwargs["x"]
		y=kwargs["y"]
		width=kwargs["width"]
		height=kwargs["height"]
		self.ctl.place(kwargs)
		ws=self.vs.winfo_width()#scrollbar width
		self.cnv_height=height-3#canvas height
		self.cnv_width=width-ws-4#canvas width
		self.cnv.place(x=0,y=0,width=self.cnv_width,height=self.cnv_height)#place the canvas
		self.vs.place(x=width-ws-2,y=0,height=self.cnv_height)#place a scrollbar
		self.visible_line_count=self.cnv_height//self.line_height#update the number of lines per canvas
		if self.line_count>self.visible_line_count:#if there are more fonts than are included on the canvas
			self.step=0.5/(self.line_count-self.visible_line_count)#calculate the step
			self.update_scrollbar()#updating the scrollbar
		else:#if less than or equal
			self.vs.set(0.0,1.0)#disable scrollbar
		self.draw_fonts()#redraw fonts
		
	def update_scrollbar(self):
		a=1.1;b=1.1
		a=self.step*self.first_visible_line#calculate the distance from the top of the scrollbar to the top of the slider
		b=a+0.5#calculate the distance from the top of the scrollbar to the bottom of the slider
		self.vs.set(a,b)#load into scrollbar
		
	def draw_fonts(self,by_selection=False):
		if self.first_visible_line!=self.old_first_visible_line or by_selection:#if the first visible line has changed
			#or the user has selected some font
			y=0;cur=0
			self.cnv.delete("all")#removing everything from the canvas
			while y<self.cnv_height and cur+self.first_visible_line<len(self.fonts) :#while there's still room
				#on canvas and there are also fonts in fonts
				i=cur+self.first_visible_line#take the index of the line, cat. we want to draw
				t=self.fonts[i]#let's get the info
				fam=t["family"]
				a=t["ascent"]
				if i==self.selected_line:#if this is a selected line
					r=self.cnv.create_rectangle(
						0,y,
						self.cnv_width,
						y+self.line_height,
						fill=self.cfg["highlight_bgcolor"],
						width=0
					)
					forecolor=self.cfg["highlight_color"]
				else:#if not selected
					r=self.cnv.create_rectangle(
						0,y,
						self.cnv_width,
						y+self.line_height,
						fill=self.cfg["text_bgcolor"],
						width=0
					)
					forecolor=self.cfg["text_color"]
				tt=self.cnv.create_text(
					5,y-a+14,
					anchor="nw", 
					text=fam, 
					font=(fam,self.font_size,"normal","roman"),
					fill=forecolor
				)#draw the name of the font
				self.cnv.tag_lower(r,tt)#overlay text on rectangle
				y+=self.line_height;cur+=1#add Y and current index
			self.old_first_visible_line=self.first_visible_line
	
	def myscroll(self,proc,arg1,arg2=None):
		if proc=="scroll":self.scroll(arg1,arg2)
		if proc=="moveto":self.moveto(arg1)
		
	def scroll(self,arg1,arg2):
		self.first_visible_line+=int(arg1)
		self.check_first_visible_line()
		self.update_scrollbar()
		self.draw_fonts()
		
	def moveto(self,arg1):
		self.first_visible_line=round((self.line_count-self.visible_line_count)*(float(arg1)/0.5))
		self.check_first_visible_line()
		self.update_scrollbar()
		self.draw_fonts()
	
	def scroll_canvas(self,event):
		# Windows/macOS: event.delta, Linux: event.num (4-up, 5-down)
		if event.delta > 0 or event.num == 4:
			self.scroll(-1, "units")
		elif event.delta < 0 or event.num == 5:
			self.scroll(1, "units")
	
	def check_first_visible_line(self):
		if self.first_visible_line<0:
			self.first_visible_line=0
		if self.first_visible_line>self.line_count-1-self.visible_line_count:
			self.first_visible_line=self.line_count-self.visible_line_count
		
	def select(self,event=None):
		self.selected_line=self.first_visible_line+event.y//self.line_height
		self.draw_fonts(True)
		self.onselect_proc(self.fonts[self.selected_line]["family"])
		
	def get_family(self):
		return self.fonts[self.selected_line]["family"]
		
	def set_family(self,new_family):
		j=-1
		for i in range(len(self.fonts)):#we are looking for the new_family index in family
			d=self.fonts[i]
			if d["family"].upper()==new_family.upper():#if found
				j=i#remember and
				exit#let's go out
		if j!=-1:#if you remember something
			self.selected_line=j#update the index of the selected row
			i=j-self.visible_line_count//2#calculate first_visible_line so that the selected
			#the line was drawn in the middle of the control
			if i>self.line_count-self.visible_line_count:i=self.line_count-self.visible_line_count
			if i<0:i=0
			self.first_visible_line=i
			self.update_scrollbar()
			self.draw_fonts(True)
			
	famyly = property(get_family,set_family)
		
	
