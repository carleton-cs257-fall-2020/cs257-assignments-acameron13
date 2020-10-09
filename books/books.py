#Alison Cameron and Cathy Guang
#Revised by Alison Cameron
#CS257 Carleton College
#September 25, 2020
#A program to experiment with command line arguments to manipulate a dataset
import csv
import argparse

def search_authors(searchstring):
    '''search_authors(searchstring) will return a list of all authors
    whose names contain the given searchstring (case insensitive),
    as well as all of the books that they have published.'''
    searchstring = searchstring.lower()
    authorbooks_dict = {}

    with open('books.csv', 'r') as bookfile:
        reader = csv.reader(bookfile)
        for row in reader:
            author = row[2]
            authorLower = author.lower()
            if searchstring in authorLower:
                if author in authorbooks_dict:
                    authorbooks_dict[author].append(row[0])
                else:
                    authorbooks_dict[author] = [row[0]]

    if len(authorbooks_dict) == 0:
        print("We couldn't find any authors that matched this search")
        exit()
    else:
        authors_matched = []
        for author in authorbooks_dict:
            authors_matched.append("Books written by "+ author + ":")
            for book in authorbooks_dict[author]:
                authors_matched.append("     " + book)
            authors_matched.append(" ")

    return authors_matched

def search_titles(searchstring):
    '''search_titles(searchstring) will return a list of all books whose
    titles contain the given searchstring (case insensitive), along
    with the author of each book.'''
    searchstring = searchstring.lower()
    books_matched = []

    with open('books.csv', 'r') as bookfile:
        reader = csv.reader(bookfile)
        for row in reader:
            title = row[0]
            titleLower = title.lower()
            if searchstring in titleLower:
                books_matched.append(title + ", written by " + row[2])

    if len(books_matched) == 0:
        print("We couldn't find any books whose titles contain", searchstring)

    return books_matched

def find_books_in_range(startyear, endyear):
    '''find_books_in_range(startyear, endyear) will return a list of all books whose
    publication year is within the given inclusive range. Each book will contain
    the title of the book, the author, and the publication date.'''
    books_matched = []

    with open('books.csv', 'r') as bookfile:
        reader = csv.reader(bookfile)
        for row in reader:
            published = int(row[1])
            if published >= startyear and published <= endyear:
                books_matched.append(row[0] + ", written by " + row[2] + ", published in " + str(published))

    if len(books_matched) == 0:
        print("We couldn't find any books that were published between", startyear, "and", endyear)

    return books_matched

def get_parsed_arguments():
    '''uses the argparse module to parse command line arguments. If the
    arguments are invalid, we display the help page and exit.'''

    arg_parse_description = "Displays books that match given search parameters. Use only one command at a time."
    author_help = "Displays all authors whose names contain AUTHOR, as well as all of their books. AUTHOR is case insensitive and should be entered without quotation marks."
    title_help = "Displays all books whose title contains TITLE. TITLE is case insensitive and should be entered without quotation marks."
    daterange_help = "Displays all books whose publication year are within the given DATERANGE. The first argument represents the start year, and the second argument represents the end year, both inclusive. The start year must be earlier than the endyear."

    parser = argparse.ArgumentParser(description=arg_parse_description)
    parser.add_argument('--author', '-a', default=None, help=author_help)
    parser.add_argument('--title', '-t', default=None, help=title_help)
    parser.add_argument('--daterange', '-d', nargs=2, help=daterange_help)

    final_args = build_arg_dict(vars(parser.parse_args()))

    if not(final_args['valid']):
        parser.print_help()
        if 'error' in final_args:
            print("\n" + final_args['error'])
        exit()

    return final_args

def build_arg_dict(parsed_args):
    '''builds a dictionary of arguments of the form:

    {"valid": True/False, "command": '-a', '-d', or '-t', ...<extra info>...},
    where the extra information for the commands -a and -t are {"searchstring": <user input>},
    the extra information for -d is {"startyear": <user input>, "endyear": <user input>}'''

    arg_dict = {}

    valid = True
    command_count = 0
    if parsed_args['author'] != None:
        command_count += 1
        arg_dict['command'] = '-a'
        arg_dict['searchstring'] = parsed_args['author']

    if parsed_args['title'] != None:
        command_count += 1
        arg_dict['command'] = '-t'
        arg_dict['searchstring'] = parsed_args['title']

    if parsed_args['daterange'] != None:
        command_count += 1
        arg_dict['command'] = '-d'
        date_list = parsed_args['daterange']
        startStr, endStr = date_list[0], date_list[1]
        try:
            startyear = int(startStr)
            endyear = int(endStr)

            if startyear <= endyear:
                arg_dict['startyear'] = startyear
                arg_dict['endyear'] = endyear
            else:
                arg_dict["error"] = "For the option -d, the start year must be earlier than end year."
                valid = False
        except:
            arg_dict['error'] = "Make sure your start year and end year are valid integers."
            valid = False

    if command_count > 1:
        arg_dict['error'] = "You can only execute one command at once."
        valid = False
    elif command_count == 0:
        arg_dict['error'] = "You did not enter any valid command line arguments."
        valid = False

    arg_dict["valid"] = valid
    return arg_dict

def main():
    parsed_args = get_parsed_arguments()

    if parsed_args["command"] == '-a':
        books_list = search_authors(parsed_args["searchstring"])
    elif parsed_args["command"] == '-t':
        books_list = search_titles(parsed_args["searchstring"])
    elif parsed_args["command"] == '-d':
        books_list = find_books_in_range(parsed_args["startyear"], parsed_args["endyear"])

    for book in books_list:
        print(book)


if __name__ == "__main__":
    main()
