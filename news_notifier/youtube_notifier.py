from BasicFuncs import BasicFuncs


basic_func = BasicFuncs()
video_list = basic_func.get_youtube_trend()
basic_func.create_checkpoint(video_list)
basic_func.create_telegram_send_conf()
basic_func.send_notification('Youtube 台灣趨勢', video_list)
