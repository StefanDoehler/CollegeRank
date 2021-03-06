from common import states, regions
import re


#  Takes a string in the form "city, state" where state is an abbreviation
#  Returns a list of 3 elements: [city, state, region] where state is spelled out
def parse_location(location):
    l = location.split(", ")
    result = []

    if len(l) is not 2:
        return result

    result.append(l[0])               # append the city

    if l[1] not in states:
        result.extend([None, None])
    else:
        result.append(states[l[1]])   # append the fully named state
        result.append(regions[l[1]])  # append the region

    return result


# Take a list of school data sets, each in dictionaries, and combine them into one large data set,
# returning a dictionary. Schools that are repeated have their count and total rank increased respectively
def combine_data_sets(data_sets):
    if data_sets is None:
        return None

    result = {}
    for data_set in data_sets:
        for school, info in data_set.iteritems():
            if school not in result:
                result[school] = info
            else:
                result[school][1] += 1        # increment the count by 1
                result[school][2] += info[2]  # add to total rank

    return result


# Take a dictionary of schools and combine entities that represent the same schools but
# may have slightly different names.
# For example "University of California--Los Angeles" and "University of California at Los Angeles"
# are two different strings but represent the same school.
# Return a dictionary with these repeated schools removed
def parse_school_names(schools):
    if schools is None:
        return None

    result = {}

    for school, info in schools.iteritems():
        # school, info
        if school not in result:
            n = 1
            for seen_school in result:
                location1 = result[seen_school][0]
                location2 = info[0]
                if check_same_school(seen_school, school) and location1 == location2:
                    result[seen_school][1] += info[1]
                    result[seen_school][2] += info[2]
                    n = 0
                    break
            if n == 1:
                result[school] = info
        else:
            result[school][1] += info[1]  # update the count
            result[school][2] += info[2]  # update the total rank

    return result


# Check two strings to see if they represent the same school name, returning True in the case
# of a match and false otherwise.
# The substring "&" is expanded to "and" while "-", "of", "and", "in", "at", "the", and "University"
# are removed entirely.
def check_same_school(name1, name2):
    n1 = re.sub(r"\([^)]*\)", "", name1)   # remove words inside parentheses
    n2 = re.sub(r"\([^)]*\)", "", name2)

    n1 = n1.replace("&", "and")            # replace certain strings to remove unneeded identifiers
    n1 = n1.replace("at", " ")
    n1 = n1.replace("of", " ").replace("and", " ")
    n1 = n1.replace("in", " ").replace("the", " ").replace("-", "")
    n1 = n1.replace("University", " ").replace("College", " ").replace("California", " ")
    n2 = n2.replace("&", "and").replace("at", " ")
    n2 = n2.replace("of", " ").replace("and", " ")
    n2 = n2.replace("in", " ").replace("the", " ").replace("-", "")
    n2 = n2.replace("University", " ").replace("College", " ").replace("California", " ")

    n1 = n1.split()                        # convert the strings to lists, splitting at whitespace and '_'
    n2 = n2.split()

    return bool(set(n1) & set(n2))


# Take in a dictionary of schools and return the same dictionary with the total rank
# replaced by the average rank, and the location expanded
def calculate_average_rank_and_location(schools):
    if schools is None:
        return None

    for school, info in schools.iteritems():
        info[0] = parse_location(info[0])
        info[2] /= float(info[1])

    return schools
