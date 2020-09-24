#Alison Cameron and Cathy Guang
import csv
import sys

def print_usage():
    #print each line of usage.txt
    with open('usage.txt', 'r') as usage:
        for line in usage:
            print(line, end = "")

def search_authors(searchstring):
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
    else:
        for author in authorbooks_dict:
            print("Books written by", author + ":")
            for book in authorbooks_dict[author]:
                print("     ", book)
            print()

def search_titles(searchstring):
    searchstring = searchstring.lower()
    title_count = 0
    with open('books.csv', 'r') as bookfile:
        reader = csv.reader(bookfile)
        for row in reader:
            title = row[0]
            titleLower = title.lower()
            if searchstring in titleLower:
                print(title + ", written by", row[2])
                title_count += 1
    if title_count == 0:
        print("We couldn't find any books that matched this search")

def find_books_in_range(startyear, endyear):
    title_count = 0
    with open('books.csv', 'r') as bookfile:
        reader = csv.reader(bookfile)
        for row in reader:
            published = int(row[1])
            if published >= startyear and published <= endyear:
                print(row[0] + ", written by", row[2] + ", published in", published)
                title_count += 1
    if title_count == 0:
        print("We couldn't find any books that were published between", startyear, "and", endyear)

def parse_arguments(arg_list):
    arg_dict = {}
    if (len(arg_list) <= 1) or ('-d' in arg_list and len(arg_list) != 4):
        valid = False

    operation_count = 0
    for arg in arg_list:
        if '-a' in arg or '--author' in arg:
            operation_count += 1
            if '=' in arg and len(arg.split('=')) == 2:
                valid = True
                searchstring = arg.split('=')[1]
                arg_dict["command"] = '-a'
                arg_dict["searchstring"] = searchstring
            else:
                arg_dict["error"] = "The option -a must include a SEARCHSTRING."
                valid = False

        if '-d' in arg or '--daterange' in arg:
            operation_count += 1
            arg_dict["command"] = '-d'
            from_count = 0
            until_count = 0
            for daterange_arg in arg_list:
                if '--from' in daterange_arg or "--until" in daterange_arg:
                    if '--from' in daterange_arg:
                        from_count += 1
                    elif '--until' in daterange_arg:
                        until_count += 1

                    if '=' in daterange_arg and len(daterange_arg.split('=')) == 2:
                        try:
                            year = int(daterange_arg.split('=')[1])
                            if '--from' in daterange_arg:
                                arg_dict["startyear"] = year
                            elif '--until' in daterange_arg:
                                arg_dict["endyear"] = year
                        except:
                            arg_dict["error"] = "Make sure your STARTYEAR and ENDYEAR are valid integers."
                    else:
                        arg_dict["error"] = "The option -d must include both --from=STARTYEAR and --until=ENDYEAR."

            if (from_count == 1 and until_count == 1) and ("startyear" in arg_dict) and ("endyear" in arg_dict):
                valid = True
                if arg_dict["startyear"] >= arg_dict["endyear"]:
                    arg_dict["error"] = "For the option -d, STARTYEAR must be earlier than ENDYEAR."
                    valid = False
            else:
                valid = False

        if '-h' in arg or '--help' in arg:
            operation_count += 1
            valid = True
            arg_dict["command"] = '-h'

        if '-t' in arg or '--title' in arg:
            operation_count += 1
            if '=' in arg and len(arg.split('=')) == 2:
                valid = True
                searchstring = arg.split('=')[1]
                arg_dict["command"] = '-t'
                arg_dict["searchstring"] = searchstring
            else:
                arg_dict["error"] = "The option -t must include a SEARCHSTRING"
                valid = False


    #users can only use one command at a time
    if operation_count != 1:
        valid = False
        if operation_count > 1:
            arg_dict["error"] = "You can only execute one command at once."
        elif operation_count == 0:
            arg_dict["error"] = "You did not enter any valid command line arguments."

    arg_dict["valid"] = valid
    return arg_dict

def main():
    #parse command-line arguments
    parsed_args = parse_arguments(sys.argv)
    if not(parsed_args["valid"]) or parsed_args["command"] == '-h':
        print_usage()
        print("\n\n" + parsed_args["error"])
        return
    #depending on the arguments, run the proper functions
    if parsed_args["command"] == '-a':
        search_authors(parsed_args["searchstring"])
    elif parsed_args["command"] == '-t':
        search_titles(parsed_args["searchstring"])
    elif parsed_args["command"] == '-d':
        find_books_in_range(parsed_args["startyear"], parsed_args["endyear"])


if __name__ == "__main__":
    main()
