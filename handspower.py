from handsrange import HandsRange
from deck import generateHands
from deck import generateCards
from deck import Card
from deck import Hands
from holdem import Poker

class HandsPower:
    def __init__(self,hands,board = [],debug = False):
        self.m_hands = hands
        self.m_board = board
        self.debug = debug
        if board:
            self.m_floap = board[:3]
        else:
            self.m_floap = []
        if len(board) > 3:
            self.m_turn = board[3]
        else:
            self.m_turn = None
        if len(board) > 4:
            self.m_river = board[4]
        else:
            self.m_river = None

    def addFloap(self,floap=[]):
        self.m_board.extend(floap)
        self.m_floap = floap

    def addTurn(self,turn=None):
        self.m_board.append(turn)
        self.m_turn = turn

    def addRiver(self,river=None):
        self.m_board.append(river)
        self.m_river = river

    def getHandsPower(self,handsObj = None,handsRange=None,valueHands = None):
        if handsObj:
            for card in self.m_hands.get():
                handsObj.eliminateCard(card)
            for card in self.m_board:
                handsObj.eliminateCard(card)
            handsRange = handsObj.get()
        if not handsRange:
            handsObj = HandsRange(debug=self.debug)
            for card in self.m_hands.get():
                handsObj.eliminateCard(card)
            for card in self.m_board:
                handsObj.eliminateCard(card)
            handsObj.addFullRange()
            handsRange = handsObj.get()

        poker = Poker(2)
        results = poker.determine_score(self.m_board,[self.m_hands.get(),])
        valueResults = poker.determine_score(self.m_board,[valueHands.get(),])

        win = 0
        tie = 0
        lose = 0
        blank = 0
        for hands in handsRange:
            cmpResult = poker.determine_score(self.m_board,[hands.get(),])
            cmpResult.extend(valueResults)
            winner = poker.determine_winner(cmpResult)

            if isinstance(winner,list):
                win += 1
            elif winner == 1:
                blank += 1
            else:
                cmpResult.extend(results)
                winner = poker.determine_winner(cmpResult)
                if isinstance(winner,list):
                    tie += 1
                elif winner == 2:
                    win += 1
                else:
                    lose += 1

        return [win,tie,lose,blank]

def Test():
    handspower = HandsPower(generateHands("8Qs"),[Card(1,4),Card(2,6),Card(3,12)])
    result = handspower.getHandsPower(valueHands=generateHands("8061"))
    for v in result:
        print v

def Test2(handsstr,boardstr,valuestr):
    handspower = HandsPower(generateHands(handsstr), generateCards(boardstr))
    handspower = handspower.getHandsPower(valueHands=generateHands(valuestr))
    print handsstr,boardstr
    for v in handspower:
        print v

def Test1():
    handspower = HandsPower(generateHands("ATo"), generateCards("T27321"))
    handspower = handspower.getHandsPower(valueHands=generateHands("T380"))
    print "ATo:T27321"
    for v in handspower:
        print v
    handspower = HandsPower(generateHands("9To"), generateCards("T27321"))
    handspower = handspower.getHandsPower(valueHands=generateHands("72Q0"))
    print "9To:T27321"
    for v in handspower:
        print v
    handspower = HandsPower(generateHands("3To"), generateCards("T27321"))
    handspower = handspower.getHandsPower(valueHands=generateHands("72Q0"))
    print "3To:T27321"
    for v in handspower:
        print v

    Test2("ATo","A37223","A240")
    Test2("9To", "T37323", "72Q0")

    Test2("A3T0", "T37323", "72Q0")
    Test2("93T0", "T37323", "72Q0")

    Test2("93T0", "A2T2913323", "A1K1")

    Test2("A0K3", "A37221", "A2T0")
    Test2("A333", "8353J3J2", "K3Q3")


if __name__ == "__main__":
    Test1()