import pandas as pd
import sys

# edit these variables
GRADES_CSV = sys.argv[1]
print(GRADES_CSV)
EXAM_WEIGHT = 0.6
HOMEWORK_WEIGHT = 0.4
OUTPUT_CSV_NAME = "final_grades_202.csv"
NUM_EXTRA_CREDITS = 1
DROP_THIS_MANY_HOMEWORKS = 2
TOTAL_HOMEWORKS_TO_DROP = NUM_EXTRA_CREDITS + DROP_THIS_MANY_HOMEWORKS
HOMEWORK_ASSIGNMENT_PREFIXES = ["Homework", "Assignment"]
EXTRA_CREDIT_PREFIXES = ["Extra Credit"]
TOTAL_EXAMS_TO_DROP = 1

# do not edit below here
def compute_student_grade(row):
    homework_average = compute_student_hw_average(row)
    exam_average = compute_student_exam_average(row)
    return HOMEWORK_WEIGHT * homework_average + EXAM_WEIGHT * exam_average

def compute_student_hw_average(row):
    """
    Average all the data that is either homework or extra credit
    """
    homeworks = row.filter(regex=("(Assignment|Extra).*"))
    homeworks_remove_invalid_cells = pd.to_numeric(homeworks, errors='coerce').fillna(0)
    to_keep = homeworks_remove_invalid_cells.nlargest(homeworks_remove_invalid_cells.size - TOTAL_HOMEWORKS_TO_DROP)
    return to_keep.mean()

def compute_student_exam_average(row):
    exams = row.filter(regex=("Exam.*"))
    exams_remove_invalid_cells = pd.to_numeric(exams, errors='coerce').fillna(0)
    to_keep = exams_remove_invalid_cells.nlargest(exams_remove_invalid_cells.size - TOTAL_EXAMS_TO_DROP)
    return to_keep.mean()


"""
These are the numbers from the njcu website.
    https://www.njcu.edu/directories/offices-centers/registrar/grading-system
We round your grade to the nearest letter.
e.g. 3.9 is closer to A than it is to A-, so 3.9 is an A.

A (4.0)

A- (3.7)

B+ (3.3)

B (3.0)

B- (2.7)

C+ (2.3)

C (2.0)

C- (1.7)

D (1.0)

F (0.0)
"""
letter_grade_cutoffs = {}
letter_grade_cutoffs['A'] = (4.0 + 3.7) / 2
letter_grade_cutoffs['A-'] = (3.7 + 3.3) / 2
letter_grade_cutoffs['B+'] = (3.3 + 3.0) / 2
letter_grade_cutoffs['B'] = (3.0 + 2.7) / 2
letter_grade_cutoffs['B-'] = (2.7 + 2.3) / 2
letter_grade_cutoffs['C+'] = (2.3 + 2.0) / 2
letter_grade_cutoffs['C'] = (2.0 + 1.7) / 2
letter_grade_cutoffs['C-'] = (1.7 + 1.0) / 2
letter_grade_cutoffs['D'] = (1.0 + 0.0) / 2
letter_grade_cutoffs['F'] = 0.0

def number_to_letter(row):
    """
    Turn a number grade into a letter grade.
    Based on this:
    https://www.njcu.edu/directories/offices-centers/registrar/grading-system

    - first take the final grade and dive by 25 to get it in the [0,4.0] range instead of [0,100]
    - then use that scaled number and get a letter
    """
    scaled_grade = row['final'] / 25
    if(scaled_grade >= letter_grade_cutoffs['A']):
        return 'A'
    elif(scaled_grade >= letter_grade_cutoffs['A-']):
        return 'A-'
    elif(scaled_grade >= letter_grade_cutoffs['B+']):
        return 'B+'
    elif(scaled_grade >= letter_grade_cutoffs['B']):
        return 'B'
    elif(scaled_grade >= letter_grade_cutoffs['B-']):
        return 'B-'
    elif(scaled_grade >= letter_grade_cutoffs['C+']):
        return 'C+'
    elif(scaled_grade >= letter_grade_cutoffs['C']):
        return 'C'
    elif(scaled_grade >= letter_grade_cutoffs['C-']):
        return 'C-'
    elif(scaled_grade >= letter_grade_cutoffs['D']):
        return 'D'
    elif(scaled_grade >= letter_grade_cutoffs['F']):
        return 'F'
    else:
        return 'ERROR'

if __name__ == "__main__":
    df = pd.read_csv(GRADES_CSV)
    df['hw_average'] = df.apply(compute_student_hw_average, axis=1)
    df['exam_average'] = df.apply(compute_student_exam_average, axis=1)
    df['final'] = df.apply(compute_student_grade, axis=1)
    df['letter'] = df.apply(number_to_letter, axis=1)
    homework=df.filter(regex=("H.*"))
    df.to_csv(OUTPUT_CSV_NAME)
    print(df[['First Name','Last Name', 'letter']])
