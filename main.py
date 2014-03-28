
import sys,os

from pygame import display, font, image, init, time, event,mixer,transform
from pygame.locals import *
from random import randrange
from helper_classes import Bird, Pipe
import os

####################

import SimpleCV
from SimpleCV import *        
from SimpleCV.Display import Display
import numpy as np

cam = Camera(0)
i = cam.getImage()
#print i.size()
d = Display(i.size())
col = Color.RED

######################

SCORE_COLOR = (255, 25, 20)
HIGHSCORE_COLOR = (0, 0, 255)
Y_SCORE_COLOR= (0,255,0 )

DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 700

factor=float(DISPLAY_HEIGHT)/480

FONT = None
FONT_SIZE = 100
HOLE_SIZE = 50

PIPE_FREQUENCY = 50
PIPE_MAXLIFETIME = 300

score = 0

highscore = 0

main_score = 0
 
mixer.init()

mixer.music.load(os.path.join(os.path.dirname(__file__),'lostlife.wav'))#load music
jump = mixer.Sound(os.path.join(os.path.dirname(__file__),'lostlife.wav'))  #load sound

mixer.music.load(os.path.join(os.path.dirname(__file__),'music.wav'))
mus = mixer.Sound(os.path.join(os.path.dirname(__file__),'music.wav'))

mixer.music.load(os.path.join(os.path.dirname(__file__),'bird_shot.wav'))
yuppie = mixer.Sound(os.path.join(os.path.dirname(__file__),'bird_shot.wav'))


def save():
    global  main_score,highscore
    if main_score >= highscore:
        highscore = main_score
        with open('save', 'a+') as f:
            f.seek(0)
            save = f.read()
            if highscore > int(save) if save.isdigit() else '0':
                f.seek(0)
                f.truncate()
                f.write(str(highscore))
            else:
                highscore= int(save)
    


def pause(display):
    global main_score
    screen = display.get_surface()

    hsfont = font.Font(FONT, 100)
    ysfont = font.Font(FONT,100)
    hs = hsfont.render("HIGH SCORE :-->" + str(highscore/2), True, HIGHSCORE_COLOR)
    
    y_score = ysfont.render("YOUR SCORE :-->"+str(main_score/2), True, Y_SCORE_COLOR)
    
    main_score = 0
    #score = 0

  
    pause_img=image.load('pause.png').convert_alpha()
    pause_img=transform.scale(pause_img, (1200, 700)) 
 
    screen.blit(pause_img, (0, 0,))
    screen.blit(hs, (200, 60))
    screen.blit(y_score, (200, 200))
    display.flip()

    while True:
        for i in event.get():
            if i.type == MOUSEBUTTONDOWN or i.type == KEYDOWN:
                    return main()
        #i = cam.getImage()
        #(r,g,b) = i[320,240]
        #print r,g,b
        #if r<80 and g<15 and b<15:
         #   return main()


def pattern():
    display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    display.set_caption('TOUCH-FREE FLAPPY')
    myfont = font.Font(FONT, FONT_SIZE)
    screen = display.get_surface()
    pt = 1
    while 1:
        i = cam.getImage()
        (r,g,b)=i[640,350]
        if r>rrm and r<rrx and g>rgm and g<rgx and b>rbm and b<rbx and pt==1:
            pt=2
        if r>grm and r<grx and g>ggm and g<ggx and b>gbm and b<gbx and pt==2:
            pt=3
        if r>yrm and r<yrx and g>ygm and g<ygx and b>ybm and b<ybx and pt==3:
            main()
                
def main():
    global score, main_score
    
    init()
    
    display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    display.set_caption('TOUCH-FREE FLAPPY')
    myfont = font.Font(FONT, FONT_SIZE)
    screen = display.get_surface()
    bird = Bird(20, 1)
    bg = image.load('background.png').convert_alpha()
    bg=transform.scale(bg, (1300, 700))
    pipes = []
    mus.play(-1)
    save()

    running = True

    while running:

        i = cam.getImage()
        f = np.array(i.getMatrix())
        '''ra1 =  f[:,120:520,2] > 150
        ra2 =  f[:,120:520,2] < 193
        ba1 =  f[:,120:520,1] > 40
        ba2 =  f[:,120:520,1] < 60
        ca1 =  f[:,120:520,0] > 70
        ca2 =  f[:,120:520,0] < 90'''
        ra1 =  f[:,120:520,2] >250
        ba1 =  f[:,120:520,1] > 250
        ca1 =  f[:,120:520,1] > 250    
        m1 = ra1 * ba1 * ca1
        #m2 = ra2 * ba2 * ca2
        m =  m1
   
  
        yc=0
        t=0
        
        for el in m:
            factor = np.sum(el)
            t = t + factor*yc
            yc = yc + 1
        
        p = np.sum(m)
        
        a=int(t/p)
        # a
      
        #a=int(factor * a)
       
        m_score = myfont.render(str(main_score/2), True, SCORE_COLOR)

        #time.Clock().tick(30)  # Set FPS to 30
        screen.blit(bg, (0, 0)) # making backgroung reappear again and again
        score += 1

        # Create new pipes
        if score % PIPE_FREQUENCY == 0:
            hole = randrange(HOLE_SIZE, DISPLAY_HEIGHT - HOLE_SIZE)# a gap is taken of 50 between top and bottom
            pipe1 = Pipe(DISPLAY_WIDTH, hole + HOLE_SIZE)
            pipe2 = Pipe(DISPLAY_WIDTH, -DISPLAY_HEIGHT + hole - HOLE_SIZE)
            pipes.extend((pipe1, pipe2))
            
          

        # 
        #Move pipes
        for pipe in pipes:
            screen.blit(pipe.img, pipe.rect)# setting the image on the surface it makes the image to actually appear on the surface
            pipe.fly()
            
            if bird.rect.right == pipe.rect.left + 10 :
                yuppie.set_volume(0.7)
                yuppie.play()
                main_score = main_score + 1
               

        # Remove old pipes
        for pipe in pipes:
            if pipe.lifetime > PIPE_MAXLIFETIME:
                pipes.remove(pipe)
        
        
        # Move the bird on the y-axis
        bird.fly(a)
        

        # Check collisions with pipes and bottom
        # If the bird is too low or touches a pipe
        if bird.rect.y >= DISPLAY_HEIGHT - bird.img.get_height() or \
                bird.checkCollisions(pipes):
                                   
            
                        bird.die()
                        mus.stop()
                        jump.play()
                        #pipes.die()
                        save()
                        pause(display)
                        main()
                        
            
        elif bird.rect.y < -HOLE_SIZE:  # The bird is too high
            bird.speedY = 1
            


        # Draw the bird and score info
        screen.blit(bird.img, bird.rect) # making the bird appear on the surface
        screen.blit(m_score, (70,60 ))

        display.flip()

if __name__ == '__main__':
    main()
