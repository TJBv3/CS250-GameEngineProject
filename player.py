# Player Class
#   Manages the powers and abilities of the player

__author__="rosbaldeston"
__date__ ="$Jan 9, 2012 10:14:59 AM$"

import attributes
import weapons
import attack

import pygame
pygame.display.set_mode([800,600])
# ----- image variables -----
playerUpImg = pygame.image.load("images/player-UP.png").convert()
playerDownImg = pygame.image.load("images/player-DOWN.png").convert()
playerLeftImg = pygame.image.load("images/player-LEFT.png").convert()
playerRightImg = pygame.image.load("images/player-RIGHT.png").convert()
enemyUpImg = pygame.image.load("images/enemy-UP.png").convert()
enemyDownImg = pygame.image.load("images/enemy-DOWN.png").convert()
enemyLeftImg = pygame.image.load("images/enemy-LEFT.png").convert()
enemyRightImg = pygame.image.load("images/enemy-RIGHT.png").convert()
playerUpImg.set_colorkey((255,255,255))
playerDownImg.set_colorkey((255,255,255))
playerLeftImg.set_colorkey((255,255,255))
playerRightImg.set_colorkey((255,255,255))
enemyUpImg.set_colorkey((255,255,255))
enemyDownImg.set_colorkey((255,255,255))
enemyLeftImg.set_colorkey((255,255,255))
enemyRightImg.set_colorkey((255,255,255))


class Player(pygame.sprite.Sprite):
	# Class controls the player information
    def __init__(self, startingClass, type, width, height):
        self.player = attributes.Attributes(startingClass)
        pygame.sprite.Sprite.__init__(self)
        self.type = startingClass
        if startingClass == "Wanderer":
            self.image = playerDownImg
        elif startingClass == "Wytch":
            self.image = enemyDownImg
        self.rect = self.image.get_rect()
        
        # Initialize player weapons
        self.weapons = weapons.Weapon()
        
    def update(self, direction, speed):
        if direction == "UP":
            if self.type == "Wanderer":
                self.image = playerUpImg
            if self.type == "Wytch":
                self.image = enemyUpImg
            self.rect.y -= speed
        if direction == "DOWN":
            if self.type == "Wanderer":
                self.image = playerDownImg
            if self.type == "Wytch":
                self.image = enemyDownImg
            self.rect.y += speed
        if direction == "LEFT":
            if self.type == "Wanderer":
                self.image = playerLeftImg
            if self.type == "Wytch":
                self.image = enemyLeftImg
            self.rect.x -= speed
        if direction == "RIGHT":
            if self.type == "Wanderer":
                self.image = playerRightImg
            if self.type == "Wytch":
                self.image = enemyRightImg
            self.rect.x += speed
        
		
	def skills(self):
		return self.player.skills.activated()

	def powers(self):
		return self.player.powers.activated()
		
	def handleAttack(self, target, attack):
		target.computeDamageTaken(self.player, attack) # Get damage return for skill/power leveling (to be added)
		if target.HP == 0:
			self.player.points = self.player.points + self.player.addXP(target.level)
			# points can be used for leveling up
			target.dead()
	
	def computeDamageTaken(self, enemy, attack):
		if attack.Type == "Active Spell":
			damage = enemy.getBasePowerDamage()*attack.modVal - self.player.getBaseDefenseVsMagic()
		elif attack.Type != "Passive Spell":
			if attack.modStat == "dex":
				if defending:
					damage = enemy.getBaseDexSkillDamage()*attack.modVal - self.player.getBaseDefenseVsPhysical()*self.shield.modVal
					# Modify Shield level here (to be added)
				else:
					damage = enemy.getBaseDexSkillDamage()*attack.modVal - self.player.getBaseDefenseVsPhysical()
			else:
				if defending:
					damage = enemy.getBaseStrSkillDamage()*attack.modVal - self.player.getBaseDefenseVsPhysical()*self.shield.modVal
					# Modify Shield level here (to be added)
				else:
					damage = enemy.getBaseStrSkillDamage()*attack.modVal - self.player.getBaseDefenseVsPhysical()
		if damage < 1:
			damage = 1
		if self.player.HP - damage < 1:
			self.player.HP = 0
		else:
			self.player.HP = self.player.HP - damage
		return damage

	def dead(self):
		None

	def getDefenseRating(self, against):
		return (self.defense / (self.defense + against))
	
	def printClassStats(self):
		print "\n\nYou have chosen to be a " + startingClass + "!"
		print "Hit Points: ", User.player.getHP()
		print "Stamina Points: ", User.player.getStamina()
		print "Vitavis Points: ", User.player.getVP()
		print "Madness Points: ", User.player.getMP()
		print "Base Power Damage: ", User.player.getBasePowerDamage()
		print "Base Dex Damage: ", User.player.getBaseDexSkillDamage()
		print "Base Str Damage: ", User.player.getBaseStrSkillDamage()
		print "Def Vs Physical: ", User.player.getBaseDefenseVsPhysical()
		print "Def Vs Magic: ", User.player.getBaseDefenseVsMagic()
		print "Dodge Likelihood: ", User.player.getDodgeLikelihood()
		print "Critical Hit Chance: ", User.player.getCriticalHitChance()

	def subPrimeDefinitions(self):
		print "\n\nA sub-prime is a secondary skill or power in which your class is also proficient."
		print "You may choose two sup-primes from the lists below"
		print "Skills: [Archery, One-Handed, Shield, Staff, Two-Handed, Unarmed]"
		print "Powers: [Blink, Fire, Hydras, Light, Manipulation, Mend, Sense, Shift, Sight, Step, Strength, Terra]"
		subPrimeOne = raw_input("What would you like your first sub-prime to be? ")
		subPrimeTwo = raw_input("What would you like your second sub-prime to be? ")
		self.player.createSubPrimes(subPrimeOne, subPrimeTwo)

	def spendInitialPerks(self):
		print "\n\nYou may start with three perks. \nThese perks can be spent and any of the 18 ability trees."
		print "Though it is suggested that they are used in the primary trees associated with your"
		print "chosen class or one of the two sub primes."

if __name__ == "__main__":
	print "Welcome!"
	print "You may choose from the following list of classes for your starting class."
	print "[Wytch, Thief, Warrior, Mage, Descendent, Assassin, Healer, Seer, Ranger, Wanderer]"
	startingClass = raw_input("What Class would you like to be? ")
	User = Player(startingClass)
	User.printClassStats()
	User.subPrimeDefinitions()
