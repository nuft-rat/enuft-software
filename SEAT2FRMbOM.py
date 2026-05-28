#imports
import pygame
import sys
import time

#pygame setup
pygame.init()
pygame.font.init()

WINDOW_WIDTH = 1780
WINDOW_HEIGHT = 780

clock = pygame.time.Clock()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Welcome to the DUNGEON")

#global variables
#font
font = pygame.font.SysFont("Arial", 40)
rooms = []

#colors
white = (255, 255, 255)
black = (0, 0, 0)

#classes
#room
class room:
    def __init__(self, name, doors, joins):
        self.name = name
        self.doors = doors
        self.joins = joins

#rooms
spawnroom0 = room("origination point", [1, 0, 0, 0], [1, -1, -1, -1])
rooms.append(spawnroom0)
armoryroom1 = room("armory room", [1, 0, 0, 0], [2, -1, -1, -1])
rooms.append(armoryroom1)
dungeonentrance2 = room("dungeon entrance", [1, 0, 0, 0], [3, -1,-1, -1])
rooms.append(dungeonentrance2)
room3 = room("the mooy room", [0, 1, 0, 1], [-1, 4, -1, 5])
rooms.append(room3)
room4 = room("puzzel room", [0, 0, 0, 1], [-1, -1, -1, 3])
rooms.append(room4)
room5 = ("room", [1, 0, 0, 1], [6, -1, 7, 3])
rooms.append(room5)
room6 = room("mooy ritural room", [0, 1, 1, 1], (-1, 8, 5, 9))
rooms.append(room6)
secretroom7 = ("secret exit!", [1, 0, 0, 0], [5, -1, -1,-1])
rooms.append(secretroom7)
room8 = ("puzzel room", [0, 0, 0, 1], [-1, -1, -1, 6])
rooms.append(room8)
room9 = ("room", [0, 1, 0, 1], [-1, 6, -1, 10])
rooms.append(room9)
room10 = ("room", [1, 1, 0, 0], [11, 10, -1, -1])
rooms.append(room10)
bloodroom11 = ("bloodroom", [0, 0, 0, 0], [-1, -1, -1, -1])
rooms.append(bloodroom11)
#print(rooms)

#player
class Adventurer: 
    def __init__(self): 
        self.room = 0
        self.objects = []
        
    # Set up the character
    def set_up_character(self):
        #non global variables
        adventurergs = font.render("ᔑ↸⍊ᒷリℸ ̣ ⚍∷ᒷ∷", True, white)
        adventurersgs = font.render("A↸⍊Eリℸ ̣ ⚍Rᒷ∷!", True, white)
        adventurerc = font.render("ADVENTURER!!!", True, white)
        ohgood = font.render("Oh good, your awake...", True, white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
        screen.blit(adventurergs, (890, 490))
        time.sleep(1)
        #screen.fill(black)
        print ("A↸⍊Eリℸ ̣ ⚍Rᒷ∷!")
        time.sleep(3)
        print ("ADVENTURER!!!")
        time.sleep(0.5)
        print ("Oh good, you awake...")
        time.sleep(0.25)
        remember = input("Do you remember your name? ")

        if remember == "no":
            self.name = input("Then what would you like me to call you? ")
            self.gender = input("Are you male (m) or female (f)? ")
            self.age = int(input("Do you remember how old you were? "))
            while self.__validate_age(self.age) == False :
                print (f"{self.name}... you seem to have told me an unrealistic age. Do not lie to me, your age is between 0 and 100.")
                self.age = int(input("Do you remember how old you *really* were? "))

        elif remember == "yes":
            self.name = input("Then what is your name adventurer? ")
            self.gender = input("Are you male (m) or female (f)? ") 
            self.age = int(input("And finally, how old are you? "))
            while self.__validate_age(self.age) == False :
                print ("Either you entered an age which is too old or too young. Dont do it again.")
                self.age = int(input("How old are you *really*? "))
        
        pygame.display.flip()
        clock.tick(30)
    
    def __validate_age(self, age):
        if age < 0 or age > 100:
            return False
        else :
            return True

        
    def describe(self):
        print (f"Your name: {self.name}")
        print (f"Your gender: {self.gender}")
        print (f"Your age: {self.age}")
        
        print (f"You are currently in room {self.room}")

#functions
#termwarning
def termwarning():
    while True:
        #non global variables
        termtxt = font.render("Please have terminal below as some stuff will be there!", True, white)
        rect1 = pygame.Rect(445, 95, 1000, 55)
        rect2 = pygame.Rect(815, 430, 170, 50)
        cont = font.render("Continue", True, white)
        contrect = cont.get_rect(center = (900, 450))
  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
        
        pygame.draw.rect(screen, black, rect1)
        pygame.draw.rect(screen, black, rect2)
        screen.blit(termtxt, (450, 100))
        screen.blit(cont, contrect)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if contrect.collidepoint(event.pos):
                return "title"

        pygame.display.flip()
        clock.tick(30)

#title
def titlescreen():
    screen.fill(black)
    while True:
        #non global variables
        enuftg = font.render("Enuft Games'", True, white)
        advgamettl = font.render("Welcome to the DUNGEON", True, white)
        startbtn = font.render("Enter the DUNGEON", True, white)
        startbtnr = startbtn.get_rect(center = (230, 300))
        rect1 = pygame.Rect(780, 100, 240, 50)
        rect2 = pygame.Rect(650, 200, 475, 50)
        rect3 = pygame.Rect(50, 275, 370, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            pygame.draw.rect(screen, black, rect1)
            pygame.draw.rect(screen, black, rect2)
            pygame.draw.rect(screen, black, rect3)
            screen.blit(enuftg, (770, 100))
            screen.blit(advgamettl, (650, 200))
            screen.blit(startbtn, startbtnr)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if startbtnr.collidepoint(event.pos):
                    return "main"

        pygame.display.flip()
        clock.tick(30)

#main
def main():
    screen.fill(black)
    while True:
        #non global variables
        adventurer = Adventurer()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            adventurer.set_up_character()
            adventurer.describe()
            
        pygame.display.flip()
        clock.tick(30)

#state manager
state = "term"
while True:
    if state == "title":
        state = titlescreen()
    elif state == "term":
        state = termwarning()
    elif state == "main":
        state == main()
    elif state == "quit":
        break

pygame.quit()
sys.exit()