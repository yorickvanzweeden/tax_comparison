import math


def calculate_employment_deduction(income):
    # Arbeidskorting
    # https://download.belastingdienst.nl/belastingdienst/docs/rekenvoorschriften_voor_geautomatiseerde_loonadministratie_lh991z31fd.pdf
    first_buildup_factor = 0.08231
    first_income_threshold = 10_740
    first_buildup_max = 884

    second_buildup_factor = 0.29861
    second_income_threshold = 23_201
    second_buildup_max = 4_605

    third_buildup_factor = 0.03085
    third_income_threshold = 37_691
    third_buildup_max = 5_052

    drawdown_factor = 0.06510
    drawdown_threshold = 115_295

    if income <= drawdown_threshold:
        first_buildup = min(first_buildup_factor * income, first_buildup_max)
        second_buildup = min(first_buildup + second_buildup_factor * max(income - first_income_threshold, 0),
                             second_buildup_max)
        third_buildup = min(second_buildup + third_buildup_factor * max(income - second_income_threshold, 0),
                            third_buildup_max)
        drawdown = third_buildup - drawdown_factor * max(income - third_income_threshold, 0)
        employment_deduction = max(drawdown, 0)
        employment_deduction = round(employment_deduction, 2)  # convert to period amount and round to 2 decimals
    else:
        employment_deduction = 0  # set to zero if income > drawdown_threshold

    return employment_deduction


def calculate_general_tax_credit(income):
    # Algemene heffingskorting
    tax_credit_base = 3070
    first_income_threshold = 22660
    second_income_threshold = 73031
    drawdown_factor = 0.06095

    if income <= first_income_threshold:
        general_tax_credit = tax_credit_base
    elif income <= second_income_threshold:
        general_tax_credit = tax_credit_base - (income - first_income_threshold) * drawdown_factor
    else:
        general_tax_credit = 0  # set to zero if income > second_income_threshold

    general_tax_credit = max(general_tax_credit, 0)  # ensure tax credit is not less than zero
    general_tax_credit = math.ceil(general_tax_credit)

    return general_tax_credit
