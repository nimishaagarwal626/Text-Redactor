## CS5293sp23 – Project1

## Name: Nimisha Agarwal

## Project Description:
This project is about redacting the information like name, phone numbers, date, gender and address from the text files provided in the project structure which are taken from http://www.enron-mail.com/. This program takes all the inputs as commandline arguments. It takes all the text files and replace names, phone numbers, dates, genders and addresses with their corresponding unicode character and also shows the statistics in the stat file.

## How to install:
Spacy installation: pipenv install Spacy
en_core_web_md installation: pipenv run python -m spacy download en_core_web_sm
pytest installation: pipenv install pytest

## How to run:
* To run the project: pipenv run python redactor.py --input '*.txt' --names --dates --phones --genders --address --output 'files/' --stats stats
[If we want to print the statistics in console, stdout can be passed instead of filename or we can even pass stderr]
* To run the pytests: pipenv run python -m pytest

# Video:


## Functions
# main.py \
* input_files (args) - This function takes the argument as input and uses glob.glob() to extract the text files and return the list of files as output. If there are no files then it return a message "there is no text file to redact".

* unicode_char (Word) - This function takes Word as input and returns its corresponding unicode full character representation.

* nameRedaction(data) - This function takes data as input and check if any entities label matches with the "PERSON" or "ORG", it replaces those with their corresponding unicode full character and store all those words along with their type in a dictionary. It returns the dictionary, count of the redacted words and the redacted data.

* dateRedaction(data) - This function takes data as input and check if any entities label matches with the "DATE", it replaces those with their corresponding unicode full character and store all those dates in a date list. It returns the date list, count of the redacted dates and the redacted data.

* phonesRedaction(data) - This function takes data as input and check if anything in data matches a given phone pattern, it replaces those phone numbers with their corresponding unicode full character and store all those phone numbers in a phone list. It returns the phone list, count of the redacted phone numbers and the redacted data.

* genderRedaction(data) - This function takes data as input and check if anything in data matches a given list of genders by converting all the token to its lower case. It also makes sure that it is matching the entire word. It then replaces those pgenders with their corresponding unicode full character and store all those genders in a gender list. It returns the gender list, count of the redacted genders and the redacted data.

* addressRedaction(data) - This function takes data as input and check if any entities label matches with the "GPE" or "LOC" or "FAC", it replaces those with their corresponding unicode full character and store all those words along with their type in a dictionary. It returns the dictionary, count of the redacted words and the redacted data.

* output(args, data, file) - This function takes args, data and file as input. It then gets the current working directory and creates a path to store redacted files. It checks if the directory passed in the argument already exist, if not it creates the directory and write all the redacted data into those files. Files are name as "inputfile.txt.redacted".

* stats(args, f, text) - Rhis function takes args, file and text as input. It then matches if the args is names/phones/address/genders/dates and call the corresponding methods defined above. It also calls the write_stats method which help in writing the statistics to file/console. It returns the redacted text as output.

* write_stats(redactedDict, count, file, args) - This function takes redactedDict, count, file, args as input. Based on the argument passed(stdout/stderr/filename), it prints the statistics either to the console or to the specified file which has the count and the redacted terms.

# redactor.py \ 
* main(parser) - It takes parser as the argument and parse the arguments passed form the command line and calls read_input method from the main.py then for every file it calls the stats and output method for succesful redaction.

# Tests:
* test_input_file.py - This file tests the input_files (args) function of main.py. It takes "*.txt" in argument.NAmespace method and calls the input_files method and then assert that the length of file is > 0.

* test_unicode.py - This file tests the unicode_char (Word) method to make sure that it is generating the correct unicode character corresponding to the word passed to it.

* test_names.py - This file takes the data and calls nameRedaction(data) from main.py and then assert the count, the dictionary generated as well as matches the redacted data with the desired result.

* test_dates.py - This file takes the data and calls dateRedaction(data) from main.py and then assert the count, the list generated as well as matches the redacted data with the desired result.

* test_phones.py - This file takes the data and calls phonesRedaction(data) from main.py and then assert the count, the list generated as well as matches the redacted data with the desired result.

* test_genders.py - This file takes the data and calls genderRedaction(data) form main.py and then assert the count, the list generated as well as matches the redacted data with the desired result.

* test_address.py - This file takes the data and calls addressRedaction(data) from main.py and then assert the count, the dictionary generated as well as matches the redacted data with the desired result.

## Bugs And Assumptions
# Bugs: 
* There might be some cases where the redactor considers Cc or Bcc from email as name and redact those specially in the case when the word before that is redacted.
* Some address are considered as GPE type although that part doesn't belong to the address section. It means some extra letters/words get redacted.
* Sometimes the spacy model considers some email addresses either as GPE or ORG category.
* All the redactions are done using spacy model, So, if those models are not accurate, there might not be 100% accuracy like few cases defined in the above points.

# Assumptions:
* Dates will be in the format : ‘06 April 2000', 'Tuesday', 'April', '2015'

* Genders are among ['he','she','him','her','his','himself','herself','male','female','men','women','ms','mr','miss','mr.','ms.','boy','girl','boys','girls','lady','ladies','gentleman','gentlemen','guy','hero','heroine','spokesman','spokeswoman','boyfriend','boyfriends','girlfriend','girlfriends','brother','brothers','sister','sisters','mother','father','mothers','fathers','grandfather','grandfathers','grandmother','grandmothers','mom','dad','moms','dads','king','kings','queen','queens','aunt','aunts','uncle','uncles','niece','nieces','nephew','nephews','groom','bridegroom','grooms','bridegrooms','son','sons','daughter','daughters','waiter','waitress']

