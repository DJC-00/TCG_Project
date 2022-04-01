from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import random
import math

class TCGCard:
    def __init__(self, inputName = ''):
        self.name = TCGCard.nameGen(self, inputName)
        self.attack = TCGCard.get_stats()
        self.defense = TCGCard.get_stats()
        self.speed = TCGCard.get_stats()
        self.luck = TCGCard.get_stats()
        self.rarity = TCGCard.get_rarity(self)
        self.specMove = getMove(self.rarity)

        

    def __str__(self):
        return(f"""{self.name}\n{self.rarity}\nAttack: {self.attack} Defense: {self.defense} Speed: {self.speed} Luck: {self.luck}\nSpecial Attack: {self.specMove}""")

    def get_stats():
        random.seed()
        randSum = 0
        for i in range(0,2):
            randNum = random.random()
            randSum += randNum
        finalSum = round(randSum*5,1)
        return finalSum

    def get_rarity(self):
        statAvg = ((self.attack+self.defense+self.speed+self.luck)/4)
        if statAvg == 10:
            return ("Masterpiece")
        elif statAvg > 8:
            return ("Legendary")
        elif statAvg > 7:
            return ("Rare")
        elif statAvg > 4:
            return ("Uncommon")
        else:
            return ("Common")

    def nameGen(self, inputName):
        random.seed()
        name = inputName
        title = ''
        if random.random() < 0.5 and name == '':
            name = getName(titlePlusName)
            name[0].upper()
            return name

        if name == '': 
            name = getName(names)
        name = name.title()

        title = getName(titles)
        title = title.title()

        if "the" in title or "The" in title or "of" in title or "Of" in title:
            return (name + ", " + title)
        else:
            return (title + " " + name)
            # return (name + ", " + title)

        return name

    def getBg():
        num = math.ceil(random.random()*5)
        return num

titles = ["https://www.fantasynamegenerators.com/banshee-names.php", "https://www.fantasynamegenerators.com/killer-names.php", "https://www.fantasynamegenerators.com/monster-names.php", "https://www.fantasynamegenerators.com/world-destroyer-names.php", "https://www.fantasynamegenerators.com/world-defender-names.php", "https://www.fantasynamegenerators.com/villain_names.php"]

names = ["https://www.fantasynamegenerators.com/bounty-hunter-names.php", "https://www.fantasynamegenerators.com/angel_names.php", "https://www.fantasynamegenerators.com/barbarian-names.php", "https://www.fantasynamegenerators.com/cyberpunk-names.php", "https://www.fantasynamegenerators.com/death-worm-names.php", "https://www.fantasynamegenerators.com/demon_names.php", "https://www.fantasynamegenerators.com/futuristic-names.php", "https://www.fantasynamegenerators.com/giant-names.php", "https://www.fantasynamegenerators.com/legendary-creature-names.php", "https://www.fantasynamegenerators.com/magic-user-names.php"]

titlePlusName = ["https://www.fantasynamegenerators.com/bandit-names.php", "https://www.fantasynamegenerators.com/code-names.php", "https://www.fantasynamegenerators.com/evil_names.php", "https://www.fantasynamegenerators.com/god-names.php", "https://www.fantasynamegenerators.com/guardian-names.php", "https://www.fantasynamegenerators.com/mad-scientist-names.php", "https://www.fantasynamegenerators.com/mecha-names.php", "https://www.fantasynamegenerators.com/pirate-names.php", "https://www.fantasynamegenerators.com/steampunk-names.php", "https://www.fantasynamegenerators.com/hero_names.php"]

allNameArrays = [titles,names,titlePlusName]

def getName(urlList):
    names = ""
    driver = webdriver.Chrome(ChromeDriverManager().install())
    url_list = urlList
    url = random.choice(url_list)
    driver.get(url)
    driver.implicitly_wait(10)
    buttons = driver.find_element(By.ID,"nameGen").get_attribute("innerHTML")
    buttonsElements = driver.find_element(By.ID,"nameGen")
    buttonsElements = buttonsElements.find_elements(By.TAG_NAME,"input")

    if len(buttonsElements) <= 1 or urlList == titles:
        buttonsElements[0].click()
    else:
        buttonSelect = random.randint(0, len(buttonsElements)-1)
        buttonsElements[buttonSelect].click()

    names += driver.find_element(By.ID, "result").get_attribute("innerHTML")

    driver.quit()
    time.sleep(10)

    name_list = names.split("<br>")
    name_list.pop()
    finalName = random.choice(name_list)

    return finalName


def getMove(rarity):
    moves = ""
    driver = webdriver.Chrome(ChromeDriverManager().install())
    url_list = ["https://www.fantasynamegenerators.com/anime-attack-names.php","https://www.fantasynamegenerators.com/attack-move-names.php","https://www.fantasynamegenerators.com/weapon-abilities.php","https://www.fantasynamegenerators.com/spell-names.php","https://www.fantasynamegenerators.com/naruto-jutsu-names.php","https://www.fantasynamegenerators.com/wrestling-move-names.php"]
    url = random.choice(url_list)
    driver.get(url)
    driver.implicitly_wait(10)
    buttons = driver.find_element(By.ID,"nameGen").get_attribute("innerHTML")
    buttonsElements = driver.find_element(By.ID,"nameGen")
    buttonsElements = buttonsElements.find_elements(By.TAG_NAME,"input")
    buttonsElements[0].click()
    moves += driver.find_element(By.ID, "result").get_attribute("innerHTML")
    driver.quit()
    time.sleep(10)

    name_list = moves.split("<br>")
    name_list.pop()
    finalMove = random.choice(name_list)

    return finalMove










#-_-_-_-_-_-_-_-_-_-_-_-_- Testing -_-_-_-_-_-_-_-_-_-_-_-_-


# friendList = ["Aaron","Kayla","Walter","Danny","Geoff","Deryk","Shashank","Amelia","John","DJ"]

# for friend in friendList:
# print("|---------------------------|")
# print(TCGCard())
# print("|___________________________|")
# print("|---------------------------|")
# print(TCGCard(friend))
# print("|___________________________|")

# cardList = []
# for i in range(0,5):
#     myCard = TCGCard()
#     cardList.append(myCard)

# for i in range(len(cardList)):
#     print("___________________")
#     print(cardList[i])