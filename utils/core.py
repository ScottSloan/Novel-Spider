import requests
import parsel

from urllib.parse import quote
from io import StringIO
from math import ceil

from .config import Config

class Site:
    id = 0
    name = site_url = search_url = ""

    search_name_css = search_author_css = search_url_css = ""

    chapter_name_list_css = chapter_url_list_css = ""

    chapter_content_css = ""

    site_list = []
    
class SearchResult:
    count = 0
    
    name_list = author_list = url_list = []

class BookInfo:
    name = author = url = ""

    chapter_count = 0
    chapter_name_list = chapter_url_list = []
    
    current_chapter_name = current_chapter_url = ""
    current_chapter_content = StringIO()

class DownloadInfo:
    filepath, filetype = "", 0

    group_list = group_list_str = []

    download_chapter_index = []

    content, file = {}, StringIO()

    download_count = complete_count = 0

    error_count = 0
    
def request_get(url: str, on_error):
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47"}       
    
    for i in range(Config.request_retry_times):
        try:
            req = requests.get(url, timeout = Config.request_timeout, headers = header)
            req.encoding = "utf-8"

            return req.text

        except requests.RequestException as e:
            if i == Config.request_retry_times - 1:
                on_error(str(e))

                return e
            
            else:
                continue

def search_book(keywords: str, on_error):
    url = Site.search_url + quote(keywords, encoding = "utf-8")
    
    selector = parsel.Selector(request_get(url, on_error))
    
    SearchResult.name_list = selector.css(Site.search_name_css).extract()
    SearchResult.author_list = selector.css(Site.search_author_css).extract()
    SearchResult.url_list = selector.css(Site.search_url_css).extract()

    SearchResult.count = len(SearchResult.name_list)
    
    process_author_list()
    process_url_list()

def process_author_list():
    count =  SearchResult.count
    author_list = SearchResult.author_list
    
    if count != 0 and author_list[0].startswith("作者"):    
        for index in range(count):
            temp = author_list[index]

            temp = temp.replace("作者", "")
            temp = temp.replace("：", "")
        
            SearchResult.author_list[index] = temp

def process_url_list():
    count =  SearchResult.count
    url_list = SearchResult.url_list

    if count != 0 and not url_list[0].startswith("http"):
        for index in range(count):
            temp = url_list[index]

            temp = Site.site_url + temp

            SearchResult.url_list[index] = temp

def get_book_chapters(url: str, on_error):
    selector = parsel.Selector(request_get(url, on_error))

    BookInfo.chapter_name_list = selector.css(Site.chapter_name_list_css).extract()
    BookInfo.chapter_url_list = selector.css(Site.chapter_url_list_css).extract()
    
    process_chapter_name_list()
    process_chapter_url_list()

    BookInfo.chapter_count = len(BookInfo.chapter_url_list)

def process_chapter_name_list():
    string = "<<---展开全部章节--->>"
    
    if string in BookInfo.chapter_name_list:
        BookInfo.chapter_name_list.remove(string)

def process_chapter_url_list():
    string = "javascript:dd_show()"

    if string in BookInfo.chapter_url_list:
        BookInfo.chapter_url_list.remove(string)

    if not BookInfo.chapter_url_list[0].startswith("http"):
        for index in range(len(BookInfo.chapter_url_list)):
            value = BookInfo.chapter_url_list[index]

            if BookInfo.chapter_url_list[index].startswith("http"):
                del BookInfo.chapter_name_list[index:]
                del BookInfo.chapter_url_list[index:]
                
                break

            new = Site.site_url + value

            BookInfo.chapter_url_list[index] = new

def get_chapter_content(url: str, on_error):
    selector = parsel.Selector(request_get(url, on_error))
    
    return process_chapter_content(selector.css(Site.chapter_content_css).extract())

def process_chapter_content(temp: list):
    temp_list = ["\r\n\t\t", "『点此报错』", "『加入书签』"]

    for value in temp_list:
        if value in temp:
            temp.remove(value)

    return StringIO("\n\n".join(temp))

def get_group_list(each: int):
    total = BookInfo.chapter_count

    group_count = ceil(total / each)

    group_list_dict = {}

    if each == 1:
        DownloadInfo.group_list_str = ["第 {} 章".format(i + 1) for i in range(BookInfo.chapter_count)]
        return

    for i in range(group_count):
        start = i * each + 1 if i != 0 else 1
        end = (i + 1) * each if i != group_count - 1 else total
        
        temp = (start - 1, end)

        temp_str = "第 {} 章 - 第 {} 章".format(start, end)

        group_list_dict[temp_str] = temp

    DownloadInfo.group_list = list(group_list_dict.values())
    DownloadInfo.group_list_str = list(group_list_dict.keys())