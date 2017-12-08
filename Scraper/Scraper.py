from Database import Database
import requests
import bs4

# CTRL + ALT + L
url_list = ["https://unleashed.be/team/?department=care", "https://unleashed.be/team/?department=consumer",
            "https://unleashed.be/team/?department=consumer", "https://unleashed.be/team/?department=people",
            "https://unleashed.be/team/?department=technology"]


class Scraper:

    def __init__(self, url, habitat_id, database):
        self.url = url
        self.database = database
        self.habitat_id = habitat_id

    def extract_persons(self):
        print("Retrieving info from department: " + self.url.split("=")[1])

        self.html = requests.get(self.url)
        self.soup = bs4.BeautifulSoup(self.html.content, 'html.parser')

        for member_code in self.soup.findAll("div", {"class": "member"}):
            html_span = member_code.span.extract().get_text("|", strip=True)
            self.name = html_span.split("|")[0]
            self.job_title = html_span.split("|")[1]

            self.before_picture = ""
            for link in member_code.findAll('img'):

                if self.before_picture is "":
                    self.before_picture = link['src']
                else:
                    self.after_picture = link['src']
            self.upload_person()

    def upload_person(self):
        self.database.add_user(self.habitat_id, self.name, self.job_title, self.before_picture, self.after_picture)


if __name__ == "__main__":

    database = Database()
    database.reset_and_delete()

    for url in range(0, len(url_list)):
        print('Working on url nr.%d: %s' % (url, url_list[url]))
        scraper = Scraper(url_list[url], url + 1, database)
        scraper.extract_persons()

    database.count_employees()
    database.close_connection()



