'''
AUTHOR: Antoine LUCIEN
NAME: Monster vs Boy
S.N: 904255
DATE: 17/12/2022
COURSES : SCRIPTING LANGUAGES
REFERENCES : http://www.pygame.org/docs
'''

# IMPORTS
import pygame
import sys

pygame.init()
clock = pygame.time.Clock()

# WINDOWS
size = (700, 500)
screen = pygame.display.set_mode(size)
win = screen.get_rect()
pygame.display.set_caption('Monster vs Boy')

# VARIABLES GLOBALES
BACKGROUND = pygame.image.load('background.jpg')
BACKGROUND2 = pygame.image.load('background2.png')
BLACK = (0, 0, 0)

left_position = 0
right_position = 600

controls = {pygame.K_a: "a", pygame.K_z: "z",
            pygame.K_e: "e", pygame.K_r: "r", pygame.K_t: "t"}

black = (0, 0, 0)
myfont = pygame.font.Font('freesansbold.ttf', 48)

# PERSONAGES
size_char = (100, 100)
monster1 = {"file": "monster.png"}
monster2 = {"file": "monster.png"}
monster3 = {"file": "monster.png"}
boy1 = {"file": "boy.png"}
boy2 = {"file": "boy.png"}
boy3 = {"file": "boy.png"}
boat = {"file": "boat.png"}

actors = [monster1, monster2, monster3, boy1, boy2, boy3, boat]

passengers = {"a": [monster1, boat],
              "z": [monster1, monster2, boat],
              "e": [monster1, boy1, boat],
              "r": [boy1, boy2, boat],
              "t": [boy1, boat]}


def getkey():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                sys.exit()
            if event.key in controls:
                key = controls[event.key]
                return key


def ferry(who, step):
    done = False
    for actor in who:
        actor["rect"] = actor["rect"].move((step, 0))
        if not win.contains(actor["rect"]):
            actor["rect"] = actor["rect"].move((-step, 0))
            actor["surf"] = pygame.transform.flip(actor["surf"], True, False)
            done = True
    return done


def failure():
    red = (255, 0, 0)
    myfont = pygame.font.Font('freesansbold.ttf', 48)
    msg = myfont.render("Failure", True, red)
    msg_box = msg.get_rect()
    msg_box.center = win.center
    screen.blit(msg, msg_box)
    pygame.display.flip()
    pygame.time.wait(1000)
    menu()


def success():
    green = (0, 170, 0)
    myfont = pygame.font.Font('freesansbold.ttf', 48)
    msg = myfont.render("Success", True, green)
    msg_box = msg.get_rect()
    msg_box.center = win.center
    screen.blit(msg, msg_box)
    pygame.display.flip()
    pygame.time.wait(1000)
    menu()


def menu():
    while True:
        # Background
        screen.blit(BACKGROUND2, win.topleft)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game()
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()
        clock.tick(120)


def game():

    for i, actor in enumerate(actors):
        actor["surf"] = pygame.image.load(actor["file"])
        actor["surf"] = pygame.transform.scale(actor["surf"], size_char)
        actor["rect"] = actor["surf"].get_rect()
        actor["rect"].midleft = (0, (i+1)*win.height/8)

    gamegraph = {
        "cccmmmb-": {"a": "ccmmm-cb", "z": "cmmm-ccb", "e": "ccmm-cmb",
                     "r": "cccm-mmb", "t": "cccmm-mb"},
        "ccmmm-cb": {"a": "cccmmmb-"},
        "cmmm-ccb": {"a": "ccmmmb-c", "z": "cccmmmb-"},
        "ccmm-cmb": {"a": "cccmmb-m", "e": "cccmmmb-", "t": "ccmmmb-c"},
        "ccmmmb-c": {"a": "cmmm-ccb", "z": "mmm-cccb", "e": "cmm-ccmb",
                     "r": "ccm-cmmb", "t": "ccmm-cmb"},
        "mmm-cccb": {"a": "cmmmb-cc", "z": "ccmmmb-c"},
        "cmmmb-cc": {"a": "mmm-cccb", "e": "mm-cccmb", "r": "cm-ccmmb",
                     "t": "cmm-ccmb"},
        "cm-ccmmb": {"a": "ccmb-cmm", "z": "cccmb-mm", "e": "ccmmb-cm",
                     "r": "cmmmb-cc", "t": "cmmb-ccm"},
        "ccmmb-cm": {"a": "cmm-ccmb", "z": "mm-cccmb", "e": "cm-ccmmb",
                     "r": "cc-cmmmb", "t": "ccm-cmmb"},
        "cc-cmmmb": {"a": "cccb-mmm", "e": "cccmb-mm", "r": "ccmmb-cm",
                     "t": "ccmb-cmm"},
        "cccb-mmm": {"a": "cc-cmmmb", "z": "c-ccmmmb"},
        "c-ccmmmb": {"a": "ccb-cmmm", "z": "cccb-mmm", "e": "ccmb-cmm",
                     "r": "cmmb-ccm", "t": "cmb-ccmm"},
        "ccb-cmmm": {"a": "c-ccmmmb", "z": "-cccmmmb"},
        "cmb-ccmm": {"a": "m-cccmmb", "e": "-cccmmmb", "m": "c-ccmmmb"},
        "cccmmb-m": "failure",
        "cccmm-mb": "failure",
        "cccmb-mm": "failure",
        "cccm-mmb": "failure",
        "ccmb-cmm": "failure",
        "ccm-cmmb": "failure",
        "cmmb-ccm": "failure",
        "cmm-ccmb": "failure",
        "mmb-cccm": "failure",
        "mm-cccmb": "failure",
        "mb-cccmm": "failure",
        "m-cccmmb": "failure",
        "-cccmmmb": "success"}

    gamestate = "cccmmmb-"

    action = "listen"

    ferry_step = -5

    cmpt = 0

    while True:
        msg = myfont.render(str(cmpt), True, black)
        msg_box = msg.get_rect()
        msg_box.center = (win.midtop[0], 30)
        if action == "listen":

            # CHECK GAME STATUS AND BOAT POSITION
            gamecount = gamestate.split("-")
            left = "c", gamecount[0].count("c"), "m",\
                   gamecount[0].count("m"), "b", gamecount[0].count("b")
            right = "c", gamecount[1].count("c"), "m",\
                    gamecount[1].count("m"), "b", gamecount[1].count("b")
            print(left)
            print(right)

            # FOR BOAT IN LEFT SIDE
            if left[5] == 1:

                # CHECK PERSONAGES POSITION
                pos_mon1 = monster1.get("rect")
                pos_mon2 = monster2.get("rect")
                pos_mon3 = monster3.get("rect")
                pos_boy1 = boy1.get("rect")
                pos_boy2 = boy2.get("rect")
                pos_boy3 = boy3.get("rect")

                # FIND BEST COMBINATION FOR 2 MONSTER
                if pos_mon2[0] == left_position:
                    if pos_mon3[0] == left_position:
                        passengers.update({"z": [monster2, monster3, boat]})
                if pos_mon1[0] == left_position:
                    if pos_mon3[0] == left_position:
                        passengers.update({"z": [monster1, monster3, boat]})
                if pos_mon1[0] == 0:
                    if pos_mon2[0] == left_position:
                        passengers.update({"z": [monster1, monster2, boat]})

                # FIND BEST COMBINATION FOR 2 BOYS
                if pos_boy2[0] == left_position:
                    if pos_boy3[0] == left_position:
                        passengers.update({"r": [boy2, boy3, boat]})
                if pos_boy1[0] == left_position:
                    if pos_boy3[0] == left_position:
                        passengers.update({"r": [boy1, boy3, boat]})
                if pos_boy1[0] == left_position:
                    if pos_boy2[0] == left_position:
                        passengers.update({"r": [boy1, boy2, boat]})

                # FIND BEST COMBINATION FOR 1 MONSTER AND 1 BOY
                if pos_boy1[0] == left_position:
                    if pos_mon1[0] == left_position:
                        passengers.update({"e": [boy1, monster1, boat]})
                if pos_boy2[0] == left_position:
                    if pos_mon2[0] == left_position:
                        passengers.update({"e": [boy2, monster2, boat]})
                if pos_boy3[0] == left_position:
                    if pos_mon3[0] == left_position:
                        passengers.update({"e": [boy3, monster3, boat]})
                if pos_boy1[0] == left_position:
                    if pos_mon2[0] == left_position:
                        passengers.update({"e": [boy1, monster2, boat]})
                if pos_boy2[0] == left_position:
                    if pos_mon3[0] == left_position:
                        passengers.update({"e": [boy2, monster3, boat]})
                if pos_boy3[0] == left_position:
                    if pos_mon1[0] == left_position:
                        passengers.update({"e": [boy3, monster1, boat]})
                if pos_boy1[0] == left_position:
                    if pos_mon3[0] == left_position:
                        passengers.update({"e": [boy1, monster3, boat]})
                if pos_boy2[0] == left_position:
                    if pos_mon1[0] == left_position:
                        passengers.update({"e": [boy2, monster1, boat]})
                if pos_boy3[0] == left_position:
                    if pos_mon2[0] == left_position:
                        passengers.update({"e": [boy3, monster2, boat]})

                # FIND BEST COMBINATION FOR 1 MONSTER
                if pos_mon3[0] == left_position:
                    passengers.update({"a": [monster3, boat]})
                if pos_mon2[0] == left_position:
                    passengers.update({"a": [monster2, boat]})
                if pos_mon1[0] == left_position:
                    passengers.update({"a": [monster1, boat]})

                # FIND BEST COMBINATION FOR 1 BOY
                if pos_boy3[0] == left_position:
                    passengers.update({"t": [boy3, boat]})
                if pos_boy2[0] == left_position:
                    passengers.update({"t": [boy2, boat]})
                if pos_boy1[0] == left_position:
                    passengers.update({"t": [boy1, boat]})

            # FOR BOAT IN RIGHT SIDE
            if right[5] == 1:

                # CHECK PERSONAGES POSITION
                pos_mon1 = monster1.get("rect")
                pos_mon2 = monster2.get("rect")
                pos_mon3 = monster3.get("rect")
                pos_boy1 = boy1.get("rect")
                pos_boy2 = boy2.get("rect")
                pos_boy3 = boy3.get("rect")

                # FIND BEST COMBINATION FOR 2 MONSTER
                if pos_mon2[0] == right_position:
                    if pos_mon3[0] == right_position:
                        passengers.update({"z": [monster2, monster3, boat]})
                if pos_mon1[0] == right_position:
                    if pos_mon3[0] == right_position:
                        passengers.update({"z": [monster1, monster3, boat]})
                if pos_mon1[0] == right_position:
                    if pos_mon2[0] == right_position:
                        passengers.update({"z": [monster1, monster2, boat]})

                # FIND BEST COMBINATION FOR 2 BOYS
                if pos_boy2[0] == right_position:
                    if pos_boy3[0] == right_position:
                        passengers.update({"r": [boy2, boy3, boat]})
                if pos_boy1[0] == right_position:
                    if pos_boy3[0] == right_position:
                        passengers.update({"r": [boy1, boy3, boat]})
                if pos_boy1[0] == right_position:
                    if pos_boy2[0] == right_position:
                        passengers.update({"r": [boy1, boy2, boat]})

                # FIND BEST COMBINATION FOR 1 MONSTER AND 1 BOY
                if pos_boy1[0] == right_position:
                    if pos_mon1[0] == right_position:
                        passengers.update({"e": [boy1, monster1, boat]})
                if pos_boy2[0] == right_position:
                    if pos_mon2[0] == right_position:
                        passengers.update({"e": [boy2, monster2, boat]})
                if pos_boy3[0] == right_position:
                    if pos_mon3[0] == right_position:
                        passengers.update({"e": [boy3, monster3, boat]})
                if pos_boy1[0] == right_position:
                    if pos_mon2[0] == right_position:
                        passengers.update({"e": [boy1, monster2, boat]})
                if pos_boy2[0] == right_position:
                    if pos_mon3[0] == right_position:
                        passengers.update({"e": [boy2, monster3, boat]})
                if pos_boy3[0] == right_position:
                    if pos_mon1[0] == right_position:
                        passengers.update({"e": [boy3, monster1, boat]})
                if pos_boy1[0] == right_position:
                    if pos_mon3[0] == right_position:
                        passengers.update({"e": [boy1, monster3, boat]})
                if pos_boy2[0] == right_position:
                    if pos_mon1[0] == right_position:
                        passengers.update({"e": [boy2, monster1, boat]})
                if pos_boy3[0] == right_position:
                    if pos_mon2[0] == right_position:
                        passengers.update({"e": [boy3, monster2, boat]})

                # FIND BEST COMBINATION FOR 1 MONSTER
                if pos_mon3[0] == right_position:
                    passengers.update({"a": [monster3, boat]})
                if pos_mon2[0] == right_position:
                    passengers.update({"a": [monster2, boat]})
                if pos_mon1[0] == right_position:
                    passengers.update({"a": [monster1, boat]})

                # FIND BEST COMBINATION FOR 1 BOY
                if pos_boy3[0] == right_position:
                    passengers.update({"t": [boy3, boat]})
                if pos_boy2[0] == right_position:
                    passengers.update({"t": [boy2, boat]})
                if pos_boy1[0] == right_position:
                    passengers.update({"t": [boy1, boat]})

            key = getkey()
            print(cmpt)
            if key in gamegraph[gamestate]:
                gamestate = gamegraph[gamestate][key]
                ferry_who = passengers[key]
                ferry_step = -ferry_step
                action = "ferry"

        if action == "ferry":
            done = ferry(ferry_who, ferry_step)
            if done:
                if gamegraph[gamestate] == "failure":
                    action = "failure"
                elif gamegraph[gamestate] == "success":
                    action = "success"
                else:
                    cmpt += 1
                    action = "listen"

        if action == "failure":
            failure()
            sys.exit()

        if action == "success":
            success()
            sys.exit()

        # Background
        screen.blit(BACKGROUND, win.topleft)

        # Display
        for actor in actors:
            screen.blit(actor["surf"], actor["rect"])
        screen.blit(msg, msg_box)
        pygame.display.flip()
        clock.tick(120)


if __name__ == "__main__":
    menu()
    game()
