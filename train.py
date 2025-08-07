import unknotter as ut
import sys

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

if len(sys.argv) not in [4, 5]:
    print("Expected `python3 training.py <data filename> <# knots> <# crossings> [<data size>]`.")
    sys.exit(1)

data_filename = sys.argv[1]
knot_count = int(sys.argv[2])
crossing_count = int(sys.argv[3])

# Read codes from CSV file
if len(sys.argv) == 4:
    dataset = ut.read_to_list(data_filename)
else:
    data_size = int(sys.argv[4])
    dataset = ut.read_to_list(data_filename, data_size)

labels = LabelEncoder().fit_transform([label for label, _ in dataset])

# Fit codes into matrix

def pd_code_to_vector(code: ut.PDNotation, num_crossings: int):
    code = [edge for crossing in code for edge in crossing]
    if len(code) < num_crossings * 4:
        for _ in range((num_crossings - int(len(code)/4)) * 4):
            code.append(0)
    if len(code) > num_crossings * 4:
        raise Exception(f'knot has more than {num_crossings} crossings')
    return code

codes: list[ut.PDNotation] = [code for _, code in dataset]
codes = [pd_code_to_vector(code, crossing_count+1) for code in codes]

code_train, code_test, label_train, label_test = train_test_split(
    codes, labels,
    test_size=0.2,
    shuffle=True,
    random_state=1,
)

clf = MLPClassifier(solver='sgd', alpha=1e-5, hidden_layer_sizes=[100, 100], max_iter=1000)

# Training

clf.fit(code_train, label_train)

# Predicting

label_prediction = clf.predict(code_test)
accuracy = accuracy_score(label_test, label_prediction)

print(f"{data_filename} | {accuracy}")
