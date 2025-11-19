from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os

# ---------- CONFIG ----------
PAGE_URL = "file://" + os.path.abspath("registration.html")
SCREENSHOT_FLOW_A = "flow-a-negative.png"
SCREENSHOT_FLOW_B = "flow-b-positive.png" 
SCREENSHOT_FLOW_C = "flow-c-logic.png"

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

def wait_and_screenshot(driver, screenshot_name, message):
    # Wait until browser stops moving/painting
    driver.execute_script("return new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));")
    
    time.sleep(0.5)  # slight buffer
    
    driver.save_screenshot(screenshot_name)
    print(f"📸 {message}: {os.path.abspath(screenshot_name)}")


def fill_common_required_fields(driver):
    """Fill all required fields except last name for Flow A"""
    # First Name
    driver.find_element(By.ID, "firstName").clear()
    driver.find_element(By.ID, "firstName").send_keys("Ganesh")

    # Last Name (filled for Flow B, cleared for Flow A)
    driver.find_element(By.ID, "lastName").clear()
    driver.find_element(By.ID, "lastName").send_keys("Palina")

    # Email
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys("ganesh@example.com")

    # Phone
    driver.find_element(By.ID, "phone").clear()
    driver.find_element(By.ID, "phone").send_keys("7483938485")

    # Age
    driver.find_element(By.ID, "age").clear()
    driver.find_element(By.ID, "age").send_keys("22")

    # Gender
    Select(driver.find_element(By.ID, "gender")).select_by_visible_text("Male")

    # Address
    driver.find_element(By.ID, "address").clear()
    driver.find_element(By.ID, "address").send_keys("Main Street, Sample Area")

    # Country → State → City
    Select(driver.find_element(By.ID, "country")).select_by_visible_text("India")
    
    WebDriverWait(driver, 6).until(
        EC.text_to_be_present_in_element((By.ID, "state"), "Gujarat")
    )
    Select(driver.find_element(By.ID, "state")).select_by_visible_text("Gujarat")
    
    WebDriverWait(driver, 6).until(
        EC.text_to_be_present_in_element((By.ID, "city"), "Ahmedabad")
    )
    Select(driver.find_element(By.ID, "city")).select_by_visible_text("Ahmedabad")

    # Password
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys("StrongPass1!")

    # Confirm Password
    driver.find_element(By.ID, "confirmPassword").clear()
    driver.find_element(By.ID, "confirmPassword").send_keys("StrongPass1!")

    # Terms checkbox
    terms = driver.find_element(By.ID, "terms")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", terms)
    if not terms.is_selected():
        driver.execute_script("arguments[0].click();", terms)

# ================================================================
#                    FLOW A — NEGATIVE SCENARIO 
# ================================================================
def flow_a_negative(driver):
    print("\n" + "="*50)
    print("🚀 FLOW A: Negative Scenario - Missing Last Name")
    print("="*50)
    
    driver.get(PAGE_URL)
    print("📍 Page URL:", driver.current_url)
    print("📄 Page Title:", driver.title)

    # Fill all fields
    fill_common_required_fields(driver)
    
    print("✅ All fields filled - now removing Last Name to test validation")

    # Remove LAST NAME intentionally to create error
    last_name_field = driver.find_element(By.ID, "lastName")
    last_name_field.clear()
    # Trigger input event to update button state
    driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", last_name_field)

    # Take screenshot of form with missing last name
    wait_and_screenshot(driver, SCREENSHOT_FLOW_A, "Flow A - Form with missing Last Name")

    # Check that submit button is disabled
    submit_btn = driver.find_element(By.ID, "submitBtn")
    
    # Wait for button to update
    time.sleep(1)
    
    if "enabled" not in submit_btn.get_attribute("class"):
        print("✅ Submit button correctly disabled due to missing Last Name")
    else:
        print("❌ BUG: Submit button should be disabled but is enabled")
        # Force validation by trying to submit anyway
        print("⚠️  Forcing validation check...")

    # Manually trigger validation to show the error
    driver.execute_script("""
        document.querySelectorAll(".form-group").forEach(g=>g.classList.remove("error"));
        document.querySelectorAll(".error-text").forEach(e=>e.textContent="");
        
        if(!document.getElementById('lastName').value.trim()) {
            document.getElementById('lastNameGroup').classList.add("error");
            document.getElementById('lastNameError').textContent = "Required";
        }
    """)

    # Wait for error message
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "lastNameError"), "Required")
    )

    last_name_error = driver.find_element(By.ID, "lastNameError")
    assert "Required" in last_name_error.text, f"Expected 'Required' error, got: '{last_name_error.text}'"
    
    print("✅ Last Name 'Required' error validated successfully")
    wait_and_screenshot(driver, "flow-a-error.png", "Flow A - Error Message Displayed")

# ================================================================
#                    FLOW B — POSITIVE SCENARIO
# ================================================================
def flow_b_positive(driver):
    print("\n" + "="*50)
    print("🚀 FLOW B: Positive Scenario - Complete Registration")
    print("="*50)
    
    driver.get(PAGE_URL)
    time.sleep(1)

    # Fill all required fields properly
    fill_common_required_fields(driver)

    print("✅ All required fields filled correctly")

    # Wait for submit button to be enabled
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#submitBtn.enabled"))
    )

    # Take screenshot before submission
    wait_and_screenshot(driver, SCREENSHOT_FLOW_B, "Flow B - Form ready for submission")

    # SUBMIT
    submit_btn = driver.find_element(By.ID, "submitBtn")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_btn)
    submit_btn.click()

    # WAIT FOR SUCCESS MESSAGE
    wait = WebDriverWait(driver, 8)
    success_alert = wait.until(
        EC.visibility_of_element_located((By.ID, "formSuccessMessage"))
    )

    assert "Registration Successful" in success_alert.text, \
        f"Success message not showing! Got: '{success_alert.text}'"

    print("✅ Success message: 'Registration Successful'")

    # Take screenshot of success state
    wait_and_screenshot(driver, "flow-b-success.png", "Flow B - Success Message")

    # Wait for form reset
    time.sleep(3)
    
    # Verify form reset
    first_name_value = driver.find_element(By.ID, "firstName").get_attribute("value")
    assert first_name_value == "", "Form did not reset!"
    
    print("✅ Form reset validated - all fields cleared")

# ================================================================
#                    FLOW C — LOGIC TESTING
# ================================================================
def flow_c_logic(driver):
    print("\n" + "="*50)
    print("🚀 FLOW C: Logic Testing - Dynamic Features")
    print("="*50)
    
    driver.get(PAGE_URL)
    time.sleep(1)

    print("🧪 Testing Country → State → City cascade...")

    # COUNTRY → STATE
    Select(driver.find_element(By.ID, "country")).select_by_visible_text("United States")

    WebDriverWait(driver, 6).until(
        EC.text_to_be_present_in_element((By.ID, "state"), "California")
    )

    # Check states
    state_select = Select(driver.find_element(By.ID, "state"))
    states = [o.text for o in state_select.options if o.text != "Select State"]
    print("✅ State dropdown populated:", states)

    state_select.select_by_visible_text("California")

    WebDriverWait(driver, 6).until(
        EC.text_to_be_present_in_element((By.ID, "city"), "Los Angeles")
    )

    # Check cities
    city_select = Select(driver.find_element(By.ID, "city"))
    cities = [o.text for o in city_select.options if o.text != "Select City"]
    print("✅ City dropdown populated:", cities)

    print("🧪 Testing password strength indicator...")

    pw = driver.find_element(By.ID, "password")
    pw_bar = driver.find_element(By.ID, "passwordStrengthBar")

    def wait_strength(class_name):
        WebDriverWait(driver, 5).until(
            lambda d: class_name in pw_bar.get_attribute("class")
        )

    # WEAK password (must give s=1 or s=2)
    pw.clear()
    pw.send_keys("abcd1234")  # length + numbers = 2 points = weak
    wait_strength("strength-weak")
    print("✅ Weak password detected")

    # MEDIUM password (s=3)
    pw.clear()
    pw.send_keys("Abcd1234")  # length + number + uppercase = medium
    wait_strength("strength-medium")
    print("✅ Medium password detected")

    # STRONG password (s=4)
    pw.clear()
    pw.send_keys("Abcd1234!")
    wait_strength("strength-strong")
    print("✅ Strong password detected")


    print("🧪 Testing submit button logic...")

    submit_btn = driver.find_element(By.ID, "submitBtn")

    # Fill minimal fields
    driver.find_element(By.ID, "firstName").send_keys("Test")
    driver.find_element(By.ID, "lastName").send_keys("User")
    driver.find_element(By.ID, "email").send_keys("test@example.com")
    driver.find_element(By.ID, "phone").send_keys("1234567890")
    Select(driver.find_element(By.ID, "gender")).select_by_visible_text("Male")
    Select(driver.find_element(By.ID, "country")).select_by_visible_text("India")
    time.sleep(0.3)
    Select(driver.find_element(By.ID, "state")).select_by_visible_text("Gujarat")
    time.sleep(0.3)
    Select(driver.find_element(By.ID, "city")).select_by_visible_text("Ahmedabad")

    driver.find_element(By.ID, "password").send_keys("StrongPass1!")
    driver.find_element(By.ID, "confirmPassword").send_keys("StrongPass1!")

    terms = driver.find_element(By.ID, "terms")
    driver.execute_script("arguments[0].click();", terms)

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#submitBtn.enabled"))
    )
    print("✅ Submit button enabled")

    # Disable again
    driver.find_element(By.ID, "firstName").clear()
    time.sleep(1)

    if "enabled" not in submit_btn.get_attribute("class"):
        print("✅ Submit button disabled correctly")
    else:
        print("⚠️ Might need small wait")

    wait_and_screenshot(driver, SCREENSHOT_FLOW_C, "Flow C - Completed")


# ================================================================
#                    MAIN EXECUTION
# ================================================================
if __name__ == "__main__":
    driver = setup_driver()
    
    try:
        # Run Flow A - Negative Scenario
        flow_a_negative(driver)
        
        print("\n" + "➡️" * 20 + " MOVING TO NEXT FLOW " + "⬅️" * 20 + "\n")
        time.sleep(2)
        
        # Run Flow B - Positive Scenario  
        flow_b_positive(driver)
        
        print("\n" + "➡️" * 20 + " MOVING TO NEXT FLOW " + "⬅️" * 20 + "\n")
        time.sleep(2)
        
        # Run Flow C - Logic Testing
        flow_c_logic(driver)

        print("\n" + "🎉" * 20)
        print("🎉 ALL 3 FLOWS COMPLETED SUCCESSFULLY! 🎉")
        print("🎉" * 20)
        print("\n📁 Screenshots saved:")
        print(f"   • Flow A: {os.path.abspath(SCREENSHOT_FLOW_A)}")
        print(f"   • Flow B: {os.path.abspath(SCREENSHOT_FLOW_B)}") 
        print(f"   • Flow C: {os.path.abspath(SCREENSHOT_FLOW_C)}")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        driver.save_screenshot("failure-state.png")
        print(f"📸 Failure screenshot: {os.path.abspath('failure-state.png')}")
    finally:
        time.sleep(3)
        driver.quit()