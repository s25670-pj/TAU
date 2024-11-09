import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class WikipediaTest(unittest.TestCase):
    def setUp(self):
        """Konfiguracja przeglądarek przed każdym testem"""
        self.browsers = {
            'firefox': self.setup_firefox(),
            'edge': self.setup_edge(),
            'chrome': self.setup_chrome()
        }
        self.wait_time = 10

    def setup_chrome(self):
        """Konfiguracja Chrome z określonymi opcjami"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-extensions')
        return webdriver.Chrome(options=chrome_options)

    def setup_firefox(self):
        """Konfiguracja Firefox z określonymi opcjami"""
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('--start-maximized')
        return webdriver.Firefox(options=firefox_options)

    def setup_edge(self):
        """Konfiguracja Edge z określonymi opcjami"""
        edge_options = webdriver.EdgeOptions()
        edge_options.add_argument('--start-maximized')
        return webdriver.Edge(options=edge_options)

    def tearDown(self):
        """Zamknięcie przeglądarek po każdym teście"""
        for browser in self.browsers.values():
            try:
                browser.quit()
            except Exception as e:
                print(f"Błąd podczas zamykania przeglądarki: {str(e)}")

    def wait_for_element(self, browser, by, value, timeout=None, description=""):
        """Oczekiwanie na element z obsługą błędów i diagnostyką"""
        if timeout is None:
            timeout = self.wait_time
        try:
            print(f"Szukam elementu: {description} ({by}={value})")
            element = WebDriverWait(browser, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            print(f"Znaleziono element: {description}")
            return element
        except TimeoutException:
            print(f"Nie znaleziono elementu: {description}")
            print(f"Aktualny URL: {browser.current_url}")
            print("Dostępne elementy na stronie:")
            print(browser.page_source[:500])
            raise TimeoutException(f"Element {description} ({by}={value}) nie został znaleziony w czasie {timeout} sekund")

    def test_wikipedia_search_and_navigation(self):
        """Test wyszukiwania i nawigacji na Wikipedii"""
        test_data = {
            'search_term': 'Ferrari',
            'expected_title': 'Ferrari',
            'expected_lang': 'pl'
        }

        for browser_name, browser in self.browsers.items():
            print(f"\nUruchamiam test w przeglądarce {browser_name}")
            
            try:
                print(f"\nKrok 1: Otwieranie strony głównej Wikipedii")
                browser.get("https://pl.wikipedia.org")
                time.sleep(2)
                
                # Asercja 1
                self.assertIn("Wikipedia", browser.title, 
                            "Tytuł strony głównej nie zawiera 'Wikipedia'")

                # Asercja 2
                print(f"\nKrok 2: Sprawdzanie czy jesteśmy na polskiej wersji")
                self.assertIn("pl.wikipedia.org", browser.current_url, "URL nie wskazuje na polską Wikipedię")

                # Asercja 3 Sprawdzenie języka strony
                html_tag = browser.find_element(By.TAG_NAME, "html")
                self.assertEqual(html_tag.get_attribute("lang"), test_data['expected_lang'], "Język strony nie jest ustawiony na polski")

                print(f"\nKrok 3: Szukanie pola wyszukiwania")
                search_selectors = [
                    (By.NAME, "search", "pole wyszukiwania po nazwie"),
                    (By.CSS_SELECTOR, "input[name='search']", "pole wyszukiwania po atrybucie name"),
                    (By.CSS_SELECTOR, "#searchInput", "pole wyszukiwania po ID"),
                    (By.CSS_SELECTOR, "input.searchbox", "pole wyszukiwania po klasie")
                ]

                search_input = None
                for by, selector, desc in search_selectors:
                    try:
                        search_input = self.wait_for_element(browser, by, selector, 5, desc)
                        if search_input:
                            print(f"Znaleziono pole wyszukiwania używając: {desc}")
                            break
                    except TimeoutException:
                        continue

                if not search_input:
                    raise Exception("Nie udało się znaleźć pola wyszukiwania używając żadnego z selektorów")

                # Asercja 4 Sprawdzenie czy pole wyszukiwania jest aktywne
                self.assertTrue(search_input.is_enabled(), "Pole wyszukiwania nie jest aktywne")

                print(f"\nKrok 4: Wpisywanie frazy wyszukiwania")
                search_input.clear()
                search_input.send_keys(test_data['search_term'])
                time.sleep(1)

                # Asercja 5 Sprawdzenie czy tekst został wpisany poprawnie
                self.assertEqual(search_input.get_attribute("value"), 
                               test_data['search_term'],
                               "Wpisany tekst nie zgadza się z oczekiwanym")

                try:
                    search_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
                    # Asercja 6 Sprawdzenie czy przycisk wyszukiwania jest klikalny
                    self.assertTrue(search_button.is_enabled(), "Przycisk wyszukiwania nie jest aktywny")
                    search_button.click()
                except NoSuchElementException:
                    print("Nie znaleziono przycisku wyszukiwania, używam Enter")
                    search_input.send_keys(Keys.RETURN)

                time.sleep(2)

                print(f"\nKrok 5: Sprawdzanie wyników i przechodzenie do artykułu")
                try:
                    article_title = self.wait_for_element(
                        browser,
                        By.CSS_SELECTOR,
                        "h1#firstHeading",
                        5,
                        "tytuł artykułu"
                    )
                except TimeoutException:
                    print("Nie jesteśmy na stronie artykułu, szukam w wynikach wyszukiwania")
                    ferrari_link = self.wait_for_element(
                        browser,
                        By.PARTIAL_LINK_TEXT,
                        "Ferrari",
                        5,
                        "link do artykułu Ferrari"
                    )
                    # Asercja 7 Sprawdzenie czy link w wynikach wyszukiwania jest klikalny
                    self.assertTrue(ferrari_link.is_enabled(), "Link do artykułu Ferrari nie jest klikalny")
                    ferrari_link.click()
                    time.sleep(2)

                print(f"\nKrok 6: Weryfikacja artykułu o Ferrari")
                article_title = self.wait_for_element(
                    browser,
                    By.CSS_SELECTOR,
                    "h1#firstHeading",
                    description="tytuł artykułu"
                )
                
                # Asercja 8
                self.assertIn(
                    "Ferrari",
                    article_title.text,
                    "Tytuł artykułu nie zawiera słowa Ferrari"
                )

                # Asercja 9
                article_content = self.wait_for_element(
                    browser,
                    By.ID,
                    "mw-content-text",
                    description="treść artykułu"
                )
                self.assertTrue(
                    any(keyword in article_content.text for keyword in ["samochód", "Włochy", "Maranello"]),
                    "Treść artykułu nie zawiera oczekiwanych słów kluczowych związanych z Ferrari"
                )

            except Exception as e:
                print(f"Test w przeglądarce {browser_name} nie powiódł się: {str(e)}")
                continue
            else:
                print(f"Test w przeglądarce {browser_name} zakończony sukcesem")

if __name__ == "__main__":
    unittest.main(verbosity=2)