
def check_word(sentence):
    # Specify the path to your text file
    file_path = "zero_tolerance_words.txt"


    words = []

    # Open the file for reading
    with open(file_path, 'r') as file:
        for line in file:
            words.append(line.strip())



    sentence = sentence.lower()
    for word in words:
        if word in sentence:
            return True
    return False


