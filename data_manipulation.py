from common import states, regions
import re
from main import scrape_niche, scrape_best_schools, scrape_best_colleges, scrape_college_raptor, scrape_us_news


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


def combine_data_sets(data_sets):
    result = {}
    for data_set in data_sets:
        for school, info in data_set.iteritems():
            if school not in result:
                result[school] = info
            else:
                result[school][2] += 1        # increment the count by 1
                result[school][3] += info[3]  # add to total rank

    return result


def parse_school_names(schools):
    result = {}
    locations = {}  # manage an extra dict to provide fast lookup for location

    for school, info in schools.iteritems():
        location = info[1]

        if location not in locations:
            result[school] = info
            locations[location] = [info[0], school, info[2], info[3]]
        else:
            seen_school = locations[location]      # school that is already stored in results

            if check_same_school(seen_school[1], school):  # schools have same name, spelled differently
                result[seen_school][2] += info[2]  # update the count
                result[seen_school][3] += info[3]  # update the total rank
            else:  # schools have same location, but are not the same school
                result[school] = info

    return result


def check_same_school(name1, name2):
    n1 = re.sub(r"\([^)]*\)", "", name1)   # remove words inside parentheses
    n2 = re.sub(r"\([^)]*\)", "", name2)

    n1 = n1.replace("&", "and")            # replace certain chars to remove unneeded identifiers
    n1 = n1.replace("at", " ")
    n1 = n1.replace("of", " ")
    n1 = n1.replace("and", " ")
    n1 = n1.replace("in", " ")
    n1 = n1.replace("the", " ")
    n1 = n1.replace("-", "")
    n1 = n1.replace("University", " ")
    n2 = n2.replace("&", "and")
    n2 = n2.replace("at", " ")
    n2 = n2.replace("of", " ")
    n2 = n2.replace("and", " ")
    n2 = n2.replace("in", " ")
    n2 = n2.replace("the", " ")
    n2 = n2.replace("-", "")
    n2 = n2.replace("University", " ")

    n1 = n1.split()                        # convert the strings to lists, splitting at whitespace and '_'
    n2 = n2.split()

    return bool(set(n1) & set(n2))

l = [scrape_niche(), scrape_us_news(), scrape_college_raptor(), scrape_best_colleges(), scrape_best_schools()]
r = combine_data_sets(l)
#for school, info in r.iteritems():
#    print str(info[0])+' | '+school+' | '+info[1]+' | '+str(info[2])+' | '+str(info[3])
final = parse_school_names(r)
for school, info in final.iteritems():
    print str(info[0])+' | '+school+' | '+info[1]+' | '+str(info[2])+' | '+str(info[3])
