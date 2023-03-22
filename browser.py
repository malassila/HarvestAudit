import asyncio
import time
import webbrowser
import tkinter.messagebox as messagebox
from playwright.async_api import async_playwright, Error

async def edit_max_qty(sku: str, max_qty: int) -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        try:
            # Navigate to the sellercloud inventory page
            await page.goto(f"https://pcsp.cwa.sellercloud.com/Inventory/Product_Dashboard.aspx?Id={sku}")

            # Wait for the page to load
            # await page.wait_for_selector("ContentPlaceHolder1_txtEmail")
            page.fill("ContentPlaceHolder1_txtEmail", "mlassila@pcsp.com")
            page.fill("ContentPlaceHolder1_txtPwd", "tempPcsp2022!")
            
            await page.click("ContentPlaceHolder1_btnLogin2")
            # Wait for the page to load
            await page.wait_for_selector("#ContentPlaceHolder1_ContentPlaceHolder1_Product_CustomColumns1_INVENTORYHIGHSTOCKNOTICE")

            # Fill the INVENTORYHIGHSTOCKNOTICE field with the given max_qty
            page.fill("#ContentPlaceHolder1_ContentPlaceHolder1_Product_CustomColumns1_INVENTORYHIGHSTOCKNOTICE", str(max_qty))

            # Click the "Update" button
            await page.click("#ContentPlaceHolder1_ContentPlaceHolder1_btnUpdate")

            # Wait for the page to update
            time.sleep(2)

            await browser.close()
        except Error as e:
            print(e)
        finally:
            await browser.close()

def view_on_google(table, value1):
    selected_item = table.selection()
    chassis = value1.cget('text')
    if selected_item:
        item_values = table.item(selected_item, 'values')
        if item_values[0] == 'CASE COMPONENT':
            if item_values[2] == 'FEET':
                messagebox.showerror(title='Weird Choice' , message='You really want to look up "feet" on Google? That\'s a bit odd, don\'t you think?')
                description = 'big feet meme'
                url = f"https://www.google.com/search?q={description}&rlz=1C1ONGR_enUS975US975&sxsrf=AJOqlzXfS0bHTN8aZinRzbsZPd9M4O4h2g:1678991274668&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj-oIf0ieH9AhWRkYkEHfQvC6EQ0pQJegQIJRAE&biw=2400&bih=1321&dpr=0.8"
                webbrowser.open_new_tab(url)
                time.sleep(5)
                description = f"rubber {item_values[2].lower()} for a {chassis.lower()}"
            else:
                description = f"{item_values[2].lower()} for a {chassis.lower().replace('4x hs', '').replace('2x hs', '').replace('1x hs', '')}"
        else:
            description = item_values[2]  # Assuming Description is the third value in item_values
        
        description = description.replace(' ', '+')
                
        url = f"https://www.google.com/search?q={description}&rlz=1C1ONGR_enUS975US975&sxsrf=AJOqlzXfS0bHTN8aZinRzbsZPd9M4O4h2g:1678991274668&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj-oIf0ieH9AhWRkYkEHfQvC6EQ0pQJegQIJRAE&biw=2400&bih=1321&dpr=0.8"
        webbrowser.open_new_tab(url)
    else:
        messagebox.showwarning(title='Warning', message='Please select a row first.')

def view_on_sellercloud(table):
    selected_item = table.selection()
    if selected_item:
        item_values = table.item(selected_item, 'values')
        sku = item_values[1]  # Assuming SKU is the second value in item_values
        sku = sku.replace(' ', '+')
        url = f"https://pcsp.cwa.sellercloud.com/Inventory/Product_Dashboard.aspx?Id={sku}"
        webbrowser.open_new_tab(url)
    else:
        messagebox.showwarning(title='Warning', message='Please select a row first.')

def open_pcsp():
    url = "https://pcserverandparts.com/"
    webbrowser.open_new_tab(url)