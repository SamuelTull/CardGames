from random import shuffle
from itertools import combinations
from collections import defaultdict


class Card:
    def __init__(self, card):
        value_dict = {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "T": 10,
            "J": 11,
            "Q": 12,
            "K": 13,
            "A": 14,
        }
        suit_dict = {"H": "♥️", "D": "♦️", "S": "♠", "C": "♣️"}
        self.value = value_dict[card[0]]
        self.suit = card[1]
        self.card = card[0] + suit_dict[card[1]]

    def __str__(self):
        return self.card

    def __eq__(self, other):
        return self.card == other.card


class Deck(list):
    def __init__(self, l):
        super(Deck, self).__init__(l)

    def __str__(self):
        return f"{[str(card) for card in self]}"

    def __sub__(self, other):
        return self.__class__([card for card in self if card not in other])

    def __add__(self, other):
        return self.__class__([card for card in self] + [card for card in other])


def rank_hand(hand):
    value_counts = defaultdict(lambda: 0)
    for card in hand:
        value_counts[card.value] += 1
    counts = sorted(value_counts.values(), reverse=True)
    v_sorted = sorted(value_counts.keys(), reverse=True)
    v_by_count = sorted(value_counts.items(), key=lambda x: x[1], reverse=True)
    suits = {card.suit for card in hand}

    # Straight Flush
    if len(suits) == 1:
        if len(v_sorted) == 5:
            if v_sorted[0] - v_sorted[4] == 4:
                return [9, v_sorted[0]]
            if v_sorted == [14, 5, 4, 3, 2]:
                return [9, 5]
    # 4 of a Kind
    if counts == [4, 1]:
        four = v_by_count[0][0]
        kicker = v_by_count[1][0]
        return [8, four, kicker]
    # Full House
    if counts == [3, 2]:
        set = v_by_count[0][0]
        pair = v_by_count[1][0]
        return [7, set, pair]
    # Flush
    if len(suits) == 1:
        return [6] + v_sorted
    # Straight
    if len(v_sorted) == 5:
        if v_sorted[0] - v_sorted[4] == 4:
            return [5, v_sorted[0]]
        if v_sorted == [14, 5, 4, 3, 2]:
            return [5, 5]
    # 3 of a Kind
    if counts == [3, 1, 1]:
        set = v_by_count[0][0]
        v_sorted.remove(set)
        return [4, set] + v_sorted
    # 2 Pairs
    if counts == [2, 2, 1]:
        pairs = [v_by_count[0][0], v_by_count[1][0]]
        kicker = v_by_count[2][0]
        return [3, max(pairs), min(pairs), kicker]
    # Pair
    if counts == [2, 1, 1, 1]:
        pair = v_by_count[0][0]
        v_sorted.remove(pair)
        return [2, pair] + v_sorted
    # High Card
    return [1] + v_sorted


def compare_ranks(rank0, rank1):
    max_i = min([len(rank) for rank in [rank0, rank1]])
    for i in range(max_i):
        if rank0[i] > rank1[i]:
            return 0
        elif rank1[i] > rank0[i]:
            return 1
    return 0.5


def best_hand(Cards, Shared):
    possible_hands = combinations(Cards + Shared, 5)
    rank_best = [0]
    hand_best = []
    for hand in possible_hands:
        rank = rank_hand(hand)
        if compare_ranks(rank_best, rank) == 1:
            rank_best = rank
            hand_best = hand
    return hand_best, rank_best


def compare(Cards0, Cards1, Shared):
    _, rank0 = best_hand(Cards0, Shared)
    _, rank1 = best_hand(Cards1, Shared)
    return compare_ranks(rank0, rank1)


def newDeck():
    suits = ["H", "D", "S", "C"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
    return Deck([Card(value + suit) for value in values for suit in suits])


def newSuit(suit):
    suits = [suit]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
    return Deck([Card(value + suit) for value in values for suit in suits])


def testDeck():
    suits = ["H", "C"]
    values = ["2", "3", "4", "5", "7", "8", "T", "A"]
    return Deck([Card(value + suit) for value in values for suit in suits])


# hand - say aces
# for hands other can have
# for all 5 cards shared can be
# compare


def getHandOddsStochastically(Hand, N=100):
    deck = newDeck() - Hand
    count = 0
    for i in range(N):
        shuffle(deck)
        Other = deck[:2]
        Shared = deck[2:7]
        count += compare(Other, Hand, Shared)
    print(f"Win {count} from {N}: {count/N*100}%")


def getVsHandOddsStochastically(Hand, Other, N=100):
    deck = newDeck() - Hand - Other
    count = 0
    for _ in range(N):
        shuffle(deck)
        Shared = deck[:5]
        count += compare(Other, Hand, Shared)
    print(f"{Hand} vs {Other}, Win {count} from {N}: {count/N*100}%")


def getVsHandOddsStochastically(Hand, Other, N=100):
    deck = newDeck() - Hand - Other
    count = 0
    for _ in range(N):
        shuffle(deck)
        Shared = deck[:5]
        count += compare(Other, Hand, Shared)
    print(f"{Hand} vs {Other}, Win {count} from {N}: {count/N*100}%")


def getVsHandOdds(Hand, Other):
    deck = newDeck() - Hand - Other
    possible_hands = combinations(deck, 5)
    i = 0
    count = 0
    for Shared in possible_hands:
        i += 1
        count += compare(Other, Hand, Shared)
    print(f"{Hand} vs {Other}, Win {count} from {i}: {count/i*100}%")


print(newDeck())

hand_best, rank_best = best_hand(
    Deck([Card("AH"), Card("AC")]),
    Deck([Card("TH"), Card("JH"), Card("2S"), Card("2C"), Card("2H")]),
)

print(Deck([x + y for x in ["1", "2", "3"] for y in ["D", "H"]]))
"""

getVsHandOdds(Deck([Card("AH"), Card("AC")]), Deck([Card("KH"), Card("KD")]))

getVsHandOddsStochastically(
    Deck([Card("AH"), Card("AC")]), Deck([Card("KH"), Card("KC")]), 1000
)

getVsHandOddsStochastically(
    Deck([Card("AS"), Card("KC")]), Deck([Card("KH"), Card("KD")]), 10000
)

getVsHandOddsStochastically(
    Deck([Card("AS"), Card("KS")]), Deck([Card("KH"), Card("KD")]), 10000
)

getVsHandOddsStochastically(
    Deck([Card("AH"), Card("KS")]), Deck([Card("KH"), Card("KD")]), 10000
)

getVsHandOddsStochastically(
    Deck([Card("TH"), Card("JH")]), Deck([Card("2S"), Card("2C")]), 1000000
)"""


def Test_Counts():
    # Check Counts correct
    possible_hands = combinations(newDeck(), 5)
    occurences = defaultdict(lambda: 0)
    for hand in possible_hands:
        occurences[rank_hand(hand)[0]] += 1
    total = sum(occurences.values())
    print("total", total)
    for key, value in sorted(occurences.items()):
        print(key, value, value / total * 100)
