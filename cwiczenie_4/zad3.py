import math
from collections import Counter

data = [
    {'Alternate': 'Yes', 'Bar': 'No', 'Friday/Saturday': 'No', 'Hungry': 'Yes', 'Patron': 'Some', 'Price': '$$$', 'Raining': 'No', 'Reservation': 'Yes', 'Type': 'French', 'WaitEstimate': '0-10', 'WillWait': 'Yes'}, # x1
    {'Alternate': 'Yes', 'Bar': 'No', 'Friday/Saturday': 'No', 'Hungry': 'Yes', 'Patron': 'Full', 'Price': '$', 'Raining': 'No', 'Reservation': 'No', 'Type': 'Thai', 'WaitEstimate': '30-60', 'WillWait': 'No'},  # x2
    {'Alternate': 'No', 'Bar': 'Yes', 'Friday/Saturday': 'No', 'Hungry': 'No', 'Patron': 'Some', 'Price': '$', 'Raining': 'No', 'Reservation': 'No', 'Type': 'Burger', 'WaitEstimate': '0-10', 'WillWait': 'Yes'}, # x3
    {'Alternate': 'Yes', 'Bar': 'No', 'Friday/Saturday': 'Yes', 'Hungry': 'Yes', 'Patron': 'Full', 'Price': '$', 'Raining': 'Yes', 'Reservation': 'No', 'Type': 'Thai', 'WaitEstimate': '10-30', 'WillWait': 'Yes'}, # x4
    {'Alternate': 'Yes', 'Bar': 'No', 'Friday/Saturday': 'Yes', 'Hungry': 'No', 'Patron': 'Full', 'Price': '$$$', 'Raining': 'No', 'Reservation': 'Yes', 'Type': 'French', 'WaitEstimate': '> 60', 'WillWait': 'No'},  # x5
    {'Alternate': 'No', 'Bar': 'Yes', 'Friday/Saturday': 'No', 'Hungry': 'Yes', 'Patron': 'Some', 'Price': '$$', 'Raining': 'Yes', 'Reservation': 'Yes', 'Type': 'Italian', 'WaitEstimate': '0-10', 'WillWait': 'Yes'}, # x6
    {'Alternate': 'No', 'Bar': 'Yes', 'Friday/Saturday': 'No', 'Hungry': 'No', 'Patron': 'None', 'Price': '$', 'Raining': 'Yes', 'Reservation': 'No', 'Type': 'Burger', 'WaitEstimate': '0-10', 'WillWait': 'No'},  # x7
    {'Alternate': 'No', 'Bar': 'No', 'Friday/Saturday': 'No', 'Hungry': 'Yes', 'Patron': 'Some', 'Price': '$$', 'Raining': 'Yes', 'Reservation': 'Yes', 'Type': 'Thai', 'WaitEstimate': '0-10', 'WillWait': 'Yes'}, # x8
    {'Alternate': 'No', 'Bar': 'Yes', 'Friday/Saturday': 'Yes', 'Hungry': 'No', 'Patron': 'Full', 'Price': '$', 'Raining': 'Yes', 'Reservation': 'No', 'Type': 'Burger', 'WaitEstimate': '> 60', 'WillWait': 'No'},  # x9
    {'Alternate': 'Yes', 'Bar': 'Yes', 'Friday/Saturday': 'Yes', 'Hungry': 'Yes', 'Patron': 'Full', 'Price': '$$$', 'Raining': 'No', 'Reservation': 'Yes', 'Type': 'Italian', 'WaitEstimate': '10-30', 'WillWait': 'No'}, # x10
    {'Alternate': 'No', 'Bar': 'No', 'Friday/Saturday': 'No', 'Hungry': 'No', 'Patron': 'None', 'Price': '$', 'Raining': 'No', 'Reservation': 'No', 'Type': 'Thai', 'WaitEstimate': '0-10', 'WillWait': 'No'},  # x11
    {'Alternate': 'Yes', 'Bar': 'Yes', 'Friday/Saturday': 'Yes', 'Hungry': 'Yes', 'Patron': 'Full', 'Price': '$', 'Raining': 'No', 'Reservation': 'No', 'Type': 'Burger', 'WaitEstimate': '30-60', 'WillWait': 'Yes'} # x12
]

# Atrybuty decyzyjne i predykat celowy
target_attribute = 'WillWait'
attributes = [
    'Alternate', 'Bar', 'Friday/Saturday', 'Hungry', 'Patron', 'Price',
    'Raining', 'Reservation', 'Type', 'WaitEstimate'
]


def calculate_entropy(data, target_attribute):
    """Oblicza entropię dla danej grupy danych."""
    if not data:
        return 0.0

    target_values = [d[target_attribute] for d in data]
    value_counts = Counter(target_values)
    total_count = len(target_values)
    entropy = 0.0

    for count in value_counts.values():
        probability = count / total_count
        if probability > 0:  # Zapobieganie log(0)
            entropy -= probability * math.log2(probability)
    return entropy


def calculate_gain(data, attribute, target_attribute):
    """Oblicza zysk informacyjny dla danego atrybutu."""
    total_entropy = calculate_entropy(data, target_attribute)
    attribute_values = [d[attribute] for d in data]
    unique_values = set(attribute_values)

    weighted_entropy = 0.0
    for value in unique_values:
        subset_data = [d for d in data if d[attribute] == value]
        subset_entropy = calculate_entropy(subset_data, target_attribute)
        weighted_entropy += (len(subset_data) / len(data)) * subset_entropy

    gain = total_entropy - weighted_entropy
    return gain


def get_majority_class(data, target_attribute):
    """Zwraca klasę większościową w zbiorze danych."""
    target_values = [d[target_attribute] for d in data]
    value_counts = Counter(target_values)
    return value_counts.most_common(1)[0][0]


def build_decision_tree(data, attributes, target_attribute, indent_level=0, first_call=True):
    """
    Buduje drzewo decyzyjne rekurencyjnie.
    `first_call`: flaga do wymuszenia wyboru atrybutu 'Patron' na pierwszym poziomie.
    """
    indent = "  " * indent_level

    # 1. Sprawdzenie warunków bazowych:
    # Jeśli wszystkie przykłady mają tę samą wartość atrybutu docelowego
    target_values = [d[target_attribute] for d in data]
    if len(set(target_values)) == 1:
        print(f"{indent}  -> Wszyskie przykłady należą do klasy '{target_values[0]}'. Tworzenie liścia.")
        return target_values[0]

    # Jeśli brak atrybutów do testowania
    if not attributes:
        majority_class = get_majority_class(data, target_attribute)
        print(
            f"{indent}  -> Brak dostępnych atrybutów. Wybór klasy większościowej: '{majority_class}'. Tworzenie liścia.")
        return majority_class

    # 2. Obliczenie entropii dla bieżącego zbioru danych
    current_entropy = calculate_entropy(data, target_attribute)
    print(f"\n{indent}--- Krok {indent_level + 1} ---")
    print(f"{indent}Dane w bieżącym węźle (liczba przykładów: {len(data)}):")
    counts = Counter(target_values)
    for k, v in counts.items():
        print(f"{indent}  - {target_attribute} = '{k}': {v} przykładów")
    print(f"{indent}Entropia bieżącego zbioru: {current_entropy:.3f}")

    best_attribute = None
    max_gain = -1

    # 3. Wybór najlepszego atrybutu
    if first_call:
        best_attribute = 'Patron'
        if best_attribute not in attributes:
            raise ValueError("Atrybut 'Patron' musi być dostępny w atrybutach początkowych.")

        # Oblicz gain dla 'Patron' dla celów wyświetlania
        gain_patron = calculate_gain(data, best_attribute, target_attribute)
        print(f"{indent}WYMUSZONY WYBÓR: Atrybut '{best_attribute}' (zysk informacyjny: {gain_patron:.3f})")
        max_gain = gain_patron  # Aktualizujemy max_gain, choć nie używany do wyboru

    else:
        print(f"{indent}Obliczanie zysku informacyjnego dla pozostałych atrybutów:")
        gains = {}
        for attr in attributes:
            gain = calculate_gain(data, attr, target_attribute)
            gains[attr] = gain
            print(f"{indent}  - Atrybut '{attr}': Zysk informacyjny = {gain:.3f}")
            if gain > max_gain:
                max_gain = gain
                best_attribute = attr

        if best_attribute is None:  # Should not happen if data is not pure and attributes exist
            majority_class = get_majority_class(data, target_attribute)
            print(
                f"{indent}  -> Nie znaleziono atrybutu z dodatnim zyskiem. Wybór klasy większościowej: '{majority_class}'. Tworzenie liścia.")
            return majority_class

        print(f"{indent}NAJLEPSZY ATRYBUT DO PODZIAŁU: '{best_attribute}' (Zysk informacyjny: {max_gain:.3f})")

    tree = {best_attribute: {}}
    remaining_attributes = [attr for attr in attributes if attr != best_attribute]

    # 4. Rekurencyjne budowanie poddrzew
    unique_values = sorted(list(set([d[best_attribute] for d in data])))
    for value in unique_values:
        subset_data = [d for d in data if d[best_attribute] == value]
        print(f"\n{indent}  Podwęzeł: '{best_attribute}' = '{value}' (liczba przykładów: {len(subset_data)})")
        if not subset_data:
            majority_class = get_majority_class(data, target_attribute)
            print(
                f"{indent}    -> Brak przykładów dla tej gałęzi. Wybór klasy większościowej z nadrzędnego węzła: '{majority_class}'. Tworzenie liścia.")
            tree[best_attribute][value] = majority_class
        else:
            tree[best_attribute][value] = build_decision_tree(
                subset_data, remaining_attributes, target_attribute, indent_level + 1, False
                # Nie jest to już pierwsze wywołanie
            )

    return tree


def print_tree(tree, indent=""):
    """Pomocnicza funkcja do ładnego wyświetlania drzewa."""
    if not isinstance(tree, dict):
        print(f"{indent}  -> {tree}")
        return

    for attribute, branches in tree.items():
        print(f"{indent}{attribute}:")
        for value, subtree in branches.items():
            print(f"{indent}  {value}:", end="")
            if isinstance(subtree, dict):
                print_tree(subtree, indent + "    ")
            else:
                print(f" {subtree}")


print("--- START BUDOWANIA DRZEWA DECYZYJNEGO ---")
decision_tree = build_decision_tree(data, list(attributes), target_attribute, first_call=True)
print("\n--- BUDOWA DRZEWA ZAKOŃCZONA ---")

print("\n--- OSTATECZNE DRZEWO DECYZYJNE ---")
print_tree(decision_tree)
