import unknotter as ut

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

def get_accuracy(knots: int, crossings: int, data_size: int, log: bool = False) -> float:
    if log: print('Reading codes from CSV file...')
    dataset = ut.read_to_list(f'training{knots}_{crossings}x.csv', data_size)
    if log: print('Done')

    labels = LabelEncoder().fit_transform([label for label, _ in dataset])

    if log: print('Fitting codes into matrix...')

    def pd_code_to_vector(code: ut.PDNotation, num_crossings: int):
        code = [edge for crossing in code for edge in crossing]
        if len(code) < num_crossings * 4:
            for _ in range(num_crossings - int(len(code)/4)):
                for _ in range(4): code.append(0)
        if len(code) > num_crossings * 4:
            raise Exception(f'knot has more than {crossings+1} crossings')
        return code

    codes: list[ut.PDNotation] = [code for _, code in dataset]
    codes = [pd_code_to_vector(code, crossings+1) for code in codes]

    if log: print('Done')

    code_train, code_test, label_train, label_test = train_test_split(
        codes, labels,
        test_size=0.2,
        shuffle=True,
        random_state=1,
    )

    clf = MLPClassifier(solver='sgd', alpha=1e-5, hidden_layer_sizes=[10, 10, 10], max_iter=1000)

    if log: print('Training...')
    clf.fit(code_train, label_train)
    if log: print('Done')

    if log: print('Predicting...')
    label_prediction = clf.predict(code_test)
    accuracy = accuracy_score(label_test, label_prediction)
    if log: print('Done')

    if log: print('Accuracy:', accuracy)
    return accuracy

for crossing_count in range(6, 20, 2):
    for knot_count in range(2, 6):
        accuracy = get_accuracy(knot_count, crossing_count, 50_000)
        print(f"{knot_count}k {crossing_count}x | {accuracy}")


# Remeasure accuracy

# successes = 0
# TRIALS = 1000
# for i in range(TRIALS):
#     unknot = ut.knot(0, 1)
#     while len(unknot.pd_code) < 8:
#         unknot = ut.apply_random_move(unknot, 0)

#     trefoil = ut.knot(3, 1)
#     while len(trefoil.pd_code) < 8:
#         trefoil = ut.apply_random_move(trefoil, 0)
    
#     # print([pd_code_to_vector(knot.pd_code, CROSSINGS+1) for knot in first_knots])
#     label_prediction = clf.predict([pd_code_to_vector(knot.pd_code, CROSSINGS+1) for knot in (unknot, trefoil)])
#     # print(label_prediction)
#     if label_prediction[0] == 0: successes += 1
#     if label_prediction[1] == 1: successes += 1
# print('Remeasured accuracy:', successes / (TRIALS*2))