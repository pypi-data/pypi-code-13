from random import randint
'''
This is an easy copy/paste for creating dicts:
Table = {
    '': ,
    '': ,
    '': ,
    '': ,
    '': ,
    '': ,
    '': ,
    '':
}
'''

def random_choice(chances_dict):
	chances = chances_dict.values()
	strings = list(chances_dict.keys())
	return strings[random_choice_index(chances)]

def random_choice_index(chances):
	dice = randint(1, sum(chances))
	running_sum = 0
	choice = 0
	for w in chances:
		running_sum += w
		if dice <= running_sum:
			return choice
		choice += 1

raceTable101 = {
    'Human': 14,
    'Elf': 2,
    'Dwarf': 1,
    'Halfling': 1,
    'Half Elf': 1,
    'other races': 1
}

raceTable101a = {
    'Beastman': 3,
    'Reptileman': 2,
    'Orc': 1,
    'Half-Orc': 4
}

cultureTable102 = {
    'Primitive': 1,
    'Nomad': 2,
    'Barbarian': 3,
    'Civilized': 3,
    'Civilized-decadent': 1
}

def cultureTable102a(char):
    if char['culture'] == 'Primitive':
        return(-3)
    elif char['culture'] == 'Nomad':
        return(0)
    elif char['culture'] == 'Barbarian':
        return(2)
    elif char['culture'] == 'Civilized':
        return(4)
    elif char['culture'] == 'Civilized-decadent':
        return(7)

def socialTable103(char):
    rand = randint(1,100) + char['cuMod'] + char['tiMod']
    if rand <= 12:
        return('Destitute', -3, '', 0)
    elif rand <= 40:
        return('Poor', -1, '', 0)
    elif rand <=84:
        return('Comfortable', 0, '', 0)
    elif rand == 85:
        socialTable103(char)
    elif rand <= 96:
        return('Well-to-do', 2, '', 0)
    elif rand <= 98:
        rand = randint(1,100)
        if rand <= char['tiMod'] + 1:
            return('Extremely Wealthy', 8, '', 0)
        else:
            return('Wealthy', 4, '', 0)
    elif rand >= 99:
        if char['culture'] == 'Primitive':
            char['title'] = random_choice(nobleTable758prim)
        elif char['culture'] == 'Nomad':
            char['title'] = random_choice(nobleTable758nomad)
        elif char['culture'] == 'Barbarian':
            char['title'] = random_choice(nobleTable758barb)
        else:
            char['title'] = random_choice(nobleTable758civil)
        char['tiMod'] = nobleTable758titleMod(char)
        # 103a is exactly like 103 but iterates at 99+ rands. Not necessary, but slightly cleaner on debug printing. Otherwise I could just keep iterating through 103 until it didn't roll into circles.
        return socialTable103a(char)
    else:
        raise ValueError("You shouldn't ever be able to see this error on socialTable103.")

def socialTable103a(char):
    rand = randint(1,100) + char['cuMod'] + char['tiMod']
    if rand <= 12:
        return('Destitute', -3, char['title'], char['tiMod'])
    elif rand <= 40:
        return('Poor', -1, char['title'], char['tiMod'])
    elif rand <=84:
        return('Comfortable', 0, char['title'], char['tiMod'])
    elif rand == 85:
        return socialTable103a(0, char['tiMod'], char['culture'], char['title'])
    elif rand <= 96:
        return('Well-to-do', 2, char['title'], char['tiMod'])
    elif rand <= 98:
        rand = randint(1,100)
        if rand <= char['tiMod'] + 1:
            return('Extremely Wealthy', 8, char['title'], char['tiMod'])
        else:
            return('Wealthy', 4, char['title'], char['tiMod'])
    elif rand >= 99:
        return socialTable103a(char)

def birthTable104(char):
    rand = randint(1,20) + char['cuMod']
    if rand >= 19:
        return(False)
    else:
        return(True)

def illegitBirthTable105(char):
    rand = randint(1,20) + char['cuMod']
    if rand <= 12:
        return 'mother was a common prostitute, unmarried'
    if rand <= 14:
        return 'mother was raped and remained unmarried'
    if rand <= 23:
        return 'mother was unmarried'
    if rand <= 27:
        return 'mother was a courtesan'

def familyTable106(char):
    rand = randint(1,20) + char['cuMod']
    if rand <= 8:
        familyInfo = 'Mother and father only'
    elif rand <= 12:
        familyInfo = 'Extended family. Mother and father, along with ' + str(randint(1,4)) + ' grandparents and ' + str(randint(1,4)) + ' aunts/uncles and cousins'
    elif rand <= 13:
        rand = randint(1,2)
        if rand > 1:
            familyInfo = "Grandparents on father's side"
        else:
            familyInfo = "Grandparents on mother's side"
    elif rand <= 14:
        rand = randint(1,2)
        if rand > 1:
            familyInfo = "Single grandparent on mother's side"
        else:
            familyInfo = "Single grandparent on father's side"
    elif rand <= 15:
        rand = randint(1,2)
        if rand > 1:
            familyInfo = "Single aunt or uncle on father's side"
        else:
            familyInfo = "Single aunt or uncle on mother's side"
    elif rand <= 16:
        rand = randint(1,2)
        if rand > 1:
            rand = randint(1,2)
            if rand > 1:
                familyInfo = "Aunt on father's side"
            else:
                familyInfo = "Aunt on mother's side"
        else:
            rand = randint(1,2)
            if rand > 1:
                familyInfo = "Uncle on father's side"
            else:
                familyInfo = "Uncle on mother's side"
    elif rand <= 18:
        familyInfo = "Only a mother"
    elif rand <= 19:
        familyInfo = "Only a father"
    elif rand <= 20:
        rand = randint(1,20)
        if rand <= 8:
            return guardiansTable754(char), True
        else:
            return familyTable106a(char), True
    elif rand <= 24:
        char['social'] = 'destitute'
        familyInfo = 'none, left to fend for yourself'
    elif rand <= 27:
        char['social'] = 'poor'
        familyInfo = 'none, raised in an orphanage'
    else:
        raise ValueError("familyTable106 is reporting a randint error for some weird fucking reason. This shouldn't be possible.")
    return familyInfo, False

def familyTable106a(char):
    rand = randint(1,20) + char['cuMod']
    if rand <= 8:
        return 'Mother and father only'
    elif rand <= 12:
        return 'Extended family. Mother and father, along with ' + str(randint(1,4)) + ' grandparents and ' + str(randint(1,4)) + ' aunts/uncles and cousins'
    elif rand <= 13:
        rand = randint(1,2)
        if rand > 1:
            return "Grandparents on father's side"
        else:
            return "Grandparents on mother's side"
    elif rand <= 14:
        rand = randint(1,2)
        if rand > 1:
            return "Single grandparent on mother's side"
        else:
            return "Single grandparent on father's side"
    elif rand <= 15:
        rand = randint(1,2)
        if rand > 1:
            return "Single aunt or uncle on father's side"
        else:
            return "Single aunt or uncle on mother's side"
    elif rand <= 16:
        rand = randint(1,2)
        if rand > 1:
            rand = randint(1,2)
            if rand > 1:
                return "Aunt on father's side"
            else:
                return "Aunt on mother's side"
        else:
            rand = randint(1,2)
            if rand > 1:
                return "Uncle on father's side"
            else:
                return "Uncle on mother's side"
    elif rand <= 18:
        return "Only a mother"
    elif rand <= 19:
        return "Only a father"

def siblingsTable107():
    rand = randint(1,19) #support for 20, just not implementing yet
    if rand <= 2:
        return 'none', '', ''
    elif rand <= 9:
        rand = randint(1,3)
    elif rand <= 15:
        rand = randint(2,4)
    elif rand <= 17:
        rand = randint(3,6)
    elif rand <= 19:
        rand = randint(2,8)
    #elif rand <= 20:
    return siblingsTable107a(rand)

def siblingsTable107a(number): # I rolled table 108 into this one because I got kinda caught up in the speed I was going. Eh, fuck it for now.
    siblingMale = 0
    siblingFemale = 0
    for i in range(number):
        rand = randint(1,20)
        if rand <= 9:
            siblingMale += 1
        else:
            siblingFemale += 1
    totalSiblings = siblingMale + siblingFemale
    birthOrder = ""
    if totalSiblings == 2:
        rand = randint(1,2)
        if rand == 1:
            birthOrder = 'first born'
        else:
            birthOrder = 'last born'
    elif totalSiblings == 2:
        rand = randint(1,3)
        if rand == 1:
            birthOrder = 'first born'
        elif rand == 2:
            birthOrder = 'middle born'
        else:
            birthOrder = 'last born'
    else:
        rand = randint(1,20)
        if rand <= 2:
            birthOrder =  'first born'
        elif rand <= 10:
            birthOrder =  'second born'
        elif rand <= 16:
            birthOrder =  'middle born'
        elif rand <= 18:
            birthOrder =  'second-to-last born'
        elif rand <= 20:
            birthOrder =  'last born'
    return siblingMale, siblingFemale, birthOrder

#note to me: I rolled 108 into 107a, that's why it's not here. I know I'll forget this.

def birthTimeTable109():
    rand = randint(1,4)
    if rand == 1:
        birthSeason = 'spring'
    elif rand == 2:
        birthSeason = 'summer'
    elif rand == 3:
        birthSeason = 'autumn'
    elif rand == 4:
        birthSeason = 'winter'

    rand = randint(1,8)
    if rand == 1:
        birthTimeOfDay = 'midnight'
    elif rand == 2:
        birthTimeOfDay = 'late night'
    elif rand == 3:
        birthTimeOfDay = 'early morning'
    elif rand == 4:
        birthTimeOfDay = 'sunrise'
    elif rand == 5:
        birthTimeOfDay = 'mid-day'
    elif rand == 6:
        birthTimeOfDay = 'afternoon'
    elif rand == 7:
        birthTimeOfDay = 'sunset'
    elif rand == 8:
        birthTimeOfDay = 'early evening'

    return birthSeason, birthTimeOfDay

def placeOfBirthTable110(char):
    rand = randint(1,20)
    if rand <= 6:
        return 'in the family home', -5
    elif rand <= 9:
        return "in a hospital or healer's hall", -7
    elif rand <= 10:
        return 'in a carriage while traveling', 1
    elif rand <= 11:
        return 'in a common barn', 1
    elif rand <= 13:
        return 'in a foreign land', 2
    elif rand <= 14:
        return 'in a cave', 5
    elif rand <= 15:
        return 'in the middle of a field', 1
    elif rand <= 16:
        return 'in a forest', 2
    elif rand <= 24:
        return exoticBirthLocationTable111(char)

def exoticBirthLocationTable111(char):
    rand = randint(1,19) #yep, it's another one of these, I took out roll 14 due to GM-only, will consider adding back in later
    if rand <= 2:
        return  'double roll thing, will keep noted here for now', 5
    elif rand == 3:
        return 'in a temple of ' + deitiesTable864(char), 5
    elif rand == 4:
        rand = randint(1,6)
        if rand == 6:
            return 'in the middle of a battlefield', 8
        else:
            return 'at a battlefield camp', 8
    elif rand == 5:
        return 'in an alley', 5
    elif rand == 6:
        return 'in a brothel', 2
    elif rand == 7:
        return 'in home of a local ruler', 2
    elif rand == 8:
        return 'home of the ruler of the country', 5
    elif rand == 9:
        return 'palace of an evil person or creature', 15
    elif rand == 10:
        return 'in a tavern', 2
    elif rand == 11:
        return 'in the sewers', 10
    elif rand == 12:
        return 'in a thieves den', 5
    elif rand == 13:
        return 'in the home of friendly nonhumans', 2
    elif rand == 14: #I know I'll be looking at this later and confused, but 14 is the one I pruned because it's set as GM ONLY
        return 'in the temple of an evil diety', 20
    elif rand == 15:
        return 'on another plane of reality', 15
    elif rand == 16:
        return 'in another time period', 10
    elif rand == 17:
        return 'on a ship at sea', 2
    elif rand == 18:
        return 'in a prison cell', 9
    elif rand == 19:
        return "in a wizard's laboratory", 20

def unusualBirthTable112(char): #this has been cleaned up, removing the GM selecting portions
    rand = randint(1,100) + char['biMod']
    if rand <= 60:
        return 'Nothing interesting', False
    elif rand <= 76:
        birthOccurance = [None]*1
        birthOccurance[0] = unusualBirthCircumstancesTable113()
    elif rand <= 92:
        birthOccurance = [None]*2
        birthOccurance[0] = unusualBirthCircumstancesTable113()
        birthOccurance[1] = unusualBirthCircumstancesTable113()
    elif rand <= 97:
        birthOccurance = [None]*3
        birthOccurance[0] = unusualBirthCircumstancesTable113()
        birthOccurance[1] = unusualBirthCircumstancesTable113()
        birthOccurance[2] = unusualBirthCircumstancesTable113()
    else:
        birthOccurance = [None]*4
        birthOccurance[0] = unusualBirthCircumstancesTable113()
        birthOccurance[1] = unusualBirthCircumstancesTable113()
        birthOccurance[2] = unusualBirthCircumstancesTable113()
        birthOccurance[3] = unusualBirthCircumstancesTable113()
    return birthOccurance, True

def unusualBirthCircumstancesTable113():
    rand = randint(1,100)
    if rand <= 5:
        return "a person of note near the character's home died when they were born"
    elif rand <= 10:
        return 'wolves and dogs set up a howling'
    elif rand <= 20:
        return 'mother died in childbirth'
    elif rand <= 23:
        return 'all glassware in the house shattered'
    elif rand <= 25:
        return 'all milk in the area soured'
    elif rand <= 27:
        return 'father believes the character is not his child'
    elif rand <= 31:
        rand = randint(1,5)
        return 'character has identical twin' + ((" that was separated at birth", "")[rand == 5])
    elif rand <= 34:
        return 'water froze or boiled by itself'
    elif rand <= 37:
        return 'unnatural weather occurred'
    elif rand <= 38:
        return 'unnaturally potent storms raged'
    elif rand <= 41:
        return 'character born at exactly noon'
    elif rand <= 44:
        return 'character born at exactly midnight'
    elif rand <= 48:
        return 'a seer declares that the character will be afflicted by an ancient family curse, ' #table 868 be here
    elif rand <= 50:
        randint(1,10)
        return 'a goose laid a golden egg' + ((", which the character still has with them", "")[rand >6])
    elif rand <= 53:
        return 'the sky darkened like an eclipse'
    elif rand <= 55:
        return 'the house became infested with poisonous snakes the next day'
    elif rand <= 56:
        return 'all gold in the house turned to lead'
    elif rand <= 57:
        return 'all metal in the house was turned into precious metals'
    elif rand <= 62:
        return 'as an infant, character was left to die on hillside by natural parents'
    elif rand <= 64:
        return 'character is born immediately after a tragedy, ' #table 528-a-gogo
    elif rand <= 69:
        return 'character is born with a birthmark' # here be table 866
    elif rand <= 75:
        return 'character is born with a curse' #868 here
    elif rand <= 81:
        return 'born with a blessing' #869
    elif rand <= 85:
        rand = randint(1,2)
        return 'character has a fraternal twin, ' + (("male", "female")[rand == 1])
    elif rand <= 86:
        return 'character is one of a set of identical triplets'
    elif rand <= 88:
        return 'witch prophesies death of the character' #here be 545
    elif rand <= 93:
        return 'character born with physical affliction' #874 go hurr
    elif rand <= 94:
        return 'character born with psychic powers' #873
    elif rand <= 99:
        return 'a mysterious stranger bestows a gift on the character at birth: ' + giftsTable863()
    else:
        return 'mother was reputed to be a virgin'

def parentTable114a(char):
    rand = randint(1,20)
    if rand <= 12:
        return 'Head of household is a ' + occupationsTable420(char)
    elif rand <= 14:
        return 'Head of household has two jobs: ' + occupationsTable420(char)
    elif rand <= 16:
        return 'Head of household does not work, the other parent does. They work as a ' + occupationsTable420(char)
    elif rand <= 18:
        return 'Both parents work. Head of household is a ' + occupationsTable420(char) + 'and other parent is a ' + occupationsTable420(char)
    elif rand <= 19:
        return 'Head of household was an adventurer, ' #table 757
    elif rand <= 20:
        return 'Head of household does not have an apparent occupation, but money is available when needed.'

def parentTable114b():
    rand = randint(1,3)
    noteworthyItems = []
    for _ in range(rand):
        noteworthyItems.append(parentTable114bA)

def parentTable114bA():
    rand = randint(1,20)
    if rand == 1:
        rand = randint(1,6)
        if rand <= 3:
            return 'noted for a personality trait, ' #647
        elif rand <= 5:
            return 'noted for a personality trait, ' #648
        else:
            return 'noted for an exotic personality trait, ' #649
    elif rand == 2:
        return 'had an unusual birth circumstance, ' + unusualBirthCircumstancesTable113()
    elif rand == 3:
        return 'devotes time to a hobby, ' #427
    elif rand == 4:
        return 'possesses an unusual item, ' + random_choice(giftsTable863)
    elif rand == 5:
        return 'is inventive, creative, and artistic'
    elif rand == 6:
        return 'affected by an exotic event which they speak of often, ' #544
    elif rand == 7:
        return 'tells tales of a legendary lost treasure'
    elif rand == 8:
        rand = randint(1,6)
        if rand == 1:
            return 'obsessed with a relationship with someone ' # 750
        elif rand == 2:
            return 'obsessed with an event from their past, ' #215
        elif rand == 3:
            return 'obsessed with working out of a personality trait, ' #fuck it, need to split here
        elif rand == 4:
            return 'obsessed with the accomplishment of a motivation, ' #page 8?
        elif rand == 5:
            return 'obsessed with accomplishing a future event, ' #217
        elif rand == 6:
            return 'obsessed with preventing a future event, ' #217
    elif rand == 9:
        return 'has a secret identity as a ' #occupation when I get to it
    elif rand == 10:
        return 'has a patron, ' #543
    elif rand == 11:
        return 'is a military veteran, ' + militaryTable535a()
    elif rand == 12:
        return 'is very religious, worships ' + deitiesTable864()
    elif rand == 13:
        rand = randint(1,4)
        if rand == 1:
            return 'does not like to talk about an important event in their past, ' #217
        elif rand == 2:
            return "does not like to talk about how they're persecuted for " #217
        elif rand == 3:
            return 'does not like to talk about their past and how important they are to their home town'
        elif rand == 4:
            return 'refuses to speak about a past event'
    elif rand == 14:
        rand = randint(1,4)
        if rand == 1:
            return 'particularly loving towards family'
        elif rand == 2:
            return 'does not love family or children'
        elif rand == 3:
            return 'is unfaithful to spouse'
        elif rand == 4:
            return 'has married more than once, current spouse is number ' + str(randint(1,4))
    elif rand == 15:
        return 'originally from a different culture'
    elif rand == 16:
        return 'originally from a different social status'
    elif rand == 17:
        return 'from a foreign land'
    elif rand == 18:
        rand = randint(1,5) # it's another re-roll
        if rand == 1:
            return 'has a rival ' #762
        elif rand == 2:
            return 'has many enemies ' #roll on 762 a lot
        elif rand == 3:
            return 'has ' + str(randint(3,13)) + ' close friends living nearby'
        elif rand == 4:
            return 'has ' + str(randint(2,7)) + ' jilted ex-lovers'
        elif rand == 5:
            return 'had a companion, ' + companionTable761()
        #elif rand == 6:
    elif rand == 19:
        return 'was horribly wounded, ' #870
    elif rand == 20:
        return 'noted for extremely unusual personality: ' #649

def childhoodEventsTable215a(char):
    rand = randint(1,3)
    childhoodEvents = []
    adolescentEvents = []
    for _ in range(rand):
        childhoodEvents.append(childhoodEventsTable215b(char))
    rand = randint(1,3)
    for _ in range(rand):
        adolescentEvents.append(childhoodEventsTable215b(char))
    return childhoodEvents, adolescentEvents

def childhoodEventsTable215b(char):
    rand = randint(1,17) + char['solMod']
    if rand == -2:
        significantEvent = "all public assistance is terminated due to war. The character's family is involved in the riots in the poorer sectors of towns and villages"
    elif rand == -1:
        significantEvent = 'while foraging in a trash heap, the character finds ' + giftsTable863()
    elif rand == 0:
        significantEvent = childhoodEventsTable215b(char)
    elif rand == 1:
        significantEvent = 'friends involve the character in illegal activities, ' #534
    elif rand == 2:
        significantEvent = 'a tragedy occurs, ' #528
    elif rand == 3:
        significantEvent = 'The character learns an unusual skill, ' #876
    elif rand == 4:
        significantEvent = 'something wonderful occurs: ' #529
    elif rand == 5:
        significantEvent = "The character learns to be adept at the head of household's occupation. If there is no head of household, then select randomly."
    elif rand == 6:
        rand = randint(1,9)
        significantEvent = 'the character runs away, '
        if rand == 1:
            significantEvent += 'and never returns'
        elif rand == 2:
            significantEvent += 'and returns after ' + str(randint(1,8)) + ' days'
        elif rand == 3:
            significantEvent += 'and returns after ' + str(randint(1,12)) + ' months'
        elif rand == 4:
            significantEvent += 'and returns after ' + str(randint(1,6)) + ' years'
        elif rand == 5:
            significantEvent += 'to a distant land'
        elif rand == 6:
            significantEvent += 'and joins the circus'
        elif rand == 7:
            significantEvent += 'and falls into the hands of criminals, ' #534
        elif rand == 8:
            significantEvent += 'and wanders the land, avoiding authorities'
        elif rand == 9:
            significantEvent += 'and lives with ' + random_choice(nonhumansTable751)
    elif rand == 7:
        significantEvent = 'character has a religious experience, ' #541
    elif rand == 8:
        rand = randint(1,6)
        if rand == 1:
            significantEvent = 'character is loved by parents'
        elif rand == 2:
            significantEvent = 'character is unloved'
        elif rand == 3:
            significantEvent = "family has great plans for the character's future"
        elif rand == 4:
            significantEvent = "family does not approve of character's friends"
        elif rand == 5:
            significantEvent = "family encourages character's interests"
        elif rand == 6:
            rand = randint(1,2)
            significantEvent = (("mother", "father")[rand == 1]) + ' is distant towards the character'
    elif rand == 9:
        significantEvent = 'character serves a patron, ' #543
    elif rand <= 11:
        significantEvent = 'age-specific event'
    elif rand == 12:
        significantEvent = 'character gains a friend, ' #750
    elif rand == 13: #skipped the real 13 and 14 for the time being
        significantEvent = 'an exotic event occurs, ' #544
    elif rand == 14:
        rand = randint(1,2)
        significantEvent = "character's parents split up, character stays with " + (("mother", "father")[rand == 1])
    elif rand == 15:
        rand = randint(1,4)
        if rand == 1:
            significantEvent = 'character is molested by ' #750
        elif rand == 2:
            significantEvent = 'a tragedy occurs, ' #528
        elif rand == 3:
            significantEvent = 'character angers an old woman who puts a curse on them, ' #868
        elif rand == 4:
            significantEvent = 'character acquires a rival, ' #762
    elif rand == 16:
        rand = randint(1,4)
        if rand == 1:
            significantEvent = 'character inherits a large sum of money'
        elif rand == 2:
            significantEvent = 'a fairy blesses the character as a reward for a good deed, ' #869
        elif rand == 3:
            significantEvent = 'something wonderful occurs, ' #529
        elif rand == 4:
            significantEvent = 'character acquires a companion, ' #761
    elif rand == 17:
        significantEvent = 'age-specific event occurs, ' #216a/216b
    elif rand == 18:
        significantEvent = 'character develops jaded tastes for exotic and expensive pleasures'
    elif rand == 19:
        significantEvent = childhoodEventsTable215b(char)
    elif rand == 20:
        significantEvent = "rivals force the character's family to move somewhere new"
    elif rand == 21:
        significantEvent = 'something wonderful occurs, ' #529
    elif rand == 22:
        significantEvent = 'a tragedy occurs, ' #528
    elif rand == 23:
        significantEvent = 'character is betrothed in a political marriage'
    elif rand == 24:
        significantEvent = 'head of household is made a close advisor of a local ruler'
    elif rand == 25: #also skipped 25
        significantEvent = 'family travels widely, visiting several foreign lands'
    elif rand == 26:
        significantEvent = 'a tutor teaches the character an unusual skill, ' #876
    elif rand == 27:
        significantEvent = 'family throws extravagant birthday party for character. Character acquires special gift, ' + giftsTable863()
    elif rand == 28:
        significantEvent = 'character exhibits exotic personality, ' #649
    elif rand == 29:
        significantEvent = 'family gives character ' + str(randint(1,10)) + ' slaves to do with as they see fit'
    elif rand == 30:
        significantEvent = 'family gives character personal estate with ' + str(randint(1,10)) + ' square miles of property'
    return significantEvent

def childhoodEventsTable216a():
    rand = randint(1,20)
    if rand == 1:
        return 'a neighbor schools the character, improving their literacy'
    elif rand == 2:
        return 'character becomes emotionally attached to a toy for ' + str(randint(2,20)) + ' years'
    elif rand == 3:
        return 'character has a collection of related things, such as rocks, dolls, animal skulls, etc.'
    elif rand == 4:
        return 'character has a close friendship with a sibling or cousin'
    elif rand == 5:
        return 'character has an imaginary friend'
    elif rand == 6:
        return 'character is a child prodigy with an unusual skill, ' #876
    elif rand == 7:
        return 'character learns use of a weapon appropriate to their culture and social status'
    elif rand == 8:
        return 'character and a friend discover secret hiding place near home'
    elif rand == 9:
        return 'character becomes proficient at a sporting event'
    elif rand == 10:
        return 'friend of the family, an old warrior, tells the character tales of adventure'
    elif rand == 11:
        return 'character becomes well-known for the occurance of an event in their life, ' + childhoodEventTables215(0)
    elif rand == 12:
        rand = randint(1,10)
        return "one of the character's grandparents dies of natural causes in the presence of the character " + (("that grandparent entrusts the character with a secret", "")[rand < 7])
    elif rand == 13:
        return 'character witnesses a crime being committed by ' + str(randint(1,4)) + ' people. They are unable to catch him. The crime is ' #875
    elif rand == 14:
        return 'race specific event, fuck'
    elif rand == 15:
        return 'an exotic event occurs, ' #544
    elif rand == 16:
        return 'character discovers they are a near exact twin of a young noble, ' + random_choice(nobleTable758civil)
    elif rand == 17:
        return 'a tragedy occurs, ' #528
    elif rand == 18:
        return 'something wonderful occurs, ' #529
    elif rand == 19:
        return childhoodEventsTable216b()
    elif rand == 20:
        return 'character acquires a hobby, ' #427

def childhoodEventsTable216b():
    rand = randint(1,19)
    if rand == 1:
        return 'character learns to use weapon appropriate to their culture and social status'
    elif rand == 2:
        return 'to be fashionable, character gets tatto on their face, ' #866
    elif rand <= 4:
        return 'apprenticed to learn an occupation, ' #419
    elif rand == 5:
        return 'a wizard teaches the character a simple spell'
    elif rand == 6:
        eventPresuppose = 'character is accused of a crime which they did not commit (' #875
        rand = randint(1,6)
        if rand == 1:
            return eventPresuppose + ', is imprisoned, ' #540 here
        elif rand == 2:
            return eventPresuppose + ', is stockaded and flogged publicly as an example to others'
        elif rand == 3:
            rand = randint(1,3)
            eventPresuppose = eventPresuppose + ', is tortured to reveal the names of accomplices'
            if rand == 3:
                eventPresuppose = eventPresuppose #870
        elif rand == 4:
            return eventPresuppose + ', is found innocent, but not before being humiliated'
        elif rand == 5:
            return eventPresuppose + ', is sentenced to death, but is rescued by outlaws.' #534 goes here
        elif rand == 6:
            return eventPresuppose + ', is sold into slavery: ' + enslavedTable539()
    elif rand == 7:
        return 'character learns an unusual skill, ' #876
    elif rand == 8:
        return 'character learns a hobby, ' #427
    elif rand == 9:
        return "character learns head of household's occupation"
    elif rand == 10:
        eventPresuppose = 'character joins the military ' + militaryTable535(char)
        rand = randint(1,4)
        if rand == 1:
            eventPresuppose = eventPresuppose + 'because they were drafted, '
        elif rand == 2:
            eventPresuppose = eventPressuppose + 'because they patriotically volunteered, '
        elif rand == 3:
            eventPresuppose = eventPresuppose + 'because they forced to, '
        elif rand == 4:
            eventPresuppose = eventPresuppose + 'on mistake, '
        eventPresuppose = eventPresuppose + 'Info: '
    elif rand == 11:
        rand = randint(1,5)
        if rand == 5:
            return 'character participated in a successful rebellion'
        else:
            rand = randint(1,10)
            if rand != 10:
                return 'character participated in a failed rebellion, but only a few close friends knew of it'
            else:
                return 'character was known to participate in a failed rebellion and is now an outlaw'
    elif rand == 12:
        return 'character becomes famous for ' + childhoodEventTables215b()
    elif rand <= 14:
        return 'character has a romantic encounter, ' #542
    elif rand == 15:
        return 'character learns to speak another language'
    elif rand == 16:
        return 'race specific event. fuck.'
    elif rand == 17:
        return 'an exotic event occurs, ' #544
    elif rand == 18:
        return 'a tragedy occurs, ' #528
    elif rand == 19:
        return 'something wonderful occurs, ' #529
#    elif rand == 20:

def adulthoodSignificantEventsTable217(char):
    rand = randint(1,3)
    adulthoodEvents = []
    for _ in range(rand):
        adulthoodEvents.append(adulthoodSignificantEventsTable217a(char))
    return adulthoodEvents

def adulthoodSignificantEventsTable217a(char):
    rand = randint(2,39) + char['solMod']
    if rand == -1:
        return 'while foraging or hunting for food, the character saves a trapped predatory beast. Later, the same beast saves the character.'
    elif rand == 0:
        return 'to earn a living, the character learns a new occupation: ' + occupationsTable420(char)
    elif rand <= 2:
        return 'something wonderful occurs, ' #529
    elif rand <= 4:
        return 'a tragedy occurs, ' #528
    elif rand == 5:
        return 'character learns an unusual skill, ' #876
    elif rand == 6:
        rand = randint(1,5)
        if rand == 5:
            return 'character participated in a successful rebellion'
        else:
            rand = randint(1,10)
            if rand != 10:
                return 'character participated in a failed rebellion, but only a few close friends knew of it'
            else:
                return 'character was known to participate in a failed rebellion and is now an outlaw'
    elif rand == 7:
        return 'Character serves a patron, ' #543
    elif rand == 8:
        eventPresuppose = 'Character has wanderlust and decides to travel for ' + str(randint(1,6)) + ' years.  During this time, the character '
        rand = randint(1,6)
        if rand == 1:
            eventPresuppose = eventPresuppose + 'visits major cities and towns in the land.'
        elif rand == 2:
            eventPresuppose = eventPresuppose + 'signs on as a seaman on a ship.'
        elif rand == 3:
            eventPresuppose = eventPresuppose + 'journeys through mountains.'
        elif rand == 4:
            eventPresuppose = eventPresuppose + 'investigates nearby dark woods.'
        elif rand == 5:
            eventPresuppose = eventPresuppose + 'travels to a distant land, learning a foreign language.'
        elif rand == 6:
            eventPresuppose = eventPresuppose + 'lives with nonhumans, ' + random_choice(nonhumansTable751)
        return eventPresuppose
    elif rand <= 10:
        return 'character has a religious experience, ' #541
    elif rand == 11:
        return "character saves someone's life, and that person becomes the character's companion: " #761
    elif rand <= 13:
        return 'race-specific event. fuck.'
    elif rand == 14: #skipping 14
        return 'an exotic event occurs, ' #544
    elif rand == 15:
        return 'character learns to use a weapon appropriate to their culture and social status'
    elif rand == 16:
        rand = randint(1,3)
        if rand == 1:
            return 'a tragedy occurs, ' #528
        elif rand == 2:
            return 'the character angers an old woman, who curses them, ' #868
        elif rand == 3:
            return 'character acquires a rival, ' #762
    elif rand == 17:
        rand = randint(1,3)
        if rand == 1:
            return 'an old man whom the character rescues blesses the character, ' #869
        elif rand == 2:
            return 'something wonderful occurs, ' #529
        elif rand == 3:
            return 'character acquires a companion, ' #761
    elif rand == 18:
        return 'character becomes well-known for ' + adulthoodSignificantEventsTable217a(char)
    elif rand == 19:
        return 'character develops an exotic personality trait, ' #649
    elif rand == 20:
        return 'character inherits property from a relative' #863 sub-table???
    elif rand <= 22: #22 regular was skipped, so this should be 23-24
        return 'character becomes involved in illegal activities, ' #534a
    elif rand == 23:
        return 'character learns to use an unusual weapon'
    elif rand <= 26:
        eventPresuppose = 'character joins the military because '
        rand = randint(1,4)
        if rand == 1:
            eventPresuppose = eventPresuppose + 'they were drafted, '
        elif rand == 2:
            eventPresuppose = eventPresuppose + 'they patriotically volunteered, '
        elif rand == 3:
            eventPresuppose = eventPresuppose + 'forced to, '
        elif rand == 4:
            eventPresuppose = eventPresuppose + 'on mistake, '
        print('MILITARY CHECK')
        service, event, rank = militaryTable535(char)
        return eventPresuppose + 'Info: ' + service + event + rank
    elif rand <= 30:
        return 'character has a romantic encounter, ' #542
    elif rand == 31:
        return 'character acquires a hobby, ' #427
    elif rand == 32:
        return 'character develops jaded tastes for exotic and expensive pleasures'
    elif rand <= 34:
        eventPresuppose = 'character is accused of a crime which they did not commit (' #875
        rand = randint(1,6)
        if rand == 1:
            return eventPresuppose + ', is imprisoned, ' #540 here
        elif rand == 2:
            return eventPresuppose + ', is stockaded and flogged publicly as an example to others'
        elif rand == 3:
            rand = randint(1,3)
            eventPresuppose = eventPresuppose + ', is tortured to reveal the names of accomplices'
            if rand == 3:
                eventPresuppose = eventPresuppose #870
        elif rand == 4:
            return eventPresuppose + ', is found innocent, but not before being humiliated'
        elif rand == 5:
            return eventPresuppose + ', is sentenced to death, but is rescued by outlaws.' #534 goes here
        elif rand == 6:
            return eventPresuppose + ', is sold into slavery: ' + enslavedTable539() + ')'
        return eventPresuppose
    elif rand <= 36: #skipping 37-38, as well as 39
        return 'character learns an occupation, ' + occupationsTable420(char)
    elif rand <= 39:
        return adulthoodSignificantEventsTable217a(char)
    elif rand == 40:
        return 'character is made close advisor to a local ruler'
    elif rand <= 43:
        return 'character develops an exotic personality trait, ' #649
    elif rand <= 45:
        return "family sends character a personal servant who refuses to leave the character's service. The servant becomes a companion: " #761
    elif rand <= 48:
        return 'a ruler with slightly lower social status than the character proposes marriage. The marriage is obviously political in nature.'
    elif rand <= 55:
        return 'a radical change in political structure strips the character of all land and nobility.'

def apprenticeshipsTable419a():
    rand = randint(1,3)
    if rand == 1:
        return random_choice(craftsTable424a)
    elif rand == 2:
        return random_choice(craftsTable424b)
    elif rand == 3:
        return random_choice(craftsTable424c)

def apprenticeshipsTable419b():
    rand = randint(1,9) #again, not doing the re-roll shit
    if rand == 1:
        return "character's master is known for their strong personality"
    elif rand == 2:
        return "character manages to accidentally break the master's valuable collection of ceramic pots. For this, he's expelled."
    elif rand == 3:
        return "Character stumbles upon a lost secret of the craft, which his master takes credit for."
    elif rand == 4:
        return "Character continues to study the craft with his master for an extra " + str(randint(1,6)) + " years."
    elif rand == 5:
        return "The character discovered that the master's shop is a front for a criminal network."
    elif rand == 6:
        return "The master is world-renowned in their craft."
    elif rand == 7:
        rand = randint(1,2)
        return "A " + (("female", "male")[rand == 1]) + " apprentice becomes best friends with the character. That person would later become a master of the craft."
    elif rand == 8:
        return "An exotic event occurs, affecting the character's master: " #544
    elif rand == 9:
        return "Character accompanies their master on a long journey: " + adulthoodSignificantEventsTable217a(randint(1,5))

def occupationsTable420(char):
    if char['culture'] == "Primitive":
        return primitiveOccupationsTable420a(char)
    elif char['culture'] == "Nomad":
        return nomadOccupationsTable421a(char)
    elif char['culture'] == "Barbarian":
        return barbarianOccupationsTable422a(char)
    else:
        return civilizedOccupationsTable423a(char)

def primitiveOccupationsTable420a(char):
    rand = randint(1,20)
    if rand <= 9:
        return 'fisherman'
    elif rand <= 18:
        return 'hunter'
    elif rand <= 19:
        return 'warrior'
    elif rand == 20:
        return primitiveOccupationsTable420b(char)

def primitiveOccupationsTable420b(char):
    rand = randint(1,4)
    if rand == 1:
        return 'shaman'
    elif rand == 2:
        return 'basket weaver'
    elif rand == 3:
        return 'artist'
    elif rand == 4:
        return 'toolmaker'

def nomadOccupationsTable421a(char):
    rand = randint(1,20)
    if rand <= 2:
        return random_choice(craftsTable424a)
    elif rand <= 12:
        return 'herder'
    elif rand <= 16:
        return 'hunter'
    elif rand <= 18:
        return 'warrior'
    elif rand == 19:
        return 'merchant'
    elif rand == 20:
        return nomadOccupationsTable421b(char)

def nomadOccupationsTable421b(char):
    rand = randint(1,10)
    if rand == 1:
        return 'priest'
    elif rand == 2:
        return 'healer'
    elif rand == 3:
        return 'adventurer, ' #757
    elif rand == 4:
        return 'career criminal, ' #755
    elif rand == 5:
        return 'tentmaker'
    elif rand == 6:
        return 'weapon master'
    elif rand == 7:
        return 'counselor/philosopher'
    elif rand == 8:
        return '423a'
    elif rand == 9:
        return 'horsemaster'
    elif rand == 10:
        return 'entertainer'

def barbarianOccupationsTable422a(char):
    rand = randint(1,20)
    if rand <= 2:
        return random_choice(craftsTable424a)
    elif rand <= 8:
        return 'farmer'
    elif rand <= 11:
        return 'fisherman'
    elif rand <= 13:
        return 'herder'
    elif rand <= 15:
        return 'hunter'
    elif rand <= 17:
        return 'warrior'
    elif rand == 18:
        return random_choice(craftsTable424b)
    elif rand == 19:
        return merchantsTable425(0)
    elif rand == 20:
        return barbarianOccupationsTable422b(char)

def barbarianOccupationsTable422b(char):
    rand = randint(1,20)
    if rand <= 7:
        return civilizedOccupationsTable423a(char)
    elif rand <= 9:
        return 'priest'
    elif rand == 10:
        return 'healer'
    elif rand == 11:
        return 'adventurer, ' #757
    elif rand == 12:
        return 'ship builder'
    elif rand == 13:
        return 'career criminal, ' #755
    elif rand == 14:
        return 'wizard, witch, or warlock'
    elif rand == 15:
        return 'counselor'
    elif rand == 16:
        return 'horsemaster'
    elif rand == 17:
        return 'explorer'
    elif rand == 18:
        return 'entertainer'
    elif rand == 19:
        return 'forester'
    elif rand == 20:
        return random_choice(craftsTable424c)

def civilizedOccupationsTable423a(char):
    rand = randint(1,10) + char['solMod']
    if rand == -2:
        return nomadOccupationsTable421a(char)
    elif rand <= 5:
        return civilizedOccupationsTable423b(char)
    elif rand == 6:
        return barbarianOccupationsTable422a(char)
    elif rand == 7:
        return civilizedOccupationsTable423e(char)
    elif rand <= 11:
        return civilizedOccupationsTable423c(char)
    elif rand <= 14:
        return civilizedOccupationsTable423d(char)
    elif rand == 15:
        return civilizedOccupationsTable423e(char)
    elif rand <= 23:
        return civilizedOccupationsTable423d(char)

def civilizedOccupationsTable423b(char):
    rand = randint(1,20)
    if rand == 1:
        return 'beggar'
    elif rand <= 6:
        rand = randint(1,4)
        if rand == 1:
            return 'freeman farmer'
        elif rand == 2:
            return 'herder'
        elif rand == 3:
            return 'sharecropper'
        elif rand == 4:
            return 'serf'
    elif rand <= 7:
        return 'tinker'
    elif rand <= 8:
        return 'sailor'
    elif rand <= 10:
        rand = randint(1,6)
        if rand == 1:
            return 'miner'
        elif rand == 2:
            return 'stone cutter'
        elif rand == 3:
            return 'wood cutter'
        elif rand == 4:
            return 'charcoal burner'
        elif rand == 5:
            return 'peat cutter'
        elif rand == 6:
            return 'unskilled laborer'
    elif rand <= 11:
        return 'launderer'
    elif rand <= 14:
        return 'fisherman'
    elif rand <= 15:
        rand = randint(1,6)
        if rand == 1:
            return 'butler'
        elif rand == 2:
            return 'cook'
        elif rand == 3:
            return 'housekeeper'
        elif rand == 4:
            return 'gardener'
        elif rand == 5:
            return 'stable hand'
        elif rand == 6:
            return 'footman'
    elif rand <= 16:
        rand = randint(1,4)
        if rand == 1:
            return 'bartender'
        elif rand == 2:
            return 'serving person'
        elif rand == 3:
            return 'housekeeper'
        elif rand == 4:
            return 'bouncer'
    elif rand <= 17:
        return 'street vendor'
    elif rand <= 18:
        return 'soldier' + militaryTable535(char)
    elif rand == 19:
        return random_choice(craftsTable424a)
    elif rand == 20:
        return 'second hand shop'

def civilizedOccupationsTable423c(char):
    rand = randint(1,20)
    if rand == 1:
        return 'money lender'
    elif rand <= 5:
        return 'merchant'
    elif rand <= 6:
        return 'business owner, ' + civilizedOccupationsTable423b(char)
    elif rand <= 8:
        return random_choice(craftsTable424b)
    elif rand <= 9:
        rand = randint(1,4)
        if rand == 1:
            return 'weapon instructor'
        elif rand == 2:
            return 'unusual skill instructor, ' #876
        elif rand == 3:
            rand = randint(1,4)
            if rand == 1:
                addIt = 'combat skills'
            elif rand == 2:
                addIt = 'horse skills'
            elif rand == 3:
                addIt = 'forestry skills'
            elif rand == 4:
                addIt = 'naval skills'
            return 'military instrutor in ' + addIt
        elif rand == 4:
            rand = randint(1,3)
            if rand == 1:
                random_choice(craftsTable424a)
            elif rand == 2:
                random_choice(craftsTable424b)
            elif rand == 3:
                random_choice(craftsTable424c)
    elif rand <= 10:
        return 'government official, ' #752
    elif rand <= 11:
        return random_choice(craftsTable424a)
    elif rand <= 12:
        return 'chef'
    elif rand <= 13:
        return 'an overseer of ' + civilizedOccupationsTable423a(char)
    elif rand <= 14:
        return 'innkeeper'
    elif rand <= 15:
        return 'scribe'
    elif rand <= 16:
        return 'guide/pilot'
    elif rand <= 17:
        return 'ship captain (not own ship)'
    elif rand <= 18:
        return 'engineer'
    elif rand <= 19:
        return 'teacher'
    elif rand <= 20:
        return 'tavern owner'

def civilizedOccupationsTable423d(char):
    rand = randint(1,20)
    if rand == 1:
        return 'alchemist'
    elif rand == 2:
        return 'engineer'
    elif rand == 3:
        return 'architect'
    elif rand == 4:
        return 'chlurgeon'
    elif rand <= 7:
        return merchantsTable425(char)
    elif rand == 8:
        return 'craftsmen' #424c
    elif rand == 9:
        return 'courtier/courtesar'
    elif rand == 10:
        return 'diplomat'
    elif rand == 11:
        return 'author/playwrite/poet'
    elif rand == 12:
        return 'litigation trickster'
    elif rand == 13:
        return 'philosopher'
    elif rand == 14:
        return 'crafter' #424b
    elif rand == 15:
        return 'interpreter'
    elif rand == 16:
        return 'government official' #752
    elif rand == 17:
        return 'banker'
    elif rand == 18:
        return 'business owner: ' + civilizedOccupationsTable423a(char)
    elif rand == 19:
        return 'landlord'
    elif rand == 20:
        return 'craftmaster' #lots of shit here

def civilizedOccupationsTable423e(char):
    rand = randint(1,20)
    if rand == 1:
        return 'assassin'
    elif rand == 2:
        return 'gladiator'
    elif rand == 3:
        return 'adventurer, ' #757
    elif rand == 4:
        return 'priest' #541b
    elif rand == 5:
        return 'wizard'
    elif rand == 6:
        return 'jack of all trades: ' + civilizedOccupationsTable423a() + ' and ' + civilizedOccupationsTable423a() + ' and ' + civilizedOccupationsTable423a()
    elif rand == 7:
        return 'career criminal, ' #755
    elif rand == 8:
        return 'entertainer'
    elif rand == 9:
        return 'printer'
    elif rand == 10:
        return 'private detective or spy'
    elif rand == 11:
        return 'professional guild thief, ' #534
    elif rand == 12:
        return 'astrologer/diviner/fortune teller'
    elif rand == 13:
        return 'rumormonger'
    elif rand == 14:
        rand = randint(1,4)
        if rand == 1:
            return 'doomsayer'
        elif rand == 2:
            return 'oracle'
        elif rand == 3:
            return 'hermit'
        elif rand == 4:
            return 'seer'
    elif rand == 15:
        return 'charlot or horse racer'
    elif rand == 16:
        return 'professional gambler'
    elif rand == 17:
        return 'healer/herbalist'
    elif rand == 18:
        return 'scientist'
    elif rand == 19:
        return 'veterinarian'
    elif rand == 20:
        return 'ship builder'

craftsTable424a = {
    'blacksmith': 1,
    'potter': 1,
    'weaver': 1,
    'stone mason': 1,
    'baker': 1,
    'butcher': 1,
    'carpenter': 1,
    'tanner': 1,
    'rope and net maker': 1,
    'leather worker': 1,
    'cobbler': 1,
    'painter': 1,
    'spinner': 1,
    'dyer': 1,
    'fletcher': 1,
    'sailmaker': 1,
    'saddle and riding harness maker': 1
}

craftsTable424b = {
    'shipwright': 1,
    'wheel/cartwright': 1,
    'distiller': 1,
    'fuller': 1,
    'sign painter': 1,
    'chandler': 1,
    'miller': 1,
    'armor smith': 1,
    'sausage maker': 1,
    'brewer': 1,
    'animal trainer': 1,
    'plasterer': 1,
    'glazier': 1,
    'tailor': 1,
    'copper and pewter smith': 1,
    'glassblower': 1,
    'cabinet maker': 1,
    'weapon master': 1,
    'dress maker': 1,
    'sword-dancer': 1
}

craftsTable424c = {
    'silver smith': 1,
    'costumer': 1,
    'goldsmith': 1,
    'jeweler': 1,
    'instrument maker': 1,
    'clock maker': 1,
    'cartographer': 1,
    'perfumer': 1,
    'animal trainer': 1,
    'apothecary': 1,
    'furrier': 1,
    'horse breeder': 1,
    'artist': 1,
    'wine maker': 1,
    'oculist': 1,
    'pastry chef': 1,
    'confectioner': 1,
    'paper and ink maker': 1,
    'sword smith': 1,
    'illuminator': 1
}

def merchantsTable425(char):
    rand = randint(1,16)
    if rand == 0:
        return 'pawnshop'
    elif rand == 1:
        return 'caravan master'
    elif rand == 2:
        return 'tavernkeeper'
    elif rand == 3:
        return 'trader'
    elif rand == 4:
        return 'innkeeper'
    elif rand == 5:
        return 'dry goods seller'
    elif rand == 6:
        return 'curio merchant'
    elif rand == 7:
        return 'snake oil salesman'
    elif rand == 8:
        return 'book seller'
    elif rand == 9:
        return 'clothing seller'
    elif rand == 10:
        return 'weapon shop'
    elif rand == 11:
        return 'fishmonger'
    elif rand == 12:
        return 'green grocer'
    elif rand == 13:
        return 'wine merchant'
    elif rand == 14:
        return 'importer'
    elif rand == 15:
        return 'furniture dealer'
    elif rand == 16:
        return 'slaver'
    elif rand == 17:
        return 'carpets & tapestries'
    elif rand == 18:
        return 'livestock trader'
    elif rand == 19:
        return 'shipping agent'
    elif rand == 20:
        return 'silk merchant'
    elif rand == 21:
        return 'art dealer'
    elif rand == 22:
        return 'gem merchant'
    elif rand == 23:
        return 'real estate broker'
    elif rand == 24:
        return 'lumber merchant'
    elif rand == 28:
        return 'master merchant: ' + merchantsTable425(6) + ', ' + merchantsTable425(6) + ', ' + merchantsTable425(6)

def hobbiesTable427():
    rand = randint(1,20)
    if rand == 1:
        hobby = 'collecting something'
    elif rand == 2:
        hobby = 'dancing'
    elif rand == 3:
        hobby = 'playing a musical instrument'
    elif rand == 4:
        hobby = 'reading for enjoyment'
    elif rand == 5:
        hobby = 'writing creatively'
    elif rand == 6:
        hobby = 'acting'
    elif rand == 7:
        hobby = 'drawing or painting'
    elif rand == 8:
        hobby = 'needlework'
    elif rand == 9:
        hobby = 'singing'
    elif rand == 10:
        rand = randint(1,8)
        if rand == 1:
            hobby = 'studying history'
        elif rand == 2:
            hobby = 'studying religion'
        elif rand == 3:
            hobby = 'studying art'
        elif rand == 4:
            hobby = 'studying astronomy'
        elif rand == 5:
            hobby = 'studying astrology'
        elif rand == 6:
            hobby = 'studying other cultures'
        elif rand == 7:
            hobby = 'studying magic'
        elif rand == 8:
            hobby = 'studying weapons'
    elif rand == 11:
        rand = randint(1,8)
        if rand == 1:
            hobby = 'wrestling'
        elif rand == 2:
            hobby = 'running'
        elif rand == 3:
            hobby = 'fencing'
        elif rand == 4:
            hobby = 'team ball sport'
        elif rand == 5:
            hobby = 'horse racing'
        elif rand == 6:
            hobby = 'swimming'
        elif rand == 7:
            hobby = 'archery'
        elif rand == 8:
            hobby = 'boxing'
    elif rand == 12:
        hobby = 'building detailed models'
    elif rand == 13:
        hobby = 'developing appreciation of the arts'
    elif rand == 14:
        hobby = 'hairdressing and cosmetics'
    elif rand == 15:
        hobby = 'hunting for sport'
    elif rand == 16:
        hobby = 'gardening'
    elif rand == 17:
        hobby = 'breeding dogs'
    elif rand == 18:
        hobby = 'animal husbandry'
    elif rand == 19:
        hobby = 'fishing for sport'
    elif rand == 20:
        hobby = 'heraldry'
    return hobby + ' (interest: ' + hobbiesTable427c() + ')'

def hobbiesTable427c():
    rand = randint(1,10)
    if rand <= 2:
        return 'casual'
    elif rand <= 7:
        return 'sporadic and variable'
    elif rand <= 9:
        return 'devoted'
    elif rand == 10:
        return 'consuming passion'

def tragediesTable528():
    rand = randint(1,19) + char['solMod']
    if rand == -2:
        return 'wild beasts attack. Character is injured ' #870 + #753
    elif rand == -1:
        return tragediesTable528() #should re-roll without char['solMod'], but fuck it for now
    elif rand == 0:
        return 'imprisoned for a crime the character did not commit, ' #875, #540
    elif rand == 1:
        return tragediesTable528() #this should be different as well
    elif rand == 2:
        return 'parents/guardians unable to pay their taxes, ' #546
    elif rand == 3:
        return 'a favorite pet dies' #requires 750
    elif rand == 4:
        return 'orphaned! ' #546
    elif rand == 5:
        tragedy = 'place character lives is wiped out by '
        rand = randint(1,6)
        if rand == 1:
            return tragedy + ' a deadly disease'
        elif rand <= 3:
            return tragedy + ' a terrible fire'
        elif rand <= 5:
            return tragedy + ' war'
        elif rand == 6:
            return tragedy #750 go hurr
    elif rand == 6:
        return 'character is responsible for a death, ' #750 and 545
    elif rand == 7:
        return 'orphaned! ' #546
    elif rand == 8: #skipping the original 8
        tragedy = 'a favorite possession is '
        rand = randint(1,6)
        if rand <= 3:
            return tragedy + ' lost'
        elif rand <= 5:
            return tragedy + ' stolen'
        elif rand == 6:
            return tragedy + ' stolen, with a fake left in its place'
    elif rand == 9:
        rand = randint(1,6)
        if rand <= 3:
            tragedy1 = 'father is outlawed due to '
        elif rand == 4:
            tragedy1 = 'mother is outlawed due to '
        elif rand <= 6:
            tragedy1 = 'parents are both outlawed due to '
        return tragedy1 #875
    elif rand == 10:
        return 'character sold into slavery, ' + enslavedTable539()
    elif rand == 11:
        rand = randint(1,8)
        if rand <= 4:
            tragedy1 = 'an accident'
        if rand == 5:
            tragedy1 = 'a terrible fire'
        if rand == 6:
            tragedy1 = 'an animal attack'
        if rand <= 8:
            tragedy1 = 'an attack by ' #750
        return 'character receives a severe injury due to ' + tragedy1
    elif rand == 12:
        rand = randint(1,2)
        if rand == 1:
            tragedy = 'father was killed by '
        elif rand == 2:
            tragedy = 'mother was killed by '
        rand = randint(1,3)
        if rand <= 2:
            return tragedy + 'an accident'
        elif rand == 3:
            return tragedy #750 and 545
    elif rand == 13:
        return 'character is banned from performing their profession and is cast out of guilds, their identity is known and they cannot continue to practice in the nearby vicinity'
    elif rand == 14:
        return 'if character has a lover, roll on this table' #I'll be elaborating on this once the basics of everything are written out
    elif rand == 15:
        return  'a disease almost kills the character and leaves horrible scars'
    elif rand == 16:
        return "war ravages the character's homeland, forcing them to join the military: " + militaryTable535(char)
    elif rand == 17:
        return "a fire destroys the character's home, along with all of their personal belongings"
    elif rand == 18:
        return "character is cursed " #868
    elif rand == 19:
        return "character's best friend dies"   #545
    elif rand == 20:
        preSuppose = "family estate destroyed by "
        rand = randint(1,6)
        if rand == 1:
            return preSuppose + ''
        elif rand <= 3:
            return preSuppose + 'a terrible fire'
        elif rand == 4:
            return preSuppose + 'an unexplainable accident'
        elif rand == 5:
            return preSuppose + 'war'
        elif rand == 6:
            return preSuppose + "someone's actions" #750
    elif rand == 21:
        return 'imprisoned for a crime the character did not commit, ' #875, #540
    elif rand == 22:
        return tragediesTable528() #reroll is supposed to be without char['solMod'], will fuck around with later
    elif rand == 23:
        return "character's family loses all wealth"
    elif rand == 24:
        return 'character is disinherited by parents'
    elif rand <= 26:
        return 'character is forced into an unwanted political marriage.'
    elif rand <= 28:
        return "a shift in economy causes severe inflation, causing wealth of character's family to drop to a tenth of what it was"
    elif rand <= 30:
        return tragediesTable528() #reroll is supposed to be without char['solMod'], will fuck around with later
    elif rand == 31:
        return "source of character or character's family's income is destroyed or lost"
    elif rand == 32:
        rand = randint(1,6)
        return "character's family is stripped of all titles and lands by the ruler of the land" + (("", ", the family is outlawed")[rand == 6])

def wonderfulTable529(char):
    rand = randint(1,20) + char['solMod']
    if rand <= -2:
        return "Wild beasts attack the character's camp. The character discovers they have the innate ability to command wild beasts."
    elif rand <= -1:
        return "The ruler pardons all prisoners of the land."
    elif rand <= 1:
        rand = randint(1,2)
        return "If the character has a lover or spouse, they are blessed with a beautiful, healthy " (("boy", "girl"), rand == 1) + "."
    elif rand <= 2:
        return "While repairing the family home, the character discovers a " + giftsTable863()
    elif rand <= 3:
        return "Character acquires a " #759
    elif rand <= 4:
        return "Character is adopted into a wealthy family, treated well."
    elif rand <= 5:
        return "The village the character lives in is destroyed, but is rebuilt and becomes more prosperous than ever."
    elif rand <= 6:
        return "The character is responsible for saving the life of " #750
    elif rand <= 9:
        return wonderfulTable529(0)
    elif rand <= 10:
        return "An evil lcoal ruler outlaws the character's parents. " + str(randint(1,10)) + " years later, the ruler's liege overthrows them. The character's parents are pardoned and honored with elevation to nobility due to their role in the ruler's demise."
    elif rand <= 11:
        return ""
    elif rand <= 12:
        return
    elif rand <= 14:
        return
    elif rand <= 16:
        return
    elif rand <= 18:
        return
    elif rand <= 19:
        return
    elif rand <= 20:
        return
    elif rand <= 21:
        return
    elif rand <= 23:
        return
    elif rand <= 25:
        return
    elif rand <= 27:
        return
    elif rand <= 29:
        return
    elif rand <= 32:
        return
    elif rand <= 33:
        return


#skipping race-specific events for now, which is 530-533

def underworldTable534():
    beginning = random_choice(underworldTable534a)
    crimeType = underworldTable534b()
    crimeEvent = underworldTable534c()

underworldTable534a = {
    'character needs money to pay debts': 1,
    'peer pressure forces the character to do criminal acts': 1,
    'character has a pathological urge to do wrong': 1,
    'character wants to defy authority': 1,
    "character wants to live a lifestyle they can't afford": 1,
    'character seeks a lifestyle filled with thrills and excitement': 1,
    'character seeks to wield power in the crime world': 1,
    'character is forced into a life of crime by cirminals who threaten their loved ones': 1
}

def underworldTable534b():
    rand = randint(1,6)
    if rand == 1:
        return 'petty theft'
    elif rand == 2:
        return 'organized guild thievery'
    elif rand == 3:
        return 'organized crime: ' #875
    elif rand == 4:
        rand = randint(1,9)
        preSuppose = 'independent criminal involved in '
        if rand == 1:
            second = 'prostitution'
        elif rand == 2:
            second = 'being a hired thug'
        elif rand == 3:
            second = 'burglary'
        elif rand == 4:
            second = 'smuggling'
        elif rand == 5:
            second = 'violating curfew'
        elif rand == 6:
            second = 'stealing livestock'
        elif rand == 7:
            second = 'selling drugs'
        elif rand == 8:
            second = 'robbing money lenders and stores'
        elif rand == 9:
            second = 'kidnapping'
        return preSuppose + second
    elif rand == 5:
        return 'piracy' #534d
    elif rand == 6:
        return 'banditry'

def underworldTable534c():
    rand = randint(1,20)
    if rand == 1:
        return 'join a gang'
    elif rand == 2:
        return 'jailed in a sweep of the streets by law enforcement'
    elif rand == 3:
        return 'seriously wounded in a fight' #870
    elif rand == 4:
        return 'character is a common criminal suspect regarding any crimes that happen in their town'
    elif rand == 5:
        rand = randint(1,6)
        return 'character becomes an informant for the law' + (("", ", labeled as a snitch, with a contract on their life")[rand == 6])
    elif rand == 6:
        return 'character participates in a jewel heist, only for their ' + str(randint(1,4)) + 'partners to disappear with the loot'
    elif rand == 7:
        return 'a key gang boss is slain and the character is blamed, members of the gang seek the death of the character'
    elif rand == 8:
        return 'character is imprisoned for a crime' #875
    elif rand == 9:
        return 'character becomes a proficient thief'
    elif rand == 10:
        return 'character goes straight, ending their life of crime. Still often recognized by criminals who remember the old days, though'
    elif rand == 11:
        return 'character develops extensive contacts in the underworld'
    elif rand == 12:
        return 'character learns the surrounding sewers like the back of their hand'
    elif rand == 13:
        return "character learns secret passages to a noble's estate"
    elif rand == 14:
        return 'character discovers that several items taken in a recent heist are cursed.' #863 and #868
    elif rand == 15:
        return "a crime lord becomes the character's patron, grooming them to a leader of organized crime"
    elif rand == 16:
        return "character's friends are killed off in horrible ways and law enforcement has no interest in stopping the killer. only the character and one friend survive."
    elif rand == 17:
        return "character discovers that a prominent government official is the head of a major crime ring"
    elif rand == 18:
        return "character's thieving skills improve considerably"
    elif rand == 19:
        return "character steals and hides a valuable gem, only to later find out it was stoled by one of the character's criminal 'friends'"
    elif rand == 20:
        return 'character becomes the leader of a gang'

def underworldTable534d():
    rand = randint(1,10)
    if rand == 1:
        return 'pirate captain buries treasure on a deserted island'
    elif rand == 2:
        return 'pirate crew is captured and all but the character are hanged'
    elif rand == 3:
        return 'character becomes adept at sailing a big ship'
    elif rand == 4:
        return 'pirate crew mutinies and the character is voted captain by the mutineers. The old captain vows revenge.'
    elif rand == 5:
        return 'pirates discover a lost island with a mysterious temple. All members of the crew are cursed by the magic of the temple, ' #868
    elif rand == 6:
        return 'an old salt teaches the character how to become an expert in wielding a cutlass'
    elif rand == 7:
        return 'a raid on a large treasure ship gives the character a lot of gold'
    elif rand == 8:
        return 'pirate captain is a woman known for taking vengeance on male captives.'
    elif rand == 9:
        return 'due to wide travel on the pirate ship, character becomes moderately skilled at ' + str(randint(1,6)+1) + ' languages.'
    elif rand == 10:
        return "character becomes oen of the captain's officers"

def militaryTable535(char):
    service = militaryTable535a(char)
    event = militaryTable535b(char, 0)
    rank = militaryRankTable538(char)
    return service, event, rank

def militaryTable535a(char):
    rand = randint(1,20)
    if char['culture'] == 'Primitive':
        if rand <= 12:
            return 'light infantry'
        elif rand <= 14:
            return 'medium infantry'
        elif rand <= 16:
            return 'archer'
        elif rand <= 18:
            return 'light cavalry'
        elif rand <= 20:
            return 'mercenary (' + militaryTable535a(char) + ')'
    elif char['culture'] == 'Civilized':
        if rand <= 1:
            return 'light infantry'
        elif rand <= 6:
            return 'medium infantry'
        elif rand <= 8:
            return 'heavy infantry'
        elif rand <= 10:
            return 'archer'
        elif rand <= 11:
            return 'chariots'
        elif rand <= 13:
            return 'light cavalry'
        elif rand <= 14:
            return 'heavy cavalry'
        elif rand <= 16:
            return 'mercenary (' + militaryTable535a(char) + ')'
        elif rand <= 18:
            return 'navy'
        elif rand <= 19:
            return 'special forces' #537 baybay
        elif rand <= 20:
            return 'noncombat duty' #536
    else: #nomad and barbarian use the same thing, soooooo
        if rand <= 3:
            return 'light infantry'
        elif rand <= 7:
            return 'medium infantry'
        elif rand <= 8:
            return 'archer'
        elif rand <= 10:
            return 'chariots'
        elif rand <= 15:
            return 'light cavalry'
        elif rand <= 17:
            return 'mercenary (' + militaryTable535a(char) + ')'
        elif rand <= 19:
            return 'navy'
        elif rand <= 20:
            return 'noncombat duty' #536

def militaryTable535b(char, modifier = None):
    if modifier is None:
        modifier = 0
    rand = randint(1,20) + modifier
    if rand <= 6: #battle rolls are fucking big
        preSuppose = 'Battle! '
        return preSuppose + militaryTable535bA(char)
    elif rand <= 8:
        return 'Character enlists for another tour of duty.'
    elif rand <= 9:
        return "Character's prowess and intelligence earn them reassignemnt to a special forces unit: " #537
    elif rand <= 10:
        return 'Character is transferred to a noncombat unit: ' #536
    elif rand <= 11:
        return 'Character is made an officer.'
    elif rand <= 12:
        rand = randint(1,5)
        if rand == 5:
            return "Character's unit is involved in " + str(randint(1,10)) + " skirmishes. One particular battle: " + militaryTable535bA()
        return "Character's unit is involved in " + str(randint(1,10)) + " skirmishes."
    elif rand <= 13:
        return "Character's unit is ambushed! " + militaryTable535bA(char, randint(1,4))
    elif rand <= 14:
        return "Character's unit is involved in a plot to overthrow the government. "
    elif rand <= 15:
        return "Character is reassigned to special forces: " #537
    elif rand <= 16:
        rand = randint(1,6)
        return "A disease ravages the army." + ("" if rand == 6 else " The character becomes sensitive to cold and damp.")
    elif rand <= 17:
        return "Character re-enlists for another hitch. " + militaryTable535b(char, 0)
    elif rand <= 18:
        return "Character learns to be proficient with a new weapon."
    elif rand <= 19:
        return "Character's hitch is extended by " + str(rand(1,4)) + " years due to a major war breaking out. " + militaryTable535b(char, 5)
    elif rand <= 21:
        return "A fierce war breaks out due to " + random_choice(militaryTable535bB) + ". Result of most important battle: " + militaryTable535bA(char)
    elif rand <= 23:
        return "Character increases their aptitude of their occupation."
    elif rand == 24:
        return "Character is assigned to accompany a military unit in the field. " + militaryTable535b(char, 0)
    elif rand == 25:
        return "In the service of " #543

def militaryTable535bA(char, modifier = 0):
    rand = randint(1,20) + modifier
    if rand <= 1:
        battleOccur = str(randint(1,100)) + "\% of the character's side was killed. They fought poorly and received an injury, " #870 also their military career could end
    elif rand <= 2:
        battleOccur = 'Serious casualties and the character was injured, being granted an impressive scar.'
    elif rand <= 3:
        battleOccur = 'The horror of battle causes the character to develop an exotic personality feature, ' #649
#   elif rand <= 5: skipping for now due to re-rolling
#       battleOccur = ''
    elif rand <= 7:
        battleOccur = 'Character sees action, but nothing noteworthy occurs.'
    elif rand <= 8:
        battleOccur = 'Character fought well, with many a foe dying by their hands.'
    elif rand <= 9:
        battleOccur = 'Character fought well and became known for their heroism. For this, they were promoted.'
    elif rand <= 10:
        battleOccur = 'Character is captured and enslaved: ' + enslavedTable539()
    elif rand <= 11:
        battleOccur = 'Character is decorated for heroism.'
    elif rand <= 12:
        battleOccur = 'Character was a coward in battle and, even though no one noticed, must live with their actions.'
    elif rand <= 13:
        battleOccur = "Character's best friend dies at their side."
    elif rand <= 14:
        battleOccur = 'Character is the only survivor of their unit.'
    elif rand <= 15:
        battleOccur = 'Character deserts during battle, revealing their cowardly side.'
    elif rand <= 16:
        battleOccur = 'Character is responsible for the deaths of ' + str(randint(1,10)) + ' of their comrades.'
    elif rand <= 17:
        battleOccur = 'Character slays the leader of the enemy.'
    elif rand <= 18:
        battleOccur = "Character's superior is slain and they assume command."
    elif rand <= 19:
        battleOccur = 'Regardless of battle performance, character is accused of dereliction of duty and is court-martialed.'
    elif rand <= 20:
        rand = randint(1,6)
        battleOccur = 'An act of the character reverses the outcome of the battle.' + (("", " They are recognized for it."), rand == 6)
    elif rand <= 21:
        battleOccur = "Victor's side suffers light casualties. " + militaryTable535b(0, char['culture'])
    elif rand <= 22:
        battleOccur = "Loser's side is utterly destroyed. " + militaryTable535b(0, char['culture'])
    return battleOccur

militaryTable535bB = {
    'armies from a neighboring land': 3,
    'armies of monsters': 1,
    'a civil war': 2,
    'a peasant rebellion': 1,
    'a war of succession': 1,
    'a holy war': 1,
    'monsters from another plane': 1
}

def noncombatTable536(char):
    rand = randint(1,20)
    if rand <= 3:
        return "A regular occupation, " + occupationsTable420(char)
    elif rand <= 5:
        return "Medical corps"
    elif rand == 6:
        return "Recruiter"
    elif rand == 7:
        return 'quartermaster corps'
    elif rand == 8:
        return 'Instructor'
    elif rand == 9:
        return 'Engineer'
    elif rand == 10:
        return 'Messenger'
    elif rand == 11:
        return 'Cook'
    elif rand == 12:
        return 'Embassy guard'
    elif rand == 13:
        return 'Mage guard'
    elif rand == 14:
        return 'Prison guard'
    elif rand == 15:
        return 'Payroll guard'
    elif rand == 16:
        return 'City guard'
    elif rand == 17:
        return 'Private body guard to leader'
    elif rand == 18:
        return 'Palace guard'
    elif rand == 19:
        return 'Temple guard'
    elif rand == 20:
        return 'border guard'

specialForcesTable537 = {
    'ranger': 2,
    'scout': 2,
    'monster squad': 1,
    'marine': 2,
    'suicide squad': 1,
    'war machine': 1,
    'espionage': 1
}

def militaryRankTable538(char):
    rand = randint(1,6) + char['solMod']
    if rand <= 10:
        return "Soldier"
    elif rand <= 12:
        return 'Corporal'
    elif rand <= 15:
        return 'Sargeant'
    elif rand <= 16:
        return 'Second Lieutenant'
    elif rand <= 18:
        return 'First Lieutenant'
    elif rand <= 20:
        return 'Captain'
    elif rand <= 24:
        return 'Major'
    elif rand <= 25:
        return "Colonel"

def enslavedTable539():
    rand = randint(1,20)
    if rand <= 1: # Escape situation
        rand = randint(1,8)
        if rand == 1:
            return 'character escaped slavery, a reward of ' + str(randint(1,10)*100) + ' gold is offered for their capture'
        elif rand == 2:
            return str(randint(1,6)) + ' slaves accompanied the character in their escape from slavery'
        elif rand == 3:
            return 'the government is offering a bounty on the escaped slave'
        elif rand == 4:
            return "the owner's " + random_choice(relativesTable753) + "helped the character escape from slavery"
        elif rand == 5:
            return 'while escaping from slavery, the character killed their owner'
        elif rand == 6:
            return 'while escaping slavery, the character stole ' + giftsTable863()
        elif rand == 7:
            return 'the character, owned by a slaverunner, was set free by the owner who is in love with them'
        elif rand == 8:
            return 're-roll on table shit, ugh.'
    elif rand <= 2:
        #owner decides to free character
        rand = randint(1,10)
        if rand == 1:
            rand = randint(1,8)
            if rand <= 4:
                return 'character is freed from slavery by owner, who is a good friend'
            elif rand <= 7:
                return "character is freed from slavery by owner, who becomes the character's patron" # table 543 here
            elif rand <= 8:
                return "character is freed from slavery by owner, who becomes the character's companion" # table 761 here
        elif rand <= 2:
            return 'character is freed from slavery by owner due to religious conversion, character is paid ' + str(randint(2,20)) + ' gold coins in reparations'
        elif rand <= 4:
            return 'character is reunired with relatives after being freed from slavery'
        elif rand <= 5:
            return 'owner dies and their will specifies that slaves are to be freed'
        elif rand <= 7:
            return ' the slave is unable to be used for work and enlists in the military' #go to table 535
        elif rand <= 8:
            return 'the character escapes slavery with the help of another, who becomes their companion' #go to table 863
        elif rand <= 9:
            return "while in slavery, the character saves their owner's life. the owner gives the character their freedom and " + giftsTable863
        elif rand <= 10:
            return '3x re-roll, will set up later'
    elif rand <= 3:
        return 'the ruler of the land declares slavery illegal and the player is given ' + str(randint(1,100)) + ' gold as reparations'
    elif rand <= 4:
        return 'the character is freed of slavery by saving money and buying their own freedom'
    elif rand <= 5:
        return 'owner dies'
        #there will be a bunch more rolls here
    elif rand <= 7:
        return 'character improves their occupational skill rating by one while in slavery'
    elif rand <= 8:
        return 'character improves their occupational skill rating by ' + str(randint(2,4)) + ' while in slavery'
    elif rand <= 9:
        return 'while in slavery, the character is often beaten by their owner'
    elif rand <= 10:
        return 'character learns an additional skill at rank 1 while enslaved'
    elif rand <= 11:
        return 'as a slave, the character is a sexual plaything of the owner and has no other duties.'
    elif rand <= 12:
        return 'character participates in a slave revolt'
        #more rolls will go here
    elif rand <= 13:
        return 'while enslaved, a character is promoted to a position of authority'
    elif rand <= 14:
        return "while enslaved, the character is the owner's favorite and becomes the senior slave. one of the other slaves becomes the character's rival" #roll table 762 here
    elif rand <= 15:
        return 'character is used as breeding stock. if male, produces ' + str(randint(1,10)) + ' kids per year. if female, one per year'
    elif rand <= 16:
        return 'character is resold ' + str(randint(1,3)) + ' times during their enslavement'
    elif rand <= 17:
        return 'character is branded on their ' + bodyLocationTable867
    elif rand <= 18:
        return 'the character attempts to escape from slavery, fails, and is branded on their ' + bodyLocationTable867 + '. they are also beaten more often'
    elif rand <= 20:
        return 'an exotic event occurs that causes the character to be freed' #roll on table 544 here

def DarksideTraitsTable648():
    rand=randint(2,40)
    if rand == 2:
       return "pessimist"
    elif rand == 3:
        return "egoist"
    elif rand == 4:
        return "obstructive"
    elif rand == 5:
        return "cruel"
    elif rand == 6:
        return "careless"
    elif rand == 7:
        return "thoughtless"
    elif rand == 8:
        return "flippant"
    elif rand == 9:
        return "drunkard"
    elif rand == 10:
        return "suspicious"
    elif rand == 11:
        return "violent"
    elif rand == 12:
        return "argumentative"
    elif rand == 13:
        return "irreverent"
    elif rand == 14:
        return "cheat"
    elif rand == 15:
        return "hateful"
    elif rand == 16:
        return "selfish"
    elif rand == 17:
        return "slovenly"
    elif rand == 18:
        return "filthy"
    elif rand == 19:
        return "tardy"
    elif rand == 20:
        return "self-doubting"
    elif rand == 21:
        return "cowardly"
    elif rand == 22:
        return "disrespectful"
    elif rand == 23:
        return "angry"
    elif rand == 24:
        return "impatient"
    elif rand == 25:
        return "foolish"
    elif rand == 26:
        return "greedy"
    elif rand == 27:
        return "dull"
    elif rand == 28:
        return "vengeful"
    elif rand == 29:
        return "immoral"
    elif rand == 30:
        return "untrustworthy"
    elif rand == 31:
        return "rude"
    elif rand == 32:
        return "harsh"
    elif rand == 33:
        return "unfriendly"
    elif rand == 34:
        return "egotistic"
    elif rand == 35:
        return "lazy"
    elif rand == 36:
        return "liar"
    elif rand == 37:
        return "morose"
    elif rand == 38:
        return "unenthuastic"
    elif rand == 39:
        return "spendthrift"
    elif rand == 40:
        return "tactless"

nonhumansTable751 = {
    'elf': 4,
    'dwarf': 3,
    'halfling': 3,
    'half elf': 4,
    'beastman': 1,
    'reptileman': 1,
    'orc': 1,
    'half orc': 2
}

relativesTable753 = {
    'first cousin': 1,
    'second cousin': 1,
    'distant cousin': 1,
    'son': 1,
    'daughter': 1,
    'sister': 1,
    'brother': 1,
    'spouse': 1,
    'aunt': 1,
    'uncle': 1,
    'great aunt': 1,
    'great uncle': 1,
    'mother': 1,
    'father': 1,
    'grandmother': 1,
    'grandfather': 1,
    'great grandmother': 1,
    'great grandfather': 1,
    'descendent': 1,
    'unknown relation': 1
}

def guardiansTable754(char):
    rand = randint(1,20)
    rand = 10
    if rand <= 5:
        return random_choice(relativesTable753)
    elif rand <= 8:
        return 'raised in an orphanage'
    elif rand <= 10:
        return familyTable106a(char)
    elif rand <= 11:
        return 'raised by priests or monks of ' + deitiesTable864(char)
    elif rand <= 12:
        return 'raised by ' + random_choice(nonhumansTable751)
    elif rand <= 13:
        return 'sold into slavery ' + enslavedTable539()
    elif rand <= 14:
        return 'raised on the street by beggars and prostitutes'
    elif rand <= 15:
        return "raised by a thieves' guild" #table534 here
    elif rand <= 16:
        return 'raised by different relatives, passed between them until coming of age'
    elif rand <= 17:
        return 'raised by an adventurer: ' #table757
    elif rand <= 18:
        return 'character mysteriously disappeared for ' + str(randint(1,10)) + ' years'
    elif rand <= 19:
        return 'raised by beasts in the wild'
    elif rand <= 20:
        return 'raised by ' #table 756

criminalTable755 = {
    'murderer': 1,
    'kidnapper': 2,
    'thief': 3,
    'pickpocket': 4,
    'extortionist': 5,
    'con man': 6,
    'armed robber': 7,
    'highwayman': 8,
    'gang bandit': 9,
    'professional assassin': 10,
    'drug dealer': 11,
    'mugger': 12,
    'horse thief': 13,
    'rustler': 14,
    'thug': 15,
    'pimp': 16,
    'prostitute': 17,
    'gang leader': 18,
    'rapist': 19,
    'pirate': 20
}

nobleTable758prim = {
    'high king': 1,
    'chieftain': 29,
    'subchieftain': 70
}

nobleTable758nomad = {
    'kahn': 10,
    'chieftain': 30,
    'subchieftain': 40,
    'hetman': 20
}

nobleTable758barb = {
    'high king': 2,
    'king': 13,
    'prince(ss)': 10,
    'chieftain': 20,
    'jarl': 15,
    'subchieftain': 10,
    'baron': 5,
    'prince(ss) (royal)': 5,
    'hetman': 20
}

nobleTable758civil = {
    'emperor': 1,
    'king': 4,
    'prince(ss) (royal)': 10,
    'archduke': 5,
    'duke': 5,
    'marquis': 10,
    'viscount': 15,
    'count': 10,
    'baron': 15,
    'lord': 3,
    'prince(ss)': 12,
    'knight': 10
}

def nobleTable758titleMod(char):
    if char['title'] == 'hetman':
        return randint(1,6)
    elif char['title'] == 'knight':
        return randint(2,12)
    elif char['title'] == 'prince(ss)':
        return randint(4,40)
    elif char['title'] == 'lord':
        return randint(2,16)
    elif char['title'] == 'baron':
        return randint(2,20)
    elif char['title'] == 'count':
        return randint(3,18)
    elif char['title'] == 'subchieftain':
        return randint(2,12)
    elif char['title'] == 'jarl':
        return randint(3,18)
    elif char['title'] == 'viscount':
        return randint(3,24)
    elif char['title'] == 'chieftain':
        return randint(3,18)
    elif char['title'] == 'marquis':
        return randint(3,30)
    elif char['title'] == 'duke':
        return randint(4,32)
    elif char['title'] == 'archduke':
        return randint(4,40)
    elif char['title'] == 'prince(ss) (royal)':
        return randint(4,40)
    elif char['title'] == 'kahn':
        return randint(5,40)
    elif char['title'] == 'king':
        return 39
    elif char['title'] == 'high king':
        return randint(5,50)
    elif char['title'] == 'emperor':
        return 60
    else:
        raise ValueError("\nnobleTable758titleMod isn't getting a char['title'] pushed to it.")

def unusualPetsTable759():
    rand = randint(1,20)
    if rand <= 2:
        petType = 'dog'
    elif rand <= 4:
        petType = 'cat'
    elif rand <= 5:
        petType = 'rabbit'
    elif rand <= 6:
        petType = 'lizard'
    elif rand <= 7:
        petType = 'monkey'
    elif rand <= 8:
        petType = 'raccoon'
    elif rand <= 9:
        petType = 'rat'
    elif rand <= 10:
        petType = 'snake'
    elif rand <= 11:
        petType = 'hawk'
    elif rand <= 12:
        petType = 'mouse'
    elif rand <= 13:
        petType = 'ferret'
    elif rand <= 14:
        petType = 'songbird'
    elif rand <= 15:
        rand = randint(1,3)
        if rand == 3:
            petType = 'fish (that can survive out of water)'
        else:
            petType = 'fish'
    elif rand <= 16:
        petType = 'puppy'
    elif rand <= 17:
        petType = 'mini-dragon'
    elif rand <= 18:
        petType = 'big cat'
    elif rand <= 19:
        petType = 'baby bear that stays a baby'
    elif rand <= 20:
        petType = 'something alien'
    petAbility = specialPetAbilitiesTable760()
    return petType + ' (' + petAbility + ')'

def specialPetAbilitiesTable760():
    rand = randint(1,20)
    if rand <= 1:
        return 'has wings'
    elif rand <= 2:
        return 'very intelligent'
    elif rand <= 3:
        return 'telepathic'
    elif rand <= 4:
        return 'unusual color: ' + colorsTable865
    elif rand <= 5:
        rand = randint(1,10)
        return 'pet is made of odd substance'
    elif rand <= 6:
        return 'pet has physical affliction ' #table874 here
    elif rand <= 7:
        return 'pet can use magic spells'
    elif rand <= 8:
        return 'pet is invisible to all but owner'
    elif rand <= 9:
        return 'pet regenerates damage done to it'
    elif rand <= 10:
        return 'when killed, pet will possess nearest animal'
    elif rand <= 11:
        rand = randint(1,2)
        if rand == 1:
            return 'pet is unusually large'
        else:
            return 'pet is unusually small'
    elif rand <= 12:
        return 'once per day, pet may assume attractive human form for ' + str(randint(1,6)) + ' hours'
    elif rand <= 13:
        return 'draws magical power from its master'
    elif rand <= 14:
        return 'supplies magical power to master'
    elif rand <= 15:
        return "pet's life is added to character's own as long as the pet lives"
    elif rand <= 16:
        return 'breathes fire'
    elif rand <= 17:
        return 'can increase its size and strength ' + str(randint(1,10)) + ' times their normal amount once per day for ' + str(randint(1,6)) + ' hours'
    elif rand <= 18:
        return 'can provide master with ' + str(randint(1,6)) + ' gold per day'
    elif rand <= 19:
        return 'can turn into mist at will'
    elif rand <= 20:
        return 'reroll shit'

def companionTable761():
    companionWho = companionTable761a()
    companionWhy = companionTable761b()
    companionPersonality = companionTable761c()
    return companionWho + ', because ' + companionWhy + ', personality: ' + companionPersonality

def companionTable761a():
    rand = randint(1,9) #easily able to add 10 to this for the re-roll once everything is set up
    if rand == 1:
        return 'childhood friend'
    elif rand == 2:
        return 'a family member, ' + random_choice(relativesTable753)
    elif rand == 3:
        return 'a nonhuman, ' + random_choice(nonhumansTable751)
    elif rand == 4:
        return 'a stranger, ' #table 750 go hurr
    elif rand == 5:
        return 'an intelligent, articulate inanimate object'
    elif rand == 6:
        return 'a kid aged ' + str(randint(7,13))
    elif rand == 7:
        rand = randint(1,2)
        if rand == 1:
            return 'an older sibling'
        else:
            return 'a younger sibling'
    elif rand == 8:
        return 'an adventurer, ' #table 757
    elif rand == 9:
        return 'a former enemy or rival, ' #table 762 go hurr
    #elif rand == 10:

def companionTable761b():
    rand = randint(1,9)
    if rand == 1:
        return 'character saved their life'
    elif rand == 2:
        return 'they seek a similar goal, are friendly rivals'
    elif rand == 3:
        return 'parents were companions in adventure'
    elif rand == 4:
        return 'they share the same enemy'
    elif rand == 5:
        return 'they were in the same place and in trouble at the same time'
    elif rand == 6:
        return 'the companion imagines the character a hero and wants to learn from them'
    elif rand == 7:
        return "the companion's original intent was to steal from the character"
    elif rand == 8:
        return 'companion feels a need to protect the character'
    elif rand == 9:
        return 'mysterious voices and feelings told the companion to seek out the character and join them'

def companionTable761c():
    rand = randint(1,10)
    if rand <= 3:
        return 'loyal friend'
    elif rand <= 5:
        return 'bumbling buffoon'
    elif rand <= 6:
        return 'grim, quiet ally'
    elif rand <= 7:
        return 'enthusiastic leader-type'
    elif rand <= 8:
        return 'a wise-cracking smart mouth who complains'
    elif rand <= 9:
        return 'rowdy fighter'
    elif rand <= 10:
        return 'incurable romantic'

def giftsTable863():
    rand = randint(1,20)
    if rand <= 1:
        return random_choice(giftsTable863a)
    elif rand <= 2:
        return 'guardianship of a young ward. Use table 761'
    elif rand <= 3:
        return 'unusual pet. Use table 760'
    elif rand <= 4:
        return random_choice(giftsTable863b)
    elif rand <= 5:
        return 'a tapestry'
    elif rand <= 6:
        return 'an anachronistic device'
    elif rand <= 7:
        return 'a key'
    elif rand <= 8:
        return 'a locked or sealed book'
    elif rand <= 9:
        return 'a shield'
    elif rand <= 10:
        return 'a sealed bottle'
    elif rand <= 11:
        return 'a tarnished old helmet'
    elif rand <= 12:
        return 'a bound wooden staff'
    elif rand <= 13:
        return 'a riding animal'
    elif rand <= 14:
        return 'a deed to ' + random_choice(giftsTable863c)
    elif rand <= 15:
        return 'a musical instrument'
    elif rand <= 16:
        return random_choice(giftsTable863d)
    elif rand <= 17:
        return 'a pouch of papers containing ' + random_choice(giftsTable863e)
    elif rand <= 18:
        return 'a sealed trunk'
    elif rand <= 19:
        return 'a chainmail hauberk'
    elif rand <= 20:
        return 'roll again shenanigans'

giftsTable863a = {
    'an ornate dagger': 1,
    'an ornate sword': 1,
    'a plain sword': 1,
    'a mace': 1,
    'an ornate spear': 1,
    'a well-made bow': 1,
    'an ornate battle axe': 1,
    'an exotic weapon': 1,
}

giftsTable863b = {
    'amulet': 1,
    'necklace': 1,
    'earrings': 1,
    'tiara': 1,
    'torc': 1,
    'arm band': 1,
    'ring': 1,
    'pin or brooch': 1,
}

giftsTable863c = {
    'a tract of land': 1,
    'an ancient castle': 1,
    'a country manor': 1,
    'an elegant town house': 1,
    'a temple': 1,
    'a factory': 1,
    'ancient ruins': 1,
    'an inn': 1,
    'an apartment building': 1,
}

giftsTable863d = {
    'a hat': 1,
    'a pair of shoes': 1,
    'a belt': 1,
    'a cape': 1,
    'a tunic': 1,
    'trousers': 1,
    'a pair of stockings': 1
}

giftsTable863e = {
    "an ancient ancestor's letter to his descendents": 1,
    'a map': 1,
    'an undelivered letter': 1,
    'diagrams and plans for a mysterious invention': 1,
    'a scroll of magic spells': 1,
    'a wild story of adventure': 1,
    'a last will and testament determining that the character is an heir': 1,
    'a treasure map': 1,
    "the character's true family history": 1
}

def deitiesTable864(char):
    rand = randint(1,20) + char['cuMod']
    if rand <= 1:
        return 'ancestor worship'
    elif rand <= 2:
        return 'beast gods'
    elif rand <= 3:
        return 'hunting god'
    elif rand <= 4:
        return 'trickster'
    elif rand <= 5:
        return 'earth goddess'
    elif rand <= 6:
        return 'agricultural goddess'
    elif rand <= 8:
        return 'agricultural goddess'
    elif rand <= 10:
        return 'ruling deity'
    elif rand <= 11:
        return 'sea god'
    elif rand <= 12:
        return 'sun god'
    elif rand <= 13:
        return 'moon goddess'
    elif rand <= 14:
        return 'storm god'
    elif rand <= 15:
        return 'evil god'
    elif rand <= 16:
        return 'war god'
    elif rand <= 17:
        return 'love goddess'
    elif rand <= 18:
        return 'underworld god'
    elif rand <= 19:
        return 'god of wisdom'
    elif rand <= 20:
        return 'healing god'
    elif rand <= 21:
        return 'trade god'
    elif rand <= 22:
        return 'luck goddess'
    elif rand <= 23:
        return 'night goddess'
    elif rand <= 24:
        return 'god of thieves'
    elif rand <= 27:
        return 'decadent god'
    else:
        raise ValueError("I done fucked up on the deitiesTable864")

colorsTable865 = {
    'red': 1,
    'red orange': 1,
    'orange': 1,
    'yellow orange': 1,
    'yellow': 1,
    'yellow-green': 1,
    'green': 1,
    'blue-green': 1,
    'blue': 1,
    'blue-violet': 1,
    'violet': 1,
    'red violet': 1,
    'pink': 1,
    'white': 1,
    'black': 1,
    'gray': 1,
    'maroon': 1,
    'silver': 1,
    'gold': 1,
    'reroll': 1
}

birthmarksTable866 = {
    'dragon': 1,
    'skull': 1,
    'bat': 1,
    'sword': 1,
    'hand': 1,
    'crescent moon': 1,
    'claw': 1,
    'eagle': 1,
    'fish': 1,
    'a random animal': 1
}

bodyLocationTable867 = {
    'right foot': 1,
    'left foot': 1,
    'right leg': 1,
    'left leg': 1,
    'abdomen': 2,
    'buttocks': 2,
    'back': 1,
    'chest': 4,
    'right arm': 1,
    'left arm': 1,
    'right hand': 1,
    'left hand': 1,
    'head': 1,
    'face': 2
}

'''
This is an easy copy/paste for creating dicts:
Table = {
    '': ,
    '': ,
    '': ,
    '': ,
    '': ,
    '': ,
    '': ,
    '':
}
'''
