from playwright.sync_api import Playwright, sync_playwright
import pandas as pd 


def main():
    with sync_playwright() as p:

        # scrape the data
        browser = p.firefox.launch()
        page = browser.new_page()
        page.goto("https://coinmarketcap.com/")
        page.wait_for_timeout(10000)


        #scrolling down
        for _ in range(7):
            page.mouse.wheel(0,3000)
            page.wait_for_timeout(1000)

        # get the data
        trs_xpath = '''//*[@id="__next"]/div[2]/div[1]/div[2]/div/div[1]/div[4]/table/tbody/tr'''
        trs_list = page.query_selector_all(trs_xpath)


        master_list = []
        for trs in trs_list:

            coin_dict = {}
            tds = trs.query_selector_all('//td')

            coin_dict["id"] = tds[1].inner_text()
            coin_dict["Name"] = tds[2].query_selector("""//p[@class='sc-65e7f566-0 iPbTJf coin-item-name']""").inner_text()
            coin_dict["Symbol"] = tds[2].query_selector("""//p[@class='sc-65e7f566-0 byYAWx coin-item-symbol']""").inner_text()
            coin_dict["Price"] = float(tds[3].inner_text().replace("$","").replace(",",""))
            coin_dict["Market_Cap"] = int(tds[7].inner_text().replace("$","").replace(",",""))
            coin_dict["Volume_24h"] = int(tds[8].query_selector("""//p[@class ="sc-71024e3e-0 bbHOdE font_weight_500"]""").inner_text().replace("$","").replace(",",""))



            master_list.append(coin_dict)


        #tuples
        list_of_tuples = [tuple(dic.values()) for dic in master_list]

        # save the data into dataframe
        df = pd.DataFrame(master_list)
        # save the data into csv
        df.to_csv("crypto.csv", index=False)
        print("Data saved to crypto.csv")

        browser.close()

    


if __name__ == "__main__":

    main()