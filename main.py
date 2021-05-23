import random
from larsen_inference import calculate_membership
from larsen_inference import filter_memberships
from larsen_inference import find_min
from larsen_inference import four_sets_cross_product
from larsen_inference import larsen_inference_evaluation
from larsen_inference import two_sets_cross_product
from larsen_inference import union
from larsen_inference import defuzzify


def print_report():
    """
    write the report of th operation in report.txt
    """
    with open('report.txt', 'w') as f:
        f.write(f'---------------------------------------------------------------------------\n'
                f'\nHouse Evaluation:\n'
                f'\nThe House Market Value {inputs[0]} has the following memberships:\n '
                f'{house_state_value}\n'
                f'\nThe House Location Value {inputs[1]} has the following memberships:\n '
                f'{house_state_location}\n'
                f'\nBy taking the cross product of the memberships we obtain:\n'
                f'{house_cross_product_set}\n'
                f'\nAccording to the House Evaluation rule set The house evaluation has\n'
                f'the following memberships:\n'
                f'{house_filtered_cross_product}\n'
                f'\nAfter defuzzification the house has the following value:\n'
                f'{home_defuzzified_value}\n'
                f'\n---------------------------------------------------------------------------'
                f'\nApplicant Evaluation:\n'
                f'\nThe Applicant Asset Value {inputs[2]} has the following memberships:\n '
                f'{assets_state}\n'
                f'\nThe Applicant Income Value {inputs[3]} has the following memberships:\n '
                f'{income_state}\n'
                f'\nBy taking the cross product of the memberships we obtain:\n'
                f'{applicant_cross_product_set}\n'
                f'\nAccording to the Applicant Evaluation rule set The applicant evaluation has\n'
                f'the following memberships:\n'
                f'{applicant_filtered_cross_product}\n'
                f'\nAfter defuzzification the applicant has the following value:\n'
                f'{applicant_defuzzified_value}\n'
                f'\n---------------------------------------------------------------------------'
                f'\nCredit Evaluation:\n'
                f'\nThe Interest Value {inputs[4]} has the following memberships:\n '
                f'{interest_state}\n'
                f'\nThe House Defuzzified Value {inputs[5]} has the following memberships:\n '
                f'{house_state_evaluation}\n'
                f'\nThe Applicant Defuzzified Value {inputs[6]} has the following memberships:\n '
                f'{applicant_state_evaluation}\n'
                f'\nThe Applicant Income Value {inputs[3]} has the following memberships:\n '
                f'{income_state}\n'
                f'\nBy taking the cross product of the memberships we obtain:\n')
        for subset in credit_cross_product_set:
            f.write(f'{subset}\n')
        f.write(f'\nAccording to the Credit Evaluation rule set The Credit evaluation has\n'
                f'the following memberships:\n'
                f'{credit_filtered_cross_product}\n'
                f'\nAfter defuzzification the credit has the following value:\n'
                f'{credit_defuzzified_value}\n'
                f'\nThe credit amount that can be given is: '
                f'{credit_defuzzified_value * 1000}$\n'
                f'\n---------------------------------------------------------------------------'
                )
        print('\n\nthe program executed successfully you can check the report!')


if __name__ == '__main__':
    # taking inputs

    stress_testing = True
    false_input = True
    inputs = []
    defuzzification_method = ''
    is_stress_testing = ''
    while false_input:
        try:
            is_stress_testing = input('Do you want to stress test the program?\n'
                                      'y for yes, n for no\n')
            if is_stress_testing == 'y':
                break
            inputs = input('\nPlease enter House Market Value, Location Value,\n'
                           'Asset Of The Applicant Value, Income Of The Applicant Value, '
                           'and Interest Value '
                           'respectively\n'
                           '------------------------------------------------------------\n'
                           'Restrictions:\n'
                           'House Market Value must be between 0.0 and 1000.0\n'
                           'Location Value must be between 0.0 and 10.0\n'
                           'Asset Of The Applicant Value must be between 0.0 and 1000.0\n'
                           'Income Of The Applicant Value must be between 0.0 and 100.0\n'
                           'Interest Value must be between 0.0 and 10.0\n'
                           '\nInputs: ').split()
            defuzzification_method = input('\nPlease choose the defuzzification method\n'
                                           '1 for center of area\n'
                                           '2 for bisector of area\n'
                                           '3 for mean of maximum\n')
            inputs = list(map(float, inputs))
            assert is_stress_testing == 'n'
            assert len(inputs) == 5
            assert (0.0 <= inputs[0] <= 1000.0 and 0.0 <= inputs[1] <= 10.0 and
                    0.0 <= inputs[2] <= 1000.0 and 0.0 <= inputs[3] <= 100.0 and
                    0.0 <= inputs[4] <= 10.0)
            assert defuzzification_method in ('1', '2', '3')
            false_input = False
        except AssertionError:
            print('Please check your inputs!')
    while stress_testing:
        if is_stress_testing == 'y':
            inputs = [random.random() * 1000, random.random() * 10, random.random() * 1000,
                      random.random() * 100, random.random() * 10]
            defuzzification_method = str(random.randint(1, 3))
            print(f'Inputs are {inputs}')
            print(f'Defuzzification Method is {defuzzification_method}\n')
        elif is_stress_testing == 'n':
            stress_testing = False
        # house evaluation
        house_state_value = calculate_membership(inputs[0], 'HV')
        house_state_location = calculate_membership(inputs[1], 'HL')
        house_cross_product_set = two_sets_cross_product(house_state_value, house_state_location)
        house_mapped_cross_product = find_min(house_cross_product_set, 'HE')
        house_filtered_cross_product = filter_memberships(house_mapped_cross_product)
        home_evaluation_results = larsen_inference_evaluation(house_filtered_cross_product, 'HMS')
        home_to_be_deffuzified = union(home_evaluation_results, label='House Evaluation')
        home_defuzzified_value = defuzzify(home_to_be_deffuzified, method=defuzzification_method,
                                           defuzzified_table='H')
        inputs.append(home_defuzzified_value)
        # applicant evaluation
        assets_state = calculate_membership(inputs[2], 'AA')
        income_state = calculate_membership(inputs[3], 'IA')
        applicant_cross_product_set = two_sets_cross_product(assets_state, income_state)
        applicant_mapped_cross_product = find_min(applicant_cross_product_set, 'AE')
        applicant_filtered_cross_product = filter_memberships(applicant_mapped_cross_product)
        applicant_evaluation_results = larsen_inference_evaluation(applicant_filtered_cross_product, 'AMS')
        applicant_to_be_deffuzified = union(applicant_evaluation_results, label='Applicant Evaluation')
        applicant_defuzzified_value = defuzzify(applicant_to_be_deffuzified, method=defuzzification_method,
                                                defuzzified_table='A')
        inputs.append(applicant_defuzzified_value)
        # credit evaluation
        interest_state = calculate_membership(inputs[4], 'I')
        house_state_evaluation = calculate_membership(inputs[5], 'HE')
        applicant_state_evaluation = calculate_membership(inputs[6], 'AE')
        credit_cross_product_set = four_sets_cross_product(interest_state, house_state_evaluation,
                                                           applicant_state_evaluation, income_state)
        credit_mapped_cross_product = find_min(credit_cross_product_set, 'CE')
        credit_filtered_cross_product = filter_memberships(credit_mapped_cross_product)
        credit_evaluation_result = larsen_inference_evaluation(credit_filtered_cross_product, 'CMS')
        to_be_deffuzified = union(credit_evaluation_result, label='Credit Evaluation')
        credit_defuzzified_value = defuzzify(to_be_deffuzified, method=defuzzification_method, defuzzified_table='C')
        if not stress_testing:
            print_report()
