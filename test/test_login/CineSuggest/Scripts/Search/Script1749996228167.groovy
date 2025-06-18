import static com.kms.katalon.core.checkpoint.CheckpointFactory.findCheckpoint
import static com.kms.katalon.core.testcase.TestCaseFactory.findTestCase
import static com.kms.katalon.core.testdata.TestDataFactory.findTestData
import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import static com.kms.katalon.core.testobject.ObjectRepository.findWindowsObject
import com.kms.katalon.core.checkpoint.Checkpoint as Checkpoint
import com.kms.katalon.core.cucumber.keyword.CucumberBuiltinKeywords as CucumberKW
import com.kms.katalon.core.mobile.keyword.MobileBuiltInKeywords as Mobile
import com.kms.katalon.core.model.FailureHandling as FailureHandling
import com.kms.katalon.core.testcase.TestCase as TestCase
import com.kms.katalon.core.testdata.TestData as TestData
import com.kms.katalon.core.testng.keyword.TestNGBuiltinKeywords as TestNGKW
import com.kms.katalon.core.testobject.TestObject as TestObject
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.kms.katalon.core.windows.keyword.WindowsBuiltinKeywords as Windows
import internal.GlobalVariable as GlobalVariable
import org.openqa.selenium.Keys as Keys

WebUI.openBrowser('')

WebUI.navigateToUrl('http://localhost:5174/')

WebUI.click(findTestObject('Object Repository/Page_Vite  React/button_Sign In'))

WebUI.setText(findTestObject('Object Repository/Page_Vite  React/input_Username or Email_username'), 'toppro')

WebUI.setEncryptedText(findTestObject('Object Repository/Page_Vite  React/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.sendKeys(findTestObject('Object Repository/Page_Vite  React/input_Password_password'), Keys.chord(Keys.ENTER))

WebUI.click(findTestObject('Object Repository/Page_Vite  React/input_Theater Movies_bg-transparent px-4 py_f85763'))

WebUI.setText(findTestObject('Object Repository/Page_Vite  React/input_Theater Movies_bg-transparent px-4 py_f85763_1_2_3_4_5_6_7_8_9_10'), 
    input_search)

WebUI.sendKeys(findTestObject('Object Repository/Page_Vite  React/input_Theater Movies_bg-transparent px-4 py_f85763_1_2_3_4_5_6_7_8_9_10'), 
    Keys.chord(Keys.ENTER))

WebUI.click(findTestObject('Object Repository/Page_Vite  React/img_Search Results_w-full h-full object-cover'))

