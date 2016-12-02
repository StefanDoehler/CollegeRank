from web_scrapers import *
from data_manipulation import *
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
