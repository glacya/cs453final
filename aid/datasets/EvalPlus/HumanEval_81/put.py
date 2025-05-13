
def numerical_letter_grade(grades):
    """It is the last week of the semester and the teacher has to give the grades
    to students. The teacher has been making her own algorithm for grading.
    The only problem is, she has lost the code she used for grading.
    She has given you a list of GPAs for some students and you have to write 
    a function that can output a list of letter grades using the following table:
             GPA       |    Letter grade
              4.0                A+
            > 3.7                A 
            > 3.3                A- 
            > 3.0                B+
            > 2.7                B 
            > 2.3                B-
            > 2.0                C+
            > 1.7                C
            > 1.3                C-
            > 1.0                D+ 
            > 0.7                D 
            > 0.0                D-
              0.0                E
    

    Example:
    grade_equation([4.0, 3, 1.7, 2, 3.5]) ==> ['A+', 'B', 'C-', 'C', 'A-']
    """
    grades = grades or []
    if not grades:
        return []
    letter_grades = [0] * len(grades)
    for i, grade in enumerate(grades):
        grade = round(grade, 1)
        if grade == 4.0:
            letter_grades[i] = 'A+'
        elif grade > 3.7:
            letter_grades[i] = 'A'
        elif grade > 3.3:
            letter_grades[i] = 'A-'
        elif grade > 3.0:
            letter_grades[i] = 'B+'
        elif grade > 2.7:
            letter_grades[i] = 'B'
        elif grade > 2.3:
            letter_grades[i] = 'B-'
        elif grade > 2.0:
            letter_grades[i] = 'C+'
        elif grade > 1.7:
            letter_grades[i] = 'C'
        elif grade > 1.3:
            letter_grades[i] = 'C-'
        elif grade > 1.0:
            letter_grades[i] = 'D+'
        elif grade > 0.7:
            letter_grades[i] = 'D'
        elif grade > 0.0:
            letter_grades[i] = 'D-'
        else:
            letter_grades[i] = 'E'
    return letter_grades
