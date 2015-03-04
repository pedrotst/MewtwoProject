import os
from lxml import html

from bs4 import BeautifulSoup
import requests

from pokemon import *
from database import PokemonManager
from pkmutils import PokeHeight, PokeWeight


def run_test(xi=1, xf=721):
    for i in range(xi, xf):
        run(i)


def run(i):
    if i < 10:
        file = os.path.join('Pages', 'page00' + str(i) +'.html')
    elif i < 100:
        file = os.path.join('Pages', 'page0'+str(i) +'.html')
    else:
        file = os.path.join('Pages', 'page0'+ str(i) +'.html')

    c = ImportSerebii()
    # c.download_html(i)
    c.get_local_html(file)
    # print(i)
    # c.donwload_mega_imgs()
    c.get_mega_data()
    # c.parse_serebii()
    # poke = Pokemon(c.get_poke())
    # poke.create_pokemon_evo_chain_database()


# poke.createAbilityDatabase()
# poke.createPokemonAbilityDatabase()
# poke.createAttacksDatabase()
#    poke.createPokemonAttacksDatabase()
#    poke.createPokemonItemsDatabase()
#    poke.createPokemonDexNavItemsDatabase()
#    poke.createPokemonEVWorthDatabase()
#    poke.createPokemonDatabase()


class ImportSerebii:

    def __init__(self):
        """
        Initializes the basic variables
        :return:
        :rtype:
        """
        self.__poke = {}
        self.__serebiiUrl = 'http://serebii.net'
        self.__urlStart = 'http://serebii.net/pokedex-xy/'
        self.__urlEnd = '.shtml'
        self.__html = ''
        self.__soup = ''
        #please take this / out and refactor the code to use os.path.join
        #that is multiplatform
        self.__imgDir = 'PokeData/'

    # --------------------------------------------------------------------------------
    # Print Pokémon data
    def __str__(self):
        p = self.__poke
        print(p['Name'])
        print(p['No'])
        print(p['Gender'])
        print(p['Types'])
        print(p['Classification'])
        print(p['Height'])
        print(p['Weight'])
        print(p['Capture Rate'])
        print(p['Base Egg Steps'])
        print(p['Abilities'])
        print(p['Experience Growth'])
        print(p['Base Happiness'])
        print(p['Effort Values Earned'])
        print(p['Eligible for Sky Battle?'])
        print(p['Weaknesses'])
        print(p['Wild Hold Item'])
        print(p['Egg Groups'])
        print(p['Evo Chain'])
        # Continuar
        print(p['Location'])
        print(p['Flavour Text'])
        # Attacks e Stats
        return ''

    # --------------------------------------------------------------------------------
    # Reference to Pokémon Data
    def get_poke(self):
        return self.__poke

    # --------------------------------------------------------------------------------
    # Download HTLM from Serebii.net
    def download_html(self, i):
        if i < 10:
            url = self.__urlStart + '00' + str(i) + self.__urlEnd
        elif i < 100:
            url = self.__urlStart + '0' + str(i) + self.__urlEnd
        else:
            url = self.__urlStart + str(i) + self.__urlEnd
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception('Download failed')
        self.__html = r.text.encode('utf-8')

    def get_local_html(self, file):
        with open(file, mode='r', encoding='latin1') as f:
            for line in f:
                self.__html += line + '\n'

                # --------------------------------------------------------------------------------

    # Parsing the HTML provided by download_html
    def parse_serebii(self):
        soup = BeautifulSoup(self.__html)
        self.__is_mega(soup)
        self.__get_basic_info(soup)
        self.__get_picture(soup)
        self.__get_battle_info(soup)
        self.__get_weaknesses(soup)
        self.__get_item_egg_group(soup)
        self.__get_evo_chain(soup)
        self.__get_location_and_flavour_text(soup)
        self.__get_attacks(soup)
        self.__get_stats(soup)

    def __is_mega(self, soup):
        if soup.find('a', {'name': 'mega'}) is not None:
            self.__hasMega = 1
        else:
            self.__hasMega = 0

    # --------------------------------------------------------------------------------

    # Get Pokemon basic info and save in dictionary
    def __get_basic_info(self, soup):
        # Parse to first line
        info = soup.find("td", {"class": "fooinfo"}).findNextSibling()

        info = self.__get_name(info)

        info = self.__get_num(info)

        info = self.__get_gender(info)

        info = self.__get_type(info)

        # Parse to second line
        name = info.findParent().findNextSibling()
        info = name.findNextSibling()
        names = name.findAll('td')
        infos = info.findAll('td')
        # Retrieve rest of the information
        for name, info in zip(names, infos):
            self.__poke[name.get_text()] = [info.get_text()]

        # --------------------------------------------------------------------------------

    def __get_picture(self, soup):
        # Parsing to find image link
        # info = soup.find("td", {"class": "fooinfo"})
        name = soup.find("td", {"class": "fooevo"})

        # Find all images that represent the Pokemon
        # infos = info.findAll("img")

        # Look non-shiny one
        # info = infos[0]

        # Create Image URL
        # imageUrl = self.__serebiiUrl + info['src']

        # Download Image
        #         self.__download_image(imageUrl,self.__poke['Name'],self.__poke['Name'])

        # Insert path to Image in the dictionary
        self.__poke[name.text] = self.__imgDir + self.__poke['Name'] + '/' + self.__poke['Name'] + '.png'

        # Get Shiny
        # info = infos[1]

        # Create Shiny Image URL
        # imageUrl = self.__serebiiUrl + info['src']

        # Download Shiny Image
        #         self.__download_image(imageUrl,self.__poke['Name'],self.__poke['Name']+'-Shiny')

        # Insert path to Image in the dictionary
        self.__poke[name.text + '-Shiny'] = self.__imgDir + self.__poke['Name'] + '/' + self.__poke[
            'Name'] + '-Shiny.png'

    # --------------------------------------------------------------------------------
    def __get_battle_info(self, soup):
        info = soup.find('a', {"name": "general"}).findNextSibling().findNextSibling()

        info = self.__get_abilities(info)

        name = info.findNextSibling()
        info = name.findNextSibling()
        names = name.findAll('td')
        infos = info.findAll('td')
        # Retrieve rest of the information
        for name, info in zip(names, infos):
            self.__poke[name.get_text()] = [info.get_text()]

            # --------------------------------------------------------------------------------

    # Retrieve name and return parsing reference
    def __get_name(self, info):
        # Insert Pokemon name into dictionary
        self.__poke['Name'] = info.string

        #  Parsing reference
        return info

    # --------------------------------------------------------------------------------
    # Retrieve num and return parsing reference
    def __get_num(self, info):
        # Parsing to find Pokemon numbers
        info = info.findNextSibling().findNextSibling()
        trs = info.findAll('tr')

        # Dictionary for the pokedex num
        numPoke = {}

        # In each collum search for region and num
        for tr in trs:
            region = tr.td.findNext()
            num = region.findNext()
            numPoke[region.string] = num.string
        self.__poke['No'] = numPoke

        #  Parsing reference
        return info

    # --------------------------------------------------------------------------------
    # Retrieve num and return parsing reference
    def __get_gender(self, info):

        # Parsing to find Gender Ratio
        info = info.findNextSibling()
        tr = info.find('tr')

        try:
            # Dictionary for the gender
            genders = {}

            #  Get Male rate
            gender = tr.td.findNext()
            ratio = gender.findNext()
            genders['Male'] = ratio.string

            # Parse to female ratio
            tr = tr.findNextSibling()

            # Get Female Ratio
            gender = tr.td.findNext()
            ratio = gender.findNext()
            genders['Female'] = ratio.string

            self.__poke['Gender'] = genders
        except AttributeError:
            self.__poke['Gender'] = 'Genderless'
        #  Parsing reference
        return info

    # --------------------------------------------------------------------------------
    # Get pokemon type and return parsing reference
    def __get_type(self, info):
        info = info.findNextSibling()
        As = info.findAll('a')
        types = []
        for a in As:
            types.append(a['href'][12:-6].capitalize())

        self.__poke['Types'] = types

        return info

    # --------------------------------------------------------------------------------
    # Download an image with URL url and save it in imgDir/name/name.png     
    def __download_image(self, url, fld, name):
        # Request URL
        r = requests.get(url)

        # Check status
        if r.status_code == 200:
            #!after refactor drop the [:-1]
            folder = os.path.join(self.__imgDir[:-1], fld)

            # Check folder existance
            self.__ensure_dir(folder)

            # Define image location
            imgPath = os.path.join(folder, name + '.png')

            # Save Image in folder
            with open(imgPath, 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)

    # --------------------------------------------------------------------------------
    # Download pokemon alternative forms images
    def __download_poke_forms(self):
        fileTree = html.fromstring(self.__html)
        orig_name = fileTree.xpath('///table[@class = "dextab"]/tr/td[1]/table/tr/td[2]/font/b/text()')
        img_name_list = fileTree.xpath('//table[@class = "dextable"]/tr[./td/text() = "Alternate Forms"]/following-sibling::tr/td/table/tr[2]/td[@class = "pkmn"]/img/@title')
        img_path_list = fileTree.xpath('//table[@class = "dextable"]/tr[./td/text() = "Alternate Forms"]/following-sibling::tr/td/table/tr[2]/td[@class = "pkmn"]/img/@src')
        how_to = fileTree.xpath('//table[@class = "dextable"]/tr[./td/text() = "Alternate Forms"]/following-sibling::tr/td/table[2]/tr/td//text()')

        # print(list(zip(img_name_list, img_path_list)))
        # print(how_to)
        # print(len(orig_name), len('pikachu'), ''.join(list(str(orig_name)[11:-2])))

        # name comes in a funky way, this was the easiest way to bipass it
        orig_name = ''.join(list(str(orig_name)[11:-2]))

        if len(img_name_list) > 0:
            for name, url in zip(img_name_list,img_path_list):
                self.__download_image(self.__serebiiUrl+url, os.path.join(orig_name, "Pokemon Forms"), name)

            with open(os.path.join(self.__imgDir[:-1], orig_name, "Pokemon Forms", "How-to.txt"), 'w') as f:
                for howto in how_to:
                    f.write(howto)

    def donwload_mega_imgs(self):
        fileTree = html.fromstring(self.__html)
        orig_name = fileTree.xpath('///table[@class = "dextab"]/tr/td[1]/table/tr/td[2]/font/b/text()')
        mega_name = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/tr[3]/td[2]/text()")
        image_path = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/tr[3]/td[1]/table/tr/td[1]/img/@src")
        s_image_path = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/tr[3]/td[1]/table/tr/td[2]/img/@src")
        # how_to = fileTree.xpath('//table[@class = "dextable"]/tr[./td/text() = "Alternate Forms"]/following-sibling::tr/td/table[2]/tr/td//text()')

        # print(list(zip(img_name_list, img_path_list)))
        # print(how_to)
        # print(len(orig_name), len('pikachu'), ''.join(list(str(orig_name)[11:-2])))

        # name comes in a funky way, this was the easiest way to bipass it
        orig_name = ''.join(list(str(orig_name)[11:-2]))
        #
        # if len(img_name_list) > 0:
        #     for name, url in zip(img_name_list,img_path_list):
        #         self.__download_image(self.__serebiiUrl+url, os.path.join(orig_name, "Pokemon Forms"), name)
        #
        #     with open(os.path.join(self.__imgDir[:-1], orig_name, "Pokemon Forms", "How-to.txt"), 'w') as f:
        #         for howto in how_to:
        #             f.write(howto)
        if len(mega_name)>0:
            print(mega_name)
            print(image_path, s_image_path)
            self.__download_image(self.__serebiiUrl+image_path[0], os.path.join(orig_name, "Mega Evolutions"), mega_name[0])
            self.__download_image(self.__serebiiUrl+s_image_path[0], os.path.join(orig_name, "Mega Evolutions"), mega_name[0]+'-Shiny')
            if len(mega_name) > 1:
                self.__download_image(self.__serebiiUrl+image_path[1], os.path.join(orig_name, "Mega Evolutions"), mega_name[1])
                self.__download_image(self.__serebiiUrl+s_image_path[1], os.path.join(orig_name, "Mega Evolutions"), mega_name[1]+'-Shiny')

    def get_mega_data(self):
        fileTree = html.fromstring(self.__html)
        orig_name = fileTree.xpath('///table[@class = "dextab"]/tr/td[1]/table/tr/td[2]/font/b/text()')
        orig_name = ''.join(list(str(orig_name)[11:-2]))
        mega_name = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/tr[3]/td[2]/text()")
        mega_name = [str(name) for name in mega_name]
        if(len(mega_name) > 0):
            national_dex = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/tr[3]/td[4]/table/tr/td[./b/text() = 'National']/following-sibling::td/text()")

            national_dex = [item.lstrip('#') for item in national_dex]
            central_dex = [0 for _ in mega_name]
            coastal_dex = [0 for _ in mega_name]
            mountain_dex = [0 for _ in mega_name]
            hoenn_dex = [0 for _ in mega_name]
            male_rate = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/tr[3]/td[5]/table/tr/td[starts-with(./text(), 'Male')]/following-sibling::td/text()")
            female_rate = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/tr[3]/td[5]/table/tr/td[starts-with(./text(), 'Female')]/following-sibling::td/text()")
            if(len(male_rate)< 1):
                male_rate = ['0%'] * len(mega_name)
            if(len(female_rate)< 1):
                female_rate = ['0%'] * len(mega_name)
            genderless = 1 if (len(male_rate) == 0 and len(female_rate) == 0) else 0
            genderless = [genderless] * len(mega_name)
            type1 = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/tr[3]/td[6]/a[1]/img/@src")
            type1 = [item[17:-4] for item in type1]
            type2 = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/tr[3]/td[6]/a[2]/img/@src")
            if(len(type2) < 1):
                type2 = [''] * len(mega_name)
            elif(len(type2) < len(mega_name)):
                type2 = [item[17:-4] for item in type2] + ['']
            else:
                type2 = [item[17:-4] for item in type2]
            classification = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/tr[5]/td[1]/text()")
            height_inches = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/tr[5]/td[2]/text()")
            height_m = height_inches[1::2]
            height_m = [height.replace('\n', '').replace('\t', '') for height in height_m]

            height_inches = height_inches[::2]
            height_inches = [height.strip('\n').strip('\t').strip('\\') for height in height_inches]
            # height_inches = [height[0] + height[2:] for height in height_inches]
            weight_kgs = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/tr[5]/td[3]/text()")
            weight_lbs = weight_kgs[::2]
            weight_kgs = weight_kgs[1::2]
            weight_kgs = [weight.strip('\n').strip('\t') for weight in weight_kgs]
            capture_rate = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/tr[5]/td[4]/text()")
            base_egg_steps = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/tr[5]/td[5]/text()")
            base_egg_steps = [step.replace(',', '') for step in base_egg_steps]
            path_img = [os.path.join('PokeData', orig_name, 'Mega Evolutions', name+'.png') for name in mega_name]
            path_simg = [os.path.join('PokeData', orig_name, 'Mega Evolutions', name+'-Shiny.png') for name in mega_name]
            exp_growth = [0] * len(mega_name)
            exp_growth_class = [''] * len(mega_name)
            base_happiness = [0] * len(mega_name)
            sky_battle = [''] * len(mega_name)
            tot_abilities = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[1]/tr[2]/td/descendant::text()")
            abilities = [''.join(tot_abilities[1:3])]
            if(len(tot_abilities) > 3):
                abilities = abilities + [''.join(tot_abilities[4:])]
            abilities = [ability.split(':') for ability in abilities]
            normal = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[2]/tr[3]/td[1]/text()")
            normal = [stat.lstrip('*') for stat in normal]
            normal = [float(weak) for weak in normal]
            fire = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[2]/tr[3]/td[2]/text()")
            fire = [stat.lstrip('*') for stat in fire]
            fire =  [float(weak) for weak in fire]
            water = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[2]/tr[3]/td[3]/text()")
            water = [stat.lstrip('*') for stat in water]
            water =  [float(weak) for weak in water]
            electric = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[2]/tr[3]/td[4]/text()")
            electric = [stat.lstrip('*') for stat in electric]
            electric = [float(weak) for weak in (electric)]
            grass = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[2]/tr[3]/td[5]/text()")
            grass = [stat.lstrip('*') for stat in grass]
            grass =  [float(weak) for weak in (grass)]
            ice = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[2]/tr[3]/td[6]/text()")
            ice = [stat.lstrip('*') for stat in ice]
            ice =  [float(weak) for weak in (ice)]
            fighting = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[2]/tr[3]/td[7]/text()")
            fighting = [stat.lstrip('*') for stat in fighting]
            fighting = [float(weak) for weak in (fighting)]
            poison = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[2]/tr[3]/td[8]/text()")
            poison = [stat.lstrip('*') for stat in poison]
            poison = [float(weak) for weak in (poison)]
            ground = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[2]/tr[3]/td[9]/text()")
            ground = [stat.lstrip('*') for stat in ground]
            ground = [float(weak) for weak in (ground)]
            flying = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[2]/tr[3]/td[10]/text()")
            flying = [stat.lstrip('*') for stat in flying]
            flying = [float(weak) for weak in (flying)]
            psychic = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[2]/tr[3]/td[11]/text()")
            psychic = [stat.lstrip('*') for stat in psychic]
            psychic = [float(weak) for weak in (psychic)]
            bug = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[2]/tr[3]/td[12]/text()")
            bug = [stat.lstrip('*') for stat in bug]
            bug =  [float(weak) for weak in (bug)]
            rock = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[2]/tr[3]/td[13]/text()")
            rock = [stat.lstrip('*') for stat in rock]
            rock = [float(weak) for weak in (rock)]
            ghost = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[2]/tr[3]/td[14]/text()")
            ghost = [stat.lstrip('*') for stat in ghost]
            ghost = [float(weak) for weak in (ghost)]
            dragon = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[2]/tr[3]/td[15]/text()")
            dragon = [stat.lstrip('*') for stat in dragon]
            dragon = [float(weak) for weak in (dragon)]
            dark = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[2]/tr[3]/td[16]/text()")
            dark = [stat.lstrip('*') for stat in dark]
            dark = [float(weak) for weak in (dark)]
            steel = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[2]/tr[3]/td[17]/text()")
            steel = [stat.lstrip('*') for stat in steel]
            steel = [float(weak) for weak in (steel)]
            fairy = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[2]/tr[3]/td[18]/text()")
            fairy = [stat.lstrip('*') for stat in fairy]
            fairy = [float(weak) for weak in (fairy)]
            eggroup1 = [''] * len(mega_name)
            eggroup2 = [''] * len(mega_name)
            locationX = [''] * len(mega_name)
            locationY = [''] * len(mega_name)
            locationAS = [''] * len(mega_name)
            dexTextX = [''] * len(mega_name)
            dexTextY = [''] * len(mega_name)
            dexTextOR = [''] * len(mega_name)
            dexTextAS = [''] * len(mega_name)
            hp = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[3]/tr[3]/td[2]/text()")
            attack = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[3]/tr[3]/td[3]/text()")
            defense = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[3]/tr[3]/td[4]/text()")
            sp_attack = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[3]/tr[3]/td[5]/text()")
            sp_defense = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[3]/tr[3]/td[6]/text()")
            speed = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[3]/tr[3]/td[7]/text()")
            total = fileTree.xpath("//table[@class='dextable' and starts-with(./tr[1]/td/font/b/text(), 'Mega Evolution')]/following-sibling::table[3]/tr[3]/td[1]/text()")
            total = [tot[-3:] for tot in total]
            for i in range(len(mega_name)):
                print(mega_name[i], national_dex[i])
                print(male_rate[i])
                print(female_rate[i], genderless[i])
                print(type1[i], type2[i])
                print(classification[i])
                heights = PokeHeight(height_m[i], height_inches[i])
                weights = PokeWeight(weight_kgs[i], weight_lbs[i])

                print(heights.get_value_in_inches(), heights.get_value_in_meters())
                print(weights.get_value_in_kg(), weights.get_value_in_lbs())
                print(capture_rate[i], base_egg_steps[i])
                print(abilities[i])
                print(normal[i], fire[i], water[i], electric[i], grass[i], ice[i], fighting[i], poison[i], ground[i], flying[i], psychic[i], bug[i], rock[i], ghost[i], dragon[i], dark[i], steel[i], fairy[i])

                print(hp[i], attack[i], defense[i], sp_attack[i], sp_defense[i], speed[i], total[i])

                db = PokemonManager()

                db.insert_pokemon_raw(mega_name[i], national_dex[i], central_dex[i],
                    coastal_dex[i], mountain_dex[i], hoenn_dex[i], float(male_rate[i][:-1]),
                    float(female_rate[i][:-1]), genderless[i], type1[i], type2[i], classification[i],
                    heights.get_value_in_meters(), heights.get_value_in_inches(), weights.get_value_in_kg(), weights.get_value_in_lbs(), '', '',
                    int(base_egg_steps[i]), path_img[i], path_simg[i], exp_growth[i], exp_growth_class[i],
                    base_happiness[i], sky_battle[i], normal[i], fire[i], water[i], electric[i],
                    grass[i], ice[i], fighting[i], poison[i], ground[i], flying[i], psychic[i],
                    bug[i], rock[i], ghost[i], dragon[i], dark[i], steel[i], fairy[i], '',
                    '', '', '', '', '', '', '', '', '', hp[i], attack[i], defense[i],
                    sp_attack[i], sp_defense[i], speed[i], total[i])
                # db.insert_ability(mega_name[i], abilities[i][0], abilities[i][1])
                print('--------------------------')
                print()

    # Ensures that directory f exists
    def __ensure_dir(self, f):
        d = os.path.dirname(f)
        if not os.path.exists(d):
            os.makedirs(d)
        if not os.path.exists(f):
            os.makedirs(f)
            # --------------------------------------------------------------------------------

    #  Get abilities
    def __get_abilities(self, info):
        info = info.findNext()
        info = info.findNextSibling()
        #         print(str(info).encode('utf-8','ignore'))
        try:
            end = info.find(text='Hidden Ability').findNext('a')
        except AttributeError:
            end = None
        #         print(end)
        tags = info.findAll('a')
        abilities = {}
        abilityType = 'Normal'
        abilities[abilityType] = []
        for tag in tags:
            if tag is end:
                abilityType = 'Hidden'
                abilities[abilityType] = []
            ability = {}
            name = tag.getText()
            description = tag.next_sibling
            ability[name] = description
            abilities[abilityType].append(ability)
        self.__poke['Abilities'] = abilities

        return info

    # --------------------------------------------------------------------------------
    def __get_weaknesses(self, soup):
        types = [Type.Normal, Type.Fire, Type.Water, Type.Electric, Type.Grass, Type.Ice, Type.Fighting, Type.Poison,
                 Type.Ground, Type.Flying, Type.Psychic, Type.Bug, Type.Rock, Type.Ghost, Type.Dragon, Type.Dark,
                 Type.Steel, Type.Fairy]
        info = soup.find('td', {'class', 'footype'})
        info = info.findParent()
        tags1 = info.findAll('td', {'class', 'footype'})
        info = info.findNextSibling()
        tags2 = info.findAll('td', {'class', 'footype'})
        weak = {}
        for tag1, tag2, t in zip(tags1, tags2, types):
            # Descomentar para baixar imagens dos Tipos
            # self.__download_image(self.__serebiiUrl+tag1.a.img['src'],'Tipos',t.__str__())
            weak[t] = tag2.string
        self.__poke['Weaknesses'] = weak

    # --------------------------------------------------------------------------------
    def __get_item_egg_group(self, soup):

        # Get Items
        name = soup.find('td', {'class', 'footwo'})
        info = name.findParent().findNextSibling().findNext()

        try:
            self.__poke[name.string] = info.get_text()
            imgUrl = self.__serebiiUrl + info.a.img['src']
        #             self.__download_image(imgUrl,self.__poke['Name']+'/Wild Items',self.__poke[name.string].split('-')[0])
        except AttributeError:
            self.__poke[name.string] = 'None'

        try:
            dexnav = info.find('table', class_='dexitem')
            items = dexnav.findAll('td')
            dexnavItems = []
            for item in items:
                imgUrl = self.__serebiiUrl + item.a.img['src']
                #                 self.__download_image(imgUrl,self.__poke['Name']+'/Wild Items/DexNav',item.get_text())
        except AttributeError:
            c = 'sem erro'

        # Get Egg Group
        name = name.findNextSibling()
        info = info.findNextSibling().find('table', class_='dexitem')
        try:
            tags = info.findAll('tr')
            eggGroup = []
            for tag in tags:
                eggGroup.append(tag.find('td').findNextSibling().get_text())
            self.__poke[name.get_text()] = eggGroup
        except AttributeError:
            self.__poke[name.get_text()] = 'Not Breedable'

            # --------------------------------------------------------------------------------

    def __get_evo_chain(self, soup):
        info = soup.find('table', class_='evochain')
        tagsTr = info.findAll('tr')
        pokeEvoChain = []
        row = 0
        column = 0
        for tagTr in tagsTr:
            tagsTd = tagTr.findAll('td')
            #print(tagTr.findParent())
            column = 0
            for tagTd in tagsTd:
                try:
                    c = tagTd['class']
                    isPokemon = True
                except KeyError:
                    isPokemon = False
                try:
                    rowSpan = tagTd['rowspan']
                except KeyError:
                    rowSpan = 0
                try:
                    columnSpan = tagTd['colspan']
                except KeyError:
                    columnSpan = 0
                #print(isPokemon,column,columnSpan,row,rowSpan)
                try:
                    aux = tagTd.a.img['src'].split('/').pop().split('.')[0]

                except AttributeError:
                    aux = tagTd.img['src'].split('/').pop().split('.')[0]

                pokeEvoChain.append((aux, row, rowSpan, column, columnSpan, isPokemon))

                column += 1
            row += 1
        self.__poke['Evo Chain'] = pokeEvoChain

    # --------------------------------------------------------------------------------
    def __get_attacks(self, soup):
        info = soup.find('a', {'name': 'attacks'})
        end = soup.find('a', {'name': 'stats'}).findNext('table', {'class': 'dextable'})
        #         print(end.next)
        exceptions = ['Generation VI Level Up', 'X & Y Level Up', 'TM & HM Attacks', '\u03a9R\u03b1S Level Up',
                      'X / Y Level Up - Attack Forme', '\u03a9R\u03b1S Level Up - Attack Forme',
                      'X / Y Level Up - Defense Forme', '\u03a9R\u03b1S Level Up - Defense Forme',
                      'X / Y Level Up - Speed Forme', '\u03a9R\u03b1S Level Up - Speed Forme',
                      'X / Y Level Up - Sandy Cloak', '\u03a9R\u03b1S Level Up - Sandy Cloak',
                      'X / Y Level Up - Trash Cloak', '\u03a9R\u03b1S Level Up - Trash Cloack',
                      'X / Y Level Up - Sky Forme', '\u03a9R\u03b1S Level Up - Sky Forme', 'X / Y Level Up - Zen Mode',
                      '\u03a9R\u03b1S Level Up - Zen Mode', 'X / Y Level Up - White Kyurem',
                      '\u03a9R\u03b1S Level Up - White Kyurem', 'X / Y Level Up - Black Kyurem',
                      '\u03a9R\u03b1S Level Up - Black Kyurem', 'X / Y Level Up - Pirouette Forme',
                      '\u03a9R\u03b1S Level Up - Pirouette Forme', 'X / Y Level Up - Eternal Flower',
                      '\u03a9R\u03b1S Level Up - Eternal Flower', 'X / Y Level Up - Female',
                      '\u03a9R\u03b1S Level Up - Female', 'Level Up - Hoopa Unbound']  # '\0u3a9''\u03b1'
        tags = info.findAllNext('tr')
        attack = []
        attacks = {}
        attackClassName = ''
        count = 0
        for tag in tags:
            if (tag == end.next):
                break
            if (tag.td is not None):
                #                 print(tag.td.encode('utf-8'))
                try:
                    if (tag.td['class'][0] == 'fooevo'):
                        attackClassName = tag.td.getText()
                        attacks[attackClassName] = []
                    elif (tag.td['class'][0] == 'fooinfo'):
                        if (count == 0):
                            attack = []
                            #                             print(attackClassName.replace('\u03a9','2').replace('\u03b1','3'))
                            if (attackClassName in exceptions):
                                countTd = 0
                            else:
                                countTd = 1
                            for td in tag.findAll('td'):
                                if (countTd == 0):
                                    attack.append(td.getText())
                                elif (countTd == 1):
                                    attack.append(td.getText())
                                elif (countTd == 2):
                                    attack.append(td.img['src'][17:-4].capitalize())
                                elif (countTd == 3):
                                    attack.append(td.img['src'][17:-4].capitalize())
                                elif (countTd == 4):
                                    attack.append(td.getText())
                                elif (countTd == 5):
                                    attack.append(td.getText())
                                elif (countTd == 6):
                                    attack.append(td.getText())
                                elif (countTd == 7):
                                    attack.append(td.getText().replace('\u2014', '-'))
                                countTd += 1
                        elif (count == 1):
                            for td in tag.findAll('td'):
                                attack.append(td.getText())
                                attacks[attackClassName].append(attack)
                        count += 1
                        if (count == 2):
                            count = 0
                except KeyError:
                    if (tag.td['colspan'][0] == '3'):
                        if (count == 1):
                            for td in tag.findAll('td'):
                                attack.append(td.getText())
                                attacks[attackClassName].append(attack)
                        count += 1
                        if (count == 2):
                            count = 0

        self.__poke['Attacks'] = attacks

    # --------------------------------------------------------------------------------
    def __get_stats(self, soup):
        stats = []
        info = soup.find('td', {'colspan': '2', 'width': '14%', 'class': 'fooinfo'})
        stats.append(info.getText())
        tags = info.findNextSiblings('td')
        for tag in tags:
            stats.append(tag.getText())
        self.__poke['Stats'] = stats

    # --------------------------------------------------------------------------------
    def __get_location_and_flavour_text(self, soup):
        location = {}
        flavourText = {}
        data = []

        # X data
        infos = soup.findAll('td', {'class': 'foox'})
        for info in infos:
            data.append(info.parent.getText())
        flavourText['X'] = data[1]
        location['X'] = data[0]
        data.clear()

        # Y data
        infos = soup.findAll('td', {'class': 'fooy'})
        for info in infos:
            data.append(info.parent.getText())
        flavourText['Y'] = data[1]
        location['Y'] = data[0]
        data.clear()

        # Ruby data
        infos = soup.findAll('td', {'class': 'ruby'})
        for info in infos:
            data.append(info.parent.getText())
        flavourText['Ruby'] = data[1]
        location['Ruby'] = data[0]
        data.clear()

        # Shappire data
        infos = soup.findAll('td', {'class': 'sapphire'})
        for info in infos:
            data.append(info.parent.getText())
        flavourText['Sapphire'] = data[1]
        location['Sapphire'] = data[0]

        self.__poke['Flavour Text'] = flavourText
        self.__poke['Location'] = location


if __name__ == '__main__':
    run_test()