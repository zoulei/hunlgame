from holdem import Poker
from handsrange import HandsRange
import copy
from deck import Hands,generateCards,generateHands

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

class SoloWinrateCalculator:
    def __init__(self, board, myhands, ophands,debug = False):
        self.m_myhands = myhands
        self.m_ophands = ophands
        self.m_board = board
        self.m_mylen = len(myhands)
        self.m_oplen = len(ophands)

        self.m_debug = debug

        self.m_pokerengine = Poker()

    def calmywinrate_(self, board, myhands, ophands):
        for card in board:
            for idx in xrange(len(myhands) - 1, -1 -1):
                if card in myhands[idx].get():
                    del myhands[idx]
            for idx in xrange(len(ophands) - 1, -1 -1):
                if card in ophands[idx].get():
                    del ophands[idx]

        if not len(myhands) or not len(ophands):
            return -1

        mylen = len(myhands)
        oplen = len(ophands)
        handinfo = []
        fullhand = myhands + ophands
        for hand in fullhand:
            handinfo.append(hand.get())
        results = self.m_pokerengine.determine_score(board, handinfo)
        results = zip(results,range(len(results)))
        results.sort(cmp=cmphands,reverse=True)

        if self.m_debug:
            for rank, data in enumerate(results):
                print rank, " : ",fullhand[data[1]]

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
                avgwinrate += self.calmywinrate_(board,myhands,ophands)

        avgwinrate /= ( len(allcards) - ignore )
        return avgwinrate

def test():
    myhandsstr = ["5SAC","2S2C","ASAC"]
    # ophandsstr = ["KSKC","KS5S"]
    ophandsstr = ["6D7D"]
    board = generateCards("ADKD4S")
    myhands = []
    for handstr in myhandsstr:
        myhands.append(generateHands(handstr))
    ophands = []
    for handstr in ophandsstr:
        ophands.append(generateHands(handstr))
    solo = SoloWinrateCalculator(board,myhands,ophands, True)
    print solo.calmywinrate()
    print solo.calnextturnwinrate()

if __name__ == "__main__":
    test()
