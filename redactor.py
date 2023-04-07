import argparse
import project1.main as project1

# Method that segrates all the functionalities of this project.
def main(parser):
    args=parser.parse_args()
    list_of_files = project1.inputFiles(args)
    for f in list_of_files:
        with open(f,'r', encoding='utf-8') as file:
            text = file.read()
            data = project1.stats(args, f, text)
            project1.output(args, data, f)

if __name__ == "__main__":
    parser =argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, nargs='*', help="It takes the input files")
    parser.add_argument("--names", action="store_true", help="Redact names")
    parser.add_argument("--dates", action="store_true", help="Redact dates")
    parser.add_argument("--phones", action="store_true", help="Redacts phones")
    parser.add_argument("--genders", action="store_true", help="Redacts genders")
    parser.add_argument("--address", action="store_true", help="Redacts address")
    parser.add_argument("--output", type=str, required=True, help="It takes the output file path")
    parser.add_argument("--stats", help="It provides the stats of the redacted files")
    main(parser)