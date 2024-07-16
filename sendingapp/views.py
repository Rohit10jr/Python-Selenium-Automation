# Create your views here.
from django.core.mail import send_mail
from django.http import HttpResponse
from django.core.mail import EmailMessage

from django.conf import settings
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def home(request):

    chromedriver_path = os.path.join(settings.BASE_DIR, 'chromedriver.exe')

    # Initialize the WebDriver
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service)

    try:
        # Open the Google Form
        driver.get("https://docs.google.com/forms/d/e/1FAIpQLSdUCd3UWQ3VOgeg0ZzNeT-xzNawU8AJ7Xidml-w1vhfBcvBWQ/viewform")
        driver.maximize_window()

        def wait_and_clear(element):
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable(element))
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.clear()

        # Wait until the input element is present
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'whsOnd'))
        )


        b_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='M7eMe']/b"))
        )

        code_text = b_element.text
        print(code_text)

        input_elements = driver.find_elements(By.CLASS_NAME, 'whsOnd')

        input_data = [
            "J Rohit",         
            "1234567890",     
            "jrohit@example.com",
            "123456",         
            "01/01/1990",      
            "Male"             
        ]

        input_data.append(code_text)

        for element, data in zip(input_elements, input_data):
            wait_and_clear(element)       
            element.send_keys(data)

        # Wait for the textarea element 
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'KHxj8b'))
        )
        textarea_element = driver.find_element(By.CLASS_NAME, 'KHxj8b')
        wait_and_clear(textarea_element)
        textarea_element.send_keys("1234 Main St")  # Full Address

        # Submit the form
        submit_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Submit']"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", submit_button)
        submit_button.click()

        # Wait and capture screenshot
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'response has been recorded')]"))
        )

        # saving screenshot to the specified path
        screenshot_path = os.path.join(settings.BASE_DIR, 'media', 'confirmation_page.png')
        driver.save_screenshot(screenshot_path)

        # Sending the email 
        subject = "Python (Selenium) Assignment - Rohit J"
        body = """
            Dear Sir/Mam,

            I hope this email finds you well.
            
            Best regards,
            Rohit J
            """
        email_from = "sender_mail_id"
        recipient_list = ['recipient_mail']
        cc_list = ['cc_mail']

        email = EmailMessage(subject, body, email_from, recipient_list, cc=cc_list)
        email.content_subtype = 'html'
        email.attach_file(screenshot_path)
        email.send()

    except Exception as e:
        print(f"An error occurred: {e}")
        # Print page source 
        # print(driver.page_source)
    finally:
        time.sleep(30)
        driver.quit()

    return HttpResponse("home page")


