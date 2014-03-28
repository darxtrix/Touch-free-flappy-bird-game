from pygame import image,transform

MAX_SPEED = 15


class Bird():
    def __init__(self, y, gravity):
        img1 = image.load('bird.png').convert_alpha()
        self.img= transform.scale(img1,(60,60))
        self.speedY = 0
        self.rect = self.img.get_rect().move(200, y)# getting the new position after moving 
        self.oldY = y
        self.gravity = gravity

    def fly(self,a):
        self.rect.y = a
  

    def die(self):
        self.rect.y = self.oldY
        self.speedY = 0

    def checkCollisions(self, pipes):
        for pipe in pipes:
            if self.rect.colliderect(pipe.rect):
                return True
        return False


class Pipe():
    def __init__(self, x, y):
        self.img = image.load('pipe.png').convert_alpha()
        self.rect = self.img.get_rect().move(x, y)
        self.lifetime = 0

    def fly(self):
        self.rect = self.rect.move(-5, 0)
        self.lifetime += 1
        
    
