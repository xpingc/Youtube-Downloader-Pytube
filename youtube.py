##############################
# UI MODs
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import datetime
import time
import moviepy.editor as mp
import os.path
from os import path

##############################
# Audio to Text MODs
from pydub import AudioSegment
import speech_recognition as sr

##############################
# Youtube JSON MODs
import json
import re
import urllib
import urllib.request
from urllib.request import urlopen
from pytube import YouTube
import pprint as pp

##############################
# For Converting GUI Media to Tkinter-compatible image objects
# https://effbot.org/tkinterbook/photoimage.htm
from PIL import Image, ImageTk

##############################
# For Tooltips
import webview

##############################
# For logging version checking, TBD
version = 1
# ****************************************
# Place your API Key below
key = ''
#  ffmpeg must be properly installed on OS, worked well with "brew install"
ffmpeg_location = ''

##############################
# Timestamp VARS
now_date = datetime.date.today().strftime('%d%b%y').upper()
now_hour = str(time.localtime().tm_hour)
now_min = str(time.localtime().tm_min)


def is_internet():
    timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
    system_log = f'{timestamp} | Checking for internet connection...'
    print(system_log)
    """
    Query internet using python, exception prevents user from accessing tool without internet connection.
    :return:
    """
    try:
        urlopen('https://www.google.com', timeout=1)
        return True
    except:
        win = Tk()
        win.geometry('1400x25')
        win.config(bg='red')
        tkinter.messagebox.showinfo(title='Design Error', message='Ths tool requires an active internet connection. '
                                                                  'Please reconnect and try again. Thanks!')
        exit()


is_internet()

win = Tk()
win.title("Youtube Handler")
# Makes GUI non-resizable
# win.resizable(0, 0)
menu = Menu(win)
win.config(menu=menu, bg='#384048', padx=7, pady=7)
timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
system_log = f'{timestamp} | Success! Your program is opened, :)'
print(system_log)

##############################
# Tray/Program Icon
my_dir = os.path.dirname(os.path.realpath(__file__))
icon_image = Image.open(f'/{my_dir}/youtube_ico.png')
photo = ImageTk.PhotoImage(icon_image)
win.iconphoto(False, photo)

##############################
# Placeholders for Global Edits | Common VARs
video_id = None
title = ''
description = ''
user_input = ''

# Tool Tip Screen share Location
help_url = 'https://drive.google.com/file/d/1JqbJgrxMqlw6Xgw6oFeT1J0SDvZpWa6t/view'

##############################
# GUI Dependent Functions


def user_action(self):
    global title
    selection = user_option_dropdown.get()
    # Get user Link
    s = user_input.get()
    helper = Helper()
    video_id = helper.id_from_url(str(s))
    api_key = key
    url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}'
    yt_stats = YouTubeStats(url)
    title = yt_stats.get_video_title()
    title = helper.title_to_underscore_title(title)
    description = yt_stats.get_video_description()

    if selection == 'Download Video':
        if path.exists(f'{my_dir}/{title}.mp4'):
            timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
            system_log = f'{timestamp} | Video detected, no download required'
            print(system_log)
            status_bar.delete(0, END)
            status_bar.insert(0, system_log)

        else:
            download_vid()

    elif selection == 'Convert Audio':
        # action_type = 'DISCONNECT'
        convert_to_mp3()

    elif selection == 'Generate Metrics File':
        # action_type = 'DISCONNECT'
        generate_metrics_report()

    elif selection == 'Generate Transcript':
        # action_type = 'DISCONNECT'
        if path.exists(f'{title}_transcript.txt'):
            pass
            timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
            system_log = f'{timestamp} | Transcript Detected, there is no write required'
            print(system_log)
            status_bar.delete(0, END)
            status_bar.insert(0, system_log)

        else:
            if path.exists(f'{title}.mp3'):
                generate_transcript()
            else:
                timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
                print(f'{timestamp} | No .mp3 for {title} detected. Please convert your mp4 to audio first')

    elif selection == 'Generate Youtube Transcript':
        # action_type == 'CONNECT'
        start = time.perf_counter()
        download_vid()
        convert_to_mp3()
        generate_metrics_report()
        generate_transcript()
        finish = time.perf_counter()
        timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
        print(f'{timestamp} | Processing Complete! Finished in {round(finish-start/60, 0)} minutes')

    else:
        print('Fail')


def show_instructions():
    instructions = tkinter.messagebox.showinfo('General Instructions', '''This tool can download MP4\'s from Youtube, convert them to MP3 files, download a text document showing pertinent information about your video, and generate a speech-to-text transcript of your audio.

Downloading Videos: Go to your Youtube Video and Click \'Share\'. You must be logged in to Youtube. Then copy the link. The link should look something like this: 'https://youtu.be/-bK4iuAlcYQ'

Converting to MP3: Currently, this tool only converts the file that was recently downloaded from Youtube. If you reopen the program and want to convert the audio from a video that is already located in your directory you must still copy the link from the youtube video because the program converts by the EXACT filename previously created.

Generate Metrics File: This will download a .txt file of your file name, it's description as posted on Youtube. More functionality will be added later on. If you have input our something you would like to see added in this file feedback can be submitted here in the 'File' menu.

Generate Transcript: There are two ways a transcript can be generated. You can do it from the beginning in Youtube by copying the link and selecting \'Generate Youtube Transcript\'''')



def link_help_prompt():
    prompt = tkinter.messagebox.askquestion('Where do I get the link?', 'The link entry box in this tool is '
                                                                        'where you paste the link of the Youtube '
                                                                        'video you are interested in. To get the '
                                                                        'correct link go to the video of interest, '
                                                                        'click share, and copy the link displayed. '
                                                                        'Make sure you do not use the URL at the very '
                                                                        'top of your browser. Want more help?')
    if prompt == 'yes':
        youtube_help()
    else:
        pass


def submit_advice():
    webview.create_window('Youtube Link', 'https://docs.google.com/forms/d/e/1FAIpQLSdQ1MGQm5IRlJFRSb4YH2irykiyqOeiRvdZWmQKhhG4aFIPXw/viewform')
    webview.start()


def display_user_choice(event):
    timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
    selection = user_option_dropdown.get()
    # system_log = f'{timestamp} | {selection} has been chosen, click \'SUBMIT\' to complete your action'
    # status_bar.delete(0, END)
    # status_bar.insert(10, system_log)


def youtube_help():
    webview.create_window('Youtube Link', 'https://drive.google.com/file/d/1JqbJgrxMqlw6Xgw6oFeT1J0SDvZpWa6t/view')
    webview.start()

################################################


class Helper:
    # strips video ID from url with REGEX
    def __init__(self):
        pass

    def title_to_underscore_title(self, title: str):
        title = title.replace('\'','')
        title = re.sub('[\W_]+', '_', title)
        return title.lower()

    def id_from_url(self, url: str):
         return url.rsplit('/', 1)[1]


class YouTubeStats:
    def __init__(self, url: str):
         self.json_url = urllib.request.urlopen(url)
         self.data = json.loads(self.json_url.read())

    def print_data(self):
        pp.pprint(self.data)

    def get_video_title(self):
        return self.data["items"][0]["snippet"]["title"]

    def get_video_description(self):
        return self.data["items"][0]["snippet"]["description"]

    def download_video(self, s: str, title: str):
        YouTube(s).streams.first().download(filename=title)

    def download_audio(self, s: str, title: str):
        YouTube(s).streams.first().download(filename=title)


def download_vid():
    global title
    global description
    selection = user_option_dropdown.get()
    # Get user Link
    s = user_input.get()
    helper = Helper()
    video_id = helper.id_from_url(str(s))
    api_key = key
    url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}'
    yt_stats = YouTubeStats(url)
    title = yt_stats.get_video_title()
    title = helper.title_to_underscore_title(title)
    description = yt_stats.get_video_description()
    answer = 'yes'
    # answer = tkinter.messagebox.askquestion('Proceed?',
    #                                         'Are you sure you want to continue with the download? Larger files will take some time to display in your active directory')
    if answer == 'yes':
        start_download = time.perf_counter()
        timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
        system_log = f'{timestamp} | Downloading, please wait...'
        # downloading_notification = tkinter.messagebox.showinfo('Downloading...', 'Downloading, you will be '
        #                                                                          'notified when it is complete. '
        #                                                                          'Closing this dialogue will not '
        #                                                                          'cancel the process.')
        # status_bar.delete(0, END)
        # status_bar.insert(10, system_log)2
        print(system_log)
        yt_stats.download_video(s, title)
        # download_complete = tkinter.messagebox.showinfo('Complete','Your download has finished and is located at: {my_dir}')
        timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
        finish_download = time.perf_counter()
        print(f'{timestamp} | Download complete in {round(finish_download-start_download, 2)} seconds!')
    else:
        system_log = f'{timestamp} | Download canceled'
        # status_bar.delete(0, END)
        # status_bar.insert(10, system_log)
        print(system_log)


def convert_to_mp3():
    # if action_type == 'CONNECT':
    #     title = title
    # else:
    #     title = user_input.get()
    if path.exists(f'{my_dir}/{title}.mp3'):
        timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
        system_log = f'{timestamp} | Audio detected, no conversion is required'
        # status_bar.delete(0, END)
        # status_bar.insert(10, system_log)
        print(system_log)
    else:
        if path.exists(f'{my_dir}/{title}.mp4'):
            timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
            answer = 'yes'
            # answer = tkinter.messagebox.askquestion('Proceed?',
            #                                         'Are you sure you want to continue with the audio conversion? Larger files will take some time to display in your active directory')
            if answer == 'yes':
                timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
                start_conversion = time.perf_counter()
                system_log = f'{timestamp} | Video detected, converting...'
                print(system_log)
                # status_bar.delete(0, END)
                # status_bar.insert(10, system_log)
                clip = mp.VideoFileClip(f'{title}.mp4')
                clip.audio.write_audiofile(f'{title}.mp3')
                timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
                end_conversion = time.perf_counter()
                print(f'{timestamp} | Your video was converted to an mp3 file in {round(end_conversion - start_conversion, 2)} seconds!')
            else:
                system_log = f'{timestamp} | Audio conversion canceled'
                print(system_log)
                # status_bar.delete(0, END)
                # status_bar.insert(10, system_log)

        else:
            timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
            system_log = f'{timestamp} | An MP4 video is required before you can convert to audio.' \
                         f' Change your dropdown to \'Download Video\' and submit that first.'
            print(system_log)
            # status_bar.delete(0, END)
            # status_bar.insert(10, system_log)


def generate_metrics_report():
    if path.exists(f'{my_dir}/{title}_description.txt'):
        timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
        system_log = f'{timestamp} | Description File Detected, there is no write required'
        print(system_log)
        # status_bar.delete(0, END)
        # status_bar.insert(10, system_log)

    else:
        with open(f'{title}_description.txt', 'w') as f:
            # write line to output file
            timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
            f.write(f'File Creation Date (Local Time): {timestamp}')
            f.write("\n")
            f.write(f'Filename: {title}')
            f.write("\n")
            f.write(f'Description: {description}')
            system_log = f'{timestamp} | No metadata file detected. {title}.txt was saved in the active directory'
            print(system_log)
            # status_bar.delete(0, END)
            # status_bar.insert(10, system_log)


def generate_transcript():
    global title
    global my_dir
    # if action_type == 'CONNECT':
    #     title = title
    # else:
    #     title = user_input.get()
    timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
    my_dir = os.path.dirname(os.path.realpath(__file__))
    # Convert to .wave
    print(f'{timestamp} | \'{title}\' detected')
    sound = AudioSegment.from_mp3(f'{title}.mp3')
    print(f'{timestamp} | Converting to .wav, standby...')
    sound.export(f'{title}.wav', format='wav')
    print(f'{timestamp} | A .wav file has been created. ')
    ############################################
    # VARs
    # ffmpeg
    AudioSegment.converter = ffmpeg_location

    # Input audio file to be sliced
    audio = AudioSegment.from_wav(f'{my_dir}/{title}.wav')

    # Length of the audio file in milliseconds
    n = len(audio)

    # Variable to count the number of sliced chunks
    counter = 1

    # Text file to write the recognized audio
    fh = open(f'{my_dir}/{title}_transcript.txt', 'w+')

    # Interval length at which to slice the audio file.
    # If length is 22 seconds, and interval is 5 seconds,
    # The chunks created will be:
    # chunk1 : 0 - 5 seconds
    # chunk2 : 5 - 10 seconds
    # chunk3 : 10 - 15 seconds
    # chunk4 : 15 - 20 seconds
    # chunk5 : 20 - 22 seconds
    min_interval = 1
    interval = (min_interval * 60) * 1000  # multiply to convert to milliseconds
    number_of_chunks = round((n / interval), 0) - 1
    timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
    print(f'{timestamp} | Splitting your audio into {number_of_chunks}, {min_interval}-minute '
          f'files for accurate voice to text conversion')

    # Length of audio to overlap.
    # If length is 22 seconds, and interval is 5 seconds,
    # With overlap as 1.5 seconds,
    # The chunks created will be:
    # chunk1 : 0 - 5 seconds
    # chunk2 : 3.5 - 8.5 seconds
    # chunk3 : 7 - 12 seconds
    # chunk4 : 10.5 - 15.5 seconds
    # chunk5 : 14 - 19.5 seconds
    # chunk6 : 18 - 22 seconds
    overlap = 1.5 * 1000

    # Initialize start and end seconds to 0
    start = 0
    end = 0

    # Flag to keep track of end of file.
    # When audio reaches its end, flag is set to 1 and we break
    flag = 0
    ############################################
    # End VARs
    # Iterate from 0 to end of the file,
    # with increment = interval
    for i in range(0, 2 * n, interval):
        # During first iteration,
        # start is 0, end is the interval
        if i == 0:
            start = 0
            end = interval
        # All other iterations,
        # start is the previous end - overlap
        # end becomes end + interval
        else:
            start = end - overlap
            end = start + interval
        # When end becomes greater than the file length,
        # end is set to the file length
        # flag is set to 1 to indicate break.
        if end >= n:
            end = n
            flag = 1
        # Storing audio file from the defined start to end
        chunk = audio[start:end]
        # Filename / Path to store the sliced audio
        filename = f'{title}_chunk_' + str(counter) + '.wav'
        # Store the sliced audio file to the defined path
        chunk.export(title, format="wav")
        # Get Timestamp
        timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
        # Print information about the current chunk
        print(f'{timestamp} | Processing chunk ' + str(counter) + '. Start = '
              + str(start) + ' end = ' + str(end))
        # Increment counter for the next chunk
        counter = counter + 1
        # Here, Google Speech Recognition is used
        # to take each chunk and recognize the text in it.
        # Specify the audio file to recognize
        AUDIO_FILE = title
        # Initialize the recognizer
        r = sr.Recognizer()
        # Traverse the audio file and listen to the audio
        with sr.AudioFile(AUDIO_FILE) as source:
            audio_recorded = r.record(source)

        # Try to recognize the listened audio
        # And catch expectations.
        try:
            rec = r.recognize_google(audio_recorded)
            # If recognized, write into the file.
            fh.write('\n')
            fh.write('\n')
            fh.write(f'Transcript #{counter - 1}')
            fh.write('\n')
            fh.write(rec + ' ')
        # If google could not understand the audio
        except sr.UnknownValueError:
            timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
            print(f'{timestamp} | Could not understand audio in')
            counter = counter - 1
        # If the results cannot be requested from Google.
        # Probably an internet connection error.
        except sr.RequestError as e:
            timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
            print(f'{timestamp} | Could not request results')
            counter = counter - 1
        # Check for flag.
        # If flag is 1, end of the whole audio reached.
        # Close the file and break.
        if flag == 1:
            fh.close()
            timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
            print(f'{timestamp} | The audio transcript was saved at {my_dir}/{title}_transcript.txt')
            break


def display_results():
    pp.pprint(data)


def doNothing():
    print('Okay, okay, I won\'t...')


def display_user_choice(event):
    selection = user_option_dropdown.get()
    if selection == '--CHOOSE ACTION--':
        pass
    else:
        timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
        system_log = f'{timestamp} | {selection} has been chosen, click \'SUBMIT\' to complete your action'
        print(system_log)


################################################
# Establish Menu
subMenu = Menu(menu)

# File Menu
menu.add_cascade(label='File', menu=subMenu)
subMenu.add_command(label='General Instructions', command=show_instructions)
subMenu.add_command(label='Submit Feedback', command=submit_advice)
subMenu.add_separator()
subMenu.add_command(label='Close', command=win.quit)

# Help Menu
helpMenu = Menu(menu)
menu.add_cascade(label='Help', menu=helpMenu)
helpMenu.add_command(label='Where do I get the link?', command=link_help_prompt)

################################################
# 'Link' Label
l1 = Label(win, text='Link', bg='#708090', fg='white', font='bold')
l1.grid(row=0, column=0, sticky='WE')

# URL Input
user_input = StringVar()
e1 = Entry(win, textvariable=user_input, width=25, highlightbackground='red', highlightthickness=1)
e1.grid(row=0, column=1, sticky='WE')

# Submit Button
submitButt = Button(win, text='Submit', highlightbackground='#708090')
submitButt.bind('<Button-1>', user_action)
submitButt.grid(row=0, column=15)

# ComboBox Style
ttk_style = ttk.Style()

ttk_style.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': '#708090',
                                       'fieldbackground': '#708090',
                                       'selectforeground': 'black',
                                       'background': '#384048',
                                       'relief': 'RAISED',
                                       }}}
                         )
# ATTENTION: this applies the new style 'combostyle' to all ttk.Combobox
ttk_style.theme_use('combostyle')

# Set Font Across All Widgets: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-style-layer.html
# ttk_style.configure('.', font=('Helvetica', 5))

# Combobox
user_option_dropdown = ttk.Combobox(win, width='20', values=['--CHOOSE ACTION--',
                                                             'Download Video',
                                                             'Convert Audio',
                                                             'Generate Metrics File',
                                                             'Generate Transcript',
                                                             'Generate Youtube Transcript'
                                                             ])
user_option_dropdown.current(0)
user_option_dropdown.grid(row=0, column=13)
user_option_dropdown.bind('<<ComboboxSelected>>', display_user_choice)

# Close Button
closeButt = Button(win, text='X', highlightbackground='red', command=win.destroy)
closeButt.grid(row=0, column=16, sticky=W)

##############################
# Progress Bar

# Progress Bar Style
ttk_style = ttk.Style()
ttk_style.theme_create('barstyle', parent='alt', settings={'TProgressbar': {'configure': {'thickness': '1', }}})

# ATTENTION: this applies the new style 'barstyle' to all ttk.Progressbar
ttk_style.theme_use('barstyle')

# Call Style and Change Progress Bar to green
s = ttk.Style()
s.configure('TProgressbar', background='green', troughcolor='grey', relief=SUNKEN)

# Progress bar
progress_var = DoubleVar()  # Here you have ints but when calc. %'s usually floats
MAX = 100   # Progress Bar Max Value
progress = ttk.Progressbar(win, orient=HORIZONTAL, variable=progress_var, maximum=MAX, length=100, mode='determinate')
progress.grid(row=1, column=0, columnspan=30, sticky='WE')
progressbar_status = True


def run_progress_1():
    # this is used for dev purposes
    global progressbar_status
    if progressbar_status:
        progressbar_status = False
        progress.start()
    else:
        progressbar_status = True
        progress.stop()


def run_progress_2():
    # this is used for dev purposes
    global progressbar_status
    if progressbar_status:
        progressbar_status = False
        k = 0
        while k <= MAX:
            # some work to be done
            progress_var.set(k)
            if progress_var.set(k) == 25:
                print('One quarter complete')
            elif progress_var.set(k) == 50:
                print('One quarter complete')
            elif progress_var.set(k) == 75:
                print('Three quarters complete')
            elif progress_var.set(k) == 100:
                print('Finished!')
            k += 1
            time.sleep(0.02)
            win.update()
    else:
        pass
        # progress_var.set(0)
        # win.update()
        # progressbar_status = True



    # some work to be done
    progress_var.set(k)
    k += 1
    time.sleep(0.02)
    win.update()

# Progress Button | this is used for dev purposes
progressButt = Button(win, text='1', highlightbackground='black', command=run_progress_1)
progressButt.grid(row=0, column=17, sticky=W)

# Progress Button | this is used for dev purposes
progressButt2 = Button(win, text='2', highlightbackground='black', command=run_progress_2)
progressButt2.grid(row=0, column=18, sticky=W)

win.mainloop()



