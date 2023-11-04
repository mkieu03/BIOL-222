import sys, pygame
from random import randint, choice

WIDTH = 600
HEIGHT = 600

class Player(pygame.sprite.Sprite):
    speed: int = 4
    direction: list[int] = [0,0]
    rect: pygame.Rect

    def __init__(self):
        super().__init__()
        # storing images for moving amoeba and flip indexes back and forth to animate 
        walk1 = pygame.image.load('final/media/amoeba_0.png').convert_alpha()
        walk2 = pygame.image.load('final/media/amoeba_1.png').convert_alpha()
        self.playerWalk = [walk1, walk2]
        self.playerIndex = 0
        self.image = self.playerWalk[self.playerIndex]
        self.rect = self.image.get_rect(midbottom = (300, 300))
        self.dir_moving = {"up": False, "down": False, "left": False, "right": False}

    def move(self) -> None:
        # i copied this one but it doesn't work that well but sets direction and movement for amoeba 
        dir = self.direction
        if((self.dir_moving["up"] or self.dir_moving["down"]) and (self.dir_moving["left"] or self.dir_moving["right"])):
            dir = [dir[0] / 2, dir[1] / 2]
        
        self.rect.y += dir[0]
        self.rect.x += dir[1]

        # prevent player from going off screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < -20:
            self.rect.left = -20
        # top of screen is 0 and bottom is the HEIGHT 
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < -20:
            self.rect.top = -20
        

    def getKey(self, key: pygame.event.Event, pressed: bool) -> None:
        # gets the key pressed if you press a key
        move: int = self.speed
        if not pressed:
            move = -1 * move
        if key.key == pygame.K_w:
            self.direction[0] -= move
        if key.key == pygame.K_s:
            self.direction[0] += move
        if key.key == pygame.K_a:
            self.direction[1] -= move
        if key.key == pygame.K_d:
            self.direction[1] += move

    def getRect(self) -> pygame.Rect:
        return self.rect

    def animationStates(self):
        # sets animation speed and if it = one index; make it equal other index, so it animates 
        self.playerIndex += 0.1
        if self.playerIndex >= len(self.playerWalk): self.playerIndex = 0
        self.image = self.playerWalk[int(self.playerIndex)]

    def update(self):
        self.move()
        self.animationStates()

class Animator:
    # copied this and I think it works basically same as my other animator
    animation_index: int
    player_rect: pygame.Rect
    index: int = 1
    time: int = 1

    def __init__(self, rect: pygame.Rect):
        # initializing 
        self.player_rect = rect

    def cycleGifs(self, screen):
        # create own timer and increase timer and if even/odd switch images 
        self.time += 1
        if(self.time % 60 == 0):
            self.index += 1
            self.index = self.index % 2
        image = pygame.image.load("final/media/amoeba_" + str(self.index) + ".png")
        image = pygame.transform.scale(image, (70, 70)) # scales image size 
        screen.blit(image, self.player_rect) # draw on screen

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # initializes images and animates the food 
        food1 = pygame.image.load('final/media/food_0.png').convert_alpha()
        food1 = pygame.transform.rotozoom(food1, 0, .5)
        food2 = pygame.image.load('final/media/food_1.png').convert_alpha()
        food2 = pygame.transform.rotozoom(food2, 0, .5)
        self.frames = [food1, food2]
        self.animationIndex = 0
        self.image = self.frames[self.animationIndex]
        self.rect = self.image.get_rect(midbottom = (randint(0,600), randint(0,600)))

    def animationState(self):
        # actually animates it using indexes 
        self.animationIndex += 0.1
        if self.animationIndex >= len(self.frames): self.animationIndex = 0
        self.image = self.frames[int(self.animationIndex)]

    def update(self):
        self.animationState()

class Enemy(pygame.sprite.Sprite):
    global direct
    def __init__(self, type) -> None:
        super().__init__()
        # initializes a left and a right fish
        # I was trying to create fish come from both sides, but i couldn't get it to work
        # so I've just left it here as remnants of the attempt 
        if type == 'rfish':
            fish1 = pygame.image.load('final/media/fish_0.png').convert_alpha()
            fish1 = pygame.transform.rotozoom(fish1, 0, 1)
            fish2 = pygame.image.load('final/media/fish_1.png').convert_alpha()
            fish2 = pygame.transform.rotozoom(fish2, 0, 1)
            self.frames = [fish1, fish2]
            x_pos = 700
        if type == 'lfish':
            fish3 = pygame.image.load('final/media/fish_2.png').convert_alpha()
            fish3 = pygame.transform.rotozoom(fish3, 0, 1)
            fish4 = pygame.image.load('final/media/fish_3.png').convert_alpha()
            fish4 = pygame.transform.rotozoom(fish4, 0, 1)
            self.frames = [fish3, fish4]
            x_pos = -100
        # create frames and indexes in order to animate fish
        self.animationIndex = 0
        self.image = self.frames[self.animationIndex]
        self.rect = self.image.get_rect(midbottom = (x_pos, randint(0,600)))

    def animationState(self):
        # animates fish using its own timer system 
        self.animationIndex += 0.1
        if self.animationIndex >= len(self.frames): self.animationIndex = 0
        self.image = self.frames[int(self.animationIndex)]

    def update(self):
        global direct
        self.animationState()
        self.rect.x -= 3
        self.destroy()

    def destroy(self):
        # if fish goes too far left; destroy it 
        if self.rect.x <= -100:
            self.kill()

def display_score():
    # displays the score on the top of the screen 
    global score
    foodCollision()
    scoreSurf = font.render(f'Score:{score}', False, (0, 0, 0)) # parameters: string, bool, color
    scoreRect = scoreSurf.get_rect(center = (300, 40))
    screen.blit(scoreSurf,scoreRect)
    return score

def foodCollision():
    # if player collides with food; delete the food and inc score by 1 
    global score
    if pygame.sprite.spritecollide(player, foodGroup, True):
        score += 1
    return score

def enemyCollision():
    # if player collides with enemy: empty the group and return false to stop the game 
    if pygame.sprite.spritecollide(player, enemyGroup, False): # parameter: sprite, group, bool - if sprite collide w/ group check if destroyed (T - delete)
        enemyGroup.empty()
        return False
    else: return True

# creating background, window, clock, music, font, game active, start time, and score 
pygame.init() # initializing pygame
screen = pygame.display.set_mode((600, 600)) # setting up the window
pygame.display.set_caption('OmNomeba')
clock = pygame.time.Clock()
background = pygame.image.load('final/media/background.png').convert() # creating background
pygame.mixer.music.load("final/media/scizzie_aquatic_ambience.mp3")
pygame.mixer.music.play(-1)
font = pygame.font.Font('final/media/Pixeltype.ttf', 50)
gameActive = False
startTime = 0
score = 0

# creating and animating player 
player = Player() 
playerAnimator = Animator(player.getRect())

# creating sprite groups and sprites and adding them to their groups
foodGroup = pygame.sprite.Group()
foodRectList = []
enemyGroup = pygame.sprite.Group()
enemyRectList = []

# Images for the beginning screen 
introImage = pygame.image.load('final/media/amoeba_0.png')
introImage = pygame.transform.rotozoom(introImage, 0, 3)
introImageRect = introImage.get_rect(center = (300, 325))
gameName = font.render('OmNomeba', False, (0, 128, 128))
gameNameRect = gameName.get_rect(center = (300, 50))
gameMsg = font.render('Press space to play!', False, (0, 128, 128))
gameMsgRect = gameMsg.get_rect(center = (300,500))
gameRules = font.render('Use W, A, S, D to move', False, (0, 128, 128))
gameRuleRect = gameName.get_rect(center = (230, 100))
gameRules2 = font.render('Eat the food and avoid enemies!', False, (0, 128, 128))
gameRuleRect2 = gameName.get_rect(center = (150, 150))

# timers
foodTimer = pygame.USEREVENT + 1
pygame.time.set_timer(foodTimer, 1500)

enemyTimer = pygame.USEREVENT + 2
pygame.time.set_timer(enemyTimer, 2000)

def main():
    """Main function"""
    global gameActive, score
    while True:
        # establishing events for pygame 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if gameActive: # if game is active then register key presses
                if event.type == pygame.KEYDOWN:
                    player.getKey(event, True)
                if event.type == pygame.KEYUP:
                    player.getKey(event, False)
            else: # when they press space; game begins 
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    gameActive = True
                    startTime = int(pygame.time.get_ticks() / 1000)
                    Player()
                    score = 0
        if gameActive: # once game is active 
            if event.type == foodTimer: # spawn food when it hits the food timer 
                foodGroup.add(Food())
            if event.type == enemyTimer: # spawn enemies when it hits the enemy timer
                enemyGroup.add(Enemy(choice(['lfish','rfish'])))
            screen.blit(background, (0, 0)) # creating background
            score = display_score() # creating score 
            # draw and update player, food, and enemy
            player.update()
            playerAnimator.cycleGifs(screen)
            foodGroup.draw(screen)
            foodGroup.update()
            enemyGroup.draw(screen)
            enemyGroup.update()
            pygame.display.flip()
            gameActive = enemyCollision() # establish when enemies collide into player; end game 

        else: # intro/ending screen 
            screen.fill((137, 213, 210)) # fill screen w/ color
            screen.blit(introImage, introImageRect) # put amoeba on screen
            foodRectList.clear() # remove sprites in food and enemy rect list
            enemyRectList.clear() # doesn't work though
            # for the ending screen: give player their score
            scoreMsg = font.render(f'Your score: {score}', False, (0, 128, 128))
            scoreMsgRect = scoreMsg.get_rect(center = (300, 500))
            screen.blit(gameName, gameNameRect)
            if score == 0: # for intro screen
                screen.blit(gameRules, gameRuleRect) # 1st line of game rules
                screen.blit(gameRules2, gameRuleRect2) # 2nd line of game rules
                screen.blit(gameMsg, gameMsgRect) # instructions: press space to start 
            else: screen.blit(scoreMsg, scoreMsgRect)

        pygame.display.update() # update game display
        clock.tick(60)  # Sets frame rate

# call main function when you press play 
if __name__ == "__main__":
    main() 