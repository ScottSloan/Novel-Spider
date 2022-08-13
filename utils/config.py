import os

class Config:
    # app
    app_name = "小说爬取工具"
    app_version = "V1.01"

    # download
    download_path = os.path.join(os.getcwd(), "download")
    add_chapter_title = True
    thread_number = 50

    # request
    request_timeout = 5
    request_retry_times = 3
