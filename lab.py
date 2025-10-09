# lab.py


from pathlib import Path
import io
import pandas as pd
import numpy as np
np.set_printoptions(legacy='1.21')


# ---------------------------------------------------------------------
# QUESTION 0
# ---------------------------------------------------------------------


def consecutive_ints(ints):
    if len(ints) == 0:
        return False

    for k in range(len(ints) - 1):
        diff = abs(ints[k] - ints[k+1])
        if diff == 1:
            return True

    return False


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def median_vs_mean(nums):
    nums_sorted = sorted(nums)
    n = len(nums)
    
    if n % 2 == 1:  
        median = nums_sorted[n // 2]
    else:  
        median = (nums_sorted[n // 2 - 1] + nums_sorted[n // 2]) / 2
    
    mean = sum(nums) / n
    
    return median <= mean


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def n_prefixes(s, n):
    prefixes = [s[:i] for i in range(1, n + 1)]
    return "".join(prefixes[::-1])


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def exploded_numbers(ints, n):
    max_val = max(x + n for x in ints)
    width = len(str(max_val)) 
    
    result = []
    for x in ints:
        exploded = [str(i).zfill(width) for i in range(x - n, x + n + 1)]
        result.append(" ".join(exploded))
    
    return result


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def last_chars(fh):
    out = []
    for line in fh:
        if line.endswith("\n"):
            line = line[:-1]
        if line:       
            out.append(line[-1])
        else:
            out.append("")       
    return "".join(out)


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def add_root(A):
    indices = np.arange(len(A))       
    return A + np.sqrt(indices)

def where_square(A):
    roots = np.sqrt(A)
    return roots.astype(int)**2 == A


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def filter_cutoff_loop(matrix, cutoff):
    rows, cols = matrix.shape
    keep_cols = []
    
    for j in range(cols):
        col_sum = 0
        for i in range(rows):
            col_sum += matrix[i][j]
        col_mean = col_sum / rows
        
        if col_mean > cutoff:
            keep_cols.append([matrix[i][j] for i in range(rows)])

    if keep_cols:  
        return np.array(keep_cols).T
    else:
        return np.empty((rows, 0), dtype=matrix.dtype)


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def filter_cutoff_np(matrix, cutoff):
    col_means = np.mean(matrix, axis=0)    
    mask = col_means > cutoff             
    return matrix[:, mask]


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def growth_rates(A):
    rates = (A[1:] - A[:-1]) / A[:-1]
    return np.round(rates, 2)

def with_leftover(A):
    daily_leftover = np.mod(20, A)                 
    cumulative_leftover = np.cumsum(daily_leftover)
    hits = np.where(cumulative_leftover >= A)[0]
    return int(hits[0]) if hits.size else -1


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def salary_stats(salary):
    team_totals = salary.groupby('Team', dropna=False)['Salary'].sum()
    total_highest = team_totals.max()            

    duplicates = salary['Player'].duplicated(keep=False).any()

    return pd.Series({
        'total_highest': total_highest,          
        'duplicates': duplicates                
    })



# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def parse_malformed(fp):
    rows = []
    with open(fp, encoding="utf-8") as f:
        _ = f.readline()  

        for raw in f:
            line = raw.strip()
            if not line:
                continue

            parts = [p.strip() for p in line.replace('"', '').split(",")]

            fields = []
            rest = []
            for tok in parts:
                if len(fields) < 4:
                    if tok == "":
                        continue
                    fields.append(tok)
                else:
                    rest.append(tok)

            first, last, w_str, h_str = fields
            weight = float(w_str)
            height = float(h_str)
            geo = ",".join([r for r in rest if r != ""]).strip()

            rows.append([first, last, weight, height, geo])

    return pd.DataFrame(rows, columns=["first", "last", "weight", "height", "geo"])


