import numpy as np
from scipy.optimize import linear_sum_assignment


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
    row_ind, col_ind = linear_sum_assignment(cost)

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
