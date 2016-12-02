from web_scrapers import scrape_best_schools, scrape_us_news, scrape_best_colleges, scrape_college_raptor, scrape_niche
import data_manipulation

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
        if