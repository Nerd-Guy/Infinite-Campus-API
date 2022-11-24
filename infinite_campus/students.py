from __future__ import annotations

from .notifications import Notification
from .assignments import Assignment
from .terms import Term
from .district import District

import requests
import xmltojson
import json


class StudentException(BaseException):
    pass


SUCCESS_MSG = "success"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}


class Student:
    """Student class for Infinite Campus students"""

    def __init__(
        self, district: str | District, state: str, username: str, password: str
    ) -> None:
        self.district_name = district
        self.state = state
        self.username = username
        self.password = password
        self.__session = requests.Session()

    def log_in(self) -> None:
        """
        Attempts to log in to IC as student.
        """
        self.district = District(self.district_name, self.state)
        self.district.validate()

        # Send a request verifying the student's login credentials
        user_reponse = self.__session.get(
            "{}/verify.jsp?nonBrowser=true&username={}&password={}&appName={}".format(
                self.district.district_baseurl,
                self.username,
                self.password,
                self.district.district_app_name,
            ),
            headers=HEADERS,
        )
        # Throw exception if there is an error with verifying the student's login credentials
        if not SUCCESS_MSG in user_reponse.text:
            raise StudentException("Error verifying student's login credentials")

    def get_notifications(self) -> list[Notification]:
        """
        Get all recent notifications from student.
        Returns a list of notification objects.
        """
        # Send a request to retrieve notifications
        notifcation_response = self.__session.get(
            "{}prism?x=notifications.Notification-retrieve".format(
                self.district.district_baseurl
            ),
            headers=HEADERS,
        )
        # Load notification xml file into JSON format
        notifcation_response_json = json.loads(
            xmltojson.parse(notifcation_response.text)
        )
        # Get the list of notifications in the JSON
        notification_json_list = notifcation_response_json["campusRoot"][
            "NotificationList"
        ]["Notification"]
        notifications: list[Notification] = list()
        # Add each notification from JSON to a notification object in notifications list with data from JSON
        for notification_content in notification_json_list:
            notifications.append(
                Notification(
                    # Add a notification to notifications with each attribute from the JSON
                    # Remove prefix @ which occurs in every key in the JSON
                    **{
                        attr.removeprefix("@"): value
                        for (attr, value) in notification_content.items()
                    }
                )
            )
        return notifications

    def get_assignments(self) -> list[Assignment]:
        """
        Get all assignments from the current school year from the student.
        Returns a list of assignment objects.
        """
        assignment_response = self.__session.get(
            "{}api/portal/assignment/listView".format(
                self.district.district_baseurl
            ),
            headers=HEADERS,
        )
        assignment_response_json = json.loads(assignment_response.text)
        assignments: list[Assignment] = []
        for assignment_data in assignment_response_json:
            assignments.append(Assignment(**assignment_data))
        return assignments

    def get_terms(self) -> list[Term]:
        """
        Get all terms from student.
        Returns a list of Term objects
        """
        # Send a request to retrieve courses/grades
        term_response = self.__session.get(
            "{}resources/portal/grades/".format(self.district.district_baseurl),
            headers=HEADERS,
        )
        # Get the list of terms in the JSON
        term_response_json = json.loads(term_response.text)
        term_json_list = term_response_json[0]["terms"]
        terms: list[Term] = list()
        # Add each term from JSON to a term object in terms list with data from the JSON
        for term in term_json_list:
            terms.append(
                Term(
                    # Add a term to terms with each attribute from the JSON
                    **term
                )
            )
        return terms
