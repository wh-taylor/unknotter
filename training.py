import unknotter as ut

CROSSINGS = 10
TRAINING_FILE = 'training2_10x.csv'

print('Reading codes from CSV file...')
dataset = ut.read_to_list(TRAINING_FILE)
print('Done')

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

labels = LabelEncoder().fit_transform([label for label, _ in dataset])

print('Fitting codes into matrix...')

def pd_code_to_vector(code: ut.PDNotation, num_crossings: int):
    code = [edge for crossing in code for edge in crossing]
    if len(code) < num_crossings * 4:
        for _ in range(num_crossings - int(len(code)/4)):
            for _ in range(4): code.append(0)
    if len(code) > num_crossings * 4:
        raise Exception(f'knot has more than {CROSSINGS+1} crossings')
    return code

codes: list[ut.PDNotation] = [code for _, code in dataset]
codes = [pd_code_to_vector(code, CROSSINGS+1) for code in codes]

print('Done')

code_train, code_test, label_train, label_test = train_test_split(
    codes, labels,
    test_size=0.2,
    shuffle=True,
    random_state=1,
)

clf = MLPClassifier(solver='sgd', alpha=1e-5, hidden_layer_sizes=[30, 30], max_iter=200)

print('Training...')
clf.fit(code_train, label_train)
print('Done')

print('Predicting...')
label_prediction = clf.predict(code_test)
accuracy = accuracy_score(label_test, label_prediction)
print('Done')

print('Accuracy:', accuracy)

# Remeasure accuracy

successes = 0
TRIALS = 100
for i in range(TRIALS):
    unknot = ut.knot(0, 1)
    while len(unknot.pd_code) < CROSSINGS:
        unknot = ut.apply_random_move(unknot, 0)

    trefoil = ut.knot(3, 1)
    while len(trefoil.pd_code) < CROSSINGS:
        trefoil = ut.apply_random_move(trefoil, 0)
    
    # print([pd_code_to_vector(knot.pd_code, CROSSINGS+1) for knot in first_knots])
    label_prediction = clf.predict([pd_code_to_vector(knot.pd_code, CROSSINGS+1) for knot in (unknot, trefoil)])
    # print(label_prediction)
    if label_prediction[0] == 0: successes += 1
    if label_prediction[1] == 1: successes += 1
print('Remeasured accuracy:', successes / (TRIALS*2))