#Alison Cameron and Cathy Guang
import csv
import sys

def print_usage():
    print("printing usage")
    #print each line of usage.txt
    return 0

def search_authors(searchstring):
    #for each line in the csv, determine if the searchstring is
    #contained in the author column (case insensitive)
        #for each author where this is the case, keep track of
        #their books, and print them out at the end

    #if the searchstring isn't contained in any author names,
    #then print some kind of error message
    return 0

def search_titles(searchstring):
    #for each line in the csv, determine if the searchstring is
    #contained in the title column (case insensitive)
        #if it is contained, print out the full title and other info (?)

    #if the searchstring isn't contained in any titles,
    #then print some kind of error message
    return 0

def find_books_in_range(startyear, endyear):
    #for each line in the csv, determine if the publication year is
    #within the given range
        #if the book is contained within the range, print out title
        #and other info(?)

    #if there are no books within the range, print out some kind
    #of error message

    return 0

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
                print("The option -a must include a SEARCHSTRING")
                print("See below for proper command-line syntax \n\n")
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
                            print("Make sure your STARTYEAR and ENDYEAR are valid integers.\n\n")
                    else:
                        print("The option -d must include both --from=STARTYEAR and --until=ENDYEAR.\n\n")

            if (from_count == 1 and until_count == 1) and ("startyear" in arg_dict) and ("endyear" in arg_dict):
                valid = True
                if arg_dict["startyear"] >= arg_dict["endyear"]:
                    print("For the option -d, STARTYEAR must be earlier than ENDYEAR.\n\n")
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
                print("The option -t must include a SEARCHSTRING")
                print("See below for proper command-line syntax \n\n")
                valid = False


    #users can only use one command at a time
    if operation_count != 1:
        valid = False
        if operation_count > 1:
            print("You can only execute one command at once.")
        elif operation_count == 0:
            print("You did not enter any valid command line arguments.")
        print("See usage page below. \n\n")

    arg_dict["valid"] = valid
    return arg_dict

def main():
    #parse command-line arguments
    arg_list = sys.argv
    print(sys.argv)
    parsed_args = parse_arguments(arg_list)
    print(parsed_args)
    if not(parsed_args["valid"]) or parsed_args["command"] == '-h':
        print_usage()
        return


    #verify that command-line arguments are valid
    #depending on the arguments, run the proper functions
    return 0

if __name__ == "__main__":
    main()
