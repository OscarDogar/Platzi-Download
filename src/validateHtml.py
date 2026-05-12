from bs4 import BeautifulSoup


def verify_cookie(soup):
    """
    Validate that the provided authenticated session cookie is still valid.

    This function inspects the parsed HTML and checks for the presence of a
    signup/header button that indicates the user is not authenticated. If such
    an element is found, it raises an exception instructing the user to update
    the `COOKIE` value in the `.env` file.

    Args:
        soup: A BeautifulSoup object containing the HTML response to validate.

    Raises:
        Exception: If the HTML suggests the session cookie is invalid or expired.
    """
    button = soup.select_one('button[data-class*="header-signup-button"]')
    if button:
        raise Exception(
            "COOKIE ERROR:\nInvalid cookie. Please check your .env file and update the COOKIE variable with a valid session cookie from Platzi."
        )


def verify_course_page(soup):
    """Validate that the parsed HTML corresponds to a Platzi course page.

    This function checks whether the provided BeautifulSoup object contains the
    expected course page title element. If the element is not found, it raises an
    exception indicating that the URL does not match a valid course page.

    Args:
        soup: BeautifulSoup object representing the parsed HTML document.

    Raises:
        Exception: If the page does not appear to be a valid course page.
    """
    h1 = soup.select_one('h1[class*="CourseHeader_CourseHeader__Title"]')
    if not h1:
        raise Exception(
            "URL ERROR:\nThe provided URL does not correspond to a valid course page. Please check your COURSE_URL variable with a valid Platzi course URL."
        )


def verify_plan(soup):
    """
    Validate whether the parsed course page is accessible with the current account plan.

    This function searches the provided BeautifulSoup object for any `<div>` element
    whose class contains `"ItemLockIndicator"`, which indicates locked content.
    If such an element is found, it raises an exception informing the user that
    their account does not have access to the course content.

    Args:
        soup: BeautifulSoup object representing the HTML content to validate.

    Raises:
        Exception: If locked-content indicators are found, meaning access is restricted.
    """
    div = soup.select_one('div[class*="ItemLockIndicator"]')
    if div:
        raise Exception(
            "ACCESS ERROR:\nYour account does not have access to this course's content. Please check your subscription status on Platzi."
        )


def validate_html(html: str):
    """
    Validate an HTML document by running a sequence of page-specific checks.

    The function parses the provided HTML string into a BeautifulSoup object and
    applies each validator in order:

    1. ``verify_cookie``
    2. ``verify_course_page``
    3. ``verify_plan``

    Each validator receives the parsed soup and is expected to raise an exception
    if validation fails.

    Args:
        html (str): Raw HTML content to validate.

    Returns:
        None

    Raises:
        Exception: Propagates any exception raised by the underlying validators.
    """
    soup = BeautifulSoup(html, "html.parser")
    VALIDATIONS = [
        verify_cookie,
        verify_course_page,
        #verify_plan, # TODO: Change this because some courses take a while to fully load
    ]
    for validation in VALIDATIONS:
        validation(soup)
