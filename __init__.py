import requests
import xmltojson
import json

class DistrictException(BaseException):
    pass

class StudentException(BaseException):
    pass

class Student:
    """Student class to create and mange Infinite Campus students"""
    def __init__(self, district, state, username, password) -> None:
        self.district  = district
        self.state     = state
        self.username  = username
        self.password  = password
        self.session = requests.Session()

    def start_session(self) -> None:
        """
        Attempts to starts a new Infinite Campus session
        with username and password. Returns True if
        sucessful, False if not.
        """
        # Send a request verifying the district
        district_response = self.session.get(
            "https://mobile.infinitecampus.com/mobile/searchDistrict?query={}&state={}".format(
                self.district, self.state
            )
        )
        # Throw exception if there is an error with verifying the district with the error message provided by IC
        dist_response_json = json.loads(district_response.text)
        if "error" in dist_response_json:
            raise DistrictException(dist_response_json["error"])

        # Set up district variables
        dist_data = dist_response_json["data"][0]
        self.dist_id = dist_data["id"]
        self.dist_name = dist_data["district_name"]
        self.dist_base_url = dist_data["district_baseurl"]
        self.app_name = dist_data["district_app_name"]

        # Send a request verifying the student's login credentials
        user_reponse = self.session.get(
            "{}/verify.jsp?nonBrowser=true&username={}&password={}&appName={}".format(
                self.dist_base_url, self.username, self.password, self.app_name
            ))
        # Throw exception if there is an error with verifying the student's login credentials
        if not "success" in user_reponse.text:
            raise StudentException("Error verifying student's login credentials")

    def start_portal(self):
        """Starts a new portal session for students.
        Must be to obtain data from user."""
        self.portal_session = self.session.get(
            "{}/prism?x=portal.PortalOutline&appName={}".format(
            self.dist_base_url, self.app_name
        ))
        self.portal = xmltojson.parse(
            self.portal_session.text
        )
        print(self.portal)

def main():
    """example program"""
    district = input("Enter district: ")
    state    = input("Enter state:    ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    user = Student(district, state, username, password)
    user.start_session()

if __name__ == "__main__":
    main()
