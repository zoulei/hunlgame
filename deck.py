from random import shuffle

def generateCards(handsstr):
    trandict = {"T": 10, "t": 10, "J": 11, "Q": 12, "K": 13, "A": 14, "j": 11, "q": 12, "k": 13, "a": 14, "S": 0,
                "s": 0,
                "H": 1, "h": 1, "C": 2, "c": 2, "D": 3, "d": 3}
    cardsList = []
    for i in xrange(0, len(handsstr), 2):
        value = handsstr[i]
        symbol = handsstr[i + 1]
        value = trandict.get(value, value)
        value = int(value)

        symbol = trandict.get(symbol, symbol)
        symbol = int(symbol)

        cardsList.append(Card(symbol, value))
    return cardsList

def generateHands(handsstr):
    trandict = {"T":10,"t":10,"J":11,"Q":12,"K":13,"A":14,"j":11,"q":12,"k":13,"a":14,"S":0,"s":0,
                "H":1,"h":1,"C":2,"c":2,"D":3,"d":3}
    if len(handsstr) == 3:
        value1 = handsstr[0]
        value2 = handsstr[1]
        if value1 > value2:
            tmp = value1
            value1 = value2
            value2 = tmp
        suti = handsstr[2]
        if suti == "s":
            suti = 1
        else:
            suti = 0
        if trandict.get(value1):
            value1 = trandict[value1]
        else:
            value1 = int(value1)

        if trandict.get(value2):
            value2 = trandict[value2]
        else:
            value2 = int(value2)

        card1 = Card(0,value1)
        if suti:
            card2 = Card(0,value2)
        else:
            card2 = Card(1,value2)
        return Hands([card1,card2])
    else:
        cardsList = []
        for i in xrange(0,len(handsstr),2):
            value = handsstr[i]
            symbol = handsstr[i+1]
            value = trandict.get(value,value)
            value = int(value)

            symbol = trandict.get(symbol,symbol)
            symbol = int(symbol)

            cardsList.append(Card(symbol,value))
        return Hands(cardsList)

class Hands:
    def __init__(self,hands):
        if hands[0].cmp(hands[1]) < 0:
            self.m_card1 = hands[0]
            self.m_card2 = hands[1]
        else:
            self.m_card1 = hands[1]
            self.m_card2 = hands[0]

    def __eq__(self, other):
        if self.m_card1.sameValue(other.m_card1) and self.m_card2.sameValue(other.m_card2) and \
            self.suti() == other.suti():
            return True
        return False

    def __str__(self):
        return str(self.m_card1) + " " +str(self.m_card2)

    def shortstr(self):
        if self.m_card1.symbol == self.m_card2.symbol:
            return str(self.m_card1)[0] + str(self.m_card2)[0] + "s"
        else:
            return str(self.m_card1)[0] + str(self.m_card2)[0] + "o"

    def equal(self,handsstr):
        trandict = {"J":11,"Q":12,"K":13,"A":14,"j":11,"q":12,"k":13,"a":14}
        value1 = handsstr[0]
        value2 = handsstr[1]
        suti = handsstr[2]
        if suti == "s":
            suti = 1
        else:
            suti = 0
        if trandict.get(value1):
            value1 = trandict[value1]
        else:
            value1 = int(value1)

        if trandict.get(value2):
            value2 = trandict[value2]
        else:
            value2 = int(value2)

    def get(self):
        return [self.m_card1,self.m_card2]

    def suti(self):
        return self.m_card1.symbol == self.m_card2.symbol

    def diff(self):
        return self.m_card2.value - self.m_card1.value

    def highCard(self):
        return self.m_card2.value

    def lowCard(self):
        return self.m_card1.value

class Card:
    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value = value

    # compare value
    def __cmp__(self, other):
        if self.value < other.value:
            return -1
        elif self.value == other.value:
            return 0
        return 1

    # compare value and symbol
    def cmp(self,other):
        if self.value < other.value:
            return -1
        elif self.value > other.value:
            return 1
        else:
            if self.symbol > other.symbol:
                return -1
            elif self.symbol < other.symbol:
                return 1
            else:
                return 0

    def __eq__(self, other):
        if self.value == other.value and self.symbol == other.symbol:
            return True
        return False

    def sameValue(self,other):
        return self.value == other.value
    
    def __str__(self):
        text = ""
        if self.value < 0:
            return "Joker";
        elif self.value == 11:
            text = "J"
        elif self.value == 12:
            text = "Q"
        elif self.value == 13:
            text = "K"
        elif self.value == 14:
            text = "A"
        else:
            text = str(self.value)

        if self.symbol == 0:    #D-Diamonds
            text += "S" 
        elif self.symbol == 1:  #H-Hearts
            text += "H"
        elif self.symbol == 2:  #S-Spade
            text += "C"
        else:   #C-Clubs
            text += "D" 
            
        return text    
    
class deck:
    
    #Initializes the deck, and adds jokers if specified
    def __init__(self, addJokers = False):
        self.cards = []
        self.inplay = []
        self.addJokers = addJokers
        for symbol in range(0,4):
            for value in range (2,15):
                self.cards.append( Card(symbol, value) )
        if addJokers:
            self.total_cards = 54
            self.cards.append( Card(-1, -1) )
            self.cards.append( Card(-1, -1) )
        else:
            self.total_cards = 52

    #Shuffles the deck
    def shuffle(self):
        self.cards.extend( self.inplay )
        self.inplay = []
        shuffle( self.cards )
    
    #Cuts the deck by the amount specified
    #Returns true if the deck was cut successfully and false otherwise
    def cut(self, amount):
        if not amount or amount < 0 or amount >= len(self.cards):
            return False #returns false if cutting by a negative number or more cards than in the deck
        
        temp = [] 
        for i in range(0,amount):
            temp.append( self.cards.pop(0) )
        self.cards.extend(temp)
        return True

    #Returns a data dictionary 
    def deal(self, number_of_cards):
        
        if(number_of_cards > len(self.cards) ):
            return False #Returns false if there are insufficient cards
        
        inplay = []
        for i in range(0, number_of_cards):
            inplay.append( self.cards.pop(0) )
        
        self.inplay.extend(inplay)            
        return inplay      
    
    def cards_left(self):
        return len(self.cards)

def Test():
    h1 = generateHands("27o")
    h4 = generateHands("72o")
    h2 = Hands([Card(2,2),Card(3,2)])
    h3 = Hands([Card(3,2),Card(2,2)])
    print h2== h3
    print h1
    print h4
    print h2
    print h3

def Test1():
    h1 = generateHands("3s5h")
    print h1

if __name__ == "__main__":
    Test()

