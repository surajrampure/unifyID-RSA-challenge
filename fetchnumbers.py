'''
fetchnumbers.py
Suraj Rampure, surajr@me.com

Fetches n random numbers from random.org/integers. rand_in_range(...) is called by rsa.py, which generates an RSA key pair using random numbers from the site.

Created for the unifyID technical challenge.
'''
from urllib.request import Request, urlopen

import threading
_LOCK = threading.Lock()

base_url = "https://www.random.org/integers/?num={0}&min={1}&max={2}&col={3}&base={4}&format=plain&rnd=new"

def rand_in_range(lower, upper, num=1):
    link = base_url.format(num, lower, upper, 1, 10)
    request = Request(link)
    request.add_header("User-agent", "surajr@me.com")
    with _LOCK:
        source_code = urlopen(request).read()
    return [int(x) for x in source_code.splitlines()]
