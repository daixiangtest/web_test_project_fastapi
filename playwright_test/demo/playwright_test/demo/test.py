from playwright.sync_api import sync_playwright

def test_request(request):

    if request.url == "https://sgp-argo.everonet.com/api/v1/info":
        print("request:",request.headers)

def test_response(response):
    print("response:",response.status_text)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.set_default_timeout(60000)
    page.goto('https://sgp-argo.everonet.com/oauth2/redirect?redirect=https://sgp-argo.everonet.com/workflows/evocloud-regression',referer='https://sgp-argo.everonet.com/oauth2/redirect?redirect=https://sgp-argo.everonet.com/workflows/evocloud-regression')
    # page.on("response", test_response)
    page.on('request', test_request)
    page.locator("#login").fill("rock.dai")
    page.locator("#password").fill('Yun#1026')
    page.locator('#submit-login').click()
    cookies = page.context.cookies()
    print("cookies",cookies)
    for cookie in cookies:
        print(cookie['name'],cookie['value'])
    page.wait_for_timeout(60000)