import requests
from typing import Dict

def download_input(url: str, filename: str, cookie: Dict[str, str]) -> bool:
    try:
        r = requests.get(url, cookies=cookie)
        with open(filename, "w") as f:
            f.write(r.text)
    except:
        print(f"Something happened")
        return False
    return True
