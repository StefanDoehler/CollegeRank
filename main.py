from web_scrapers import *
from data_manipulation import *
import database
import sys

if __name__ == "__main__":
    data_sets = []
    possible_data_sets = [
        scrape_best_colleges(),
        scrape_niche(),
        scrape_us_news(),
        scrape_college_raptor(),
        scrape_best_schools()
    ]

    for ds in possible_data_sets:
        if isinstance(ds, dict):
            data_sets.append(ds)
        else:
            print ds + " is broken"  # the broken url is returned from scraper in the case of failure

    school_list = combine_data_sets(data_sets)

    if school_list is None:
        print "Data set is broken"
        sys.exit(1)

    proper_names = parse_school_names(school_list)
    final_list = calculate_average_rank_and_location(proper_names)

    con = database.connect_db()
    cursor = con.cursor()
    for name, info in final_list.iteritems():
        if not info[0]:
            continue
    #    print name, info
    #    print name, info[0][0], info[0][1], info[0][2], info[1], info[2]
        database.add_school(name, info, con, cursor)

    cursor.close()
    con.close()
