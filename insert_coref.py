import jsonlines

from allennlp.predictors.predictor import Predictor
import allennlp_models.tagging
import rucoref
import re
import pymorphy2
from pyphrasy.inflect import PhraseInflector
morph = pymorphy2.MorphAnalyzer()
inflector = PhraseInflector(morph)
import spacy
from spacy.tokens import Span
nlp = spacy.load("ru_core_news_sm")
predictor = Predictor.from_path("RucocoAncor_rubertb_a150_s20_sw04.tar.gz")

"""
This code uses pyphrasy package (https://github.com/summerisgone/pyphrasy). However, as we made slight changes to this package,
we do not add it as a submodule.
"""

def resolve(text):
    
    output = predictor.predict(
        document=text
    )
    return output

def normalize_text(string):
    """ Text normalization from
    https://github.com/yoonkim/CNN_sentence/blob/23e0e1f735570/process_data.py
    as specified in Yao's paper.
    """
    
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip()


    

def align_inflection(mention, head_mention):

    def get_pymorphy_case(spacy_case, word):
        if spacy_case == 'Nom':
            pym_case = 'nomn'
            return pym_case
        elif spacy_case == 'Gen':
            pym_case = 'gent'
            return pym_case
        elif spacy_case == 'Dat':
            pym_case = 'datv'
            return pym_case
        elif spacy_case == 'Acc':
            pym_case = 'accs'
            return pym_case
        elif spacy_case == 'Ins':
            pym_case = 'ablt'
            return pym_case
        elif spacy_case == 'Loc':
            pym_case = 'loct'
            return pym_case
        else:
            print("Couldn't define case for word {}".format(word))
            return None
    try:
        root = [token for token in mention if len(list(token.subtree)) >= len(mention)][0]
    except IndexError:
        return mention.text
    try:
        spacy_case = root.morph.get("Case")[0]
        pymorphy_case = get_pymorphy_case(spacy_case, root.text)
        if pymorphy_case is not None:
            head_mention = inflector.inflect(head_mention.text, pymorphy_case)
            return head_mention
        else:
            return mention.text
    except IndexError:
        return mention.text

    

def coref_resolved(predictions):

    def get_head_mention(doc, cluster):
        head_offsets = cluster[0]
        head_mention = doc[head_offsets[0]:head_offsets[1]+1]
        return head_mention

    clusters = predictions["clusters"]
    document = predictions['document']
    document_string = " ".join(document)
    spacy_document = nlp(document_string)
    for cluster in clusters:
        head_mention = get_head_mention(spacy_document, cluster)
        for mention in cluster:
            this_mention = spacy_document[mention[0]:mention[1]+1]
            
            
            this_head_mention = align_inflection(this_mention, head_mention)
            document[mention[0]] = this_head_mention
            for i in range(mention[0] + 1, mention[1] + 1):
                document[i] = ''

    document = list(filter(('').__ne__, document))
    enddoc = ' '.join(document)

    return enddoc

if __name__ == '__main__':
    raw_text = input('Enter text: ')
    output = resolve(raw_text)
    resolved_text = coref_resolved(output)
    print(normalize_text(resolved_text))