# Read text from a file, and count the occurence of words in that text
# Example:
# count_words("The cake is done. It is a big cake!") 
# --> {"cake":2, "big":1, "is":2, "the":1, "a":1, "it":1}

def read_file_content(filename):
    # [assignment] Add your code here
    file = open(filename, "r")
    data = file.read()

    return "Hello World"


def count_words(string):
    text = read_file_content("./story.txt")
    # [assignment] Add your code here
    text2 = dict()
    words = string.split()
    for word in words:
        if word in text:
            text2[word] += 1
        else:
            text2[word] = 1

    return text2


print(count_words('management'))
