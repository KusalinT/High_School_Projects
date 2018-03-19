from visual import *
from math import atan,sin,cos
from random import randint

#dt=0.01

def calc_theta(x,y):
    theta=math.atan(x/y)
    if y<0:
        if x>0:
            theta+=pi
        else:
            theta-=pi
    return theta

def mutate(x):
    #needs to change
    dice=random.randint(1,100)
    randnum=random.randint(0,500)/100
    if dice<=10:
        x-=randnum
    elif dice>=90:
        x+=randnum
    return x

def give_score(code):
    score=0
    ballmass,ballposx,ballposy=0.2,1,6 #starting theta calculated by this
    cartmass,cartposx,cartposy=0.5,0,1
    rodlength=5
    g=9.81
    dt=0.01
    dtheta,ddx,dx=0,0,0
    theta=math.asin((ballposx-cartposx)/rodlength)
    for subforce in code:
        F=subforce
        
        ddtheta=((ddx*math.cos(theta))+(g*math.sin(theta)))/rodlength
        dtheta+=ddtheta*dt
        theta+=dtheta*dt

        ddx=-(F+ballmass*rodlength*(ddtheta*math.cos(theta)-(dtheta**2)*math.sin(theta)))/(cartmass+ballmass)
        dx+=ddx*dt 
        cartposx+=dx*dt
        
        ballposx=(cartposx)+(rodlength*math.sin(theta))
        ballposy=(cartposy)+(rodlength*math.cos(theta))

        score+=5*(theta**2)
        score+=(dx**2)
        score+=999*(cartposx)
        theta=calc_theta(ballposx-cartposx,ballposy-cartposy)
        
    return score

def display(code):
    strip1= box(pos=(0,-0.5,2),size=(16,1,1),color=(30,30,30))
    strip2= box(pos=(0,-0.5,-2),size=(16,1,1),color=(30,30,30))
    cart = box(pos=(0,1,0), size=(4,2,4), color=color.cyan)
    ball = sphere (pos=(1,6,0), radius=1, color=color.blue)
    bar = cylinder (pos=cart.pos, axis=ball.pos-cart.pos, radius=0.3, color=color.red)

    ball.mass=0.2
    cart.mass=0.5
    rodlength=5
    g=9.81
    dt=0.01
    dtheta,ddx,dx=0,0,0

    theta=math.asin((ball.pos.x-cart.pos.x)/rodlength)
   
    for subforce in code:
        rate(100)
        F=subforce

        ddtheta=((ddx*math.cos(theta))+(g*math.sin(theta)))/rodlength
        dtheta+=ddtheta*dt
        theta+=dtheta*dt

        ddx=-(F+ball.mass*rodlength*(ddtheta*math.cos(theta)-(dtheta**2)*math.sin(theta)))/(cart.mass+ball.mass)
        dx+=ddx*dt
        cart.pos.x+=dx*dt
    
        ball.pos.x=(cart.pos.x)+(rodlength*math.sin(theta))
        ball.pos.y=(cart.pos.y)+(rodlength*math.cos(theta))
        bar.axis=ball.pos-cart.pos
        bar.pos=cart.pos

        theta=calc_theta(ball.pos.x-cart.pos.x,ball.pos.y-cart.pos.y)
        
class Force:
    def __init__(self,seedcode):
        count=0
        for subforce in seedcode:
            seedcode[count]=mutate(subforce)
            count+=1
        self.code=seedcode

    def get_score(self):
        self.score=give_score(self.code)
        return self.score

#make seed
#make all the Force objects
#rank by their score
#make best one seed of the next generation
def survive(obj): #take in Force object and return a 'better' one
    #needs to change
    obj1=Force(obj.code)
    obj2=Force(obj.code)
    if obj.get_score()<=obj2.get_score():
        return obj1
    else:
        return obj2

def make_seed():
    stack=[]
    for count in range(0,500):
        stack.append(0)
    return stack

def main():
    seed=make_seed()
    seedforce=Force(seed)
    for gen in range(0,1000):
        print(gen)
        seedforce=survive(seedforce)
    last=seedforce
    display(last.code)

main()
        
        
        
