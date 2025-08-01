# Card format: String(ValueSuit) 
# e.g. AD, QS, 10H, 4C

# Hand order:
#     10 Royal Flush
#     9 Straight Flush
#     8 Four of a Kind
#     7 Flush
#     6 Straight
#     5 Full House
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
    suit = getSuit(hand[0])
    return all(suit == getSuit(card) for card in hand[1:-1])

def isStraight(hand):
    ordered= [getVal(card) for card in hand]
    ordered.sort()
    for i in range(0,len(ordered)-1):
        if ordered[i] != ordered[i+1]-1:
            return False
    return ordered[-1]

def isStraightFlush(hand):
    
    return(isFlush(hand) and isStraight(hand))

def isRoyalFlush(hand):
    # total = sum(getVal(card) for card in hand)
    return(isStraightFlush(hand) == 14)

def handDist(hand):
    dist = {}
    for card in hand:
        val = getVal(card)
        if not val in dist:
            dist[val] = 1
        else:
            dist[val] += 1
    return dist

def pairs(dist):
    twos = 0
    three = 0
    four = 0
    for val in dist.values():
        if val == 2:
            twos += 1
        elif val == 3:
            three += 1
        elif val == 4:
            four += 1
    return (twos,three,four)

def score(hand):
    straight = isStraight(hand)
    flush = isFlush(hand)
    if straight and flush:
        if straight == 14: return 10
        else: return 9
    dist = handDist(hand)
    two,three,four = pairs(dist)
    if four: return 8
    if flush: return 7
    if straight: return 6
    if three and two: return 5
    if two:
        if two == 2: return 3
        else: return 2
    return max(dist.values())

def compare(h1, h2):
    score1 = score(h1)
    score2 = score(h2)
    if score1 > score2:
        return "W"
    if score1 < score2:
        return "L"
    if score1 == 10: return "T"
    if score1 == 9:
    


if __name__ == "__main__":
    print(score(['9H','QS','JS','KS','10S']))
