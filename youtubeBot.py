from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import random
import requests

# List of common user agents to randomize browser identification
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
]

# Get proxies from proxy.txt
proxy_list = []
try:
    with open('proxy.txt') as fil:
        proxy_list = [i.strip() for i in fil if i.strip()]
except FileNotFoundError:
    print("Error: proxy.txt not found!")
    exit(1)

if not proxy_list:
    print("Error: No proxies found in proxy.txt!")
    exit(1)

# Get input from user
URLs = input("Enter YouTube video URL(s) (comma-separated for multiple): ").split(',')
URLs = [url.strip() for url in URLs if url.strip()]

timeToReopenBrowser = int(input("Reopen the browser n times: "))
videoLength = int(input("How long is the video (in seconds)?: "))
headless = input("Run in headless mode? (y/n): ").lower() == 'y'

def is_proxy_working(proxy_ip_port):
    """Check if proxy is working before using it"""
    try:
        response = requests.get('http://httpbin.org/ip', proxies={'http': f'http://{proxy_ip_port}', 'https': f'http://{proxy_ip_port}'}, timeout=5)
        return response.status_code == 200
    except:
        return False

def simulate_human_behavior(driver, duration):
    """Simulate human-like behavior: scrolling, pausing, etc."""
    actions = ActionChains(driver)
    start_time = sleep.__module__
    
    # Random scrolling
    for _ in range(random.randint(3, 8)):
        scroll_amount = random.randint(2, 5)
        driver.execute_script(f"window.scrollBy(0, {scroll_amount * 100});")
        sleep(random.uniform(2, 5))
    
    # Scroll back up
    driver.execute_script("window.scrollTo(0, 0);")
    
    # Random mouse movements on video player
    try:
        video_element = driver.find_element(By.TAG_NAME, "video")
        actions.move_to_element(video_element).perform()
        sleep(random.uniform(1, 3))
    except:
        pass

# Watch videos
for video_url in URLs:
    print(f"\n--- Processing: {video_url} ---")
    
    for attempt in range(timeToReopenBrowser):
        # Select random proxy
        proxy_ip_port = random.choice(proxy_list)
        
        # Validate proxy before using (optional - can slow down, remove if needed)
        # if not is_proxy_working(proxy_ip_port):
        #     print(f"Proxy {proxy_ip_port} not working, skipping...")
        #     continue
        
        print(f"[{attempt + 1}/{timeToReopenBrowser}] Using proxy: {proxy_ip_port}")
        
        try:
            # Set up Chrome options
            chrome_options = Options()
            
            if headless:
                chrome_options.add_argument("--headless")
            
            # Add random user agent
            user_agent = random.choice(USER_AGENTS)
            chrome_options.add_argument(f"user-agent={user_agent}")
            
            # Additional options for stealth
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-web-resources")
            chrome_options.add_argument("--disable-default-apps")
            
            # Set proxy
            proxy = Proxy()
            proxy.proxy_type = ProxyType.MANUAL
            proxy.http_proxy = proxy_ip_port
            proxy.ssl_proxy = proxy_ip_port
            proxy.add_to_capabilities(chrome_options.to_capabilities())
            
            # Launch Chrome
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(video_url)
            
            # Random initial wait
            initial_wait = random.uniform(2, 5)
            print(f"Waiting {initial_wait:.1f}s for page to load...")
            sleep(initial_wait)
            
            # Simulate human behavior
            simulate_human_behavior(driver, videoLength)
            
            # Watch video with random pauses
            print(f"Watching video for {videoLength}s...")
            elapsed = 0
            while elapsed < videoLength:
                pause_duration = random.uniform(5, 15)
                sleep(min(pause_duration, videoLength - elapsed))
                elapsed += pause_duration
                print(f"Progress: {min(elapsed, videoLength):.0f}s / {videoLength}s")
            
            # Random final wait
            final_wait = random.uniform(2, 5)
            sleep(final_wait)
            
            print("✓ Video completed")
            
        except Exception as e:
            print(f"✗ Error: {str(e)}")
        
        finally:
            try:
                driver.quit()
            except:
                pass
        
        # Random wait between browser sessions
        if attempt < timeToReopenBrowser - 1:
            next_wait = random.uniform(3, 8)
            print(f"Waiting {next_wait:.1f}s before next session...\n")
            sleep(next_wait)

print("\n✓ All videos completed!")

# https://openproxy.space/api replace static proxies
