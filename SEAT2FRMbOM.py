#imports
import pygame
import sys
import time

#pygame setup
pygame.init()
pygame.font.init()

WINDOW_WIDTH = 1780
WINDOW_HEIGHT = 780
print ("67")

clock = pygame.time.Clock()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Welcome to the DUNGEON")

#global variables
starttime = 0
elapsed = pygame.time.get_ticks()
directions = ["north", "south", "east", "west"]

#font
font = pygame.font.SysFont("Arial", 40)
smolfont = pygame.font.SysFont("Arial", 20)
rooms = []

#colors
white = (255, 255, 255)
black = (0, 0, 0)
grey = (130, 130, 130)

#classes
#room
class room:
    def __init__(self, name, doors, joins, description):
        self.name = name
        self.doors = doors
        self.joins = joins
        self.description = description
    
    #def ioejf(self, direction):


#rooms
spawnroom0 = room("origination point", [1, 0, 0, 0], [1, -1, -1, -1], "")
rooms.append(spawnroom0)
armoryroom1 = room("armory room", [1, 0, 0, 0], [2, -1, -1, -1], "")
rooms.append(armoryroom1)
dungeonentrance2 = room("dungeon entrance", [1, 0, 0, 0], [3, -1,-1, -1], "")
rooms.append(dungeonentrance2)
room3 = room("the mooy room", [0, 0, 1, 1], [-1, -1, 4, 5], "")
rooms.append(room3)
room4 = room("puzzel room", [0, 0, 0, 1], [-1, -1, -1, 3], "")
rooms.append(room4)
room5 = room("room", [1, 0, 0, 1], [6, -1, 7, 3], "")
rooms.append(room5)
room6 = room("mooy ritural room", [0, 1, 1, 1], [-1, 8, 5, 9], "")
rooms.append(room6)
secretroom7 = room("secret exit!", [1, 0, 0, 0], [5, -1, -1,-1], "")
rooms.append(secretroom7)
room8 = room("puzzel room", [0, 0, 0, 1], [-1, -1, -1, 6], "")
rooms.append(room8)
room9 = room("room", [0, 1, 0, 1], [-1, 6, -1, 10], "")
rooms.append(room9)
room10 = room("room", [1, 1, 0, 0], [-1, 10, -1, 11], "")
rooms.append(room10)
fairyroom11 = room("fairy room", [1, 1, 0, 0], [12, 10, -1, -1], "")
rooms.append(fairyroom11)
bloodroom12 = room("bloodroom", [0, 0, 0, 0], [-1, -1, -1, -1], "")
rooms.append(bloodroom12)
#print(rooms)

#player
class Adventurer: 
    def __init__(self): 
        self.room = 0
        self.name = ""
        self.objects = []
        
    def describe(self):
        print (f"Your name: {self.name}")
        
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
                    return "intro"

        pygame.display.flip()
        clock.tick(30)

#intro sequence
def intro():
    screen.fill(black)
    starttime = 0
    while True:
        #non global variables
        advgs = smolfont.render("A  en   er", True, grey)
        advgsrect = advgs.get_rect(center=(890, 390))
        advsgs = smolfont.render(" VENTU ER!", True, grey)
        advsgsrect = advsgs.get_rect(center=(890, 390))
        advc = font.render("ADVENTURER!!!", True, white)
        advcrect = advc.get_rect(center=(890, 390))
        ohgood = font.render("Oh good, your awake...", True, white)
        ohgoodrect = ohgood.get_rect(center=(890, 390))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
        screen.fill(black)
        screen.blit(advgs, advgsrect)
        if starttime == 0:
            starttime = pygame.time.get_ticks()
        elapsed = pygame.time.get_ticks()-starttime
        if elapsed >= 1000 and elapsed < 4000:
            screen.fill(black)
            screen.blit(advsgs, advsgsrect)
        elif elapsed >= 4000 and elapsed < 5000:
            screen.fill(black)
            screen.blit(advc, advcrect)
        elif elapsed >= 5000 and elapsed < 6000:
            screen.fill(black)
            screen.blit(ohgood, ohgoodrect)
        elif elapsed >= 6000:
            return "naming"
            
        pygame.display.flip()
        clock.tick(30)

#naming the character
def naming():
    global name
    usertxt = ""
    name = ""
    q = ""
    while True:
        #non global variables
        remember = font.render("Do you remember your name was before?", True, white)
        confirmbtn = font.render("Confirm", True, white)
        confirmbtnr = confirmbtn.get_rect(center=(165, 225))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    usertxt = usertxt[:-1]
                elif event.key == pygame.K_RETURN:
                    q = ""
                elif len(usertxt) < 20:
                    usertxt += event.unicode
                

            if event.type == pygame.MOUSEBUTTONDOWN:
                if confirmbtnr.collidepoint(event.pos):
                    name = usertxt
                    usertxt = ""
                    #print (name)
                    return "main"
        
        namep2 = font.render(usertxt, True, white)

        screen.fill(black)
        screen.blit(remember, (100, 100))
        screen.blit(namep2, (100, 150))

        if len(usertxt) >= 3:
            screen.blit(confirmbtn, confirmbtnr)

        pygame.display.flip()
        clock.tick(30)

def main():
    adventurer.name = name
    btn_w, btn_h = 140, 60
    north_rect = pygame.Rect(WINDOW_WIDTH // 2 - btn_w // 2, 450, btn_w, btn_h)
    south_rect = pygame.Rect(WINDOW_WIDTH // 2 - btn_w // 2, 610, btn_w, btn_h)
    east_rect  = pygame.Rect(WINDOW_WIDTH // 2 + btn_w,     530, btn_w, btn_h)
    west_rect  = pygame.Rect(WINDOW_WIDTH // 2 - btn_w * 2, 530, btn_w, btn_h)
    buttons = {
        0: {"rect": north_rect, "text": "NORTH"},
        1: {"rect": south_rect, "text": "SOUTH"},
        2: {"rect": east_rect,  "text": "EAST"},
        3: {"rect": west_rect,  "text": "WEST"}
    }
    while True:
        screen.fill(black)
        current_room_id = adventurer.room
        current_room = rooms[current_room_id]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for direction_index, button_data in buttons.items():
                        if button_data["rect"].collidepoint(event.pos):
                            
                            destination_room = current_room.joins[direction_index]
                            
                            if destination_room != -1:
                                adventurer.room = destination_room
                                print(f"Moved to: {rooms[destination_room].name}")
                            else:
                                print("Ouch! You walked straight into a wall.")
        
        room_title = font.render(f"Room: {current_room.name.upper()}", True, white)
        screen.blit(room_title, (100, 50))
        
        player_info = smolfont.render(f"Adventurer: {adventurer.name} | Room ID: {current_room_id}", True, grey)
        screen.blit(player_info, (100, 110))

        for direction_index, button_data in buttons.items():
            path_exists = current_room.joins[direction_index] != -1
            
            button_color = grey if path_exists else (40, 40, 40)
            text_color = white if path_exists else grey

            pygame.draw.rect(screen, button_color, button_data["rect"])
        
            btn_txt = smolfont.render(button_data["text"], True, text_color)
            txt_rect = btn_txt.get_rect(center=button_data["rect"].center)
            screen.blit(btn_txt, txt_rect)

        pygame.display.flip()
        clock.tick(30)

#state manager
state = "term"
adventurer = Adventurer()
while True:
    if state == "title":
        state = titlescreen()
    elif state == "term":
        state = termwarning()
    elif state == "intro":
        state = intro()
    elif state == "naming":
        state = naming()
    elif state == "main":
        state = main()
    elif state == "quit":
        break

pygame.quit()
sys.exit()