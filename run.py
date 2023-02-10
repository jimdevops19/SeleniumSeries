from prettytable import PrettyTable

from booking import config
from booking.booking import Booking


def main():
    with Booking() as bot:
        bot.land_first_page()
        bot.select_place_to_go(config.PLACE_TO_GO)
        bot.select_dates(check_in_date=config.CHECK_IN_DATE,
                         check_out_date=config.CHECK_OUT_DATE)
        bot.click_search()
        bot.apply_star_rating(*config.PREFERRED_STAR_RATINGS)
        bot.sort_price_lowest_first()
        bot.refresh()

        results = bot.extract_results()

    print_results(results)


def print_results(results):
    table = PrettyTable(["Hotel Name", "Hotel Price", "Hotel Score"])
    table.add_rows(results)
    print(table)


if __name__ == '__main__':
    main()
