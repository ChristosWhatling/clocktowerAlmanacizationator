from mediawiki import MediaWiki
from bs4 import BeautifulSoup
import json
import subprocess

# VARIABLE DEFINITIONS
emptyList = []
characters = []
preCharacterLaTeX = "\\documentclass{article}\n\\usepackage[margin=0.5in]{geometry}\n\\usepackage{multicol,lipsum,graphicx,float,ragged2e,mdframed}\n\\usepackage[utf8]{inputenc}\n\\usepackage{textcomp}\n\\usepackage{pifont}\n\\usepackage{CJKutf8}\n\\setlength{\\parindent}{0pt}\n\\tolerance=1\n\\emergencystretch=\\maxdimen\n\\hyphenpenalty=10000\n\\hbadness=10000\n\\setcounter{tocdepth}{2}\n\n\\title{Blood on the Clocktower}\n\\author{Full character almanac}\n\\date{last updated 27-12-2025}\n\\begin{document}\n\\maketitle\n\\begin{multicols}{2}\n\\tableofcontents\n\\end{multicols}\n\\clearpage\n\n"
postCharacterLaTeX = "\\end{document}"

# FUNCTION DEFINITIONS

def splitIntoPoints(text):
    temp = text.split('\n');
    for i in range(len(temp)):
        temp[i] = "- " + temp[i].strip()
    temp[:] = [x for x in temp if len(x) > 2] # empty strings resolve as false -> you can easily filter them out by checking "if {string}"
    return temp

def fetchCharacter(characterName):
    p = botcWiki.page(characterName)
    soup = BeautifulSoup(p.html, "html.parser")
    testCharacter = clocktowerCharacter(characterName, soup)
    return testCharacter

def fixAmpersands(input):
    return input.replace("&amp;", "\\&").replace(" & ", " \\& ")

def boldFullyCapitalisedWords(input):
    words = input.split(" ")
    output, trailingComma, boldOpen = "", "", False
    for word in words:
        if word[-1:] == ",":
            trailingComma = word[-1:]
            tempWord = word[:-1]
        else:
            trailingComma = ""
            tempWord = word
        
        if isUpperOrDecimal(tempWord) and not boldOpen:
            output += "\\textbf{" + tempWord + trailingComma + " "
            boldOpen = True
        elif isUpperOrDecimal(tempWord):
            output += tempWord + trailingComma + " "
        elif boldOpen:
            output += "}" + tempWord + trailingComma + " "
            boldOpen = False
        else:
            output += tempWord + trailingComma + " "
    if boldOpen:
        output += "}"
    return output.replace(", }", "}, ").replace(" }", "} ")

def isUpperOrDecimal(input):
    return input.isupper() or input.isdecimal()

def fixCharacterLinks(input):
    if '<a href="/' in input:
        print("Character link deletion triggered!")
        pre = input.split('<a href="/')[0]
        name = input.split('<a href="/')[1].split('"')[0]
        post = input.split('</span></a>')[1]
        return pre + name + post
    return input

# CLASS DEFINITIONS

class clocktowerCharacter:
    def __init__(self, name: str, wikiText: BeautifulSoup):
        self.name = name            # Page title (e.g., "Imp")
        self.wikiText = wikiText    # Original wiki text
        self.cType, self.ability, self.flavour, self.artist, self.summary, self.url, self.cleanedWikiText, self.iconName, self.designer = "", "", "", "", "", "", "", "", ""
        self.summaryPoints, self.howToRunPoints, self.examplePoints = [], [], []
        
    def infodump(self):
        print("====================")
        print(self.name + " {" + self.cType + "} - " + self.ability)
        print("")
        print('"' + self.flavour + '"')
        print("")
        print(self.summary)
        for point in self.summaryPoints:   
            print(point)
        print("")
        print("[How to Run]")
        for point in self.howToRunPoints:   
            print(point)
        print("")
        print("[Examples]")
        for point in self.examplePoints:   
            print(point)
        print("")
        print("Designed by The Pandemonium Institute. Icon by " + self.artist + ".")
        print("====================")
        
    def parseWikiText(self):
        failCount = 0
        self.cleanedWikiText = self.wikiText.getText()
        self.iconName = "icons/Icon_" + self.name.lower().replace(" ", "").replace("'", "").replace("-", "") + ".png"
        self.designer = "The Pandemonium Institute"
        try: self.cType = str(self.wikiText.find_all("td")[1]).split('title="Character Types">')[1].split('<')[0]
        except:
            self.cType = "Unknown type"
            failCount += 1
        try: self.ability = str(self.wikiText.h2.find_all_next("p")[0]).split('"')[1].split('"')[0]
        except:
            self.ability = "Ability not found."
            failCount += 1
        try: self.flavour = str(self.wikiText.find_all("p", class_="flavour")).split('">"')[1].split('"')[0]
        except:
            self.flavour = "Nobody knows which way the wind goes. Or this flavour text."
            failCount += 1
        try: self.artist = str(self.wikiText.find_all("td")[3])[4:-5]
        except:
            self.artist = "Unknown artist"
            failCount += 1
        try: self.summary = str(self.wikiText.h2.find_all_next("p")[1])[3:-4].strip()
        except:
            self.summary = "This character does something. Not sure what."
            failCount += 1
        try: self.summaryPoints = splitIntoPoints(str(self.wikiText.h2.find_all_next("ul")[0])[4:-5].replace("<li>","").replace("</li>",""))
        except:
            self.summaryPoints = []
            failCount += 1
        try: self.howToRunPoints = splitIntoPoints(self.cleanedWikiText.split('How to Run[edit]')[1].split('Examples[edit]')[0].strip())
        except:
            self.howToRunPoints = []
            failCount += 1
        try: self.examplePoints = splitIntoPoints(self.cleanedWikiText.split('Examples[edit]')[1].split('Tips & Tricks')[0].strip())
        except:
            self.examplePoints = []
            failCount += 1
        print(self.name + ": " + str(failCount) + " missing info(s)")
        
    def textRemedies(self):
        # make setup abilities bold and fix % (only in the Voudon's ability so far)
        self.ability = self.ability.replace("[", "\\textbf{[").replace("]", "]}").replace("%", "\%")
        # fix ampersands and character links across all
        self.ability = fixCharacterLinks(fixAmpersands(self.ability))
        self.summary = fixCharacterLinks(fixAmpersands(self.summary))
        self.summaryPoints = [fixCharacterLinks(fixAmpersands(point)) for point in self.summaryPoints]
        self.howToRunPoints = [fixCharacterLinks(boldFullyCapitalisedWords(fixAmpersands(point))) for point in self.howToRunPoints]
        self.examplePoints = [fixCharacterLinks(fixAmpersands(point)) for point in self.examplePoints]
        self.flavour = "FLAVOUR TEMPORARILY DISABLED DUE TO COOL ISSUES"
        
        
# fetch wiki
botcWiki = MediaWiki(url='https://wiki.bloodontheclocktower.com/api.php',
                     user_agent='clocktowerAlmanacizationator/0.0 (discord @ Panfex)')

# get list of character names
characterNamesToFetch = []
with open('roles.json', 'r') as file:
    data = json.load(file)
    for character in data:
        characterNamesToFetch.append(character['name'])
characterNamesToFetch = characterNamesToFetch[:20]

# for each name, fetch that character's info
for name in characterNamesToFetch:
    try:
        fetched = fetchCharacter(name)
        fetched.parseWikiText()
        fetched.textRemedies()
        characters.append(fetched)
    except:
        print(name + " failed to pull.")
        
# sort characters
tempList = sorted(characters , key=lambda x: x.name)
characters = sorted(tempList , key=lambda x: x.cType)

for character in characters:
    print(character.name)

# print LaTeX output to "output.txt"
with open("output.txt", "w") as f:
    output = preCharacterLaTeX
    for character in characters:
        output += "\\begin{multicols}{2}\n\\subsection{" + character.name + "}\n\\begin{figure}[H]\n\t\\centering\n\t\\includegraphics[width=0.5\\linewidth]{" + character.iconName + "}"
        output += "\\end{figure}\n{\\large " + character.ability + '}\n\\newline\n\\newline\n{\\large \\textit{"' + character.flavour + '"}}\n\\newline\n\n\\subsubsection{Summary}'
        output += "\n" + character.summary + "\n\\begin{itemize}"
        for point in character.summaryPoints:
            output += "\n\\item " + point[2:]
        output += "\n\\end{itemize}\n\n\\subsubsection{How to Run}\n\\begin{itemize}"
        for point in character.howToRunPoints:
            output += "\n\\item " + point[2:]
        output += "\n\\end{itemize}\n\n\\subsubsection{Examples}\n\\begin{itemize}"
        for point in character.examplePoints:
            output += "\n\\item " + point[2:]
        output += "\n\\end{itemize}\n\n\\textit{Designed by " + character.designer + "; icon by " + character.artist + "}\n\n\\end{multicols}\n\\clearpage\n\n"
        print(output, file=f)
        output = ""
    print(postCharacterLaTeX, file=f)
subprocess.run(["notepad","output.txt"])

