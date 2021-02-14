from BasicFuncs import BasicFuncs


basic_func = BasicFuncs()
news_list = basic_func.get_islander_news()
basic_func.create_checkpoint(news_list)
basic_func.create_telegram_send_conf()
basic_func.send_notification('島民衛星 Islander', news_list)
