from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import re
import pandas as pd
import csv

# jud = "Cluj"
# jud = "Bucureszzti"
jud = "Ilfov"
input_file_name ="LC" + jud + ".csv"
output_file_name ="LC_coord_" + jud + ".csv"

### main function
def main():
    df = pd.read_csv(input_file_name)
    x_field, y_field = [], []
    counter = 1

    for link in df["link_harta"]:
        try:
            coord = get_coordinates(link)
        except:
            coord = "Null : Null"

        xy = coord.split(" : ")
        y = xy[0]
        x = xy[1]
        print("judetul " + jud + " - " + str(counter) + " - " + x + ": " + y)
        x_field.append(x)
        y_field.append(y)

        counter += 1

    df["x_field"] = x_field
    df["y_field"] = y_field
    df.to_csv(output_file_name, index = False)

     
def get_coordinates(link):
    browser = webdriver.Firefox()
    browser.get(link)
    browser.maximize_window()

    elem = browser.find_element_by_id("divHarta")

    actions = ActionChains(browser)
    actions.move_to_element(elem).perform()
    actions.click()

    coordinates = browser.find_element_by_class_name("leaflet-control-mouseposition").text

    browser.quit()
    return coordinates

if __name__ == "__main__":
    main()