import math


def calculate_zorgtoeslag(toetsingsinkomen):
    # constants for 2023
    standard_premie = 1889
    drempelinkomen = 25070
    max_toetsingsinkomen = 38520

    # Check if the toetsingsinkomen is too high
    if toetsingsinkomen > max_toetsingsinkomen:
        return 0

    # Calculate the normpremie
    if toetsingsinkomen > drempelinkomen:
        normpremie = 0.00123 * drempelinkomen + 0.1364 * (toetsingsinkomen - drempelinkomen)
    else:
        normpremie = 0.00123 * drempelinkomen

    # Calculate the zorgtoeslag
    zorgtoeslag = max(0, standard_premie - round(normpremie, 2))

    return math.floor(zorgtoeslag / 12) * 12


if __name__ == "__main__":
    for i in range(33000, 33200, 1):
        print(i, calculate_zorgtoeslag(i) / 12)
