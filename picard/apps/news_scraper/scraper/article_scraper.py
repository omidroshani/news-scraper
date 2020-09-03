from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from django.conf import settings
from apps.news_scraper.models import Article

def extract_news_content(pk):
    if Article.objects.filter(pk=pk).exists():
        
        article_obj = Article.objects.get(pk=pk)

        try :

            options = Options()
            options.headless = True
            driver = webdriver.Firefox(options=options, executable_path=settings.BROWSER_DRIVER_EXEC_PATH)

            driver.get(f"about:reader?url={article_obj.url}")
            timeout = 10

            WebDriverWait(driver, timeout).until(lambda driver: driver.find_element_by_css_selector('h1.reader-title').get_attribute("innerHTML") != "")
            # title = driver.find_element_by_css_selector("h1.reader-title").get_attribute("innerHTML")
            # author = driver.find_element_by_css_selector('div[class="credits reader-credits"]').get_attribute("innerHTML")
            article = driver.find_element_by_css_selector('div.content').get_attribute("innerHTML")

            soup = BeautifulSoup(article, "html.parser")
            images = [image['src'] for image in soup.select("img")]
            for elem in soup.select("img"):
                elem.extract()

            hyperlinks = [{'title': link.text, 'url': link['href']} for link in soup.find_all('a', href=True)]

            
            article_obj.content = soup.text
            article_obj.images = images
            article_obj.hyperlinks = hyperlinks
            article_obj.status = 'completed'
            article_obj.save()


            return True

        except:

            return None

    else :
        return False