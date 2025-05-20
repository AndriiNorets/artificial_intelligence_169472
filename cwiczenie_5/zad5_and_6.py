from itertools import product

def implies(a, b):
    # a ⇒ b to znaczy: jeśli a, to b. W logice: ¬a ∨ b
    return (not a) or b

def zadanie_5():
    print("ZADANIE 5: Czy (p ⇒ q) |= ((p ∧ r) ⇒ q)?\n")
    print(f"{'p':<2}{'q':<2}{'r':<2} {'p⇒q':<6} {'(p∧r)⇒q':<10}")
    wynik = True

    for p, q, r in product([0, 1], repeat=3):
        left = implies(p, q)
        right = implies(p and r, q)
        print(f"{p:<2}{q:<2}{r:<2} {int(left):<6} {int(right):<10}")
        if left and not right:
            wynik = False

    if wynik:
        print("\nTak, wynikanie zachodzi: (p ⇒ q) |= ((p ∧ r) ⇒ q)")
    else:
        print("\nNie, są przypadki gdzie wynikanie nie zachodzi")

def zadanie_6(expr, vars_names):
    print(f"\nZADANIE 6: Analiza wyrażenia: {expr.__doc__}")
    rows = []
    all_vars = sorted(vars_names)
    print("Tabela prawdziwości:")
    print(" ".join(f"{v}" for v in all_vars) + " | wynik")

    for values in product([0, 1], repeat=len(all_vars)):
        env = dict(zip(all_vars, values))
        result = expr(**env)
        rows.append((env, result))
        row_str = " ".join(str(env[v]) for v in all_vars)
        print(f"{row_str} |   {int(result)}")

    # DNF: True
    dnf = []
    for env, result in rows:
        if result:
            terms = [f"{v}" if env[v] else f"¬{v}" for v in all_vars]
            dnf.append(f"({' ∧ '.join(terms)})")

    # CNF: False
    cnf = []
    for env, result in rows:
        if not result:
            terms = [f"¬{v}" if env[v] else f"{v}" for v in all_vars]
            cnf.append(f"({' ∨ '.join(terms)})")

    print("\nDNF:")
    print(" ∨ ".join(dnf) if dnf else "Formuła zawsze fałszywa — brak DNF")
    print("\nCNF:")
    print(" ∧ ".join(cnf) if cnf else "Formuła zawsze prawdziwa — brak CNF")

def formula_1(p, q):
    """(p ⇒ q) ⇒ (¬p ⇒ ¬q)"""
    return implies(implies(p, q), implies(not p, not q))

def formula_2(p, q, r):
    """(p ⇒ q) ⇒ ((p ∧ r) ⇒ q)"""
    return implies(implies(p, q), implies(p and r, q))

zadanie_5()
zadanie_6(formula_1, ['p', 'q'])
zadanie_6(formula_2, ['p', 'q', 'r'])
