from .libs.crshpiptools import autopipImport

BeautifulSoup = autopipImport("bs4",attr="BeautifulSoup")
fm = autopipImport("matplotlib.font_manager",pipName="matplotlib")
requests = autopipImport("requests")

# Function to scrape nerdfonts website for names.
def _nerdfont_scrape(url=str):
    '''Internal function to scrape nerdfonts.'''
    response = requests.get(url)
    if response.status_code == 200: # valid response
        soup = BeautifulSoup(response.content, 'html.parser')
        font_names = []
        # Assuming font names are in the 'style' attribute of 'a' elements with the class 'font-preview'
        font_elements = soup.find_all('a', class_='font-preview')
        for font_element in font_elements:
            style_attribute = font_element.get('style', '')
            # Extract font name from the 'style' attribute
            start_index = style_attribute.find('url(')
            end_index = style_attribute.find('.svg')
            if start_index != -1 and end_index != -1:
                font_name = style_attribute[start_index + len('url(\'') : end_index + len('.svg')]
                font_name = font_name.replace("/assets/img/previews/","",1)
                font_name = font_name.rstrip(".svg")
                font_names.append(font_name)
        return font_names,None
    else:
        return [],f"Failed to fetch the page. Status code: {response.status_code}"

# Function using matplotlib.font_manager to see if a font is installed on the system
def _font_isinstalled(font_name) -> bool:
    '''Internal function to check if a font is installed.'''
    fonts = [f.name for f in fm.fontManager.ttflist]
    return font_name in fonts

# Function to check if the user has nerdfonts installed
def has_nerd_font(silentDebugOut=False,scrapeUrl="https://www.nerdfonts.com/font-downloads") -> bool:
    '''Function to check if user has any nerd-fonts installed'''
    has = False
    if silentDebugOut == False: print("\033[33mFetching nerdfonts...\033[0m")
    # Fetch
    nerd_fonts,msg = _nerdfont_scrape(scrapeUrl)
    # Check result
    if msg == None:
        if nerd_fonts:
            if silentDebugOut == False: print("\033[34mDone!\033[0m")
        else:
            if silentDebugOut == False: print("\033[31mFetched nerdfonts was empty!\033[0m")
    else:
        if silentDebugOut == False: print(f"\033[31m{msg}\033[0m")
    # Check installed fonts
    if nerd_fonts:
        if silentDebugOut == False: print("\033[33mChecking installed fonts for NF fonts...\033[0m")
        for font_name in nerd_fonts:
            if _font_isinstalled(font_name):
                has = True
    # Result
    if has == True and silentDebugOut == False:
        print("\033[32mAt least one Nerd Font is installed.\033[0m")
    else:
        print("\033[31mNo Nerd Fonts are installed.\033[0m")
    return has