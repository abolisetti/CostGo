# FP: COSTGO- An interactive Costco game
#By Arvind Bolisetti and Shahed El Baba
# 6/16/2016

"""This game is basically a game version of what it'd be like to shop at the
the real costco. The main goal of this game is to collect 10 items from your
randomized shopping list before time runs out, which is 5 minutes. The game has
many different feautures. There are insturctions, load game, new game, highscores,
pause and music."""

##-----IMPORTS-----##
from pygame import *
from random import *
import glob
import datetime
from time import time as timer
from time import localtime
from pprint import *



##-----FONTS-----##
font.init()
bodyFont = font.SysFont("Comic Sans MS", 15)
titleFont = font.SysFont("Comic Sans MS", 20)
titleFont.set_bold(True)



##-----MUSIC-----##
mixer.init()#starts mixer for bgm
mixer.music.load("music/BGmusic.mp3")



##-----IMAGES-----##
storeMap = image.load("masks/testmap.png")#The map of costco
pausePic = image.load("PauseButtons/pause.png")#pause menu images
playPic = image.load("PauseButtons/play.png")
backImg=image.load("menu/Back.png")
nextImg = image.load("menu/Next.png")


##-----CONSTANTS-----##
username = "" #username for save profile
userNum = 0 #which data file

storeMapW, storeMapH = storeMap.get_width(), storeMap.get_height()#w and h for map

width, height = 1024, 768 #screen
screen = display.set_mode((width, height))

width, height = 1024 - (128+64) -10, 768 #then size of the screen ur playing exlcuding shopping list

shopRect = [Rect(625, 417, 3264, 5216)]#the rect inside the walls of cosctco

start = True


##-----DATA FILES-----##
"""These data files contain
    -Shelf Rect Data
    -Items Rect Data
    -List of items """

shelfRects = open("Rect Data/shelf-locations-only-rects.txt").readlines()
shelfRects = [i.split(",") for i in shelfRects]
shelfRects = [Rect(int(i[0]), int(i[1]), int(i[2]), int(i[3])) for i in shelfRects]

shelfItems=open("Rect Data/Item List.txt")
shelfItems = [str(i.strip('\n')) for i in shelfItems]

shelfItemRects=open("Rect Data/Item Rects.txt").readlines()
shelfItemRects = [i.split(",") for i in shelfItemRects]
shelfItemRects=[Rect(int(i[0]), int(i[1]), int(i[2]), int(i[3])) for i in shelfItemRects]



##--------------------FUNCTIONS------------------------##

##-----MOVING-----##

def sprites(CHRName):
    """Organizes the sprties by direction for move function"""
    
    directions = "Right Down Up Left".split()
    string = "sprites/%s/%s/"
    someStrings = [((string %(CHRName, directions[i])+"*.png")) for i in range(4)]
    return [glob.glob(someStrings[i]) for i in range(4)]#Gets pictures for each direction folder
  
def moveX(mapX, mapY, badGuys, badGuyRects, shelfRects, objRects, charRect, shelfItemRects):
    """Moves the map, as well as updates the position of the shelves. Does not
    move the character( the character's position is static to center of screen )"""
    
    #FUNCTION TAKEN FROM MR.MCKENZIE'S CLASS FOLDER
    keys = key.get_pressed()#Movements for main character

    X=0
    Y=1

    global move, frame, start

    totalX = 0#keeps track of toal change in x and y
    totalY = 0

    RIGHT = 0 
    DOWN = 1  
    UP = 2
    LEFT = 3

    newMove=-1
    dist = 6*2
    if keys[K_RIGHT] or keys[K_d]:
        newMove = RIGHT
        if moveCheck(12, 0, objRects, charRect):#a checking function to see if there are objects infront of user
            mapX -= dist
            totalX -= dist
        
    elif keys[K_LEFT] or keys[K_a]:
        
        newMove = LEFT
        if moveCheck(-12, 0, objRects, charRect):
            mapX += dist
            totalX += dist

    elif keys[K_UP] or keys[K_w]:
        newMove = UP
        if moveCheck(0, -12, objRects, charRect):
            mapY += dist
            
            totalY += dist

    elif keys[K_DOWN] or keys[K_s]:
        newMove = DOWN
        if moveCheck(0, +12, objRects, charRect):
            mapY -= dist
            totalY -= dist

    else:
        frame = 0

    

    if move == newMove:     # 0 is a standing pose, so we want to skip over it when we are moving
        frame = frame + 0.5 # adding 0.2 allows us to slow down the animation
        if frame >= len(pics[0][move]):
            frame = 1
    elif newMove != -1:     # a move was selected
        move = newMove      # make that our current move
        frame = 1

    objRects = [charRect] + badGuyRects + shelfRects
    return mapX, mapY, totalX, totalY, badGuys, badGuyRects, shelfRects, objRects, charRect, shelfItemRects




def makeMove(character, direction):#makes the moves
    #TAKEN FROM MR.MCKENZIE
    ''' This returns a list of pictures. They must be in the folder "name"
        and start with the name "name".
        start, end - The range of picture numbers 
    '''
    character = character[direction]
    move = [transform.scale(image.load(character[i]),(18,24)) for i in range(len(character))]
            
    return move




def moveCheck(x, y, objRects, charRect):
    """Checks to see if player has collided with an item"""
    #creates a new rect, runs it through all objRects, and if there are collisions
    
    newMove = Rect(charRect[0]+x, charRect[1]+y, charRect[2], charRect[3])
    for i in objRects:
        if newMove.colliderect(i) and i!=charRect:
            return False
    return True



    
def moveY(guy, guyRect, objRects):
    #taken from mr mckenzies class folder
    X=0
    Y=1
    DIR = 2
    
    
    RIGHT = 0 
    DOWN = 1  
    UP = 2
    LEFT = 3

    checkDist = 50
    if randint(1,100)==1:#So they turn less often
        guy[DIR]=randint(0,3)
    if guy[DIR] == RIGHT:
        if badGuyCollide(guyRect, checkDist, 0, objRects):
            guy[DIR] = randint(0,3)#if they are gonna going to collide then they will turn away
        else:
            guy[X]+=5
            
    if guy[DIR] == LEFT:
        if badGuyCollide(guyRect, -checkDist, 0, objRects):
            guy[DIR] = randint(0,3)
        else:
            guy[X]-=5
            
    if guy[DIR] == UP:
        if badGuyCollide(guyRect, 0, -checkDist, objRects):
            guy[DIR] = randint(0,3)
        else:
            guy[Y]-=5
            
    if guy[DIR] == DOWN:
        if badGuyCollide(guyRect, 0, checkDist, objRects):
            guy[DIR] = randint(0,3)
        else:
            guy[Y]+=5





##-----Checking Functions-----##
def rectCheck(rectA, rectB, rectC):
    for i, j in zip(rectA, rectB):
        collide = False
        
        for k in rectC:
            if j.colliderect(k):
                collide = True
        if collide:
            rectA.remove(i)
            rectB.remove(j)
               
def rectDraw(lst, color = 0):
    for i in lst:
        draw.rect(screen, color, i, 1)



def picsCreate(char):
    """Gets pic based off of character's movement"""
    return [makeMove(char, i) for i in range(4)]

##-----ENEMIES-----##

def guyCollideCheck(rect1, rectList):#keeps track of scores
    return (len([i for i in rectList if rect1.colliderect(i)]))


def badGuyCreate(num, objRects, pics):
    """Creates a random enemy, and makes sure they don't collide with a shelf/the player or another enemy"""
    
    badGuys = []
    badGuyRects = []

    for i in range(num):
        guy = [randint(625+mapX,3264+mapX),randint(417+mapY, 5216+mapY),randint(0,3),randint(0,len(pics)-1)]
        
        guyRect = Rect(guy[0], guy[1], pics[guy[-1]][0][0].get_width(), pics[guy[-1]][0][0].get_height())

        collide = False
        for i in objRects:
            if guyRect.colliderect(i): #if the chaacter comes into contact with the guyrect
                collide = True #they have collided with a shelf

                
        if collide == False:
            badGuys.append(guy)
            badGuyRects.append(guyRect)
            objRects.append(guyRect)

    return badGuys, badGuyRects, objRects





def moveBadGuys(badGuys, badGuyRects, objRects):
    """Goes through every bad guy and moves them around map"""
        
    for i in range(len(badGuys)):
        moveY(badGuys[i], badGuyRects[i], objRects)#using the move y function on each badguy
        


def badGuyCollide(guy, x, y, objRects):
    """Checks to see if enemy has collided with an object/an enemy/ the player"""

    guyMove = Rect(guy[0]+x, guy[1]+y, guy[2], guy[3])
    guyOriginal = Rect(guy[0], guy[1], guy[2], guy[3])

    #same logic as moveCheck, but for badguys
  
    for i in objRects:
        if guyMove.colliderect(i) and i!=guyOriginal:
            if i == guy:
                print(True)
            return True
            
    return False




def rectUpdate(rectList, x, y):
    """Updates enemy and shelves positions based off of offset"""
    return [Rect(rect[0]+x, rect[1]+y, rect[2], rect[3]) for rect in rectList]




##-----SHOPPING FUNCTIONS-------##

def pickItemUp(shelfRects,shelfItems,shelfItemRects,shoppingList,click):
    """Main Game function
    Checks for if an item has picked up an item, and if it was in the shoppingList
    """
    
    

    mx,my=mouse.get_pos()
    global charRect
    
    for shelfRect in shelfRects:
        for shelfItemRect in shelfItemRects: #goes through every item/shelf rect
            if shelfItemRect.collidepoint(mx,my) and shelfRect.collidepoint(mx,my) and charRect[1]> shelfRect[1]:
                
                #if they're in front of the shelf/they've clicked on the shelf
                if charRect[1] - (shelfRect[1] + shelfRect[3]) <= 30 and 100 > abs(charRect[0] - mx) > 0:
                    if click:#distance between character and shelf less than 30px
                        
                        itemPos = shelfItemRects.index(shelfItemRect) #finds position of item in file,
                                                                       #uses that index to find which item it is
                        item = shelfItems[itemPos]
                        if item in shoppingList:
                            return item
                        

                            
def generateShoppingList(shelfItems): #this creates the first instance of the shopping list and only runs once
    """Creates a random shopping list based off of items"""
    indices=sample(range(0,150),15) #Creates a list of 10 indices, then 10 items
    shoppingList=[shelfItems[i] for i in indices]
    return shoppingList


def updateShoppingList(shoppingList, itemBought):
    """Updates the shopping list whenever something is bought"""

    shoppingList.remove(itemBought) #removes the item

    return  shoppingList


##-----PAGES-------##

    


def runMainMenu():
    running=True
    
    menuBack=image.load("menu/menuPicBack.png")
    screen.blit(menuBack,(0,0))

    if username!="":
        draw.rect(screen,(255,255,255),(0,0,1024,20))
        text= "User currently playing: %s " %(username)
        text= bodyFont.render(text,True,(0,0,0))
        screen.blit(text,(1024//2-text.get_width()//2,1))

    # the images of the buttons
    newGameImg=image.load("menu/New Game.png")
    loadGameImg=image.load("menu/Load Game.png")
    highScoresImg=image.load("menu/High Scores.png")
    
    
    newGameButton=screen.blit(newGameImg,(115,650))
    loadGameButton=screen.blit(loadGameImg,(415,620))
    highScoresButton=screen.blit(highScoresImg,(715,590))

    title=screen.blit(image.load("menu/title.png"),(425,50))



    buttons=[newGameButton,loadGameButton,highScoresButton] #this is a list of the images
    vals=["Make Profile","Load Game","Highscores"]

   
        
    display.flip()
    
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "exit"

        mx, my=mouse.get_pos()
        mb=mouse.get_pressed()

        for r, v in zip(buttons,vals):
            if r.collidepoint(mx,my):
                #make clicked vers. of text red!
                if mb[0]==1:
                    return v

                

    quit()
    return "exit"




def runNewGame():
    global username
    global userNum
    
    instructions=["It is required that you create a user in order to proceed",
                    "Creating a new user gives you the ability to create",
                   "and access highscores you have acquired in your playthroughs",
                   "",
                   "Enter a name below:",
                   ]

    
    screen.fill((220,220,220))
    
    
    
    newgameImg=image.load("menu/New Game title.png")
    screen.blit(newgameImg,(512-(newgameImg.get_width()//2),20))

    backImg=image.load("menu/Back.png")
    nextImg = image.load("menu/Next.png")
    
    backButton=screen.blit(backImg,(100,568))
    nextButton=screen.blit(nextImg,(((824-nextImg.get_width()//2),568)))    
    
    texty=100
    for line in instructions:
        text=titleFont.render(line,True,(255,0,0))
        texty+=(text.get_height()+20)
        screen.blit(text,(((1024//2)-(text.get_width()//2)),texty))

    textRect=Rect(100,345+100,(1024-200),50)

    
    username=getName((255,255,255),textRect)


    display.flip()

    """since this is where you make a user, you need to create a data file
of exisiting users"""

    
    usernamesFile = open("User Data/%d.txt" %(userNum),"w")
    usernamesFile.write("%s,%d,%d" %(username, 0, 0))
    usernamesFile.close()

    running=True

    while running:
        for e in event.get():
            if e.type == QUIT:        
                running = False



        mx, my=mouse.get_pos()
        mb= mouse.get_pressed()
        if backButton.collidepoint(mx,my) and mb[0] == 1 :
            return "Main Menu"

        if nextButton.collidepoint(mx,my) and mb[0] ==1:
            return "Load Game" #techinically this should be load game but i havent made that so...
        
    return "exit"
    quit()


def makeProfile():
    global userNum
    global userName
    
    screen.fill((220,220,220))  
    loadgameTitleImg = image.load("menu/New Game title.png")
    screen.blit(loadgameTitleImg,(512-loadgameTitleImg.get_width()//2,20))
    

    size = 100

    profileRects= [Rect(100,258,1024-200,80),Rect(100,358,1024-200,80),Rect(100,458,1024-200,80)]
    


    texty= 100
    for i in profileRects:
        draw.rect(screen,(255,255,255),i)
    instructions=["Here, you can create or overwrite save files.",
                    "Just chose one of the following, then enter a username!"]
    for i in instructions:
        subtitleText= titleFont.render(i,True,(255,0,0))
        texty+=50
        screen.blit(subtitleText,(512-subtitleText.get_width()//2,texty))
            
    playerNames = []
    allFiles = glob.glob("User Data/*txt")
    files = [open(i, "r").read().strip().split(",") for i in allFiles]
    
    for i in files:
        if i[0]!=None:
            playerNames.append(i[0])
        else:
            playerNames.append("Empty: no player")
    texty=200
    
    for player in playerNames:
        playerPos=playerNames.index(player)
        text= titleFont.render(player,True,(0,0,0))
        texty+=100
        screen.blit(text,((110),texty))

    running = True
    
    while running:
        clk = False
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
        for e in event.get():
            if e.type == QUIT:
                running = False
            if e.type == MOUSEBUTTONDOWN:
                clk = True

        backButton=screen.blit(backImg,(100,568))
        #nextButton=screen.blit(nextImg,(((824-nextImg.get_width()//2),568)))
      
        for i in profileRects:
            draw.rect(screen,(255,255,255),i,2)
        
        for i in profileRects:
            if i.collidepoint(mx,my):
                rectDraw([i])
                if clk:#will see if u get ckick on a certain profile
                    userNum = profileRects.index(i)+1
                    
                    
                    usernamesFile = open("User Data/%d.txt" %(userNum),"r").read().strip().split(",")
                    choose = True#true until overwrutewindow says otherwise
                    if len(usernamesFile)>1:
                        choose = overwriteFileWindow()
                    
                    
                    if choose:   
                        screen.fill((220,220,220))
                        
                        userNum = profileRects.index(i)+1
                        return "New Game"#if they wanna overwrite they make profile
                    if not choose:
                        return "Make Profile"#If they dont wanna overwrite they leave this page
        
        mx, my=mouse.get_pos()
        mb= mouse.get_pressed()
        if backButton.collidepoint(mx,my) and mb[0] == 1 :
            screen.fill((220,220,220))  

            return "Main Menu"

        if running == False:
            screen.fill((220,220,220))  

        display.flip()

    return "exit"
    quit()





def overwriteFileWindow():
    screen.fill((220,220,220))
    messageTitle=image.load("menu/overwrite message.png")
    screen.blit(messageTitle,(512-messageTitle.get_width()//2,384-messageTitle.get_height()))

    yesImg= image.load("menu/Yes.png")
    noImg=image.load("menu/No.png")

    yesButton=screen.blit(yesImg,(512-yesImg.get_width()-100,384+messageTitle.get_height()//2))
    noButton=screen.blit(noImg,(512+noImg.get_width(),384+messageTitle.get_height()//2))

    areUSureRect = [yesButton, noButton]
    running = True
    while running:
        clk = False
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
        for e in event.get():
            if e.type == QUIT:
                running = False
            if e.type == MOUSEBUTTONDOWN:
                clk = True

        for i in areUSureRect:#checks if clicking on yes or no
            if clk and areUSureRect.index(i) == 0 and i.collidepoint(mx,my):
                screen.fill((220,220,220))
                return True
            elif clk and areUSureRect.index(i) == 1 and i.collidepoint(mx,my):
                screen.fill((220,220,220))
                return False
        

    


        
        if running == False:
            screen.fill((220,220,220))
        display.flip()
        
def runHighscores():
    
    screen.fill((220,220,220))
    highscoreImg= image.load("menu/highscoresTitle.png")
    screen.blit(highscoreImg,(512-highscoreImg.get_width()//2,20))

    instructions="These are the top highscores of all players existing with save files"
    subtitleText= titleFont.render(instructions,True,(255,0,0))
    screen.blit(subtitleText,(512-subtitleText.get_width()//2,200))

    draw.rect(screen,(255,255,255),(100,309,1024-200,200))
    draw.rect(screen,(0,0,0),(100,309,1024-200,200),4)
    
    for y in range(309,309+200,200//4):
        draw.line(screen,(0,0,0),(100,y),(924,y),2)

    
    texty=275+50

    screen.blit(titleFont.render("Rank",True,(0,0,0)),(140,texty))
    screen.blit(titleFont.render("Name",True,(0,0,0)),(250,texty))
    screen.blit(titleFont.render("Score",True,(0,0,0)),(550,texty))
    screen.blit(titleFont.render("Time Left",True,(0,0,0)),(800,texty))




    files= getHighScores(getOldScores())
    
    for i in files:
        texty+=50
        screen.blit(titleFont.render(str(files.index(i)+1),True,(0,0,0)),(140,texty))

        screen.blit(titleFont.render(str(i[0]),True,(0,0,0)),(250,texty))
        
        screen.blit(titleFont.render(str(i[1]),True,(0,0,0)),(550,texty))

        screen.blit(titleFont.render(str(i[2]),True,(0,0,0)),(800,texty))



        #screen.blit(()


    backButton=screen.blit(backImg,(512-backImg.get_width()//2,620))
    

    running = True
    while running:
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
        for e in event.get():
            if e.type == QUIT:
                running = False

        if backButton.collidepoint(mx,my) and mb[0] == 1 :
            screen.fill((220,220,220))
            time.wait(10)

            return ("Main Menu")
        
        
        display.flip()
    return "exit"
    quit()
    




def load():
    global username
    global userNum
    screen.fill((220,220,220))
    #same thing as make new profile but no overwhite window
    profileRects= [Rect(100,258,1024-200,80),Rect(100,358,1024-200,80),Rect(100,458,1024-200,80)]

    rectDraw(profileRects, (255,255,255))
    loadgameTitleImg = image.load("menu/Load Game title.png")
    screen.blit(loadgameTitleImg,(512-loadgameTitleImg.get_width()//2,20))
    

    profileRects= [Rect(100,258,1024-200,80),Rect(100,358,1024-200,80),Rect(100,458,1024-200,80)]
    

    texty= 100
    for i in profileRects:
        draw.rect(screen,(255,255,255),i)
    instructions=["Here, you can load old save files.",
                    "The currently loaded player will be displayed on the top of the menu screen"]
    for i in instructions:
        subtitleText= titleFont.render(i,True,(255,0,0))
        texty+=50
        screen.blit(subtitleText,(512-subtitleText.get_width()//2,texty))
            
    playerNames = []
    allFiles = glob.glob("User Data/*txt")
    files = [open(i, "r").read().strip().split(",") for i in allFiles]
    
    for i in files:
        if i[0]!=None:
            playerNames.append(i[0])
        else:
            playerNames.append("Empty: no player")
    texty=200
    for player in playerNames:
        playerPos=playerNames.index(player)
        text= titleFont.render(player,True,(0,0,0))
        texty+=100
        screen.blit(text,((110),texty))

    

    running = True
    while running:
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
        for e in event.get():
            if e.type == QUIT:
                running = False
                return "exit"

        
      
        for i in profileRects:
            draw.rect(screen,(255,255,255),i,2)
            
        for i in profileRects:
            if i.collidepoint(mx,my):
                rectDraw([i])
                if mb[0] == 1:
                    screen.fill((220,220,220))
                    userNum = profileRects.index(i)+1
                    print('true')
                    
                    usernamesFile = open("User Data/%d.txt" %(userNum),"r")
                    username = usernamesFile.read().split(",")[0]
                    
                    userNum = profileRects.index(i)+1
                    return "Instructions"


        if running == False:
            screen.fill((220,220,220))
        display.flip()

def getName(colour,textArea):
    #TAKEN FROM MCKENZIES CLASSS FOLDER
    
    ans = ""
    # final answer will be built one letter at a time.
    back = screen.subsurface(textArea).copy()        # copy screen so we can replace it when done
    
    typing = True
    while typing:
        for e in event.get():
            if e.type == QUIT:
                event.post(e)   # puts QUIT back in event list so main quits
                return ""
        
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    typing = False
                    ans = None
                elif e.key == K_BACKSPACE:    # remove last letter
                    if len(ans)>0:
                        ans = ans[:-1]
                elif e.key == K_KP_ENTER or e.key == K_RETURN : 
                    typing = False
                    return ans
                elif e.key < 256:
                    ans += e.unicode       # add character to ans


        
        txtPic = titleFont.render(ans, True, (0,0,0))   #
        draw.rect(screen,colour,textArea)        # draw the text window and the text.
        draw.rect(screen,(0,0,0),textArea,2)            #
        screen.blit(txtPic,(textArea.x+3,textArea.y+2))

        display.flip()
        
        
    screen.blit(back,(0,0))



            

def runGameOver():
    running=True

    global pics,move,frame
    
    blackFade=screen.copy()  #screenshot of where character lost. 
    blackFade=blackFade.convert()  #this part mkakes a fade to black effect which then displays game over. kind of like kh death scenes lol
 
    
    alpha=255 #transparency of image
    displayText=False
    canClick= False #this is so they dont click until everything has daded in succesfully
    
    while running:
        for e in event.get():
            if e.type==QUIT:
                running==False
                return "exit"
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
                
        screen.fill((0,0,0))
        blackFade.set_alpha(alpha)
        screen.blit(blackFade,(0,0))

        
        if alpha<=255 and alpha>=1:
            alpha-=1
            time.delay(10)
            displayText=False
        else:
            displayText= True
            

        pic = pics[0][move][int(frame)]
        screen.blit(pic,(width//2-((pic.get_width())//2), height//2-((pic.get_height())//2)))

        if displayText:

            gameOverImg= image.load("menu/GameOver.png")
            screen.blit(gameOverImg,(512-gameOverImg.get_width()//2,20))

            playAgainImg= image.load("menu/playAgain.png")
            playAgainButton = screen.blit(playAgainImg,(574,height//2-playAgainImg.get_height()//2-50))

            mainMenuImg = image.load("menu/mainMenu.png")
            mainMenuButton = screen.blit(mainMenuImg,(574,height//2+mainMenuImg.get_height()//2+50))
            canClick==True

            if mb[0] == 1 and playAgainButton.collidepoint(mx, my):
                resetVals()
                return "Play Game"

            if mb[0] ==1 and mainMenuButton. collidepoint(mx, my):
                return "Main Menu"
            

                
            
        display.flip()
    quit()
    return "exit"

def runGameWin():
    running = True
    global pics,move,frame

    whiteFade=screen.copy()  #screenshot of where character lost. 
    whiteFade=whiteFade.convert()  #this part mkakes a fade to black effect which then displays game over. kind of like kh death scenes lol
 
    
    alpha=255 #transparency of image
    displayText=False
    canClick= False #this is so they dont click until everything has daded in succesfully

    while running:
        for e in event.get():
            if e.type==QUIT:
                running==False
                return "exit"
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
                
        screen.fill((255,255,255))
        whiteFade.set_alpha(alpha)
        screen.blit(whiteFade,(0,0))

        
        if alpha<=255 and alpha>=1:
            alpha-=1
            time.delay(10)
            displayText=False
        else:
            displayText= True
            

        pic = pics[0][move][int(frame)]
        screen.blit(pic,(width//2-((pic.get_width())//2), height//2-((pic.get_height())//2)))

        if displayText:
            gameWinImg= image.load("menu/Game Win.png")
            screen.blit(gameWinImg,(512-gameWinImg.get_width()//2,20))

            playAgainImg= image.load("menu/playAgain.png")
            playAgainButton = screen.blit(playAgainImg,(574,height//2-playAgainImg.get_height()//2-50))

            mainMenuImg = image.load("menu/mainMenu.png")
            mainMenuButton = screen.blit(mainMenuImg,(574,height//2+mainMenuImg.get_height()//2+50))

            canClick==True

            if mb[0] == 1 and playAgainButton.collidepoint(mx, my):
                resetVals()
                return "Play Game"

            if mb[0] ==1 and mainMenuButton. collidepoint(mx, my):
                return "Main Menu"
            
        display.flip()
    quit()
    return "exit"




    
def runInstructions(): # This code was taken from Grace Wang's CUBIS. THANKS!
    mouseHold = False
    running = True

    canClick = True
    tutPageImgs=[]
    for i in range(1,6):
        tutPageImgs.append(image.load ("tutpages/tutpage" + str(i) + ".png"))
    tutPage=1

    display.flip()
    while running:
        for e in event.get():
            if e.type==QUIT:
                return "exit"
            if e.type==MOUSEBUTTONUP:
                mouseHold= False
            if e.type == MOUSEBUTTONDOWN:
                mouseHold = True
    

        mb = mouse.get_pressed()
        mx ,my = mouse.get_pos()
        screen.blit(tutPageImgs[tutPage-1],(0,0))

        backImg=image.load("menu/Back.png")
        nextImg = image.load("menu/Next.png")

        arrowImg= image.load("menu/arrow.png")
        if tutPage not in [4,5]:
            backButton=screen.blit(backImg,(100,568))
            nextButton=screen.blit(nextImg,(((824-nextImg.get_width()//2),568)))
        else:
            nextButton=screen.blit(arrowImg,(1022-arrowImg.get_width(),height//2-arrowImg.get_height()//2))
            backButton=screen.blit(transform.flip(arrowImg,True,False),(2,height//2-arrowImg.get_height()//2))

            
        if mb[0]==1 and canClick:
            if tutPage==1:
                if backButton.collidepoint(mx,my):
                    return "Main Menu"
                if nextButton.collidepoint(mx,my):
                    tutPage+=1
            elif 2<= tutPage <=4:
                if backButton.collidepoint(mx,my):
                    tutPage-=1
                if nextButton.collidepoint(mx,my):
                    tutPage+=1
            elif tutPage==5:
                if backButton.collidepoint(mx,my):
                    tutPage-=1
                if nextButton.collidepoint(mx,my):
                    return "Play Game"

        if mouseHold:
            canClick = False
        else:
            canClick = True
            
        display.flip()
    quit()
    return "exit"


def resetVals():
    """puts the game back to its orginial state"""
    global shoppingList, timeLimit, timeLeft, mapX, mapY
    
    #every variables that needs to be reset will be reset
    shelfRects = []
    shelfItems = []
    shelfItemRects=[]
    badGuys = []
    badGuyRects = []
    objRects = []
    
    shelfRects = open("Rect Data/shelf-locations-only-rects.txt").readlines()
    shelfRects = [i.split(",") for i in shelfRects]
    shelfRects = [Rect(int(i[0]), int(i[1]), int(i[2]), int(i[3])) for i in shelfRects]

    shelfItems=open("Rect Data/Item List.txt")
    shelfItems = [str(i.strip('\n')) for i in shelfItems]

    shelfItemRects = open("Rect Data/Item Rects.txt").readlines()
    shelfItemRects = [i.split(",") for i in shelfItemRects]
    shelfItemRects = [Rect(int(i[0]), int(i[1]), int(i[2]), int(i[3])) for i in shelfItemRects]

    totalX, totalY = 0, 0
    
    shoppingList = generateShoppingList(shelfItems) #The list of items you need to buy
    timeLimit = 300
    timeLeft = 300
    elapsed = 0
    mapX, mapY = -3334, -5506


    shelfRects = rectUpdate(shelfRects, mapX, mapY)


    shelfItemRects = rectUpdate(shelfItemRects,mapX,mapY)
    display.flip()

    badGuys, badGuyRects, objRects = badGuyCreate(400, objRects, pics)

    #Updates position of shelves in relation with the map

##-----DRAWING FUNCTIONS-------##

def drawShoppingList(shoppingList):
    """the objective screen shows the player the items they have bought, and their shopping List"""
    #the objectives background
    draw.rect(screen,(255,255,255),((1024-(128+62)),12,(128+52),746))
    draw.rect(screen,(255,0,0),((1024-(128+62)),12,(128+52),746),2)

    

    shoppinglistTitleText = titleFont.render("Shopping List: ",True,(0,0,0))
    screen.blit(shoppinglistTitleText,((1024-(128+64)+(128+54)-shoppinglistTitleText.get_width(),20)))
    

    shoppinglistTexty=-20
    for item in shoppingList:
        shoppinglistTexty+=35
        itemText=bodyFont.render(item,True,(0,0,0))
        screen.blit(itemText,(((1024-(128+64)+5),(shoppinglistTitleText.get_height()+20)+shoppinglistTexty)))
        




def drawScene(MAP, pics, move, frame,fullshoppingList, timeLeft, mapX, mapY, totalX, totalY, DIR = 2):
    """Draws all items to map"""
    X=0
    Y=1
    
    screen.fill((255,255,255))
    #this is the space where the game actually runs (so the game minus the border)

    
    
    screen.blit(MAP, (mapX,mapY))

    global shelfRects, badGuyRects, shelfItemRects

    for guy in badGuys:
        
        guy[X] += totalX
        guy[Y] += totalY

    shelfRects = rectUpdate(shelfRects, totalX, totalY)
    badGuyRects = rectUpdate(badGuyRects, totalX, totalY)
    shelfItemRects = rectUpdate(shelfItemRects, totalX, totalY)

    
    for guy in badGuys:
        f = frame2//4 % len(pics[guy[3]][guy[DIR]])
        pic = pics[guy[3]][guy[DIR]][f]
        screen.blit(pic,guy[:2])


    pic = pics[0][move][int(frame)]
    
    screen.blit(pic,(width//2-((pic.get_width())//2), height//2-((pic.get_height())//2)))

    gameScreen=Rect(0,0,(1024),(768))
    draw.rect(screen,(255,255,255),gameScreen,20)

    drawShoppingList(fullshoppingList)

    drawTimer(timeLeft)
    


    display.flip()

def drawTimer(timeLeft):

    if len(str(timeLeft%60)) ==1 : #if the seconds is less than 10, show :01, not just :1
        timeText= str(timeLeft // 60) + " : 0" + str(timeLeft % 60)
    else:
        timeText = str(timeLeft // 60) + " : " + str(timeLeft % 60)
    text = titleFont.render(timeText,True,(255,0,0),(255,255,255))

    timerRect=  Rect(width//2-100,20,200,50)
    draw.rect(screen,(255,255,255),timerRect)
    draw.rect(screen,(255,0,0),timerRect,2)

    screen.blit(text, (width//2-text.get_width()//2,20+text.get_height()//2)) 





##-----TIME FUNCTIONS-------##

def getTime(elapsed):
    #finds time remaining since game function was called

    global timeLimit,timeLeft, timeWithoutPause
    now = datetime.datetime.now()
    now = now.minute*60 + now.second

    

    timeLeft = timeLimit-(now-timeWithoutPause)+elapsed
    



def pauseButton(keys,mx, my, mb, pic1, pic2):
    global timeLeft, elapsed
    pauseRect = Rect(25, 25, 25, 25)

    pic1 = transform.smoothscale(pic1, (pauseRect[-2], pauseRect[-1]))
    
    rectDraw([pauseRect], (0,255,255))
    screen.blit(pic1, pauseRect)
    if pauseRect.collidepoint(mx, my) and mb[0] == 1 or keys[K_p]:
        return pause(pic2)


        
        
def pause(pic2):
    global timeLeft, wasPaused, elapsed
    playRect=  Rect(width//2-50,height//2-50,100,100)
    pic2 = transform.smoothscale(pic2, (playRect[-2], playRect[-1]))

    screen.blit(pic2, playRect)
    
      
    mainMenuImg= image.load("pauseButtons/mainMenu.png")
    muteImg = image.load("pauseButtons/mute.png")
    resetImg = image.load("pauseButtons/reset.png")

    mainMenuImg = transform.smoothscale(mainMenuImg, (playRect[-2], playRect[-1]))
    mainMenuButton= screen.blit(mainMenuImg,(width//2-150-2,height//2-50))
    

    resetImg = transform.smoothscale(resetImg, (playRect[-2], playRect[-1]))
    resetButton = screen.blit(resetImg,(width//2+50+2,height//2-50))

 
    start = timer()
    

    running = True
    while running:
        click= False
        keys = key.get_pressed()
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
        for evnt in event.get():          
            if (playRect.collidepoint(mx, my) and mb[0] == 1) or keys[K_k]:
                running = False
            if evnt.type== MOUSEBUTTONDOWN:
                click= True
            if evnt.type == KEYDOWN:
                keys = key.get_pressed()
                if keys[K_k]:
                    pClick = True

        if mainMenuButton.collidepoint(mx,my) and click:
            return "Main Menu"
        if resetButton.collidepoint(mx,my) and click:
            resetVals()
            return "Play Game"


        display.flip()
    elapsed += round((timer() - start))
    



##-----HIGHSCORES-------##

def timeScore(timeLeft):#score for time
    return timeLeft * 100    
    

def getOldScores():#finds old scores
    allFiles = glob.glob("User Data/*txt")
    files = [open(i, "r").read().strip().split(",") for i in allFiles]
    
    files = [[i[0], int(i[1]), int(i[2])] for i in files]
    return files
def getHighScores(files):#
    
    return sorted(files,key=lambda x:x[1], reverse=True)




def writeHighScores(dat):
    hScoreFile = open("HighScores/HighScore.txt", "w")
    for i in dat:
        hScoreFile.write("%s,%d\n" %(i[0], i[1]))
    hScoreFile.close()



    
def changeScore(userNum, username, score, timeLeft):
    usernamesFile = open("User Data/%s.txt" %(userNum),"r")
    userData = usernamesFile.read().strip().split(",")
    #changes if it is bigger than previous
    if int(userData[1]) < score:
        usernamesFile.close()
        usernamesFile = open("User Data/%s.txt" %(userNum),"w")
        usernamesFile.write("%s,%d,%d" %(username, score, timeLeft))
        usernamesFile.close()

##-----GAME FUNCTION-----##
    
def runGame():
    """This is where the main game runs"""
    global badGuys, badGuyRects, objRects, mapX, mapY, shelfRects, shelfItems, shelfItemRects, charRect, frame2, shoppingList, elapsed, page,timeWithoutPause, userNum, username

    mixer.music.set_volume(.7)
    mixer.music.play(-1) #music will repeat forever
    

    now = datetime.datetime.now()
    timeWithoutPause = now.minute*60 + now.second   

    shoppingList = generateShoppingList(shelfItems) #The list of items you need to buy

    mapX, mapY = -3334, -5506 #offset at which the map will be blit to screen

    #reset values didnt work so had to resett here rip

    shelfRects = open("Rect Data/shelf-locations-only-rects.txt").readlines()
    shelfRects = [i.split(",") for i in shelfRects]
    shelfRects = [Rect(int(i[0]), int(i[1]), int(i[2]), int(i[3])) for i in shelfRects]

    shelfItems=open("Rect Data/Item List.txt")
    shelfItems = [str(i.strip('\n')) for i in shelfItems]

    shelfItemRects = open("Rect Data/Item Rects.txt").readlines()
    shelfItemRects = [i.split(",") for i in shelfItemRects]
    shelfItemRects = [Rect(int(i[0]), int(i[1]), int(i[2]), int(i[3])) for i in shelfItemRects]

    shelfRects = rectUpdate(shelfRects, mapX, mapY)
    shelfItemRects = rectUpdate(shelfItemRects,mapX,mapY)

    
    #All the objRects
    objRects = [charRect]+shelfRects#keeps track of the objRects i have now

    badGuys, badGuyRects, objRects = badGuyCreate(400, objRects, pics)

    #Updates position of shelves in relation with the map
    rectCheck(badGuys, badGuyRects, shelfRects)

    running = True

    wasPaused = False

    myClock = time.Clock()

    score = 0
    collides = 0
    elapsed = 0
    while running:
        click=False
        for e in event.get():
            if e.type==QUIT:
                running=False
            if e.type==MOUSEBUTTONDOWN: #ill get rid of this w/e
                click=True
    #-------------------------------        
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()


        moveBadGuys(badGuys, badGuyRects, objRects)

        keys = key.get_pressed()

        
        
        #time related sutff
        
        getTime(elapsed)
        if timeLeft==-1 and len(shoppingList)!=0:
            return "Game Over"
        if timeLeft>-1 and timeLeft<300 and len(shoppingList)==0 :
            score += timeScore(timeLeft) + collides*-1000


            changeScore(userNum, username, score, timeLeft)
            writeHighScores(getHighScores(getOldScores()))
            return "Game Win"

        #if the game is paused, you wil lkeep track of time during the pause

        mapX, mapY, totalX, totalY, badGuys, badGuyRects, shelfRects, objRects, charRect, shelfItemRects = moveX(mapX, mapY, badGuys, badGuyRects, shelfRects, objRects, charRect, shelfItemRects)
        drawScene(storeMap, pics, move, frame, shoppingList, timeLeft, mapX, mapY, totalX, totalY)


        badGuyRects = [Rect(guy[0], guy[1], pics[guy[-1]][0][0].get_width(), pics[guy[-1]][0][0].get_height()) for guy in badGuys]
        #rectDraw(shelfRects+badGuyRects)
        #rectDraw(shelfItemRects)
        frame2+=1

        #rectDraw(shelfRects)
        itemBought=pickItemUp(shelfRects,shelfItems,shelfItemRects,shoppingList,click)
 

        if itemBought!=None:
            shoppingList=updateShoppingList(shoppingList,itemBought)
            

        menuOption = pauseButton(keys,mx, my, mb, pausePic, playPic)
        if menuOption!=None:
            return menuOption

        rectCheck(badGuys, badGuyRects, shelfRects)

        collides += guyCollideCheck(charRect, badGuyRects)

        myClock.tick(60)

        #print(len(badGuys))

    #-------------------------------
        display.flip()
    quit()
    return "exit"
    
##-----CONSTANTS-----##
page="Main Menu"
RIGHT = 0
DOWN = 1  
UP = 2
LEFT = 3

move=0
frame = 0
frame2 = 0

littleBoy = sprites("little boy")
fatMan = sprites("fat man")
beauty = sprites("beauty")
pokefanA = sprites("Pokefan a")
pokefanM = sprites("pokefan m")
sukhman = sprites("sukhman")

blueHead = sprites("BlueHead")
redHead = sprites("RedHead")
brunette = sprites("brunette")
farmer = sprites("Farmer Hat")
oldPerson = sprites("Old Person")
scientist = sprites("scientist")
smallBoy = sprites("SmallBoy")
snapBack = sprites("SnapBack")
yellowBow = sprites("YellowBow")


timeLimit = 300
timeLeft = 300

#All the characters available
pics = [picsCreate(littleBoy), picsCreate(fatMan), picsCreate(beauty), picsCreate(pokefanA), picsCreate(pokefanM), picsCreate(sukhman),
        picsCreate(blueHead), picsCreate(redHead), picsCreate(brunette), picsCreate(farmer), picsCreate(oldPerson), picsCreate(scientist),
        picsCreate(smallBoy), picsCreate(snapBack), picsCreate(yellowBow)]

charRect = Rect(width//2-((pics[0][0][0].get_width())//2), height//2-((pics[0][0][0].get_height())//2), pics[0][0][0].get_width(), pics[0][0][0].get_height())



#-------------------------------        
while page != "exit":
    if page == "Main Menu":
        page = runMainMenu()
    if page == "New Game":
        page = runNewGame()
    if page == "Load Game":
        page = load()
    if page == "Game Win":
        page = runGameWin()
    if page == "Game Over":
        page = runGameOver()
    if page == "Play Game":
        page = runGame()
    if page == "Instructions":
        page = runInstructions()
    if page == "Highscores":
        page = runHighscores()
    if page == "Make Profile":
        page = makeProfile()
    
#-------------------------------
quit()
