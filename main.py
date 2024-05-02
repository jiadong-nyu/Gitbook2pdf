from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import time
import base64

def setup_driver():
    chromedriver_autoinstaller.install()  # Automatically checks and installs the latest chromedriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # Headless mode
    chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration
    chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def save_page_as_pdf(driver, url, output_path):
    driver.get(url)
    time.sleep(2)  # Wait for the page to fully load
    # Setting Chrome print options to output to PDF
    print_option = {
        'printBackground': True,
        'pageRanges': '1',  # Print all pages, you can specify ranges e.g., '1-2'
    }
    pdf = driver.execute_cdp_cmd('Page.printToPDF', print_option)
    with open(output_path, 'wb') as f:
        f.write(base64.b64decode(pdf['data']))

def main():
    driver = setup_driver()
    try:
        base_url = "https://docs.movementlabs.xyz/"
        driver.get(base_url)
        time.sleep(10)  # Wait for the page to fully load
        elements = driver.find_elements(By.CSS_SELECTOR, "a")
        links = {element.get_attribute('href') for element in elements if 'docs.movementlabs.xyz' in (element.get_attribute('href') or '')}
        for link in links:
            output_filename = f"{link.split('/')[-1] if link.split('/')[-1] else 'index'}.pdf"
            save_page_as_pdf(driver, link, output_filename)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
