from socket import *
from threading import *
from tkinter import *

sendFlag = 0
flag = 0

def sendMsgUtil():
    global sendFlag
    sendFlag = 1

def sendMsg(connection, add):
    
    while True:
        re = ''
        global sendFlag

        while(sendFlag != 1):
            pass
            
        re = input_sendMsg.get()
        sendFlag = 0
        input_sendMsg.delete(0, END)
        global flag

        if flag == 0:
            connection.send(re.encode('UTF-8'))
            if re == '!':
                break

            
        else:
            flag = 0
            break

def receiveMsg(connection, add):

    while True:
        re = connection.recv(1024).decode('UTF-8')
        
        if re:
            text_receivedMsg.configure(text = f'Server: {re}')
            
            if re == '!!':
                break
            
            if re == '!':
                global flag
                flag = 1
                re += '!'
                connection.send(re.encode('UTF-8'))
                break

def main(client, address):

    thread1 = Thread(target = sendMsg, args = (client, address))
    thread2 = Thread(target = receiveMsg, args = (client, address))

    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()

    client.close()

def getIPPort():

    address, port = input_PortIP.get().split(':')
    port = int(port)

    if port < 0 and port > 65535:
        print('Error: Port  number out of range')
        return -1

    return address, port

def connectToSocket():

    address, port = getIPPort()

    client = socket(AF_INET, SOCK_STREAM)
    client.connect((address, port))

    button_connect.configure(state = DISABLED)
    text_PortIP.configure(state = DISABLED)
    input_sendMsg.configure(state = NORMAL)
    input_PortIP.configure(state = DISABLED)
    button_sendMsg.configure(state = NORMAL)
    text_connStatus.configure(text = 'STATUS: Connected')

    mainthread = Thread(target = main, args = (client, 5))

    text_receivedMsg.configure(text = 'Connected')
    mainthread.start()

window = Tk()

window.geometry("650x380")
window.title("LAN Messanger: Client")

text_PortIP = Label(    window, 
                        font = ('Arial', 13),
                        text = 'Enter IP and Port: ',
                        padx = 8)

text_PortIP.place(  y = 20,
                    anchor  = NW)

input_PortIP = Entry(   window,
                        font = ('Arial', 13), 
                        width = 40)

input_PortIP.place( y = 51,
                    x = 13,
                    anchor = NW)

text_connStatus = Label(    window,
                            borderwidth = 3,
                            font = ('Arial', 13),
                            text = 'STATUS: Waiting For Connection',
                            padx = 3,
                            pady = 3,
                            width = 39,
                            height = 1)

text_connStatus.place(      relx = 0.02,
                            rely = 0.21)

button_connect = Button(    window,
                            command = connectToSocket,
                            text = 'CONNECT',
                            font = ('Arial', 17, 'bold'),
                            relief = RAISED,
                            bd = 5,
                            bg = 'white',
                            fg = 'black',
                            activebackground = 'white',
                            activeforeground = 'grey',
                            state = ACTIVE)

button_connect.place(   relx = 0.927,
                        rely = 0.12,
                        x =- 2,
                        y = 2,
                        anchor = NE)

text_receivedMsg = Label(   window,
                            borderwidth = 3,
                            font = ('Arial', 13),
                            text = 'Not Connected',
                            padx = 30,
                            pady = 30,
                            bg = 'white',
                            width = 58,
                            height = 3)

text_receivedMsg.place(     relx = 0.0199999,
                            rely = 0.35)

input_sendMsg = Entry(  window,
                        font=('Arial', 13),
                        width = 65,
                        state = DISABLED)

input_sendMsg.place(    relx = 0.0199999,
                        rely = 0.7)

button_sendMsg = Button(    window,
                            command = sendMsgUtil,
                            text = 'SEND MSG',
                            font = ('Arial', 11, 'bold'),
                            relief = RAISED,
                            bd = 5,
                            bg = 'white',
                            fg = 'black',
                            activebackground = 'white',
                            activeforeground = 'grey',
                            state = DISABLED)

button_sendMsg.place(   relx = 0.77,
                        rely = 0.8)

window.mainloop()