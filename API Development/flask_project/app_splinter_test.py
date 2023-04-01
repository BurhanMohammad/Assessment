from splinter import Browser
from flask import url_for

# Define the base URL for the app
BASE_URL = 'http://localhost:5000'

def test_create_ta():
    # Open a browser instance
    with Browser('chrome') as browser:
        # Navigate to the create TA page
        browser.visit(BASE_URL + url_for('index'))
        browser.click_link_by_text('Create TA')

        # Fill in the form fields
        browser.fill('native_english_speaker', 'True')
        browser.fill('course_instructor', 'John Doe')
        browser.fill('course', 'Intro to Computer Science')
        browser.fill('semester', 'Fall 2022')
        browser.fill('class_size', '25')
        browser.fill('performance_score', '4.5')

        # Submit the form
        browser.find_by_name('submit').click()

        # Check that the TA was created successfully
        assert browser.is_text_present('TA created successfully')

def test_get_ta():
    # Open a browser instance
    with Browser('chrome') as browser:
        # Navigate to the get TA page
        browser.visit(BASE_URL + url_for('index'))
        browser.click_link_by_text('View TA')

        # Click on the first TA in the list
        browser.find_by_css('.ta-link').first.click()

        # Check that the TA information is displayed correctly
        assert browser.is_text_present('John Doe')
        assert browser.is_text_present('Intro to Computer Science')
        assert browser.is_text_present('Fall 2022')
        assert browser.is_text_present('25')
        assert browser.is_text_present('4.5')

def test_update_ta():
    # Open a browser instance
    with Browser('chrome') as browser:
        # Navigate to the get TA page
        browser.visit(BASE_URL + url_for('index'))
        browser.click_link_by_text('View TA')

        # Click on the first TA in the list
        browser.find_by_css('.ta-link').first.click()

        # Click on the edit button
        browser.find_by_css('.edit-button').click()

        # Fill in the form fields
        browser.fill('native_english_speaker', 'False')
        browser.fill('course_instructor', 'Jane Doe')
        browser.fill('course', 'Data Structures')
        browser.fill('semester', 'Spring 2023')
        browser.fill('class_size', '30')
        browser.fill('performance_score', '4.0')

        # Submit the form
        browser.find_by_name('submit').click()

        # Check that the TA was updated successfully
        assert browser.is_text_present('TA updated successfully')

def test_delete_ta():
    # Open a browser instance
    with Browser('chrome') as browser:
        # Navigate to the get TA page
        browser.visit(BASE_URL + url_for('index'))
        browser.click_link_by_text('View TA')

        # Click on the first TA in the list
        browser.find_by_css('.ta-link').first.click()

        # Click on the delete button
        browser.find_by_css('.delete-button').click()

        # Confirm the deletion
        browser.get_modal().click_button('OK')

        # Check that the TA was deleted successfully
        assert browser.is_text_present('TA deleted successfully')
