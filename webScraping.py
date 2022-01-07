import pytesseract as pytesseract
import time
import LatLng_Geocode
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from pytesseract import image_to_string
from PIL import Image

'''
GLOBALS
'''
url = "http://preco.anp.gov.br/include/Resumo_Semanal_Index.asp"
driver = webdriver.Chrome()
driver.get(url)
selState = ""
selCombustivel = ""
stateOptCount = 1
stateBypass = 0
stateName = ""
gasType = ""
gasOptCount = 1
gasBypass = 0

'''
FUNCTIONS
'''
def getCaptchaText(location, size):
    pytesseract.tesseract_cmd = 'tesseract'
    img = Image.open('screenshot.png')
    img = img.crop((location['x'], location['y'], location['x']+size['width'], location['y']+size['height']))
    img.save('screenshot.png')
    captcha_text = image_to_string(Image.open('screenshot.png'))
    return captcha_text

def initState():
    global driver
    global stateOptCount

    selState = driver.find_element_by_xpath('//*[@id="divMunicipios"]/select')
    stateOptCount = len(selState.find_elements_by_tag_name('option'))

def changeState():
    global stateBypass
    global stateOptCount
    global gasBypass

    gasBypass = 0
    stateBypass = stateBypass + 1
    stateOptCount = stateOptCount - stateBypass

def selectState():
    global driver
    global stateOptCount
    global stateName

    selState = driver.find_element_by_xpath('//*[@id="divMunicipios"]/select')
    stateNameElement = selState.find_element_by_xpath('//*[@id="divMunicipios"]/select/option[' + str(stateOptCount) + ']')
    stateName = stateNameElement.text
    stateNameElement.click()

def selectGas():
    global driver
    global selCombustivel
    global gasBypass
    global gasOptCount
    global gasType

    selCombustivel = driver.find_element_by_id('selCombustivel')
    gasOptCount = len(selCombustivel.find_elements_by_tag_name('option')) - 1
    gasOptCount = gasOptCount - gasBypass
    gasBypass = gasBypass + 1
    gasTypeElement = selCombustivel.find_element_by_xpath('//*[@id="selCombustivel"]/option[' + str(gasOptCount) + ']')
    gasType = gasTypeElement.text
    gasTypeElement.click()
    return gasOptCount

def start():
    global driver
    global selState
    global selCombustivel
    selState = driver.find_element_by_xpath('//*[@id="divMunicipios"]/select')
    initState()
    selCombustivel = driver.find_element_by_id('selCombustivel')
    bypassCaptchaScreen()


def bypassCaptchaScreen():
    global selState
    global selCombustivel
    global gasBypass
    global stateBypass
    global driver
    driver.find_element_by_id('rdResumo3').click()

    #STOP
    if stateOptCount == 0:
        exit(0)

    #SELECT STATE
    if gasOptCount == 0:
        changeState()
        selectState()
    else:
        selectState()

    #SELECT GAS
    selectGas()

    #CAPTCHA BYPASS
    captchaImage = driver.find_element_by_xpath('//*[@id="frmAberto"]/table[2]/tbody/tr[2]/td[1]/img')
    captchaImageLocation = captchaImage.location
    captchaImageSize = captchaImage.size
    driver.save_screenshot('screenshot.png')
    captchaText = getCaptchaText(captchaImageLocation,captchaImageSize)

    #CAPTCHA FILL FORM
    captchaTextField = driver.find_element_by_xpath('//*[@id="txtValor"]')
    captchaTextField.clear()
    captchaTextField.send_keys(captchaText)
    driver.find_element_by_id('image1').click()

    #TRY IF CAPTCHA BYPASS WORKED, OTHERWISE TRY AGAIN
    try:
        driver.find_element_by_xpath('//*[@id="frmAberto"]/div[1]/table/tbody/tr[4]/td[1]')
        scrapeData()
    except NoSuchElementException:
        time.sleep(2)
        gasBypass = gasBypass - 1
        bypassCaptchaScreen()

def scrapeData():
    global driver

    if len(driver.find_elements_by_xpath('//*[@id="frmAberto"]/div[1]/table/tbody/tr[4]/td[1]/b')) == 0:
        cityTable = driver.find_elements_by_xpath('//*[@id="frmAberto"]/div[1]/table/tbody/tr')
        for cityCounter in range(4,len(cityTable)+1):
            gasStationCount = driver.find_element_by_xpath('//*[@id="frmAberto"]/div[1]/table/tbody/tr[' + str(cityCounter) + ']/td[2]').text
            driver.find_element_by_xpath('//*[@id="frmAberto"]/div[1]/table/tbody/tr[' + str(cityCounter) + ']/td[1]/a').click()
            cityName = driver.find_element_by_xpath('//*[@id="frmAberto"]/input[5]').get_attribute('value')
            cityName = cityName.capitalize()
            for x in range(2,int(gasStationCount)+2):
                gasStationName = driver.find_element_by_xpath('//*[@id="frmAberto"]/span[2]/div[1]/table/tbody/tr['+str(x)+']/td[1]').text
                gasStationAddr = driver.find_element_by_xpath('//*[@id="frmAberto"]/span[2]/div[1]/table/tbody/tr['+str(x)+']/td[2]').text
                gasStationNeigh = driver.find_element_by_xpath('//*[@id="frmAberto"]/span[2]/div[1]/table/tbody/tr['+str(x)+']/td[3]').text
                gasStationBrand = driver.find_element_by_xpath('//*[@id="frmAberto"]/span[2]/div[1]/table/tbody/tr['+str(x)+']/td[4]').text
                gasStationPrice = driver.find_element_by_xpath('//*[@id="frmAberto"]/span[2]/div[1]/table/tbody/tr['+str(x)+']/td[5]').text
                gasStationAddr = gasStationAddr.split(", ")
                dataList = [gasStationName,gasStationBrand,gasStationAddr,gasStationNeigh,cityName,stateName,"Brasil",gasType,gasStationPrice]
                coord = LatLng_Geocode.getLatLng_Geocode(dataList)
                dataList = dataList + coord
                #insertDataDB()
            driver.back()
            time.sleep(2)
    #NEW BYPASS
    driver.get(url)
    bypassCaptchaScreen()


'''
MAIN
'''
start()