import pandas as pd

# edit these variables
GRADES_CSV = "database.csv"
EXAM_WEIGHT = 1
HOMEWORK_WEIGHT = 0
OUTPUT_CSV_NAME = "final_grades.csv"
NUM_EXTRA_CREDITS = 1
DROP_THIS_MANY_HOMEWORKS = 2
TOTAL_HOMEWORKS_TO_DROP = NUM_EXTRA_CREDITS + DROP_THIS_MANY_HOMEWORKS
HOMEWORK_ASSIGNMENT_PREFIXES = ["Homework", "Assignment"]
EXTRA_CREDIT_PREFIXES = ["Extra Credit"]

# do not edit below here
def compute_student_grade(row):
    homework_average = compute_student_hw_average(row)
    exam_average = compute_student_exam_average(row)
    return HOMEWORK_WEIGHT * homework_average + EXAM_WEIGHT * exam_average

def compute_student_hw_average(row):
    """
    Average all the data that is either homework or extra credit
    """
    homeworks = row.filter(regex=("(Homework|Extra).*"))
    homeworks_remove_invalid_cells = pd.to_numeric(homeworks, errors='coerce').fillna(0)
    to_keep = homeworks_remove_invalid_cells.nlargest(homeworks_remove_invalid_cells.size - TOTAL_HOMEWORKS_TO_DROP)
    print("hw")
    print(to_keep)
    print(to_keep.mean())
    return to_keep.mean()

def compute_student_exam_average(row):
    exams = row.filter(regex=("Exam.*"))
    exams_remove_invalid_cells = pd.to_numeric(exams, errors='coerce').fillna(0)
    to_keep = exams_remove_invalid_cells.nlargest(exams_remove_invalid_cells.size)
    print("exam")
    print(to_keep.mean())
    return to_keep.mean()


if __name__ == "__main__":
    df = pd.read_csv(GRADES_CSV)
    df['final'] = df.apply(compute_student_grade, axis=1)
    homework=df.filter(regex=("H.*"))
    df.to_csv(OUTPUT_CSV_NAME)
    print(df[['Last Name', 'final']])
