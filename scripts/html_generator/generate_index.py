from slugify import slugify
import pandas as pd


def generate_index(df):
    brands = df.groupby(["brand"])
    main_string = ""
    brand_string = '''
    <div class="list-brand">
        <div class="collapsible" id="<!--PARENT-->" data-num="<!--NUM-->">
            <div style="white-space: nowrap; overflow: hidden;"><!--BRAND--></div>
            <span></span>
            <i class="fa fa-caret-down" style="float: right;"></i>
        </div>
        <div class="content" id="<!--PARENT-->-child">
            <!--BLENDS-->
        </div>
    </div>
    '''
    blend_string = '''
    <div class="content-text" onclick="saveScroll('<!--LINK-->', '<!--PARENT-->')"><!--BLEND--></div>
    '''
    counter = 0
    for brand in sorted(brands, key=lambda i: i[0]):
        counter = counter + 1
        custom_id = slugify(str(counter) + " " + brand[0])
        temp_string = brand_string.replace("<!--BRAND-->", brand[0]) \
            .replace("<!--PARENT-->", custom_id) \
            .replace("<!--NUM-->", str(counter))
        sub_temp_string = ""
        for blend in sorted(brand[1].blend.unique()):
            sub_temp_string = sub_temp_string + blend_string \
                .replace("<!--LINK-->", slugify(brand[0] + " " + blend) + ".html") \
                .replace("<!--BLEND-->", blend) \
                .replace("<!--PARENT-->", custom_id)
        temp_string = temp_string.replace("<!--BLENDS-->", sub_temp_string)
        main_string = main_string + "\n" + temp_string

    return main_string
