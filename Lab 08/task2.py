from collections import namedtuple

Card = namedtuple('Card', ['rank', 'suit'])

deck = [
    Card(rank, suit) 
    for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    for rank in [str(i) for i in range(2, 11)] + ['Jack', 'Queen', 'King', 'Ace']
]

face_cards = ['Jack', 'Queen', 'King'] 
card_prob = {card: 1/52 for card in deck}

red_prob = round(sum(prob for card, prob in card_prob.items() if card.suit in ['Hearts', 'Diamonds']), 4)
print("Probability of drawing a red card:", red_prob)

p_heart_and_red = sum(prob for card, prob in card_prob.items() if card.suit == 'Hearts')
p_heart_given_red = round(p_heart_and_red / red_prob, 4)
print("Given red, probability it's a heart:", p_heart_given_red)

p_face = sum(prob for card, prob in card_prob.items() if card.rank in face_cards)
p_face_and_diamond = sum(prob for card, prob in card_prob.items() if card.rank in face_cards and card.suit == 'Diamonds')
p_diamond_given_face = round(p_face_and_diamond / p_face, 4)
print("Given face card, probability it's a diamond:", p_diamond_given_face)

p_face_and_spade_or_queen = sum(prob for card, prob in card_prob.items() if card.rank in face_cards and (card.suit == 'Spades' or card.rank == 'Queen'))
p_spade_or_queen_given_face = round(p_face_and_spade_or_queen / p_face, 4)
print("Given face card, probability it's a spade or queen:", p_spade_or_queen_given_face)