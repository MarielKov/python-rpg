import sys
import os
import random
import pickle
import pygame
import math
from pygame import *

# Inicializar Pygame
pygame.init()

# Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e Icono
pygame.display.set_caption("Juego RPG")
icono = pygame.image.load("espadas.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("fondo2.png")
img_jugador = pygame.image.load("ariety.png")

se_ejecuta = True
while se_ejecuta:

    # image de fondo
    pantalla.blit(fondo, (0, 0))

    # iterar eventos
    for evento in pygame.event.get():

        # evento cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False

pantalla.blit(img_jugador, (0,0))
pygame.display.update()



armasMelee= {"Katana Plateada": 30, "Katana de Sangre": 40}
armasMagicas = {"Vara de Principiante": 20, "Vara Potenciadora" : 25}
armasMecanicas = {"Cañon Basico": 20, "Pistola de Metralla":30}

class guerrero:
    def __init__(self):
        self.name = ""
        self.maxhealth = 100
        self.health = self.maxhealth
        self.base_attack = 10
        self.gold = 0
        self.pots = 0
        self.weap = ["Katana Plateada"]
        self.curweap = ["Katana Plateada"]

    @property
    def attack(self):
        attack = self.base_attack
        if self.curweap == "Katana Plateada":
            attack += 7

        if self.curweap == "Katana de Sangre":
            attack += 15

        return attack


class mago:
    def __init__(self):
        self.name = ""
        self.maxhealth = 60
        self.health = self.maxhealth
        self.base_attack = 4
        self.gold = 0
        self.pots = 0
        self.weap = ["Vara de Principiante"]
        self.curweap = ["Vara de Principiante"]

    @property
    def attack(self):
        attack = self.base_attack
        if self.curweap == "Vara de Principiante":
            attack += 3

        if self.curweap == "Vara Potenciadora":
            attack += 9

        return attack

class maquina:
    def __init__(self):
        self.name = "Ariety"
        self.maxhealth = 60
        self.health = self.maxhealth
        self.base_attack = 4
        self.gold = 0
        self.pots = 0
        self.weap = ["Cañon Basico"]
        self.curweap = ["Cañon Basico"]
        self.img_jugador = pygame.image.load("ariety.png")


    @property
    def attack(self):
        attack = self.base_attack
        if self.curweap == "Cañon Basico":
            attack += 5

        if self.curweap == "Pistola de Metralla":
            attack += 11

        return attack

class Goblin:
    def __init__(self, name):
        self.name = name
        self.maxhealth = 50
        self.health = self.maxhealth
        self.attack = 5
        self.goldgain = 10
GoblinIG = Goblin("Goblin")

class Zombie:
    def __init__(self, name):
        self.name = name
        self.maxhealth = 70
        self.health = self.maxhealth
        self.attack = 7
        self.goldgain = 15
ZombieIG = Zombie("Zombie")

def main():



    print ("Welcome to my game!\n")
    print ("1.) Start")
    print ("2.) Load")
    print ("3.) Exit")
    option = input("--> ")
    if option == "1":
       start1()
    elif option == "2":
        if os.path.exists("savefile") == True:

            with open('savefile', 'rb') as f:
                global PlayerIG
                PlayerIG = pickle.load(f)
            print ("Loaded Save State...")
            option = input(" ")
            start1()
        else:
            print ("You have no save file for this game.")
            option = input(" ")
            main()

    elif option == "3":
        sys.exit()
    else:
        main()



def start1():

    print ("Name: %s" % PlayerIG.name)
    print ("Attack: %i" % PlayerIG.attack)
    print ("Gold: %d" % PlayerIG.gold)
    print ("Current Weapons: %s" % PlayerIG.curweap)
    print ("Potions: %d" % PlayerIG.pots)
    print ("Health: %i/%i\n" % (PlayerIG.health, PlayerIG.maxhealth))
    print ("1.) Fight")
    print ("2.) Store")
    print ("3.) Save")
    print ("4.) Exit")
    print ("5.) Inventory")
    option = input("--> ")
    if option == "1":
        prefight()
    elif option == "2":
        store()
    elif option == "3":

        with open('savefile', 'wb') as f:
            pickle.dump(PlayerIG, f)
            print ("\nGame has been saved!\n")
        option = input(" ")
        start1()
    elif option == "4":
        sys.exit()
    elif option == "5":
        inventory()
    else:
        start1()

def inventory():

    print ("what do you want to do?")
    print ("1.) Equip Weapon")
    print ("b.) go back")
    option = input(">>> ")
    if option == "1":
        equip()
    elif option == 'b':
        start1()

def equip():

    print ("What do you want to equip?")
    for weapon in PlayerIG.weap:
        print (weapon)
    print ("b to go back")
    option = input(">>> ")
    if option == PlayerIG.curweap:
        print ("You already have that weapon equipped")
        option = input(" ")
        equip()
    elif option == "b":
        inventory()
    elif option in PlayerIG.weap:
        PlayerIG.curweap = option
        print ("You have equipped %s." % option)
        option = input(" ")
        equip()
    else:
        print ("You don't have %s in your inventory" % option)




def prefight():
    global enemy
    enemynum = random.randint(1, 2)
    if enemynum == 1:
        enemy = GoblinIG
    else:
        enemy = ZombieIG
    fight()

def fight():

    print ("%s     vs      %s" % (PlayerIG.name, enemy.name))
    print ("%s's Health: %d/%d    %s's Health: %i/%i" % (PlayerIG.name, PlayerIG.health, PlayerIG.maxhealth, enemy.name, enemy.health, enemy.maxhealth))
    print ("Potions %i\n" % PlayerIG.pots)
    print ("1.) Attack")
    print ("2.) Drink Potion")
    print ("3.) Run")
    option = input(" ")
    if option == "1":
        attack()
    elif option == "2":
        drinkpot()
    elif option == "3":
        run()
    else:
        fight()

def attack():

    PAttack = random.randint(PlayerIG.attack / 2, PlayerIG.attack)
    EAttack = random.randint(int(enemy.attack/2), enemy.attack)
    if PAttack == PlayerIG.attack / 2:
        print ("You miss!")
    else:
        enemy.health -= PAttack
        print ("You deal %i damage!" % PAttack)
    option = input(" ")
    if enemy.health <= 0:
        win()

    if EAttack == enemy.attack/2:
        print ("The enemy missed!")
    else:
        PlayerIG.health -= EAttack
        print ("The enemy deals %i damage!" % EAttack)
    option = input(" ")
    if PlayerIG.health <= 0:
        dead()
    else:
        fight()

def drinkpot():

    if PlayerIG.pots == 0:
        print ("You don't have any potions!")
    else:
        PlayerIG.health += 50
        if PlayerIG.health > PlayerIG.maxhealth:
            PlayerIG.health = PlayerIG.maxhealth
        print ("You drank a potion!")
    option = input(" ")
    fight()

def run():

    runnum = random.randint(1, 3)
    if runnum == 1:
        print ("You have successfully ran away!")
        option = input(" ")
        start1()
    else:
        print ("You failed to get away!")
        option = input(" ")

        EAttack = random.randint(int(enemy.attack/2), enemy.attack)
        if EAttack == enemy.attack/2:
            print ("The enemy missed!")
        else:
            PlayerIG.health -= EAttack
            print ("The enemy deals %i damage!" % EAttack)
        option = input(" ")
        if PlayerIG.health <= 0:
            dead()
        else:
            fight()

def win():

    enemy.health = enemy.maxhealth
    PlayerIG.gold += enemy.goldgain
    print ("You have defeated the %s" % enemy.name)
    print ("You found %i gold!" % enemy.goldgain)
    option = input(" ")
    start1()

def dead():

    print ("You have died")
    option = input(" ")

def store():

    print ("Welcome to the shop!")
    print ("\nWhat would you like to buy?\n")
    print ("1.) Great Sword")
    print ("back")
    print (" ")
    option = input(" ")

    if option in armasMelee:
        if PlayerIG.gold >= armasMelee[option]:

            PlayerIG.gold -= armasMelee[option]
            PlayerIG.weap.append(option)
            print ("You have bought %s" % option)
            option = input(" ")
            store()

        else:

            print ("You don't have enough gold")
            option = input(" ")
            store()

    elif option == "back":
        start1()

    else:

        print ("That item does not exist")
        option = input(" ")
        store()





main()