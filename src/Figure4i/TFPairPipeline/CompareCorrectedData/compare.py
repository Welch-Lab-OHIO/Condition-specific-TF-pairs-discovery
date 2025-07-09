import pandas as pd
import sys

if __name__ == '__main__':

    corrected_contacts_path = sys.argv[1]
    old_contacts_path = sys.argv[2]

    corrected_contacts = pd.read_csv(corrected_contacts_path, sep='\t')
    old_contacts = pd.read_csv(old_contacts_path, sep='\t')

    correct_set = set(map(lambda x: f'{x[0]}-{x[1]}', corrected_contacts.values))
    old_set = set(map(lambda x: f'{x[0]}-{x[1]}', old_contacts.values))

    print('length of corrected contact set: ', len(correct_set))
    print('length of corrected contact set:', len(old_set))

    diff = abs(len(correct_set) - len(old_set)) / ((len(correct_set) + len(old_set)) / 2)
    print('percent difference: ', diff*100)

    same = 0
    for i in correct_set:
        if i in old_set:
            same += 1

    print('Percent of corrected contacts that are the same as the original contacts ', same / len(correct_set) * 100)
