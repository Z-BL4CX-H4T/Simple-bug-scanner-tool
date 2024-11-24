import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def print_colored(message, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "end": "\033[0m"
    }
    print(f"{colors[color]}{message}{colors['end']}")

def check_broken_links(url):
    print("\nChecking for Broken Links...")
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print_colored(f"Broken Links On First Page: {url} (Status: {response.status_code})", "red")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)

        for link in links:
            href = link['href']
            if href.startswith('http'):
                link_response = requests.get(href)
                if link_response.status_code != 200:
                    print_colored(f"Valid Links: {href} (Status: {link_response.status_code})", "red")
                else:
                    print_colored(f"Valid Links: {href}", "green")
    except Exception as e:
        print_colored(f"Error While Checking Link: {e}", "red")

def monitor_performance(url):
    print("\nMonitoring Site Performance...")
    try:
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()

        load_time = end_time - start_time
        if response.status_code == 200:
            print_colored(f"Page Loaded In {load_time:.2f} detik (Status: 200)", "green")
        else:
            print_colored(f"Page Failed to Load (Status: {response.status_code})", "red")
    except Exception as e:
        print_colored(f"Errors While Monitoring Performance: {e}", "red")

def check_ui_and_js_errors(url):
    print("\nChecks UI elements and JavaScript errors...")
    try:
        options = Options()
        options.headless = True
        options.add_experimental_option('w3c', True)

        options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

        driver = webdriver.Chrome(service=Service('path_ke_chromedriver/chromedriver'), options=options)

        driver.get(url)

        try:
            login_form = driver.find_element(By.ID, 'login-form')
            if login_form.is_displayed():
                print_colored("From Login Found.", "green")
            else:
                print_colored("Login Form Not Visible.", "red")
        except Exception:
            print_colored("Login Form Not Found.", "red")

        logs = driver.get_log('browser')
        if logs:
            print_colored("\nJavaScript Error Found:", "red")
            for log in logs:
                print_colored(log['message'], "red")
        else:
            print_colored("No JavaScript errors were found.", "green")

        driver.quit()
    except Exception as e:
        print_colored(f"Error while inspecting UI element: {e}", "red")


print("""\033[1;36m
                            -=:      .%:          .%:      .==
                           +#        %+            =@.       **
                          -#:       +@      --      @*       .#=
                          .@        %#      =+      *%.       %:
                          +%=      .**      +*      +*:      -%*
                          :**       *#      +*      #+:      +*-
                           :%*=     +#* -*+:++-+*- =%+     =*@-
                           .==*=    :*#+..@%**@%- +#*-    -*=-:
                             :*+*-   :*#%#%#++*%#%##:   :*+*-
                          :-==+*@@%#*=:@%###=-##%%@-=*##@%*+==-:
                      -+%@%#+++=+*###%@@@%%+=+=%#@@@%%%%#*==++*%@%*-
                    =@%###**=::+*##%@%#%%%@*++*@#%%##@%##*+::-*#**%%@+
                   #@%*=+++*===+**@@@@@#%#%@@@@@*%#@@@@@##+===++++=*#@#.
                  ==*=#%@%%%%#%####*#%@@@%@@%%@@%@@@%**####%#%%%%@%%=*=+
                  .+%@@%####*+**#*+#%@@%*%@@@@@@@*%@@%%*##****###*@@@%+.
                      .:-+*#%@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@@%@#*+-:.
                    :-=**##%@@@@@@%@%%#*#@@@@@@@@###%%@%@@@@@@%%#++==:
                  #@%@#%@@@@%%#+=#%@=@%%%@%****#%%%#@-@#%+=#@%@@@@%#@@@#.
                :%@@@@@%+**=:: :## %+@@@@*+*##*++%@@@*@ *#- ::=*++#@@@@@%-
              .*@@@%=::-*--  :-%-=-@#%@@*%@@@@@@%*%@%#@-=:%=:  --*=::=%@@@#.
             =%@@#- .*#-.:.  =#:.#@-##@%#%@@@@@@@*#@#%-@%.:*+   -.-#*: :#@@@=
           .#@%+:::+*-...-..*%:  ## .##@#*#%@@@#*#@##. +%  .##..-...-**:::=#@%:
          +@#=.:.=%=.:.     :   .%*   -*@%#+=+=#%@#-   =%-   :     .:.-#+.:.-#@*.
         -=:     .              .##      :-====-:      *#:              .     .==
                                 -#=                  -#=
                                  .%-                :%:
                                   :+%-..        ..:#*:
                                      -:          :-.""")
url = input("Enter Website URL: \033[1;37m")

check_broken_links(url)
monitor_performance(url)
check_ui_and_js_errors(url)
