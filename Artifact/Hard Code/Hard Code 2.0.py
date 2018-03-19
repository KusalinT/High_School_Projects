from visual import *
from math import asin,sin,cos

def calc_tinker(index,switch,theta):
    sign=theta/abs(theta)
    if not switch:
        tinker=0
    elif index==0:
        tinker=1
    elif index==1:
        tinker=-1
    elif index>=2 and abs(theta)>0.001:
        tinker=0
    elif index>=2 and abs(theta)<=0.001 and switch==True:
        tinker=-1
        switch=0
    elif switch==0:
        tinker=1
    return tinker,index+1,switch
        

floor = box(pos=(0,-2,0),size=(64,4,24),color=(30,30,30))
cart = box(pos=(0,4,0), size=(16,8,16), color=color.cyan)
ball = sphere (pos=(4,24,0), radius=4, color=color.blue)
bar = cylinder (pos=cart.pos, axis=ball.pos-cart.pos, radius=1.2, color=color.red)

rodlength=20
g=9.81
dtheta=0
dt=0.01
cor=1 #coefficient of restitution 
dx=0
k=5 #0.3*dt with x**3
comp=True
kfact=False
damp=False
tink=True
switch=[False,False]
index,tinker=0,0


theta=math.asin((ball.pos.x-cart.pos.x)/rodlength)

while True:
    #limit checks
    if (ball.pos.y-ball.radius-(floor.size.y)*.5)<floor.pos.y:
        dtheta=(-dtheta)*cor

##    if ((ball.pos.x+ball.radius)>(floor.pos.x+floor.size.x/2)
##        or (ball.pos.x-ball.radius)<(floor.pos.x-floor.size.x/2)):
##        print("out of range")
##        thetadotdot=(-thetadotdot)
##        theatadot=(-thetadot)*cor
##    if ((cart.pos.x+cart.size.x/2)>(floor.pos.x+floor.size.x/2)
##        or (cart.pos.x-cart.size.x/2)<(floor.pos.x-floor.size.x/2)):
##        xdot=(-xdot)
        
##    #debugging
##    print(ball.pos.x-cart.pos.x)
##    print((ball.pos.x-cart.pos.x)-abs(ball.pos.x-cart.pos.x))
##    print("b"+str(ball.pos.x))
##    print(cart.pos.x)
        
    #calculations for motion of ball
    rate(100)
    oldballpos=ball.pos.x
##    initthetadot = thetadot
    ddtheta=(g/rodlength)*math.sin(theta)*dt
    dtheta+=ddtheta*dt
##    theta+=(thetadot+initthetadot)/2
    theta+=dtheta
    ball.pos.x=(cart.pos.x)+(rodlength*math.sin(theta))
    ball.pos.y=(cart.pos.y)+(rodlength*math.cos(theta))
    bar.axis=ball.pos-cart.pos
    bar.pos=cart.pos
##    print(ball.pos.x-oldballpos)
    print(cart.pos.x)
    
    if comp:
        #calculations for cart compensation
        x=(ball.pos.x-cart.pos.x)
        l=rodlength
##        oldxdot = xdot
        ddx=(l*(math.sin(ddtheta+math.asin((x-dx)/l))))-x+dx
        if tink:
            sign=(theta/abs(theta))
            if theta>0 and not switch[0]:
                tinker=10*sign
                switch[0]=True
            elif switch[0] and abs(theta)>0.001:
                tinker=0
            elif not switch[1]:
                tinker=-10*sign
                switch[1]=True
            else:
                tinker=0

##        if abs(theta)>0.1:
##            switch[0]=True
##        if switch[0]:
##            tinker,index,switch[0],=calc_tinker(index,switch[0],theta)
                 
        if kfact:
            ddx+=k*(theta)

        oldddx=ddx
        ddx=ddx +tinker
        olddx=dx
        dx+=ddx*dt #+tinker
##        cart.pos.x+=(oldxdot+xdot)/2
        cart.pos.x+=dx
        

    if damp:
        k-=dt**3

    theta=math.asin((ball.pos.x-cart.pos.x)/rodlength)

    
