import os

class Config:
    app_name = "小说爬取工具"

    app_version = "V1.40"

    download_path = os.path.join(os.getcwd(), "download")

    add_chapter_title = True