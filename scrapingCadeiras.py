# pip install selenium

# Modulo para controlar o navegador web 
from selenium import webdriver

# localizador de elementos
from selenium.webdriver.common.by import By

# Servico para configurar o caminho do executavel chromedriver
from selenium.webdriver.chrome.service import Service

# classe que permite executar acoes avancadas(o mover do mouse, clique/arrasta)
from selenium.webdriver.common.action_chains import ActionChains

# classe que espera de forma explicita ate que uma condicao seja satisfeita(ex: que um elemento apareca)
from selenium.webdriver.support.ui import WebDriverWait

# condicoes esperadas usadas com WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# Trabalhar com dataframe
import pandas as pd

# uso de funcoes relacionadas ao tempo
import time 

# uso de tratamento de excesao
from selenium.common.exceptions import TimeoutException

# definir o caminho do chromedriver
chrome_driver_path = r"C:\Program Files\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# configuracao do WebeDriver
Service = Service(chrome_driver_path) # navegador controlado pelo Selenium
options = webdriver.ChromeOptions()   # configurar as opcoes do navegador 
options.add_argument("--disable-gpu") # evita possiveis erros graficos
options.add_argument("--window-size=1920,1080") # define uma resolucao fixa


# inicializacao do WebDriver
driver = webdriver.Chrome(service=Service, options=options)

#  URL inicial
url_site = "https://www.kabum.com.br/espaco-gamer/cadeiras-gamer"
driver.get(url_site)
time.sleep(5) # aguarda 5 seg para garantir que a pagina carregue

# criar um dicionario vazio para armazenar as marcas  e precos das cadeiras 
dic_produtos = {"marca":[], "preco":[]}

# vamos iniciar na pagina 1 e incrementamos a cada troca de pagina
pagina = 1

while True:
    print(f"\n coletando dados da pagina {pagina}...")

    try:

        # WebDriverWait(driver,10): cria uma espera de ate 10 seg
        # until(...): faz com que o codigo espere ate que a condicao seja verdadeira
        # resence_of_all_elements_located(...): verifica se todos os elementos "productCard" estao acessiveis
        # By.CLASS_NAME, "productCard": indica que a busca sera feita atraves 
        WebDriverWait(driver,10).until(
            ec.presence_of_all_elements_located((By.CLASS_NAME, "productCard"))
        )
        print("Elementos encontrados com sucesso")
    except TimeoutException:
        print("Tempo de espera excedido")

    produtos = driver.find_elements(By.CLASS_NAME,"productCard")

    for produto in produtos:
        try:
            nome = produto.find_element(By.CLASS_NAME, "nameCard").text.strip()
            preco = produto.find_element(By.CLASS_NAME, "priceCard").text.strip()

            print(f"{nome} - {preco}")

            dic_produtos["marca"].append(nome)
            dic_produtos["preco"].append(preco)
    
        except Exception:
            print("Erro ao coletar dados:", Exception)

# Encontrar botao da proxima pagina

    try:
        # Encontrar o elemento
        botao_proximo = WebDriverWait(driver, 5).until(
            ec.element_to_be_clickable((By.CLASS_NAME, "nextLink"))
        )
        botao_proximo = driver.find_element(By.CLASS_NAME, "nextLink")
        if botao_proximo:
            driver.execute_script("arguments[0].scrollIntoView();", botao_proximo)
            time.sleep(1)

            # Clicar no botao
            driver.execute_script("arguments[0].click();", botao_proximo)
            print(f"indo para pagina {pagina}")
            pagina += 1
            time.sleep(5)

        else:
            print("Voce chegou na ultima pagina.")
            break

    except Exception as e:
        print("Erro ao tentar avancar para a proxima pagina", e)
        break

# Fechar o Navegador 
driver.quit()

df = pd.DataFrame(dic_produtos)
df.to_excel("cadeiras.xlsx", index=False)

print(f"Arquivo 'cadeiras' salvo com sucesso. ({len(df)} produtos capturados)")


            
        





    # encontrar o acesso para a proxima pagina
    # fechar o navegador 
    # dataframe
    # salvar os dados em csv()

