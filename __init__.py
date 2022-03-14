from notification import Notification

import requests
import xmltojson
import json

class DistrictException(BaseException):
    pass

class StudentException(BaseException):
    pass

HEADERS = {
    "user-agent": 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}

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
            ), headers=HEADERS
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
        self.dist_app_name = dist_data["district_app_name"]

        # Send a request verifying the student's login credentials
        user_reponse = self.session.get(
            "{}/verify.jsp?nonBrowser=true&username={}&password={}&appName={}".format(
                self.dist_base_url, self.username, self.password, self.dist_app_name
            ), headers=HEADERS)
        # Throw exception if there is an error with verifying the student's login credentials
        if not "success" in user_reponse.text:
            raise StudentException("Error verifying student's login credentials")

    def get_notifications(self) -> list[Notification]:
        """
        Get all recent notifications from student.
        Returns a list of notifications objects.
        """
        # Send a request to retrieve notifications
        notifcation_response = self.session.get("{}prism?x=notifications.Notification-retrieve".format(
            self.dist_base_url
        ), headers=HEADERS)
        # Load notification xml file into JSON format
        notifcation_response_json = json.loads(xmltojson.parse(
            notifcation_response.text
        ))
        # Get the list of notifications in the JSON
        notification_json_list = notifcation_response_json["campusRoot"]["NotificationList"]["Notification"]
        print(json.dumps(notification_json_list, indent=4))
        notifications: list[Notification] = list()
        # Add each notification from JSON to a notification object in notifications list with data from JSON
        for i, _ in enumerate(notification_json_list):
            notification_content = notification_json_list[i]
            notifications.append(Notification(
                # Add a notification to notifications with each attribute from the JSON
                # Remove prefix @ which occurs in every key in the JSON
                **{attr.removeprefix("@"): value for (attr, value) in notification_content.items()}
            ))
        return notifications

def main():
    """example program"""
    district = input("Enter district: ")
    state    = input("Enter state (e.g ny): ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    user = Student(district, state, username, password)
    user.start_session()
    print(user.get_notifications())

if __name__ == "__main__":
    main()
