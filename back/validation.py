import re
from bs4 import BeautifulSoup
import requests


# A url validation funtion
def contains_wikinews(url):
    """
    Function to check if the input string contains the regex pattern.

    Parameters:
    input_string (str): The string to be searched.
    pattern_string (str): The regex pattern to search for.

    Returns:
    bool: True if the pattern is found in the input string, False otherwise.
    """

    # Compile the regex pattern from the pattern string
    pattern = re.compile(r"\bhttps?://.*wikinews.org\b")

    # Search for the pattern in the input string
    match = pattern.search(url)

    # Return True if a match is found, False otherwise
    return bool(match)


# string_to_check = "Check out this news article: https://en.wikinews.org/wiki/Main_Page."
# result = contains_wikinews(string_to_check)
# print(result)


def website_validator(url):
    try:
        response = requests.get(url)
        # Ensure the request was successful
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all h1 tags
        h1_tags = soup.find_all("h1")

        # Check if any h1 tag contains 'Page not found'
        for h1 in h1_tags:
            if h1.get_text().strip() == "Page not found":
                return False

        # Return True if 'Page not found' is not found in any h1 tag
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def check_wiki(url):
    try:
        response = requests.get(url)
        # Ensure the request was successful
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all a tags
        a_tags = soup.find_all("a")

        # Check if any a tag contains 'Create an account'
        for tag in a_tags:
            if (
                "create an account" in tag.get_text()
                or "crea una cuenta" in tag.get_text()
            ):
                return False

        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
