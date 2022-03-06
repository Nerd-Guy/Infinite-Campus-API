from math import dist
from platformdirs import user_state_dir
import requests
import xmltodict

class Student:
    def __init__(self, district, state, username, password) -> None:
        self.district  = district
        self.state     = state
        self.username  = username
        self.password  = password
        self.app_name  = district
        self.dist_url  = "https://{}{}.infinitecampus.org/campus".format(
            district, state
        )
        self.logged_in = False
        self.session = requests.Session()

    def start_session(self) -> bool:
        headers = {
            "user-agent": 
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        }
        self.request = self.session.get(
            "{}/verify.jsp?nonBrowser=true&username={}&password={}&appName={}".format(
                self.dist_url, self.username, self.password, self.app_name
            ), 
            headers=headers
            )
        return "<AUTHENTICATION>success</AUTHENTICATION>" in self.request.text # this means the login was successful

    def start_portal(self):
        self.portal_session = self.session.get(
            "{}/prism?x=portal.PortalOutline&appName={}".format(
            self.dist_url, self.app_name
        ))
        self.portal = xmltodict.parse(
            self.portal_session.text
        )
        print(self.portal)

def main():
    district = input("Enter district: ")
    state    = input("Enter state: ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    user = Student(district, state, username, password)
    if user.start_session():
        user.start_portal()

if __name__ == "__main__":
    main()
