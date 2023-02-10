from booking.booking import Booking

with Booking() as bot:
    bot.land_first_page()
    # bot.change_currency(currency='USD')
    bot.accept_cookies()
    bot.select_place_to_go("warsaw")
    bot.select_dates(check_in_date="2023-02-20", check_out_date="2023-02-23")
    bot.click_search()
    bot.apply_filtrations()
    bot.refresh() # A workaround to let our bot to grab the data properly
    bot.report_results()