from Bot.Booking import Booking
import Bot.constants as const


try:
    with Booking() as bot:
        bot.land_first_page()
        #print("Existing....")  #if indentataion ends then it will directly call exit method in booking class
        bot.change_currency(const.currency)
        bot.select_placetogo(const.place_to_go)
        bot.select_dates(const.check_in_date, const.check_out_date)
        bot.select_adults(const.adults)
        bot.click_search()
        bot.apply_filterations()
        bot.refresh()           #a workaround to let our bot to grab the data properly
        bot.report_results()



except Exception as e:
    if 'in PATH' in str(e):         #matches the string with exception occured
        print(
            'You are trying the run the bot from the command line\n'
            'Please add a PATH to your selenium drivers\n'
            'Windows: \n'
            '        set PATH=%PATH%; C:path-to-your-folder \n\n'
            'Linux: \n'
            '        PATH=$PATH:/path/toyour/folder/  \n'
        )
    else:
        raise       #raise the exception