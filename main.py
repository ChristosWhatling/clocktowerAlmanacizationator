from mediawiki import MediaWiki
from bs4 import BeautifulSoup

# CLASS DEFINITIONS

class clocktowerCharacter:
    def __init__(self, name: str, wikiText: BeautifulSoup, cType: str = "", ability: str = "", flavour: str = "",
                 artist: str = "", summary: str = "", summaryPoints: str = "", howToRunPoints: str = "",
                 examplePoints: str = "", url: str = ""):
        self.name = name                        # Page title (e.g., "Imp")
        self.cType = cType                      # Character Type
        self.ability = ability                  # Ability text
        self.flavour = flavour                  # Flavour text
        self.artist = artist                    # Artist credit
        self.summary = summary                  # Summary blurb, e.g. "The Amnesiac doesn’t know their own ability."
        self.summaryPoints = summaryPoints      # Summary points
        self.howToRunPoints = howToRunPoints    # "How to Run" points
        self.examplePoints = examplePoints      # Example points
        self.url = url                          # Original wiki URL
        self.wikiText = wikiText                # Original wiki text
        
    def infodump(self):
        print("====================")
        print(self.name + " {" + self.cType + "} - " + self.ability)
        print('"' + self.flavour + '"')
        print("====================")
        
    def parseWikiText(self):
        self.cType = str(self.wikiText.find_all("td")[1]).split('title="Character Types">')[1].split('<')[0]
        self.ability = str(self.wikiText.h2.find_all_next("p")[0]).split('"')[1].split('"')[0]
        self.flavour = str(self.wikiText.find_all("p", class_="flavour")).split('">"')[1].split('"')[0]
        

# fetch wiki
botcWiki = MediaWiki(url='https://wiki.bloodontheclocktower.com/api.php',
                     user_agent='clocktowerAlmanacizationator/0.0 (discord @ Panfex)')
# temp list of character names
characterNames = ["Washerwoman", "Butler", "Scarlet Woman", "Imp", "Scapegoat", "Deus ex Fiasco", "Big Wig"]

# match wiki page name formatting
for name in characterNames:
    name = name.replace(" ", "_")

# step 2: for each character, pull their wiki page

characterToSearch = "Kazali"
p = botcWiki.page(characterToSearch)
soup = BeautifulSoup(p.html, "html.parser")
# soupedText = soup.get_text(separator=" ", strip=True)
# print(soup)
testCharacter = clocktowerCharacter(characterToSearch, soup)
testCharacter.parseWikiText()
testCharacter.infodump()

# step 3: extract relevant info from wiki page and format into LaTeX



# step 4: assemble full LaTeX output (as .txt file?)


