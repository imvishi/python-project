import os, pygame
from pygame.locals import *
from pygame.compat import geterror
import random,math
#classes for our game objects

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')
screen_dims=[1200,600]
flag_for_bat=0
ball=0
bat=0
blocks_hit=0
touch=0
miss=0
count=0
count1=0
pattern=[[0 for i in range(30)]for j in range(8)]
for i in range(30):
    pattern[0][i]=1
    pattern[1][i]=1
    pattern[7][i]=1
    pattern[6][i]=1
    pattern[4][i]=1

for i in range(8):
    pattern[i][0]=1
    pattern[i][1]=1
    pattern[i][29]=1
    pattern[i][28]=1
    pattern[i][15]=1
    pattern[i][16]=1

def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class dummysound:
    def play(self): pass

def load_sound(file):
    if not pygame.mixer: return dummysound()
    file = os.path.join(main_dir, 'data', file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print ('Warning, unable to load, %s' % file)
    return dummysound()


class Block(pygame.sprite.Sprite):

    def __init__(self, color, width, height,x,y):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
class Bat(pygame.sprite.Sprite):

    def __init__(self,up,down,right,left,pos,screen):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('bat.bmp', -1)
        self.image = pygame.transform.scale(self.image, (100, 6))
        self.rect.center=(screen_dims[0]/2,pos+45)
        self.angle=0
        self.original=self.image
        self.up=up
        self.down=down
        self.right=right
        self.left=left
        self.pos=pos;

    def update(self):
        keystate=pygame.key.get_pressed()
        #self.move(ball.rect.x)
        if keystate[self.up]==1:
            self.moveup()
        if keystate[self.down]==1:
            self.movedown()
        if keystate[self.right]==1:
            self.rightmove()
        if keystate[self.left]==1:
            self.leftmove()
    def move(self,t):
        if (t>0)&(t<screen_dims[0]-100):
            self.rect.x=t;
    def rightmove(self):
        if self.rect.x>0:
            self.rect.x-=4
    def leftmove (self):
        if self.rect.x<screen_dims[0]-100:
            self.rect.x+=4
    def moveup(self):
        if self.rect.y>500:
            self.rect.y-=1
    def movedown(self):
        if self.rect.y<screen_dims[1]-6:
            self.rect.y+=1

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = load_image('ball.bmp', -1)
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect=self.image.get_rect()
        self.rect.x=600
        self.rect.y=600
        self.original=self.image
        self.velocity=[1,1]
    def update(self):
        global flag_for_bat,screen_dims,blocks_hit,count
        #print self.rect
        self.rect.x+=self.velocity[0]
        self.rect.y+=self.velocity[1]
        if (self.rect.x>screen_dims[0])|(self.rect.x<0):
            self.velocity[0]=-self.velocity[0]
        if self.rect.y<0:
            self.velocity[1]=-self.velocity[1]
        if self.rect.y>screen_dims[1]:
            miss.play()
            count+=1;
            self.rect.x=bat.rect.x
            self.rect.y=bat.rect.y
            self.velocity=[2,2]
            self.velocity[1]=-self.velocity[1]
        if flag_for_bat==1:
            #touch.play()
            self.velocity[1]=-2
            self.rect.x+=self.velocity[0]*3
            self.rect.y-=3
            flag_for_bat=0
        if blocks_hit==1:
            touch.play()
            a=self.rect.x%20
            if a>10:
                a=abs(20-a)
            b=self.rect.y%20
            if b>10:
                b=abs(20-b)
            if a<b:
                self.velocity[0]=-self.velocity[0]
            else:
                self.velocity[1]=-self.velocity[1]
            blocks_hit=0
def main():
#Initialize Everything
    global flag_for_bat,ball,bat,blocks_hit,touch,miss,count1
    pygame.init()
    if pygame.mixer and not pygame.mixer.get_init():
        print ('Warning, no sound')
        pygame.mixer = None

    screen = pygame.display.set_mode(screen_dims)
    pygame.display.set_caption('Brick-Breaker')
    pygame.mouse.set_visible(0)

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 250, 250))

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    bat_list = pygame.sprite.Group()
    all_sprites_list = pygame.sprite.Group()
    block_list = pygame.sprite.Group()
    ball=Ball()
    bat = Bat(273,274,276,275,screen_dims[1],background)
    bat_list.add(bat)

    for i in range(8):
        for j in range(30):
            if pattern[i][j]==1:
                block=Block([random.randrange(255),random.randrange(255),0],40,40,40*j,40*i);
                block_list.add(block)
                all_sprites_list.add(block)
    all_sprites_list.add(bat)
    all_sprites_list.add(ball)

    #load the sound effects
    touch= load_sound('touch.wav')
    miss = load_sound('missed-ball.wav')

#Main Loop
    going = True
    t=0
    score=0
    while going:
        if count==4:
            print "you lose";
            going=0
        if count1==168:
            print "you win";
            going=0
        background.fill((0, 250, 250))
        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
        background.set_at((ball.rect.x,ball.rect.y),(0,0,0))
        hita=pygame.sprite.collide_mask(ball, bat)
        #flag_for_bat=0
        if hita:
            flag_for_bat=1

        blocks_hit_list = pygame.sprite.spritecollide(ball, block_list, True)
        for i in blocks_hit_list:
            count1+=1
        if blocks_hit_list:
            blocks_hit=1

        all_sprites_list.update()

        #Draw Everything
        screen.blit(background, (0, 0))
        all_sprites_list.draw(screen)
        pygame.display.flip()

    pygame.quit()
if __name__ == '__main__':
    main()
