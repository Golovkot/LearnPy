import string
import re
from collections import Counter

f = open('wiki_00', 'r', encoding='utf-8')
r = open('FreqWordList.tsv', 'w', encoding='utf-8')

text = re.sub('</?doc.*>', '', f.read().lower())
words = text.split()
for i in range(len(words)):
    words[i] = words[i].strip(string.punctuation)
c = Counter(words)
del(c[''])
for word, count in c.most_common(len(c)):
    r.write("{0}  {1}\n".format(word, count))

f.close()
r.close()
