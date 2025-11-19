Intelligent Registration Form Validation & Selenium Automation

A complete implementation of Section A – Task 2: Build & Automate an Intelligent Registration System for Frugal Testing Software Engineer Assignment.

This project contains:

✅ A responsive Registration Form Web Page (registration.html)

✅ Full client-side form validations using HTML, CSS, and JavaScript

✅ Success & error user feedback messages

✅ A lightweight backend runner (app.py) to serve the page

✅ Complete Selenium test automation for Negative, Positive & Logic Validation scenarios

✅ Screenshots + execution video (as required)

📌 Project Objective

Build a modern, user-friendly registration form with strong validations and automate the entire workflow using Selenium.

This project covers:

Registration Form UI

Client-side validations

Automation with Selenium

Negative, Positive & Logic Testing

Screenshots + video recording

GitHub submission (this repo)

🧩 1. Registration Form Web Page

The file registration.html includes the following required fields:

Field	Validation
First Name	Required
Last Name	Required
Email	Required + no disposable domains
Phone Number	Required + must start with valid country code
Age	Optional
Gender	Required (Male/Female/Other)
Address	Optional
Country, State, City	Dropdowns (dynamic behavior tested)
Password	Strength meter (Weak/Medium/Strong)
Confirm Password	Must match Password
Terms & Conditions	Required checkbox
✔ Client-Side Validation Implemented

Highlights invalid fields in red

Displays inline error messages

Disables Submit button until all required fields are valid

Validates phone number format

Validates email domain (blocks temporary emails like @tempmail.com)

Password Strength Meter using JavaScript

Success message displayed after valid submission

Scroll-to-top error banner for invalid submission

🧪 2. Automation Testing Using Selenium

The automation script validates all flows specified in the assignment.

Selenium Test File:
test_registration_form.py

Automation performed using:

Selenium WebDriver

Python

ChromeDriver / WebDriverManager

PyTest (optional)

🧪 Automation Flow A — Negative Scenario
Steps:

Launch the registration page

Print page URL & Title

Fill form with:

First Name → entered

Last Name → ❌ skipped

Email → valid

Phone → valid

Gender → selected

All other required fields → filled

Click Submit

Verify:

Error message for missing Last Name

Invalid fields highlighted

Capture screenshot → error-state.png

🟢 Automation Flow B — Positive Scenario
Steps:

Fill all fields with valid values

Password & Confirm Password match

Accept Terms & Conditions

Submit

Verify:

Success message displayed

Form fields reset

Capture screenshot → success-state.png

🔄 Automation Flow C — Logic Validation
Validations Covered:

Changing Country → updates States dropdown

Changing State → updates Cities dropdown

Password Strength Meter working

Mismatched Confirm Password shows error

Submit button remains disabled until:

All required fields valid

Passwords match

T&C checkbox selected

🗂 Project Structure
RegisterFormValidationTestSelenium/
│
├── registration.html
├── app.py
├── screenshots/
│   ├── error-state.png
│   └── success-state.png
│
│
└── README.md

▶️ How to Run the Project
1. Run the Web Page (Flask Server)
Install dependencies
pip install flask selenium webdriver-manager pytest

Start the app
python app.py


2. Run Selenium Tests

Start the server first.

Then run:

python tests/test_registration_form.py


or if using pytest:

pytest -s


Screenshots will be saved into /screenshots.

🖼 Screenshots Included

error-state.png → Negative scenario

success-state.png → Positive scenario

Dropdown logic validation screenshot (optional)
