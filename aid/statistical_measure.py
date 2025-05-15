# Here are the terms we use:
# - PUT: Program under test.
# - REF: Reference solution program. It is considered as ground truth.

# Let newly produced test be T.
# True positive: PUT(T.in) != T.out && REF(T.in) == T.out
# False positive: T.in is invalid || PUT(T.in) != T.out && PUT(T.in) == REF(T.in)
# False negative: PUT(T.in) != T.out && REF(T.in) != T.out

# Precision = (TP) / (TP + FP)
# Recall = (TP) / (TP + FN)
# F1 = 2 / ((1 / Precision) + (1 / Recall))

def produce_statistical_result() -> dict:
    precision = None
    recall = None
    f1 = None

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }