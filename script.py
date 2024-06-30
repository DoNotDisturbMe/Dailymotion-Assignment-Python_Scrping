from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter
import time

def scrape_tseries_videos(url, max_videos=500):
    service = Service(r"./chromedriver.exe")  # Use raw string for Windows paths
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    video_ids = []

    while len(video_ids) < max_videos:
        try:
            # Wait for the video cards to load (increased timeout)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-testid="video-card"]')))

            # Extract all video links on the page
            video_links = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="video-card"]')
            for link in video_links:
                video_url = link.get_attribute('href')
                video_ids.append(video_url)
                if len(video_ids) >= max_videos:
                    break

            # Scroll down to load more videos if available
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait briefly before scraping the next batch (adjust as necessary)
            time.sleep(2)
        except TimeoutError:
            # If timeout occurs, wait and retry
            print("Timeout occurred, waiting and retrying...")
            time.sleep(10)
        except Exception as e:
            print(f"Exception occurred: {e}")
            print("Page source:\n", driver.page_source)
            break

    driver.quit()
    return video_ids[:max_videos]  # Return up to max_videos

def count_most_frequent_alphabet(video_ids):
    # Extract only the video IDs from the URLs
    video_ids = [url.split('/')[-1] for url in video_ids]

    # Join all video IDs into a single string
    all_ids = ''.join(video_ids)

    # Count the frequency of each alphabet character
    counter = Counter(char.lower() for char in all_ids if char.isalpha())  # Count only alphabetic characters

    return counter

if __name__ == '__main__':
    url = 'https://www.dailymotion.com/tseries2'
    max_videos = 500

    # Scrape 500 video URLs
    video_urls = scrape_tseries_videos(url, max_videos)
    print(f"First {max_videos} video URLs: {video_urls}")

    # Count alphabet frequencies in video IDs
    character_counts = count_most_frequent_alphabet(video_urls)

    # Print character frequencies in real-time
    print("\nCharacter frequencies:")
    for char, count in character_counts.items():
        print(f"Character: {char}, Count: {count}")

    # Find and print the most frequent character
    most_common_char, most_common_count = character_counts.most_common(1)[0]
    print(f"\nMost frequent character: {most_common_char}, Count: {most_common_count}")
