import random
import math

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

def getSuit(card):
    return card[-1]

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

def isFlush(hand):
    suitDist = handSuits(hand)
    for suit in suitDist:
        if suitDist[suit] >= 5:
            scoringHand = []
            for card in hand:
                if getSuit(card) == suit:
                    scoringHand.append(card)
            return scoringHand
    return False
    # suit = getSuit(hand[0])
    # return all(suit == getSuit(card) for card in hand[1:-1])

def isStraight(hand):
    run = 1
    ordered= [getVal(card) for card in hand]
    ordered.sort(reverse=True)
    if ordered[0] == 14:
        ordered.append(1)
    high = ordered[0]
    for i in range(0,len(ordered)-1):
        if ordered[i] == ordered[i+1] + 1:
            run += 1
            if run == 5:
                return [high]
        elif ordered[i] != ordered[i+1]:
            run = 1
            high = ordered[i+1]
    return False

def isStraightFlush(hand):
    highCard = isStraight(hand)
    if (highCard and isFlush(hand)):
        return highCard
    return False

def isRoyalFlush(hand):
    # total = sum(getVal(card) for card in hand)
    return(isStraightFlush(hand) == 14)

def handVals(hand):
    dist = {}
    for card in hand:
        val = getVal(card)
        if not val in dist:
            dist[val] = 1
        else:
            dist[val] += 1
    return dist

def handSuits(hand):
    dist = {}
    for card in hand:
        suit = getSuit(card)
        if not suit in dist:
            dist[suit] = 1
        else:
            dist[suit] += 1
    return dist

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

def score(hand):
    vals = handVals(hand)
    straight = isStraight(hand)
    flush = isFlush(hand)
    if straight and flush:
        if straight == 14: return (10, [10])
        else: return (9, straight)
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
    
    # Flush, scoring hand derived in flush function
    if flush: 
        return (6,flush)
    
    # Scoring hand derived in straight function
    if straight: return (5,straight)
    
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

def compare(h1, h2):
    score1 = score(h1)
    score2 = score(h2)
    for me, opp in zip(score1, score2):
        if me > opp:
            return 1
        if me < opp:
            return 0
    return 1
    

def buildDeck() -> set:
    vals = ['A','K','Q','J','10','9','8','7','6','5','4','3','2']
    suits = ['S','C','D','H']
    deck = set()
    for val in vals:
        for suit in suits:
            card = val + suit
            deck.add(card)
    return deck

def randCards(deck:set, num:int):
    hand = []
    newDeck = deck.copy()
    for _ in range(num):
        card = random.choice(list(newDeck))
        newDeck.remove(card)
        hand.append(card)
    return hand, newDeck

def backPropagate(node:Node):
    myHand, oppHand = simulate(node)
    outcome = compare(myHand, oppHand)
    backProp = node
    while backProp:
        backProp.visits+=1
        backProp.wins+=outcome
        backProp=backProp.parent
    return

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
        
def ucb1(node:Node):
    w = node.wins
    n = node.visits
    N = node.parent.visits
    c = math.sqrt(2)
    ln = math.log(N)

    return (w/n) + c * math.sqrt(ln/n)

def estimator(hole: list):
    deck = buildDeck()
    for card in hole:
        deck.remove(card)
    
    root = Node(0,0,hole,[],[],deck,[],None)
    # branch(root, deck)

    for _ in range(20000):
        selection(root)
    print(root.wins/ root.visits)
    
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
            turn.extend(parent.comm)
            node = Node(0,0,parent.hand.copy(),parent.opp.copy(),turn,newDeck,[],parent)
        elif len(parent.comm) == 4:
            river, newDeck = randCards(deck, 1)
            river.extend(parent.comm)
            node = Node(0,0,parent.hand.copy(),parent.opp.copy(),river,newDeck,[],parent)
        
        parent.children.append(node)
        # if not done: branch(node, newDeck, done)
    return


    


if __name__ == "__main__":
    estimator(['4H','4C'])