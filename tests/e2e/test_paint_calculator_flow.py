import re
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope='function')
def setup_teardown(page: Page):
    """Setup and teardown for each test."""
    page.goto('http://localhost:9200')
    yield

def test_home_page_loads(setup_teardown, page: Page):
    """Test that the home page loads correctly."""
    expect(page).to_have_title("Home")
    expect(page.get_by_role("heading", name="Calculating Paint Required")).to_be_visible()
    expect(page.get_by_text("Enter the number of rooms")).to_be_visible()
    expect(page.locator('input[name="rooms"]')).to_be_visible()
    expect(page.locator('input[type="submit"]')).to_be_visible()

def test_room_selection_flow(setup_teardown, page: Page):
    """Test the flow of selecting number of rooms and proceeding to dimensions."""
    page.locator('input[name="rooms"]').fill("2")
    page.locator('input[type="submit"]').click()
    expect(page).to_have_url("http://localhost:9200/dimensions?rooms=2")
    expect(page.get_by_role("heading", name="Calculating Paint Required")).to_be_visible()
    expect(page.get_by_text("1", exact=True).first).to_be_visible()
    expect(page.get_by_text("2", exact=True).first).to_be_visible()
    expect(page.get_by_text("Room Number")).to_be_visible()
    expect(page.get_by_text("Length")).to_be_visible()
    expect(page.get_by_text("Width")).to_be_visible()
    expect(page.get_by_text("Height")).to_be_visible()
    expect(page.get_by_role("columnheader", name="Height")).to_be_visible()
    expect(page.get_by_text("Submit Query")).to_be_visible()

def test_calculation_flow(setup_teardown, page: Page):
    """Test the complete flow from room selection to calculation results."""
    page.goto("http://localhost:9200/dimensions?rooms=1")
    page.locator('input[name="length-0"]').fill("10")
    page.locator('input[name="width-0"]').fill("12")
    page.locator('input[name="height-0"]').fill("8")
    page.locator('input[type="submit"]').click()
    expect(page).to_have_url("http://localhost:9200/results")
    page.get_by_role("button", name="View Results").click()
    expect(page.get_by_text("Paint Calculation Results")).to_be_visible()
    page.wait_for_timeout(6000)
    expect(page.locator(".room-feet").first).to_contain_text("960")
    expect(page.locator(".room-total-gallons").first).to_contain_text("2")

def test_navigation_back_to_home(setup_teardown, page: Page):
    """Test that the Home button works correctly."""
    page.goto("http://localhost:9200/dimensions?rooms=1")
    page.locator('input[name="length-0"]').fill("10")
    page.locator('input[name="width-0"]').fill("12")
    page.locator('input[name="height-0"]').fill("8")
    page.locator('input[type="submit"]').click()
    page.locator('input[value="Home"]').click()
    expect(page).to_have_url(re.compile(r'http://localhost:9200/\??$'))
    expect(page.get_by_role("heading", name="Calculating Paint Required")).to_be_visible()
