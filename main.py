from ast import While
import json
import requests
import tkinter as tk
import time
from tkinter import *
from tkinter import ttk
from plyer import notification
import threading
from tkinter import messagebox
global Active
Active = True
checkedMessage: int = 0
global currentString
currentString: str = ""
global mostRecentMessage
mostRecentMessage = None
def Message(name,message):
    url = f"https://blakewerlinger.pythonanywhere.com/message?name={name}&message={message}"
    response = requests.post(url)
    content = response.content.decode()
    jsonContent = json.loads(content)
    return jsonContent

def CheckForMessage():
    global currentString
    global mostRecentMessage
    global checkedMessage
    url = f"https://blakewerlinger.pythonanywhere.com/check"
    response = requests.get(url)
    content = response.content.decode()
    if (content == "No new message found"):
        return None
    jsonContent = json.loads(content)
    print(f"{jsonContent} - - {mostRecentMessage}")
    if (jsonContent != mostRecentMessage):
        mostRecentMessage = jsonContent
        notification.notify(
        title = f"Message sent by: {jsonContent['name']}",
        message = jsonContent["message"],
        app_icon = None,
        timeout = 1
        )
        messageAuthor = jsonContent['name']
        messageMessage = jsonContent['message']
        messageTime = jsonContent['time']
        currentString = f"{messageAuthor}: {messageMessage} \n ({messageTime})"
        label.config(text=f"New Message: \n {currentString}")
        if (checkedMessage):
            w = win.winfo_width - 10
            frame.config(width=w)
            print(w)
        label.pack(pady=30)
        win.update()
        checkedMessage += 1
        
    
    return jsonContent

scriptOver = False
def MessageLoop():

    global Active
    while True:
        if not Active:
            break
        CheckForMessage()
        time.sleep(1)

win = Tk()
# win.iconbitmap("Iconn.ico")
win.title("ALA Messanger")
win.geometry("")
frame = LabelFrame(win, width= 400, height= 180, bd=5)
frame.pack(expand=True,fill="both")
frame.pack_propagate(False)
label= Label(frame, text= "", font= ('Arial', 12, 'italic'))
entry = ttk.Entry(frame, width= 40)
nameEntry = ttk.Entry(frame, width= 40)
entry.insert(INSERT, "Enter a message")
nameEntry.insert(INSERT, "Enter Name")
entry.pack()
nameEntry.pack()
entry.delete(0, 'end')


def SendMessage():
    message = entry.get()
    name = nameEntry.get()
    global Name
    Name = name
    Message(name,message)
    entry.delete(0, 'end')
    
ttk.Button(win,text= "Send Message", command= SendMessage).pack(pady=20)
def on_closing():
    global Active
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        Active = False
        win.destroy()
        checkThread.join()
if __name__ == '__main__':
    checkThread = threading.Thread(target=MessageLoop)
    checkThread.start()
    win.protocol("WM_DELETE_WINDOW", on_closing)
    win.mainloop()


