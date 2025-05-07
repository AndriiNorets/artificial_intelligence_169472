import pandas as pd


data = [
    [1, 1, 1, 1, 3, 1, 1],  # o1
    [1, 1, 1, 1, 3, 2, 1],  # o2
    [1, 1, 1, 3, 2, 1, 0],  # o3
    [1, 1, 1, 3, 3, 2, 1],  # o4
    [1, 1, 2, 1, 2, 1, 0],  # o5
    [1, 1, 2, 1, 2, 2, 1],  # o6
    [1, 1, 2, 2, 3, 1, 0],  # o7
    [1, 1, 2, 2, 4, 1, 1],  # o8
]
columns = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'd']
df = pd.DataFrame(data, columns=columns, index=[f'o{i+1}' for i in range(8)])
df['d'] = df['d'].astype(str)


def rule_accuracy(rule, df, target_class):
    if not rule:
        return 0, 0
    subset = df
    for attr, val in rule.items():
        subset = subset[subset[attr] == val]
    if subset.empty:
        return 0, 0
    total = len(subset)
    correct = len(subset[subset['d'] == target_class])
    return correct / total, total

def learn_one_rule(df, target_class):
    rule = {}
    attrs = [c for c in df.columns if c != 'd']
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
    remaining = df[df['d'] == target_class].copy()
    while not remaining.empty:
        rule = learn_one_rule(df, target_class)
        if not rule:
            break
        rules.append(rule)
        match = df
        for attr, val in rule.items():
            match = match[match[attr] == val]
        covered = match[match['d'] == target_class]
        df = df.drop(covered.index)
        remaining = remaining.drop(covered.index, errors='ignore')
    return rules


rules_1 = sequential_covering(df.copy(), '1')
rules_0 = sequential_covering(df.copy(), '0')


def print_rules(rules, target):
    print(f"\n🔹 Rules for class '{target}':")
    for i, rule in enumerate(rules, 1):
        conds = ' ∧ '.join([f"{k}={v}" for k, v in rule.items()])
        print(f"Rule {i}: IF {conds} THEN d={target}")

print_rules(rules_1, '1')
print_rules(rules_0, '0')