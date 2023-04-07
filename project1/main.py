import glob
import spacy
import sys
import os
import re

nlp=spacy.load('en_core_web_md')

# Takes the argument from command line and store the matching files in the files list
def inputFiles (args):
    files = []
    if args.input==[]:
        print ("There is no file to redact.",file = sys.stderr)
        exit(0)
    else:
        files = glob.glob(str(args.input[0]).strip('\''))
    if files == []:
        print ("There is no text file to redact.",file = sys.stderr)
        exit(0)
    return files

# Utility function to replace characters with their corresponding unicode full-block characters.
def unicodeChar (Word):
    item = ''
    for i in Word:
        if i  == ' ':
            item  += ' '
        else:
            item  += '\u2588'
    return item

# Redact the Names that matches with the type Person or ORG
def nameRedaction(data):
    doc = nlp(data)
    count = 0
    # Stores all the names with its label in the dictionary for stats
    namesdict = {}
    with doc.retokenize() as retokenizer:
        for ent in doc.ents:
            retokenizer.merge(ent)
            if ent.label_ == 'PERSON' or ent.label_ == 'ORG':
                count += 1
                data = data.replace(str(ent), unicodeChar(str(ent)))
                namesdict[ent.text] = ent.label_
    return data, namesdict, count

# Redact dates that matches the tyope DATE
def dateRedaction(data):
    doc = nlp(data)
    count = 0
    # stores all the dates in this list for stats
    dates = []
    with doc.retokenize() as retokenizer:
        for ent in doc.ents:
            retokenizer.merge(ent)
            if ent.label_ == 'DATE':
                count += 1
                data = data.replace(str(ent), unicodeChar(str(ent)))
                dates.append(ent.text)
    return data, dates, count

# Redact phone numbers that matches the pattern given
def phonesRedaction(data):
    count = 0
    # Stores all phone numbers in the phones list for stats
    phones = []
    phone_patterns = re.findall(r'\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}', data)
    for ph in phone_patterns:
        count += 1
        data = data.replace(str(ph), unicodeChar(str(ph)))
        phones.append(ph)
    return data, phones, count

# Redact genders that matches with the given gender list
def genderRedaction(data):
    count = 0 
    # stores all the matching genders in genderlist for stats
    genderlist = []
    doc = nlp(data)
    gender = ['he','she','him','her','his','himself','herself','male','female','men','women','ms','mr','miss','mr.','ms.','boy','girl','boys','girls','lady','ladies','gentleman','gentlemen','guy','hero','heroine','spokesman','spokeswoman','boyfriend','boyfriends','girlfriend','girlfriends','brother','brothers','sister','sisters','mother','father','mothers','fathers','grandfather','grandfathers','grandmother','grandmothers','mom','dad','moms','dads','king','kings','queen','queens','aunt','aunts','uncle','uncles','niece','nieces','nephew','nephews','groom','bridegroom','grooms','bridegrooms','son','sons','daughter','daughters','waiter','waitress']
    for token in doc:
        if token.lower_ in gender:
            count += 1
            # makes sure that only the entire matching word gets redacted.
            data = re.sub(r"\b{}\b".format(token), unicodeChar(str(token)), data)
            genderlist.append(token.text)
    return data, genderlist, count

# Redact addresses that matches with 'GPE', 'LOC' or 'FAC'
def addressRedaction(data):
    count = 0
    # stores all the matching addresses in the addressDict along with its types
    addressDict = {}
    doc = nlp(data)
    with doc.retokenize() as retokenizer:
        for ent in doc.ents:
            retokenizer.merge(ent)
            if ent.label_ == 'LOC' or ent.label_ == 'GPE' or ent.label_ == 'FAC':
                count += 1
                data = data.replace(str(ent), unicodeChar(str(ent)))
                addressDict[ent.text] = ent.label_
    return data, addressDict, count

# Creates/Displays the output files the the specified folder with .redacted extension
def output(args, data, file):
    cwd = os.getcwd()
    folder = os.path.join(cwd,str(args.output).strip('\''))
    path=os.path.basename(file)+ '.redacted'
    redacted_file_path = os.path.join(folder, path)
    # Checks if the folder already exists, if not it creates one 
    if os.path.isdir(folder):
        redactedfile = open(redacted_file_path, "w+" ,encoding="utf-8")
    else:
        os.mkdir(folder)
        redactedfile = open(redacted_file_path, "w" ,encoding="utf-8")
    redactedfile.write(data)
    redactedfile.close()

# This provides the statistics of the data based on the redactions.
def stats(args, f, text):
    if args.names:
        text, namesdict, count = nameRedaction(text)
        write_stats(namesdict, count, f, args, "names")
    if args.dates:
        text, dates, count = dateRedaction(text)
        write_stats(dates, count, f, args, "dates")
    if args.phones:
        text, phones, count = phonesRedaction(text)
        write_stats(phones, count, f, args, "phone numbers")
    if args.genders:
        text, gender, count = genderRedaction(text)
        write_stats(gender, count, f, args, "genders")
    if args.address:
        text, addressDict, count = addressRedaction(text)
        write_stats(addressDict, count, f, args, "address")
    return text

# Write stats to the file/console
def write_stats(redactedDict, count, file, args, value):
    if args.stats == 'stdout':
        print("Number of redacted terms =", count, file = sys.stdout)
        print("Redacted values =", redactedDict, '\n' , file = sys.stdout)
    elif args.stats == 'stderr':
        print("No error found", sys.stderr)
    else:
        statfile = open(str(args.stats), "a+" ,encoding="utf-8")
        statfile.write("Number of redacted {} from {} = {}".format(value, file, str(count)) +'\n')
        statfile.write("Redacted values = " + str(redactedDict) + '\n')
        statfile.close()