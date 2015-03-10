import os
import requests
import html.parser as html_
from lxml import html, etree
__author__ = 'pedroabreu'

from database import AttacksManager

class AttackScrapper():

    __attack_folder = 'Attacks'
    __main_list_path = os.path.join(__attack_folder, 'MainList.html')
    __main_url = 'http://www.serebii.net/attackdex-xy/'
    __core_url = 'http://www.serebii.net'
    __main_html = ''

    def db_update_sec_eff(self, attack_name, sec_effect, speed_priority):
        print("Inserting {} with Priority: {} :: \"{}\"".format(attack_name, speed_priority, sec_effect))
        db = AttacksManager()
        # db.add_secundary_eff_col()
        db.insert_sec_effect(attack_name, sec_effect, speed_priority)
        # print(db.get_attack_by_name("Yawn"))

    def download_main_attack_page_xy(self):

        if(not os.path.exists(self.__attack_folder)):
            os.mkdir(self.__attack_folder)
            r = requests.get(self.__url)
            if (r.status_code != 200):
                raise  Exception('Download failed')

            self.__main_html = html_.unescape(r.text)
            with open(self.__main_list_path,mode='wb') as f:
                f.write(r.content)
                f.close()

    def download_attack_pages(self):
        main_html = html.parse(self.__main_list_path)
        pages_links = main_html.xpath('//td/form/div/select/option/@value')
        pages_names = main_html.xpath('//td/form/div/select/option/text()')
        # print(html.tostring(pages_links[0]))
        for page_link, page_name in zip(pages_links, pages_names):
            print("Downloading: %s" % page_name )
            r = requests.get(self.__core_url+page_link)
            if r.status_code != 200:
                raise Exception('Download failed')

            # text = html_.unescape(r.text)
            page_path = os.path.join(self.__attack_folder, page_name+".html")
            with open(page_path, mode = 'wb') as f:
                f.write(r.content)
                f.close()


    def scrap_attack_name_seceff(self, f_path):
        """
        Takes a filepath and returns it's attack name and secundary effect
        :param f_path: file path
        :return: (name, sec_eff)
        """
        attack_html = html.parse(f_path)
        name = attack_html.xpath('//table[./tr[1]/td/b/text() = "Attack Name"]/tr[2]/td/text()')
        sec_eff = attack_html.xpath("//table/tr[./td[1]/text() = 'Secondary Effect:']/following-sibling::tr[1]/td[1]/text()")
        speed_priority = attack_html.xpath("//table/tr[./td[2]/b/text() = 'Speed Priority']/following-sibling::tr[1]/td[2]/text()")
        name = name[0].lstrip('\n').lstrip('\t')
        sec_eff = sec_eff[0].strip('\n').strip('\t')
        speed_priority = speed_priority[0].strip('\t').strip('\n')
        return str(name), str(sec_eff), int(speed_priority)

    def db_insert_sec_effs(self):
        info_list = []
        for root, dirs, files in os.walk(self.__attack_folder, topdown = False):
            for f in files:
                if f != 'MainList.html':
                    f_path = os.path.join(root, f)
                    att_name, att_sec_eff, speed_priority = self.scrap_attack_name_seceff(f_path)
                    info_list.append((att_name, att_sec_eff))
                    self.db_update_sec_eff(att_name, att_sec_eff, speed_priority)
        return 0



if __name__ == '__main__':
    c = AttackScrapper()
    # c.download_main_attack_page_xy()
    # c.download_attack_pages()
    # print(list(c.list_names_effects()))
    # print(c.scrap_attack_name_seceff(os.path.join("Attacks", "Wild Charge.html")))
    print(c.db_insert_sec_effs())
    # db = AttacksManager()
    # db.add_speed_priority()
    # db.view()
    # print(db.get_attack_by_name("Round"))