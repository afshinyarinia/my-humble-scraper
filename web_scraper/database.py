import sqlite3
import logging

class Database:
  def __init__(self, db_name='data/scraper.db'):
      self.db_name = db_name
      self.setup_database()

  def setup_database(self):
      conn = sqlite3.connect(self.db_name)
      c = conn.cursor()
      c.execute('''CREATE TABLE IF NOT EXISTS scraped_data
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    domain TEXT,
                    content TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
      conn.commit()
      conn.close()

  def save_data(self, url, domain, content):
      conn = sqlite3.connect(self.db_name)
      c = conn.cursor()
      c.execute("INSERT INTO scraped_data (url, domain, content) VALUES (?, ?, ?)",
                (url, domain, content))
      conn.commit()
      conn.close()
      logging.info(f"Data saved to database: {self.db_name}")