
import random
from larsen_inference import calculate_membership
from larsen_inference import filter_memberships
from larsen_inference import find_min
from larsen_inference import four_sets_cross_product
from larsen_inference import larsen_inference_evaluation
from larsen_inference import two_sets_cross_product
from larsen_inference import union
from larsen_inference import defuzzify

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
            inputs = [random.random()*1000, random.random()*10, random.random()*1000,
                      random.random()*100, random.random()*10]
            defuzzification_method = str(random.randint(1, 3))
        elif is_stress_testing == 'n':
            stress_testing = False
        # house evaluation
        house_state_value = calculate_membership(inputs[0], 'HV')
        # print(house_state_value)
        house_state_location = calculate_membership(inputs[1], 'HL')
        # print(house_state_location)
        cross_product_set = two_sets_cross_product(house_state_value, house_state_location)
        # print(cross_product_set)
        mapped_cross_product = find_min(cross_product_set, 'HE')
        # print(mapped_cross_product)
        filtered_cross_product = filter_memberships(mapped_cross_product)
        # print(filtered_cross_product)
        home_evaluation_results = larsen_inference_evaluation(filtered_cross_product, 'HMS')
        # print(home_evaluation_results)
        home_to_be_deffuzified = union(home_evaluation_results)
        inputs.append(defuzzify(home_to_be_deffuzified, method=defuzzification_method))
        print(defuzzify(home_to_be_deffuzified, method=defuzzification_method))
        # applicant evaluation
        assets_state = calculate_membership(inputs[2], 'AA')
        # print(assets_state)
        income_state = calculate_membership(inputs[3], 'IA')
        # print(income_state)
        cross_product_set = two_sets_cross_product(assets_state, income_state)
        # print(cross_product_set)
        mapped_cross_product = find_min(cross_product_set, 'AE')
        # print(mapped_cross_product)
        filtered_cross_product = filter_memberships(mapped_cross_product)
        applicant_evaluation_results = larsen_inference_evaluation(filtered_cross_product, 'AMS')
        applicant_to_be_deffuzified = union(applicant_evaluation_results)
        inputs.append(defuzzify(applicant_to_be_deffuzified, method=defuzzification_method))
        print(defuzzify(applicant_to_be_deffuzified, method=defuzzification_method))
        # credit evaluation
        interest_state = calculate_membership(inputs[4], 'I')
        house_state_evaluation = calculate_membership(inputs[5], 'HE')
        applicant_state_evaluation = calculate_membership(inputs[6], 'AE')
        cross_product_set = four_sets_cross_product(interest_state, house_state_evaluation,
                                                    applicant_state_evaluation, income_state)
        mapped_cross_product = find_min(cross_product_set, 'CE')
        filtered_cross_product = filter_memberships(mapped_cross_product)
        credit_evaluation_result = larsen_inference_evaluation(filtered_cross_product, 'CMS')
        to_be_deffuzified = union(credit_evaluation_result)
        print(defuzzify(to_be_deffuzified, method=defuzzification_method))