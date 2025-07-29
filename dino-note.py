#! /bin/python
import operator, os, sys, getopt, re
from datetime import datetime

def save_message(options, filename, generated_filename=None):
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
        if generated_filename:
            print(generated_filename)

    sys.exit()

def get_stats(contents, common_word_count=4):
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
        if counter == common_word_count:
            break
        else:
            if not word in skipped_words:
                common_words += "-" + word
                counter += 1
    return {'count': word_count, 'common': common_words}

def save(options, contents, filename=None):
    
    word_stats = get_stats(contents)

    # Set filename
    filename = ''
    if options.get('filename'):
        filename = options.get('-f') or options.get('--filename')
        filename += '-'
    filename += datetime.now().strftime("%Y%m%d%a-%H%M%S")
    filename += "-" + word_stats['count'] + "w" if word_stats['count'] else ''
    if options.get('filename') == None:
        filename += word_stats['common'] 
    
    # Save append
    if options.get('append'):
        append_file = options.get('-a') or options.get('--append')
        try:
            # Save file
            f = open(append_file, "a")
            f.write("\n")
            f.write("\n")
            f.write(f"## {filename}")
            f.write("\n")
            for line in contents: 
                f.write(line)
                f.write("\n")
            f.close()
            save_message(options, append_file, generated_filename=filename)
        except Exception as e:
            pass

    # Save new file
    filename += ".md"
    f = open(filename, "a")
    for line in contents: 
        f.write(line)
        f.write("\n")
    f.close()
    save_message(options, filename)


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

def project_prompt(question, variable_type="int", maximum=500):
    while True:
        try:
            if variable_type == "int":
                response = int(input(question + " "))
                if response > maximum:
                    raise ValueError("Response higher than maximum!")
            elif variable_type == "y/n":
                response = str(input(question + " (Y/N) ")).lower()
                if not re.match(r'^[yn]$', response):
                    raise ValueError("Does not match regex (y/n)")
            else:
                response = input(question)
        except ValueError:
            if variable_type == "int":
                print("Invalid response! Please enter a number.")
            elif variable_type == "y/n":
                print("Invalid response! Please enter a 'Y' for yes or an 'N' for no.")
            else:
                print("Invalid response!")
        else:
            break
    
    return response

def create_project(options):
    
    confirm = project_prompt("This command creates a project folder structure in your current directory. Are you in the directory where you want these folders to be created?", "y/n")
    
    if confirm == "n":
        print("Project creation cancelled! Move to the directory where you want these folders created and run the command again.")
        sys.exit()

    chapters = project_prompt("How many chapters should this project have?", "int", 250)
    print(f"Creating {chapters} chapter directories...")
    count = 1
    while count <= chapters:
        os.mkdir(f"Chapter {count}")
        count += 1

    scenes = project_prompt("How many scenes should each chapter have?", "int", 50)
    print(f"Creating {scenes} scene directories in each chapter directory...")
    chap_count = 1
    base_dir = os.getcwd()
    while chap_count <= chapters:
        scene_count = 1
        while scene_count <= scenes:
            os.mkdir(f"Chapter {chap_count}/Scene {scene_count}")
            scene_count += 1
        chap_count += 1
    os.chdir(base_dir)

    characters = project_prompt("Generate character folders?", "y/n")
    if characters == 'y':
        print(f"Creating Character folders...")
        os.mkdir('Characters')
        os.chdir(f"{base_dir}/Characters")
        os.mkdir('Main')
        os.mkdir('Secondary')
        os.mkdir('Locations')
        os.chdir(base_dir)

    print("Project created successfully!")
    return True

def main(argv):
    inputfile = ''
    outputfile = ''
    opts, args = getopt.getopt(argv,"hnca:f:",["help","no-dino","create-project","append=","filename="])
    options = {}
    for opt, arg in opts:
        options[opt] = arg

    if any(o in options for o in ['-h','--help']):
        print ('Dino Note is a simple command line writing application for jotting down notes and writing stories.')
        print()
        print('OPTIONS')
        print('\t-h --help\t\t\tDisplay this help message')
        print('\t-c --create_project\t\tCreate chapter/scene/character folders in the current directory')
        print('\t-a --append [filename]\t\tAppend writing to an existing file')
        print('\t-f --filename [filename]\tSet the name of the file your writing will be saved as')
        print('\t-n --no-dino\t\t\tHide dino when file is saved')
        sys.exit()
    if any(o in options for o in ["-c", "--create_project"]):
        create_project(options)
        sys.exit()
    if any(o in options for o in ["-f", "--filename"]):
        options['filename'] = options.get('-f') or options.get('--filename')
    if any(o in options for o in ["-a", "--append"]):
        options['append'] = options.get('-a') or options.get('--append')

    write(options)

if __name__ == "__main__":
   main(sys.argv[1:])

