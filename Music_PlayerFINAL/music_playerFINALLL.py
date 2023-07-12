# pip install pygame

import os
import pickle
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
from pygame import mixer
import time

class Player(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.configure(bg='#33495f')
		self.pack()
		mixer.init()

		if os.path.exists('songs.pickle'):
			with open('songs.pickle', 'rb') as f:
				self.playlist = pickle.load(f)
		else:
			self.playlist=[]

		self.current = 0
		self.paused = True
		self.played = False
		self.muted = False
		self.GIF=False

		self.create_frames()
		self.track_widgets()
		self.control_widgets()
		self.tracklist_widgets()



		self.songlist = []
		directory = "C:/Users/eduar/Desktop/ProjetoCLOCK/Music_PlayerFINAL"
		
		for root_, dirs, files in os.walk(directory):
				for file in files:
					if os.path.splitext(file)[1] == '.mp3':
						path = (root_ + '/' + file).replace('\\','/')
						self.songlist.append(path)

		with open('songs.pickle', 'wb') as f:
			pickle.dump(self.songlist, f)
		self.playlist = self.songlist
		self.tracklist['text'] = f'PlayList - {str(len(self.playlist))}'
		self.list.delete(0, tk.END)
		self.enumerate_songs()




	def create_frames(self):

		self.track = tk.LabelFrame(self, bg='#33495f',relief='flat')
		self.track.config(width=410,height=80)
		self.track.grid(row=0, column=0, padx=10)


		self.track = tk.LabelFrame(self, text='Music App', background="red",
					font=("Helvetica",15,"bold", "italic"),
					bg="SlateGray4",fg="white",bd=7,relief=tk.GROOVE)
		self.track.config(width=410,height=300)
		self.track.grid(row=1, column=0)#, padx=10)

		self.tracklist = tk.LabelFrame(self, text=f'PlayList - {str(len(self.playlist))}',
							font=("Helvetica",9,"bold"),
							background="SlateGray4",fg="white",bd=7,relief=tk.GROOVE)
		self.tracklist.config(width=410,height=300)
		self.tracklist.grid(row=2, column=0)#, pady=5)

		self.controls = tk.LabelFrame(self, relief='flat',
							font=("Helvetica",15,"bold"),
							bg="#33495f",fg="white",bd=2)
		self.controls.config(width=410,height=80)
		self.controls.grid(row=3, column=0, pady=5, padx=10)

	def track_widgets(self):
		

		self.canvas = tk.Label(self.track, bg="SlateGray4")
		self.canvas.configure(width=400, height=240)
		self.canvas.grid(row=1,column=0)

		# if self.GIF==True:
				
		# GIF GIF GIF
		frameCnt=41
		frames=[PhotoImage(file='serd.gif', format = 'gif -index %i' %(i)) for i in range(frameCnt)]

		def update(ind):
			frame = frames[ind]
			ind += 1
			if ind == frameCnt:
				ind = 0
			self.canvas.configure(image=frame)
			self.canvas.after(50, update, ind)

		self.canvas.after(0, update, 0)
		# else:
		# 	frames=[PhotoImage(file='serd.gif', format = 'gif -index %i' %(i)) for i in range(41)]
		# 	self.canvas.configure(image="stopdisk.png")

		


		self.songtrack = tk.Label(self.track, font=("Helvetica",16,"bold"), bg='SlateGray4',
						fg="white")
		self.songtrack['text'] = 'MP3 Player'
		self.songtrack.config(width=30, height=1)
		self.songtrack.grid(row=2,column=0,padx=10)

	def control_widgets(self):
		
		self.prev = tk.Button(self.controls, activebackground='SlateGray4', image=prev, bg='SlateGray4',width='136.7', height='100')
		self.prev['command'] = self.prev_song
		self.prev.grid(row=0, column=1)

		self.pause = tk.Button(self.controls, activebackground='SlateGray4', image=pause, bg='SlateGray4',width='136.7', height='100')
		self.pause['command'] = self.pause_song
		self.pause.grid(row=0, column=2)

		self.next = tk.Button(self.controls, activebackground='SlateGray4', image=next_, bg='SlateGray4',width='136.7', height='100')
		self.next['command'] = self.next_song
		self.next.grid(row=0, column=3)
		

		self.mute = tk.Button(self.controls, activebackground='SlateGray4', image=mute, bg='SlateGray4',width='136.7', height='100')
		self.mute['command'] = self.mute_song
		self.mute.grid(row=1, column=1)

		self.volumeDown = tk.Button(self.controls, activebackground='SlateGray4', image=volumeDown, bg='SlateGray4',width='136.7', height='100')
		self.volumeDown['command'] = self.volume_down
		self.volumeDown.grid(row=1, column=2)

		self.volumeUp = tk.Button(self.controls, activebackground='SlateGray4',image=volumeUp, bg='SlateGray4',width='136.7', height='100')
		self.volumeUp['command'] = self.volume_up
		self.volumeUp.grid(row=1, column=3)

		self.volume = tk.DoubleVar(self)
		self.slider = tk.Scale(self.controls, sliderlength=0, relief='flat', from_ = 0, to = 10,
								highlightbackground='#33495f', orient = tk.HORIZONTAL,
								 bg='#33495f', troughcolor='#33495f', bd=0, fg='#33495f')
		self.slider['variable'] = self.volume
		
		self.slider.set(8)
		mixer.music.set_volume(0.8)
		self.slider['command'] = self.change_volume
		self.slider.grid(row=3, column=2, padx=5)


	def tracklist_widgets(self):
		self.scrollbar = tk.Scrollbar(self.tracklist, orient=tk.VERTICAL)
		self.scrollbar.grid(row=0,column=1, rowspan=5, sticky='ns')

		self.list = tk.Listbox(self.tracklist, selectmode=tk.SINGLE, bg='SlateGray3',
					 yscrollcommand=self.scrollbar.set, selectbackground='SlateGray4')
		self.enumerate_songs()
		self.list.config(width=66, height=7)
		self.list.bind('<Double-1>', self.play_song) 

		self.scrollbar.config(command=self.list.yview)
		self.list.grid(row=0, column=0, rowspan=5)

	
	def enumerate_songs(self):
		for index, song in enumerate(self.playlist):
			self.list.insert(index, os.path.basename(song))


	def play_song(self, event=None):
		if event is not None:
			self.current = self.list.curselection()[0]
			for i in range(len(self.playlist)):
				self.list.itemconfigure(i, bg="white")

		print(self.playlist[self.current])
		mixer.music.load(self.playlist[self.current])
		self.songtrack['anchor'] = 'w' 
		self.songtrack['text'] = os.path.basename(self.playlist[self.current])

		self.pause['image'] = play
		self.paused = False
		self.played = True
		self.list.activate(self.current) 
		self.list.itemconfigure(self.current, bg='sky blue')

		mixer.music.play()

	def pause_song(self):
		if not self.paused:
			self.paused = True
			mixer.music.pause()
			self.pause['image'] = pause
		else:
			if self.played == False:
				self.play_song()
			self.paused = False
			mixer.music.unpause()
			self.pause['image'] = play

	def prev_song(self):
		if self.current > 0:
			self.current -= 1
		else:
			self.current = 0
		self.list.itemconfigure(self.current + 1, bg='white')
		self.play_song()

	def next_song(self):
		if self.current < len(self.playlist) - 1:
			self.current += 1
		else:
			self.current = 0
		self.list.itemconfigure(self.current - 1, bg='white')
		self.play_song()

	def change_volume(self, event=None):
		self.v = self.volume.get()
		mixer.music.set_volume(self.v / 10)


	def mute_song(self):
		self.v = self.volume.get()
		if not self.muted:
			self.muted = True
			mixer.music.set_volume(0)
			self.mute['image'] = self.mute.configure(bg='gray40')
		else:
			self.muted = False
			mixer.music.set_volume(self.v / 10)
			self.mute['image'] = self.mute.configure(bg='SlateGray4')


	def volume_down(self, event=None):
		self.v = self.volume.get()
		self.mute['image'] = self.mute.configure(bg='SlateGray4')
		self.muted = False
		if(self.v>=0):
			self.aux=self.v-1
			mixer.music.set_volume(self.aux/ 10)
			self.slider.set(self.aux)
		

	def volume_up(self):
		self.v = self.volume.get()
		self.mute['image'] = self.mute.configure(bg='SlateGray4')
		self.muted = False
		if(self.v<=10):
			self.aux=self.v+1
			mixer.music.set_volume(self.aux/ 10)
			self.slider.set(self.aux)


# ----------------------------- Main -------------------------------------------

root = tk.Tk()
root.geometry('1920x1080')
root.wm_title('MP3 Player')
root.configure(bg='#33495f')
# root.attributes("-fullscreen", True)

# img = PhotoImage(file='fundoOti.gif')

next_ = PhotoImage(file = 'next.png')
prev = PhotoImage(file='reverse.png')
play = PhotoImage(file='pause.png')
pause = PhotoImage(file='play.png')
mute = PhotoImage(file='mute.png')
volumeDown = PhotoImage(file='volumeDown.png')
volumeUp = PhotoImage(file='volumeUp.png')

app = Player(master=root)

app.mainloop()



