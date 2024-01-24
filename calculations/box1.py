import math


def belasting_box_1(salary, mkb_vrijstelling: bool = False, zelfstandigenaftrek: bool = False,
                    wbso_aftrek: bool = False, debug: bool = False):
    if debug:
        print("{:<30} {:<15.0f}".format('Bruto jaarinkomen', salary))
    belastbaar_inkomen = salary
    if zelfstandigenaftrek:
        belastbaar_inkomen -= 5_030

    if wbso_aftrek:
        belastbaar_inkomen -= 14_202 / 2  # 50% wbso aftrek want 2 founders

    if mkb_vrijstelling:
        belastbaar_inkomen = 0.86 * belastbaar_inkomen  # 14% mkb vrijstelling

    belastbaar_inkomen = max(0, belastbaar_inkomen)

    tier2_salary = max(0, belastbaar_inkomen - 73_032)
    tier1_salary = max(0, belastbaar_inkomen - tier2_salary)

    belasting_box_1 = math.floor(tier1_salary * 0.3693) + math.floor(tier2_salary * 0.4950)
    if debug:
        print("{:<30} {:<15.0f}".format('Belasting box 1', belasting_box_1))

    tier2_salary_before_rebate = max(0, salary - 73_032)
    total_rebate = salary - belastbaar_inkomen
    tariefsaanpassing = min(total_rebate, tier2_salary_before_rebate) * 0.1257
    tariefsaanpassing = math.floor(tariefsaanpassing)
    if debug:
        print("{:<30} {:<15.0f}".format('Tariefsaanpassing', tariefsaanpassing))

    bijdrage_zvw = min(belastbaar_inkomen, 66_956) * 0.0543
    bijdrage_zvw = math.floor(bijdrage_zvw)
    if debug:
        print("{:<30} {:<15.0f}".format("Bijdrage Zvw", bijdrage_zvw))

    algemene_heffingskorting = 0
    if belastbaar_inkomen < 22_661:
        algemene_heffingskorting = 3_070
    elif belastbaar_inkomen < 73_031:
        algemene_heffingskorting = 3_070 - 0.06095 * (belastbaar_inkomen - 22_660)
    algemene_heffingskorting = math.ceil(algemene_heffingskorting)
    if debug:
        print("{:<30} {:<15.0f}".format("Algemene heffingskorting", algemene_heffingskorting))

    if salary < 10_741:
        arbeidskorting = 0.08231 * salary
    elif salary < 23_201:
        arbeidskorting = 884 + 0.29861 * (salary - 10_740)
    elif salary < 37_691:
        arbeidskorting = 4_605 + 0.03085 * (salary - 23_201)
    elif salary < 115_295:
        arbeidskorting = 5_052 - 0.06510 * (salary - 37_691)
    else:
        arbeidskorting = 0
    arbeidskorting = math.ceil(arbeidskorting)
    if debug:
        print("{:<30} {:<15.0f}".format("Arbeidskorting", arbeidskorting))

    subtotal_taxes = belasting_box_1 + tariefsaanpassing + bijdrage_zvw
    subtotal_reduction = algemene_heffingskorting + arbeidskorting
    if subtotal_reduction > subtotal_taxes:
        subtotal_reduction = subtotal_taxes

    netto = salary - subtotal_taxes + subtotal_reduction
    if debug:
        print("{:<30} {:<15.0f}".format("Netto", netto))
        print()
    return netto


if __name__ == "__main__":
    belasting_box_1(115_000, mkb_vrijstelling=True, zelfstandigenaftrek=False, wbso_aftrek=False)
