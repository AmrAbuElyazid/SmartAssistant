import nltk
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
st = StanfordNERTagger('./english.all.3class.distsim.crf.ser.gz', './stanford-ner.jar', encoding='utf-8')
text = "when is my next event Sam at Starbucks"
for sent in nltk.sent_tokenize(text):
    tokens = nltk.tokenize.word_tokenize(sent)
    tags = st.tag(tokens)
    name = []
    for tag in tags:
    	print(tag)
        # if tag[1]=='PERSON': name.append(tag[0])
    # name = " ".join(name)
# print(name)
