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
start_time = 0
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
# [north, south, east, west]
spawnroom0 = room("origination point", [1, 0, 0, 0], [1, -1, -1, -1], "")
rooms.append(spawnroom0)
armoryroom1 = room("armory room", [1, 0, 0, 0], [2, -1, -1, -1], "")
rooms.append(armoryroom1)
dungeonentrance2 = room("dungeon entrance", [1, 0, 0, 0], [3, -1,-1, -1], "")
rooms.append(dungeonentrance2)
room3 = room("the mooy room", [0, 0, 1, 1], [-1, -1, 5, 4], "")
rooms.append(room3)
room4 = room("puzzel room", [0, 0, 0, 1], [-1, -1, 3, -1], "")
rooms.append(room4)
room5 = room("room", [1, 0, 0, 1], [6, 7, -1, 3], "")
rooms.append(room5)
room6 = room("mooy ritural room", [0, 1, 1, 1], [-1, 5, 8, 9], "")
rooms.append(room6)
secretroom7 = room("secret exit!", [1, 0, 0, 0], [5, -1, -1,-1], "")
rooms.append(secretroom7)
room8 = room("puzzel room", [0, 0, 0, 1], [-1, -1, -1, 6], "")
rooms.append(room8)
room9 = room("room", [0, 0, 1, 1], [-1, -1, 6, 10], "")
rooms.append(room9)
fairyroom10 = room("fairy room", [1, 0, 1, 0], [11, -1, 9, -1], "")
rooms.append(fairyroom10)
bloodroom11 = room("bloodroom", [0, 0, 0, 0], [-1, -1, -1, -1], "")
rooms.append(bloodroom11)
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
        term_txt = font.render("Please have terminal below as some stuff will be there!", True, white)
        rect1 = pygame.Rect(445, 95, 1000, 55)
        rect2 = pygame.Rect(815, 430, 170, 50)
        cont = font.render("Continue", True, white)
        cont_rect = cont.get_rect(center = (900, 450))
  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
        
        pygame.draw.rect(screen, black, rect1)
        pygame.draw.rect(screen, black, rect2)
        screen.blit(term_txt, (450, 100))
        screen.blit(cont, cont_rect)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if cont_rect.collidepoint(event.pos):
                return "title"

        pygame.display.flip()
        clock.tick(30)

#title
def titlescreen():
    screen.fill(black)
    while True:
        #non global variables
        enuft_games = font.render("Enuft Games'", True, white)
        adventure_game_title = font.render("Welcome to the DUNGEON", True, white)
        start_btn = font.render("Enter the DUNGEON", True, white)
        start_btnr = start_btn.get_rect(center = (230, 300))
        rect1 = pygame.Rect(780, 100, 240, 50)
        rect2 = pygame.Rect(650, 200, 475, 50)
        rect3 = pygame.Rect(50, 275, 370, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            pygame.draw.rect(screen, black, rect1)
            pygame.draw.rect(screen, black, rect2)
            pygame.draw.rect(screen, black, rect3)
            screen.blit(enuft_games, (770, 100))
            screen.blit(adventure_game_title, (650, 200))
            screen.blit(start_btn, start_btnr)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btnr.collidepoint(event.pos):
                    return "intro"

        pygame.display.flip()
        clock.tick(30)

#intro sequence
def intro():
    screen.fill(black)
    starttime = 0
    while True:
        #non global variables
        adventurer_txt1 = smolfont.render("A  en   er", True, grey)
        adventurer_txtr1 = adventurer_txt1.get_rect(center=(890, 390))
        adventurer_txt2 = smolfont.render(" VENTU ER!", True, grey)
        adventurer_txtr2 = adventurer_txt2.get_rect(center=(890, 390))
        adventurer_txt3 = font.render("ADVENTURER!!!", True, white)
        adventurer_txtr3 = adventurer_txt3.get_rect(center=(890, 390))
        ohgood_txt = font.render("Oh good, your awake...", True, white)
        ohgood_txtr = ohgood_txt.get_rect(center=(890, 390))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
        screen.fill(black)
        screen.blit(adventurer_txt1, adventurer_txtr1)
        if starttime == 0:
            starttime = pygame.time.get_ticks()
        elapsed = pygame.time.get_ticks()-starttime
        if elapsed >= 1000 and elapsed < 4000:
            screen.fill(black)
            screen.blit(adventurer_txt2, adventurer_txtr2)
        elif elapsed >= 4000 and elapsed < 5000:
            screen.fill(black)
            screen.blit(adventurer_txt3, adventurer_txtr3)
        elif elapsed >= 5000 and elapsed < 6000:
            screen.fill(black)
            screen.blit(ohgood_txt, ohgood_txtr)
        elif elapsed >= 6000:
            return "naming"
            
        pygame.display.flip()
        clock.tick(30)

#naming the character
def naming():
    global name
    user_txt = ""
    name = ""
    q = ""
    while True:
        #non global variables
        remember = font.render("Do you remember your name was before?", True, white)
        confirm_btn = font.render("Confirm", True, white)
        confirm_btnr = confirm_btn.get_rect(center=(165, 225))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_txt = user_txt[:-1]
                elif event.key == pygame.K_RETURN:
                    q = ""
                elif len(user_txt) < 20:
                    user_txt += event.unicode
                

            if event.type == pygame.MOUSEBUTTONDOWN:
                if confirm_btnr.collidepoint(event.pos):
                    name = user_txt
                    user_txt = ""
                    #print (name)
                    return "main"
        
        namep2 = font.render(user_txt, True, white)

        screen.fill(black)
        screen.blit(remember, (100, 100))
        screen.blit(namep2, (100, 150))

        if len(user_txt) >= 3:
            screen.blit(confirm_btn, confirm_btnr)

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