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
            text_receivedMsg.configure(text = f'Client: {re}')

            if re == '!!':
                break

            if re == '!':
                global flag
                flag = 1
                re += '!'
                connection.send(re.encode('UTF-8'))
                break

def main(server, d):

    while True:

        connection, add = server.accept()

        input_sendMsg.configure(state = NORMAL)
        button_sendMsg.configure(state = ACTIVE)
        text_receivedMsg.configure(text = "Connected")

        thread1 = Thread(target = sendMsg, args = (connection, add))
        thread2 = Thread(target = receiveMsg, args = (connection, add))

        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

        connection.close()

        input_sendMsg.configure(state = DISABLED)
        button_sendMsg.configure(state = DISABLED)
        text_receivedMsg.configure(text = "Not Connected")

def getPort():

    port = int(input_portNo.get())

    if port < 0 and port > 65535:
        print('Error: Port  number out of range')
        return -1

    return port
    

def hostSocket():
    
    port = getPort()

    if port == -1:
        return

    address = '127.0.0.1'                       #Hosting on local host
    server = socket(AF_INET, SOCK_STREAM)
    server.bind( (address, port) )
    server.listen(1)
    button_hostSocket.configure(state = DISABLED)
    input_portNo.configure(state = DISABLED)
    mainthread = Thread( target = main, args = (server, 5) )
    mainthread.start()
    
window = Tk()

window.geometry("650x380")
window.title("LAN Messanger: Server")

text_portNo = Label(    window, 
                        font = ('Arial', 13),
                        text = 'Port Number :',
                        padx = 8 )

text_portNo.place(  y = 20, 
                    anchor = NW)

text_receivedMsg = Label(   window,
                            borderwidth = 3,
                            font = ('Arial', 13),
                            text = 'Not Connected',
                            padx = 30,
                            pady = 30,
                            bg = 'white',
                            width = 54,
                            height = 3 )

text_receivedMsg.place( relx = 0.07, 
                        rely = 0.22)

input_portNo = Entry(   window, 
                        font = ('Arial', 13) )

input_portNo.place( y = 21, 
                    x = 130, 
                    anchor = NW)

button_hostSocket = Button( window,
                            command = hostSocket,
                            text = 'Start Listening',
                            font = ('Arial', 11, 'bold'),
                            relief = RAISED,
                            bd = 5,
                            bg = 'white',
                            fg = 'black',
                            activebackground = 'white',
                            activeforeground = 'grey',
                            state = ACTIVE )

button_hostSocket.place(    relx = 0.92, 
                            rely = 0.025, 
                            x = -2,                                     #x/y horizontal offsets
                            y = 2, 
                            anchor = NE )                               #Spot where other widgets refer to north west


input_sendMsg = Entry(  window,
                        font = ('Arial', 13),
                        width = 61,
                        state = DISABLED )

input_sendMsg.place(    relx = 0.07, 
                        rely = 0.6)

button_sendMsg = Button(    window,
                            command = sendMsgUtil,          #function to call when pressed
                            text = 'SEND MSG',
                            font = ('Arial', 11, 'bold'),
                            relief = RAISED,                #button border type
                            bd = 5,                         #border width
                            bg = 'white',                   #background color
                            fg = 'black',                   #foreground color
                            activebackground = 'white',     #color when widget has focus
                            activeforeground = 'grey',
                            state = DISABLED )              #Grey colored when mouse is not over it

button_sendMsg.place(   relx = 0.767,                       #relx/rely relative horizontal and vertical positions to parent 
                        rely = 0.7)

window.mainloop()