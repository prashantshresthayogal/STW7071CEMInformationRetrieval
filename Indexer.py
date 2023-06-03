import ujson
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Downloading libraries to use their methods
nltk.download('stopwords')
nltk.download('punkt')

# Preprocessing data before indexing
with open('scraper_results.json', 'r', encoding='utf-8') as doc:
    scraper_results = doc.read()

pubName = []
pubURL = []
pubCUAuthor = []
pubDate = []
data_dict = ujson.loads(scraper_results)
array_length = len(data_dict)
print(array_length)

# Separate name, url, date, author into different lists
for item in data_dict:
    pubName.append(item["name"])
    pubURL.append(item["pub_url"])
    pubCUAuthor.append(item["cu_author"])
    pubDate.append(item["date"])
with open('pub_name.json', 'w') as f:
    ujson.dump(pubName, f)
with open('pub_url.json', 'w') as f:
    ujson.dump(pubURL, f)
with open('pub_cu_author.json', 'w') as f:
    ujson.dump(pubCUAuthor, f)
with open('pub_date.json', 'w') as f:
    ujson.dump(pubDate, f)


# Open a file with publication names in read mode
with open('pub_name.json', 'r') as f:
    publication = f.read()

# Load JSON File
pubName = ujson.loads(publication)

# Predefined stopwords in nltk are used
stop_words = stopwords.words('english')
stemmer = PorterStemmer()
pub_list_first_stem = []
pub_list = []
pub_list_wo_sc = []
print(len(pubName))

for file in pubName:
    # Splitting strings into tokens (words)
    words = word_tokenize(file)
    stem_word = ""
    for i in words:
        if i.lower() not in stop_words:
            stem_word += stemmer.stem(i) + " "
    pub_list_first_stem.append(stem_word)
    pub_list.append(file)

# Removing special characters
special_characters = '''!()-—[]{};:'"\, <>./?@#$%^&*_~0123456789+=’‘'''
for file in pub_list:
    word_wo_sc = ""
    if len(file.split()) == 1:
        pub_list_wo_sc.append(file)
    else:
        for a in file:
            if a in special_characters:
                word_wo_sc += ' '
            else:
                word_wo_sc += a
        pub_list_wo_sc.append(word_wo_sc)

# Stemming Process
pub_list_stem_wo_sw = []
for name in pub_list_wo_sc:
    words = word_tokenize(name)
    stem_word = ""
    for a in words:
        if a.lower() not in stop_words:
            stem_word += stemmer.stem(a) + ' '
    pub_list_stem_wo_sw.append(stem_word.lower())

data_dict = {}

# Indexing process
for a in range(len(pub_list_stem_wo_sw)):
    for b in pub_list_stem_wo_sw[a].split():
        if b not in data_dict:
            data_dict[b] = [a]
        else:
            data_dict[b].append(a)

print(len(pub_list_wo_sc))
print(len(pub_list_stem_wo_sw))
print(len(pub_list_first_stem))
print(len(pub_list))

with open('pub_list_stemmed.json', 'w') as f:
    ujson.dump(pub_list_first_stem, f)

with open('pub_indexed_dictionary.json', 'w') as f:
    ujson.dump(data_dict, f)
