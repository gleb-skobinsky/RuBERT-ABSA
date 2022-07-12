import pymorphy2
from pyphrasy.inflect import PhraseInflector

morph = pymorphy2.MorphAnalyzer()
inflector = PhraseInflector(morph)
form = 'gent'
phrase = 'мой автомобиль'
print(inflector.inflect(phrase, form))