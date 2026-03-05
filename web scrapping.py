import requests
from bs4 import BeautifulSoup
import lxml
import csv
import os

# url_text = "https://www.magicbricks.com/property-for-rent/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Bangalore&category=B&parameter=recent&hideviewed=N&postedSince=11001&filterCount=3&incSrc=Y&fromSrc=homeSrc&sortBy=postRecency"

url_text = "https://www.magicbricks.com/property-for-sale/residential-real-estate?category=S&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=3327-1001012&exc=Y&incSrc=Y&ListingsType=I&showCnt=10"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nobroker.in/"
}



response = requests.get(url_text, headers=header, timeout=10)

if response.status_code == 200:
    print("Request successful")
    html_content = response.text

    soap=BeautifulSoup(html_content, "html.parser")
    # print(soap.prettify())

    properties_for_sale = soap.find_all("div", class_="mb-srp__list")

    file_exists = os.path.isfile("property_data.csv")
    with open("property_data.csv", "a", encoding='utf-8', newline='') as file_csv:
        csv_writer = csv.writer(file_csv)
        # Write header only if file is empty
        if not file_exists or os.stat("property_data.csv").st_size == 0:
            csv_writer.writerow(["bhk", "sqft", "price_of_property", "per_sqrt", "furnishing", "bathroom", "car_parking", "builders_name"])
            
        for property in properties_for_sale:

            # bhk = property.find("h2", class_="mb-srp__card--title").text.strip()
            bhk_tag = property.find("h2", class_="mb-srp__card--title")
            if bhk_tag:
                bhk = bhk_tag.text.strip()
            else:
                bhk = "N/A"

            # sqft = property.find("div", class_="mb-srp__card__summary--value").text.strip()
            sqft = property.find("div", class_="mb-srp__card__summary--value")
            if sqft:
                sqft = sqft.text.strip()
            else:
                sqft = "N/A"

            price_of_property = property.find("div", class_="mb-srp__card__price--amount")
            if price_of_property:
                price_span = price_of_property.find("span", class_="rupees")
                if price_span and price_span.next_sibling:
                    price = price_span.next_sibling.strip()
                else:
                    price = price_of_property.text.replace("₹", "").strip()
            else:
                price = "N/A"

            # per_sqrt = property.find("div", class_="mb-srp__card__price--size").text.strip()
            per_sqrt = property.find("div", class_="mb-srp__card__price--size")
            if per_sqrt:
                per_sqrt = per_sqrt.text.strip()
            else:
                per_sqrt = "N/A"


            furnishing_div = property.find("div", attrs={"data-summary": "furnishing"})
            if furnishing_div:
                furnishing_value = furnishing_div.find("div", class_="mb-srp__card__summary--value")
                if furnishing_value:
                    furnishing = furnishing_value.text.strip()
                else:
                    furnishing = "N/A"
            else:
                furnishing = "N/A"

            bathroom_div = property.find("div", attrs={"data-summary": "bathroom"})
            if bathroom_div:
                bathroom_value = bathroom_div.find("div", class_="mb-srp__card__summary--value")
                if bathroom_value:
                    bathroom = bathroom_value.text.strip()
                else:
                    bathroom = "N/A"
            else:
                bathroom = "N/A"


            car_parking_div = property.find("div", attrs={"data-summary": "parking"})
            if car_parking_div:
                car_parking_value = car_parking_div.find("div", class_="mb-srp__card__summary--value")
                if car_parking_value:
                    car_parking = car_parking_value.text.strip()
                else:
                    car_parking = "N/A"
            else:
                car_parking = "N/A"

            builders_name = property.find("div", class_="mb-srp__card__ads--name")
            if builders_name:
                builders_name = builders_name.text.strip()
            else:
                builders_name = "N/A"


            csv_writer.writerow([bhk, sqft, price, per_sqrt, furnishing, bathroom, car_parking, builders_name])

            # print(bhk)
            # print(sqft)
            # print(price_of_property.text)
            # print(per_sqrt)
            # print(furnishing)
            # print(bathroom)
            # print(car_parking)
            # print(builders_name)


else:
    print("Request failed")

print(response.status_code)