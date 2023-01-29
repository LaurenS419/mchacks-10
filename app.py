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


app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/test')
@cross_origin()
def index():
    return "Hello, World!"


@app.route('/pdf-analysis', methods=['POST'])
@cross_origin()
def pdf_analysis():

    file = request.files['files']  # a multidict containing POST data
    print(file)
    filepath = '/Users/laurenspee/Desktop/' + 'testfile.pdf'
    file.save(filepath)

    try:
        new_filename, text = textpdf_to_txt(filepath)
        return text
        # if text==    ---------- :
        #   text=ocr_pdf_to_text(filename)
    except:
        new_filename, text = textpdf_to_txt(filepath)
        return text

    reading_speed = 238  # check this value non-fiction
    word_count = word_counter(text)
    time_to_read = reading_time(word_count, reading_speed)
    summary = cohere_summary(text)
    bottom_text = 'Word count: ' + str(word_count)
    mp3_filename = text_to_speech(text)


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
    # import os
    # import codecs
    # os.chdir(r'C:\Users\ellaw\Desktop\McHacks10')

    text = pdfminer.high_level.extract_text(filename)
    new_filename = filename[:(len(filename)-3)]+'txt'
    fobj = open(new_filename+'.txt', 'w')
    fobj.write(text)
    fobj.close()
    return new_filename, text


@app.route('/mp3')
def text_to_speech(text):

    filename = "pdfAudio"
    engine = pyttsx3.init()
    new_filename = filename+".mp3"
    engine.save_to_file(text, new_filename)
    # return new_filename


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

    co = cohere.Client('M56z1g38WE83LZuXxzIjrtpO4oo99Ez9p7J7w3bW')

    response = co.generate(
        prompt=text,
        max_tokens=100,  # figure out number of tokens
        temperature=0.8,
        stop_sequences=["--"])

    return ("Summary: {}".format(response.generations[0].text))


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

    # FUCK THE PICTURES

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
    output_filename = 'Analysis PDF of ' + input_filename
    pdf.output(output_filename, 'F')

    return output_filename


@app.get('/pdf-analysis')
def test():
    return 'hi'
