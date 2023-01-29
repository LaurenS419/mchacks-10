import gtts

newFile = open("test.txt")
data = newFile.read()

tts = gtts.gTTS(data)
tts.save("test.mp3")