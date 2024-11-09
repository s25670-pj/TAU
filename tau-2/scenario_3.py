import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class AmazonTest(unittest.TestCase):
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

    def test_amazon_search_in_suggestions(self):
        """Test wyszukiwania 'logitech mx master 3s' w sugestiach na Amazon.com"""
        test_data = {
            'search_term': 'logitech mx master 3s',
            'expected_title': 'logitech mx master 3s',
        }

        for browser_name, browser in self.browsers.items():
            print(f"\nUruchamiam test w przeglądarce {browser_name}")
            
            try:
                print(f"\nKrok 1: Otwieranie strony głównej Amazon.com")
                browser.get("https://www.amazon.com")
                time.sleep(2)
                
                # Asercja 1: Sprawdzamy tytuł strony głównej
                self.assertIn("Amazon", browser.title, 
                            "Tytuł strony głównej nie zawiera 'Amazon'")

                # Asercja 2: Sprawdzamy, czy URL wskazuje na stronę Amazon.com
                self.assertIn("amazon.com", browser.current_url, "URL nie wskazuje na stronę Amazon.com")

                print(f"\nKrok 2: Szukanie pola wyszukiwania")
                search_selectors = [
                    (By.ID, "twotabsearchtextbox", "pole wyszukiwania po ID"),
                    (By.CSS_SELECTOR, "input#twotabsearchtextbox", "pole wyszukiwania po selektorze CSS")
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

                # Asercja 3: Sprawdzamy, czy pole wyszukiwania jest aktywne
                self.assertTrue(search_input.is_enabled(), "Pole wyszukiwania nie jest aktywne")

                print(f"\nKrok 3: Wpisywanie frazy wyszukiwania")
                search_input.clear()
                search_input.send_keys(test_data['search_term'])
                time.sleep(1)

                # Asercja 4: Sprawdzamy, czy tekst został wpisany poprawnie
                self.assertEqual(search_input.get_attribute("value"), 
                            test_data['search_term'],
                            "Wpisany tekst nie zgadza się z oczekiwanym")

                print(f"\nKrok 4: Sprawdzanie sugestii wyszukiwania")
                suggestion_selector = By.CSS_SELECTOR, "div.s-suggestion"
                suggestions = browser.find_elements(*suggestion_selector)
                self.assertGreater(len(suggestions), 0, "Brak sugestii wyszukiwania")

                # Asercja 5: Sprawdzamy, czy pierwsza sugestia zawiera 'logitech mx master 3s'
                first_suggestion = suggestions[0].text
                self.assertIn(test_data['search_term'], first_suggestion, 
                            "Pierwsza sugestia nie zawiera 'logitech mx master 3s'")

                suggestions[0].click()
                time.sleep(2)

                print(f"\nKrok 5: Kliknięcie w obrazek pierwszego produktu")
                product_image = self.wait_for_element(
                    browser,
                    By.XPATH,
                    "/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[2]/div/div/span/div/div/div/div[1]/div/div[2]",
                    description="obrazek produktu"
                )
                product_image.click()
                time.sleep(2)

                print(f"\nKrok 6: Weryfikacja strony produktu")
                product_title = self.wait_for_element(
                    browser,
                    By.CSS_SELECTOR,
                    "span#productTitle",
                    description="nazwa produktu"
                )

                # Asercja 6: Sprawdzamy, czy tytuł strony produktu zawiera 'logitech mx master 3s'
                normalized_product_title = product_title.text.lower().strip()
                normalized_search_term = test_data['search_term'].lower().strip()

                print(f"Porównanie tytułów:\n  Produkt: '{normalized_product_title}'\n  Wyszukiwanie: '{normalized_search_term}'")

                self.assertIn(
                    normalized_search_term,
                    normalized_product_title,
                    f"Strona produktu nie zawiera '{test_data['search_term']}'"
                )

                # Asercja 7: Sprawdzanie ceny produktu
                try:
                    price_element = self.wait_for_element(
                        browser,
                        By.XPATH,
                        "/html/body/div[1]/div/div[9]/div[3]/div[1]/div[6]/div/div[1]/div/div/div/form/div/div/div/div/div[3]/div/div[1]/div/div/span[1]/span[2]/span[3]",
                        description="cena produktu"
                    )
                    self.assertIsNotNone(price_element.text, "Brak ceny produktu")
                    print(f"Znaleziono cenę produktu: {price_element.text}")
                except TimeoutException:
                    print("Nie znaleziono ceny produktu.")
                    raise TimeoutException("Nie znaleziono ceny produktu na stronie.")

            except Exception as e:
                print(f"Test w przeglądarce {browser_name} nie powiódł się: {str(e)}")
                continue
            else:
                print(f"Test w przeglądarce {browser_name} zakończony sukcesem")


if __name__ == "__main__":
    unittest.main(verbosity=2)
