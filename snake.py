#coding:utf-8

from __future__ import print_function
import os
import time
import random
import threading
from pynput import keyboard

map =[[' ' for i in range (0,51)] for i in range(0,26)]
snk =[[0 for i in range(0,2)] for i in range(0,1251)]
slen =0
dx=0;dy=0
judge =True
speed=1
gameflag=1
pauseflag='p'

def init():
    global slen,judge,dx,dy,map,snk,pauseflag,gameflag

    for i in range(0,26):
        for j in range(0,51):
            map[i][j]=' '

    for i in range(0,51):
        map[25][i]='-'
    for i in range(0,26):
        map[i][50]='|'
    map[12][25]=map[13][25]=map[14][25]=map[15][25]='#'

    dx=-1;dy=0
    slen=4
    snk[0]=[15,25];snk[1]=[14,25];snk[2]=[13,25];snk[3]=[12,25]
    map[random.randint(1,24)][random.randint(1,49)] ='0'
    judge=True
    pauseflag='r';gameflag=1

#--------------------------------------------------------------------

def foward():
    global judge,map,slen,snk,dx,dy
    eat =False
    llen =slen-1

    if map[(snk[llen][0]+dx)%24][(snk[llen][1]+dy)%49]=='#': 
        judge=False

    snk[slen]=[(snk[llen][0]+dx)%25,(snk[llen][1]+dy)%50]
    if map[(snk[llen][0]+dx)%25][(snk[llen][1]+dy)%50]=='0':
        map[(snk[llen][0]+dx)%25][(snk[llen][1]+dy)%50]='#'
        slen=slen+1;eat= True
    else:
        map[(snk[llen][0]+dx)%25][(snk[llen][1]+dy)%50] = '#'

    if judge ==False:
        return

    if not eat:
        map[snk[0][0]][snk[0][1]]=' '
        for i in range (0,slen+1):
            snk[i]=snk[i+1]
    else:
        posx=random.randint(1,24);posy=random.randint(1,49)
        while map[posx][posy]=='#':
            posx = random.randint(2, 23);posy = random.randint(2, 48)
        map[posx][posy]='0'

def spd(sp):
    global speed
    if speed==1:
        return 0.1
    if speed==2:
        return 0.07
    if speed==3:
        return 0.05
    if speed==4:
        return 0.03

def show():
    global speed,map
    os.system('cls')
    print("speed: "+str(speed))
    s=''
    for i in range(0,52):
        s=s+'-'
    print(s)
    for i in range(0, 26):
        s = '|'
        for j in range(0, 51):
            s = s + map[i][j]
        print(s)    

    print("长度："+str(slen))
        
    prop = slen*100// 400
    print(" 完成度： "+str(prop) + '% ' + "▋" * (prop) + '\r', end='')


def game():
    global judge,map,snk,slen,speed,pauseflag,gameflag
    init()
    while judge and gameflag!=-1:
        # os.system('cls')
        if pauseflag=='r':
            foward()
        show()
        time.sleep(spd(speed))

    record=0
    with open("rec.txt",'r') as f:
        record=int(f.read())
    if slen>record:
        record=slen
        with open("rec.txt", 'w') as f:
            f.write(str(record))

    print("GAME OVER")
    print("历史最高： "+str(record))
    print("q for exit,r for restart")
    gameflag=0

def gamecontrol():
    global gameflag
    while gameflag!=-1:
        if gameflag==1:
            game()

#----------------------------------------------------------------
def getpre(x,y):
    global dx,dy
    if dx+x==0 and dy+y==0:
            return False
    return True

def on_press(key):
    global flag,dx,dy,pauseflag,gameflag
    if key == keyboard.KeyCode.from_char('i'):
        if getpre(-1,0):
            dx= -1;dy=0
    elif key == keyboard.KeyCode.from_char('l'):
        if getpre(0,1):
            dx= 0;dy= 1
    elif key == keyboard.KeyCode.from_char('k'):
        if getpre(1,0):
            dx=1;dy=0
    elif key == keyboard.KeyCode.from_char('j'):
        if getpre(0,-1):
            dx=0;dy=-1
    elif key == keyboard.KeyCode.from_char('q'):
        gameflag=-1
        print("exit")
        return False
    elif key ==keyboard.KeyCode.from_char('p'):
        pauseflag='p'
    elif key == keyboard.KeyCode.from_char('c'):
        pauseflag='r'
    elif key == keyboard.KeyCode.from_char('r'):
        print("restart")
        gameflag=1

def keylisten():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

#-----------------------------------------------

init()
for i in range (0,26):
    s=''
    for j in range(0,51):
        s=s+map[i][j]
    print(s)
print("i,l,k,j for deriction | p for pause | c for continue")
speed=int(input("sped[1-4](recommend 4)："))


t1=threading.Thread(target=gamecontrol)
t2=threading.Thread(target=keylisten)

t1.setDaemon(True)
t2.setDaemon(True)

t2.start()
t1.start()

t2.join()