# 台灣中立消息推播

[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/ClarkChiu/Taiwan-Neutral-NEWS-Notifier.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ClarkChiu/Taiwan-Neutral-NEWS-Notifier/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/ClarkChiu/Taiwan-Neutral-NEWS-Notifier.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ClarkChiu/Taiwan-Neutral-NEWS-Notifier/alerts/)
[![codecov](https://codecov.io/gh/ClarkChiu/Taiwan-Neutral-NEWS-Notifier/branch/main/graph/badge.svg?token=HS0NPXQRFQ)](https://codecov.io/gh/ClarkChiu/Taiwan-Neutral-NEWS-Notifier)

# 簡介

目前台灣遇到了許多困境，身為一個學習資訊也從事資訊業的攻城獅，我相信正確資訊的傳播可以解決許多問題，抹除不公不義，讓這個社會越來越好。因緣際會下看到了台大資工陳縕儂教授所創立之 [島民衛星](https://islander.cc/) 網站後深感佩服，故產生了撰寫機器人推播消息之想法，期望能為台灣正確資訊的傳播盡一份心力。

# 核心理念

推播之消息來源希望符合以下其一要素，也歡迎任何消息來源之建議。

- **運用機器學習技術分析及整合**
- **非個人或非單一組織所建立之內容** 

# 消息來源

- [島民衛星](https://islander.cc/) (修正)
- [PTT 熱門文章](https://www.pttweb.cc/hot/all/today) (修正)
- [Mobile01 熱門文章](https://www.mobile01.com/hottopics.php) (規劃)
- [台灣地區 Youtube 熱門影片前 10 名](https://www.youtube.com/channel/UCBcIWZhWqUwknlxikVHQoyA) (規劃)

# 程式流程

1. 固定間隔時間抓取各網站更新之消息
2. 推播至 Telegram 頻道中

# Telegram 頻道

[**台灣中立消息推播**](https://t.me/Taiwan_Neutral_NEWS_Notifier)

# 備註

- 為避免 Telegram 傳送限制，故訊息傳送會有間隔時間，建議將頻道靜音避免過度頻繁的手機提醒
