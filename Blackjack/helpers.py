import numpy as np

cardValues = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
fullDeck = np.array([4, 4, 4, 4, 4, 4, 4, 4, 16, 4])
emptyHand = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
bustProb = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 1.0])
standProb = lambda count: np.array([count - 17 == i for i in range(6)]).astype(float)
countHand = lambda hand: sum(hand[cardI] * cardValues[cardI] for cardI in range(10))
# does 21/Bj push against dealer 21/BJ?
