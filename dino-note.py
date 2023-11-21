#! /bin/python
import operator
import json
from datetime import datetime

print("Write your story! (Ctrl-D to save)")
contents = []

while True:
    try:
        line = input()
    except EOFError:
        break
    contents.append(line)

# Load text filters
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
filename = datetime.now().strftime("%Y%m%d%a-%H%M%S")
filename += "-" + word_count + "w" if word_count else ''
filename += common_words 
filename += ".md"

# Save file
f = open(filename, "a")
for line in contents: 
    f.write(line)
    f.write("\n")
f.close()

multiplier = len(filename) + 2
dialog_multiplier = multiplier - 16
save_dialog = f"File saved as {filename}!"


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


#print(save_dialog)
