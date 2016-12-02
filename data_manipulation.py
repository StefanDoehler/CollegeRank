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

    if l[1] not in states.keys():
        result.extend([None, None])
    else:
        result.append(states[l[1]])   # append the fully named state
        result.append(regions[l[1]])  # append the region

    return result


def parse_schools(schools):
    result = {}

    for group in schools:
        for school in group:
            pass
            # if check_same_school(school):


def check_same_school(name1, location1, name2, location2):
    name1 = re.sub(r"\([^)]*\)", "", name1)
    name1.replace("&")
    name1 = name1.split(' -')
