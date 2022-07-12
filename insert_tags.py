import spacy
from spacy.tokens import Doc
from tqdm import tqdm
nlp = spacy.load("ru_core_news_sm")

dataset_filepath = input('Enter name of the file:')

all_tags = []
if dataset_filepath == "location_train.tsv" or dataset_filepath == "location_test.tsv":
    terms_path = 'location_terms.txt'
elif dataset_filepath == "service_train.tsv" or dataset_filepath == "service_test.tsv":
    terms_path = 'service_terms.txt'
elif dataset_filepath == "room_train.tsv" or dataset_filepath == "room_test.tsv":
    terms_path = 'room_terms.txt'
else:
    print('Incorrect path to dataset. Options are: location_train.tsv, location_test.tsv, service_train.tsv, service_test.tsv, room_train.tsv, room_test.tsv')
    exit()
with open('tagging_terms\\' + terms_path, encoding='utf-8') as tags:
    for tag in tags:
        all_tags.append(tag.rstrip())

all_docs_in_dataset = []
all_labels_in_dataset = []
print('Reading and tagging data...')
with open('data\\' + dataset_filepath, encoding='utf-8') as train:
    total = len(train.readlines())
    train.close()

with open('data\\' + dataset_filepath, encoding='utf-8') as train:
    
    for index, row in tqdm(enumerate(train), total=total):
        text = row.split('\t')[0]
        label = row.split('\t')[1]
        all_labels_in_dataset.append(label)
        document = nlp(text)
        for token in document:
            if token.text in all_tags:
                new_words = ["<ASPECT> "+tok.text+" </ASPECT>" if tok.text==token.text else tok.text for tok in document]
                spaces = [bool(word.whitespace_) for word in document]
                document = Doc(document.vocab, words=new_words, spaces=spaces)
        all_docs_in_dataset.append(document)
    train.close()
assert len(all_docs_in_dataset) == len(all_labels_in_dataset)
print('Writing data...')
with open('tagged_data\\' + dataset_filepath, 'a', encoding='utf-8') as output:
    for doc, label in tqdm(zip(all_docs_in_dataset, all_labels_in_dataset), total=len(all_docs_in_dataset)):
        output.write(str(doc.text) + '\t' + label)
    output.close()
print("All done.")

        
    
