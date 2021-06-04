# two_layer_fuzzy_logic_system
Outline: 
1. The data 
2. The membership functions 
3. Taking the Cartesian product of the membership values 
4. Identifying the linguistic variables from the rule set along with the membership values 
5. Taking the union of the fuzzy numbers of the linguistic variables and returning a set of points that form the union 
6. Defuzzification process and making the program versatile to three defuzzification methods 
7. Generating a report of the process in a ‘txt’ file 
The Data: 
When designing the program the first thing to do was to write the data as dictionaries. This way a lot of flexibility is 
offered in the upcoming stages of designing the program. 
In the program all fuzzy numbers are assumed to be trapezoidal fuzzy numbers. By doing that there is no need to 
design functions for each triangular numbers and trapezoidal numbers separately. If the second and third entries of 
the fuzzy number’s tuple are equal then the fuzzy number is triangular else it’s trapezoidal. 
The memberships: 
The user gives a crisp value in a legit interval, exception handling, to the program, and the program must evaluate 
the membership value of that value. 
Example: The user gives the value ‘x’ to the program. The program iterates through each key, value pairs in the 
dictionary of the fuzzy numbers. Using the following pseudocode: memberships = [] 
for key, value in fuzzy_nubers_set: 
 if value[0] < x < value[1]: 
 membership_value = (x – value[0])/(value[1] – value[0]) 
 state = key 
 elseif value[1] <= x <= value[2]: 
 membership_value = 1 
 state = key 
 elseif value[2] < x < value[3]: 
 membership_value = (value[3] – x)/(value[3] – value[2]) 
 state = key 
 memberships.append( (state, membership_value) ) 
return memberships 
The actual code: 
The algorithm works for both triangular and trapezoidal fuzzy numbers. Evaluating the Cartesian product of the memberships: After evaluating the memberships of each input of a specific 
evaluation whether it’s the house, applicant, or credit evaluation the Cartesian product of the memberships is found. 
Example: in the house evaluation there is two parameters location and market value. After evaluating the 
memberships of both of them the Cartesian product of the memberships is evaluated as follows: 
Code Used: 
First function used for house and applicant evaluation since they have two inputs, and the second is used for credit 
evaluation since it has four inputs. 
After having the cross product of memberships the combinations are passed to find_min(combinations) function; for 
each combination the function finds the linguistic variable of the associated with the value being evaluated 
according to its rule set, and the min membership value among the memberships is assigned to the linguistic 
variable. Example: The Applicant has the following combination of memberships: 
((medium, 0.5), (high, 0.75)) 
First tuple is asset second is income. According to the rule set if asset is medium and income is high applicant 
evaluation is high so the linguistic variable is high and the membership is the min value among the two which is 0.5 
so 0.5 is assigned to high and the tuple (high, 0.5) is appended to the result list.
Then having the list of linguistic variable, membership pairs, some cleaning is made, for the sake of simplicity, to 
the list and a new list is returned e.g. 
The list have two pairs with the same linguistic variable but different memberships, the one with the min 
membership is omitted 
Example: 
[(high, 0.5), (high, 0.75)] here the first tuple is omitted from the list. 
Code used: Now the filtered list of linguistic variable, membership pairs is passed to 
larsen_inference_evaluation(memberships); the function returns a list of triples sorted by each containing (fuzzy 
number, membership value, linguistic variable). The triples then are used in the union function 
1. The fuzzy numbers are used for graphing and finding intersection points. 
2. Membership values are used for determining the height of the fuzzy number (Larsen multiplication). 
3. Linguistic variables are only used for labeling the graphs (matplotlib). 
The list is sorted according to the last entry of the fuzzy number. 
Taking the union of the fuzzy numbers of the linguistic variables and returning a set of points that form the union: 
After having the linguistic variable with the membership value, the product of the membership value with the 
linguistic variable fuzzy number is taken (shrinking the fuzzy number). 
For each fuzzy number the intersection point with the next fuzzy number is found using the line_intersection(line1, 
line2) function. Then the fuzzy union of the fuzzy numbers is taken, and a set of the points forming the union is returned. 
In the previous example the set of points forming the figure on the right 
[(2, 0), (5, 4.5), (7, 1.5), (8, 3.1), (10, 3.1)] is returned for the deffuzification process. 
The code: Defuzzification process and making the program versatile to three defuzzification methods: First a wrapper was 
made in order to call any defuzzification method from the same place 
Center of Area: After having the set of points of the union for each two points forming a line the slope and yintercept of the line is found and returned. 
Then the area under the line is calculated and summed up to the total area.  Also the definite integral of the (line*x) is calculated and summed up. 
At the end the following value is returned: 
Bisector of area: The aim is to find the ‘x’ coordinate that splits the union into two equal subareas. So first the area 
under the union was calculated using integration. After that it was divided by two to find half the area. After having 
half of the area value, the following algorithm was applied to find the x-coordinate. 
subarea = 0 
for line in union: 
 temp = calculate_definite_integral(line) 
 if temp + subarea > half the area: //the xcoordinate lies between the ends of line 
 return find_x(line, bounds,subarea, half_area) 
 elseif temp + subarea < half the area: 
 subarea += temp 
 elseif subarea + temp == half the area: //the xcoodinate lies at the end of the line 
 return right_end_of_line Determining the two points where x-coordinate of half the area lies between the following equality holds. 
Where x-coordinate is the coordinate of half the area. 
By making some algebraic manipulations the root of the following quadratic that lies between the two end points of 
the line is the x-coordinate of half the area. Given that the slope isn’t equal to zero. 
If the slope is zero using some area algebraic area formulas the x-coordinate of half the area can be found using the 
following formula. The function that determines the bounds where half the area lies: 
The function that finds the root of the quadratic or the algebraic formula according to the slope value. Mean of Maximum: The process is straight forward find the maximum points and return the mean of them. 
if max point lies on a triangle return the x of that point 
else if the max point lies on a trapezoid return the mean of ‘x’s of the trapezoid x of B and x of C. 
table_limits is used for determining whether the fuzzy number is triangular or trapezoidal. 
Printing the report: After finishing the design, it’s time to see some results. 
First the input from the user is taken: 
A char indicating whether the user wants to stress test the program or not. 
House Market Value 
House Location 
Asset of Applicant 
Income of Applicant 
Interest 
Defuzzification method The program make the calculations in the following order: 
1_ House Evaluation 
1. The memberships of house market value and house location is found. 
2. Cross product is found 
3. Linguistic variable, membership value calculations 
4. Filtering (deleting duplicate entries with same linguistic variables, only max membership value is kept) 
5. Forming the set of (fuzzy number, membership value, linguistic variable) triples. 
6. Finding the union and returning the set of points forming the curve. 
7. Deffuzifying to a crisp value 
2_Applicant Evaluation is done in the same manner. 
3_Credit Evaluation 
1. The membership of interest, house, and applicant is found. 
2. The cross product of the income, interest, house, and applicant is found. 
3. Linguistic variable, membership value calculations 
4. Filtering (deleting duplicate entries with same linguistic variables, only max membership value is kept) 
5. Forming the set of (fuzzy number, membership value, linguistic variable) triples. 
6. Finding the union and returning the set of points forming the curve. 
7. Deffuzifying to a crisp value 
And at the end a report summarizing the process is printed in a txt file. Inputs: 
1_For the first input the following set was used 
House Market Value = 600 
House Location = 6 
Applicant Asset = 400 
Applicant Income = 30 
Interest = 7.5 
Deffuzification Method = Center Of Area House Evaluation has the following memberships: 
Applicant Evaluation has the following memberships: 
Credit Evaluation has the following memberships: 
Summary: 
--------------------------------------------------------------------------- 
House Evaluation: The House Market Value 600.0 has the following memberships: 
 [('high', 1.0)] 
The House Location Value 6.0 has the following memberships: 
 [('fair', 1.0)] 
By taking the cross product of the memberships we obtain: 
[(('high', 1.0), ('fair', 1.0))] 
According to the House Evaluation rule set The house evaluation has 
the following memberships: 
[('high', 1.0)] 
After defuzzification the house has the following value: 
7.000000000000009 
--------------------------------------------------------------------------- 
Applicant Evaluation: 
The Applicant Asset Value 400.0 has the following memberships: 
 [('medium', 1.0)] 
The Applicant Income Value 30.0 has the following memberships: 
 [('medium', 0.75)] 
By taking the cross product of the memberships we obtain: 
[(('medium', 1.0), ('medium', 0.75))] 
According to the Applicant Evaluation rule set The applicant evaluation has 
the following memberships: 
[('medium', 0.75)] 
After defuzzification the applicant has the following value: 
5.0 
--------------------------------------------------------------------------- 
Credit Evaluation: 
The Interest Value 7.5 has the following memberships: 
 [('medium', 0.25), ('high', 0.6)] 
The House Defuzzified Value 7.000000000000009 has the following memberships: 
 [('medium', 0.3333333333333304), ('high', 0.999999999999997), ('very_high', 2.960594732333751e-15)] 
The Applicant Defuzzified Value 5.0 has the following memberships: 
 [('medium', 1.0)] 
The Applicant Income Value 30.0 has the following memberships: 
 [('medium', 0.75)] 
By taking the cross product of the memberships we obtain: 
(('medium', 0.25), ('medium', 0.3333333333333304), ('medium', 1.0), ('medium', 0.75)) 
(('medium', 0.25), ('high', 0.999999999999997), ('medium', 1.0), ('medium', 0.75)) 
(('medium', 0.25), ('very_high', 2.960594732333751e-15), ('medium', 1.0), ('medium', 0.75)) 
(('high', 0.6), ('medium', 0.3333333333333304), ('medium', 1.0), ('medium', 0.75)) (('high', 0.6), ('high', 0.999999999999997), ('medium', 1.0), ('medium', 0.75)) 
(('high', 0.6), ('very_high', 2.960594732333751e-15), ('medium', 1.0), ('medium', 0.75)) 
According to the Credit Evaluation rule set The Credit evaluation has 
the following memberships: 
[('medium', 0.3333333333333304), ('high', 0.999999999999997), ('very_low', 0.6)] 
After defuzzification the credit has the following value: 
287.1201657458556 
The credit amount that can be given is: 287120.1657458556$ 
--------------------------------------------------------------------------- 
2_For the second input the following set was used 
House Market Value = 400 
House Location = 7.5 
Applicant Asset = 800 
Applicant Income = 90 
Interest = 5 
Deffuzification Method = Bisector of Area 
House Evaluation has the following memberships: 
Applicant Evaluation has the following memberships: Credit Evaluation has the following memberships: 
Summary: 
--------------------------------------------------------------------------- 
House Evaluation: 
The House Market Value 400.0 has the following memberships: 
 [('high', 1.0)] 
The House Location Value 7.5 has the following memberships: 
 [('fair', 0.4), ('excellent', 0.6)] 
By taking the cross product of the memberships we obtain: 
[(('high', 1.0), ('fair', 0.4)), (('high', 1.0), ('excellent', 0.6))] 
According to the House Evaluation rule set The house evaluation has 
the following memberships: 
[('high', 0.4), ('very_high', 0.6)] 
After defuzzification the house has the following value: 
7.775140453871299 
--------------------------------------------------------------------------- 
Applicant Evaluation: 
The Applicant Asset Value 800.0 has the following memberships: 
 [('high', 1.0)] 
The Applicant Income Value 90.0 has the following memberships: 
 [('very_high', 1.0)] 
By taking the cross product of the memberships we obtain: 
[(('high', 1.0), ('very_high', 1.0))] 
According to the Applicant Evaluation rule set The applicant evaluation has 
the following memberships: 
[('high', 1.0)] 
After defuzzification the applicant has the following value: 
8.5 --------------------------------------------------------------------------- 
Credit Evaluation: 
The Interest Value 5.0 has the following memberships: 
 [('medium', 1.0)] 
The House Defuzzified Value 7.775140453871299 has the following memberships: 
 [('medium', 0.07495318204290029), ('high', 0.741619848709567), ('very_high', 0.25838015129043307)] 
The Applicant Defuzzified Value 8.5 has the following memberships: 
 [('high', 1.0)] 
The Applicant Income Value 90.0 has the following memberships: 
 [('very_high', 1.0)] 
By taking the cross product of the memberships we obtain: 
(('medium', 1.0), ('medium', 0.07495318204290029), ('high', 1.0), ('very_high', 1.0)) 
(('medium', 1.0), ('high', 0.741619848709567), ('high', 1.0), ('very_high', 1.0)) 
(('medium', 1.0), ('very_high', 0.25838015129043307), ('high', 1.0), ('very_high', 1.0)) 
According to the Credit Evaluation rule set The Credit evaluation has 
the following memberships: 
[('high', 0.741619848709567), ('very_high', 0.25838015129043307)] 
After defuzzification the credit has the following value: 
377.8454991374924 
The credit amount that can be given is: 377845.49913749244$ 
--------------------------------------------------------------------------- 
3_For the third input the following set was used 
House Market Value = 300 
House Location = 9 
Applicant Asset = 637.5 
Applicant Income = 43.7 
Interest = 5.66 
Deffuzification Method = Mean of Maximum 
House Evaluation has the following memberships: Applicant Evaluation has the following memberships: 
Credit Evaluation has the following memberships: 
Summary: 
--------------------------------------------------------------------------- 
House Evaluation: 
The House Market Value 300.0 has the following memberships: 
 [('high', 1.0)] 
The House Location Value 9.0 has the following memberships: 
 [('excellent', 1.0)] 
By taking the cross product of the memberships we obtain: 
[(('high', 1.0), ('excellent', 1.0))] 
According to the House Evaluation rule set The house evaluation has 
the following memberships: 
[('very_high', 1.0)] 
After defuzzification the house has the following value: 
10.0 
--------------------------------------------------------------------------- Applicant Evaluation: 
The Applicant Asset Value 637.5 has the following memberships: 
 [('medium', 0.07142857142857142), ('high', 0.6875)] 
The Applicant Income Value 43.7 has the following memberships: 
 [('medium', 0.5649999999999998), ('high', 0.18500000000000014)] 
By taking the cross product of the memberships we obtain: 
[(('medium', 0.07142857142857142), ('medium', 0.5649999999999998)), (('medium', 0.07142857142857142), ('high', 0.18500000000000014)), (('high', 0.6875), 
('medium', 0.5649999999999998)), (('high', 0.6875), ('high', 0.18500000000000014))] 
According to the Applicant Evaluation rule set The applicant evaluation has 
the following memberships: 
[('medium', 0.5649999999999998), ('high', 0.18500000000000014)] 
After defuzzification the applicant has the following value: 
5.0 
--------------------------------------------------------------------------- 
Credit Evaluation: 
The Interest Value 5.66 has the following memberships: 
 [('medium', 1.0)] 
The House Defuzzified Value 10.0 has the following memberships: 
 [('very_high', 1.0)] 
The Applicant Defuzzified Value 5.0 has the following memberships: 
 [('medium', 1.0)] 
The Applicant Income Value 43.7 has the following memberships: 
 [('medium', 0.5649999999999998), ('high', 0.18500000000000014)] 
By taking the cross product of the memberships we obtain: 
(('medium', 1.0), ('very_high', 1.0), ('medium', 1.0), ('medium', 0.5649999999999998)) 
(('medium', 1.0), ('very_high', 1.0), ('medium', 1.0), ('high', 0.18500000000000014)) 
According to the Credit Evaluation rule set The Credit evaluation has 
the following memberships: 
[('high', 1.0)] 
After defuzzification the credit has the following value: 
375.0 
The credit amount that can be given is: 375000.0$ 
-------------------------------------------------------------------------- 
