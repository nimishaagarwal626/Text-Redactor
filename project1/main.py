import glob
import spacy
import sys
import os
import re

nlp=spacy.load('en_core_web_md')

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

def unicodeChar (Word):
    item = ''
    for i in Word:
        if i  == ' ':
            item  += ' '
        else:
            item  += '\u2588'
    return item

def nameRedaction(data):
    doc = nlp(data)
    count = 0
    namesdict = {}
    with doc.retokenize() as retokenizer:
        for ent in doc.ents:
            retokenizer.merge(ent)
            if ent.label_ == 'PERSON' or ent.label_ == 'ORG':
                count += 1
                data = data.replace(str(ent), unicodeChar(str(ent)))
                namesdict[ent.text] = ent.label_
    return data, namesdict, count

def dateRedaction(data):
    doc = nlp(data)
    count = 0
    dates = []
    with doc.retokenize() as retokenizer:
        for ent in doc.ents:
            retokenizer.merge(ent)
            if ent.label_ == 'DATE':
                count += 1
                data = data.replace(str(ent), unicodeChar(str(ent)))
                dates.append(ent.text)
    return data, dates, count

def phonesRedaction(data):
    count = 0
    phones = []
    phone_patterns = re.findall(r'\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}', data)
    for ph in phone_patterns:
        count += 1
        data = data.replace(str(ph), unicodeChar(str(ph)))
        phones.append(ph)
    return data, phones, count

def genderRedaction(data):
    count = 0 
    genderlist = []
    doc = nlp(data)
    gender = ['he','she','him','her','his','himself','herself','male','female','men','women','ms','mr','miss','mr.','ms.','boy','girl','boys','girls','lady','ladies','gentleman','gentlemen','guy','hero','heroine','spokesman','spokeswoman','boyfriend','boyfriends','girlfriend','girlfriends','brother','brothers','sister','sisters','mother','father','mothers','fathers','grandfather','grandfathers','grandmother','grandmothers','mom','dad','moms','dads','king','kings','queen','queens','aunt','aunts','uncle','uncles','niece','nieces','nephew','nephews','groom','bridegroom','grooms','bridegrooms','son','sons','daughter','daughters','waiter','waitress']
    for token in doc:
        if token.lower_ in gender:
            count += 1
            data = re.sub(r"\b{}\b".format(token), unicodeChar(str(token)), data)
            genderlist.append(token.text)
    return data, genderlist, count

def addressRedaction(data):
    count = 0
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

def output(args, data, file):
    cwd = os.getcwd()
    folder = os.path.join(cwd,str(args.output).strip('\''))
    path=os.path.basename(file)+ '.redacted'
    redacted_file_path = os.path.join(folder, path)
    if os.path.isdir(folder):
        redactedfile = open(redacted_file_path, "w+" ,encoding="utf-8")
    else:
        os.mkdir(folder)
        redactedfile = open(redacted_file_path, "w" ,encoding="utf-8")
    redactedfile.write(data)
    redactedfile.close()

def stats(args, f, text):
    if args.names:
        text, namesdict, count = nameRedaction(text)
        write_stats(namesdict, count, f, args)
    if args.dates:
        text, dates, count = dateRedaction(text)
        write_stats(dates, count, f, args)
    if args.phones:
        text, phones, count = phonesRedaction(text)
        write_stats(phones, count, f, args)
    if args.genders:
        text, gender, count = genderRedaction(text)
        write_stats(gender, count, f, args)
    if args.address:
        text, addressDict, count = addressRedaction(text)
        write_stats(addressDict, count, f, args)
    return text

def write_stats(redactedDict, count, file, args):
    if args.stats == 'stdout':
        print("No. of redacted terms =", count, file = sys.stdout)
        print("Redacted values =", redactedDict, '\n' , file = sys.stdout)
    elif args.stats == 'stderr':
        print("No error found", sys.stderr)
    else:
        statfile = open(str(args.stats), "a+" ,encoding="utf-8")
        statfile.write("No. of redacted terms from " +file + "= " + str(count)  + '\n')
        statfile.write("Redacted values = " + str(redactedDict) + '\n')
        statfile.close()