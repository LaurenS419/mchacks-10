#text to speach
import gtts

newFile = open("test.txt")
data = newFile.read()

tts = gtts.gTTS(data)
tts.save("test.mp3")

#cohere
import cohere

co = cohere.Client('M56z1g38WE83LZuXxzIjrtpO4oo99Ez9p7J7w3bW')

newFile = open("test.txt")
data = newFile.read()

response = co.generate(
    prompt = data,
    max_tokens = 50,
    temperature = 0.8,
    stop_sequences = ["--"])

print("Summary: {}".format(response.generations[0].text))

#word count
newFile = open("test.txt")
data = newFile.read()

#wordCount = data.count(" ") + 1

textList = []
wordList = data.split(" ")
for i in range(0, len(wordList)):
    textList.append(wordList[i])
    
print(len(textList))