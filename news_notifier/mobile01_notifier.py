from BasicFuncs import BasicFuncs


basic_func = BasicFuncs()
news_list = basic_func.get_mobile01_hot_news()
basic_func.create_checkpoint(news_list)
basic_func.create_telegram_send_conf()
basic_func.send_notification('Mobile 01', news_list)
