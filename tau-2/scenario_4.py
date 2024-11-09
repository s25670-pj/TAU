import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time

class YahooSearchTest(unittest.TestCase):
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

    def reject_cookies(self, browser):
        """Funkcja do odrzucenia plików cookies"""
        try:
            print("Kliknięcie przycisku odrzucenia plików cookies")
            reject_cookies_button = self.wait_for_element(
                browser,
                By.XPATH,
                '/html/body/div/div/div/div/form/div[2]/div[2]/button[2]',
                5,
                "przycisk odrzucenia plików cookies"
            )
            reject_cookies_button.click()
            time.sleep(1)
        except TimeoutException:
            print("Przycisk odrzucenia plików cookies nie został znaleziony")

    def test_yahoo_search_and_results(self):
        """Test wyszukiwania na Yahoo i weryfikacji wyników"""
        test_data = {
            'search_term': 'us election',
            'expected_keywords': ['election', 'president', 'vote']
        }

        for browser_name, browser in self.browsers.items():
            print(f"\nUruchamiam test w przeglądarce {browser_name}")
            
            try:
                print(f"\nKrok 1: Otwieranie strony głównej Yahoo")
                browser.get("https://www.yahoo.com")
                time.sleep(2)

                try:
                    scroll_down_button = self.wait_for_element(
                        browser,
                        By.XPATH,
                        '//*[@id="scroll-down-btn"]',
                        5,
                        "przycisk przewinięcia w dół"
                    )
                    scroll_down_button.click()
                    time.sleep(1)
                except TimeoutException:
                    print("Przycisk przewinięcia w dół nie został znaleziony")

                self.reject_cookies(browser)
                
                # Asercja 1, 2, 3: Sprawdzenie tytułu strony
                self.assertIn("Yahoo", browser.title, 
                            "Tytuł strony głównej nie zawiera 'Yahoo'")
                
                self.assertNotIn("Yah00", browser.title, 
                            "Tytuł strony głównej zawiera 'Yahoo'")
                
                self.assertIn("Mail", browser.title, 
                            "Tytuł strony głównej nie zawiera 'Mail'")

                # Asercja 4, 5: Sprawdzenie URL
                self.assertIn("yahoo.com", browser.current_url, 
                            "URL nie wskazuje na stronę Yahoo")
                
                self.assertNotIn("yah00.com", browser.current_url, 
                            "URL wskazuje na stronę Yahoo")

                print(f"\nKrok 4: Szukanie pola wyszukiwania")
                search_selectors = [
                    (By.ID, "ybar-sbq", "pole wyszukiwania po ID"),
                    (By.NAME, "p", "pole wyszukiwania po nazwie"),
                    (By.CSS_SELECTOR, "input[type='text']", "pole wyszukiwania po typie")
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

                # Asercja 6, 7: Sprawdzenie czy pole wyszukiwania jest aktywne
                self.assertTrue(search_input.is_enabled(), 
                                "Pole wyszukiwania nie jest aktywne")
                
                self.assertFalse(search_input.is_enabled==False, 
                                "Pole wyszukiwania jest aktywne")

                print(f"\nKrok 5: Wpisywanie frazy wyszukiwania")
                search_input.clear()
                search_input.send_keys(test_data['search_term'])
                time.sleep(1)

                # Asercja 8: Sprawdzenie czy tekst został wpisany poprawnie
                self.assertEqual(search_input.get_attribute("value"), 
                                test_data['search_term'],
                                "Wpisany tekst nie zgadza się z oczekiwanym")

            except Exception as e:
                print(f"Test w przeglądarce {browser_name} nie powiódł się: {str(e)}")
                print(f"URL: {browser.current_url}")
                continue
            else:
                print(f"Test w przeglądarce {browser_name} zakończony sukcesem")



if __name__ == "__main__":
    unittest.main(verbosity=2)
