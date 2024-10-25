from playwright.sync_api import Page
import pytest

@pytest.mark.skip_browser("chromium")
def test_login_and_add_to_cart(page: Page):

    page.goto('https://www.saucedemo.com')
    page.fill('input[id="user-name"]', 'standard_user')
    page.fill('input[id="password"]', 'secret_sauce')
    page.click('input[id="login-button"]')
    
    assert page.title() == 'Swag Labs'
    
    page.click('button[id="add-to-cart-sauce-labs-backpack"]')
    page.click('button[id="add-to-cart-sauce-labs-bike-light"]')
    
    page.click('a.shopping_cart_link')
    
    cart_items = page.query_selector_all('.inventory_item_name')
    cart_item_names = [item.inner_text() for item in cart_items]
    
    assert 'Sauce Labs Backpack' in cart_item_names
    assert 'Sauce Labs Bike Light' in cart_item_names
    
    page.click('button[id="checkout"]')
    page.click('input[id="continue"]') 
    
    error_message = page.inner_text('h3')
    assert error_message == 'Error: First Name is required'
    
    page.fill('input[id="first-name"]', 'Syed')
    page.fill('input[id="last-name"]', 'Atta')
    page.fill('input[id="postal-code"]', '12345')
    page.click('input[id="continue"]')
    
    assert page.inner_text('span.title') == 'Checkout: Overview'
    
    page.click('button[id="finish"]')
    assert page.inner_text('.complete-header').lower() == 'thank you for your order!'