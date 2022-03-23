import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from threading import *
from pytube import YouTube

file_size = 0


def complete_download(stream=None, file_path=None):
    print("Download Concluído com sucesso!")
    showinfo("Mensagem", "Video baixado com sucesso.")
    btn['text'] = "Download"
    btn['state'] = "active"
    tInput.delete(0, tk.END)
    progressbar['value'] = 1


def progress_download(stream=None, chunk=None, bytes_remaining=None):
    percent = (100 * ((file_size - bytes_remaining) / file_size))
    btn['text'] = "{:00.0f}% downloaded ".format(percent)
    progressbar['value'] = percent
    root.update_idletasks()


def start_download(url):
    global file_size
    path_to_save = askdirectory()
    if path_to_save is None:
        return

    try:
        yt = YouTube(url)
        print("Instanciado a classe")
        stream = yt.streams.filter(file_extension="mp4", res="720p").first()
        print("Stream localizado")
        yt.register_on_complete_callback(complete_download)
        yt.register_on_progress_callback(progress_download)

        file_size = stream.filesize
        stream.download(output_path=path_to_save)
        print("Download Iniciado")
    except Exception as e:
        print(e)
        print("Algo deu errado")


# this is a function to get the user input from the text input box
def getInputBoxValue():
    userInput = tInput.get()
    return userInput


# this is the function called when the button is clicked
def btnClickFunction():
    try:
        btn['text'] = "Aguarde..."
        btn['state'] = "disabled"
        url = tInput.get()
        if url == "":
            btn['text'] = "Download"
            btn['state'] = "active"
            return
        print(url)
        thread = Thread(target=start_download, args=(url,))
        thread.start()

    except Exception as e:
        print(e)


# This is a function which increases the progress bar value by the given increment amount
def makeProgress():
    progressbar['value'] = progressbar['value'] + 1
    root.update_idletasks()
    return progressbar['value']


root = Tk()

# This is the section of code which creates the main window
root.geometry('480x210')
root.configure(background='#CFCFCF')
root.title('Youtube Downloader')

# This is the section of code which creates the a label
Label(root, text='Insira o Link do video:', bg='#CFCFCF', font=('helvetica', 11, 'normal')).place(x=17, y=100)

# This is the section of code which creates a text input box
tInput = Entry(root)
tInput.place(x=167, y=100)

# This is the section of code which creates a button
btn = Button(root, text='Download', bg='#CFCFCF', font=('helvetica', 11, 'normal'), command=btnClickFunction)
btn.place(x=317, y=90)

# This is the section of code which creates a color style to be used with the progress bar
progressbar_style = ttk.Style()
progressbar_style.theme_use('clam')
progressbar_style.configure('progressbar.Horizontal.TProgressbar', foreground='#FF4040', background='#FF4040')

# This is the section of code which creates a progress bar
progressbar = ttk.Progressbar(root, style='progressbar.Horizontal.TProgressbar', orient='horizontal', length=440,
                              mode='determinate', maximum=100, value=1)
progressbar.place(x=18, y=163)

# First, we create a canvas to put the picture on
youtubepicture = Canvas(root, height=48, width=48)
# Then, we actually create the image file to use (it has to be a *.gif)
picture_file = PhotoImage(
    file='')  # <-- you will have to copy-paste the filepath here, for example 'C:\Desktop\pic.gif'
# Finally, we create the image on the canvas and then place it onto the main window
youtubepicture.create_image(48, 0, anchor=NE, image=picture_file)
youtubepicture.place(x=207, y=20)

root.mainloop()
