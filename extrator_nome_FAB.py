import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import unquote, urlparse
import os
import re

# Lista de páginas por estado
links_estados = [
    'https://www.fab.mil.br/organizacoes/estado/AC',
    'https://www.fab.mil.br/organizacoes/estado/AL',
    'https://www.fab.mil.br/organizacoes/estado/AP',
    'https://www.fab.mil.br/organizacoes/estado/AM',
    'https://www.fab.mil.br/organizacoes/estado/BA',
    'https://www.fab.mil.br/organizacoes/estado/CE',
    'https://www.fab.mil.br/organizacoes/estado/DF',
    'https://www.fab.mil.br/organizacoes/estado/ES',
    'https://www.fab.mil.br/organizacoes/estado/GO',
    'https://www.fab.mil.br/organizacoes/estado/MA',
    'https://www.fab.mil.br/organizacoes/estado/MT',
    'https://www.fab.mil.br/organizacoes/estado/MS',
    'https://www.fab.mil.br/organizacoes/estado/MG',
    'https://www.fab.mil.br/organizacoes/estado/PA',
    'https://www.fab.mil.br/organizacoes/estado/PB',
    'https://www.fab.mil.br/organizacoes/estado/PR',
    'https://www.fab.mil.br/organizacoes/estado/PE',
    'https://www.fab.mil.br/organizacoes/estado/PI',
    'https://www.fab.mil.br/organizacoes/estado/RJ',
    'https://www.fab.mil.br/organizacoes/estado/RN',
    'https://www.fab.mil.br/organizacoes/estado/RS',
    'https://www.fab.mil.br/organizacoes/estado/RO',
    'https://www.fab.mil.br/organizacoes/estado/RR',
    'https://www.fab.mil.br/organizacoes/estado/SC',
    'https://www.fab.mil.br/organizacoes/estado/SP',
    'https://www.fab.mil.br/organizacoes/estado/SE',
    'https://www.fab.mil.br/organizacoes/estado/TO'
]

# Setup Selenium
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Descomente se quiser rodar sem abrir o navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

dados = []

# Função para extrair dados de uma página de unidade
def extrair_dados(link):
    driver.get(link)
    time.sleep(2)
    try:
        # Nome completo da organização a partir da URL
        nome = unquote(urlparse(link).path.split("/")[-1]).replace("-", " ").title()

        descricoes = driver.find_elements(By.CSS_SELECTOR, "p.description.title")

        endereco = descricoes[0].text.strip() if len(descricoes) > 0 else ''
        linha_cep = descricoes[1].text.strip() if len(descricoes) > 1 else ''

        cep = ''
        cidade = ''
        estado = ''

        cep_match = re.search(r'CEP\s*(\d{2}\.\d{3}-\d{3})', linha_cep)
        if cep_match:
            cep = cep_match.group(1)

        cidade_estado_match = re.search(r'-\s*([\wÀ-ÿ\s]+),\s*(\w{2})', linha_cep)
        if cidade_estado_match:
            cidade = cidade_estado_match.group(1).strip()
            estado = cidade_estado_match.group(2).strip()

        dados.append([nome, endereco, cep, cidade, estado])

    except Exception as e:
        print(f"⚠️ Erro ao extrair de {link}: {e}")

# Loop pelos estados e depois por cada link “mostra”
for estado_link in links_estados:
    driver.get(estado_link)
    time.sleep(2)

    # Captura os hrefs diretamente antes que virem "stale"
    links_unidades = [
        link.get_attribute("href")
        for link in driver.find_elements(By.CSS_SELECTOR, 'a[href*="/organizacoes/mostra/"]')
    ]

    for url in links_unidades:
        extrair_dados(url)

# Fecha navegador
driver.quit()

# Cria DataFrame e salva no Excel
df = pd.DataFrame(dados, columns=["Nome", "Endereço", "CEP", "Cidade", "Estado"])
caminho = os.path.join(os.path.expanduser("~"), "Downloads", "dados_fab_completos.xlsx")
df.to_excel(caminho, index=False)

print(f"✅ Arquivo Excel salvo com sucesso em: {caminho}")
