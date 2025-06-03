def activation(dot_product):
    return 1 if dot_product > 0 else -1

def perceptron_learn(examples, weights, alpha=0.5, max_epochs=10):
    for epoch in range(max_epochs):
        print(f"\nEpoch {epoch + 1}")
        error_made = False
        for x_input, y_expected in examples:
            x_vec = [1] + x_input
            dot = sum(w * x for w, x in zip(weights, x_vec))
            output = activation(dot)
            print(f"  Input: {x_input}, Target: {y_expected}, Output: {output}")
            if output != y_expected:
                error_made = True
                for i in range(len(weights)):
                    delta_w = alpha * (y_expected - output) * x_vec[i]
                    weights[i] += delta_w
                    print(f"    w[{i}] updated by {delta_w:.2f} to {weights[i]:.2f}")
        if not error_made:
            print("  No errors, training completed.")
            break
    return weights

training_data = [
    ([0, 0], -1),
    ([0, 1], -1),
    ([1, 0],  1),
    ([1, 1], -1)
]

initial_weights = [0.5, 0.5, 0.5]

final_weights = perceptron_learn(training_data, initial_weights.copy())

print("\nFinal weights:", final_weights)
