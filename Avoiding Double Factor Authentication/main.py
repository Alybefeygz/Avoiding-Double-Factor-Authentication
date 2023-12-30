import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import re


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
hareket = ActionChains(driver)
driver.maximize_window()
mailAriDroid = "" #AirDroid uygulamasında kullanılacak mail adresi.
passwordAirDroid = "" #AirDroid uygulamasında kullanılacak şifreniz.
kullaniciAdiIns = "" #Instagram kullanıcı adınız.
passwordIns = "" #Instagram şifreniz.

# senkronizasyon fonksiyonu aranan Web elentler bulunana kadar beklenmesini sağlar.
def senkronizasyon(webElementtip, webElement):

    webElementtip= webElementtip.upper()

    try:
        if webElementtip == "CLASS_NAME":
            WebDriverWait(driver, 30).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, webElement)))
        elif webElementtip == "ID":
            WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.ID, webElement)))
        elif webElementtip == "NAME":
            WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.NAME, webElement)))
        elif webElementtip == "XPATH":
            WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, webElement)))
        elif webElementtip == "CSS_SELECTOR":
            WebDriverWait(driver, 30).until(
                expected_conditions.presence_of_element_located((By.CSS_SELECTOR, webElement)))

    except:
        print("Hata: Web Element Bulunamadı.")

# webSitelerarasigecme fonksiyonu program çalışırken açık olan pencereler arasında geçiş yapmanızı sağlar.
def webSitearasigecme(baslik):
    for sayfa in driver.window_handles:
        driver.switch_to.window(sayfa)
        if baslik in driver.title.lower():
            print(f"Şu Web Siteye Geçilmiştir.: {baslik.upper()}.")
            break

# mesajKutusuYenileme fonksiyonu mesaj kutusu yenileme butonuna basmanızı sağlar.
def mesajKutusuYenile():

    yenileBoxWE = "//button[@type='button' and @class='mod-messageList-refresh btn i-float-right']"
    senkronizasyon("XPATH", yenileBoxWE)
    yenileBox = driver.find_element(By.XPATH, yenileBoxWE)
    yenileBox.click()

#instagramGiris fonksiyonu İnstagram'ı açıp gerekli bilgiler ile giriş yapan kod parçasıdır.
def instagramGiris():

    instagramUrl = "https://www.instagram.com/"
    driver.get(instagramUrl)

    insUsernameBoxWE = "username"  # NAME
    time.sleep(2)
    senkronizasyon("NAME", insUsernameBoxWE)
    insUsernameBox = driver.find_element(By.NAME, insUsernameBoxWE)

    insPasswordBoxWE = "password"  # NAME
    senkronizasyon("NAME", insPasswordBoxWE)
    insPasswordBox = driver.find_element(By.NAME, insPasswordBoxWE)

    insUsernameBox.send_keys(kullaniciAdiIns)
    insPasswordBox.send_keys(passwordIns)
    time.sleep(2)
    insPasswordBox.send_keys(Keys.ENTER)
    driver.switch_to.new_window("tab")

# airDroidGiris fonksiyonu AirDroid'i açıp gerekli bilgiler ile giriş yapan kod parçasıdır.
def airDroidGiris():
    singinMailboxWE = "//input[@class='widget-login-account-input']"  # XPATH
    senkronizasyon("XPATH", singinMailboxWE)
    singinMailbox = driver.find_element(By.XPATH, singinMailboxWE)

    singinPasswordboxWE = "//input[@class='widget-login-pwd-input']"  # XPATH
    singinPasswordbox = driver.find_element(By.XPATH, singinPasswordboxWE)

    singinButtonboxWE = "//button[@class='btn widget-login-btn']"  # XPATH
    singinButtonbox = driver.find_element(By.XPATH, singinButtonboxWE)

    time.sleep(2)
    singinMailbox.send_keys(mailAriDroid)
    time.sleep(2)
    singinPasswordbox.send_keys(passwordAirDroid)
    time.sleep(2)
    singinButtonbox.click()

# fbMesajKutusuBulma fonksiyonu AirDroid üzerinde gözüken mesajlar araasında facebook'u arayan ve bulunca ona tıklayan kod parçasıdır.
def fbMesajKutusuBulma():
    while True:
        sonMesajBoxWE = "//div[@role='listitem']"  # XPATH
        senkronizasyon("XPATH", sonMesajBoxWE)

        try:
            sonMesajBox = driver.find_element(By.XPATH, sonMesajBoxWE)

            destDegeri = sonMesajBox.get_attribute("dest")

            if destDegeri.upper() == "FACEBOOK":
                print("En son mesaj FACEBOOK tarafından alınmıştır.")
                print("3 saniye bekleniyor.")
                time.sleep(3)
                sonMesajBox.click()
                break

            else:
                print("En son mesaj FACEBOOK tarafından alınmamıştır.")
                mesajKutusuYenile()
                time.sleep(1)
                continue

        except:
            print("Hata: Stale Element Reference Exception. Element güncellendi.")
            mesajKutusuYenile()
            time.sleep(1)
            continue

# facebookSonMesaj Facebook tarafından gelen son mesajı sonMesaj isimli string değere döndüren kod parçasıdır.
def facebookSonMesaj():
    facebookMesajBoxWE = "//div[@class='mod-multiChat-smsItemBody']"  # XPATH
    senkronizasyon("XPATH", facebookMesajBoxWE)

    facebookMesajBox = driver.find_elements(By.XPATH, facebookMesajBoxWE)
    sonMesaj = facebookMesajBox[-1].text  # Listenin sonundaki öğeyi seç ve metnini al
    return sonMesaj

# dogrulamaKoduBulma sonMesaj değişkeni içerisinden sadece doğrulama kodunu çeken fonksiyondur.
def dogrulamaKoduBulma(sonMesaj):
    sayi_str = re.search(r'\b\d+\s?\d+\b', sonMesaj).group()
    dogrulamaKodu = int(sayi_str.replace(" ", ""))
    return dogrulamaKodu

# AirDroid açıldığı zaman karşımıza çıkan güncelleme mesajını kapattıran kod parçasıdır.
def guncellemeMesaji():
    while True:
        try:
            time.sleep(2)
            guncellemeMesajboxWE = "//button[@class='btn btn-primary' and text()='Başla']"  # XPATH
            senkronizasyon("XPATH", guncellemeMesajboxWE)
            guncellemeMesajbox = driver.find_element(By.XPATH, guncellemeMesajboxWE)
            guncellemeMesajbox.click()
            print("Güncelleme Mesajı Çıktı ve Kapatıldı.")
            break

        except:
            print("Güncelleme Mesajı Çıkmadı")
            break


# telefonKontrol fonksiyonu telefona bağlanıp bağlanmadığını kontrol etmektedir.
def telefonKontrol():


    telefonKontrolWE = "//div[@class='layout-taskbar-battery-v i-taskbar-battery-v']" #XPATH
    senkronizasyon("XPATH", telefonKontrolWE)
    time.sleep(2)
    telefonKontrol = driver.find_element(By.XPATH, telefonKontrolWE)

    if telefonKontrol.is_enabled() == True:
        print("Telefon AirDroid'e bağlanmıştır.")

    else:
        print("Telefon AirDroid'e bağlanamamıştır. \n"
              "Telefonunuzu kontrol ediniz.")

#sonMesaj içerisinde çekilen dogrulamaKodu değerini instagrama geçip onay kodu kısmına yazan ve instagrama giriş yapan kod parçasıdır.
def onayKoduGirme(dogrulamaKodu):
    time.sleep(1)
    insOnayKoduBox = driver.find_element(By.NAME, 'verificationCode')
    insOnayKoduButton = driver.find_element(By.CSS_SELECTOR, 'button[type="button"]')

    insOnayKoduBox.send_keys(dogrulamaKodu)
    time.sleep(2)
    insOnayKoduButton.click()


# İnstagrama giriş yapılıp yapılmadığını kontrol eden kod parçasıdır.
def instagramGirisKontrol():
    try:
        insWebElemnt = "//span[contains(text(), 'Ana Sayfa')]" #XPATH
        senkronizasyon("XPATH", insWebElemnt)
        print("İnstagrama Giriş Yapılmıştır.")


    except:
        print("İnstagrama Girilemedi. Onay Kodunu Kontrol Et.")

# AirDroid açıldığı zaman karşımıza çıkan uyarı mesajını kapattıran kod parçasıdır.
def uyariMesaji():
    time.sleep(2)
    singinAlertWE = "alert_box_yes_btn"  # ID
    senkronizasyon("ID", singinAlertWE)
    singinAlert = driver.find_element(By.ID, singinAlertWE)
    singinAlert.click()

# mesajKutusuGiris fonksiyonu AirDroid üzerinde mesaj kutusuna basan fonksiyondur.
def mesajKutusuGiris():
    mesajBoxWE = "//div[@class='l' and text()='Mesajlar']"
    senkronizasyon("XPATH", mesajBoxWE)
    time.sleep(2)
    mesajBox = driver.find_element(By.XPATH, mesajBoxWE)
    hareket.click(mesajBox)
    hareket.perform()


instagramGiris()
airDroidurl = "https://web.airdroid.com/"

driver.get(airDroidurl)

uyariMesaji()

airDroidGiris()

guncellemeMesaji()
print("AirDroide Bilgisayar üzerinden girilmiştir.")

#telefonKontrol()

mesajKutusuGiris()

airDroidBaslik = "AIRDROID"
webSitearasigecme(airDroidBaslik)

fbMesajKutusuBulma()

sonMesaj = facebookSonMesaj()

dogrulamaKodu = dogrulamaKoduBulma(sonMesaj)

print(f"Facebook tarafından gelen doğrulama kodu: {dogrulamaKodu}")

time.sleep(3)

instagramBaslik = "instagram"
webSitearasigecme(instagramBaslik)

onayKoduGirme(dogrulamaKodu)

instagramGirisKontrol()

time.sleep(1000000)
