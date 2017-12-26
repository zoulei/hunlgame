from holdem import Poker
from handsrange import HandsRange
import copy
from deck import Hands,generateCards,generateHands
import commonfunc

# bigger, idx lesser
def cmphands(result1,result2):
    result1 = result1[0]
    result2 = result2[0]
    if result1[0] > result2[0]:
        return 1
    elif result1[0] < result2[0]:
        return -1
    else:
        for kiker1, kiker2 in zip(result1[1],result2[1]):
            if kiker1 > kiker2:
                return 1
            elif kiker1 < kiker2:
                return -1
        else:
            return 0

class WinrateCalculator:
    def __init__(self, board, myhand, ophands):
        self.m_board = board
        self.m_myhands = myhand
        self.m_ophands = ophands
        self.m_pokerengine = Poker()



    def calmywinrate__(self, board, myhand, ophandslist):
        for ophands in ophandslist:
            for card in myhand.get():
                ophandskey = ophands.keys()
                for hand in ophandskey:
                    if card in hand.get():
                        del ophands[hand]
            if not len(ophands):
                return -1
            mylen = 1
            oplen = len(ophands)
            handinfo = []
            ophandskey = ophands.keys()



            fullhand = [myhand,] + list(ophandskey)
            for hand in fullhand:
                handinfo.append(hand.get())
            results = self.m_pokerengine.determine_score(board, handinfo)
            results = zip(results, range(len(results)))
            results.sort(cmp=cmphands, reverse=True)

            opremain = oplen
            totalwin = 0
            for _, idx in results:
                if idx == 0:
                    # my hand
                    totalwin += opremain
                    break
                else:
                    opremain -= 1
            avgwin = totalwin * 1.0 / mylen
            avgwinrate = avgwin / oplen
            return avgwinrate

    def calmywinrate_(self, board, myhands, ophands):
        for card in board:
            for idx in xrange(len(myhands) - 1, -1, -1):
                if card in myhands[idx].get():
                    del myhands[idx]
            for idx in xrange(len(ophands) - 1, -1, -1):
                if card in ophands[idx].get():
                    del ophands[idx]

        if not len(myhands) or not len(ophands):
            return -1

        totalwinrate = 0
        totalhand = 0
        for hand in myhands:
            curwinrate = self.calmywinrate__(board, hand, copy.deepcopy(ophands))
            if curwinrate != -1:
                totalwinrate += curwinrate
                totalhand += 1
        if totalhand == 0:
            return -1
        return totalwinrate / totalhand

    def calmywinrate(self):
        myhands = copy.deepcopy(self.m_myhands)
        ophands = copy.deepcopy(self.m_ophands)
        return self.calmywinrate_(self.m_board,myhands,ophands)

class FPWinrateEngine:
    def __init__(self, board, myhand, ophands = None):
        self.m_board = board
        self.m_myhand = myhand
        if ophands is None:
            self.initophands()
        else:
            self.m_ophands = ophands

        self.determinscore()

    def determinscore(self):
        self.m_pokerengine = Poker()
        handinfo = []
        fullhand = [self.m_myhand,] + self.m_ophands
        for hand in fullhand:
            handinfo.append(hand.get())
        results = self.m_pokerengine.determine_score(self.m_board, handinfo)
        results = zip(results, range(len(results)))
        results.sort(cmp=cmphands, reverse=True)

        self.m_handrank = []
        lastresult = results[0][0]
        idxlist = [results[0][1],]
        for result, idx in results[1:]:
            if result == lastresult:
                idxlist.append(idx)
            else:
                self.m_handrank.append(idxlist)
                idxlist = [idx]
            lastresult = result
        self.m_handrank.append(idxlist)

    def initophands(self):
        handsrange = HandsRange()
        handsrange.addFullRange()
        for card in self.m_board:
            handsrange.eliminateCard(card)
        for card in self.m_myhand.get():
            handsrange.eliminateCard(card)
        self.m_ophands = handsrange.get()

    def isnuts(self):
        if 0 in self.m_handrank[0]:
            return True
        return False

    # para:
    # equalvalue: how much win when tie
    def calmywinrate(self, equalvalue = 0):
        winhand = 0
        losehand = 0
        lose = True
        for idxlist in self.m_handrank:
            if lose:
                if 0 in idxlist:
                    winhand += (len(idxlist) - 1 ) * equalvalue
                    losehand += (len(idxlist) - 1 ) * (1 - equalvalue)
                    lose = False
                else:
                    losehand += len(idxlist)
            else:
                winhand += len(idxlist)
        winrate = winhand * 1.0 / (winhand + losehand)
        return winrate

class SoloWinrateCalculator:
    def __init__(self, board, myhands, ophands,debug = False):
        self.m_myhands = myhands
        self.m_ophands = ophands
        self.m_board = list(board)
        self.m_mylen = len(myhands)
        self.m_oplen = len(ophands)

        self.m_debug = debug

        self.m_pokerengine = Poker()

    def calmywinrate__(self, board, myhand, ophands):
        for card in myhand.get():
            for idx in xrange(len(ophands) - 1, -1, -1):
                if card in ophands[idx].get():
                    del ophands[idx]
        if not len(ophands):
            return -1
        mylen = 1
        oplen = len(ophands)
        handinfo = []
        fullhand = [myhand,] + ophands
        for hand in fullhand:
            handinfo.append(hand.get())
        results = self.m_pokerengine.determine_score(board, handinfo)
        results = zip(results, range(len(results)))
        results.sort(cmp=cmphands, reverse=True)

        if self.m_debug:
            for rank, data in enumerate(results):
                print rank, " : ", fullhand[data[1]],
                if data[1] < mylen:
                    print "   from myhand"
                else:
                    print

        opremain = oplen
        totalwin = 0
        for _, idx in results:
            if idx < mylen:
                # my hand
                totalwin += opremain
                # curwinrate = opremain / self.m_oplen
            else:
                opremain -= 1
        avgwin = totalwin * 1.0 / mylen
        avgwinrate = avgwin / oplen
        return avgwinrate

    def calmywinrate_(self, board, myhands, ophands):
        for card in board:
            for idx in xrange(len(myhands) - 1, -1, -1):
                if card in myhands[idx].get():
                    del myhands[idx]
            for idx in xrange(len(ophands) - 1, -1, -1):
                if card in ophands[idx].get():
                    del ophands[idx]

        if not len(myhands) or not len(ophands):
            return -1

        totalwinrate = 0
        totalhand = 0
        for hand in myhands:
            curwinrate = self.calmywinrate__(board, hand, copy.deepcopy(ophands))
            if curwinrate != -1:
                totalwinrate += curwinrate
                totalhand += 1
        if totalhand == 0:
            return -1
        return totalwinrate / totalhand

    def calmywinrate(self):
        myhands = copy.deepcopy(self.m_myhands)
        ophands = copy.deepcopy(self.m_ophands)
        return self.calmywinrate_(self.m_board,myhands,ophands)

    def calnextturnwinrate(self):
        handrangeobj = HandsRange()
        allcards = handrangeobj._generateallcard()
        for card in self.m_board:
            allcards.remove(card)

        avgwinrate = 0
        ignore = 0
        for card in allcards:
            board = copy.deepcopy(self.m_board)
            board.append(card)

            myhands = copy.deepcopy(self.m_myhands)
            ophands = copy.deepcopy(self.m_ophands)

            winrate = self.calmywinrate_(board,myhands,ophands)
            if winrate == -1:
                ignore += 1
            else:
                avgwinrate += winrate

        if len(allcards) == ignore:
            return -1
        else:
            avgwinrate /= ( len(allcards) - ignore )
            return avgwinrate

    def calnextturnstackwinrate(self):
        handrangeobj = HandsRange()
        allcards = handrangeobj._generateallcard()
        for card in self.m_board:
            allcards.remove(card)

        nextturnwinratelist = []

        for card in allcards:
            board = copy.deepcopy(self.m_board)
            board.append(card)

            myhands = copy.deepcopy(self.m_myhands)
            ophands = copy.deepcopy(self.m_ophands)

            winrate = self.calmywinrate_(board,myhands,ophands)
            if winrate == -1:
                continue

            nextturnwinratelist.append([board, winrate])

        nextturnwinratelist.sort(key = lambda v:v[1])
        return nextturnwinratelist

def test():
    myhandsstr = ["8S9D"]
    # ophandsstr = ["KSKC","KS5S"]
    ophandsstr = ["5S7D", "ACKC", "2C7C"]
    board = generateCards("ADKD4S")
    myhands = []
    for handstr in myhandsstr:
        myhands.append(generateHands(handstr))
    ophands = []
    for handstr in ophandsstr:
        ophands.append(generateHands(handstr))
    solo = SoloWinrateCalculator(board,myhands,ophands, False)
    print solo.calmywinrate()
    print solo.calnextturnstackwinrate()

def testFPWinrate():
    myhandsstr = "8S9D"
    # ophandsstr = ["KSKC","KS5S"]
    ophandsstr = ["5S7D", "ACKC", "2C7C","8S9D"]
    board = generateCards("ADKD4S")
    myhands = generateHands(myhandsstr)
    ophands = []
    for handstr in ophandsstr:
        ophands.append(generateHands(handstr))
    fp = FPWinrateEngine(board,myhands,ophands)
    print fp.calmywinrate()
    print fp.isnuts()

if __name__ == "__main__":
    # test()
    testFPWinrate()