from tkinter import Tk, Frame, Label, Entry, Button, Canvas, Scrollbar, StringVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import Figure

d_frame = dict( padx = 5, pady= 5 )
d_entry = dict( font = 'Arial 20 bold', bg = '#555555', fg = 'white', borderwidth=5, relief='flat', insertbackground='#F9AE58')
d_button = dict( font = 'Arial 20 bold', fg = 'white', relief='flat', bd=0, takefocus=False)
d_label = dict( font = 'Arial 20 bold', bg = '#383838', fg = 'white', relief='groove')
d_btn_dialog = dict( font = 'Arial 14 bold', bg='#494949', fg = 'white', activebackground='#565656', activeforeground = '#E5E5E5')
d_btn_close = dict( font = 'Arial 18 bold', fg = 'white', relief='flat', bd=0)
d_btn_del = dict( font = 'Arial 18 bold', fg = 'white', relief='flat', bd=0, takefocus=False)
d_btn_fav = dict(font = 'Arial 18 bold', fg = 'white', bg='#5B5B5B', relief='raised', activebackground='#656565', activeforeground='#F0F0F0' )

class Layout:
	SEEK_1 = 0
	SEEK_2 = 1
	FAV = 2
	INPUT_MAX_LENGTH = 7

	def __init__(self):
		self.root = self.__create_root()
		self.canvas, self.fig = self.__create_figure()
		self.fr_sidebar = self.__create_sidebar()
		self.fr_favs = self.__create_frame_favs()
		self.sv_asset_1 = self.__create_field(btn_callback=self.__on_click_seek_1)
		self.sv_asset_2 = self.__create_field(btn_callback=self.__on_click_seek_2)
		self.sv_message = self.__create_message()
		self.__create_toolbar()
		self.fr_dialog, self.fr_scroll, self.canvas_scroll = self.__create_dialog()
	
		# self.show_dialog()


	def __create_root(self):
		root = Tk()
		root.geometry('1000x600')
		root.bind_all('<Control-q>',lambda _ : self.root.destroy())
		root.grid_columnconfigure(0, weight=1)
		root.grid_rowconfigure(0, weight=1)
		return root
	
	def __create_figure(self):
		fig = Figure()
		fig_canvas = FigureCanvasTkAgg(fig, master=self.root)
		canvas = fig_canvas.get_tk_widget()
		canvas.config(highlightthickness=0, bg='black')
		canvas.grid(row=0, column=0, sticky='news')
		return canvas, fig

	def __create_sidebar(self):
		fr_sidebar = Frame(master=self.root, bg='#4C4C4C')
		fr_sidebar.config(**d_frame)
		fr_sidebar.grid(row=0, column=1, sticky='news')
		return fr_sidebar

	def __create_field(self,btn_callback):
		
		def on_validate(action_type,text):
			if action_type == '1' and (len(text) > Layout.INPUT_MAX_LENGTH) :
				return False
			return True

		bg = self.fr_sidebar['bg']
		
		fr_input = Frame(master=self.fr_sidebar, bg=bg)
		fr_input.pack(side='top', fill='both')
		sv = StringVar(value='')
		sv.last = ''
		sv.trace_add('write', lambda *args : sv.set(sv.get().upper()))
		
		entry = Entry(master=fr_input, textvar=sv, width=12, **d_entry)
		entry.insert( 0 , 'USTC' )

		vcmd = ( self.root.register(on_validate), '%d', '%P')
		entry.config( validate='key', validatecommand=vcmd)
		entry.pack(side='left', expand=True)
		entry.bind('<Return>', lambda e: self.__on_press_enter())
		entry.bind('<Up>', lambda e: entry.tk_focusPrev().focus())
		entry.bind('<Down>', lambda e: entry.tk_focusNext().focus())
		entry.bind('<Control-BackSpace>', lambda e: sv.set(''))
			
		bg_entry = entry['bg']

		btn_del = Button(master=entry,text='✖', **d_btn_del)
		btn_del.config(bg=bg_entry, activebackground=bg_entry)
		btn_del['command'] = lambda : sv.set('')
		btn_del['cursor'] = 'arrow'
		btn_del.place( in_=entry, relx = 1.05, rely=0.5, relheight=1, anchor='e')

		btn_seek = Button(master=fr_input, text='🔍', width=2 )
		btn_seek.config(bg=bg,  **d_button, activebackground = bg )
		btn_seek['command'] = btn_callback
		btn_seek.pack(side='left')
		return sv

	def __create_message(self):
		sv = StringVar(value='MSG')
		label = Label(master=self.fr_sidebar, textvar=sv, **d_label )
		label.config(padx=5)
		label.pack(side='top', fill='x')
		return sv

	def __create_toolbar(self):
		fr_toolbar = Frame(master=self.fr_sidebar, bg='#515151')
		fr_toolbar.pack(side='top', fill = 'x')
		bg_toolbar = fr_toolbar['bg']
		
		btn_fav = Button(master=fr_toolbar, text='⭐', **d_button)
		btn_fav.config(bg=bg_toolbar, activebackground=bg_toolbar)
		btn_fav['command'] = lambda opt=self.FAV : self.__on_selected_option(opt)
		btn_fav.pack(side='right')

	def __create_frame_favs(self):
		fr_favs = Frame(master=self.fr_sidebar, bg='#404040')
		fr_favs.config(**d_frame)
		fr_favs.pack(side='bottom', fill='both', expand=True, pady=5)
		return fr_favs

	def __create_dialog(self):
		fr_dialog = Frame(master=self.root, bg='white', bd=1)
		bg_dialog = fr_dialog['bg']
		# fr_dialog.place(in_= self.root, relx=0.5,rely=0.5, anchor='center', relwidth = 0.8, relheight = 0.8)

		fr_head = Frame(master=fr_dialog, bg='#3F3F3F')
		fr_head.pack(side='top', fill='both')

		btn_close = Button(master=fr_head, text='✖', **d_btn_close)
		bg_head = fr_head['bg']
		btn_close.config(bg=bg_head, activebackground=bg_head, activeforeground = bg_head)
		btn_close.pack(side='right')
		btn_close['command'] = self.hide_dialog

		fr_body = Frame(master=fr_dialog, bg='#4D4D4D', padx=5, pady=5)
		fr_body.pack(side='top', fill='both', expand=True)
		bg_body = fr_body['bg']
		
		canvas = Canvas(master=fr_body, bg=bg_body, highlightthickness=0)

		scrollbar = Scrollbar(master=fr_body, orient='vertical', command=canvas.yview)
		scrollbar.config(width=20)
		scrollbar.pack(side='right', fill='y')

		fr_scroll = Frame(master=canvas, bg=bg_body)

		self.id_canvas_fr_scroll = canvas.create_window((0,0), window=fr_scroll, anchor='nw', width=0)
		canvas.configure(yscrollcommand=scrollbar.set)
		canvas.bind_all( '<MouseWheel>', lambda e : canvas.yview_scroll(-1 * int(e.delta / 120), 'units'))
		canvas.bind( '<Configure>', self.__on_canvas_configure)
		canvas.pack(side='left', fill='both', expand=True)

		return fr_dialog, fr_scroll, canvas

	def __on_selected_option(self,option):
		self.on_selected_option(option)

	def __on_canvas_configure(self,event):
		self.__update_canvas()

	def __update_canvas(self):
		canvas = self.canvas_scroll
		canvas.configure(scrollregion=canvas.bbox('all'))
		canvas.itemconfig(self.id_canvas_fr_scroll, width=canvas.winfo_width())

	def __on_click_seek_1(self):
		self.on_click_seek(Layout.SEEK_1)
		self.current_seek = Layout.SEEK_1
			
	def __on_click_seek_2(self):
		self.on_click_seek(Layout.SEEK_2)
		self.current_seek = Layout.SEEK_2

	def __on_click_asset(self,asset):
		self.on_click_asset(asset)

	def __on_press_enter(self):
		self.on_press_enter()

	def add_favourite(self,text):
		if not self.fav_exists(text):
			button = Button(master=self.fr_favs, text=text, **d_btn_fav)
			button['command'] = lambda : self.on_select_fav(text)
			button.pack(side='top', fill='x')
			self.root.update()

	def fav_exists(self,text):
		for child in self.fr_favs.winfo_children():
			if child['text'] == text:
				return True
		return False

	def set_callbacks(self,
		on_click_seek, on_click_asset, on_press_enter,
		on_selected_option, on_select_fav):
		self.on_click_seek = on_click_seek
		self.on_click_asset = on_click_asset
		self.on_press_enter = on_press_enter
		self.on_selected_option = on_selected_option
		self.on_select_fav = on_select_fav

	def set_assets(self,asset_1,asset_2):
		return self.sv_asset_1.set(asset_1), self.sv_asset_1.get(asset_2)

	def get_assets(self):
		return self.sv_asset_1.get(), self.sv_asset_2.get()

	def get_seek(self,id_seek):
		if id_seek == Layout.SEEK_1:
			sv = self.sv_asset_1
		else:
			sv = self.sv_asset_2

		value, last_value = sv.get(), sv.last
		sv.last = value
		return value, last_value
		
	def set_message(self,text):
		self.sv_message.set(text)

	def clear_dialog_body(self):
		for widget in self.fr_scroll.grid_slaves():
			widget.destroy()

	def show_dialog(self):
		self.fr_dialog.place(in_= self.root, relx=0.5,rely=0.5, anchor='center', relwidth = 0.8, relheight = 0.9)

	def hide_dialog(self):
		self.fr_dialog.place_forget()
	
	def set_dialog_content(self,l_texts):
		n_items = len(l_texts)
		n_cols = 5
		n_rows = n_items // n_cols
		n_mod_cols = n_items % n_cols

		if n_rows <= 1:
			l_row_col = [ [0,c] for c in range(n_mod_cols)]
		else:
			l_row_col = [ [r,c] for r in range(n_rows) for c in range(n_cols) ]
			l_row_col += [ [n_rows - 1,c] for c in range(n_mod_cols)]
		
		self.clear_dialog_body()

		for text,(r,c) in zip(l_texts,l_row_col):
			button = Button(master=self.fr_scroll, text=text, **d_btn_dialog)
			button.grid(row=r,column=c,stick='news')
			button['command'] = lambda asset=text: self.on_click_asset(asset)

		for c in range(n_cols):
			self.fr_scroll.grid_columnconfigure(c, weight=1, uniform='column')

		self.root.update()

		self.__update_canvas()