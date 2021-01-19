import re
import os
import heapq
import numpy as np

def tokenize(jack_filename):                                    # receives a file; tokenize("Square/Main.jack")
    split_lines = []    # after splitting by symbols
    tokens = []         # after splitting by spaces
    xml_tokens = []     # after adding xmljmarkup

    jack_file = open(jack_filename, "r")
    lines = jack_file.readlines()                               # lines of .jack file

    for line in lines:
        line = line.strip()

        if line.startswith("//") or line == "":                 # if comment line or empty
            continue
        if line.startswith("/**") or line.startswith("/*"):     # if comment line
            continue
        if line.strip().startswith("*"):                        # multi-line comment
            continue

        line = line.split("//")[0].strip()                      # remove trailing comment

        # get anything between quotation marks => \".*\"
        # else split by these symbols => |[}{\(\)\[\].,;\+\-*/&|<>=~]
        # do not remove results => use a bracket around the whole thing when using re.split
        line = re.split('(\".*\"|[}{\(\)\[\].,;\+\-*/&|<>=~])', line)  # "class Main {" => ["class Main", "{"]

        split_lines += line

    split_lines = [x for x in split_lines if (x != None and x.strip() != "")]             # remove empty lines

    # print(split_lines)

    for i in range(len(split_lines)):
        split_lines[i] = split_lines[i].strip()
        if split_lines[i].startswith('"'):
            tokens.append(split_lines[i])                       # add "string of words" to list
        else:
            tokens += split_lines[i].split(" ")                 # add list of tokens to final list

    tokens = [x for x in tokens if x.strip() != ""]             # after splitting by spaces

    # xml_tokens = convertToXML(tokens)                           # convert tokens to XML tokens
    # xml_tokens.insert(0, "<tokens>")
    # xml_tokens.append("</tokens>")                              # <tokens> ... </tokens>

    # for i in range(len(tokens)):
    #     tokens[i] = tokens[i].replace("&", "&amp;")         # & => &amp;
    #     tokens[i] = tokens[i].replace("<", "&lt;")          # < => &lt;
    #     tokens[i] = tokens[i].replace(">", "&gt;")          # > => &gt;

    punctuation = "!@#$%^&*()_-+<>?:.,;}/{"

    result = []
    for i in tokens:
        if re.match(r'^([\s\d]+)$', i):
            continue
        if i not in punctuation:
            result.append(i)
    return result
    

def convertToXML(tokens):                                       # var => <keyword> var </keyword>
    for i in range(len(tokens)):
        if tokens[i] in keyword_list:
            tokens[i] = "<keyword> " + tokens[i] + " </keyword>"

        elif tokens[i] in symbol_list:
            tokens[i] = tokens[i].replace("&", "&amp;")         # & => &amp;
            tokens[i] = tokens[i].replace("<", "&lt;")          # < => &lt;
            tokens[i] = tokens[i].replace(">", "&gt;")          # > => &gt;
            tokens[i] = "<symbol> " + tokens[i] + " </symbol>"

        elif tokens[i].isdigit():                               # <integerConstant> 16 </integerConstant>
            tokens[i] = "<integerConstant> " + tokens[i] + " </integerConstant>"

        elif tokens[i].startswith('"'):                         # <stringConstant> string constant </stringConstant>
            tokens[i] = "<stringConstant> " + tokens[i][1:-1] + " </stringConstant>"

        else:                                                   # otherwise, it is an identifier
            tokens[i] = "<identifier> " + tokens[i] + " </identifier>"
    
    return tokens

keyword_list = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 
                'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if',
                'else', 'while', 'return']

symbol_list = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']

if __name__ == "__main__":

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, './test_files')

    token_dictionary = {}

    file_list = []
    
    for file in os.listdir(filename):
        f = os.path.join(filename, file)

        tokens = tokenize(f)

        token_per_file = []

        for i in tokens:
            if i not in token_dictionary.keys():
                token_dictionary[i] = 1
            else:
                token_dictionary[i] += 1
            token_per_file.append(i)

        file_list.append(token_per_file)

    most_freq = heapq.nlargest(10, token_dictionary, key = token_dictionary.get)

    result = []

    for files in file_list:
        file_token = []
        for token in tokens:
            if token in files:
                file_token.append(1)
            else:
                file_token.append(0)
                
        result.append(file_token)

    print(result)

        


