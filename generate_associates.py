from dt import RDT
def get_syns(key_word, export_path):
        key_word = key_word.lower()
        list_of_replacements = []
        rdt = RDT(dt_pkl_fpath="rdt.pkl")
        with open(export_path, 'a', encoding='utf-8') as out_file:
            for i, (word, score) in enumerate(rdt.most_similar(key_word)):
                out_file.write(word + '\n')

get_syns("месторасположение", 'test.txt')
