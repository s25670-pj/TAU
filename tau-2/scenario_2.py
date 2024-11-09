import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class YouTubeTest(unittest.TestCase):
    def setUp(self):
        """Konfiguracja przeglądarek przed każdym testem"""
        self.browsers = {
            'firefox': self.setup_firefox(),
            'edge': self.setup_edge(),
            'chrome': self.setup_chrome()
        }
        self.wait_time = 10

    def setup_chrome(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--start-maximized')
        return webdriver.Chrome(options=chrome_options)

    def setup_firefox(self):
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('--start-maximized')
        return webdriver.Firefox(options=firefox_options)

    def setup_edge(self):
        edge_options = webdriver.EdgeOptions()
        edge_options.add_argument('--start-maximized')
        return webdriver.Edge(options=edge_options)

    def tearDown(self):
        for browser in self.browsers.values():
            try:
                browser.quit()
            except Exception as e:
                print(f"Błąd podczas zamykania przeglądarki: {str(e)}")

    def wait_for_element(self, browser, by, value, timeout=None, description=""):
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

    def bypass_consent(self, browser):
        """Funkcja zamykająca pop-up zgody na YouTube"""
        try:
            consent_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button")
                )
            )
            consent_button.click()
            print("Pop-up zgody zamknięty.")
            time.sleep(2)
        except TimeoutException:
            print("Pop-up zgody nie pojawił się lub czas oczekiwania minął.")

    def test_youtube_search_and_navigation(self):
        """Test wyszukiwania i nawigacji na YouTube"""
        test_data = {
            'search_term': 'FORMULA 1',
            'expected_channel': 'FORMULA 1',
        }

        for browser_name, browser in self.browsers.items():
            print(f"\nUruchamiam test w przeglądarce {browser_name}")
            
            try:
                print(f"\nKrok 1: Otwieranie strony głównej YouTube")
                browser.get("https://www.youtube.com")
                time.sleep(2)

                self.bypass_consent(browser)

                self.assertIn("YouTube", browser.title, 
                            "Tytuł strony głównej nie zawiera 'YouTube'")

                print(f"\nKrok 2: Sprawdzanie, czy logo YouTube jest widoczne")
                logo = self.wait_for_element(browser, By.ID, "logo", 5, "logo YouTube")
                self.assertTrue(logo.is_displayed(), "Logo YouTube nie jest widoczne")

                print(f"\nKrok 3: Sprawdzanie, czy strona załadowała się poprawnie")
                self.assertIn("youtube.com", browser.current_url, "Nie załadowano strony YouTube")

                print(f"\nKrok 4: Szukanie pola wyszukiwania")
                search_input = self.wait_for_element(browser, By.NAME, "search_query", 5, "pole wyszukiwania")
                self.assertTrue(search_input.is_enabled(), "Pole wyszukiwania nie jest aktywne")

                print(f"\nKrok 5: Wpisywanie frazy wyszukiwania")
                search_input.clear()
                search_input.send_keys(test_data['search_term'])
                time.sleep(1)
                self.assertEqual(search_input.get_attribute("value"), 
                               test_data['search_term'],
                               "Wpisany tekst nie zgadza się z oczekiwanym")

                try:
                    search_button = browser.find_element(By.CSS_SELECTOR, "button#search-icon-legacy")
                    self.assertTrue(search_button.is_enabled(), "Przycisk wyszukiwania nie jest aktywny")
                    search_button.click()
                except NoSuchElementException:
                    print("Nie znaleziono przycisku wyszukiwania, używam Enter")
                    search_input.send_keys(Keys.RETURN)

                time.sleep(2)

                print(f"\nKrok 6: Weryfikacja wyników wyszukiwania i przechodzenie do kanału FORMULA 1")
                try:
                    video_title = self.wait_for_element(
                        browser,
                        By.CSS_SELECTOR,
                        "a#video-title",
                        5,
                        "pierwszy wynik wyszukiwania"
                    )
                except TimeoutException:
                    print("Nie znaleziono wyników wyszukiwania")
                    raise

                video_title.click()
                time.sleep(2)

                print(f"\nKrok 7: Weryfikacja czy jesteśmy na kanale FORMULA 1")
                channel_name = self.wait_for_element(
                    browser,
                    By.CSS_SELECTOR,
                    "ytd-channel-name#channel-name yt-formatted-string",
                    description="nazwa kanału"
                )
                
                self.assertIn(
                    test_data['expected_channel'],
                    channel_name.text,
                    "Nazwa kanału nie zawiera 'FORMULA 1'"
                )

                print(f"\nKrok 8: Sprawdzanie, czy przycisk wideo jest aktywny")
                video_button = self.wait_for_element(browser, By.CSS_SELECTOR, "button.ytp-play-button", 5, "przycisk wideo")
                self.assertTrue(video_button.is_enabled(), "Przycisk wideo nie jest aktywny")


            except Exception as e:
                print(f"Test w przeglądarce {browser_name} nie powiódł się: {str(e)}")
                continue
            else:
                print(f"Test w przeglądarce {browser_name} zakończony sukcesem")

if __name__ == "__main__":
    unittest.main(verbosity=2)
