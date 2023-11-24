#! /bin/python
import operator, sys, getopt
from datetime import datetime

def save_message(options, filename):
    if any(o in options for o in ['-n','--no-dino']):
        print('')
        print(f"=== File saved as: {filename} ===")
    else:
        multiplier = len(filename) + 2
        dialog_multiplier = multiplier - 16
        print('')
        print(f"           ▅████████▅    ╭{'─' * multiplier}╮")
        print(f"           ██ ████████   │ File saved as: {' ' * dialog_multiplier}│")
        print(f"           ███████████  <  {filename} │")
        print(f"           █████▅▅▅▅▅    ╰{'─' * multiplier}╯")
        print("▅         █████          ")
        print("█▒     ▒████████▅        ")
        print("██▒  ▒█████████ ▀        ")
        print(" █████████████           ")
        print("  ▒█████████▒            ")
        print("      ██ ▒██             ")
        print("     ███   ███           ")
        print('')

    sys.exit()

def save(options, contents, filename=None):
    
    punctuations =  ["!", "(", ")", "-", "[", "]", "{", "}", ";", ":", "'", "\\", '"', ",", "<", ">", ".", "/", "?", "@", "#", "$", "%", "^", "&", "*", "_", "~"]
    skipped_words = ["the", "a", "to", "if", "is", "it", "of", "and", "or", "an", "as", "i", "me", "my", "we", "our", "ours", "you", "your", "yours", "he", "she", "him", "his", "her", "hers", "its", "they", "them", "their", "what", "which", "who", "whom", "this", "that", "am", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "but", "at", "by", "with", "from", "here", "when", "where", "how", "all", "any", "both", "each", "few", "more", "some", "such", "no", "nor", "too", "very", "can", "will", "just", "in", "he", "him", "his", "she", "her", "hers", "they", "their", "theirs", "said", 'there', 'here', 'would', 'could', 'nt']

    content_string = ''
    for line in contents:
        content_string += line

    for character in punctuations:
        content_string = content_string.replace(character, '')

    word_count = str(len(content_string.split()))

    # Determine most frequent words
    words = {}
    for word in content_string.split():
        if word.lower() in words.keys():
            words[word.lower()] += 1
        else:
            words[word.lower()] = 1
    sorted_words = dict( sorted(words.items(), key=operator.itemgetter(1), reverse=True))
    common_words = ''
    counter = 0
    for word in sorted_words:
        if counter == 4:
            break
        else:
            if not word in skipped_words:
                common_words += "-" + word
                counter += 1

    # Set filename
    newfile = datetime.now().strftime("%Y%m%d%a-%H%M%S")
    newfile += "-" + word_count + "w" if word_count else ''
    newfile += common_words 
    
    # Save append
    if filename:
        try:
            # Save file
            f = open(filename, "a")
            f.write("\n")
            f.write("\n")
            f.write(f"## {newfile}")
            f.write("\n")
            for line in contents: 
                f.write(line)
                f.write("\n")
            f.close()
            save_message(options, filename)
        except Exception as e:
            pass

    # Save new file
    newfile += ".md"
    f = open(newfile, "a")
    for line in contents: 
        f.write(line)
        f.write("\n")
    f.close()
    save_message(options, newfile)


def write(options, filename=None):
    print("Write your story! (Ctrl-D to save)")
    contents = []

    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)

    save(options, contents, filename)


def main(argv):
    inputfile = ''
    outputfile = ''
    opts, args = getopt.getopt(argv,"hna:",["help","no-dino","append="])
    options = {}
    for opt, arg in opts:
        options[opt] = arg

    if any(o in options for o in ['-h','--help']):
        print ('Dino Note is a simple command line writing application for jotting down notes and writing stories.')
        print()
        print('OPTIONS')
        print('\t-h --help\t\t\tDisplay this help message')
        print('\t-a --append [filename]\t\tAppend writing to an existing file')
        print('\t-n --no-dino\t\t\tHide dino when file is saved')
        sys.exit()
    elif any(o in options for o in ["-a", "--append"]):
        write(options, filename=arg)

    write(options)

if __name__ == "__main__":
   main(sys.argv[1:])

