import pytest
from unittest.mock import MagicMock, patch
from core import selenium_util


def test_get_link_from_element_success():
    mock_element = MagicMock()
    mock_element.get_attribute.return_value = "https://example.com"
    result = selenium_util.get_link_from_element(mock_element)
    assert result == "https://example.com"


def test_get_link_from_element_failure():
    mock_element = MagicMock()
    mock_element.get_attribute.side_effect = Exception("No attribute")
    result = selenium_util.get_link_from_element(mock_element)
    assert result is None


def test_get_link_from_elements():
    mock_element_1 = MagicMock()
    mock_element_1.get_attribute.return_value = "https://a.com"

    mock_element_2 = MagicMock()
    mock_element_2.get_attribute.return_value = None  # Should be skipped

    mock_element_3 = MagicMock()
    mock_element_3.get_attribute.return_value = "https://b.com"

    elements = [mock_element_1, mock_element_2, mock_element_3]
    result = selenium_util.get_link_from_elements(elements)
    assert result == ["https://a.com", "https://b.com"]


@patch("core.selenium_util.webdriver.Chrome")
def test_go_to_url(mock_chrome):
    mock_driver = MagicMock()
    mock_chrome.return_value = mock_driver
    selenium_util.go_to_url(mock_driver, "https://example.com")
    mock_driver.get.assert_called_once_with("https://example.com")
    mock_driver.implicitly_wait.assert_called_once_with(10)


@patch("core.selenium_util.webdriver.Chrome")
def test_scroll_down(mock_chrome):
    mock_driver = MagicMock()
    mock_chrome.return_value = mock_driver
    selenium_util.scroll_down(mock_driver, 500)
    mock_driver.execute_script.assert_called_once_with("window.scrollBy(0, 500);")


@patch("core.selenium_util.webdriver.Chrome")
def test_click_on_text_success(mock_chrome):
    mock_driver = MagicMock()
    mock_element = MagicMock()
    mock_driver.find_element.return_value = mock_element

    selenium_util.click_on_text(mock_driver, "Play")
    mock_driver.find_element.assert_called_once()
    mock_element.click.assert_called_once()


@patch("core.selenium_util.webdriver.Chrome")
def test_click_on_text_failure(mock_chrome):
    mock_driver = MagicMock()
    mock_driver.find_element.side_effect = Exception("Not found")

    # Should not raise, just print error
    selenium_util.click_on_text(mock_driver, "Play")

@patch("core.selenium_util.get_driver")
def test_get_movie_info_from_link_success(mock_get_driver):
    mock_driver = MagicMock()
    mock_get_driver.return_value = mock_driver

    # Images
    image_1 = MagicMock()
    image_1.get_attribute.return_value = "poster.jpg"
    image_2 = MagicMock()
    image_2.get_attribute.return_value = "backdrop.jpg"

    # Duration elements
    duration_1 = MagicMock()  # index 0
    duration_2 = MagicMock()
    duration_2.text = "Duration\n 120 mins"

    # Description
    tab_content = MagicMock()
    tab_content.text = "This is the description"

    # Trailer iframe
    iframe = MagicMock()
    iframe.get_attribute.return_value = "https://www.youtube.com/embed/abc123"

    # Setup full find_elements (4 calls)
    mock_driver.find_elements.side_effect = [
        [image_1, image_2],                # 1. for poster/backdrop
        [duration_1, duration_2],          # 2. for duration (get index 1)
        [tab_content],                     # 3. for description
        [iframe]                           # 4. for trailer
    ]

    # Setup full find_element (7 calls)
    mock_driver.find_element.side_effect = [
        MagicMock(text="Movie Title"),                              # name
        MagicMock(text="Director\n John Smith"),                    # director
        MagicMock(text="Actors\n Actor A, Actor B"),                # actors
        MagicMock(text="Genres\n Action"),                          # genres
        MagicMock(text="Release Date\n 2023-06-01"),                # release_date
        MagicMock(text="Language\n English"),                       # language
        MagicMock(text="Rated\n PG-13"),                            # rated
    ]

    result = selenium_util.get_movie_info_from_link("https://movie.com/details")

    assert result["name"] == "Movie Title"
    assert result["director"] == "John Smith"
    assert result["actors"] == "Actor A, Actor B"
    assert result["genres"] == "Action"
    assert result["release_date"] == "2023-06-01"
    assert result["duration"] == "120 mins"
    assert result["language"] == "English"
    assert result["rating"] == "PG-13"
    assert result["description"] == "This is the description"
    assert result["poster_path"] == "poster.jpg"
    assert result["backdrop_path"] == "backdrop.jpg"
    assert result["trailer"] == "https://www.youtube.com/watch?v=abc123"
    assert result["link"] == "https://movie.com/details"
    mock_driver.quit.assert_called_once()


@patch("core.selenium_util.get_driver")
def test_get_movie_info_from_link_failure(mock_get_driver):
    mock_driver = MagicMock()
    mock_get_driver.return_value = mock_driver
    mock_driver.find_element.side_effect = Exception("Broken page")
    result = selenium_util.get_movie_info_from_link("https://broken.com")
    assert "error" in result
    assert result["link"] == "https://broken.com"
    mock_driver.quit.assert_called_once()
