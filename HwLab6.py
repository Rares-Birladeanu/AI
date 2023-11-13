import numpy as np


def read_dataset(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = [list(map(float, line.strip().split())) for line in lines]
    data = np.array(data)

    np.random.shuffle(data)

    train_data, test_data = data[:190], data[190:]

    train_features, train_labels = train_data[:, :-1], train_data[:, -1]
    test_features, test_labels = test_data[:, :-1], test_data[:, -1]

    train_labels_encoded = np.eye(3)[train_labels.astype(int) - 1]
    test_labels_encoded = np.eye(3)[test_labels.astype(int) - 1]

    return train_features, train_labels_encoded, test_features, test_labels_encoded


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))


file_path = 'seeds_dataset.txt'
train_features, train_labels, test_features, test_labels = read_dataset(file_path)

weights_input_hidden = np.random.uniform(-0.5, 0.5, (4, 7))
bias_hidden = np.zeros((4, 1))
weights_hidden_output = np.random.uniform(-0.5, 0.5, (3, 4))
bias_output = np.zeros((3, 1))
learn_rate = 0.1
epochs = 100

for epoch in range(epochs):
    for seed, lbl in zip(train_features, train_labels):
        seed.shape += (1,)
        lbl.shape += (1,)

        hidden_pre = bias_hidden + weights_input_hidden.dot(seed)
        hidden = sigmoid(hidden_pre)

        output_pre = bias_output + weights_hidden_output.dot(hidden)
        output = sigmoid(output_pre)

        error = output - lbl

        gradient = error * sigmoid_derivative(output_pre)
        weights_hidden_output -= learn_rate * gradient.dot(np.transpose(hidden))
        bias_output -= learn_rate * gradient

        gradient = np.transpose(weights_hidden_output).dot(gradient) * sigmoid_derivative(hidden_pre)
        weights_input_hidden -= learn_rate * gradient.dot(np.transpose(seed))
        bias_hidden -= learn_rate * gradient

    if epoch % 5 == 0:
        print(f"Epoch: {epoch}")

nr_correct = 0
for seed, lbl in zip(test_features, test_labels):
    seed.shape += (1,)
    lbl.shape += (1,)

    hidden_pre = bias_hidden + weights_input_hidden.dot(seed)
    hidden = sigmoid(hidden_pre)

    output_pre = bias_output + weights_hidden_output.dot(hidden)
    output = sigmoid(output_pre)

    if np.argmax(output) == np.argmax(lbl):
        nr_correct += 1

print(f"Test acc on test set: {round((nr_correct / test_features.shape[0]) * 100, 2)}%")
