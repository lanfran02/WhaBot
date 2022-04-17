from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
from PIL import Image
import time
import sys
import os


class WhatsAppElements:
    """
    The variables in this class may vary along of WhatsApp's updates to the web.
    """
    search_box = (By.XPATH, "//div[@contenteditable='true']") #Chat's search box

    input_mess = (By.XPATH, '//div[@title="Type a message"]') #Text input normal message
 
    chat_name = (By.XPATH, '//*[@id="main"]//span[@dir="auto"]') #Contact name's string

    contact_boxes_unread = (By.XPATH,"//*[contains(@aria-label,'unread message')]/../../../../..") #Unread chats

    contact_boxes_muted = (By.XPATH, "//*[contains(@data-icon,'muted')]/../../../../..") #Muted chats

    contact_boxes_pinned = (By.XPATH, "//*[contains(@data-icon,'pinned')]/../../../../..") #Pinned chats

    confirm_button = (By.XPATH, '//*[@id="app"]/div[1]/span[2]/div[1]/div/div/div/div/div/div[2]/div[2]/div/div') #Common confirm button

    header_contact = (By.XPATH, '//*[@id="main"]//header') #Contact header

    attachments_clip = (By.XPATH,'//span[@data-testid="clip"]') #Attachments button

    settings_menu = (By.XPATH,'//div[@id="side"]//span[@data-testid="menu"]') #Setting dropdown menu

class WhaBot:
    browser = None
    timeout = 10  # The timeout is set for about ten seconds
    def __init__(self, wait=15, reloaded=True, binary_location=None, port=None, stored_session=None, driver_location=None,):
        self.show_status("⚙️  Loading all necessaries configurations...")

        self.reloaded = reloaded
        self.chropt = webdriver.ChromeOptions()
        #self.chropt.headless = True  # Whatsapp doesn't allow it :(
        if binary_location != None:
            self.chropt.binary_location = binary_location
        
        if stored_session != None:
            self.chropt.add_argument(f"user-data-dir={stored_session}") 
        else:
            self.chropt.add_argument(f"user-data-dir={os.getcwd()}/stored_session") 

        if port != None:
            self.chropt.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
        
        if driver_location == None:
            driver_location = os.getcwd() + "/chromedriver"
        self.show_status("⚙️  Launching chromedriver...")

        try:
            self.browser = webdriver.Chrome(executable_path=driver_location, options = self.chropt) # In case driver doesn't exists
        except Exception as e:
            raise RuntimeError(f"We have an error with the driver\n\n{e}")
    
        self.show_status("📞 Loading WhatsApp...")

        if self.browser.current_url == "https://web.whatsapp.com/" and self.reloaded != True:
            pass
        else:
            self.browser.get("https://web.whatsapp.com/")

        try:
            self.browser.maximize_window()
        except Exception:
            pass

        try:
            WebDriverWait(self.browser,wait).until(EC.visibility_of_element_located(WhatsAppElements.search_box)) #wait till search element appears
        except Exception:
            try:
                WebDriverWait(self.browser,5).until(EC.visibility_of_element_located((By.XPATH,'//canvas[@aria-label="Scan me!"]')))
                self.show_status("ℹ️ You are not logged in!")
                input("\n\nScan the code and hit enter!")
            except Exception:
                pass
        try:
            WebDriverWait(self.browser,5).until(EC.visibility_of_element_located(WhatsAppElements.search_box)) #wait till search element appears
        except Exception as e:
            self.CloseDriver()
            raise RuntimeError(f"We had an issue, please try again!\n\n{e}")

        self.show_status("🤖 WhaBot Ready!")
    
    def wait_for_element(self, *args):
        element = locals()
        try:
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((element["args"])))    
            return element["args"]
        except Exception:
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((element["args"][0])))
            return element["args"][0]

    def click_element(self, *args):
        try:
            element = locals()
            self.browser.execute_script("arguments[0].click();", self.browser.find_element(*self.wait_for_element(element["args"])))
            return True

        except Exception:
            return False
        
    def goto_main(self):
        try:
            self.browser.refresh()
            Alert(self.browser).accept()
        except Exception as e:
            print(e)
        WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(WhatsAppElements.search_box))
 
    def GetUnreadChats(self, scrolls=100):
        try:
            if self.reloaded:
                self.goto_main()
            initial = 10
            chats = []
            self.browser.execute_script(f"document.getElementById('pane-side').scrollTop={initial}")
            unreads = self.browser.find_elements(*WhatsAppElements.contact_boxes_unread)
            for unread_contact in unreads:
                parts = unread_contact.text.split("\n")
                chat_name = parts[0]
                last_time = parts[1]
                if chat_name == "TODAY":
                    continue
                elif parts[3] == ": ":
                    last_message = parts[4]
                    amount_unread = parts[5]
                    is_group = True
                else:
                    last_message = parts[2]
                    is_group = False
                    try:
                        amount_unread = parts[3]
                    except Exception:
                        amount_unread = None

                chats.append({"Chat_Name":chat_name, "Last_Message":last_message, "Time":last_time, "Unreads":amount_unread, "is_group": is_group})
            return chats
        except Exception as e:
            print(e)
            raise

    def GetMutedChats(self, scrolls=100):
        try:
            if self.reloaded:
                self.goto_main()
            initial = 10
            chats = []
            for i in range(0, scrolls):
                self.browser.execute_script(f"document.getElementById('pane-side').scrollTop={initial}")
                muted = self.browser.find_elements(*WhatsAppElements.contact_boxes_muted)
                for muted_chat in muted:
                    parts = muted_chat.text.split("\n")
                    chat = parts[0]
                    chats.append(chat)
                initial += 10
            return chats
        except Exception as e:
            print(e)
            raise

    def GetPinnedChats(self):
        try:
            if self.reloaded:
                self.goto_main()
            initial = 10
            chats = []
            self.browser.execute_script(f"document.getElementById('pane-side').scrollTop={initial}")
            pinned = self.browser.find_elements(*WhatsAppElements.contact_boxes_pinned)
            for pinned_chat in pinned:
                parts = pinned_chat.text.split("\n")
                chat = parts[0]
                chats.append(chat)
            return chats
        except Exception as e:
            print(e)
            raise
    
    def GetLastMessagesFrom(self, chat=str):
        messages = list()
        self.go_to_chat(name)
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        for i in soup.find_all("div", class_="message-in"): #Get all the incoming mesages
            message = i.find("span", class_="selectable-text") 
            if message:
                message2 = message.find("span")
                if message2:
                    messages.append(message2.text)
        messages = list(filter(None, messages))
        return messages

    def GetChatName(self):
        name = self.browser.find_element(*WhatsAppElements.chat_name).text
        return name

    def SendMessage(self, chat=False, message=""):
        if chat:
            self.go_to_chat(chat)
        try:
            input_message = self.browser.find_element(*WhatsAppElements.input_mess)
            parts = message.split("\n")
            for part in parts:
                # input_message.send_keys(part)
                self.browser.execute_script(f'''
                    const text = `{part}`;
                    const dataTransfer = new DataTransfer();
                    dataTransfer.setData('text', text);
                    const event = new ClipboardEvent('paste', {{
                      clipboardData: dataTransfer,
                      bubbles: true
                    }});
                    arguments[0].dispatchEvent(event)
                    ''', input_message)
                chain = ActionChains(self.browser)
                chain.key_down(Keys.CONTROL).key_down(Keys.ENTER).key_up(Keys.CONTROL).key_up(Keys.ENTER).perform()
            input_message.send_keys(Keys.ENTER)
            self.WaitMessages()
            return True
        except NoSuchElementException as e:
            print("We couldn't find the input message box!\nMessage not sent!")
            return False
    
    def SendImage(self, chat=str, message="", image=str):
        if chat:
            self.go_to_chat(chat)
        try:
            self.click_element(*WhatsAppElements.attachments_clip)
            self.browser.find_element(By.XPATH,'//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]').send_keys(os.getcwd()+f"/{image}")
            parts = message.split("\n")
            self.wait_for_element(By.XPATH,'//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[2]')
            input_message = self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[2]')
            self.wait_for_element(By.XPATH ,'//div[@class="konvajs-content"]')
            for part in parts:
                self.browser.execute_script(f'''
                    const text = `{part}`;
                    const dataTransfer = new DataTransfer();
                    dataTransfer.setData('text', text);
                    const event = new ClipboardEvent('paste', {{
                      clipboardData: dataTransfer,
                      bubbles: true
                    }});
                    arguments[0].dispatchEvent(event)
                    ''', input_message)
                chain = ActionChains(self.browser)
                chain.key_down(Keys.CONTROL).key_down(Keys.ENTER).key_up(Keys.CONTROL).key_up(Keys.ENTER).perform()
            input_message.send_keys(Keys.ENTER)
            return True

        except NoSuchElementException as e:
            print("We couldn't find the attach image button!\nMessage not sent!")
            return False
    
    def SendDocument(self, chat=str, document=str):
        if chat:
            self.go_to_chat(chat)
        try:
            self.click_element(*WhatsAppElements.attachments_clip)
            try:
                self.browser.find_element(By.XPATH,'//input[@accept="*"]').send_keys(os.getcwd()+f"/{document}")
            except Exception as e:
                print("There was an issue while uploading this photo.")
                print(e)
            self.wait_for_element(By.XPATH,'//span[@data-testid="send"]')
            self.click_element(By.XPATH,'//span[@data-testid="send"]')
            return True

        except NoSuchElementException as e:
            print("We couldn't find the attach document button!\nMessage not sent!")
            return False

    def CommandHandler(self, ctx, command):
        if command in ctx["Last_Message"].lower():
            return True
        else: 
            return False

    def BlockContact(self,chat=str):
        try:
            self.go_to_chat(chat)
            self.browser.find_element(*WhatsAppElements.header_contact).click()
            self.wait_for_element(By.XPATH, '//*[contains(@title, "Block")]')
            self.click_element(By.XPATH, '//*[contains(@title, "Block")]')
            self.click_element(*WhatsAppElements.confirm_button)
            return True
        except NoSuchElementException as e:
            print("This contact can't be blocked\n",e)
            return False

    def UnblockContact(self,chat=str):
        try:
            self.go_to_chat(chat)
            self.click_element(*WhatsAppElements.header_contact)
            self.click_element(By.XPATH, '//*[contains(@title, "Unblock")]')
            self.click_element(*WhatsAppElements.confirm_button)
            return True
        except NoSuchElementException as e:
            print("This contact can't be unblocked")
            return False

    def ExitGroup(self, group_name=str):
        try:
            self.go_to_chat(group_name)
            self.click_element(*WhatsAppElements.header_contact)
            self.click_element(By.XPATH, '//*[contains(@title, "Exit group")]')
            self.click_element(*WhatsAppElements.confirm_button)
            return True
        except NoSuchElementException as e:
            print("You can't exit this group")
            return False

    def ArchiveChat(self, chat=str):
        self.go_to_chat(chat)
        chain = ActionChains(self.browser)
        chain.key_down(Keys.CONTROL).key_down(Keys.ALT).key_down(Keys.SHIFT).send_keys('E').key_up(Keys.CONTROL).key_up(Keys.ALT).key_up(Keys.SHIFT).perform()
        return True

    def PinChat(self, chat=str):
        self.go_to_chat(contact)
        chain = ActionChains(self.browser)
        chain.key_down(Keys.CONTROL).key_down(Keys.ALT).key_down(Keys.SHIFT).send_keys('P').key_up(Keys.CONTROL).key_up(Keys.ALT).key_up(Keys.SHIFT).perform()
        return True

    def MuteChat(self, chat=str, mute_time=str):
        mute_time = mute_time.lower()
        if type(mute_time) != None and mute_time != "8h" and mute_time != "1w" and mute_time != "always":
            raise ValueError("Invalid option selected!\nWe only accept 8h(8 Hours), 1w(1 Week) or always.")
        self.go_to_chat(chat)
        chain = ActionChains(self.browser)
        chain.key_down(Keys.CONTROL).key_down(Keys.ALT).key_down(Keys.SHIFT).send_keys('M').key_up(Keys.CONTROL).key_up(Keys.ALT).key_up(Keys.SHIFT).perform()

        self.wait_for_element(By.XPATH,'//label[contains(@for,"duration")]')
        try:
            if mute_time == "8h":
                self.browser.execute_script("arguments[0].click();", self.browser.find_element(By.XPATH,'//label[@for="duration-8"]'))
            elif mute_time == "1w":
                self.browser.execute_script("arguments[0].click();", self.browser.find_element(By.XPATH,'//label[@for="duration-168"]'))
            else: 
                self.browser.execute_script("arguments[0].click();", self.browser.find_element(By.XPATH, '//label[@for="duration-Infinity"]'))

            self.wait_for_element(By.XPATH, '//*[@id="app"]/div[1]/span[2]/div[1]/div/div/div/div/div/div[3]/div[2]')
            self.browser.execute_script("arguments[0].click();", self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/span[2]/div[1]/div/div/div/div/div/div[3]/div[2]'))
            return True

        except NoSuchElementException:
            print("This user was already on mute, \"remuting\" now...")
            self.mute_current_chat(mute_time)

        except Exception as e:
            raise
            print(e)
            return False

    def UnmuteChat(self, chat=str):
        self.go_to_chat(chat)
        self.browser.find_element(*WhatsAppElements.header_contact).click()
        try:
            self.browser.find_element(By.XPATH, "//*/span[contains(text(),'Mute notifications')]")
            print("This chat isn't muted.")
            return False
        except Exception:
            chain = ActionChains(self.browser)
            chain.key_down(Keys.CONTROL).key_down(Keys.ALT).key_down(Keys.SHIFT).send_keys('M').key_up(Keys.CONTROL).key_up(Keys.ALT).key_up(Keys.SHIFT).perform()
            return True

    def ChangeTheme(self, theme="dark"):
        if type(theme) != None and theme.lower() != "light" and theme.lower() != "dark" :
            raise ValueError("Invalid option selected!\nWe only accept Light or Dark.")
        try:
            self.browser.execute_script("arguments[0].click();", self.browser.find_element(*WhatsAppElements.settings_menu))
            self.click_element(By.XPATH,'//*[@aria-label="Settings"]')
            self.click_element(By.XPATH,'//div[@title="Theme"]')
            if theme == "light":
                self.click_element(By.XPATH, '//*[@name="theme"][@value="light"]')
            else:
                self.click_element(By.XPATH, '//*[@name="theme"][@value="dark"]')
            self.wait_for_element(By.XPATH, '//*[@id="app"]/div[1]/span[2]/div[1]/div/div/div/div/div/div[3]/div')
            self.click_element(By.XPATH, '//*[@id="app"]/div[1]/span[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]')
            self.click_element(By.XPATH, '//*[@data-icon="back"]')
            return True
        except Exception as e:
            print(e)
            raise
            return False

    def go_to_chat(self, chat=None):
        search = self.browser.find_element(*WhatsAppElements.search_box)
        search.send_keys(chat+Keys.ENTER)
        try:
            contact = self.GetChatName()
        except Exception as e:
            contact = "Null"
            pass
        return contact

    def WaitMessages(self):
        input_message = self.browser.find_element(*WhatsAppElements.input_mess)
        input_message.send_keys(Keys.PAGE_UP)
        return True

    def TerminateSession(self,sure=str):
        if sure.lower() == "yes" or sure.lower() == "y":
            self.click_element(*WhatsAppElements.settings_menu)
            self.click_element(By.XPATH, '//div[@aria-label="Log out"]')
            return True
        else:
            return False

    def CloseDriver(self):
        self.browser.quit()

    def show_status(self, message):
        sys.stdout.write("\r                                                      ")
        sys.stdout.flush()
        sys.stdout.write(f"\r{message}")
        sys.stdout.flush()