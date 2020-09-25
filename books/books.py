#Alison Cameron and Cathy Guang
#CS257 Carleton College
#September 25, 2020
#A program to experiment with command line arguments to manipulate a dataset
import csv
import sys

def print_usage():
    '''print_usage prints out a help page for the program
    that tells the user how to use the command line syntax.'''
    #print each line of usage.txt
    with open('usage.txt', 'r') as usage:
        for line in usage:
            print(line, end = "")

def search_authors(searchstring):
    '''search_authors(searchstring) will display all authors
    whose names contain the given searchstring (case insensitive),
    as well as all of the books that they have published.'''
    searchstring = searchstring.lower()
    authorbooks_dict = {}

    #open dataset and loop through
    with open('books.csv', 'r') as bookfile:
        reader = csv.reader(bookfile)
        for row in reader:
            author = row[2]
            authorLower = author.lower()
            if searchstring in authorLower:
                #if the searchstring matches the author
                if author in authorbooks_dict:
                    #if the author is already in our dictionary, add the book
                    #to their list of books
                    authorbooks_dict[author].append(row[0])
                else:
                    #if the author is not in our dictionary, initialize their
                    #list of books, adding the current one.
                    authorbooks_dict[author] = [row[0]]

    if len(authorbooks_dict) == 0:
        #if there are no matching authors, print an error message.
        print("We couldn't find any authors that matched this search")
    else:
        #for each author in the dictionary, print out all their published books
        for author in authorbooks_dict:
            print("Books written by", author + ":")
            for book in authorbooks_dict[author]:
                print("     ", book)
            print()

def search_titles(searchstring):
    '''search_titles(searchstring) will display all books whose
    titles contain the given searchstring (case insensitive), along
    with the author of each book.'''
    searchstring = searchstring.lower()
    title_count = 0

    #open the dataset and loop through
    with open('books.csv', 'r') as bookfile:
        reader = csv.reader(bookfile)
        for row in reader:
            title = row[0]
            titleLower = title.lower()
            if searchstring in titleLower:
                #if the searchstring is contained in the title,
                #print out information
                print(title + ", written by", row[2])
                title_count += 1

    if title_count == 0:
        #if no book titles match the searchstring, print this error message.
        print("We couldn't find any books that matched this search")

def find_books_in_range(startyear, endyear):
    '''find_books_in_range(startyear, endyear) will display all books whose
    publication year is within the given inclusive range. Each line will contain
    the title of the book, the author, and the publication date.'''
    title_count = 0

    #open the dataset and loop through
    with open('books.csv', 'r') as bookfile:
        reader = csv.reader(bookfile)
        for row in reader:
            published = int(row[1])

            if published >= startyear and published <= endyear:
                #if the publication year is within the range, print out information
                print(row[0] + ", written by", row[2] + ", published in", published)
                title_count += 1

    if title_count == 0:
        #if no books were published within the given range, print this error message
        print("We couldn't find any books that were published between", startyear, "and", endyear)

def parse_arguments(arg_list):
    '''parse_arguments takes a list of command-line arguments accessed by sys.argv
    and returns a dictionary of relevant values.

    Structure of dictionary:
    {"valid": True/False, "command": '-a', '-d', '-h', or '-t', ...<extra info>...},
    where the extra information for the commands -a and -t are {"searchstring": <user input>},
    the extra information for -d is {"startyear": <user input>, "endyear": <user input>},
    and there is no extra information for -h.

    If any of the commands or extra information is incorrect, "valid" will be set to False
    and the main function will print the help page for the command line syntax. In some
    of these cases, there will also be an "error" field in the dictonary, and that message
    will be displayed to the user at the bottom of the help page.'''

    #initialize the argument dictionary
    arg_dict = {}

    #set valid flag for obviously incorrect input and return the dictionary
    if (len(arg_list) <= 1) or ('-d' in arg_list and len(arg_list) != 4):
        arg_dict["valid"] = False
        arg_dict["error"] = "Please enter the correct number of command line arguments."
        return arg_dict

    #keep track of the number of commands that a user inputs - only one at
    #a time is allowed
    operation_count = 0

    #loop through arguments in sys.argv list
    for arg in arg_list:
        if '-a' in arg or '--author' in arg:
            #user is trying to search for an author
            operation_count += 1
            if '=' in arg and len(arg.split('=')) == 2:
                #user provided a non-empty search string, the argument is valid
                valid = True
                searchstring = arg.split('=')[1]
                arg_dict["command"] = '-a'
                arg_dict["searchstring"] = searchstring
            else:
                #the user did not provide a correctly formatted search string
                arg_dict["error"] = "The option -a must include a SEARCHSTRING."
                valid = False

        if '-d' in arg or '--daterange' in arg:
            #user is trying to search for books within a date range
            operation_count += 1
            arg_dict["command"] = '-d'

            #used to ensure that only one --from argument and only one --until
            #argument is used.
            from_count = 0
            until_count = 0

            #find the --from and --until arguments in the arg_list
            for daterange_arg in arg_list:
                if '--from' in daterange_arg or "--until" in daterange_arg:
                    if '--from' in daterange_arg:
                        from_count += 1
                    elif '--until' in daterange_arg:
                        until_count += 1

                    #verify that the dates provided are formatted correctly
                    if '=' in daterange_arg and len(daterange_arg.split('=')) == 2:
                        try:
                            year = int(daterange_arg.split('=')[1])
                            #the year is valid, add to the dictionary
                            if '--from' in daterange_arg:
                                arg_dict["startyear"] = year
                            elif '--until' in daterange_arg:
                                arg_dict["endyear"] = year
                        except:
                            #the year is invalid, add an error message to the dictionary
                            arg_dict["error"] = "Make sure your STARTYEAR and ENDYEAR are valid integers."
                    else:
                        #the user did not provide a date after a --from or --until argument
                        arg_dict["error"] = "The option -d must include both --from=STARTYEAR and --until=ENDYEAR."

            if (from_count == 1 and until_count == 1) and ("startyear" in arg_dict) and ("endyear" in arg_dict):
                #if there was only one --from and only one --until argument, and each of them were valid
                valid = True
                if arg_dict["startyear"] >= arg_dict["endyear"]:
                    #the startyear is later than the endyear, set an error message
                    arg_dict["error"] = "For the option -d, STARTYEAR must be earlier than ENDYEAR."
                    valid = False
            else:
                #there is an incorrect combination of arguments for the daterange, or some arguments are invalid
                valid = False

        if '-h' in arg or '--help' in arg:
            #user is requesting help on command line syntax
            operation_count += 1
            valid = True
            arg_dict["command"] = '-h'

        if '-t' in arg or '--title' in arg:
            #user is trying to search for a title
            operation_count += 1
            if '=' in arg and len(arg.split('=')) == 2:
                #user provided a valid searchstring, set the proper values to the dictionary
                valid = True
                searchstring = arg.split('=')[1]
                arg_dict["command"] = '-t'
                arg_dict["searchstring"] = searchstring
            else:
                #user provided an invalid searchstring or did not provide one
                arg_dict["error"] = "The option -t must include a SEARCHSTRING"
                valid = False


    #users can only use one command at a time
    if operation_count != 1:
        valid = False

        #set the proper error message
        if operation_count > 1:
            arg_dict["error"] = "You can only execute one command at once."
        elif operation_count == 0:
            arg_dict["error"] = "You did not enter any valid command line arguments."

    #after checking all cases that would influence validity, set the valid value
    arg_dict["valid"] = valid

    return arg_dict

def main():
    #parse command-line arguments
    parsed_args = parse_arguments(sys.argv)

    if not(parsed_args["valid"]) or parsed_args["command"] == '-h':
        #if arguments are invalid or user is requesting help, print help page
        print_usage()

        #if an error message has been set, print the error message
        if "error" in parsed_args:
            print("\n\n" + parsed_args["error"])

        #exit out of the program
        return

    #depending on the command, run the proper functions
    if parsed_args["command"] == '-a':
        search_authors(parsed_args["searchstring"])
    elif parsed_args["command"] == '-t':
        search_titles(parsed_args["searchstring"])
    elif parsed_args["command"] == '-d':
        find_books_in_range(parsed_args["startyear"], parsed_args["endyear"])


if __name__ == "__main__":
    main()
