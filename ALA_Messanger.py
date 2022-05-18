import json
import uuid
import requests
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
global Name
Name = ""
name = ""
ID = uuid.uuid1()
print(ID)
win = Tk()
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

class Command:
    def __init__(self,function,call):
        self.function = function
        self.call = call

def Close():
    global checkThread
    global Active
    Active = False
    win.destroy()
    checkThread.join()

def Message(name,message):
    global ID
    url = f"https://blakewerlinger.pythonanywhere.com/message?name={name}&message={message}&id={ID}"
    response = requests.post(url)
    content = response.content.decode()
    jsonContent = json.loads(content)
    return jsonContent

def CloseName(t):
    print(t)
    print(Name)
    if (t == Name):
        Close()

global Commands
Commands = [Command(CloseName,"close")]

def ParseCommands(message):
    for com in Commands:
        if (f"/{com.call}" in message and message.index(f"/{com.call}") == 0):
            param = message.split()[1]
            com.function(param)
            



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
        if ('id' in jsonContent):
            messageID = jsonContent['id']
            currentString = f"{messageAuthor}: {messageMessage} \n ({messageTime} \n {messageID})"
        else: 
            currentString = f"{messageAuthor}: {messageMessage} \n ({messageTime})"
        label.config(text=f"New Message: \n {currentString}")
        label.pack(pady=30)
        win.update()
        ParseCommands(messageMessage)
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




def SendMessage():
    message = entry.get()
    name = nameEntry.get()
    global Name
    Name = name
    Message(name,message)
    entry.delete(0, 'end')
    
ttk.Button(win,text= "Send Message", command= SendMessage).pack(pady=20)
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        Close()

if __name__ == '__main__':
    global checkThread
    checkThread = threading.Thread(target=MessageLoop)
    checkThread.start()
    win.protocol("WM_DELETE_WINDOW", on_closing)
    win.mainloop()


