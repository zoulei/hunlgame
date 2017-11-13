import deck


class Rule:
    def __init__(self,highCard=0,lowCard=0,suti=0,diff=0):
        self.m_highCard = highCard
        self.m_lowCard = lowCard
        self.m_suti = suti
        self.m_diff = diff

    def include(self,hands):
        if self.m_highCard and self.m_highCard != hands.highCard():
            return False
        if self.m_lowCard and self.m_lowCard > hands.lowCard():
            return False
        if self.m_suti and not hands.suti():
            return False
        if self.m_diff and self.m_diff != hands.diff():
            return False
        return True

class HandsRange:
    #==============================
    #---------constructor----------
    #==============================
    def __init__(self,debug = False):
        self.reset()
        self.debug = debug

    def reset(self):
        self.m_ruleStack = []
        self.m_eliminateHands = []
        self.m_addHands = []
        self.m_eliminateCard = []

    #==============================
    #---------remove hands---------
    #==============================
    # Hands' type determines suti or not
    def eliminate(self,hands):
        self.m_eliminateHands.append(hands)

    #==============================
    #----eliminate specific card---
    #==============================
    # this is used since the card on the board and my hand
    # cannot appeal in my opponent's hand
    def eliminateCard(self,card):
        self.m_eliminateCard.append(card)

    #===============================
    #----------add hands to range---
    #===============================
    # Hands' type determines suti or not
    def add(self,hands):
        self.m_addHands.append(hands)

    #===============================
    #--------add hands satisfying the rule
    #===============================
    def addRule(self,highCard=0,lowCard=0,suti=0,diff=0):
        self.m_ruleStack.append(Rule(highCard,lowCard,suti,diff))


    def _generateallcard(self):
        cardslist = []
        for symbol in xrange(4):
            for value in xrange(14,1,-1):
                curCard = deck.Card(symbol,value)
                print "card:"
                print curCard
                print self.m_eliminateCard
                if curCard not in self.m_eliminateCard:
                    cardslist.append(curCard)
        if self.debug:
            print "remain ",len(cardslist)," cards"
        return cardslist

    #===============================
    #-----get a list of hands-------
    #===============================
    # get a list of hands that is in this range,
    # the rules that generate the list is as blow:
    # 1. if hands is in addhands, then include it.
    # 2. if hands is in eliminatehands, then exclude it.
    # 3. if hands is in any rules, then include it.
    def get(self):
        handslist = []
        cardslist = self._generateallcard()
        cardsnum = len(cardslist)

        # count = 0
        for card1 in xrange(cardsnum):
            for card2 in xrange(card1 + 1,cardsnum):
                curhands = deck.Hands([cardslist[card1],cardslist[card2]])
                if self.include(curhands):
                    handslist.append(curhands)
        #         else:
        #             print "hands:",curhands," not in range"
        #         count += 1
        # print "count:",count
        if self.debug:
            print "generate ",len(handslist)," hands"
        return handslist

    #================================
    #------if a hands is in range-----
    #================================
    # the rule is the same as self.get function
    def include(self,hands):
        for cmphands in self.m_eliminateHands:
            if  hands == cmphands:
                return False
        for cmphands in self.m_addHands:
            if  hands == cmphands:
                return True

        for rule in self.m_ruleStack:
            if rule.include(hands):
                return True
        return False

    #=================================
    #------add pocket pair------------
    #=================================
    # upper and lower limit the range
    def addpair(self,upper = 14,lower=2):
        for i in xrange(lower,upper+1):
            self.add(deck.Hands([deck.Card(0,i),deck.Card(1,i)]))

    def getPreflopTight(self):
        self.addRule(suti =1,diff=1,lowCard=4)
        self.addRule(suti=1,diff=2,lowCard=3)
        self.addRule(highCard=14,lowCard=10)
        self.addpair()
        self.addRule(suti=1,highCard=14)
        #self.eliminate(deck.generateHands("22o"))
        #self.add(deck.Hands([deck.Card(0,2),deck.Card(1,7)]))
        return self.get()

    def addFullRange(self):
        self.addRule(lowCard=2)

def Test():
    a = HandsRange()
    rangelist=a.getPreflopTight()
    print len(rangelist)
    for hands in rangelist:
        print hands
    # import pprint
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(a.getPreflopTight())

if __name__ == "__main__":
    Test()