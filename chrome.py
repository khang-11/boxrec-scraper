from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import time

def login(driver: webdriver.chrome.webdriver.WebDriver, user: str, pw: str):
	driver.get("https://boxrec.com/en/login")
	username_box = driver.find_element_by_id("username")
	username_box.send_keys(user)
	password_box = driver.find_element_by_id("password")
	password_box.send_keys(pw)
	password_box.send_keys(Keys.ENTER) 

def scrape_results(driver: webdriver.chrome.webdriver.WebDriver, match_id: int):
	results = []

	driver.get("https://boxrec.com/en/event/" + str(match_id))

	table = driver.find_element_by_css_selector("table.calendarTable")
	for row in table.find_elements_by_css_selector("tbody"):
		personLink = row.find_elements_by_class_name("personLink")
		wins = row.find_elements_by_css_selector(".textWon")
		losses = row.find_elements_by_css_selector(".textLost")
		draws = row.find_elements_by_css_selector(".textDraw")

		if (len(personLink) == 2 & len(wins) == 2):
			boxer1_wins = int(wins[0].text)
			boxer1_losses = int(losses[0].text)
			boxer1_draws = int(draws[0].text)
			boxer1_link = personLink[0].get_attribute('href')
			boxer1_id = int(boxer1_link[boxer1_link.rfind("/")+1:])

			boxer2_wins = int(wins[1].text)
			boxer2_losses = int(losses[1].text)
			boxer2_draws = int(draws[1].text)
			boxer2_link = personLink[1].get_attribute('href')
			boxer2_id = int(boxer2_link[boxer2_link.rfind("/")+1:])

			if (len(row.find_elements_by_css_selector(".boutResult.bgL")) == 1):
				result = -1
			elif (len(row.find_elements_by_css_selector(".boutResult.bgW")) == 1):
				result = 1
			else:
				result = 0

			results.append((boxer1_id, boxer1_wins, boxer1_losses, boxer1_draws, boxer2_id, boxer2_wins, boxer2_losses, boxer2_draws, result))

	return results

def save_results(min: int, max: int):
	driver = webdriver.Chrome()
	errors = 0


	login(driver, "khang11", "misterious1")

	for i in range(min, max + 1):
		if (i % 5 == 0):
			time.sleep(30)

		try:
			results = scrape_results(driver, i)

			with open('results.csv','a') as f:
				writer=csv.writer(f, delimiter=",", lineterminator="\r\n") 
				writer.writerows(results)

			print(str(i))
			
			errors = 0

		except:
			print(str(i) + "NOTWORKING")
			errors += 1
			time.sleep(30)
			if errors > 5:
				time.sleep(300)

		time.sleep(2)

save_results(222, 500)
