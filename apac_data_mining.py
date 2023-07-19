import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

# chrome_options = Options()
# chrome_options.add_argument("--headless")

def interagir_e_baixar(data_inicial, data_final, outfname):

    # Configurar o driver do Selenium (neste exemplo, usaremos o Chrome)
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Abrir a página web
    url = 'http://old.apac.pe.gov.br/meteorologia/monitoramento-pluvio.php'
    driver.get(url)

    ########

    # Encontrar o campo de data inicial e preenchê-lo
    data_inicial_input = driver.find_element(By.ID, 'dataInicial')
    data_inicial_input.send_keys(Keys.HOME)
    data_inicial_input.send_keys(data_inicial)

    # Encontrar o campo de data final e preenchê-lo
    data_final_input = driver.find_element(By.ID, 'dataFinal')
    data_final_input.send_keys(Keys.HOME)
    data_final_input.send_keys(data_final)

    # Mesorregião
    button = driver.find_element(By.XPATH, "//button[@title='Mesorregião']")
    # button.click()

    # Crie uma instância de ActionChains
    actions = ActionChains(driver)

    # Selecionado a região metropolitana com as teclas de seta
    actions.click(button).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

    # Apertando o botão de pesquisa
    pesquisar = driver.find_element(By.ID, 'btPesquisaPluvio')
    pesquisar.click()

    # Esperando carregar a query
    time.sleep(30)

    # Encontrando o elemento de tabela
    table_element = driver.find_element(By.ID, "tbMonPluvio")

    # Extrair os dados da tabela e salvar em um arquivo CSV
    mode = "a" if os.path.exists(outfname) else "w"

    with open(outfname, mode, newline="") as file:
        writer = csv.writer(file)
        row_iterator = iter(table_element.find_elements(By.TAG_NAME, "tr"))
        if mode == 'a':
            next(row_iterator) 
        for row in row_iterator:
            row_data = []
            for cell in row.find_elements(By.TAG_NAME, "td"):
                row_data.append(cell.text)
            writer.writerow(row_data)

    driver.close()

# outfname = 'apac_pluvio.csv'

for ano in range(2010,2023+1):
    print(f'Processando ano {ano}')
    interagir_e_baixar(f"01/01/{ano}", f"31/12/{ano}", f"apac/apac_pluvio_{ano}.csv")
