from holdem import Poker
import sys, random
import deck
from handsrange import HandsRange
from deck import Hands, Card, generateCards, Board, Cardsengine, generateHands
import copy
from toygame import Toypoker
from WinrateCalculator import SoloWinrateCalculator, FPWinrateEngine

# card prensetation is [symbol, value]
def getwinner(board,privatecard):
    poker = Poker(9, False)

    results = poker.determine_score(board, [v.get() for v in privatecard])
    winner = poker.determine_winner(results)
    if isinstance(winner,list):
        return winner
    else:
        return [winner,]

def sorthands(board, privatecard, coloroffset = 0):
    # poker = Poker()

    cardboard = []
    for carddata in board:
        cardboard.append(deck.Card(carddata[0]+coloroffset,carddata[1]))

    handsdata = []
    for hands in privatecard:
        cardhand = []
        for carddata in hands:
            cardhand.append(deck.Card(carddata[0]+coloroffset,carddata[1]) )
        handsdata.append(cardhand)

    return sorthands_(cardboard,handsdata)

def sorthands_(cardboard,handsdata):
    poker = Poker(debug=False)
    results = poker.determine_score(cardboard, handsdata)
    results = zip(results,range(len(results)))
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

    results.sort(cmp = cmphands)
    lastrank = 1
    sortresult = {1:[results[0][1]]}
    for idx in xrange(1,len(results)):
        curresult = results[idx]
        lastresult = results[idx - 1]
        if curresult[0] == lastresult[0]:
            # the same strength
            sortresult[lastrank].append(curresult[1])
        else:
            sortresult[idx + 1] = [curresult[1]]
            lastrank = idx + 1

    return sortresult

# opponenthandsdata is a list of hands list, each hands list represent a opponent's hands range with its' probability.
# Example:  [[[handsobj1, 0.01],[handsobj2, 0.015],...] ,   []]
# the smallest element is Card object.
def calwinrate(ownhands, opponenthandsdata, board):
    winrate = 0
    for handsdata in opponenthandsdata:
        newhandsdata = [v[0] for v in handsdata] + [ownhands,]
        ownidx = len(newhandsdata) - 1
        sortresult = sorthands_(board,newhandsdata)
        for key,value in sortresult.items():
            if ownidx in value:
                # win ownidx -1 hands
                # tie len(value) -1 hands
                # lose to len(newhandsdata) - win - tie - 1
                win = ownidx - 1
                tie = len(value) - 1
                lose = len(newhandsdata) - win - tie - 1
                winrate*=( 1.0 * (win + tie) / (win + tie + lose) )
                break
    return winrate

def board2str(board):
    tmpboard = copy.deepcopy(list(board))
    tmpboard.sort()
    tmpboardstr = [str(v) for v in tmpboard]
    return " ".join(tmpboardstr)

if __name__ == "__main__":
    print getwinner(generateCards('9d 9c 8c 9h 8h'), [generateHands("5s 5d") ,generateHands('1h 1s')])
    # print getwinner([[1,13],[1,12],[1,11],[2,5],[3,8]], [[[2,14],[2,10]] ,[[3,10],[3,9]]],-1)
    # print "sorthands:"
    # print sorthands([[1,13],[1,12],[1,11],[2,5],[3,8]], [[[2,14],[2,10]] ,[[3,10],[3,9]],[[3,10],[3,9]]],-1)
    # print sorthands([[1,13],[1,12],[1,11],[2,5],[3,8]], [[[2,14],[2,10]] ,[[3,10],[3,9]] ,[[1,6],[1,2]]],-1)
    # print sorthands([[1,13],[1,12],[1,11]], [[[2,14],[2,10]] ,[[3,10],[3,9]] ,[[1,6],[1,2]]],-1)
    # print sorthands([[1,11],[2,5],[3,8]], [[[2,14],[2,10]] ,[[3,10],[3,9]] ,[[1,6],[1,2]]],-1)
    # print sorthands([[1,13],[1,12],[1,11],[3,2]], [[[2,14],[2,10]] ,[[3,10],[3,9]] ,[[1,6],[1,2]]],-1)
    # print sorthands([[1,13],[1,12],[1,14],[4,2],[4,3]], [[[2,9],[1,11]] ,[[2,8],[1,11]] ,[[2,6],[1,11]]],-1)
    # print sorthands([[1,13],[1,12],[1,14]], [[[2,9],[1,11]] ,[[2,8],[1,11]] ,[[2,6],[1,11]]],-1)

    # print board2str([Card(1,13),Card(1,12),Card(3,13)])
    #
    # print sorthands([[1,6],[2,7],[1,14],[3,2],[3,3]], [[[3,6],[3,7]] ,[[3,6],[3,14]] ,[[3,7],[3,14]]],-1)
