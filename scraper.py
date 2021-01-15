import requests
import lxml.html as html
import os 
import datetime

HOME_URL = 'https://www.larepublica.co'

#Puede ser que el navegador muestre elementos distintos del HTML
#, por eso, si hay errores en las instrucciones del XPath, puedes 
#imprimir la respuesta del html que haces con Python y ver las etiquetas exactas.

XPATH_LINKS_TO_ARTICLE = '//a[@class="economiaSect" or @class="kicker globoeconomiaSect"]/@href' #'//div[@class="V_Title"]/h2/a/@href'

XPATH_TITLE = '//div[@class="mb-auto"]/text-fill/a/text()' #'//h2/a/text()'

XPATH_SUMMARY = '//div[@class="lead"]/p/text()'

XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            #Es importante indicar a Python el formato de caracteres especiales
            home = response.content.decode('utf-8')
            #Convertimos el html de texto plano a algo que se pueda manipular con python y Xpath gracias a lxml
            parsed = html.fromstring(home)
            #obtenemos una lista de python con los strings de todos los links
            links_to_notices = parsed.xpath(XPATH_LINKS_TO_ARTICLE)
            #print(links_to_notices)

            today = datetime.date.today().strftime('%d-%m-%y')
            #verificamos que no exista una carpeta con el nombre de la fecha del día en la presente carpeta
            if not os.path.isdir(today):
                os.mkdir(today)  #creamos la carpeta con el nombre deseado
                for link in links_to_notices:
                    parse_notice(link, today)

    except ValueError as ve:
        print(ve)


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]  #Sabemos que sólo es un elemento pero hay que sacarlo de la lista por eso el [0]
                title.replace('\"', '')
            except IndexError:
                print("Error: title vacío")
            try:
                summary = parsed.xpath(XPATH_SUMMARY)[0]
            except IndexError:
                print("Error: summary vacío")
            try:
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                print("Error: body vacío")
            
            
            #with es un manejador contextual de python
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')

                for p in body:
                    f.write(p)
                    f.write('\n')

        else:
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:
        print(ve)


def run():
    parse_home()

if __name__ == '__main__':
    run()