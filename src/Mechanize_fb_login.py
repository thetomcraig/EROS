from bs4 import BeautifulSoup
import mechanize
import cookielib
import html2text

def setup(browser):
    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    browser.set_cookiejar(cj)
    
    # Browser options
    browser.set_handle_equiv(True)
    browser.set_handle_gzip(True)
    browser.set_handle_redirect(True)
    browser.set_handle_referer(True)
    browser.set_handle_robots(False)
    
    # User-Agent
    browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.41 Safari/534.7')]

logger = mechanize.Browser()
setup(logger)

logger.open('https://www.facebook.com/')
logger.select_form(nr=0)
logger.form['email'] = 'thetomcraig@icloud.com'
logger.form['pass'] = 'fac3b00k'
logger.submit()

html = logger.open('https://www.facebook.com/?_rdr=p')
soup = BeautifulSoup(html)
#print len(soup.findAll("div", { "class" : "_5pbx userContent" }))

marked = BeautifulSoup(soup, "html5lib")
code_blocks = marked.findAll('code')
print code_blocks












