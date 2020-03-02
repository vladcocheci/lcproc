import urllib.request
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import csv
import time
from yelp_uri.encoding import recode_uri
from random import randrange

exceptions_file_name = "exceptions.txt"     # exceptions file
base_link = "http://www.cimec.ro/Monumente/LacaseCult/RO/Documente/ASP/seljud.asp?"
jud = "Cluj"
output_file_name ="LC" + jud + ".csv"

### main function
def main():
    n = get_pages_no(base_link + "nr=1&jud=" + jud)
    pages_link_list = list_generator(base_link, n)
    link_list = LC_scraper(pages_link_list)
    # print(link_list)

    scraper(link_list,output_file_name)

    
# function that returns the number of LC pages
def get_pages_no(base_link):
    try:
        req = urllib.request.Request(
            base_link,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0'
            }
        )
        f = urllib.request.urlopen(req)
        soup = bs(f.read().decode('utf-8'))

        try:
            links = soup.find_all('a', href = re.compile(r'seljud.asp\?nr=')) # a list of links to the next LC pages
            pages_no = len(links)
            return pages_no + 1     # one page is ommited from the count
        except:
            print("error")

    except Exception as e:
        exceptions_file = open(exceptions_file_name,'a')
        exceptions_file.write(str(e) + ": " + url + "\n")
        exceptions_file.close()


# function generating the list of links for all LC pages
def list_generator(base_link, n):
    link_list = []  # a list containing all the links to the LC site pages
    for i in range(1, n+1):
        url = base_link + "nr=" + str(i) + "&jud=" + jud
        link_list.append(url)
        print(url)
    return link_list


# LC scraper function -returns a list of links to all records
def LC_scraper(page_link_list):
    cod_list = []
    for url in page_link_list:
        try:
            req = urllib.request.Request(
                url, 
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0'
                }
            )
            
            f = urllib.request.urlopen(req)
            soup = bs(f.read().decode('utf-8'))
            
            for link in soup.find_all('a'):
                text = link.get_text()
                href = link.get('href')
                if re.match(re.compile(r"[0-9]*\-"),text):
                    cod_list.append("http://www.cimec.ro/Monumente/LacaseCult/RO/Documente/ASP/" + href)
                    print("http://www.cimec.ro/Monumente/LacaseCult/RO/Documente/ASP/" + href)
        
        except Exception as e:
            exceptions_file = open(exceptions_file_name,'a')
            exceptions_file.write(str(e) + ": " + url + "\n")
            exceptions_file.close()

        time.sleep(1)
    return cod_list


# content scraper function -scraps relevant content from each page and saves it to .csv files
def scraper(link_list, output_file_name):
    rec = []    # stores information from all tables
    count = 0

    for url in link_list:
        url = recode_uri(url)   # re-encoding potentially poorly encoded urls
        try:
            req = urllib.request.Request(
                url,
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0'
                }
            )
            f = urllib.request.urlopen(req)
            soup = bs(f.read().decode('utf-8'))

            count += 1
            print("count = " + str(count))
            ### Info
            try:
                denumirea = soup.find("td", string = "Denumirea").find_next_sibling("td").contents[0]
            except:
                denumirea = "lipsa denumire"
            print(denumirea)

            try:
                parohia = soup.find("td", string = "Parohia").find_next_sibling("td").contents[0]
            except:
                parohia = "lipsa parohie"
            print(parohia)

            try:
                datare = soup.find("td", string = "Datare").find_next_sibling("td").contents[0]
            except:
                datare = "lipsa datare"
            print(datare)

            try:
                tip = soup.find("td", string = "Tip").find_next_sibling("td").contents[0]
            except:
                tip = "lipsa tip"
            print(tip)

            try:
                link_harta = soup.find("td", string = "Localizare pe hartă").find_next_sibling("td").contents[0]['href']
            except:
                link_harta = "lipsa localizare"
            print(link_harta)

            try:
                judet = soup.find("td", string = "Judeţ").find_next_sibling("td").contents[0]
            except:
                judet = "lipsa judet"
            print(judet)

            try:
                localitate = soup.find("td", string = "Localitate").find_next_sibling("td").contents[0]
            except:
                localitate = "lipsa localitate"
            print(localitate)

            try:
                comuna = soup.find("td", string = "Comuna").find_next_sibling("td").contents[0]
            except:
                comuna = "lipsa comuna"
            print(comuna)

            try:
                adresa = soup.find("td", string = "Adresa").find_next_sibling("td").contents[0]
            except:
                adresa = "lipsa adresa"
            print(adresa)

            try:
                protopopiat = soup.find("td", string = "Protopopiat").find_next_sibling("td").contents[0]
            except:
                protopopiat = "lipsa protopopiat"
            print(protopopiat)

            try:
                episcopie_arhiepiscopie = soup.find("td", string = "Episcopie/Arhiepiscopie").find_next_sibling("td").contents[0]
            except:
                episcopie_arhiepiscopie = "lipsa episcopie/arhiepiscopie"
            print(episcopie_arhiepiscopie)

            try:
                mitropolie = soup.find("td", string = "Mitropolie").find_next_sibling("td").contents[0]
            except:
                mitropolie = "lipsa mitropolie"
            print(mitropolie)

            try:
                LMI_2004 = soup.find("td", string = "Cod oficial LMI 2004").find_next_sibling("td").contents[0]
            except:
                LMI_2004 = "lipsa cod LMI 2004"
            print(LMI_2004)

            try:
                descriere = soup.find("td", string = "Descriere").find_next_sibling("td").contents[0]
            except:
                descriere = "lipsa descriere"
            print(descriere)

            rec.append([denumirea, parohia, datare, tip, link_harta, judet, localitate, comuna, adresa, protopopiat, episcopie_arhiepiscopie, mitropolie, LMI_2004, descriere])
            
            print("__________________________________________________________________________________________________________")    
        
        except Exception as e:
            exceptions_file = open(exceptions_file_name,'a')
            exceptions_file.write(str(e) + ": " + url + "\n")
            exceptions_file.close()

        time.sleep(randrange(3))
        if count % 10 == 0:
            print("sleeping 5")
            time.sleep(5)

    df = pd.DataFrame(rec, columns = ['denumirea', 'parohia', 'datare', 'tip', 'link_harta', 'judet', 'localitate', 'comuna', 'adresa', 'protopopiat', 'episcopie_arhiepiscopie', 'mitropolie', 'cod_LMI', 'descriere'])
    df.to_csv(output_file_name, index = False)



# calling the main function
if __name__ == "__main__":
    main()