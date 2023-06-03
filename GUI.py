import tkinter as tk
from tkinter import scrolledtext, messagebox
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import ujson
import webbrowser

# Initialize GUI
window = tk.Tk()
window.title("Publication Search")
window.geometry('1150x700')
window.configure(bg='#439A97')

# Load data and models
with open('pub_list_stemmed.json', 'r') as file:
    pub_list_first_stem = ujson.load(file)
with open('pub_indexed_dictionary.json', 'r') as file:
    pub_index = ujson.load(file)
with open('pub_name.json', 'r') as file:
    pub_name = ujson.load(file)
with open('pub_url.json', 'r') as file:
    pub_url = ujson.load(file)
with open('pub_cu_author.json', 'r') as file:
    pub_cu_author = ujson.load(file)
with open('pub_date.json', 'r') as file:
    pub_date = ujson.load(file)

# Initialize NLTK components
stemmer = PorterStemmer()
stop_words = stopwords.words('english')
tfidf = TfidfVectorizer()

# Function to perform publication search
def pub_qp_data():
    outputData.delete('1.0', tk.END)
    outcome.delete(0, tk.END)
    inputText = inputBar.get()
    abc = {}

    if operator.get() == 2:  # OR operator
        outputData.configure(fg='black')
        inputText = inputText.lower().split()
        pointer = []
        for token in inputText:
            if len(inputText) < 2:
                messagebox.showinfo(title="Hello There!!!", message="Please enter at least 2 words..")
                break
            if len(token) <= 3:
                messagebox.showinfo("Error!!!", "Please enter more than 4 characters.")
                break
            stem_temp = ""
            stem_word_file = []
            temp_file = []
            word_list = word_tokenize(token)

            for x in word_list:
                if x not in stop_words:
                    stem_temp += stemmer.stem(x) + " "
            stem_word_file.append(stem_temp)
            if pub_index.get(stem_word_file[0].strip()):
                pointer = pub_index.get(stem_word_file[0].strip())
            else:
                if len(inputText) == 1:
                    pointer = []

            if len(pointer) == 0:
                abc = {}
            else:
                for j in pointer:
                    temp_file.append(pub_list_first_stem[j])
                temp_file = tfidf.fit_transform(temp_file)
                cosine_output = cosine_similarity(temp_file, tfidf.transform(stem_word_file))

                if pub_index.get(stem_word_file[0].strip()):
                    for j in pointer:
                        abc[j] = cosine_output[pointer.index(j)]

    else:  # AND operator
        outputData.configure(fg='brown')
        inputText = inputText.lower().split()
        pointer = []
        match_word = []
        for token in inputText:
            if len(inputText) < 2:
                messagebox.showinfo("Error!!!", "Please enter at least 2 words to apply the operator.")
                break
            if len(token) <= 3:
                messagebox.showinfo("Error!!!", "Please enter more than 4 characters.")
                break
            temp_file = []
            set2 = set()
            stem_word_file = []
            word_list = word_tokenize(token)
            stem_temp = ""
            for x in word_list:
                if x not in stop_words:
                    stem_temp += stemmer.stem(x) + " "
            stem_word_file.append(stem_temp)
            if pub_index.get(stem_word_file[0].strip()):
                set1 = set(pub_index.get(stem_word_file[0].strip()))
                pointer.extend(list(set1))

                if match_word == []:
                    match_word = list({z for z in pointer if z in set2 or (set2.add(z) or False)})
                else:
                    match_word.extend(list(set1))
                    match_word = list({z for z in match_word if z in set2 or (set2.add(z) or False)})
            else:
                pointer = []

        if len(inputText) > 1:
            match_word = {z for z in match_word if z in set2 or (set2.add(z) or False)}

            if len(match_word) == 0:
                abc = {}
            else:
                for j in list(match_word):
                    temp_file.append(pub_list_first_stem[j])
                temp_file = tfidf.fit_transform(temp_file)
                cosine_output = cosine_similarity(temp_file, tfidf.transform(stem_word_file))

                for j in list(match_word):
                    abc[j] = cosine_output[list(match_word).index(j)]
        else:
            if len(pointer) == 0:
                abc = {}
            else:
                for j in pointer:
                    temp_file.append(pub_list_first_stem[j])
                temp_file = tfidf.fit_transform(temp_file)
                cosine_output = cosine_similarity(temp_file, tfidf.transform(stem_word_file))

                for j in pointer:
                    abc[j] = cosine_output[pointer.index(j)]

    aa = 0
    rank_sorting = sorted(abc.items(), key=lambda z: z[1], reverse=True)
    for a in rank_sorting:
        outputData.insert(tk.INSERT, "Rank: ")
        outputData.insert(tk.INSERT, "{:.2f}".format(a[1][0]))
        outputData.insert(tk.INSERT, "\n")
        outputData.insert(tk.INSERT, 'Title: ' + pub_name[a[0]] + "\n")
        outputData.insert(tk.INSERT, 'URL: ' + pub_url[a[0]] + "\n", 'link')
        outputData.insert(tk.INSERT, 'Date: ' + pub_date[a[0]] + "\n")
        outputData.insert(tk.INSERT, 'Cov_Uni_Author: ' + pub_cu_author[a[0]] + "\n")
        outputData.insert(tk.INSERT, "\n")
        aa += 1

    if aa == 0:
        messagebox.showinfo("Error!!!", "No results found. Please try again.")
    outcome.insert(tk.END, aa)


# Function to handle hyperlink redirection
def browse_url(event):
    widget = event.widget
    index = widget.index("@%s,%s" % (event.x, event.y))
    url = widget.get(index)
    if url.startswith('URL: '):
        url = url[5:]
    webbrowser.open(url)


# GUI elements
label = tk.Label(window, text="What Are You Looking For?", bg="#439A97", fg="white", font="Arial 24 bold")
label.place(x=50, y=20)

inputBar = tk.Entry(window, width=55,bg="#B9EDDD")
inputBar.place(x=55, y=75)

apply = tk.Label(window, text='APPLY :', bg="#439A97", fg="#321E1E", font="Arial 12 bold")
apply.place(x=650, y=50)

operator = tk.IntVar()
operator.set(2)
rb_and = tk.Radiobutton(window, text='AND',  bg="#577D86", fg="white", value=1, variable=operator, command=pub_qp_data,font="Arial 12 bold")
rb_or = tk.Radiobutton(window, text='OR', bg="#577D86", fg="white",  value=2, variable=operator, command=pub_qp_data, font="Arial 12 bold")
rb_and.place(x=730, y=50)
rb_or.place(x=800, y=50)

search = tk.Button(window, text='SEARCH', bg="#577D86", fg="white", font="Arial 10 bold", command=pub_qp_data)
search.place(x=410, y=70)

count = tk.Label(window, text='COUNT :', bg="#439A97", fg="#321E1E", font="Arial 12 bold")
count.place(x=650, y=85)

outcome = tk.Entry(window, width=10,bg="#B9EDDD")
outcome.place(x=730, y=87)

outputData = scrolledtext.ScrolledText(window, width=130, height=35,bg="#B9EDDD")
outputData.place(x=50, y=130)
outputData.tag_config('link', foreground='blue', underline=True)
outputData.bind("<Button-1>", browse_url)

# Run the GUI
window.mainloop()
