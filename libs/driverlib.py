import undetected_chromedriver as uc

def DriverOptions():
    opts = uc.ChromeOptions()
    opts.page_load_strategy = 'none'
    opts.add_argument("--headless"); 
    # opts.add_argument("--no-sandbox");
    # opts.add_argument("--disable-dev-shm-usage");
    # opts.add_argument("--disable-browser-side-navigation");
    # opts.add_argument("--disable-gpu")

    driver = uc.Chrome(options = opts, version_main = 110)
    return driver