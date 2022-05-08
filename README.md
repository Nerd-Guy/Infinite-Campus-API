# Infinite-Campus-API
An API wrapper for [Infinite Campus](https://www.infinitecampus.org) in Python. To create a new student:
```python
s = Student("School District Here", "State Here", "Username Here", "Password Here")
s.start_session()
```
Get all the terms of the student from the current school year:
```python
terms = s.get_terms()
```
