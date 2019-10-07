import os
import xml.etree.ElementTree as etree
import xml
import unicodedata
from recipeClass import Recipe

# set up a path and read all xml files
path = os.getcwd()
xml_folder = os.path.join(os.getcwd(), "xml")

filenames = os.listdir(xml_folder)

print(os.path.join(path, "/xml")) 
print('------------------------------')

noOfFiles = 0
for filename in filenames:
    # rename and change space for dash
    #    os.rename(os.path.join(path, filename), os.path.join(path, filename.replace(' ', '-')).lower())
  
    print(f"file {filename}")
    if filename.endswith('.xml'):
        # print(f"file {filename} ends with .xml")

        # open file xml
        #file_name = 'gingerbread_skeletons_.xml'

        # create html file name based on the xml file
        file_name_output = filename.split('.')
        # print(file_name_output)

        # create new html file
        full_file = os.path.abspath(os.path.join('xml', filename))
        with open(full_file, 'r') as xml_file:
            xml_tree = etree.parse(full_file)
        file_name_output = f"{file_name_output[0]}.html"

        dist = os.path.abspath(os.path.join('dist', file_name_output))
        # creating new file
        f = open(dist, "w", encoding="utf-8")

        # set Recipe Title
        recipe_title = xml_tree.find('title')
        # print(recipe_title.text)
        # recipe = Recipe(recipe_title)
        # f.write(f"<h1>{recipe_title.text}</h1> \n")

        img_name = xml_tree.getroot().get('online_title')
                    
        print('-----------------------------------------------------')
        print(img_name)

        img_name_no_spaces = img_name.replace(',', '')
        img_name_no_spaces = img_name_no_spaces.replace(' ', '-').lower()
        print('-----------------------------------------------------')

        #serving 
        servings = xml_tree.find('serving')
   
        #meta
        f.write('{% set recipe = {')
        meta_str = f'''
                title: "{recipe_title.text}",
                img: "{img_name_no_spaces}.jpg",
                preptime: "{servings.attrib.get("preptimeqty")} {servings.attrib.get("preptimeunits")}",
                preptimeschema: "{servings.attrib.get("preptimeqty")}M",
                prepadd: "{servings.attrib.get("preptimeextra")}",
                cooktime: "{servings.attrib.get("cooktimeqty")} {servings.attrib.get("cooktimeunits")}",
                cooktimeschema: "{servings.attrib.get("cooktimeqty")}M",
                cookadd: "{servings.attrib.get("cooktimeextra")}",
                difficulty: "Easy",
                serves: "{servings.attrib.get("yield")}",
                ctaurl: "",
                today : "01/09/2019",
                description: "",
                keywords: "",
                cuisine : "Australian"
            '''
        f.write(meta_str)
        f.write('} %}')


        # Set up the category

        meta_cat_str = '''

            {% set category = {
                    name: 'Lunchbox Ideas',
                    uri: '/inspireandcreate/lunchboxideas'
            } %}

            '''
        f.write(meta_cat_str)

        #open block fore ings nj

        ings_open_tag = '''
        {% block ingridients %}
        
        '''

        f.write(ings_open_tag)


        # Looping through Ingredients
        ingredients = xml_tree.findall('ingredients')

        for ingredient in ingredients:
            # print(ingredient.tag)

            for inggroup in ingredient:
                #    print(inggroup.tag, inggroup.attrib)

                # infgriedient gorup ? no addidtional titles
                for ing in inggroup.find('ings'):

                    c = ing.attrib.get('qty') + "\n"
                    d = f'<li itemprop="recipeIngredient">{ing.text}</li> \n'
                    f.write(d)
                #  print(f'ingridient:  {ing.attrib.get("qty")} {ing.attrib.get("unit")} {ing.attrib.get("fooditem")} \n' )


        #write close ing tag and open method tag
        ings_close_tag = '''
        {% endblock %}
        {% block method %}
        
        '''
        f.write(ings_close_tag)

        # method
        method = xml_tree.find('preparation')

        for step in method:
            for prepstepgroup in step:
                f.write('<ol>\n')
                for prepstep in prepstepgroup:
                    f.write(f'   <li>{prepstep.text}</li> \n')

                f.write('</ol>\n')




        method_end_tag = '''

            {% endblock %}

            '''

        f.write(method_end_tag)    

         # nutrition
        if  xml_tree.findall('nutrition'):

            nutrition = xml_tree.find('nutrition')

            f.write('''     {% set nutri = false  %}
                            {% block nutriblock %}
            ''')

            nutrition_str = f'''
     
            <div class="nutrition">
                <p><strong>NUTRITION INFORMATION (per {nutrition.attrib.get("per")}) </strong><br>                              
                    <strong><strong>Energy</strong> {nutrition.attrib.get("kJ")}kJ</span>
                    <span><strong>Cals</strong> {nutrition.attrib.get("calories")} </span>
                    <span><strong>Protein </strong> {nutrition.attrib.get("protein_g")}g</span>
                    <span><strong>Fat</strong> {nutrition.attrib.get("fat_g")}g</span>
                    <span><strong>Sat Fat</strong> {nutrition.attrib.get("saturatedfat")}g </span>
                    <span><strong>Sodium</strong> {nutrition.attrib.get("sodium_mg")}mg</span>
                    <span><strong>Carb</strong> {nutrition.attrib.get("carb_g")}g</span>
                    <span><strong>Sugar</strong> {nutrition.attrib.get("sugars_g")}g</span>
                    <span><strong>Dietary Fibre</strong> {nutrition.attrib.get("dietaryfibre_g")}g</span>
            </p> </div>
            \n  '''

            f.write(nutrition_str)
            f.write(' {% endblock %}')


        else: 
            print(f"{noOfFiles} - no nutri!")         

        # save the file
        noOfFiles += 1
        f.close()
