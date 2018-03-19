from visual import *
from math import asin,sin, cos

floor = box(pos=(0,-0.5,0),size=(16,1,6),color=(30,30,30))
cart = box(pos=(0,1,0), size=(4,2,4), color=color.cyan)
ball = sphere (pos=(1,6,0), radius=1, color=color.blue)
bar = cylinder (pos=cart.pos, axis=ball.pos-cart.pos, radius=0.3, color=color.red)

ballmass=1
rodlength=5
g=9.81
thetadot=0
dt=0.01
cor=1 #coefficient of restitution 
xdot=0
comp=True
k=0.45*dt #0.3*dt with x**3
kfact=True
damp=True

theta=math.asin((ball.pos.x-cart.pos.x)/rodlength)

while True:
    #limit checks
    if (ball.pos.y-ball.radius-(floor.size.y)*.5)<floor.pos.y:
        thetadot=(-thetadot)*cor
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
    thetadotdot=(g/rodlength)*math.sin(theta)*(dt**2)
    thetadot+=thetadotdot
    theta+=thetadot
    ball.pos.x=(cart.pos.x)+(rodlength*math.sin(theta))
    ball.pos.y=(cart.pos.y)+(rodlength*math.cos(theta))
    bar.axis=ball.pos-cart.pos
    bar.pos=cart.pos
    
    if comp:
        #calculations for cart compensation
        x=(ball.pos.x-cart.pos.x)
        l=rodlength
        xdotdot=(l*(math.sin(thetadotdot+math.asin((x-xdot)/l))))-x+xdot
        if kfact:
            xdotdot+=k*(x)
        xdot+=xdotdot
        cart.pos.x+=xdot

    if damp:
        k-=dt**3

    theta=math.asin((ball.pos.x-cart.pos.x)/rodlength)

    
