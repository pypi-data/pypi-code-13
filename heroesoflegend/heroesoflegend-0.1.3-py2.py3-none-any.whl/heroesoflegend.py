#! python3
import random
from random import randint
from rolltables import *

# This is the random choice initializer functions

char = {
    'race': 'human', #charRace
    'culture': 'primitive', #charCulture
    'cuMod': 0,
    'tiMod': 0,
    'social': 0, #charSocial
    'adopted': False, #charAdopted
    'solMod': 0,
    'legitBirth': True,
    'biMod': 0,
    'title': ''
}

def charGen():
    char['race'] = random_choice(raceTable101)
    if char['race'] == 'other races':
        char['race'] = random_choice(raceTable101a)
    char['culture'] = random_choice(cultureTable102)
    char['cuMod'] = cultureTable102a(char)
    char['social'], char['solMod'], char['title'], char['tiMod'] = socialTable103(char)
    char['legitBirth'] = birthTable104(char)
    if char['legitBirth'] == False:
        if char['cuMod'] >= 0:
            char['cuMod'] = char['cuMod'] - randint(1,4)
        illegitReason = illegitBirthTable105(char)
        illegitBirth = 'Birth was illegitimate. Cause: ' + illegitReason + '.'
    charFamily, char['adopted'] = familyTable106(char)
    if char['adopted'] == True:
        charFamily = '(adopted) ' + str(charFamily)
    siblingMale, siblingFemale, birthOrder = siblingsTable107()
    birthSeason, birthTimeOfDay = birthTimeTable109()
    placeOfBirth, char['biMod'] = placeOfBirthTable110(char)
    birthOccurance, unusualBirth = unusualBirthTable112(char)
    if unusualBirth == True:
        birthOccurance = ", ".join(birthOccurance)
    #shit about parents go hurr
    hohOccupation = parentTable114a(char)
    childhoodEvents, adolescentEvents = childhoodEventsTable215a(char)
    childhoodEvents = capitalize_shit(childhoodEvents)
    adolescentEvents = capitalize_shit(adolescentEvents)
    childhoodEvents = " | ".join(childhoodEvents)
    adolescentEvents = " | ".join(adolescentEvents)
    adulthoodEvents = adulthoodSignificantEventsTable217(char)
    adulthoodEvents = capitalize_shit(adulthoodEvents)
    adulthoodEvents = " | ".join(adulthoodEvents)
    return('Race: ' + char['race'] + ' | Culture: ' + char['culture'] + ' | Social Standing: ' + char['social'] + ((' | Title: ', "")[char['title'] == ""]) + char['title'] + "\nFamily: " + str(charFamily) + '.\n' +
    'Birth: In ' + birthSeason + ' at ' + birthTimeOfDay + ' ' + placeOfBirth + '.' +
    ('Birth Circumstances: ' + birthOccurance.capitalize() if unusualBirth == True else '' ) + (illegitBirth if char['legitBirth'] == False else '') + '\n' +
    'Siblings: ' + ('None' if siblingMale == 'none' else str(siblingMale) + ' male' + (('s', '')[siblingMale == 1]) + ' and ' + str(siblingFemale) + ' female' + (('s', '')[siblingFemale == 1]) + ', of which the character is the ' + birthOrder + '.') + '\n' +
    'Parents Info: ' + hohOccupation + '\n' +
    'Childhood: ' + childhoodEvents + "\n" +
    'Adolescence: ' + adolescentEvents + '\n' +
    'Adulthood: ' + adulthoodEvents
    )

def main():
    print(charGen())

def capitalize_shit(array): #I don't feel like re-writing everything from lower-case in the rolltables, so fuck it. Here.
    for i in range(len(array)):
        array[i] = array[i].capitalize()
    return array

if __name__ == "__main__":
    main()
