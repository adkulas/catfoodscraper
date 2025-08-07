from furl import furl


def parse_brand_links(soup, url):
    parsed = furl(url)
    links = {
        parsed.copy().join(a["href"]).url
        for a in soup.select('a[href^="brand/"]')
        if a.get("href")
    }

    return list(sorted(links))


def parse_brand(soup):
    bold_tag = soup.select_one("div.panel-heading > h2 > b")
    if bold_tag:
        return bold_tag.get_text(" ", strip=True)
    return None


def parse_review_links(soup, url):
    base = furl(url).origin
    buttons = soup.find_all("button", class_="btn-review")
    links = []
    for button in buttons:
        a = button.find_parent("a")
        if a and a.get("href"):
            link = furl(base).join(a["href"]).url
            links.append(link)

    return links

def parse_product_review(soup):
    product_name = soup.select_one('h1').get_text(" ", strip=True)
    
    quick_analysis_h4s = soup.find('h3').find_parent().find_all('h4')
    ingredient_score = len(soup.select('i.ingredient-paws'))
    nutrition_score = len(soup.select('i.nutrition-paws'))
    potential_allergens = quick_analysis_h4s[2].find('span').get_text(" ", strip=True)
    kcal_100g_estimated = quick_analysis_h4s[3].find('span').get_text(" ", strip=True)

    general_conclusion_text = ""
    elem = soup.select_one("div > span")
    if elem:
        general_conclusion_text = elem.get_text(" ", strip=True)

    def get_ingredients_from_panel(selector):
        result = []
        list_items = soup.select(selector)
        for ingredient in list_items:
            is_top_ingredient = 'top' in ingredient.get('class', [])
            result.append({
                'ingredient': ingredient.get_text(" ", strip=True),
                'is_top': is_top_ingredient
            })
        return result

    quality_ingredients_selector = 'div.panel-success ul.ingredients > li'
    quality_ingredients = get_ingredients_from_panel(quality_ingredients_selector)
    
    questionable_ingredients_selector = 'div.panel-danger ul.ingredients > li'
    questionable_ingredients = get_ingredients_from_panel(questionable_ingredients_selector)

    potential_allergens_selector = 'div.panel-warning ul.ingredients > li'
    potential_allergen_ingredients = get_ingredients_from_panel(potential_allergens_selector)
    
    allergen_alert_text = ''
    
    nutritional_summary_list_elem = soup.selector('ul')[-1]



    return {
        'product_name': product_name,
        'ingredient_score': ingredient_score,
        'nutrition_score': nutrition_score,
        'potential_allergens': potential_allergens,
        'energy_density': kcal_100g_estimated,
        'overall_quality': general_conclusion_text,
        'ingredients' : {
            'quality_ingredients': quality_ingredients,
            'questionable_ingredients': questionable_ingredients,
            'potential_allergens': potential_allergen_ingredients
        },
        'allergen_alert_text': '',
        'ingredient_summary_text': '',
    }

    

