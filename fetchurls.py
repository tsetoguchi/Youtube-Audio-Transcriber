from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selectolax.parser import HTMLParser

# Function to fetch all video URLs from a YouTube channel or playlist
def fetch_youtube_urls(page_url):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set up Chrome WebDriver
    service = Service(executable_path='C:\\Users\\tao\\.wdm\\drivers\\chromedriver\\win64\\129.0.6668.100\\chromedriver-win32\\chromedriver.exe')  # Adjust the path to your chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Load the YouTube page
    driver.get(page_url)
    time.sleep(3)  # Wait for the page to load

    # Scroll down to load more videos (optional for long pages)
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)  # Wait for new content to load
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Get the HTML content of the page
    page_source = driver.page_source

    # Parse the HTML using selectolax
    tree = HTMLParser(page_source)

    # Find all video links using XPath-like selection
    video_elements = tree.css('a#video-title')

    # Extract the href attributes (video URLs)
    video_urls = [element.attributes.get('href') for element in video_elements if element.attributes.get('href')]

    # Close the browser
    driver.quit()

    # Convert relative URLs to full URLs (YouTube video links are sometimes relative)
    video_urls = [f"https://www.youtube.com{url}" if not url.startswith("http") else url for url in video_urls]

    return video_urls


# Example usage
if __name__ == "__main__":
    youtube_page_url = 'https://www.youtube.com/@CloserToTruthTV'  # Replace with the actual channel or playlist URL
    video_urls = fetch_youtube_urls(youtube_page_url)

    print(len(video_urls))

    # Print the list of video URLs
    for url in video_urls:
        print(url)