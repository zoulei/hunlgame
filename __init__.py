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

if __name__ == "__main__":
    #print getwinner([[1,13],[1,12],[1,11],[2,5],[3,8]], [[[2,14],[2,10]] ,[[3,10],[3,9]] ,[[1,6],[1,2]]],-1)
    print getwinner([[1,13],[1,12],[1,11],[2,5],[3,8]], [[[2,14],[2,10]] ,[[3,10],[3,9]]],-1)