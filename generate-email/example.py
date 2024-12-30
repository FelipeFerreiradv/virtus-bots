import re 
from playwright.sync_api import Page, expect

def test_of_automation(page:Page):
    page.goto("https://accounts.google.com/signup")