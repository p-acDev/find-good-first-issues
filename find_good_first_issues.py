from bs4 import BeautifulSoup
import requests
import os

def get_html_data(url, status):
    
    try:
        os.mkdir("./_html_data")
    except FileExistsError:
        pass

    if status == "TEST":
    
        # save the output to avoid doing too many queries on the github site during tests =D
        try:
            with open(f"./_html_data/_html_data_{'_'.join(url.split('/')[-2:])}.txt", 'rb') as f:
                html_raw_data = f.read()
                print("[+] File read from already downloaded html")
        except FileNotFoundError:
            req = requests.get(url)
            html_raw_data = req.content
            with open(f"./_html_data/_html_data_{'_'.join(url.split('/')[-2:])}.txt", 'wb') as f:
                # write in case of further use
                f.write(html_raw_data)
            print("[*] File was not available and was downloaded")
    
    elif status == "PROD":
        
        # to ensure we have up to date data
        req = requests.get(url)
        html_raw_data = req.content
        
    return html_raw_data

def find_issues(html_raw_data, status):
    
    soup = BeautifulSoup(html_raw_data, 'html.parser')

    # get the list of all repositories
    repo_list = [elem['href'] for elem in soup.find_all("a", class_=os.environ.get("REPO_CLASS"))]

    # find in each repo check if there is a good-firt issue
    good_first_issues = {}
    for repo in repo_list:
        # create the new url
        url = f"https://github.com{repo}/contribute"
        soup = BeautifulSoup(get_html_data(url, status), 'html.parser')
        # find if there is good firt issue
        extract_issue_num = lambda elem: elem.split('/')[-1] 
        __good_first_issues = [f"https://github.com{repo}/issues/{extract_issue_num(elem['href'])}" for elem in soup.find_all("a", class_=os.environ.get("ISSUES_CLASS"))]
        good_first_issues[repo] = __good_first_issues
        
        
    return good_first_issues

if __name__ == "__main__":
    
    topic = "python"

    url = f"https://github.com/topics/{topic}"

    html_raw_data = get_html_data(url)
    
    good_first_issues = find_issues(html_raw_data)