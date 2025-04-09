# NEEDS the mediawikiAPI


def wikiScrapeCategories(categoryName, resultCount):
    from mediawiki import MediaWiki
    wiki = MediaWiki(url='https://en.wikipedia.org/w/api.php')
    wiki.user_agent = "CompanyHunterWikiAPI/1.0"
    category = wiki.categorymembers(categoryName,results=resultCount, subcategories=False) #ISSUE: need to already know the total number of results, otherwise stops way too early.. set it to a super high number? will that work? idk #categoryName = name of category in url: 'English-only_movement' gets the url https://en.wikipedia.org/wiki/Category:English-only_movement.

    return category
    for thing in category:
        print(thing + '\n')

