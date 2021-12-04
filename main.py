from xml.dom.minidom import parse
import xml.dom.minidom
from pathlib import Path
from navec import Navec
import time

from natasha import (
    Segmenter,
    MorphVocab,
    
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    
    PER,
    NamesExtractor,

    Doc
)

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
names_extractor = NamesExtractor(morph_vocab)

path = 'D:\\Downloads\\navec_hudlit_v1_12B_500K_300d_100q.tar'
navec = Navec.load(path)

result = list(Path("D:\\Downloads\\RNC_million\\RNC_million\\sample_ar\\TEXTS").rglob("*.[xX][hH][tT][mM][lL]"))

intUnfamilliar = 0
intKnown = 0
wordCount = 0
accuracy = 0
isAdded = 0
total = 0

for i in range (0, len(result) - 1):
    print("opened " + str(result[i]))
    text = xml.dom.minidom.parse(str(result[i]))
    collection_node = text.firstChild
    for body in collection_node.childNodes:
        if (body.nodeType != body.TEXT_NODE and body.tagName == "body"):
            for p in body.childNodes:
                if (p.nodeType != p.TEXT_NODE and p.nodeType != p.COMMENT_NODE) and (p.tagName == "p" or p.tagName == "speach"):
                    for se in p.childNodes:
                        if (se.nodeType != se.TEXT_NODE and se.nodeType != p.COMMENT_NODE) and se.tagName == "se":
                            for word in se.childNodes:
                                if word.nodeType != word.TEXT_NODE and word.tagName == "w":
                                    if word.childNodes[1].nodeValue is not None:
                                        wordCount = wordCount + 1
                                        start = time.process_time()
                                        for ana in word.childNodes:
                                            if ana.nodeType != ana.TEXT_NODE and ana.tagName == "ana":
                                                if word.childNodes[1].nodeValue.lower().replace('`', '').replace(' ', '') in navec:
                                                    intKnown = intKnown + 1
                                                    text = word.childNodes[1].nodeValue.lower().replace('`', '').replace(' ', '')
                                                    doc = Doc(text)
                                                    doc.segment(segmenter)
                                                    doc.tag_morph(morph_tagger)
                                                    for token in doc.tokens:
                                                        token.lemmatize(morph_vocab)
                                                    if doc.tokens[0].lemma == ana.getAttribute('lex'):
                                                        accuracy = accuracy + 1
                                                else:
                                                    intUnfamilliar = intUnfamilliar + 1
                                        end = time.process_time() - start
                                        total = total + end


print("Всего слов " + str(wordCount))
print("Неизвесных " + str(intUnfamilliar))
print("В словаре " + str(intKnown))
print("Правильная начальная форма " + str(accuracy))
print("Точность" + str(accuracy/intKnown))
print("Затраченное время " + str(total))