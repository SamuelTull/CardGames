from helpers import *

dealerOddsCache = {}
dealerOddsInfCache = {}

playerEVCache = {}
standEVCache = {}
hitEVCache = {}
doubleEVCache = {}
splitEVCache = {}


def dealerOdds(dealerCards, burntCards=emptyHand, nDecks=1):
    if isinstance(dealerCards, int):
        assert 0 <= dealerCards <= 9
        return dealerOdds(
            np.array([dealerCards == i for i in range(10)]).astype(int),
            burntCards,
            nDecks,
        )
    key = str(nDecks) + str(dealerCards) + str(burntCards)
    if key in dealerOddsCache:
        return dealerOddsCache[key]
    count = countHand(dealerCards)
    if count - 10 * dealerCards[-1] > 21:
        dealerOddsCache[key] = bustProb
        return dealerOddsCache[key]
    for ace in range(dealerCards[-1] + 1):
        if 17 <= count - 10 * ace <= 21:
            dealerOddsCache[key] = standProb(count - 10 * ace)
            return dealerOddsCache[key]

    calculatedProb = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    totalRemaining = 52 * nDecks - sum(dealerCards) - sum(burntCards)
    for cardI in range(10):
        cardValue = cardValues[cardI]
        if cardValue == 10:
            cardRemaining = 16 * nDecks - dealerCards[cardI] - burntCards[cardI]
        else:
            cardRemaining = 4 * nDecks - dealerCards[cardI] - burntCards[cardI]
        p = cardRemaining / totalRemaining

        if p > 0:
            calculatedProb += p * dealerOdds(
                dealerCards + np.array([cardI == i for i in range(10)]).astype(int),
                burntCards,
                nDecks,
            )

    dealerOddsCache[key] = calculatedProb
    return dealerOddsCache[key]


def dealerOddsInf(dealerTotal, dealerAces=0):
    while dealerTotal > 21 and dealerAces > 0:
        dealerTotal -= 10
        dealerAces -= 1
    if (dealerTotal, dealerAces) in dealerOddsInfCache:
        return dealerOddsInfCache[(dealerTotal, dealerAces)]
    if dealerTotal > 21:
        dealerOddsInfCache[(dealerTotal, dealerAces)] = bustProb
        return dealerOddsInfCache[(dealerTotal, dealerAces)]
    if 17 <= dealerTotal <= 21:
        dealerOddsInfCache[(dealerTotal, dealerAces)] = standProb(dealerTotal)
        return dealerOddsInfCache[(dealerTotal, dealerAces)]

    calculatedProb = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    for cardI in range(10):
        cardValue = cardValues[cardI]
        p = 1 / 13 if cardValue != 10 else 4 / 13
        if p > 0:
            calculatedProb += p * dealerOddsInf(
                dealerTotal + cardValue, dealerAces + (cardValue == 11)
            )

    dealerOddsInfCache[(dealerTotal, dealerAces)] = calculatedProb
    return dealerOddsInfCache[(dealerTotal, dealerAces)]


def standEV(playerTotal, playerAces, dealerTotal, dealerAces):
    while playerTotal > 21 and playerAces > 0:
        playerTotal -= 10
        playerAces -= 1
    if playerTotal > 21:
        return -1
    if (playerTotal, playerAces, dealerTotal, dealerAces) in standEVCache:
        return standEVCache[(playerTotal, playerAces, dealerTotal, dealerAces)]
    dealerOdds = dealerOddsInf(dealerTotal, dealerAces)
    winChance = dealerOdds[-1]
    drawChance = 0
    loseChance = 0
    for i in range(5):
        if i + 17 < playerTotal:
            winChance += dealerOdds[i]
        elif i + 17 == playerTotal:
            drawChance += dealerOdds[i]
        else:
            loseChance += dealerOdds[i]
    standEVCache[(playerTotal, playerAces, dealerTotal, dealerAces)] = (
        winChance - loseChance
    )
    return winChance - loseChance


def hitEV(playerTotal, playerAces, dealerTotal, dealerAces):
    if (playerTotal, playerAces, dealerTotal, dealerAces) in hitEVCache:
        return hitEVCache[(playerTotal, playerAces, dealerTotal, dealerAces)]
    while playerTotal > 21 and playerAces > 0:
        playerTotal -= 10
        playerAces -= 1
    if playerTotal > 21:
        return -1
    EV = 0
    for cardI in range(10):
        cardValue = cardValues[cardI]
        p = 1 / 13 if cardValue != 10 else 4 / 13
        if p > 0:
            EV += p * max(
                playerEV(
                    playerTotal + cardValue,
                    playerAces + (cardValue == 11),
                    dealerTotal,
                    dealerAces,
                )
            )
    hitEVCache[(playerTotal, playerAces, dealerTotal, dealerAces)] = EV
    return EV


def doubleEV(playerTotal, playerAces, dealerTotal, dealerAces):
    if (playerTotal, playerAces, dealerTotal, dealerAces) in doubleEVCache:
        return doubleEVCache[(playerTotal, playerAces, dealerTotal, dealerAces)]
    while playerTotal > 21 and playerAces > 0:
        playerTotal -= 10
        playerAces -= 1
    if playerTotal > 21:
        return -1
    EV = 0
    for cardI in range(10):
        cardValue = cardValues[cardI]
        p = 1 / 13 if cardValue != 10 else 4 / 13
        if p > 0:
            EV += (
                p
                * 2
                * standEV(
                    playerTotal + cardValue,
                    playerAces + (cardValue == 11),
                    dealerTotal,
                    dealerAces,
                )
            )
    doubleEVCache[(playerTotal, playerAces, dealerTotal, dealerAces)] = EV
    return EV


def splitEV(playerTotal, playerAces, dealerTotal, dealerAces):
    if (playerTotal, playerAces, dealerTotal, dealerAces) in splitEVCache:
        return splitEVCache[(playerTotal, playerAces, dealerTotal, dealerAces)]
    playerTotal = playerTotal // 2
    playerAces = playerAces // 2
    EV = 0
    for cardI in range(10):
        cardValue = cardValues[cardI]
        p = 1 / 13 if cardValue != 10 else 4 / 13
        if p > 0:
            EV += (
                p
                * 2
                * max(
                    playerEV(
                        playerTotal + cardValue,
                        playerAces + (cardValue == 11),
                        dealerTotal,
                        dealerAces,
                        canSplit=False,  # (cardValue == playerTotal) would lead to inf loop i think
                        canDouble=True,
                    )
                )
            )
    splitEVCache[(playerTotal, playerAces, dealerTotal, dealerAces)] = EV
    return EV


def playerEV(
    playerTotal, playerAces, dealerTotal, dealerAces, canDouble=False, canSplit=False
):
    stand = standEV(playerTotal, playerAces, dealerTotal, dealerAces)
    hit = hitEV(playerTotal, playerAces, dealerTotal, dealerAces)
    double = (
        doubleEV(playerTotal, playerAces, dealerTotal, dealerAces)
        if canDouble
        else -1e10
    )  #
    split = (
        splitEV(playerTotal, playerAces, dealerTotal, dealerAces) if canSplit else -1e10
    )  #
    return np.array([stand, hit, double, split])
