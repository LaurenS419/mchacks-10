import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import csv
import pandas as pd
from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request
import cohere
import pyttsx3
from fpdf import FPDF
import pdfminer.high_level
from io import StringIO
import ast
import requests
import base64
import os
os.chdir(r'/Users/laurenspee/Desktop/')


app = Flask(__name__)
cors = CORS(app)
names = ["Text", "Average Word Length", "Average Sentence Length",
         "Punctuation per Sentence", "Ratio of Unique Words to Total"]
stop = ["0o", "0s", "3a", "3b", "3d", "6b", "6o", "a", "a1", "a2", "a3", "a4", "ab", "able", "about", "above", "abst", "ac", "accordance", "according", "accordingly", "across", "act", "actually", "ad", "added", "adj", "ae", "af", "affected", "affecting", "affects", "after", "afterwards", "ag", "again", "against", "ah", "ain", "ain't", "aj", "al", "all", "allow", "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "ao", "ap", "apart", "apparently", "appear", "appreciate", "appropriate", "approximately", "ar", "are", "aren", "arent", "aren't", "arise", "around", "as", "a's", "aside", "ask", "asking", "associated", "at", "au", "auth", "av", "available", "aw", "away", "awfully", "ax", "ay", "az", "b", "b1", "b2", "b3", "ba", "back", "bc", "bd", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "bi", "bill", "biol", "bj", "bk", "bl", "bn", "both", "bottom", "bp", "br", "brief", "briefly", "bs", "bt", "bu", "but", "bx", "by", "c", "c1", "c2", "c3", "ca", "call", "came", "can", "cannot", "cant", "can't", "cause", "causes", "cc", "cd", "ce", "certain", "certainly", "cf", "cg", "ch", "changes", "ci", "cit", "cj", "cl", "clearly", "cm", "c'mon", "cn", "co", "com", "come", "comes", "con", "concerning", "consequently", "consider", "considering", "contain", "containing", "contains", "corresponding", "could", "couldn", "couldnt", "couldn't", "course", "cp", "cq", "cr", "cry", "cs", "c's", "ct", "cu", "currently", "cv", "cx", "cy", "cz", "d", "d2", "da", "date", "dc", "dd", "de", "definitely", "describe", "described", "despite", "detail", "df", "di", "did", "didn", "didn't", "different", "dj", "dk", "dl", "do", "does", "doesn", "doesn't", "doing", "don", "done", "don't", "down", "downwards", "dp", "dr", "ds", "dt", "du", "due", "during", "dx", "dy", "e", "e2", "e3", "ea", "each", "ec", "ed", "edu", "ee", "ef", "effect", "eg", "ei", "eight", "eighty", "either", "ej", "el", "eleven", "else", "elsewhere", "em", "empty", "en", "end", "ending", "enough", "entirely", "eo", "ep", "eq", "er", "es", "especially", "est", "et", "et-al", "etc", "eu", "ev", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "ey", "f", "f2", "fa", "far", "fc", "few", "ff", "fi", "fifteen", "fifth", "fify", "fill", "find", "fire", "first", "five", "fix", "fj", "fl", "fn", "fo", "followed", "following", "follows", "for", "former", "formerly", "forth", "forty", "found", "four", "fr", "from", "front", "fs", "ft", "fu", "full", "further", "furthermore", "fy", "g", "ga", "gave", "ge", "get", "gets", "getting", "gi", "give", "given", "gives", "giving", "gj", "gl", "go", "goes", "going", "gone", "got", "gotten", "gr", "greetings", "gs", "gy", "h", "h2", "h3", "had", "hadn", "hadn't", "happens", "hardly", "has", "hasn", "hasnt", "hasn't", "have", "haven", "haven't", "having", "he", "hed", "he'd", "he'll", "hello", "help", "hence", "her", "here", "hereafter", "hereby", "herein", "heres", "here's", "hereupon", "hers", "herself", "hes", "he's", "hh", "hi", "hid", "him", "himself", "his", "hither", "hj", "ho", "home", "hopefully", "how", "howbeit", "however", "how's", "hr", "hs", "http", "hu", "hundred", "hy", "i", "i2", "i3", "i4", "i6", "i7", "i8", "ia", "ib", "ibid", "ic", "id", "i'd", "ie", "if", "ig", "ignored", "ih", "ii", "ij", "il", "i'll", "im", "i'm", "immediate", "immediately", "importance", "important", "in", "inasmuch", "inc", "indeed", "index", "indicate", "indicated", "indicates", "information", "inner", "insofar", "instead", "interest", "into", "invention", "inward", "io", "ip", "iq", "ir", "is", "isn", "isn't", "it", "itd", "it'd", "it'll", "its", "it's", "itself", "iv", "i've", "ix", "iy", "iz", "j", "jj", "jr", "js", "jt", "ju", "just", "k", "ke", "keep", "keeps", "kept", "kg", "kj", "km", "know", "known", "knows", "ko", "l", "l2", "la", "largely", "last", "lately", "later", "latter", "latterly", "lb", "lc", "le", "least", "les", "less", "lest", "let", "lets", "let's", "lf", "like", "liked", "likely", "line", "little", "lj", "ll", "ll", "ln", "lo", "look", "looking", "looks", "los", "lr", "ls", "lt", "ltd", "m", "m2", "ma", "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "mightn", "mightn't", "mill", "million", "mine", "miss", "ml", "mn", "mo", "more", "moreover", "most", "mostly", "move", "mr", "mrs", "ms", "mt", "mu", "much", "mug", "must", "mustn", "mustn't", "my", "myself", "n", "n2", "na",
        "name", "namely", "nay", "nc", "nd", "ne", "near", "nearly", "necessarily", "necessary", "need", "needn", "needn't", "needs", "neither", "never", "nevertheless", "new", "next", "ng", "ni", "nine", "ninety", "nj", "nl", "nn", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "novel", "now", "nowhere", "nr", "ns", "nt", "ny", "o", "oa", "ob", "obtain", "obtained", "obviously", "oc", "od", "of", "off", "often", "og", "oh", "oi", "oj", "ok", "okay", "ol", "old", "om", "omitted", "on", "once", "one", "ones", "only", "onto", "oo", "op", "oq", "or", "ord", "os", "ot", "other", "others", "otherwise", "ou", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "ow", "owing", "own", "ox", "oz", "p", "p1", "p2", "p3", "page", "pagecount", "pages", "par", "part", "particular", "particularly", "pas", "past", "pc", "pd", "pe", "per", "perhaps", "pf", "ph", "pi", "pj", "pk", "pl", "placed", "please", "plus", "pm", "pn", "po", "poorly", "possible", "possibly", "potentially", "pp", "pq", "pr", "predominantly", "present", "presumably", "previously", "primarily", "probably", "promptly", "proud", "provides", "ps", "pt", "pu", "put", "py", "q", "qj", "qu", "que", "quickly", "quite", "qv", "r", "r2", "ra", "ran", "rather", "rc", "rd", "re", "readily", "really", "reasonably", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "research-articl", "respectively", "resulted", "resulting", "results", "rf", "rh", "ri", "right", "rj", "rl", "rm", "rn", "ro", "rq", "rr", "rs", "rt", "ru", "run", "rv", "ry", "s", "s2", "sa", "said", "same", "saw", "say", "saying", "says", "sc", "sd", "se", "sec", "second", "secondly", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "sf", "shall", "shan", "shan't", "she", "shed", "she'd", "she'll", "shes", "she's", "should", "shouldn", "shouldn't", "should've", "show", "showed", "shown", "showns", "shows", "si", "side", "significant", "significantly", "similar", "similarly", "since", "sincere", "six", "sixty", "sj", "sl", "slightly", "sm", "sn", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "sp", "specifically", "specified", "specify", "specifying", "sq", "sr", "ss", "st", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure", "sy", "system", "sz", "t", "t1", "t2", "t3", "take", "taken", "taking", "tb", "tc", "td", "te", "tell", "ten", "tends", "tf", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that's", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "there's", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'd", "they'll", "theyre", "they're", "they've", "thickv", "thin", "think", "third", "this", "thorough", "thoroughly", "those", "thou", "though", "thoughh", "thousand", "three", "throug", "through", "throughout", "thru", "thus", "ti", "til", "tip", "tj", "tl", "tm", "tn", "to", "together", "too", "took", "top", "toward", "towards", "tp", "tq", "tr", "tried", "tries", "truly", "try", "trying", "ts", "t's", "tt", "tv", "twelve", "twenty", "twice", "two", "tx", "u", "u201d", "ue", "ui", "uj", "uk", "um", "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "uo", "up", "upon", "ups", "ur", "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "ut", "v", "va", "value", "various", "vd", "ve", "ve", "very", "via", "viz", "vj", "vo", "vol", "vols", "volumtype", "vq", "vs", "vt", "vu", "w", "wa", "want", "wants", "was", "wasn", "wasnt", "wasn't", "way", "we", "wed", "we'd", "welcome", "well", "we'll", "well-b", "went", "were", "we're", "weren", "werent", "weren't", "we've", "what", "whatever", "what'll", "whats", "what's", "when", "whence", "whenever", "when's", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "where's", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever", "whos", "who's", "whose", "why", "why's", "wi", "widely", "will", "willing", "wish", "with", "within", "without", "wo", "won", "wonder", "wont", "won't", "words", "world", "would", "wouldn", "wouldnt", "wouldn't", "www", "x", "x1", "x2", "x3", "xf", "xi", "xj", "xk", "xl", "xn", "xo", "xs", "xt", "xv", "xx", "y", "y2", "yes", "yet", "yj", "yl", "you", "youd", "you'd", "you'll", "your", "youre", "you're", "yours", "yourself", "yourselves", "you've", "yr", "ys", "yt", "z", "zero", "zi", "zz"]


app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/pdf-analysis', methods=['POST'])
@cross_origin()
def pdf_analysis():
    print("te")
    file = request.files['files']  # a multidict containing POST data
    print(file)
    filepath = '/Users/laurenspee/Desktop/' + 'testfile.pdf'
    file.save(filepath)

    try:
        new_filename, text = textpdf_to_txt(filepath)

        # if text==    ---------- :
        #   text=ocr_pdf_to_text(filename)
    except:
        new_filename, text = textpdf_to_txt(filepath)

    text_to_speech(text)

    reading_speed = 238  # check this value non-fiction
    word_count = word_counter(text)
    time_to_read = reading_time(word_count, reading_speed)
    summary = cohere_summary(text)
    bottom_text = 'Word count: ' + str(word_count)
    generate_plots(text)
    final_pdf_name = makePDF('filename', summary, 'Word count = ' + str(word_count), 'graph1.png',
                             'graph2.png', 'graph3.png', 'graph4.png', time_to_read)

    return text


@app.route('/get_pdf_image')
def ocr_pdf_to_text(filename):
    url = "https://app.nanonets.com/api/v2/OCR/FullText"

    payload = {'urls': ['MY_IMAGE_URL']}
    files = [
        ('file', (filename, open(filename)))
    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files,
                                auth=requests.auth.HTTPBasicAuth('8b819689-9f3b-11ed-a60f-ba1ca0caa142', ''))
    data = response.text
    data = ast.literal_eval(data)
    enter_results = data['results']
    enter_page_data = enter_results[0]['page_data']
    text = enter_page_data[0]['raw_text']
    return text


@app.route('/get_pdf_text')
def textpdf_to_txt(filename):
    text = pdfminer.high_level.extract_text(filename)
    new_filename = filename[:(len(filename)-3)]+'txt'
    fobj = open(new_filename+'.txt', 'w')
    fobj.write(text)
    fobj.close()
    return new_filename, text


def text_to_speech(text):
    engine = pyttsx3.init()
    # /Users/laurenspee/Desktop/
    engine.save_to_file(text, "pdfAudio.mp3")
    engine.runAndWait()


def word_counter(text):

    # gets rid of uppers
    text = text.lower()

    # gets rid of bad characters
    removelist = [',', '.', '<', '>', '?', '/', ':', ';', '"', '[', ']', '{', '}', '_', '+', '=', '\\', '|',
                  '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', "'"]
    for i in removelist:
        text = text.replace(i, '')
    text = text.replace("\n", " ")
    text = text.replace("  ", " ")

    # makes a list
    text_list = text.split(" ")

    # removes empty strings
    empty = ''
    while empty in text_list:
        text_list.remove(empty)

    word_count = len(text_list)

    return word_count


def reading_time(word_count, reading_speed):
    minutes_taken = word_count/reading_speed
    hours = 0
    while minutes_taken > 60:
        hours += 1
        minutes_taken -= 60
    return str(hours) + ' hours and ' + str(minutes_taken) + ' minutes'


def cohere_summary(text):
    if len(text) > 500:
        text = text[:500]
    co = cohere.Client('M56z1g38WE83LZuXxzIjrtpO4oo99Ez9p7J7w3bW')

    response = co.generate(
        prompt=text,
        max_tokens=100,  # figure out number of tokens
        temperature=0.8,
        stop_sequences=["--"])

    return ("Summary: {}".format(response.generations[0].text))

########


def makePDF(input_filename, summary, bottom_text, punctuation_filename, avg_word_length_filename, unique_word_types_filename, sentence_length_filename, reading_time):

    font = 'Arial'
    pdf = FPDF()
    pdf.add_page()

    # make a title
    pdf.set_font(font, 'B', 30)
    #        x,y , text
    pdf.set_text_color(129, 179, 210)
    pdf.text(25, 25, 'ANALYSIS REPORT')
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(font, 'B', 16)
    max_chars_in_one_line = 70

    y_spacing = 7

    # makes it so that any text entered fits on a line or is moved onto the next line
    text = summary
    text_lst = []
    while len(text) > max_chars_in_one_line:
        counter = max_chars_in_one_line
        while text[counter] != ' ':
            counter -= 1
        text1 = text[0:counter] + '\n'
        text = text[counter:]
        text_lst.append(text1)
    text_lst.append(text)

    # make the top text; max characters: 300
    y = 45
    x = 25
    pdf.text(x, y, 'Summary:')
    y += y_spacing+8
    pdf.set_font(font, 'B', 14)
    pdf.set_font('')
    for i in range(len(text_lst)):
        while text_lst[i][0] == ' ':
            text_lst[i] = text_lst[i][1:]
        pdf.text(x, y+y_spacing*i, text_lst[i])

    # print the reading time
    y += 10
    y_reading_time = len(text_lst)*y_spacing+y
    pdf.text(x, y_reading_time,
             'The average reading time for this document is: ' + reading_time)

    #       obj.image(filename,x,y,size)
    image_size = 75
    image_y = 122
    pdf.image(punctuation_filename, 25, image_y, image_size)
    # Image 2
    pdf.image(avg_word_length_filename, 110, image_y, image_size)
    # Image 3
    pdf.image(unique_word_types_filename, 25, image_y+50, image_size)
    # Image 4
    pdf.image(sentence_length_filename, 110, image_y+50, image_size)

    # bottom text -- make it fit; max number of characters is 200
    if len(bottom_text) > 350:
        bottom_text = bottom_text[:350] + " -- character maximum reached --"

    bottom_text_lst = []
    while len(bottom_text) > max_chars_in_one_line:
        counter = max_chars_in_one_line
        while bottom_text[counter] != ' ':
            counter -= 1
        bottom_text1 = bottom_text[0:counter] + '\n'
        bottom_text = bottom_text[counter:]
        bottom_text_lst.append(bottom_text1)

    bottom_text_lst.append(bottom_text)

    y = 240

    for i in range(len(bottom_text_lst)):
        while bottom_text_lst[i][0] == ' ':
            bottom_text_lst[i] = bottom_text_lst[i][1:]
        pdf.text(x, y+y_spacing*i, bottom_text_lst[i])

    # output the pdf
    output_filename = 'Analysis PDF of ' + input_filename + '.pdf'
    pdf.output(output_filename, 'F')

    return output_filename


# df = pd.read_csv("table.csv", header=None)
# mylist = list(df.values)
# print(df.values)
def starting_png_generation():
    global title, word, sentence, punc, ttr
    title = 1
    word = 1
    sentence = 1
    punc = 1
    ttr = 1

    names = ["Text", "Average Word Length", "Average Sentence Length",
             "Punctuation per Sentence", "Ratio of Unique Words to Total"]
    # list of stopwords
    stop = ["0o", "0s", "3a", "3b", "3d", "6b", "6o", "a", "a1", "a2", "a3", "a4", "ab", "able", "about", "above", "abst", "ac", "accordance", "according", "accordingly", "across", "act", "actually", "ad", "added", "adj", "ae", "af", "affected", "affecting", "affects", "after", "afterwards", "ag", "again", "against", "ah", "ain", "ain't", "aj", "al", "all", "allow", "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "ao", "ap", "apart", "apparently", "appear", "appreciate", "appropriate", "approximately", "ar", "are", "aren", "arent", "aren't", "arise", "around", "as", "a's", "aside", "ask", "asking", "associated", "at", "au", "auth", "av", "available", "aw", "away", "awfully", "ax", "ay", "az", "b", "b1", "b2", "b3", "ba", "back", "bc", "bd", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "bi", "bill", "biol", "bj", "bk", "bl", "bn", "both", "bottom", "bp", "br", "brief", "briefly", "bs", "bt", "bu", "but", "bx", "by", "c", "c1", "c2", "c3", "ca", "call", "came", "can", "cannot", "cant", "can't", "cause", "causes", "cc", "cd", "ce", "certain", "certainly", "cf", "cg", "ch", "changes", "ci", "cit", "cj", "cl", "clearly", "cm", "c'mon", "cn", "co", "com", "come", "comes", "con", "concerning", "consequently", "consider", "considering", "contain", "containing", "contains", "corresponding", "could", "couldn", "couldnt", "couldn't", "course", "cp", "cq", "cr", "cry", "cs", "c's", "ct", "cu", "currently", "cv", "cx", "cy", "cz", "d", "d2", "da", "date", "dc", "dd", "de", "definitely", "describe", "described", "despite", "detail", "df", "di", "did", "didn", "didn't", "different", "dj", "dk", "dl", "do", "does", "doesn", "doesn't", "doing", "don", "done", "don't", "down", "downwards", "dp", "dr", "ds", "dt", "du", "due", "during", "dx", "dy", "e", "e2", "e3", "ea", "each", "ec", "ed", "edu", "ee", "ef", "effect", "eg", "ei", "eight", "eighty", "either", "ej", "el", "eleven", "else", "elsewhere", "em", "empty", "en", "end", "ending", "enough", "entirely", "eo", "ep", "eq", "er", "es", "especially", "est", "et", "et-al", "etc", "eu", "ev", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "ey", "f", "f2", "fa", "far", "fc", "few", "ff", "fi", "fifteen", "fifth", "fify", "fill", "find", "fire", "first", "five", "fix", "fj", "fl", "fn", "fo", "followed", "following", "follows", "for", "former", "formerly", "forth", "forty", "found", "four", "fr", "from", "front", "fs", "ft", "fu", "full", "further", "furthermore", "fy", "g", "ga", "gave", "ge", "get", "gets", "getting", "gi", "give", "given", "gives", "giving", "gj", "gl", "go", "goes", "going", "gone", "got", "gotten", "gr", "greetings", "gs", "gy", "h", "h2", "h3", "had", "hadn", "hadn't", "happens", "hardly", "has", "hasn", "hasnt", "hasn't", "have", "haven", "haven't", "having", "he", "hed", "he'd", "he'll", "hello", "help", "hence", "her", "here", "hereafter", "hereby", "herein", "heres", "here's", "hereupon", "hers", "herself", "hes", "he's", "hh", "hi", "hid", "him", "himself", "his", "hither", "hj", "ho", "home", "hopefully", "how", "howbeit", "however", "how's", "hr", "hs", "http", "hu", "hundred", "hy", "i", "i2", "i3", "i4", "i6", "i7", "i8", "ia", "ib", "ibid", "ic", "id", "i'd", "ie", "if", "ig", "ignored", "ih", "ii", "ij", "il", "i'll", "im", "i'm", "immediate", "immediately", "importance", "important", "in", "inasmuch", "inc", "indeed", "index", "indicate", "indicated", "indicates", "information", "inner", "insofar", "instead", "interest", "into", "invention", "inward", "io", "ip", "iq", "ir", "is", "isn", "isn't", "it", "itd", "it'd", "it'll", "its", "it's", "itself", "iv", "i've", "ix", "iy", "iz", "j", "jj", "jr", "js", "jt", "ju", "just", "k", "ke", "keep", "keeps", "kept", "kg", "kj", "km", "know", "known", "knows", "ko", "l", "l2", "la", "largely", "last", "lately", "later", "latter", "latterly", "lb", "lc", "le", "least", "les", "less", "lest", "let", "lets", "let's", "lf", "like", "liked", "likely", "line", "little", "lj", "ll", "ll", "ln", "lo", "look", "looking", "looks", "los", "lr", "ls", "lt", "ltd", "m", "m2", "ma", "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "mightn", "mightn't", "mill", "million", "mine", "miss", "ml", "mn", "mo", "more", "moreover", "most", "mostly", "move", "mr", "mrs", "ms", "mt", "mu", "much", "mug", "must", "mustn", "mustn't", "my", "myself", "n", "n2", "na",
            "name", "namely", "nay", "nc", "nd", "ne", "near", "nearly", "necessarily", "necessary", "need", "needn", "needn't", "needs", "neither", "never", "nevertheless", "new", "next", "ng", "ni", "nine", "ninety", "nj", "nl", "nn", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "novel", "now", "nowhere", "nr", "ns", "nt", "ny", "o", "oa", "ob", "obtain", "obtained", "obviously", "oc", "od", "of", "off", "often", "og", "oh", "oi", "oj", "ok", "okay", "ol", "old", "om", "omitted", "on", "once", "one", "ones", "only", "onto", "oo", "op", "oq", "or", "ord", "os", "ot", "other", "others", "otherwise", "ou", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "ow", "owing", "own", "ox", "oz", "p", "p1", "p2", "p3", "page", "pagecount", "pages", "par", "part", "particular", "particularly", "pas", "past", "pc", "pd", "pe", "per", "perhaps", "pf", "ph", "pi", "pj", "pk", "pl", "placed", "please", "plus", "pm", "pn", "po", "poorly", "possible", "possibly", "potentially", "pp", "pq", "pr", "predominantly", "present", "presumably", "previously", "primarily", "probably", "promptly", "proud", "provides", "ps", "pt", "pu", "put", "py", "q", "qj", "qu", "que", "quickly", "quite", "qv", "r", "r2", "ra", "ran", "rather", "rc", "rd", "re", "readily", "really", "reasonably", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "research-articl", "respectively", "resulted", "resulting", "results", "rf", "rh", "ri", "right", "rj", "rl", "rm", "rn", "ro", "rq", "rr", "rs", "rt", "ru", "run", "rv", "ry", "s", "s2", "sa", "said", "same", "saw", "say", "saying", "says", "sc", "sd", "se", "sec", "second", "secondly", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "sf", "shall", "shan", "shan't", "she", "shed", "she'd", "she'll", "shes", "she's", "should", "shouldn", "shouldn't", "should've", "show", "showed", "shown", "showns", "shows", "si", "side", "significant", "significantly", "similar", "similarly", "since", "sincere", "six", "sixty", "sj", "sl", "slightly", "sm", "sn", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "sp", "specifically", "specified", "specify", "specifying", "sq", "sr", "ss", "st", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure", "sy", "system", "sz", "t", "t1", "t2", "t3", "take", "taken", "taking", "tb", "tc", "td", "te", "tell", "ten", "tends", "tf", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that's", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "there's", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'd", "they'll", "theyre", "they're", "they've", "thickv", "thin", "think", "third", "this", "thorough", "thoroughly", "those", "thou", "though", "thoughh", "thousand", "three", "throug", "through", "throughout", "thru", "thus", "ti", "til", "tip", "tj", "tl", "tm", "tn", "to", "together", "too", "took", "top", "toward", "towards", "tp", "tq", "tr", "tried", "tries", "truly", "try", "trying", "ts", "t's", "tt", "tv", "twelve", "twenty", "twice", "two", "tx", "u", "u201d", "ue", "ui", "uj", "uk", "um", "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "uo", "up", "upon", "ups", "ur", "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "ut", "v", "va", "value", "various", "vd", "ve", "ve", "very", "via", "viz", "vj", "vo", "vol", "vols", "volumtype", "vq", "vs", "vt", "vu", "w", "wa", "want", "wants", "was", "wasn", "wasnt", "wasn't", "way", "we", "wed", "we'd", "welcome", "well", "we'll", "well-b", "went", "were", "we're", "weren", "werent", "weren't", "we've", "what", "whatever", "what'll", "whats", "what's", "when", "whence", "whenever", "when's", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "where's", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever", "whos", "who's", "whose", "why", "why's", "wi", "widely", "will", "willing", "wish", "with", "within", "without", "wo", "won", "wonder", "wont", "won't", "words", "world", "would", "wouldn", "wouldnt", "wouldn't", "www", "x", "x1", "x2", "x3", "xf", "xi", "xj", "xk", "xl", "xn", "xo", "xs", "xt", "xv", "xx", "y", "y2", "yes", "yet", "yj", "yl", "you", "youd", "you'd", "you'll", "your", "youre", "you're", "yours", "yourself", "yourselves", "you've", "yr", "ys", "yt", "z", "zero", "zi", "zz"]
    return names, stop


def quantify2(text, textname):
    global title, word, sentence, punc, ttr
    names, stop = starting_png_generation()
    title = textname
    word = findlength_word(text)
    sentence = findlength_sentence(text)
    punc = punctuation(text)
    ttr = wordtypes(text)


def findlength_word(text):

    # gets rid of uppers
    text = text.lower()

    # gets rid of bad characters
    removelist = [',', '.', '<', '>', '?', '/', ':', ';', '"', '[', ']', '{', '}', '_', '+', '=', '\\', '|',
                  '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', "'"]
    for i in removelist:
        text = text.replace(i, '')
    text = text.replace("\n", " ")
    text = text.replace("  ", " ")

    # makes a list
    text_list = text.split(" ")

    # removes empty strings
    empty = ''
    while empty in text_list:
        text_list.remove(empty)

    # removes stop words
    for s in stop:
        if s in text_list:
            text_list.remove(s)
            # print(s)

    word_lengths = []
    for t in text_list:
        word_lengths.append(len(t))

    numWords = len(text_list)
    chars = sum(word_lengths)
    average = chars/numWords

    # print(numWords, chars, average)
    return (str(average))


def findlength_sentence(text):

    titles = ['Mr.', "Ms.", "Mrs.", "Dr."]
    for t in titles:
        text = text.replace(t, "Ms")

    text_list = text.split(" ")

    empty = ''
    while empty in text_list:
        text_list.remove(empty)

    sentence = []
    sentence_lengths = []

    stops = ['.', '?', '!']

    for i in text_list:
        sentence.append(i)
        for s in stops:
            if s in i:
                sentence_lengths.append(len(sentence))
                sentence = []

    total = sum(sentence_lengths)
    average = total/len(sentence_lengths)
    # print(total, average)

    return (average)


def punctuation(text):

    titles = ['Mrs.', 'Mr.', 'Ms.', 'Dr.']
    for t in titles:
        text = text.replace(t, 'Ms')

    stops_list = ['.', '?', '!']
    punctuation_list = ['<', ',', '>', '/', ':', ';', '{', '[', '}', ']', '|', '\\',
                        '-', '_', '+', '=', ')', '(', '*', '&', '^', '%', '$', '#', '@']

    inside_punctuation_list = []
    inside_punctuation_counter = 0
    for char in text:
        if char in punctuation_list:
            inside_punctuation_counter += 1
        if char in stops_list:
            inside_punctuation_list.append(inside_punctuation_counter)
            inside_punctuation_counter = 0

    total = sum(inside_punctuation_list)
    average = total/len(inside_punctuation_list)
    print(total, average)
    return (average)


def wordtypes(text):

    # gets rid of uppers
    text = text.lower()

    # gets rid of bad characters
    removelist = [',', '.', '<', '>', '?', '/', ':', ';', '"', '[', ']', '{', '}', '_', '+', '=', '\\', '|',
                  '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', "'"]
    for i in removelist:
        text = text.replace(i, '')
    text = text.replace("\n", " ")
    text = text.replace("  ", " ")

    # makes a list
    text_list = text.split(" ")

    # removes empty strings
    empty = ''
    while empty in text_list:
        text_list.remove(empty)

    if len(text_list) > 5000:
        text_list = text_list[0:5000]

    # gives dictionary with keys of a word, value of number of occurences
    dictionary = {}
    key_list = list(dictionary)
    for k in text_list:
        if key_list == [{}] or (k not in key_list):
            dictionary[k] = 1
        else:
            dictionary[k] += 1
        key_list = list(dictionary)

    # calculate the proportion
    number_of_uniques = 0
    number_of_repeated = 0
    for i in key_list:
        if dictionary[i] == 1:
            number_of_uniques += 1
        else:
            number_of_repeated += 1

    uniqueWords = len(dictionary)
    proportion = uniqueWords/len(text_list)
    # print(str(len(text_list)))
    return (proportion)


def generate_plots(text, s="YourDoc"):
    quantify2(text, "YourDoc")
    mylist = [['Alice in W.', 4.09174276576889, 15.76709796672828, 2.252612169637369,
               0.2138],
              ['P and P', 4.416975965424522, 19.530199151159,
                  1.8806383325191336, 0.2226],
              ['Scientific', 5.234590256196931, 18.45785876993166, 2.570383125269049,
               0.188],
              ['CS Lewis', 4.078806634633656,
                  14.062934362934364, 0.936006168080185, 0.207],
              [title, word, sentence, punc, ttr]]

    print(mylist)

    n = 1
    while n < 5:
        # plt.ylabel("Frequency")
        # plt.xlabel("Text Name")

        list1 = []
        list2 = []

        for i in mylist:
            # print(i[0])
            list1.append(i[0])
            # print(i[n])
            list2.append(round(float(i[n]), 2))

        df2 = pd.DataFrame(
            dict(
                xvals=list1,
                yvals=list2
            )
        )

        df_sorted = df2.sort_values('yvals')

        # print(df_sorted)
        texts_sorted = df_sorted['xvals'].values.tolist()
        # print(texts_sorted)
        # set color to blue, except for the one that is added

        colors = []
        for value in texts_sorted:
            if value == "YourDoc":
                colors.append('red')
            else:
                colors.append('blue')

        plt.title(names[n])

        # plt.bar(list1,list2)
        plt.bar('xvals', 'yvals', data=df_sorted, color=colors, width=0.2)

        plt.grid()
        # plt.xlim(-5, 10)
        # plt.ylim(0,50)
        # plt.legend()
        plt.savefig("graph"+str(n)+".png")
        plt.clf()

        n += 1


@app.get('/pdf-analysis')
def test():
    return 'hi'
