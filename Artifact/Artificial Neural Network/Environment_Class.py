#Seperate Environment file

import pygame as pg
import numpy as np
from numpy import sin,cos
from time import sleep
from math import pi
#(56,141,237)
class IP_env:
    def __init__(self):
        self.mag=200 #magnification for visuals
        self.display_width=800
        self.display_height=800
        
        self.mass=1.1 #mass of pendulum and cart
        self.pmass=.1 #mass of pendulum
        self.length=0.5 #rod length
        self.g=9.8 #Gravitational freefall acceleration
        self.forcemultiplier=10 #force of fixed 10 Newtons
        self.ang=0.1 #angle
        self.ang_vel=0 #angular velocity
        self.pos=0 #cart position
        self.vel=0 #cart velocity
        self.fps=50 #frames per second ??
        self.dt=(self.fps)**-1
        self.clock=pg.time.Clock() #clock object

        pg.init()
        self.display = pg.display.set_mode((self.display_width,self.display_height))
        pg.display.set_caption("Inverted Pendulum")
    def update_window(self):
        pposx=(self.length*sin(self.ang))*self.mag #calculate pendulum position relative to cart
        pposy=(self.length*cos(self.ang))*self.mag
        pposx=400+self.pos*self.mag+pposx
        pposy=375-pposy
        self.display.fill((237, 169, 35))
        #draw objects, make sure magnification is right
        pg.draw.rect(self.display,(56,141,237),[350+self.pos*self.mag,375,100,50])
        pg.draw.line(self.display,(0,0,0),(400+self.pos*self.mag,375),(pposx,pposy),5)
        pg.draw.circle(self.display,(100,20,30),(int(pposx),int(pposy)),20)
        pg.display.update()
    def close_window(self):
        pg.quit()
    def correct_angle(self): #keep the angle in range [-pi,pi]
        if self.ang>pi:
            self.ang=-2*pi+self.ang
        elif self.ang<-pi:
            self.ang=2*pi+self.ang
    def step(self,action): #take the action, give observations for next timestep
        if action==0: #0 inputted is move to the left
            action=-1
        elif action==-1:#-1 inputted is for testing oscillation with no drive
            action=0
        
        #calculate next state variables
        F=action*self.forcemultiplier
        ang_acc=((self.mass*self.g*sin(self.ang) #calculate second order derivs
                 -cos(self.ang)*(F+self.pmass*self.length*sin(self.ang)*
                                 (self.ang_vel)**2))
                 /(((4/3)*self.mass*self.length)-self.pmass*self.length*
                   (cos(self.ang))**2))
        
        cart_acc=((F+(self.pmass*self.length*((sin(self.ang)*self.ang_vel**2)
                                              -(ang_acc*cos(self.ang)))))
                  /self.mass)
        self.ang+=self.ang_vel*self.dt
        self.ang_vel+=ang_acc*self.dt #calculate state variables after action taken
        self.pos+=self.vel*self.dt
        self.vel+=cart_acc*self.dt

        if (-pi/12)<self.ang<(pi/12)and(-2.4<self.pos<2.4): #if pendulum still in range, give reward
            reward=1
            done=False
        else: reward,done=0,True
        info=None
        return np.array([self.ang,self.ang_vel,self.pos,self.vel]),reward,done,info #observations after action taken
    def reset(self,init_obs=[0.1,0,0,0]):
        self.ang=init_obs[0] #angle
        self.ang_vel=init_obs[1] #angular velocity
        self.pos=init_obs[2] #cart position
        self.vel=init_obs[3] #cart velocity
        #self.update_window() #update visuals
    def get_obs(self): #return observations at that timestep
        return np.array([self.ang,self.ang_vel,self.pos,self.vel])
    def rendergame(self,obs_list): #produce visuals for a game
        for obs in obs_list:
            print(obs)
            self.clock.tick(self.fps)
            self.ang=obs[0]
            self.pos=obs[1]
            self.update_window()
            
    
if __name__=="__main__": #for checking code
    m=IP_env()
    m.update_window()
    init_obs=m.get_obs()
    obs_list=[]
    obs_list.append([init_obs[0],init_obs[2]])
    for _ in range(5000):
        obs,reward,done,info=m.step2()
        obs_list.append([obs[0],obs[2]])
        if done:
            pass
    print(len(obs_list))
    m.rendergame(obs_list)
    m.close_window()
