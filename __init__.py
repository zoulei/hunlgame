from holdem import Poker
import sys, random
import deck

def getwinner(board, privatecard, coloroffset = 0):
    poker = Poker(9, False)

    cardboard = []
    for carddata in board:
        cardboard.append(deck.Card(carddata[0]+coloroffset,carddata[1]))

    handsdata = []
    for hands in privatecard:
        cardhand = []
        for carddata in hands:
            cardhand.append(deck.Card(carddata[0]+coloroffset,carddata[1]) )
        handsdata.append(cardhand)

    results = poker.determine_score(cardboard, handsdata)
    winner = poker.determine_winner(results)
    if isinstance(winner,list):
        return winner
    else:
        return [winner,]

def sorthands(board, privatecard, coloroffset = 0):
    poker = Poker()

    cardboard = []
    for carddata in board:
        cardboard.append(deck.Card(carddata[0]+coloroffset,carddata[1]))

    handsdata = []
    for hands in privatecard:
        cardhand = []
        for carddata in hands:
            cardhand.append(deck.Card(carddata[0]+coloroffset,carddata[1]) )
        handsdata.append(cardhand)

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

if __name__ == "__main__":
    print getwinner([[1,13],[1,12],[1,11],[2,5],[3,8]], [[[2,14],[2,10]] ,[[3,10],[3,9]] ,[[1,6],[1,2]]],-1)
    print getwinner([[1,13],[1,12],[1,11],[2,5],[3,8]], [[[2,14],[2,10]] ,[[3,10],[3,9]]],-1)
    print "sorthands:"
    print sorthands([[1,13],[1,12],[1,11],[2,5],[3,8]], [[[2,14],[2,10]] ,[[3,10],[3,9]],[[3,10],[3,9]]],-1)
    print sorthands([[1,13],[1,12],[1,11],[2,5],[3,8]], [[[2,14],[2,10]] ,[[3,10],[3,9]] ,[[1,6],[1,2]]],-1)
    print sorthands([[1,13],[1,12],[1,11]], [[[2,14],[2,10]] ,[[3,10],[3,9]] ,[[1,6],[1,2]]],-1)
    print sorthands([[1,11],[2,5],[3,8]], [[[2,14],[2,10]] ,[[3,10],[3,9]] ,[[1,6],[1,2]]],-1)
    print sorthands([[1,13],[1,12],[1,11],[3,2]], [[[2,14],[2,10]] ,[[3,10],[3,9]] ,[[1,6],[1,2]]],-1)
