market_value_of_houses_ms = {'low': (0, 0, 80, 100),
                             'medium': (50, 100, 200, 250),
                             'high': (200, 300, 650, 850),
                             'very_high': (650, 850, 1000, 1000)}

location_of_houses_ms = {'bad': (0, 0, 1.5, 4),
                         'fair': (2.5, 4.75, 6, 8.5),
                         'excellent': (6, 8.5, 10, 10)}

assets_of_applicant_ms = {'low': (0, 0, 0, 150),
                          'medium': (50, 225, 475, 650),
                          'high': (500, 700, 1000, 1000)}

income_of_applicant_ms = {'low': (0, 0, 10, 25),
                          'medium': (15, 35, 35, 55),
                          'high': (40, 60, 60, 80),
                          'very_high': (60, 80, 100, 100)}

interest_ms = {'low': (0, 0, 2, 5),
               'medium': (2, 4, 6, 8),
               'high': (6, 8.5, 10, 10)}

house_ms = {'very_low': (0, 0, 0, 3),
            'low': (0, 3, 3, 6),
            'medium': (2, 5, 5, 8),
            'high': (4, 7, 7, 10),
            'very_high': (7, 10, 10, 10)}

applicant_ms = {'low': (0, 0, 2, 4),
                'medium': (2, 5, 5, 8),
                'high': (6, 8, 10, 10)}

credit_amount_ms = {'very_low': (0, 0, 0, 125),
                    'low': (0, 125, 125, 250),
                    'medium': (125, 250, 250, 375),
                    'high': (250, 375, 375, 500),
                    'very_high': (375, 500, 500, 500)}

# first value is location, second is market value-----------------------------------------------------------------------
house_evaluation_rule_set = {'bad': {'low': 'very_low', 'medium': 'low', 'high': 'medium', 'very_high': 'high'},
                             'fair': {'low': 'low', 'medium': 'medium', 'high': 'high', 'very_high': 'very_high'},
                             'excellent': {'low': 'medium', 'medium': 'high', 'high': 'very_high',
                                           'very_high': 'very_high'}}
# an additional rule for market value
house_evaluation_additional_mv_rule = {'low': 'low'}
# an additional rule for location
house_evaluation_additional_loc_rule = {'bad': 'low'}
# ----------------------------------------------------------------------------------------------------------------------


# first value is asset, second is income--------------------------------------------------------------------------------
applicant_evaluation_rule_set = {'low': {'low': 'low', 'medium': 'low', 'high': 'medium', 'very_high': 'high'},
                                 'medium': {'low': 'low', 'medium': 'medium', 'high': 'high', 'very_high': 'high'},
                                 'high': {'low': 'medium', 'medium': 'medium', 'high': 'high', 'very_high': 'high'}}
# ----------------------------------------------------------------------------------------------------------------------


# first value is income second is interest------------------------------------------------------------------------------
evaluation_of_the_credit_rule_set_ii = {'low': {'medium': 'very_low', 'high': 'very_low'},
                                        'medium': {'high': 'very_low'}}
# first value is applicant
evaluation_of_the_credit_rule_set_applicant = {'low': 'very_low'}
# first value is house
evaluation_of_the_credit_rule_set_house = {'very_low': 'very_low'}
# first value is applicant, second is house
evaluation_of_the_credit_rule_set_ah = {'medium': {'very_low': 'low', 'low': 'low', 'medium': 'medium', 'high': 'high',
                                                   'very_high': 'high'},
                                        'high': {'very_low': 'low', 'low': 'medium', 'medium': 'high', 'high': 'high',
                                                 'very_high': 'very_high'}}
# ----------------------------------------------------------------------------------------------------------------------
