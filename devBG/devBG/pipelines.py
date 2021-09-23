import sqlite3

# from itemadapter import ItemAdapter


class DevbgPipeline:
    def __init__(self) -> None:
        self.con = sqlite3.connect('./jobs.db')
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS jobs(
            position TEXT,
            company TEXT,
            location TEXT,
            date TEXT,
            link TEXT,
            is_sent INT
            )"""
        )

    def process_item(self, item, spider):
        self.cur.execute(
            """INSERT OR IGNORE INTO jobs VALUES (?,?,?,?,?,?)""",
            (
                item['position'],
                item['company'],
                item['location'],
                item['date'],
                item['link'],
                0
            )
        )
        self.con.commit()
        return item
