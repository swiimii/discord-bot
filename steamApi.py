import requests
from bs4 import BeautifulSoup
 

def getGameSaleInfo(appId: str):
    # Write your primary script logic here
    try:
        response = requests.get(f'https://store.steampowered.com/app/{appId}/')
        if( response and response.status_code == 200 ):
            soup = BeautifulSoup(response.text, 'html.parser')

            if( soup.find('div', class_="home_page_content") ):
                print(f"Failed to get game {appId}" )
                return { }
            
            gameName = soup.find('div', class_='apphub_AppName').text
            gameWrapper = soup.find('div', class_='game_area_purchase_game_wrapper' )
            if( not gameWrapper ):
                # game is prerelease
                return {
                    "appId": appId,
                    "name": gameName,
                    "price": 9999
                }
            sale = gameWrapper.find('div', class_='discount_pct')
            price = gameWrapper.find('div', class_='discount_final_price')
            
            if( sale ):
                # print( gameName + " is on sale! " + sale.text + " off, down to " + price.text )
                saleTimeline = gameWrapper.find('p', class_='game_purchase_discount_countdown').get_text()
                print(saleTimeline)
                return {
                    "appId": appId,
                    "sale": sale.text,
                    "saleDetails": saleTimeline,
                    "price": price.text,
                    "name": gameName
                }

            else:
                print( gameName + " is not on sale." )
                return { 
                    "appId": appId,
                    "name": gameName
                }
        else:
            print( f"Failed to get game {appId}" )
            return { }
    except:
        print( f"Failed to get game {appId}" )
        return { }




if __name__ == "__main__":
    print(getGameSaleInfo(3768760)) # 007 First Light
    print(getGameSaleInfo(3768761231230)) # invalid
    print(getGameSaleInfo(2692990)) # DON'T SCREAM TOGETHER
    print(getGameSaleInfo(3065800)) # Marathon