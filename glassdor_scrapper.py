from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_jobs(keyword, num_jobs, verbose, driver_path, sleep_time):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    options = webdriver.ChromeOptions()

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.set_window_size(1120, 1000)

    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=%22"' + keyword + '"&suggestCount=0&suggestChosen=false&clickSource=searchBox'
    driver.get(url)
    jobs = []
    close_popup = True  # Initialize as True to close the sign in pop up window when it appears (it appears just once)

    while len(jobs) < num_jobs:  # If true, should be still looking for new jobs.

        # Let the page load. Change this number based on your internet speed.
        # Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(sleep_time)

        # Going through each job in this page
        # driver.find_element_by_xpath('.//div[@class="hover p-0  css-7ry9k1 exy0tjh5" and @data-test="jlGrid"]')
        job_list = driver.find_element_by_xpath(
            "/html/body/div[3]/div/div/div[1]/div/div[2]/section/article/div[1]/ul")
        job_buttons = [el for el in job_list.find_elements_by_tag_name('li')]
        # job_buttons = driver.find_elements_by_class_name("hover p-0  css-7ry9k1 exy0tjh5")  #jl for Job Listing. These are the buttons we're going to click.
        print(len(job_buttons))

        for job_button in job_buttons:

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break
            job_button.text
            job_button.click()  # You might
            time.sleep(1)
            # Test for the "Sign Up" prompt and get rid of it.
            if close_popup:
                try:
                    element = WebDriverWait(driver, 40).until(EC.visibility_of_element_located(
                        (By.XPATH, "/html/body/div[10]/div/div[2]/span/svg")))
                    driver.find_element_by_xpath("/html/body/div[10]/div/div[2]/span/svg").click()
                    close_popup = False
                except:
                    pass

                time.sleep(10)

                try:
                    driver.find_element_by_xpath("/html/body/div[12]/div/div[2]/span/svg").click()
                    close_popup = False
                except:
                    pass

                time.sleep(10)

                try:
                    driver.find_element_by_xpath('/html/body/div[12]/div/div[2]/span').click()
                    close_popup = False
                except:
                    pass

                try:
                    driver.find_element_by_xpath(".//span[@class='SVGInline modal_closeIcon']").click()
                    close_popup = False
                except:
                    pass


            collected_successfully = False

            while not collected_successfully:

                # print(driver.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/div/div[2]/section/div/div/article/div/div[2]').text)
                # change to css locator?

                try:
                    company_name = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/div/div['
                                                                '2]/section/div/div/article/div/div[1]/div/div/div['
                                                                '1]/div[3]/div[1]/div[1]').text.splitlines()[0]
                    location = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/div/div['
                                                            '2]/section/div/div/article/div/div[1]/div/div/div['
                                                            '1]/div[3]/div[ '
                                                            '1]/div[3]').text
                    job_title = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/div/div['
                                                             '2]/section/div/div/article/div/div[1]/div/div/div['
                                                             '1]/div[3]/div[1]/div[2]').text
                    job_description = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/div/div['
                                                                   '2]/section/div/div/article/div/div[2]').text
                    collected_successfully = True

                except:
                    pass

            try:
                salary_estimate = driver.find_element_by_xpath('.//span[@data-test="detailSalary"]').text
            except NoSuchElementException:
                salary_estimate = -1  # You need to set a "not found value. It's important."

            try:
                rating = driver.find_element_by_xpath('.//span[@data-test="detailRating"]').text
            except NoSuchElementException:
                rating = -1  # You need to set a "not found value. It's important."

            # Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            # Going to the Company tab...
            # clicking on this:
            # <div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                driver.find_element_by_xpath('.//div[@data-item="tab"  and @data-tab-type="overview"]').click()

                try:
                    # <div class="infoEntity">
                    #    <label>Headquarters</label>
                    #    <span class="value">San Francisco, CA</span>
                    # </div>
                    headquarters = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                except NoSuchElementException:
                    headquarters = -1

                try:

                    size = driver.find_element_by_xpath(
                        ".//span[@class='css-i9gxme e1pvx6aw2']").text
                except NoSuchElementException:
                    size = -1
                '//*[@id="EmpBasicInfo"]/div[1]/div/div[2]/span[2]'
                try:

                    founded = driver.find_element_by_xpath(
                        '//*[@id="EmpBasicInfo"]/div[1]/div/div[2]/span[2]').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element_by_xpath(
                        '//*[@id="EmpBasicInfo"]/div[1]/div/div[3]/span[2]').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element_by_xpath(
                        '//*[@id="EmpBasicInfo"]/div[1]/div/div[4]/span[2]').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element_by_xpath(
                        '//*[@id="EmpBasicInfo"]/div[1]/div/div[5]/span[2]').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element_by_xpath(
                        '//*[@id="EmpBasicInfo"]/div[1]/div/div[6]/span[2]').text
                except NoSuchElementException:
                    revenue = -1

                try:
                    competitors = driver.find_element_by_xpath(
                        '//*[@id="EmpBasicInfo"]/div[1]/div/div[7]/span[2]').text
                except NoSuchElementException:
                    competitors = -1

            except NoSuchElementException:  # Rarely, some job postings do not have the "Company" tab.
                print('Failed to find overview tab')
                headquarters = -1
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                competitors = -1

            if verbose:
                print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title": job_title,
                         "Salary Estimate": salary_estimate,
                         "Job Description": job_description,
                         "Rating": rating,
                         "Company Name": company_name,
                         "Location": location,
                         "Headquarters": headquarters,
                         "Size": size,
                         "Founded": founded,
                         "Type of ownership": type_of_ownership,
                         "Industry": industry,
                         "Sector": sector,
                         "Revenue": revenue,
                         "Competitors": competitors})
            # add job to jobs

        # Clicking on the "next page" button
        try:
            driver.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/div/div[2]/section/article/div[2]/div['
                                         '2]/div/div/ul/li[7]/a/span').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs,
                                                                                                         len(jobs)))
            break

    return pd.DataFrame(jobs)  # This line converts the dictionary object into a pandas DataFrame.
