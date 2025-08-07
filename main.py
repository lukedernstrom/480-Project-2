import random
import math

# Class definition for the node of the tree
class Node:
    def __init__(self,
                 wins:int,
                 visits:int,
                 hand:list,
                 opp:list,
                 comm:list,
                 deck:set,
                 children:list,
                 parent):
        self.wins = wins
        self.visits = visits
        self.hand = hand
        self.opp = opp
        self.comm = comm
        self.deck = deck
        self.children = children
        self.parent = parent

# Card format: String(ValueSuit) 
# e.g. AD, QS, 10H, 4C

# Hand order:
#     10 Royal Flush
#     9 Straight Flush
#     8 Four of a Kind
#     7 Full House
#     6 Flush
#     5 Straight
#     4 Three of a Kind
#     3 Two Pair
#     2 Two of a Kind
#     1 High Card

# Returns the suit of the given card as a string
def getSuit(card):
    return card[-1]

# Returns the value of the given card as an int, converting face cards
def getVal(card):
    val = card[0:-1]
    if val == 'A':
        return 14
    if val == 'K':
        return 13
    if val == 'Q':
        return 12
    if val == 'J':
        return 11
    
    return int(val)

# Given a list of cards, return the 5 card hand that makes the best flush, or False if none exist
# Returns strings, not values
def isFlush(hand):
    suitDist = handSuits(hand)
    for suit in suitDist:
        if suitDist[suit] >= 5:
            scoringHand = []
            for card in hand:
                if getSuit(card) == suit:
                    scoringHand.append(card)
            scoringHand.sort(reverse=True)
            return scoringHand[:5]
    return False

# Given a list of cards, return the high card for the hand that makes the best straight, or False if none exist
def isStraight(hand):
    run = 1
    ordered= [getVal(card) for card in hand]
    ordered.sort(reverse=True)
    if ordered[0] == 14: #Treats Aces as highest value and lowest value
        ordered.append(1)
    high = ordered[0]
    for i in range(len(ordered)-1):
        if ordered[i] == ordered[i+1] + 1:
            run += 1
            if run == 5:
                return high
        elif ordered[i] != ordered[i+1]:
            run = 1
            high = ordered[i+1]
    return False

# Returns the high card of the hand that makes a straight flush
def isStraightFlush(hand):
    if (x := isStraight(hand)):
        return x
    return False

# Returns a dictionary mapping each appearing card value to the number of times it appears in the hand
def handVals(hand):
    dist = {}
    for card in hand:
        val = getVal(card)
        if not val in dist:
            dist[val] = 1
        else:
            dist[val] += 1
    return dist

# Returns a dictionary mapping each suit to the number of times it appears in the hand
def handSuits(hand):
    dist = {}
    for card in hand:
        suit = getSuit(card)
        if not suit in dist:
            dist[suit] = 1
        else:
            dist[suit] += 1
    return dist

# Returns a tuple of three lists. Each list contains the card values that appear the given number of times 
# (i.e. three[] contains the list of cards that appear 3 times)
def pairs(dist:dict):
    twos = []
    three = []
    four = []
    for val in dist:
        if dist[val] == 2:
            twos.append(val)
        elif dist[val] == 3:
            three.append(val)
        elif dist[val] == 4:
            four.append(val)
    return (twos,three,four)

# Returns a tuple score for the hand. The first value is the numeric value of that hand, the second is cards/values to be used in the case of a tie
def score(hand):
    vals = handVals(hand)
    flush = isFlush(hand)
    # if straight and flush:
    #     if straight == 14: return (10, [10])
    #     else: return (9, straight)

    if flush and (strFlush := isStraightFlush(flush)):
        if strFlush == 14: return (10, [10])
        else: return (9, strFlush)
    two,three,four = pairs(vals)

    # Four of a kind, kicker = highest card not in the 4
    if four:
        kicker = max(vals)
        if kicker == four[0]:
            vals.pop(kicker)
            kicker = max(vals)
        return (8,[four[0], kicker])
    
    # Full house 3 & 2, no kicker
    if three and two: return (7,[max(three),max(two)])
    # Full house 3 & 3, no kicker
    if len(three) > 1:
        three.sort()
        return(7,[three[-1],three[-2]])
    
    # Flush
    if flush: 
        scoringHand = []
        for card in flush:
            scoringHand.append(getVal(card))
        return (6,flush[:6])
    
    # Scoring hand derived in straight function
    straight = isStraight(hand)
    if straight: return (5,[straight])
    
    # Three of a kind, kicker = 2 highest cards not in the pair
    if three: 
        kicker = []
        while len(kicker) < 2:
            card = max(vals)
            if card != three[0]: kicker.append(card)
            vals.pop(card)
        kicker.sort(reverse=True)
        three.extend(kicker)
        return (4,three)
    if two:
        if len(two) >= 2:
        # Two pair, kicker = highest card not in pairs
            two.sort() 
            kicker = 0
            while kicker == 0:
                kicker = max(vals)
                if kicker in two:
                    vals.pop(kicker)
                    kicker = 0
            return (3,[two[-1],two[-2], kicker])
        else:
        # One pair, kicker = highest 3 cards not in pairs
            kicker = []
            while len(kicker) < 3:
                card = max(vals)
                if card != two[0]: kicker.append(card)
                vals.pop(card)
            kicker.sort(reverse=True)
            two.extend(kicker)
            return (2,two)
        
    scoringHand = []
    while len(scoringHand) < 5:
        highCard = max(vals)
        scoringHand.append(highCard)
        vals.pop(highCard)
    return (1,scoringHand)

# Calculates the score for two hands then compares. First by looking at the hand category, then tiebreakers if necessary.
def compare(h1, h2):
    score1 = score(h1)
    score2 = score(h2)
    for me, opp in zip(score1, score2):
        if me > opp:
            return 1
        if me < opp:
            return 0
    return 1

#Creates a deck of 52 unique cards as a set by iterating through every possible suit and value
def buildDeck() -> set:
    vals = ['A','K','Q','J','10','9','8','7','6','5','4','3','2']
    suits = ['S','C','D','H']
    deck = set()
    for val in vals:
        for suit in suits:
            card = val + suit
            deck.add(card)
    return deck

# Given a deck and n number of cards, picks n cards, removes them from a copy of the deck, and returns the selected cards along with the new deck 
def randCards(deck:set, num:int):
    hand = []
    newDeck = deck.copy()
    for _ in range(num):
        card = random.choice(list(newDeck))
        newDeck.remove(card)
        hand.append(card)
    return hand, newDeck

# Given a node of the tree, simulates the resulting poker game and updates itself and all preceeding nodes with the outcome
def backPropagate(node:Node):
    myHand, oppHand = simulate(node)
    outcome = compare(myHand, oppHand)
    backProp = node
    while backProp:
        backProp.visits+=1
        backProp.wins+=outcome
        backProp=backProp.parent
    return

# Selects the best node to explore
def selection(root:Node):        
    if len(root.comm) == 5:
        backPropagate(root)
        return
    if root.visits == 0:
        branch(root, root.deck)
        backPropagate(root)
        return
    bestScore = 0
    bestNode = root.children[0]
    for child in root.children:
        if child.visits == 0:
            selection(child)
            return
        score = ucb1(child)
        if score > bestScore:
            bestScore = score
            bestNode = child
    selection(bestNode)
    return

# Manual ucb1 calculation
def ucb1(node:Node):
    w = node.wins
    n = node.visits
    N = node.parent.visits
    c = math.sqrt(2)
    ln = math.log(N)

    return (w/n) + c * math.sqrt(ln/n)

# Populates the remainder of the environment with randomized information
# Returns a complete 7 card hand consisting of 2 unique hole cards for the player and opponent and 5 shared community cards
def simulate(node:Node):
    deck = node.deck.copy()
    opp = node.opp.copy()
    comm = node.comm.copy()
    if not opp:
        opp, deck = randCards(deck, 2)
    if len(comm) < 5:
        newComm, deck = randCards(deck, 5-len(comm))
        comm.extend(newComm)
    myHand = node.hand.copy()
    myHand.extend(comm)
    opp.extend(comm)
    return (myHand,opp)

# Branches off of the given node to create 1000 unique children
def branch(parent:Node, deck:set):
    for _ in range(1000):
        if parent.opp == []:
            opHole, newDeck = randCards(deck, 2)
            node = Node(0,0,parent.hand.copy(),opHole,[],newDeck,[],parent)
        elif len(parent.comm) == 0:
            flop, newDeck = randCards(deck, 3)
            node = Node(0,0,parent.hand.copy(),parent.opp.copy(),flop,newDeck,[],parent)
        elif len(parent.comm) == 3:
            turn, newDeck = randCards(deck, 1)
            comm = parent.comm + turn
            node = Node(0,0,parent.hand.copy(),parent.opp.copy(),comm,newDeck,[],parent)
        elif len(parent.comm) == 4:
            river, newDeck = randCards(deck, 1)
            comm = parent.comm + river
            node = Node(0,0,parent.hand.copy(),parent.opp.copy(),comm,newDeck,[],parent)
        parent.children.append(node)
    return

def main(hole: list):
    deck = buildDeck()
    for card in hole:
        deck.remove(card)
    
    root = Node(0,0,hole,[],[],deck,[],None)

    for _ in range(20000):
        selection(root)
    print(root.wins/ root.visits)
    


if __name__ == "__main__":
    main(['4H','4C'])