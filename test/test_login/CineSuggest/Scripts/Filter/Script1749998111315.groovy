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

WebUI.click(findTestObject('Object Repository/Page_Vite  React/a_Movie Shows'))

WebUI.selectOptionByLabel(findTestObject('Object Repository/Page_Vite  React/select_All Years20252024202320222021'), Year, 
    true)

WebUI.selectOptionByValue(findTestObject('Object Repository/Page_Vite  React/select_All GenresActionAdultAdventureAnimat_c8c8df'), 
    Genre, true)

WebUI.selectOptionByValue(findTestObject('Object Repository/Page_Vite  React/select_NoneAscendingDescending'), SortbyRating, 
    true)

WebUI.click(findTestObject('Object Repository/Page_Vite  React/button_Next'))

