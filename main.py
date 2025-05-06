import pandas as pd

df = pd.DataFrame([
    ['wysoka', 'bliski', 'średni', 'tak'],
    ['wysoka', 'bliski', 'średni', 'tak'],
    ['wysoka', 'bliski', 'średni', 'tak'],
    ['więcej niż średnia', 'daleki', 'silny', 'nie pewne'],
    ['więcej niż średnia', 'daleki', 'silny', 'nie'],
    ['więcej niż średnia', 'daleki', 'lekki', 'nie'],
    ['wysoka', 'bliski', 'średni', 'tak'],
    ['więcej niż średnia', 'daleki', 'lekki', 'nie'],
    ['więcej niż średnia', 'daleki', 'lekki', 'tak'],
], columns=['a1', 'a2', 'a3', 'class'], index=[f'o{i+1}' for i in range(9)])

X1 = {'o1', 'o2', 'o3', 'o7', 'o9'}  # tak
X2 = {'o5', 'o6', 'o8'}             # nie

def get_equivalence_classes(df, attrs):
    return df.groupby(attrs).groups

def rough_approximations(objects, eq_classes):
    lower, upper = set(), set()
    for cls in eq_classes.values():
        cls_set = set(cls)
        if cls_set.issubset(objects):
            lower |= cls_set
        if cls_set & objects:
            upper |= cls_set
    return lower, upper

eq_A = get_equivalence_classes(df, ['a1', 'a2', 'a3'])
eq_B = get_equivalence_classes(df, ['a1', 'a2'])

X1_lower_A, X1_upper_A = rough_approximations(X1, eq_A)
X2_lower_A, X2_upper_A = rough_approximations(X2, eq_A)
X1_lower_B, X1_upper_B = rough_approximations(X1, eq_B)
X2_lower_B, X2_upper_B = rough_approximations(X2, eq_B)

def rule_accuracy(rule, df, target_class):
    if not rule:
        return 0, 0
    subset = df
    for attr, val in rule.items():
        subset = subset[subset[attr] == val]
    if subset.empty:
        return 0, 0
    total = len(subset)
    correct = len(subset[subset['class'] == target_class])
    return correct / total, total

def learn_one_rule(df, target_class, attributes):
    rule = {}
    attrs = attributes[:]
    while True:
        best_acc, best_attr, best_val, best_cov = -1, None, None, 0
        for attr in attrs:
            for val in df[attr].unique():
                trial = rule.copy()
                trial[attr] = val
                acc, cov = rule_accuracy(trial, df, target_class)
                if acc > best_acc or (acc == best_acc and cov > best_cov):
                    best_acc, best_attr, best_val, best_cov = acc, attr, val, cov
        if best_attr is None:
            break
        rule[best_attr] = best_val
        attrs.remove(best_attr)
        acc, _ = rule_accuracy(rule, df, target_class)
        if acc == 1.0:
            break
    return rule

def sequential_covering(df, target_class):
    rules = []
    attrs = [col for col in df.columns if col != 'class']
    remaining = df[df['class'] == target_class].copy()
    while not remaining.empty:
        rule = learn_one_rule(df, target_class, attrs)
        rules.append(rule)
        match = df
        for attr, val in rule.items():
            match = match[match[attr] == val]
        covered = match[match['class'] == target_class]
        df = df.drop(covered.index)
        remaining = remaining.drop(covered.index, errors='ignore')
    return rules

rules_tak = sequential_covering(df.copy(), 'tak')
rules_nie = sequential_covering(df.copy(), 'nie')

def print_rules(rules, target):
    print(f"\n🔹 Rules for class: '{target}'")
    for i, r in enumerate(rules, 1):
        conds = ' ∧ '.join([f"{k}={v}" for k, v in r.items()])
        print(f"Rule {i}: IF {conds} THEN class={target}")

print("📌 Rough Approximations (5):")

print(f"\nX1 (tak) w.r.t A:\n  Lower: {X1_lower_A}\n  Upper: {X1_upper_A}")
print(f"X2 (nie) w.r.t A:\n  Lower: {X2_lower_A}\n  Upper: {X2_upper_A}")

print(f"\nX1 (tak) w.r.t B:\n  Lower: {X1_lower_B}\n  Upper: {X1_upper_B}")
print(f"X2 (nie) w.r.t B:\n  Lower: {X2_lower_B}\n  Upper: {X2_upper_B}")

print_rules(rules_tak, 'tak')
print_rules(rules_nie, 'nie')
