import pygame
from pygame.locals import *
import sys
from enigma.machine import EnigmaMachine



red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)
yellow = (255,242,0)

map={1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H',9:'I',10:'J',11:'K',12:'L',13:'M',14:'N',15:'O',16:'P',17:'Q',18:'R',19:'S',20:'T',21:'U',22:'V',23:'W',24:'X',25:'Y',26:'Z'}



color=white

screen = pygame.display.set_mode((0,0),pygame.RESIZABLE)


#Screen class
class Pane(object):
    
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont('Arial', 25)
        pygame.display.set_caption("Enigma")
        self.screen=pygame.display.set_mode((0,0),pygame.RESIZABLE)
        self.r1Count=self.r2Count=self.r3Count=1
        #Adding hooks
        pygame.draw.lines(self.screen,yellow,False,[(620,260),(650,260)],5)
        pygame.draw.lines(self.screen,yellow,False,[(310,260),(340,260)],5)
        #border lines
        pygame.draw.lines(self.screen,white,False,[(0,500),(1600,500)],5)
        pygame.draw.lines(self.screen,white,False,[(750,0),(750,1500)],5)
        #Initalizing enigma
        self.machine = EnigmaMachine.from_key_sheet(
            rotors='II IV V',
            reflector='B',
            ring_settings=[1, 20, 11],
            plugboard_settings='AV BS CG DL FU HZ IN KM OW RX')
        self.f = open("output.txt", "a")
        self.x=850
        self.y=100
        self.count=0

        #Output screen
        pygame.draw.rect(self.screen,white,(850,100,600,300))
        #Reset button
        pygame.draw.rect(self.screen,white,(440,400,70,40))
        self.reset=self.screen.blit(self.font.render("RESET", True, black), (440, 400))

    def addText(self,letter,x,y):
        self.screen.blit(self.font.render(letter, True, black), (x+10, y))

    def modRound(self,num,check):
    	if check==1:
    		if num+1==27:
    			return 1
    		return (num+1)%27
    	elif check==-1:
    		if num-1==0:
    			return 26
    		return (num-1)%27
    	elif check==0:
    		if num==0:
    			return 1
    		return num%27

    def rotorRoll(self,letter):
        keys=pygame.key.get_pressed()
        for i in range( pygame.K_a, pygame.K_z + 1 ): 
            if keys[i] == True:
                if self.r3Count==26:
                    self.r3Count=1
                    if self.r2Count==26:
                        self.r2Count=1
                        if self.r1Count==26:
                            self.r1Count=1
                        else:
                            self.r1Count+=1
                    else:
                        self.r2Count+=1
                else:
                    self.r3Count+=1
                self.machine.set_display(map[self.r1Count]+map[self.r2Count]+map[self.r3Count])
                print(map[self.r1Count]+map[self.r2Count]+map[self.r3Count])
                output=self.machine.process_text(letter)
                self.f.write(output)
                self.addText(output,self.x,self.y)
                self.x+=20
                self.count+=1
                if self.count==29:
                    self.x=850
                    self.y+=20
                    self.count=0

    def addCircle(self,letter,x,y):
        color=white
        keys=pygame.key.get_pressed()
        if(keys[ord(letter.lower())]):
            color=yellow
            self.rotorRoll(letter)
        else:
            color=white
        self.cir = pygame.draw.circle(self.screen,color,(x,y),25)
        self.addText(letter,x-20,y-15)


    def addRotors(self):
        pos=pygame.mouse.get_pos()
        r3c3=pygame.draw.rect(self.screen,white,(550,200,50,30))
        self.screen.blit(self.font.render(str(self.modRound(self.r3Count,-1)), True, black), (550+10, 200))
        pygame.draw.rect(self.screen,white,(550,250,50,30))
        self.screen.blit(self.font.render(str(self.modRound(self.r3Count,0)), True, black), (550+10, 250))
        r3c1=pygame.draw.rect(self.screen,white,(550,300,50,30))
        self.screen.blit(self.font.render(str(self.modRound(self.r3Count,+1)), True, black), (550+10, 300))

        r2c3=pygame.draw.rect(self.screen,white,(450,200,50,30))
        self.screen.blit(self.font.render(str(self.modRound(self.r2Count,-1)), True, black), (450+10, 200))
        pygame.draw.rect(self.screen,white,(450,250,50,30))
        self.screen.blit(self.font.render(str(self.modRound(self.r2Count,0)), True, black), (450+10, 250))
        r2c1=pygame.draw.rect(self.screen,white,(450,300,50,30))
        self.screen.blit(self.font.render(str(self.modRound(self.r2Count,+1)), True, black), (450+10, 300))

        r1c3=pygame.draw.rect(self.screen,white,(350,200,50,30))
        self.screen.blit(self.font.render(str(self.modRound(self.r1Count,-1)), True, black), (350+10, 200))
        pygame.draw.rect(self.screen,white,(350,250,50,30))
        self.screen.blit(self.font.render(str(self.modRound(self.r1Count,0)), True, black), (350+10, 250))
        r1c1=pygame.draw.rect(self.screen,white,(350,300,50,30))
        self.screen.blit(self.font.render(str(self.modRound(self.r1Count,+1)), True, black), (350+10, 300))

        
        if r3c3.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
        	self.r3Count=self.modRound(self.r3Count,-1)
        	r3c3=pygame.draw.rect(self.screen,white,(550,200,50,30))
        	self.screen.blit(self.font.render(str(self.modRound(self.r3Count,-1)), True, black), (550+10, 200))


        if r3c1.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            self.r3Count=self.modRound(self.r3Count,1)
            r3c1=pygame.draw.rect(self.screen,white,(550,300,50,30))
            self.screen.blit(self.font.render(str(self.modRound(self.r3Count,+1)), True, black), (550+10, 300))

        if r2c3.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
        	self.r2Count=self.modRound(self.r2Count,-1)
        	r2c3=pygame.draw.rect(self.screen,white,(450,200,50,30))
        	self.screen.blit(self.font.render(str(self.modRound(self.r2Count,-1)), True, black), (450+10, 200))


        if r2c1.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            self.r2Count=self.modRound(self.r2Count,1)
            r2c1=pygame.draw.rect(self.screen,white,(450,300,50,30))
            self.screen.blit(self.font.render(str(self.modRound(self.r2Count,+1)), True, black), (450+10, 300))

        if r1c3.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
        	self.r1Count=self.modRound(self.r1Count,-1)
        	r1c3=pygame.draw.rect(self.screen,white,(350,200,50,30))
        	self.screen.blit(self.font.render(str(self.modRound(self.r1Count,-1)), True, black), (350+10, 200))


        if r1c1.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            self.r1Count=self.modRound(self.r1Count,1)
            r1c1=pygame.draw.rect(self.screen,white,(350,300,50,30))
            self.screen.blit(self.font.render(str(self.modRound(self.r1Count,+1)), True, black), (350+10, 300))
        
        if self.reset.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            self.r3Count=self.modRound(1,0)
            self.r2Count=self.modRound(1,0)
            self.r1Count=self.modRound(1,0)
            self.x=850
            self.y=100
            self.count=0
            pygame.draw.lines(self.screen,white,False,[(0,500),(1600,500)],5)
            pygame.draw.rect(self.screen,white,(850,100,600,300))
            self.f.write("   ")
            
        pygame.display.update()

     
run = True

clock = pygame.time.Clock()

Pane1=Pane()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        keys=pygame.key.get_pressed()
        
        Pane1.addCircle('Q',100,600)
        Pane1.addCircle('W',160,600)
        Pane1.addCircle('E',220,600)
        Pane1.addCircle('R',280,600)
        Pane1.addCircle('T',340,600)
        Pane1.addCircle('Y',400,600)
        Pane1.addCircle('U',460,600)
        Pane1.addCircle('I',520,600)
        Pane1.addCircle('O',580,600)
        Pane1.addCircle('P',640,600)

        Pane1.addCircle('A',130,700)
        Pane1.addCircle('S',190,700)
        Pane1.addCircle('D',250,700)
        Pane1.addCircle('F',310,700)
        Pane1.addCircle('G',370,700)
        Pane1.addCircle('H',430,700)
        Pane1.addCircle('J',490,700)
        Pane1.addCircle('K',550,700)
        Pane1.addCircle('L',610,700)

        Pane1.addCircle('Z',180,800)
        Pane1.addCircle('X',240,800)
        Pane1.addCircle('C',300,800)
        Pane1.addCircle('V',360,800)
        Pane1.addCircle('B',420,800)
        Pane1.addCircle('N',480,800)
        Pane1.addCircle('M',540,800)
        if event.type==pygame.KEYUP:
            continue

    Pane1.addRotors()            

    pygame.display.update()
    pygame.display.flip()
    clock.tick(7)
pygame.quit()
