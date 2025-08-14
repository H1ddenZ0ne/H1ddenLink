from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.utils import platform
import requests
import re
import json
import webbrowser
import threading
import traceback
#Any copyright is prohibited.
#Any copyright is prohibited.
Window.clearcolor = (0, 0, 0, 1)
Window.size = (480, 800)
#Any copyright is prohibited.
#Any copyright is prohibited.
API_KEY = ""
#Any copyright of hiddenlink is prohibited.
TELEGRAM_USERNAME = "HiddenByHidden"
#Any copyright is prohibited.
#Any copyright is prohibited.
def log_error():
    """Logs errors to error_log.txt file"""
    with open("error_log.txt", "a", encoding="utf-8") as f:
        f.write(traceback.format_exc())
        f.write("\n\n")
#Any copyright of hiddenlink is prohibited.
#Any copyright is prohibited.
def offline_check(url: str) -> str:
    """
    Perform offline checks on the URL:
    - HTTPS presence
    - Suspicious TLDs
    - Common phishing keywords
    - IP-based URLs
    - Excessive length
    """
    url = url.lower().strip()
    suspicious_tlds = ['.tk', '.ml', '.ga', '.ru', '.gq', '.xyz']
    phishing_keywords = ['login', 'verify', 'account', 'update', 'free', 'reset']
#Any copyright is prohibited.
    if not url.startswith("https"):
        return "[!] URL does not use HTTPS"
    if any(tld in url for tld in suspicious_tlds):
        return "[!] Suspicious domain suffix detected"
    if any(keyword in url for keyword in phishing_keywords):
        return "[!] Possible phishing keywords found"
    if re.match(r'https?://(?:\d{1,3}\.){3}\d{1,3}', url):
        return "[!] URL is IP-based"
    if len(url) > 100:
        return "[!] URL length is unusually long"
    return "[✓] Offline check passed"
#Any copyright is prohibited.
#Any copyright is prohibited.
def online_check(url: str) -> str:
    """
    Check URL with Google Safe Browsing API online.
    Detect malware, phishing, harmful apps.
    Includes error handling and timeout.
    """
    #Any copyright of hiddenlink is prohibited.
    #Any copyright of hiddenlink is prohibited.
    #Any copyright of hiddenlink is prohibited.
    #Any copyright of hiddenlink is prohibited.
    #Any copyright of hiddenlink is prohibited.
    #Any copyright of hiddenlink is prohibited.
    try:
        endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"
        body = {
            "client": {"clientId": "hiddenlink", "clientVersion": "1.0"},
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "POTENTIALLY_HARMFUL_APPLICATION"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}]
            }
        }
        response = requests.post(endpoint, data=json.dumps(body), timeout=6)
        response.raise_for_status()
        data = response.json()
        if "matches" in data:
            return "[🚫] Warning: URL is dangerous!"
        else:
            return "[✅] Google Safe Browsing: URL is safe"
    except requests.exceptions.Timeout:
        return "[⚠️] Error: Request timed out"
    except requests.exceptions.RequestException as e:
        return f"[⚠️] Network error: {e}"
    except json.JSONDecodeError:
        return "[⚠️] Invalid response from server"
    except Exception:
        log_error()
        return "[⚠️] Unknown error during online check"
#Any copyright is prohibited.
#Any copyright is prohibited.
class SplashScreen(Screen):
    def on_enter(self):
        title = Label(
            text="HIDDENLINK",
            font_size=48,
            color=(0, 1, 0, 1),
            bold=True,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            opacity=1
        )
        #Any copyright of hiddenlink is prohibited.
        #Any copyright of hiddenlink is prohibited.
        self.add_widget(title)
        animation = Animation(opacity=0.2, duration=0.6) + Animation(opacity=1, duration=0.6)
        animation.repeat = True
        animation.start(title)
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'main'), 2.8)
#Any copyright is prohibited.
#Any copyright is prohibited.
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.build_ui()
        self.add_widget(self.layout)
#Any copyright is prohibited.
    def build_ui(self):
        self.url_input = TextInput(
            hint_text="Enter-URL-Example=>https://www.moharam.com/ ",
            multiline=False,
            size_hint=(0.9, 0.08),
            pos_hint={'x': 0.05, 'top': 0.95},
            background_color=(0, 0, 0, 1),
            foreground_color=(0, 1, 0, 1),
            cursor_color=(0, 1, 0, 1),
            halign='center',
            font_size=18,
            padding=[10, 12, 10, 12]
        )
        self.layout.add_widget(self.url_input)
#Any copyright is prohibited.
        self.result_label = Label(
            text='',
            size_hint=(0.95, 0.25),
            pos_hint={'x': 0.025, 'top': 0.65},
            color=(0, 1, 0, 1),
            font_size=16,
            halign='center',
            valign='middle'
        )
        #Any copyright of hiddenlink is prohibited.
        self.result_label.bind(size=self.result_label.setter('text_size'))
        self.layout.add_widget(self.result_label)
#Any copyright is prohibited.
        self.scan_button = Button(
            text="[ SCAN LINK ]",
            size_hint=(0.9, 0.1),
            pos_hint={'x': 0.05, 'top': 0.8},
            background_color=(0.05, 0.6, 0.1, 1),
            color=(0, 1, 0, 1),
            font_size=18,
            bold=True
        )
        self.scan_button.bind(on_press=self.on_scan_press)
        self.layout.add_widget(self.scan_button)
        self.animate_button(self.scan_button)
#Any copyright is prohibited.
        self.telegram_button = Button(
            text="HIDDEN SECURITY",
            size_hint=(0.9, 0.08),
            pos_hint={'x': 0.05, 'y': 0.02},
            background_color=(0.1, 0.1, 0.1, 1),
            color=(0.5, 1, 0.5, 1),
            font_size=14
        )
        self.telegram_button.bind(on_press=lambda _: webbrowser.open(f"https://t.me/{TELEGRAM_USERNAME}"))
        self.layout.add_widget(self.telegram_button)
        self.animate_button(self.telegram_button)
#Any copyright is prohibited.
    def on_scan_press(self, _):
        url = self.url_input.text.strip()
        if not url:
            self.result_label.text = "[!] Please enter a URL"
            return
#Any copyright is prohibited.

        offline_result = offline_check(url)
        self.result_label.text = offline_result
        self.animate_result()

#Any copyright is prohibited.
        if platform != 'android':
            def thread_func():
                try:
                    online_result = online_check(url)
                    Clock.schedule_once(lambda dt: self.append_result(online_result))
                except Exception:
                    log_error()
                    Clock.schedule_once(lambda dt: self.append_result("[⚠️] Unknown error during online check"))
#Any copyright is prohibited.
            threading.Thread(target=thread_func, daemon=True).start()
#Any copyright is prohibited.
    def append_result(self, text):
        self.result_label.text += f"\n{text}"
        self.animate_result()
#Any copyright is prohibited.
    def animate_result(self):
        anim = Animation(color=(0.4, 1, 0.4, 1), duration=0.25) + Animation(color=(0, 1, 0, 1), duration=0.25)
        anim.repeat = 2
        anim.start(self.result_label)
#Any copyright is prohibited.
    def animate_button(self, btn):
        anim = Animation(background_color=(0.1, 1, 0.3, 1), duration=0.6) + Animation(background_color=(0.05, 0.5, 0.05, 1), duration=0.6)
        anim.repeat = True
        anim.start(btn)
#Any copyright of hiddenlink is prohibited.
#Any copyright is prohibited.
class HiddenLinkApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(MainScreen(name="main"))
        return sm
#Any copyright of hiddenlink is prohibited.

if __name__ == "__main__":
    try:
        HiddenLinkApp().run()
    except Exception:
        log_error()
        print("An error occurred. Check error_log.txt for details.")
#Any copyright of hiddenlink is prohibited.
