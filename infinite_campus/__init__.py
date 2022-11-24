from .students import Student

if __name__ == "__main__":
    """An example using this library."""
    my_student = Student(
        input("Enter district: "),
        input("Enter state abbreviation: "),
        input("Enter username: "),
        input("Enter password"),
    )
    my_student.log_in()
