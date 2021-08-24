#Snek
import pygame
import sys
import random
import time

pygame.init()
pygame.display.set_caption('Snek')

#Define all variables here

snekIcon = pygame.image.load('C:\\Users\\Youss\\Desktop\\Random\\Programming\\Python\\Games\\Images\\snekIcon.png')
pygame.display.set_icon(snekIcon)

gameClose = False

Game_over = False

Direction = "Still"

timeSinceLastAction = time.time()

#Of canvas/ display
Width = 680
Height = 600

Green = (255,0,0)
Red = (255,0,0)
BodyColor = (255,255,255)
Background_colour = (88,209,61)

Head_pos = [160, 320]
Head_size = 40

Food_size = 20

Bodysize = 40
BodyLength = [[120,320], [80,320]]

score = 0

foodexists = "no"

myFont = pygame.font.SysFont("monospace", 35)

Clock = pygame.time.Clock()

Display = pygame.display.set_mode((Width, Height))

#Function for generating a random co-ord everytime food is consumed
def placeFood(Food_size):
    global randx
    randx = random.randint(0, Width - Food_size)
    global randy
    randy = random.randint(0, Height - Food_size)
    pygame.draw.rect(Display, Red, (randx, randy, Food_size, Food_size))

def drawBody():
    for body in BodyLength:
        pygame.draw.rect(Display, BodyColor, (body[0], body[1], Bodysize, Bodysize))

#For making a new body piece everytime
def addBody(Head_pos, Bodysize, BodyLength, Direction):
    global Bodyx
    global Bodyy
    if Direction == "Left":
        Bodyx = Head_pos[0] + 40 + (len(BodyLength) * 30)
        Bodyy = Head_pos[1] + 5
        BodyLength.append([Bodyx, Bodyy])
    elif Direction == "Right":
        Bodyx = Head_pos[0] - 30 - (len(BodyLength) * 30)
        Bodyy = Head_pos[1] + 5
        BodyLength.append([Bodyx, Bodyy])
    elif Direction == "Up":
        Bodyy = Head_pos[1] + 40 + (len(BodyLength) * 30)
        Bodyx = Head_pos[0] + 5
        BodyLength.append([Bodyx, Bodyy])
    elif Direction == "Down":
        Bodyy = Head_pos[1] - 30 - (len(BodyLength) * 30)
        Bodyx = Head_pos[0] + 5
        BodyLength.append([Bodyx, Bodyy])

def Collision_food_detect():
    p_x = Head_pos[0]
    p_y = Head_pos[1]

    f_x = current_x
    f_y = current_y

    if (f_x >= p_x and f_x < (p_x + Head_size)) or (p_x >= f_x and p_x < (f_x + Food_size)):
        if (f_y >= p_y and f_y < (p_y + Head_size)) or (p_y >= f_y and p_y < (f_y + Food_size)):
            return True
    return False

def Border_collision():
    h_x = Head_pos[0]
    h_y = Head_pos[1]

    if h_x > (Width - Head_size + 1) or h_x < 0:
        return True
    elif h_y > (Height - Head_size + 1) or h_y < 0:
        return True
    else:
        return False

#Check if head collides with body
def Head_collision():
    h_x = Head_pos[0]
    h_y = Head_pos[1]

    for body in BodyLength:
        b_x = body[0]
        b_y = body[1]
        if h_y == b_y and h_x == b_x:
            return True

def Text(W, H):
    Display.blit(Label, (Width - W, Height - H))

#Everything in this while loop is the game actually running
while not gameClose:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        #This is prevents moving opposite direction
        if event.type == pygame.KEYDOWN:
            x = Head_pos[0]
            y = Head_pos [1]
            #Checks if its been 0.2 seconds between last move, this is a very bad way of doing this but i cant think of another way
            #Actually i can but this works so i cant be bothered
            if timeSinceLastAction > 0.2:
                timeSinceLastAction = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if Direction =="Right" or Direction == "Still":
                        break
                    else:
                        Direction = "Left"
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if  Direction == "Left":
                        break
                    else:
                        Direction = "Right"
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if  Direction == "Down":
                        break
                    else:
                        Direction = "Up"
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if  Direction == "Up":
                        break
                    else:
                        Direction = "Down"

    #Drawing the canvas black
    Display.fill(Background_colour)

    #Moving the head in different directions
    x = Head_pos[0]
    y = Head_pos [1]
    prevHead_pos = [x,y]
    if Direction == "Left":
        x -= 40
        Head_pos = [x,y]
    elif Direction == "Right":
        x += 40
        Head_pos = [x,y]
    elif Direction == "Up":
        y -= 40
        Head_pos = [x,y]
    elif Direction == "Down":
        y += 40
        Head_pos = [x,y]

    #Creation of food
    if foodexists == "no":
        placeFood(Food_size)
        current_x = randx
        current_y = randy
        foodexists = "yes"

    #Drawing the food
    pygame.draw.rect(Display,Red, (current_x, current_y, Food_size, Food_size))
    #Drawing the head
    pygame.draw.rect(Display, Green, (Head_pos[0],Head_pos[1], Head_size, Head_size))

    #Detection if food is in contact with snake
    if Collision_food_detect():
        placeFood(Food_size)
        current_x = randx
        current_y = randy
        addBody(Head_pos, Bodysize, BodyLength, Direction)
        score += 1

    #Ends game if head collides with body
    if Head_collision():
        Game_over = True

    #This removes a body from the back, and adds it to where the head used to be
    #Then it changes the Body array to match the snakes body order
    if len(BodyLength) > 0:
        if Direction != "Still":
            BodyLength[-1] = prevHead_pos
            BodyLength.insert(0,BodyLength[-1])
            BodyLength.pop(-1)
    drawBody()

    #Ends game if collided with border
    if Border_collision():
        Game_over = True

    #Score
    if not Game_over:
        text = "Score: " + str(score)
        Label = myFont.render(text, 1, (Green))
        Text(255, 40)

    if Game_over:
        Direction = "Still"
        BodyLength = [[120,320], [80,320]]
        Head_pos = [160,320]
        #Only works with some keys like a and arrow keys, not space, works on my other laptop thought so i dont know what the problem is
        Restart = myFont.render("Hold a to restart", 1, (Green))
        Display.blit(Restart, (Width - 575, Height - 400))
        Text(450, 475)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                score = 0
                Game_over = False

    Clock.tick(5)

    #Start timer again
    timeSinceLastAction = time.time()

    pygame.display.update()
