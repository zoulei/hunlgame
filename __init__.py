from holdem import Poker
import sys, random

def getwinner(board, privatecard):
    poker = Poker(9, False)
    results = poker.determine_score(board, privatecard)
    winner = poker.determine_winner(results)
    if isinstance(winner,list):
        return winner
    else:
        return [winner,]