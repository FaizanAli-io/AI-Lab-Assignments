one_dice_probabilities = {i: 0 for i in range(1, 7)}

for key, value in one_dice_probabilities.items():
    one_dice_probabilities[key] = 1 / len(one_dice_probabilities)

print("Single dice:-")

# Probability of even roll
p = round(sum(one_dice_probabilities[i] for i in one_dice_probabilities.keys() if i % 2 == 0), 2)

print("Probability of even roll:", p)

# Probability of roll > 4
p = round(sum(one_dice_probabilities[i] for i in one_dice_probabilities.keys() if i > 4), 2)

print("Probability of roll > 4:", p)

# Probability of roll < 3
p = round(sum(one_dice_probabilities[i] for i in one_dice_probabilities.keys() if i < 3), 2)

print("Probability of roll < 3:", p)

two_dice_probabilities = {(i, j): 0 for i in range(1, 7) for j in range(1, 7)}

for key, value in two_dice_probabilities.items():
    two_dice_probabilities[key] = 1 / len(two_dice_probabilities)

print("\nTwo dice:-")

# Probability of sum of rolls >= 7
p = round(sum(two_dice_probabilities[(i, j)] for i, j in two_dice_probabilities.keys() if i + j >= 7), 2)

print("Probability of sum of rolls >= 7:", p)

# Probability of sum of rolls == 8
p = round(sum(two_dice_probabilities[(i, j)] for i, j in two_dice_probabilities.keys() if i + j == 8), 2)

print("Probability of sum of rolls == 8:", p)

# P(A | B) = P(A ^ B) /  P(B)
# A = Second roll is odd
# B = First roll is > 4

p_a_and_b = sum(two_dice_probabilities[(i, j)] for i, j in two_dice_probabilities.keys() if (i > 4 and j % 2 == 1))
p_b = sum(two_dice_probabilities[(i, j)] for i, j in two_dice_probabilities.keys() if (i > 4))

# Probability of A given B
p = round(p_a_and_b / p_b, 2)

print("Probability of A given B:", p)