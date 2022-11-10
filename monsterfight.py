from operator import attrgetter
from random import randint
from collections import deque

# TODO: More play testing to balance enemies better

class Dice:

  def d2(): return randint(1, 2)
  def d4(): return randint(1, 4)
  def d6(): return randint(1, 6)
  def d8(): return randint(1, 8)
  def d10(): return randint(1, 10)
  def d12(): return randint(1, 12)
  def d20(): return randint(1, 20)

dice = {
  'd2': Dice.d2,
  'd4': Dice.d4,
  'd6': Dice.d6,
  'd8': Dice.d8,
  'd10': Dice.d10,
  'd12': Dice.d12,
  'd20': Dice.d20,
}


class Hero:

  def __init__(self, name: str, armor_class: int=16, attack_bonus: int=2, level: int=1) -> None:
    self.name = name
    self.level = level
    self.health = (level * 8) + 10
    self.max_health = self.health
    self.armor = armor_class
    self.attack_bonus = attack_bonus
    self.xp = (level * 20) - 20
    self.initiative = 0

  def level_up(self) -> None:
    self.level += 1
    self.max_health = self.max_health + 8
    self.health = self.max_health
    if (self.level % 5 == 0):
      self.armor += 1
      self.attack_bonus += 1
    print(f"You have reached level {self.level} and now have {self.health} health. Your armor class is {self.armor}. Your attack bonus is {self.attack_bonus}.")

  def damage(self, value) -> None:
    print(f"You take {value} damage.")
    self.health -= value

  def heal(self, value) -> None:
    self.health += value
    print(f"You heal {value} points of health. Your current health is {self.health} / {self.max_health}.")

  def max_heal(self) -> None:
    print("\nYou rest for a time and heal your wounds...")
    self.heal(self.max_health - self.health)

  def heal_self(self) -> None:
    heal_amount = 0
    for _ in range(self.level):
      heal_amount += Dice.d4()
    if self.health + heal_amount > self.max_health: self.heal(self.max_health - self.health)
    else: self.heal(heal_amount)

  def attack(self, opponent_ac):
    if attack(self.attack_bonus, opponent_ac=opponent_ac):
      print("You hit your target dealing damage!")
      return roll_damage('d6', 2, 3)
    print("Your sword misses its mark!")
    return 0


class Monster:

  def __init__(self, level: int, max_health: int, monster_type: str) -> None:
    self.level = level
    self.max_health = max_health
    self.health = max_health
    self.monster_type = monster_type
    self.initiative = 0

  def __repr__(self) -> str:
    return f"A {self.monster_type} (level {self.level}) that has {self.health} hit points out of {self.max_health} hit points."

  def damage(self, value):
    print(f"The {self.monster_type} (level {self.level}) takes {value} points of damage!")
    self.health -= value

  def heal(self, value):
    print(f"The {self.monster_type} (level {self.level}) heals for {value}!")
    self.health += value

  # Method intended to be overridden by subclasses
  def heal_self(self):
    pass


class Dragon(Monster):

  def __init__(self, level) -> None:
    self.level = level + randint(0, 5)
    health = (self.level * 8) + 80
    self.armor = 16
    self.fire_breath_uses = 3
    self.xp = 20
    super().__init__(level=self.level, max_health=health, monster_type="Dragon")

  def __repr__(self) -> str:
    return super().__repr__()

  def attack(self, opponent_ac):
    if Dice.d10() > 7 and self.fire_breath_uses > 0:
      dmg = self.fire_breath(opponent_ac=opponent_ac)
      if dmg: print(f"\nDragon blasts you with fire breath for {dmg} damage!")
      else: print("\nDragon sputters and blows smoke at you but no damage is done. Your eyes water a bit.")
      return dmg
    else:
      dmg = self.bite(opponent_ac=opponent_ac)
      if dmg: print(f"\nDragon bites you for {dmg} damage!")
      else: print("\nDragon snaps at you but misses.")
      return dmg

  def fire_breath(self, opponent_ac):
    self.fire_breath_uses -= 1
    if attack(8, opponent_ac=opponent_ac):
      return roll_damage('d6', 7)
    return 0

  def bite(self, opponent_ac):
    if attack(6, opponent_ac=opponent_ac):
      return roll_damage('d10', 1, 7)
    return 0

  def heal_self(self):
    heal_amount = 0
    for _ in range(self.level):
      heal_amount += Dice.d4()
    if self.health + heal_amount > self.max_health: self.heal(self.max_health - self.health)
    else: self.heal(heal_amount)


class Wolf(Monster):

  def __init__(self, level) -> None:
    self.level = level + randint(-2, 2) if level > 2 else level
    health = (self.level * 2) + 8
    self.armor = 8
    self.xp = 5
    super().__init__(level=self.level, max_health=health, monster_type="Wolf")

  def __repr__(self) -> str:
    return super().__repr__()

  def bite(self, opponent_ac):
    if attack(4, opponent_ac=opponent_ac):
      return roll_damage('d4', 1, 2)
    return 0

  def attack(self, opponent_ac):
    dmg = self.bite(opponent_ac=opponent_ac)
    if dmg: print(f"\nWolf bites you for {dmg} damage.")
    else: print("\nWolf lunges at you trying to bite but misses.")
    return dmg

  def heal_self(self):
    heal_amount = self.level // 2
    if self.health + heal_amount > self.max_health: self.heal(self.max_health - self.health)
    else: self.heal(heal_amount)


class Bandit(Monster):

  def __init__(self, level) -> None:
    self.level = level + randint(-2, 5)
    health = (self.level * 4) + 8
    self.armor = 12
    self.xp = 10
    super().__init__(level=self.level, max_health=health, monster_type="Bandit")

  def __repr__(self) -> str:
    return super().__repr__()

  def sword(self, opponent_ac):
    if attack(3, opponent_ac=opponent_ac):
      return roll_damage('d6', 1, 2)
    return 0

  def crossbow(self, opponent_ac):
    if attack(3, opponent_ac=opponent_ac):
      return roll_damage('d8', 1, 2)
    return 0

  def attack(self, opponent_ac):
    if Dice.d10() > 6:
      dmg = self.crossbow(opponent_ac=opponent_ac)
      if dmg: print(f"\nBandit shoots you with his crossbow for {dmg} damage. You have a bolt sticking out of you.")
      else: print("\nBandit shoots at you with his crossbow but the bolt whistles by.")
      return dmg
    else:
      dmg = self.sword(opponent_ac=opponent_ac)
      if dmg: print(f"\nBandit strikes you with his sword and hits you for {dmg} damage.")
      else: print("\nBandit swings his sword at you but misses.")
      return dmg

  def heal_self(self):
    heal_amount = 0
    for _ in range(self.level):
      heal_amount += Dice.d2()
    if self.health + heal_amount > self.max_health: self.heal(self.max_health - self.health)
    else: self.heal(heal_amount)


def generate_monsters(hero_level: int) -> list:
  monsters = []

  if hero_level < 5:
    if Dice.d20() > 18:
      monsters.append(Wolf(hero_level))
    monsters.append(Wolf(hero_level))

  elif hero_level >= 5 and hero_level < 10:
    die_roll = Dice.d20()
    if die_roll <= 5:
      monsters.append(Wolf(hero_level))
    elif die_roll > 5 and die_roll <= 15:
      monsters.append(Wolf(hero_level))
      monsters.append(Wolf(hero_level))
    elif die_roll > 15 and die_roll <= 19:
      monsters.append(Bandit(hero_level))
    elif die_roll == 20:
      monsters.append(Wolf(hero_level))
      monsters.append(Bandit(hero_level))

  elif hero_level >= 10 and hero_level < 15:
    die_roll = Dice.d20()
    if die_roll == 1:
      monsters.append(Wolf(hero_level))
    elif die_roll > 1 and die_roll <= 5:
      monsters.append(Wolf(hero_level))
      monsters.append(Wolf(hero_level))
    elif die_roll > 5 and die_roll <= 10:
      monsters.append(Bandit(hero_level))
    elif die_roll > 10 and die_roll <= 15:
      monsters.append(Bandit(hero_level))
      monsters.append(Wolf(hero_level))
    elif die_roll > 15 and die_roll <= 19:
      monsters.append(Bandit(hero_level))
      monsters.append(Wolf(hero_level))
      monsters.append(Wolf(hero_level))
    elif die_roll == 20:
      monsters.append(Dragon(hero_level))

  elif hero_level >= 15:
    die_roll = Dice.d20()
    if die_roll <= 5:
      monsters.append(Bandit(hero_level))
    elif die_roll > 5 and die_roll <= 15:
      monsters.append(Bandit(hero_level))
      monsters.append(Wolf(hero_level))
      monsters.append(Wolf(hero_level))
    else:
      monsters.append(Dragon(hero_level))

  return monsters

def attack(attack_bonus, opponent_ac) -> bool:
  return (Dice.d20() + attack_bonus) > opponent_ac

def roll_damage(die_type, die_num, bonus=0) -> int:
  return (die_num * dice[die_type]()) + bonus

def investigate(monster: Monster) -> None:
  if Dice.d20() >= 14:
    print(f"\n{monster}")
  else:
    print(f"\nYour sense of {monster.monster_type} level {monster.level} is clouded at the moment...")

def sanitize_hero_level_input(player_input) -> int:
  if player_input == '':
    return 1
  try:
    hero_level = int(player_input)
  except ValueError:
    return None
  if hero_level < 1 or hero_level >= 20:
    return None
  return hero_level

actions = {
  'a': 'attack',
  'atk': 'attack',
  'attack': 'attack',
  'h': 'heal',
  'heal': 'heal',
  'i': 'investigate',
  'inv': 'investigate',
  'q': 'quit',
  'quit': 'quit',
  'help': 'help'
  }
def sanitize_player_input(player_input) -> str:
  if player_input not in actions:
    return None
  return actions[player_input]

def sanitize_attack_choice(player_input) -> int:
  try:
    attack_choice = int(player_input)
  except ValueError:
    return None
  return attack_choice


# Main game
if __name__ == "__main__":
  # Input name and level (default=1)
  print("Fight the monsters and gain glory!")
  hero_name = input("What is your hero's name?\n").strip()
  hero_level = sanitize_hero_level_input(input("Input level you wish to start at or leave blank to start at 1:\n"))
  while not hero_level:
    hero_level = sanitize_hero_level_input(input("That is not an available level. Please enter a number between 1 and 19:\n"))
  hero = Hero(name=hero_name, level=hero_level if hero_level else 1)
  quit_flag = False
  monsters_killed = 0
  dragons_killed = 0

  print(f"You are a mighty-sword-wielding hero named {hero.name}! You have taken on the task of slaying monsters across the realm.")
  print("Starting stats:")
  print(f"\tLevel: {hero.level}")
  print(f"\tMax health: {hero.max_health}")
  print(f"\tArmor class: {hero.armor}")
  print(f"\tAttack bonus: {hero.attack_bonus}")

  # Game loop
  while hero.health > 0 and hero.level <= 20 and not quit_flag:
    print("\nAnother battle is ahead!")
    # Generate monster(s)
    monsters = generate_monsters(hero.level)
    print(f"Prepare to fight! You are faced by {'an enemy' if len(monsters) == 1 else 'enemies'}!")
    print(('\n').join([str(m) for m in monsters]))

    # Determine turn order
    hero.initiative = Dice.d20()
    turn_order = [hero]
    for monster in monsters:
      monster.initiative = Dice.d20()
      turn_order.append(monster)
    sorted(turn_order, key=attrgetter('initiative'))
    turn_order = deque(turn_order)

    # Fight loop
    while len(turn_order) > 1:
      # Action
      current_fighter = turn_order[-1]

      # Hero turn
      if type(current_fighter) == Hero:
        player_choice = sanitize_player_input(input("Quick! Make a decision! What do you do? (Type 'help' for help)\n"))
        while not player_choice:
          player_choice = sanitize_player_input(input("That is not an action you can take here. What do you do? (Type 'help' for help)\n"))
          if player_choice == 'help':
            print("You can use any of the following for actions\n" + (', ').join(actions.keys()))
            player_choice = None

        if player_choice == 'quit':
          quit_flag = True
          break

        elif player_choice == 'attack':
          attackers = [m for m in turn_order if type(m) != Hero]
          sorted(attackers, key=attrgetter('health'))
          if len(attackers) < 2:
            target = attackers[0]
          else:
            print("Which monster do you attack?")
            for i, monster in enumerate(attackers):
              print(f"{i+1} - {monster.monster_type} (level {monster.level})")
            attack_choice = sanitize_attack_choice(input("Number for desired choice: "))
            while not attack_choice or attack_choice not in range(1, len(attackers)+1):
              attack_choice = sanitize_attack_choice(input("That is not a number for one of the monsters. Please try again: "))
            target = attackers[attack_choice - 1]
          print(f"\nYou swing your mighty sword at the {target.monster_type} (level {target.level})!")
          target.damage(hero.attack(target.armor))

        elif player_choice == 'heal':
          hero.heal_self()

        elif player_choice == 'investigate':
          for monster in [m for m in turn_order if type(m) != Hero]:
            investigate(monster)

      # Monster turn
      else:
        die_roll = Dice.d20()
        if die_roll == 20:
          current_fighter.heal_self()
        else:
          dmg = current_fighter.attack(hero.armor)
          hero.damage(dmg)
      for monster in monsters:
        if monster.health <= 0 and monster in turn_order:
          print(f"\n{monster.monster_type} (level {monster.level}) was felled by your sword!")
          turn_order.remove(monster)
      if hero.health <= 0: 
        print(f"\n***** You have fallen in battle! *****")
        break
      turn_order.rotate(1)

    # Post battle clean up
    if hero.health <= 0: break
    rest_input = input(f"Do you wish to pause and rest after the previous battle? (Health: {hero.health} / {hero.max_health})\t y/n:").lower()
    while rest_input not in ['y', 'yes', 'n', 'no']:
      rest_input = input("That is not a valid response. Do you wish to rest? y/n: ").lower()
    hero.max_heal()
    if quit_flag: break

    # Level up
    for monster in monsters:
      hero.xp += monster.xp
      monsters_killed += 1
      if type(monster) == Dragon:
        dragons_killed += 1
    monsters = []
    if hero.xp // 20 > hero.level:
      for level in range((hero.xp // 20) - hero.level):
        hero.level_up()
    print("==============================")
  # End game
  print("******************************")
  if hero.health <= 0:
    print("Game Over: You were unable to defeat the monsters and succumbed to their attacks. Perhaps next time...")
  if quit_flag:
    print("Goodbye. The monsters await you next time.")
  if hero.level >= 20:
    print("Congratulations! You have conquered these monsters and have decided to travel abroad in search of more adventure!")
  
  print("Stats:")
  print(f"\tLevel: {hero.level}")
  print(f"\tMonsters defeated: {monsters_killed}")
  print(f"\tDragons killed: {dragons_killed}")
