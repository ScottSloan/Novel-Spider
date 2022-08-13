import os
import sqlite3

from .core import Site

def query(sql: str, fetch = False):
    with sqlite3.connect(os.path.join(os.getcwd(), "site.db")) as db:
        cursor = db.cursor()

        cursor.execute(sql)
        db.commit()

        if fetch: return cursor.fetchall()

def load_site_cfg(site_id: int):
    sql_1 = "SELECT * FROM site"

    result = query(sql_1, True)[site_id]

    Site.id = result[0]
    Site.name = result[1]
    Site.site_url = result[2]

    Site.search_url = result[3]
    Site.search_name_css = result[4]
    Site.search_author_css = result[5]
    Site.search_url_css = result[6]
    
    Site.chapter_name_list_css = result[7]
    Site.chapter_url_list_css = result[8]
    
    Site.chapter_content_css = result[9]

    sql_2 = "SELECT name FROM site"

    Site.site_list = query(sql_2, True)[0]