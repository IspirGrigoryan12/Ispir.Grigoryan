import numpy as np

def hungarian_algorithm(cost: np.ndarray):
   
    n = cost.shape[0]
    m = cost.shape[1]
    size = max(n, m)

    # Քառակուսի մատրից — padding զրոներով
    C = np.zeros((size, size))
    C[:n, :m] = cost

    # Փուլ 1. Տողերի նվազագույնի հանում 
    for i in range(size):
        C[i] -= C[i].min()

    #  Փուլ 2. Սյունների նվազագույնի հանում 
    for j in range(size):
        C[:, j] -= C[:, j].min()

    # Կողային փոփոխականներ
    row_covered = np.zeros(size, dtype=bool)
    col_covered = np.zeros(size, dtype=bool)
    starred     = np.zeros((size, size), dtype=bool)  # ★ զրոներ
    primed      = np.zeros((size, size), dtype=bool)  # ′ զրոներ

    #  Փուլ 3. Անկախ զրոների նախնական 
    for i in range(size):
        for j in range(size):
            if C[i, j] == 0 and not row_covered[i] and not col_covered[j]:
                starred[i, j] = True
                row_covered[i] = True
                col_covered[j] = True

    row_covered[:] = False
    col_covered[:] = False

    def cover_starred_cols():
        """★ զրո ունեցող սյուները ծածկում ենք։"""
        col_covered[:] = False
        for j in range(size):
            if starred[:, j].any():
                col_covered[j] = True

    def find_uncovered_zero():
        """Գտնում է չծածկված զրո։"""
        for i in range(size):
            for j in range(size):
                if C[i, j] == 0 and not row_covered[i] and not col_covered[j]:
                    return i, j
        return -1, -1

    def find_starred_in_row(row):
        """Տողում ★ գտնում է։"""
        for j in range(size):
            if starred[row, j]:
                return j
        return -1

    def find_starred_in_col(col):
        """Սյունում ★ գտնում է։"""
        for i in range(size):
            if starred[i, col]:
                return i
        return -1

    def find_primed_in_row(row):
        """Տողում ′ գտնում է։"""
        for j in range(size):
            if primed[row, j]:
                return j
        return -1

    def augment_path(path):
        """★ և ′ փոխանակում է ճանապարհի երկայնքով։"""
        for i, j in path:
            if starred[i, j]:
                starred[i, j] = False
            else:
                starred[i, j] = True

    def step_adjust():
        """Չծածկված նվազագույնը հանում/գումարում է։"""
        min_val = np.inf
        for i in range(size):
            for j in range(size):
                if not row_covered[i] and not col_covered[j]:
                    if C[i, j] < min_val:
                        min_val = C[i, j]
        for i in range(size):
            for j in range(size):
                if row_covered[i]:
                    C[i, j] += min_val
                if not col_covered[j]:
                    C[i, j] -= min_val

    # Գլխավոր ցիկլ
    cover_starred_cols()

    while not col_covered.all():
        # Չծածկված զրո փնտրում
        while True:
            row, col = find_uncovered_zero()

            if row == -1:
                # Չկա չծածկված զրո → մատրիցը ճշգրտում ենք
                step_adjust()
                continue

            primed[row, col] = True
            starred_col = find_starred_in_row(row)

            if starred_col == -1:
                # ★ չկա այդ տողում → ճանապարհ կառուցում
                path = [(row, col)]
                while True:
                    starred_row = find_starred_in_col(path[-1][1])
                    if starred_row == -1:
                        break
                    path.append((starred_row, path[-1][1]))
                    primed_col = find_primed_in_row(starred_row)
                    path.append((starred_row, primed_col))

                augment_path(path)
                primed[:] = False
                row_covered[:] = False
                cover_starred_cols()
                break
            else:
                # ★ կա → ծածկում ենք տողը, բացում սյունը
                row_covered[row]        = True
                col_covered[starred_col] = False

    # ── Արդյունք ──
    rows_out, cols_out = [], []
    for i in range(n):
        for j in range(m):
            if starred[i, j]:
                rows_out.append(i)
                cols_out.append(j)

    return np.array(rows_out), np.array(cols_out)


def get_valid_int(prompt: str, min_val: int = 1) -> int:
    #Ստանում է դրական ամբողջ թիվ։
    while True:
        try:
            value = int(input(prompt))
            if value >= min_val:
                return value
            print(f"Սխալ։ Արժեքը պետք է լինի առնվազն {min_val}։")
        except ValueError:
            print("Սխալ։ Ներմուծեք ամբողջ թիվ։")

def get_choice() -> int:
    #Ստանում է 1 կամ 2 ընտրությունը։
    while True:
        choice = get_valid_int("Ընտրություն (1 կամ 2): ")
        if choice in (1, 2):
            return choice
        print("Սխալ։ Ներմուծեք 1 կամ 2։")

def get_matrix(rows: int, cols: int) -> np.ndarray:
    #Ստանում է մատրից՝ տող-առ-տող validation-ով։
    matrix = []
    print(f"\nՆերմուծեք {rows}×{cols} մատրիցի արժեքները:")
    for i in range(rows):
        while True:
            parts = input(f"  Տող {i+1}: ").strip().split()
            if len(parts) != cols:
                print(f"  Սխալ։ Պետք է լինի ուղիղ {cols} արժեք։")
                continue
            try:
                matrix.append(list(map(float, parts)))
                break
            except ValueError:
                print("  Սխալ։ Ներմուծեք միայն թվային արժեքներ։")
    return np.array(matrix)

def solve(matrix: np.ndarray, maximize: bool = False) -> dict:
    cost = -matrix if maximize else matrix.copy()

    # ← Միակ փոփոխությունը՝ scipy-ի փոխարեն մեր ֆունկցիան
    row_ind, col_ind = hungarian_algorithm(cost)

    assignments = [
        {
            "resource": int(r) + 1,
            "task":     int(c) + 1,
            "value":    float(matrix[r, c]),
        }
        for r, c in zip(row_ind, col_ind)
    ]
    return {
        "assignments": assignments,
        "total":       sum(a["value"] for a in assignments),
        "maximize":    maximize,
    }

def print_results(result: dict) -> None:
    #Արտածում է արդյունքները կառուցված ձևաչափով։
    mode_label  = "ԱՌԱՎԵԼԱԳՈՒՅՆ ՇԱՀՈՒՅԹ" if result["maximize"] else "ՆՎԱԶԱԳՈՒՅՆ ԾԱԽՍ"
    total_label = "Ընդհանուր շահույթ"    if result["maximize"] else "Ընդհանուր ծախս"
    print(f"\n{'='*50}")
    print(f"ՕՊՏԻՄԱԼ ԲԱՇԽՈՒՄ — {mode_label}")
    print(f"{'='*50}")
    print(f"  {'Ռեսուրս':<12} {'Առաջադրանք':<14} {'Արժեք':>8}")
    print(f"  {'-'*36}")
    for a in result["assignments"]:
        print(f"  {a['resource']:<12} {a['task']:<14} {a['value']:>8.2f}")
    print(f"{'─'*50}")
    print(f"  {total_label}: {result['total']:.2f}")
    print(f"{'='*50}")

def run() -> dict:
    print("\n--- Ռեսուրսների օպտիմալ բաշխման համակարգ ---")
    rows = get_valid_int("Ռեսուրսների քանակը: ")
    cols = get_valid_int("Առաջադրանքների քանակը: ")
    matrix = get_matrix(rows, cols)
    print("\nԽնդրի տեսակ:")
    print("  1 — Նվազագույն ծախս")
    print("  2 — Առավելագույն շահույթ")
    choice = get_choice()
    result = solve(matrix, maximize=(choice == 2))
    print_results(result)
    return result

if __name__ == "__main__":
    run()
