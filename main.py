import pygame
import tkinter as tk
from tkinter import filedialog, END, Scale
import os

pygame.mixer.init()

root = tk.Tk()
root.title("Music Player")
root.geometry("500x400")

menubar = tk.Menu(root)
root.config(menu=menubar)


def load_song():
    global curr_song
    root.directory = filedialog.askdirectory()

    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext == '.mp3':
            songs.append(song)

    for song in songs:
        song_list.insert("end", song)

    if songs:
        song_list.selection_set(0)
        curr_song = songs[song_list.curselection()[0]]


def play_song():
    global curr_song, paused

    if not paused:
        pygame.mixer.music.load(os.path.join(root.directory, curr_song))
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.unpause()
        paused = False


def pause_song():
    global paused
    pygame.mixer.music.pause()
    paused = True


def next_song():
    global curr_song, paused

    try:
        current_index = songs.index(curr_song)
        next_index = (current_index + 1) % len(songs)
        curr_song = songs[next_index]
        song_list.selection_clear(0, END)
        song_list.selection_set(next_index)
        song_list.activate(next_index)
        pygame.mixer.music.load(os.path.join(root.directory, curr_song))
        pygame.mixer.music.play()
        paused = False
    except IndexError:
        pass


def prev_song():
    global curr_song, paused

    try:
        current_index = songs.index(curr_song)
        prev_index = (current_index - 1) % len(songs)
        curr_song = songs[prev_index]
        song_list.selection_clear(0, END)
        song_list.selection_set(prev_index)
        song_list.activate(prev_index)
        pygame.mixer.music.load(os.path.join(root.directory, curr_song))
        pygame.mixer.music.play()
        paused = False
    except IndexError:
        pass


def set_volume(val):
    volume = int(val) / 100
    pygame.mixer.music.set_volume(volume)


organize_menu = tk.Menu(menubar, tearoff=False)
organize_menu.add_command(label="Select Folder", command=load_song)
menubar.add_cascade(label="Import Music", menu=organize_menu)

song_list = tk.Listbox(root, bg="black", fg="white", width=100, height=15)
song_list.pack()

songs = []
curr_song = ""
paused = False

play_img = tk.PhotoImage(file="play.png")
pause_img = tk.PhotoImage(file="pause.png")
prev_img = tk.PhotoImage(file="previous.png")
next_img = tk.PhotoImage(file="next.png")

control_frame = tk.Frame(root, bg="white")
control_frame.pack()

prev_button = tk.Button(control_frame, image=prev_img, command=prev_song, borderwidth=0)
play_button = tk.Button(control_frame, image=play_img, command=play_song, borderwidth=0)
pause_button = tk.Button(control_frame, image=pause_img, command=pause_song, borderwidth=0)
next_button = tk.Button(control_frame, image=next_img, command=next_song, borderwidth=0)

prev_button.grid(row=0, column=0, padx=10, pady=10)
play_button.grid(row=0, column=1, padx=10, pady=10)
pause_button.grid(row=0, column=2, padx=10, pady=10)
next_button.grid(row=0, column=3, padx=10, pady=10)

volume_slider = Scale(root, from_=0, to=100, orient='horizontal', command=set_volume)
volume_slider.set(70)
volume_slider.pack(pady=10)

root.mainloop()
