from bs4 import BeautifulSoup
from collections import namedtuple
from Table import *
import urllib

class Page:

    def __init__(self, url):
        """
        Retrieves and stores the urllib.urlopen object for a given url
        """

        self.link = urllib.urlopen(url)

    def get_tables(self):
        """
        Extracts each table on the page and places it in a dictionary.
        Converts each dictionary to a Table object. Returns a list of
        pointers to the respective Table object(s).
        """

        raw_html = self.link.read()
        soup = BeautifulSoup(raw_html, "html.parser")
        tables = soup.findAll("table")

        final_tables = []
        for table in tables:
            rows = table.findAll("tr")
            col_list = []
            for row in rows:
                cols = row.findAll("td")
                cols = [e.text.strip() for e in cols]
                col_list.append(cols)
            col_list = [c for c in col_list if len(c) > 0] # remove empties

            # every element in col_list must have the same length
            # otherwise, the table is not properly formatted

            if all(len(i) == len(col_list[0]) for i in col_list):
                # the table is valid, we can convert it to a dict

                table_dict = {}
                for k in range(0, len(col_list[0])):
                    row_data = []
                    for col in col_list:
                        row_data.append(col[k])
                    table_dict[k] = row_data

            # convert to a table object and append to our final list
            final = Table(table_dict)
            final_tables.append(final)

        return final_tables

    def save_tables(self, tables, format, names):
        """
        Extracts the tables from HTML and converts them to the given format
        and returns metadata about the files created
        """

        return True


if __name__ == "__main__":
    url = "https://computerservices.temple.edu/creating-tables-html"
    page = Page(url)
    page.get_tables()
