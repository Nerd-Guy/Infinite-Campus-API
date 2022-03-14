
class Notification:
    """
    Notifcation class for student notifications.
    Each notification has a notificationID, userID,
    creationTimestamp, notifcationTypeID, read,
    notificationText, notificationTypeText,
    displayedDate, finalText, and finalUrl.
    """
    # A dataclass should be used here but **unused needs to be here since we may get unexpected attributes passed. 
    def __init__(self, notificationID: int, userID: int,
        creationTimestamp: str, notificationTypeID: int,
        read: bool, notificationText: str,
        notificationTypeText: str,  displayedDate: str, 
        finalText: str, finalUrl: str, **unused):
        self.notificationID = notificationID
        self.userID = userID
        self.creationTimestamp = creationTimestamp
        self.notificationTypeID = notificationTypeID
        self.read = read
        self.notificationText = notificationText
        self.notificationTypeText = notificationTypeText
        self.displayedDate = displayedDate
        self.finalText = finalText
        self.finalUrl = finalUrl
        self.unused = unused

    def __repr__(self):
        return "{}: {}.".format(
            self.displayedDate, self.notificationText 
        )
