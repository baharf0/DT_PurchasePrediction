import numpy as np
import pandas as pd
import math

read = pd.read_csv("file.csv")
file = read.drop(read.columns[0], axis=1)

p_yes = (file.iloc[:, -1] == 'yes').sum() / len(file)
p_no = (file.iloc[:, -1] == 'no').sum() / len(file)
table_yes = file.drop(file[file['buys_computer'] == 'no'].index)
table_no = file.drop(file[file['buys_computer'] == 'yes'].index)


def entropy(a):
    if a > 0:
        return - a * math.log2(a)
    else:
        return 0


h = entropy(p_yes) + entropy(p_no)
print("total entropy:", h)

# age
p_age_youth = (file['age'] == 'youth').sum() / len(file)
p_age_middle_aged = (file['age'] == 'middle-aged').sum() / len(file)
p_age_senior = (file['age'] == 'senior').sum() / len(file)

split_age = entropy(p_age_youth) + entropy(p_age_middle_aged) + entropy(p_age_senior)

# income
p_income_high = (file['income'] == 'high').sum() / len(file)
p_income_medium = (file['income'] == 'medium').sum() / len(file)
p_income_low = (file['income'] == 'low').sum() / len(file)
split_income = entropy(p_income_high) + entropy(p_income_medium) + entropy(p_income_low)

# student
p_student_yes = (file['student'] == 'yes').sum() / len(file)
p_student_no = (file['student'] == 'no').sum() / len(file)
split_student = entropy(p_student_yes) + entropy(p_student_no)

# credit_rating
p_credit_fair = (file['credit_rating'] == 'fair').sum() / len(file)
p_credit_excellent = (file['credit_rating'] == 'excellent').sum() / len(file)
split_credit = entropy(p_credit_fair) + entropy(p_credit_excellent)

# positive & negative
p_age_youth_yes = (table_yes['age'] == 'youth').sum() / (file['age'] == 'youth').sum()
p_age_middle_aged_yes = (table_yes['age'] == 'middle-aged').sum() / (file['age'] == 'middle-aged').sum()
p_age_senior_yes = (table_yes['age'] == 'senior').sum() / (file['age'] == 'senior').sum()
p_age_youth_no = (table_no['age'] == 'youth').sum() / (file['age'] == 'youth').sum()
p_age_middle_aged_no = (table_no['age'] == 'middle-aged').sum() / (file['age'] == 'middle-aged').sum()
p_age_senior_no = (table_no['age'] == 'senior').sum() / (file['age'] == 'senior').sum()

p_income_high_yes = (table_yes['income'] == 'high').sum() / (file['income'] == 'high').sum()
p_income_medium_yes = (table_yes['income'] == 'medium').sum() / (file['income'] == 'medium').sum()
p_income_low_yes = (table_yes['income'] == 'low').sum() / (file['income'] == 'low').sum()
p_income_high_no = (table_no['income'] == 'high').sum() / (file['income'] == 'high').sum()
p_income_medium_no = (table_no['income'] == 'medium').sum() / (file['income'] == 'medium').sum()
p_income_low_no = (table_no['income'] == 'low').sum() / (file['income'] == 'low').sum()

p_student_yes_yes = (table_yes['student'] == 'yes').sum() / (file['student'] == 'yes').sum()
p_student_no_yes = (table_yes['student'] == 'no').sum() / (file['student'] == 'no').sum()
p_student_yes_no = (table_no['student'] == 'yes').sum() / (file['student'] == 'yes').sum()
p_student_no_no = (table_no['student'] == 'no').sum() / (file['student'] == 'no').sum()

p_credit_excellent_yes = (table_yes['credit_rating'] == 'excellent').sum()/(file['credit_rating'] == 'excellent').sum()
p_credit_fair_yes = (table_yes['credit_rating'] == 'fair').sum() / (file['credit_rating'] == 'fair').sum()
p_credit_excellent_no = (table_no['credit_rating'] == 'excellent').sum() / (file['credit_rating'] == 'excellent').sum()
p_credit_fair_no = (table_no['credit_rating'] == 'fair').sum() / (file['credit_rating'] == 'fair').sum()

h_age = p_age_youth * (entropy(p_age_youth_yes) + entropy(p_age_youth_no)) + \
        p_age_middle_aged * (entropy(p_age_middle_aged_yes) + entropy(p_age_middle_aged_no)) + \
        p_age_senior * (entropy(p_age_senior_yes) + entropy(p_age_senior_no))
h_income = p_income_high * (entropy(p_income_high_yes) + entropy(p_income_high_no)) + \
           p_income_medium * (entropy(p_income_medium_yes) + entropy(p_income_medium_no)) +\
           p_income_low * (entropy(p_income_low_yes)+entropy(p_income_low_no))
h_student = p_student_yes * (entropy(p_student_yes_yes) + entropy(p_student_yes_no)) + \
            p_student_no * (entropy(p_student_no_yes) + entropy(p_student_no_no))
h_credit = p_credit_excellent * (entropy(p_credit_excellent_yes) + entropy(p_credit_excellent_no)) +\
           p_credit_fair * (entropy(p_credit_fair_yes) + entropy(p_credit_fair_no))

gain_age = h - h_age
gain_income = h - h_income
gain_student = h - h_student
gain_credit = h - h_credit

gain_ratio_age = gain_age / split_age
gain_ratio_income = gain_income / split_income
gain_ratio_student = gain_student / split_student
gain_ratio_credit = gain_credit / split_credit

dic = {'age': gain_ratio_age, 'income': gain_ratio_income,
       'student': gain_ratio_student, 'credit': gain_ratio_credit}
root = max(dic, key=dic.get)
print(dic)
print("root:", root)

###########

gain_age = -5/14 * math.log2(5/14) - 9/14 * math.log2(9/14)
gain_youth_income = gain_age - (2/5 * 0 + 2/5 * (-1/2 * math.log2(1/2) - 1/2 * math.log2(1/2)) + 1/5 * 0)
gain_youth_student = gain_age - 0
gain_youth_credit = gain_age - (3/5 * (-2/3 * math.log2(2/3) - 1/3 * math.log2(1/3)) +
                                (2/5 * -1/2 * math.log2(1/2) - 1/2 * math.log2(1/2)) + 1/5 * 0)

gain_youth_income_ratio = gain_youth_income / (-2/5 * math.log(2/5) + -2/5 * math.log(2/5) + -1/5 * math.log(1/5))
gain_youth_student_ratio = gain_youth_student / (-2/5 * math.log(2/5) + -3/5 * math.log(3/5))
gain_youth_credit_ratio = gain_youth_credit / (-3/5 * math.log(2/5) + -2/5 * math.log(2/5))

dic_youth = {'income': gain_youth_income_ratio, 'student': gain_youth_student_ratio,
             'credit': gain_youth_credit_ratio}
age_left = max(dic_youth, key=dic_youth.get)
print("age_left: youth - > ", age_left)
print("age_middle: middle-aged")

gain_senior_income = gain_age - (3/5 * (-2/3 * math.log2(2/3) - 1/3 * math.log2(1/3)) +
                                 (2/5 * -1/2 * math.log2(1/2) - 1/2 * math.log2(1/2)))
gain_senior_credit = gain_age - 0
gain_senior_income_ratio = gain_senior_income / (-3/5 * math.log(2/5) + -2/5 * math.log(2/5))
gain_senior_credit_ratio = gain_senior_credit / (-3/5 * math.log(2/5) + -2/5 * math.log(2/5))
dic_senior = {'income': gain_senior_income_ratio, 'credit': gain_senior_credit_ratio}
age_right = max(dic_senior, key=dic_senior.get)
print("age_right: senior - > ", age_right)






