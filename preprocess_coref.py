from insert_coref import resolve, coref_resolved, normalize_text
from tqdm import tqdm

all_texts = []
all_labels = []
with open('data\\location_train.tsv', encoding='utf-8') as file:
    length_of_file = len(file.readlines())
    file.close()
print(length_of_file)
with open('data\\location_train.tsv', encoding='utf-8') as file:
    for line in tqdm(file, total=length_of_file):
        text = line.rstrip().split('\t')[0]
        label = line.rstrip().split('\t')[1]
        output = resolve(text)
        resolved_text = coref_resolved(output)
        all_texts.append(normalize_text(resolved_text))
        all_labels.append(label)
    file.close()

with open('coref_resolved_data\\location_train.tsv', 'a', encoding='utf-8') as output:
    for text, label in zip(all_texts, all_labels):
        output.write(text + '\t' + label)
    output.close()
