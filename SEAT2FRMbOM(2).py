#imports
import pygame
import sys
import os

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
username = ""
password = ""
file = "loginstuff.txt"
name = ""

#font
font = pygame.font.SysFont("Arial", 40)
smolfont = pygame.font.SysFont("Arial", 20)
rooms = []
enemies = []

#colors
white = (255, 255, 255)
black = (0, 0, 0)
grey = (130, 130, 130)
green = (0, 255, 0)
red = (255, 0, 0)
darkgrey = (40, 40, 40)

#classes
#room
class room:
    def __init__(self, name, doors, joins, description):
        self.name = name
        self.doors = doors
        self.joins = joins
        self.description = description
        self.locked_door = {}

#health bar
class HealthBar:
    def __init__(self, x, y, width, height, max_hp, color=green):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_hp = max_hp
        self.color = color

    def draw(self, surface, current_hp):
        ratio = max(0.0, min(current_hp / self.max_hp, 1.0))
       
        pygame.draw.rect(surface, red, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, self.color, (self.x, self.y, int(self.width * ratio), self.height))

#enemy
class Enemy:
    def __init__(self, name, hp, attack, room_id):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.room = room_id
        self.is_alive = True
        self.health_bar = HealthBar(100, 260, 300, 15, self.max_hp)
        self.last_attack_time = 0
        self.attack_cooldown = 1500
    
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False

    def update_combat(self, player_target):
        if self.is_alive:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_attack_time >= self.attack_cooldown:
                player_target.hp = max(0, player_target.hp - self.attack)
                self.last_attack_time = current_time
                return f"{self.name} hit you for {self.attack} DMG!"
        return None

#weapons
class Weapon:
    def __init__(self, name, damage_modifier, speed_modifier):
        self.name = name
        self.damage_mod = damage_modifier
        self.speed_mod = speed_modifier

#player
class Adventurer:
    def __init__(self):
        self.room = 0
        self.name = ""
        self.password = password
        self.objects = []
        self.max_hp = 100
        self.hp = 100
        self.base_damage = 5
        self.base_speed = 1000
        self.weapon = Weapon("Fists", 0, 0)
        self.has_chosen_weapon = False


    def get_total_damage(self):
        return self.base_damage + self.weapon.damage_mod
   
    def get_total_speed(self):
        return max(200, self.base_speed - self.weapon.speed_mod)

adventurer = Adventurer()

#lists for classes
#rooms
#"name", [1 = door, 0 = no door][north, south, east, west], "room description"
spawnroom0 = room("origination point", [1, 0, 0, 0], [1, -1, -1, -1], "")
rooms.append(spawnroom0)
armoryroom1 = room("armory room", [1, 0, 0, 0], [2, -1, -1, -1], "")
rooms.append(armoryroom1)
dungeonentrance2 = room("dungeon entrance", [1, 0, 0, 0], [3, -1,-1, -1], "")
rooms.append(dungeonentrance2)
room3 = room("the mooy room", [0, 0, 1, 1], [-1, -1, 5, 4], "")
rooms.append(room3)
room4 = room("puzzle room", [0, 0, 1, 0], [-1, -1, 3, -1], "")
rooms.append(room4)
room5 = room("corpse room", [1, 0, 0, 1], [6, 7, -1, 3], "")
rooms.append(room5)
room6 = room("mooy ritural room", [0, 1, 1, 1], [-1, 5, 8, 9], "")
rooms.append(room6)
secretroom7 = room("secret room", [1, 1, 0, 0], [5, 12, -1,-1], "")
rooms.append(secretroom7)
room8 = room("puzzle room", [0, 0, 0, 1], [-1, -1, -1, 6], "")
rooms.append(room8)
room9 = room("room", [0, 0, 1, 1], [-1, -1, 6, 10], "")
rooms.append(room9)
fairyroom10 = room("fairy room", [1, 0, 1, 0], [11, -1, 9, -1], "")
rooms.append(fairyroom10)
bloodroom11 = room("bloodroom", [1, 0, 0, 0], [12, -1, -1, -1], "")
rooms.append(bloodroom11)
winconditionroom12 = room("12", [0, 0, 0, 0], [-1, -1, -1, -1], "")
rooms.append(winconditionroom12)
room3.locked_door = {"east": "mooy key"}
room5.locked_door = {"north": "mooy key"}
room6.locked_door = {"west": "mooy key"}
fairyroom10.locked_door = {"north": "blood key"}
#print(rooms)

#enemys
#"name", health, damage, spawnroom
light_enemy = Enemy("Jenkins", 30, 5, 5)
enemies.append(light_enemy)
medium_enemy = Enemy("Skaggs", 50, 8, 9)
enemies.append(medium_enemy)
heavy_enemy = Enemy("Friggin Bartholemule The 8th yo!", 70, 12, 11)
enemies.append(heavy_enemy)
innocent_fairy = Enemy("An Innocent Fairy", 60, 0, 10)
enemies.append(innocent_fairy)

#weapons
weapons_pool = {
    "rustysword": Weapon("Rusty Sword", 5, 200),
    "heavyaxe": Weapon("Heavy Axe", 15, -300),
    "dungeonknife": Weapon("Swift Dagger", 2, 500)
}

#functions
#title
def titlescreen():
    while True:
        #non global variables
        enuft_games = font.render("Enuft Games'", True, white)
        adventure_game_title = font.render("Welcome to the DUNGEON", True, white)
        start_button = font.render("Enter the DUNGEON", True, white)
        start_buttonr = start_button.get_rect(center = (230, 300))
        
        has_save = os.path.exists(file)
        load_color = white if has_save else grey
        load_button = font.render("Load Saved Progress", True, load_color)
        load_buttonr = load_button.get_rect(center=(230, 400))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_buttonr.collidepoint(event.pos):
                    return "intro"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if load_buttonr.collidepoint(event.pos):
                    return "login"
        
        screen.fill(black)
        screen.blit(enuft_games, (770, 100))
        screen.blit(adventure_game_title, (650, 200))
        screen.blit(start_button, start_buttonr)
        screen.blit(load_button, load_buttonr)

        if not has_save:
            no_save_txt = smolfont.render("(No saved game data found)", True, grey)
            no_save_rect = no_save_txt.get_rect(center=(230, 450))
            screen.blit(no_save_txt, no_save_rect)

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
    global password
    user_txt = ""
    name = ""
    namep2 = font.render("", True, white)
    password = ""
    passwordp2 = font.render("", True, white)
    typing_field = "playername"
    stop_enter_from_working = ""
    while True:
        #non global variables
        remember = font.render("Do you remember your name was before?", True, white)
        password_enter = font.render("Please enter a password: ", True, white)
        cont_button = font.render("Continue", True, white)
        cont_buttonr = cont_button.get_rect(center=(165, 275))
        press_tab = smolfont.render("please press tab to switch fields and again when you finish typing the password to unlock the continue button", True, grey)
        press_tab2 = smolfont.render("name and password must be more than 3 char long!", True, grey)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
           
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_txt = user_txt[:-1]
                elif event.key == pygame.K_TAB:
                    if typing_field == "playername":
                        name = user_txt
                        user_txt = ""
                    elif typing_field == "playerpasskey":
                        password = user_txt
                    typing_field = "playerpasskey"
                elif event.key == pygame.K_RETURN:
                    stop_enter_from_working = ""
                elif len(user_txt) < 20:
                    user_txt += event.unicode
               
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cont_buttonr.collidepoint(event.pos):
                    password = user_txt
                    user_txt = ""
                    #print (name)
                    return "main"
        
        if typing_field == "playername":
            namep2 = font.render(user_txt, True, white)
        elif typing_field == "playerpasskey":
            namep2 = font.render(name, True, white)
            passwordp2 = font.render(user_txt, True, white)

        screen.fill(black)
        screen.blit(remember, (100, 100))
        screen.blit(password_enter, (100, 150))
        screen.blit(namep2, (830, 100))
        screen.blit(passwordp2, (540, 150))
        screen.blit(press_tab, (100, 200))
        screen.blit(press_tab2, (100, 225))

        if len(name) >= 3 and len(password) >=3:
            screen.blit(cont_button, cont_buttonr)

        pygame.display.flip()
        clock.tick(30)

def login_screen():
    global username, password
    print("\n" + "="*40)
    print("      DUNGEON LOGIN & REGISTRATION      ")
    print("="*40)
    print("Please look at your terminal window to type.")
    
    user_input = input("Enter Username: ").strip()
    pass_input = input("Enter Password: ").strip()
    
    while not user_input or not pass_input:
        print("\n[ERROR] Fields cannot be empty. Try again.")
        user_input = input("Enter Username: ").strip()
        pass_input = input("Enter Password: ").strip()
        
    username = user_input
    password = pass_input
    
    existing_room = 0
    existing_hp = 100
    existing_weapon = "Fists"
    existing_inventory = ""
    
    if os.path.exists(file):
        try:
            with open(file, "r") as f:
                for line in f:
                    if line.startswith("room:"):
                        existing_room = int(line.strip().split(":", 1)[1])
                    elif line.startswith("hp:"):
                        existing_hp = int(line.strip().split(":", 1)[1])
                    elif line.startswith("weapon:"):
                        existing_weapon = line.strip().split(":", 1)[1]
                    elif line.startswith("inventory:"):
                        parts = line.strip().split(":", 1)
                        if len(parts) > 1:
                            existing_inventory = parts[1]
        except Exception as e:
            print(f"[LOGIN WARNING] Reading existing save layout failed: {e}")

    with open(file, "w") as f:
        f.write(f"username:{username}\n")
        f.write(f"password:{password}\n")
        f.write(f"room:{existing_room}\n")
        f.write(f"hp:{existing_hp}\n")
        f.write(f"weapon:{existing_weapon}\n")
        f.write(f"inventory:{existing_inventory}\n")
        
    print("\n[SUCCESS] Profile synced! Loading your progress...")
    print("="*40 + "\n")
    return "load"

def save_game():
    saved_user, saved_pass = adventurer.name, adventurer.password
    
    if os.path.exists(file):
        try:
            with open(file, "r") as f:
                for line in f:
                    if line.startswith("username:"):
                        saved_user = line.strip().split(":", 1)[1]
                    elif line.startswith("password:"):
                        saved_pass = line.strip().split(":", 1)[1]
        except Exception as e:
            print(f"[SAVE WARNING] Could not parse old log file credentials: {e}")

    if not saved_user: saved_user = adventurer.name

    wpn_key = "Fists"
    for k, v in weapons_pool.items():
        if v.name == adventurer.weapon.name:
            wpn_key = k
            break

    try:
        with open(file, "w") as f:
            f.write(f"username:{saved_user}\n")
            f.write(f"password:{saved_pass}\n")
            f.write(f"room:{int(adventurer.room)}\n")
            f.write(f"hp:{int(adventurer.hp)}\n")
            f.write(f"weapon:{str(wpn_key)}\n")
            f.write(f"inventory:{','.join(adventurer.objects)}\n")
        print(f"[TERMINAL LOG] Game saved successfully! Room: {adventurer.room} | HP: {adventurer.hp}")
    except Exception as e:
        print(f"[TERMINAL ERROR] Failed writing save state data: {e}")

def load_game():
    global name
    print("\n" + "-"*40)
    print("  TERMINAL LOG: INITIALISING LEVEL LOAD  ")
    print("-"*40)
    
    if not os.path.exists(file):
        print("[LOAD ERROR] No target save file found on disk.")
        return False
        
    try:
        with open(file, "r") as f:
            for line in f:
                line = line.strip()
                if not line or ":" not in line:
                    continue
                key, val = line.split(":", 1)
                
                if key == "username":
                    name = str(val)
                    adventurer.name = str(val)
                    print(f" > Loaded Adventurer Profile: {name}")
                elif key == "room":
                    adventurer.room = int(val)
                    print(f" > Dispatched to Room Space: {adventurer.room}")
                elif key == "hp":
                    loaded_hp = int(val)
                    adventurer.hp = loaded_hp if loaded_hp > 0 else adventurer.max_hp
                    print(f" > Restored Health Pools: {adventurer.hp}/{adventurer.max_hp}")
                elif key == "weapon":
                    if val in weapons_pool:
                        adventurer.weapon = weapons_pool[val]
                        adventurer.has_chosen_weapon = True
                    else:
                        adventurer.weapon = Weapon("Fists", 0, 0)
                        adventurer.has_chosen_weapon = False
                    print(f" > Standardised Weaponry Core: {adventurer.weapon.name}")
                elif key == "inventory":
                    if val and val.strip():  
                        adventurer.objects = val.split(",")
                    else:
                        adventurer.objects = []
                    print(f" > Vault Inventory Synced: {adventurer.objects}")
                    
        for enemy in enemies:
            enemy.hp = enemy.max_hp
            enemy.is_alive = True
            enemy.last_attack_time = pygame.time.get_ticks() + 1000
            
        print("[LOAD SUCCESS] Core matrices verified. Opening Pygame screen.")
        print("-"*40 + "\n")
        return True
    except Exception as e:
        print(f"[CRITICAL PARSE ERROR] Load operation failed: {e}")
        return False

def main():
    global name
    adventurer.name = name
    button_w, button_h = 140, 60
    north_rect = pygame.Rect(WINDOW_WIDTH // 2 - button_w // 2, 450, button_w, button_h)
    south_rect = pygame.Rect(WINDOW_WIDTH // 2 - button_w // 2, 610, button_w, button_h)
    east_rect  = pygame.Rect(WINDOW_WIDTH // 2 + button_w, 530, button_w, button_h)
    west_rect  = pygame.Rect(WINDOW_WIDTH // 2 - button_w * 2, 530, button_w, button_h)
    buttons = {
        0: {"rect": north_rect, "text": "NORTH"},
        1: {"rect": south_rect, "text": "SOUTH"},
        2: {"rect": east_rect,  "text": "EAST"},
        3: {"rect": west_rect,  "text": "WEST"}
    }

    weapon_buttons = {
        "rustysword": {"rect": pygame.Rect(100, 450, 220, 50), "text": "Pick Rusty Sword"},
        "heavyaxe":   {"rect": pygame.Rect(100, 520, 220, 50), "text": "Pick Heavy Axe"},
        "dungeonknife": {"rect": pygame.Rect(100, 590, 220, 50), "text": "Pick Swift Dagger"}
    }

    player_health_bar = HealthBar(WINDOW_WIDTH - 210, 32, 200, 20, adventurer.max_hp)
    attack_btn_rect = pygame.Rect(100, 340, 200, 50)
    combat_log = ["Dungeon entered. Stay alert..."]
    player_last_attack = 0

    puzzle_input = ""
    puzzle_input2 = ""
    puzzle_solved = False
    puzzle_solved2 = False
    enemies_killed = 0

    while True:
        screen.fill(black)
        current_room_id = adventurer.room
        current_room = rooms[current_room_id]

        #win condition
        if current_room_id == 12:
            screen.fill(black)
            victory_txt = font.render("VICTORY! You escaped the DUNGEON!", True, green)
            congrat_txt = smolfont.render(f"Congratulations, {adventurer.name}! You survived the depths.", True, white)
           
            screen.blit(victory_txt, (WINDOW_WIDTH // 2 - 300, WINDOW_HEIGHT // 2 - 50))
            screen.blit(congrat_txt, (WINDOW_WIDTH // 2 - 250, WINDOW_HEIGHT // 2 + 20))
           
            pygame.display.flip()
            pygame.time.delay(4000)
           
            adventurer.room = 0
            adventurer.hp = adventurer.max_hp
            adventurer.weapon = Weapon("Fists", 0, 0)
            adventurer.has_chosen_weapon = False
            adventurer.objects = []
            enemies_killed = 0
           
            for enemy in enemies:
                enemy.hp = enemy.max_hp
                enemy.is_alive = True
               
            return "title"

        #loss contition
        if adventurer.hp <= 0:
            game_over_txt = font.render("YOU DIED! Game Over.", True, red)
            screen.blit(game_over_txt, (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(3000)
           
            adventurer.room = 0
            adventurer.hp = adventurer.max_hp
            adventurer.weapon = Weapon("Fists", 0, 0)
            adventurer.has_chosen_weapon = False
            adventurer.objects = []
            enemies_killed = 0
           
            for enemy in enemies:
                enemy.hp = enemy.max_hp
                enemy.is_alive = True
               
            return "title"

        hp_label = smolfont.render("HEALTH:", True, white)
        wpn_text = smolfont.render(f"Weapon: {adventurer.weapon.name}", True, grey)
        dmg_text = smolfont.render(f"Total DMG: {adventurer.get_total_damage()}", True, grey)
        spd_text = smolfont.render(f"Attack Delay: {adventurer.get_total_speed()}ms", True, grey)
       
        screen.blit(hp_label, (WINDOW_WIDTH - 300, 30))
        screen.blit(wpn_text, (WINDOW_WIDTH - 300, 80))
        screen.blit(dmg_text, (WINDOW_WIDTH - 300, 110))
        screen.blit(spd_text, (WINDOW_WIDTH - 300, 140))
       
        player_health_bar.draw(screen, adventurer.hp)

        current_enemy = None
        for enemy in enemies:
            if enemy.room == current_room_id and enemy.is_alive:
                current_enemy = enemy
                break

        if current_enemy:
            enemy_text = font.render(f"{current_enemy.name} blocks your path!", True, (255, 50, 50))
            screen.blit(enemy_text, (100, 200))
            current_enemy.health_bar.draw(screen, current_enemy.hp)
            current_enemy.update_combat(adventurer)

            enemy_msg = current_enemy.update_combat(adventurer)
            if enemy_msg:
                combat_log.append(enemy_msg)
           
            pygame.draw.rect(screen, red, attack_btn_rect)
            atk_lbl = smolfont.render("ATTACK MONSTER", True, white)
            screen.blit(atk_lbl, atk_lbl.get_rect(center=attack_btn_rect.center))

        if len(combat_log) > 4:
            combat_log = combat_log[-4:]
           
        log_y = 450 if not current_enemy else 400
        for i, log_entry in enumerate(combat_log):
            text_color = red if "DMG" in log_entry and "You" not in log_entry else (green if "You hit" in log_entry else grey)
            log_surface = smolfont.render(log_entry, True, text_color)
            screen.blit(log_surface, (100, log_y + (i * 25)))

        if current_room_id == 1 and not adventurer.has_chosen_weapon:
            instruction_txt = smolfont.render("You must choose a weapon before you can leave:", True, white)
            screen.blit(instruction_txt, (100, 400))
           
            for wpn_id, btn_data in weapon_buttons.items():
                pygame.draw.rect(screen, grey, btn_data["rect"])
                btn_txt = smolfont.render(btn_data["text"], True, white)
                txt_rect = btn_txt.get_rect(center=btn_data["rect"].center)
                screen.blit(btn_txt, txt_rect)

        elif current_room_id == 1 and adventurer.has_chosen_weapon:
            taken_txt = smolfont.render(f"You have taken the {adventurer.weapon.name}. The other racks are bare.", True, grey)
            screen.blit(taken_txt, (100, 400))
                       
        if current_room_id == 4:
            if not puzzle_solved:
                puzzle_q = font.render("A magical barrier holds your key. Solve: 9 + 10", True, white)
                puzzle_a = font.render(f"Your Answer: {puzzle_input}", True, green if puzzle_input == "19" else red)
                instruction = smolfont.render("Type your answer and press ENTER to submit.", True, grey)
               
                screen.blit(puzzle_q, (100, 310))
                screen.blit(puzzle_a, (100, 370))
                screen.blit(instruction, (100, 420))

        if current_room_id == 8:
            if not puzzle_solved2:
                puzzle_q2 = font.render("A magical barrier holds your key. Solve: 136 / 8", True, white)
                puzzle_a2 = font.render(f"Your Answer: {puzzle_input2}", True, green if puzzle_input2 == "17" else red)
                instruction2 = smolfont.render("Type your answer and press ENTER to submit.", True, grey)
               
                screen.blit(puzzle_q2, (100, 310))
                screen.blit(puzzle_a2, (100, 370))
                screen.blit(instruction2, (100, 420))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
           
            if event.type == pygame.KEYDOWN and current_room_id == 4 and not puzzle_solved:
                if event.key == pygame.K_BACKSPACE:
                    puzzle_input = puzzle_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if puzzle_input.strip() == "19":
                        puzzle_solved = True
                        adventurer.objects.append("mooy key")
                        combat_log.append("Correct! You received a Mooy Key.")
                    else:
                        combat_log.append("The magical barrier flashes red. Incorrect answer.")
                        puzzle_input = ""
                else:
                    if event.unicode.isdigit() and len(puzzle_input) < 5:
                        puzzle_input += event.unicode

            if event.type == pygame.KEYDOWN and current_room_id == 8 and not puzzle_solved2:
                if event.key == pygame.K_BACKSPACE:
                    puzzle_input2 = puzzle_input2[:-1]
                elif event.key == pygame.K_RETURN:
                    if puzzle_input2.strip() == "17":
                        puzzle_solved2 = True
                        adventurer.objects.append("mooy key")
                        combat_log.append("Correct! You received a Mooy Key.")
                    else:
                        combat_log.append("The magical barrier flashes red. Incorrect answer.")
                        puzzle_input2 = ""
                else:
                    if event.unicode.isdigit() and len(puzzle_input2) < 5:
                        puzzle_input2 += event.unicode
           
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    if current_enemy and attack_btn_rect.collidepoint(event.pos):
                        now = pygame.time.get_ticks()
                        if now - player_last_attack >= adventurer.get_total_speed():
                            dmg_dealt = adventurer.get_total_damage()
                            current_enemy.take_damage(dmg_dealt)
                           
                            if current_enemy.is_alive:
                                combat_log.append(f"You hit {current_enemy.name} for {dmg_dealt} DMG!")
                            else:
                                combat_log.append(f"You defeated {current_enemy.name}!")
                                if current_enemy.name == "Jenkins":
                                    adventurer.objects.append("mooy key")
                                    combat_log.append("You found a mooy key on Jenkins' corpse.")
                                elif current_enemy.name == "An Innocent Fairy":
                                    adventurer.objects.append("blood key")
                                    combat_log.append("The fairy's blood coagulates into a key.")

                            save_game()

                            player_last_attack = now
                   
                    if current_room_id == 1 and not adventurer.has_chosen_weapon:
                        for wpn_id, btn_data in weapon_buttons.items():
                            if btn_data["rect"].collidepoint(event.pos):
                                adventurer.weapon = weapons_pool[wpn_id]
                                adventurer.has_chosen_weapon = True

                    can_move = True

                    if current_room_id == 1 and not adventurer.has_chosen_weapon:
                        can_move = False

                    if current_enemy:
                        can_move = False

                    if current_room_id == 4 and not puzzle_solved:
                        can_move = False

                    if current_room_id == 8 and not puzzle_solved2:
                        can_move = False

                    if can_move:
                        for direction_index, button_data in buttons.items():
                            if button_data["rect"].collidepoint(event.pos):
                                destination_room = current_room.joins[direction_index]
                           
                                if destination_room != -1:
                                    direction_name = directions[direction_index]

                                    if direction_name in current_room.locked_door:
                                        required_key = current_room.locked_door[direction_name]
                                        if required_key in adventurer.objects:
                                            del current_room.locked_door[direction_name]
                                            for i in adventurer.objects:
                                                if i == "mooy key":
                                                    adventurer.objects.remove("mooy key")
                                            adventurer.room = destination_room
                                            combat_log.append(f"You used the {required_key} and unlocked the door!")
                                            combat_log.append("The key disintergrated after the door opened.")
                                            save_game()
                                        else:
                                            combat_log.append(f"The {direction_name} door is locked! Needs: {required_key}")
                                    else:
                                        adventurer.room = destination_room
                                        save_game()
#room move confirmation - debug
#                                        print(f"Moved to: {rooms[destination_room].name}")
#                                    else:
#                                        print("No room there")
       
        room_title = font.render(f"Room: {current_room.name.upper()}", True, white)
        screen.blit(room_title, (100, 50))
       
        player_info = smolfont.render(f"Adventurer: {adventurer.name} | Room ID: {current_room_id}", True, grey)
        screen.blit(player_info, (100, 110))

        show_movement = True

        if current_room_id == 1 and not adventurer.has_chosen_weapon:
            show_movement = False

        if current_enemy:
            show_movement = False

        if current_room_id == 4 and not puzzle_solved:
            show_movement = False

        if current_room_id == 8 and not puzzle_solved2:
            show_movement = False

        if show_movement:
            for direction_index, button_data in buttons.items():
                path_exists = current_room.doors[direction_index] != 0
           
                button_color = grey if path_exists else darkgrey
                text_color = white if path_exists else grey

                pygame.draw.rect(screen, button_color, button_data["rect"])
       
                button_txt = smolfont.render(button_data["text"], True, text_color)
                txt_rect = button_txt.get_rect(center=button_data["rect"].center)
                screen.blit(button_txt, txt_rect)

        pygame.display.flip()
        clock.tick(30)

#state manager
state = "title"
while True:
    if state == "title":
        state = titlescreen()
    elif state == "intro":
        state = intro()
    elif state == "naming":
        state = naming()
    elif state == "login":
        state = login_screen()
    elif state == "load":
        if load_game():
            state = "main"
        else:
            state = "title" 
    elif state == "load":
        state = load_game()
    elif state == "main":
        state = main()
    elif state == "quit":
        break

pygame.quit()
sys.exit()