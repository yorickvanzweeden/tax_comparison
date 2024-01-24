import math

from calculations.heffingskortingen import calculate_general_tax_credit, calculate_employment_deduction


def bereken_jaarloon(bruto_inkomen):
    Lv = 54  # Tot en met Lmax: stapgrootte van het loon in de brontabel (met jaarbedragen).
    Lmax = 115560  # Het hoogste loonbedrag dat in de brontabel (met jaarbedragen) staat.

    if bruto_inkomen <= 0:
        return 0

    if bruto_inkomen <= Lmax:
        bruto_inkomen = (bruto_inkomen // Lv) * Lv

    return round(bruto_inkomen, 2)


def bereken_bijzonder_tarief(bruto_inkomen, bijzondere_verloning):
    if bruto_inkomen <= 10697:
        rate = 0
    elif bruto_inkomen <= 11599:
        rate = 28.70
    elif bruto_inkomen <= 21482:
        rate = 7.07
    elif bruto_inkomen <= 22660:
        rate = 33.84
    elif bruto_inkomen <= 37691:
        rate = 39.94
    elif bruto_inkomen <= 73031:
        rate = 49.54
    elif bruto_inkomen <= 124519:
        rate = 56.01
    else:
        rate = 49.50

    return round(bijzondere_verloning * rate / 100, 2)


def belasting_box_1_werknemer(bruto_inkomen, vakantietoeslag: bool = False, dertiende_maand: bool = False):
    jaarloon = bereken_jaarloon(bruto_inkomen)

    algemene_heffingskorting = calculate_general_tax_credit(jaarloon)
    # print("{:<30} {:<15.0f}".format("Algemene heffingskorting", algemene_heffingskorting))

    arbeidskorting = calculate_employment_deduction(jaarloon)
    # print("{:<30} {:<15.0f}".format("Arbeidskorting", arbeidskorting))

    schijf2_deel = max(0, jaarloon - 73_032)
    schijf1_deel = max(0, jaarloon - schijf2_deel)

    belasting_box_1 = math.floor(schijf1_deel * 0.3693) + math.floor(schijf2_deel * 0.4950)
    # print("{:<30} {:<15.0f}".format('Belasting box 1', belasting_box_1))

    loonheffing = max(0, math.floor(belasting_box_1 - (algemene_heffingskorting + arbeidskorting)))
    # print("{:<30} {:<15.0f}".format('Loonheffing', loonheffing))

    bijzondere_beloningen = 0
    if vakantietoeslag:
        bijzondere_beloningen = bruto_inkomen * 0.08
    if dertiende_maand:
        bijzondere_beloningen += bruto_inkomen / 12
    belasting_bijzonder_tarief = bereken_bijzonder_tarief(jaarloon, bijzondere_beloningen)
    # print("{:<30} {:<15.2f}".format("Belasting bijzonder tarief", belasting_bijzonder_tarief))

    return bruto_inkomen + bijzondere_beloningen - loonheffing - belasting_bijzonder_tarief


if __name__ == "__main__":
    print(belasting_box_1_werknemer(60000, True, True))
