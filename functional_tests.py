from selenium import webdriver

ffoptions = webdriver.FirefoxOptions()
ffoptions.headless = True

browser = webdriver.Firefox(options=ffoptions)
browser.get("http://localhost:8000")

assert "The install worked successfully! Congratulations!" in browser.title