# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 17:32:15 2021

@author: HP
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
   public static void main(String[] args) {
      System.setProperty("webdriver.chrome.driver", "C:\\Users\\ghs6kor\\Desktop\\Java\\chromedriver.exe");
      WebDriver driver = new ChromeDriver();
      driver.get("https://www.tutorialspoint.com/index.htm");
      // wait of 5 seconds
      driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
      // identify element, enter text
      WebElement m= driver.findElement(By.xpath ("//*[local-name()='svg' and @data-icon='home']/*[localname()='path']"));
      // Action class to move and click element
      Actions a = new Actions(driver);
      a.moveToElement(m).
      click().build().perform();
   }
}