from prettytable import PrettyTable

from booking.booking import Booking


def run():
    with Booking() as bot:
        bot.land_first_page()
        # bot.change_currency(currency='USD')
        bot.accept_cookies()
        bot.select_place_to_go("warsaw")
        bot.select_dates(check_in_date="2023-02-20", check_out_date="2023-02-23")
        bot.click_search()
        bot.apply_star_rating(4, 5)
        bot.sort_price_lowest_first()
        bot.refresh() # A workaround to let our bot to grab the data properly

        results = bot.extract_results()

    print_results(results)


def print_results(results):
    table = PrettyTable(field_names=["Hotel Name", "Hotel Price", "Hotel Score"])
    table.add_rows(results)
    print(table)


if __name__ == '__main__':
    run()
