

def refactor():
    template = open("template.py", "r").read()
    code = open("product_scraper.py", "r").read()
    website_list = [{"name": "cupojoes", "url": "https://www.cupojoes.com/pipe-tobacco"},
                        {"name": "smokingpipes", "url": "https://www.smokingpipes.com/tobacco/tinned/"},
                        {"name": "tobaccopipes", "url": "https://www.tobaccopipes.com/pipe-tobacco/"},
                        {"name": "niceashcigars",
                         "url": "https://www.niceashcigars.com/Pipe-Tobacco-s/1888.htm?searching=Y&sort=7&cat=1888&show=300&page=1"},
                        {"name": "ansteads",
                         "url": "https://ansteads.storebyweb.com/s/1000-1/b?ps=64&Dept=07%20Pipe%20Tobacco&pn="},
                        {"name": "pipesandcigars",
                         "url": "https://www.pipesandcigars.com/shop/packaged-tobacco/1800125/?v=5000"},
                        {"name": "4noggins", "url": "https://4noggins.com/tobacco/tinned-tobacco.html"},
                        {"name": "iwanries", "url": "https://www.iwanries.com/Import-Domestic-Tobacco-C14.cfm"},
                        {"name": "pipenook", "url": "https://www.thepipenook.com/store/c14/pipe-tobacco"},
                        {"name": "boswell", "url": "https://boswellpipes.com/brand-tobacco/"},
                        {"name": "windycitycigars",
                         "url": "https://windycitycigars.com/product-category/pipe-tobacco-buy-online/"},
                        {"name": "smokershaven", "url": "https://www.smokershaven.com/sh-tins/"},
                        {"name": "watchcitycigar", "url": "https://watchcitycigar.com/packaged-tobacco/"},
                        {"name": "kingsmoking", "url": "http://www.kingsmokingpipesandcigars.com/pipe-tobacco"},
                        {"name": "countrysquire",
                         "url": "https://www.thecountrysquireonline.com/product-category/tobacco/name-brand-favorites/"},
                        {"name": "cigarsintl", "url": "https://www.cigarsinternational.com/shop/pipe-tobacco/1800049/"},
                        {"name": "cdmcigars", "url": "https://www.cdmcigars.com/product-category/pipe-tobacco"},
                        {"name": "mccranies", "url": "http://www.mccranies.com/store/index.php?main_page=index&cPath=2_35"},
                        {"name": "thebriary", "url": "http://www.thebriary.com/tobacco.html"},
                        {"name": "tophat", "url": "https://tophattobacco.com/pipes-and-pipe-tobacco/pipe-tobacco/"},
                        {"name": "marscigars", "url": "http://www.marscigars.com/pipetobacco.aspx"},
                        {"name": "wilke", "url": "https://www.wilkepipetobacco.com/tincellar"}]

    for section in code.split("if name[n] == "):
        if code.split("if name[n] == ").index(section) != 0:
            data = section[section.find(":")+1:]
            name = section[:section.find(":")]
            url = ""
            for website in website_list:
                if website["name"] == name[1:len(name)-1]:
                    url = '''"'''+website["url"]+'''"'''
            new_file = template.replace("replace_name", name).replace("Data", data).replace("replace_url", url).replace("[n]", "")
            open("product_scrapers/"+name[1:len(name)-1]+".py", "w").write(new_file)
