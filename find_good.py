from bs4 import BeautifulSoup
import requests

topic = "python"

url = f"https://github.com/topics/{topic}"

status = "TEST"

def get_html_data():

    # save the output to avoid doing too many queries on the github site during tests =D
    try:
        with open(f"_html_data_{url.split('/')[-1]}.txt", 'rb') as f:
            html_raw_data = f.read()
            print("[+] File read from already downloaded html")
    except FileNotFoundError:
        req = requests.get(url)
        html_raw_data = req.content
        with open(f"_html_data_{url.split('/')[-1]}.txt", 'wb') as f:
            # write in case of further use
            f.write(html_raw_data)
        print("[*] File was not available and was downloaded")
        
    return html_raw_data
    
soup = BeautifulSoup(get_html_data(), 'html.parser')

# get the list of all repositories
repo_list = [elem['href'] for elem in soup.find_all("a", class_="text-bold wb-break-word")]

# find in each repo if there is a good-firt issue