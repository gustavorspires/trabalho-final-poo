# scraper.py

import time
import re
from typing import Dict, List, Tuple
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager

from data_models import Unidade, Curso, Disciplina

class USPDataCollector:
    """Coleta dados de cursos e disciplinas do portal Júpiter Web."""

    BASE_URL = "https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275"

    def __init__(self, max_units: int = None):
        self.max_units = max_units
        self.driver = self._setup_driver()
        self.wait = WebDriverWait(self.driver, 20)

    def _setup_driver(self) -> webdriver.Chrome:
        """Configura e inicializa o WebDriver do Selenium."""
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def _parse_number(self, text: str) -> int:
        """Extrai um número de uma string, retornando 0 se não encontrar."""
        if text:
            match = re.search(r'\d+', text)
            if match:
                return int(match.group())
        return 0

    def _get_or_create_discipline(self, disciplinas_db: Dict[str, Disciplina], codigo: str, nome: str) -> Disciplina:
        """Retorna uma disciplina existente do banco de dados ou cria uma nova."""
        if codigo not in disciplinas_db:
            disciplinas_db[codigo] = Disciplina(codigo, nome)
        return disciplinas_db[codigo]
        
    def _extract_course_data(self, soup: BeautifulSoup, disciplinas_db: Dict[str, Disciplina]) -> Dict:
        """
        Extrai todos os dados de uma página de curso, implementando a lógica de parsing correta.
        """
        course_name_element = soup.select_one('#step4 .curso')
        if not course_name_element:
            return None

        # Dicionário para armazenar os dados extraídos
        data = {
            'nome': course_name_element.text.strip(),
            'duracao_ideal': self._parse_number(soup.select_one('#step4 .duridlhab').text),
            'duracao_minima': self._parse_number(soup.select_one('#step4 .durminhab').text),
            'duracao_maxima': self._parse_number(soup.select_one('#step4 .durmaxhab').text),
            'obrigatorias': [], 'optativas_livres': [], 'optativas_eletivas': []
        }
        
        grade_div = soup.find('div', id='gradeCurricular')
        if not grade_div:
            return data

        current_list = None
        # Itera em todas as linhas <tr> da grade para identificar seus tipos
        for row in grade_div.find_all('tr'):
            style = row.get('style', '')

            # Se a linha for um cabeçalho de categoria (azul), define a lista atual
            if 'background-color: rgb(16, 148, 171);' in style:
                header_text = row.get_text(strip=True)
                if 'Obrigatórias' in header_text:
                    current_list = data['obrigatorias']
                elif 'Optativas Livres' in header_text:
                    current_list = data['optativas_livres']
                elif 'Optativas Eletivas' in header_text:
                    current_list = data['optativas_eletivas']
                else:
                    current_list = None  # Categoria desconhecida
                continue # Pula para a próxima linha

            # Ignora a linha se não estivermos dentro de uma categoria válida
            if current_list is None:
                continue
            
            # Ignora linhas de pré-requisitos (laranja) e cabeçalhos de semestre (cinza)
            if 'color: rgb(235, 143, 0);' in style or 'background-color: rgb(204, 204, 204);' in style:
                continue

            # Tenta extrair dados de uma linha de disciplina
            cells = row.find_all('td')
            # Uma linha de disciplina válida tem pelo menos 8 células e um link na primeira
            if len(cells) >= 8 and cells[0].find('a'):
                codigo = cells[0].get_text(strip=True)
                nome = cells[1].get_text(strip=True)
                
                disciplina = self._get_or_create_discipline(disciplinas_db, codigo, nome)
                disciplina.creditos_aula = self._parse_number(cells[2].text)
                disciplina.creditos_trabalho = self._parse_number(cells[3].text)
                disciplina.carga_horaria = self._parse_number(cells[4].text)
                disciplina.carga_estagio = self._parse_number(cells[5].text)
                disciplina.carga_praticas = self._parse_number(cells[6].text)
                disciplina.atividades_aprofundamento = self._parse_number(cells[7].text)
                
                current_list.append(disciplina)
        
        return data

    def _navigate_to_curriculum(self, course_code: str):
        """Seleciona um curso, busca e espera a grade curricular carregar."""
        Select(self.driver.find_element(By.ID, "comboCurso")).select_by_value(course_code)
        
        try:
            self.driver.find_element(By.ID, "enviar").click()
        except ElementClickInterceptedException:
            enviar_button = self.driver.find_element(By.ID, "enviar")
            self.driver.execute_script("arguments[0].click();", enviar_button)

        self.wait.until(EC.element_to_be_clickable((By.ID, 'step4-tab')))
        self.wait.until(EC.presence_of_element_located((By.ID, "gradeCurricular")))

    def _return_to_search_form(self, unit_code: str):
        """Retorna para o formulário de busca de cursos."""
        try:
            tab_element = self.wait.until(EC.element_to_be_clickable((By.ID, 'step1-tab')))
            tab_element.click()
        except ElementClickInterceptedException:
            tab_element = self.driver.find_element(By.ID, 'step1-tab')
            self.driver.execute_script("arguments[0].click();", tab_element)
        
        self.wait.until(EC.presence_of_element_located((By.ID, "comboUnidade")))
        Select(self.driver.find_element(By.ID, "comboUnidade")).select_by_value(unit_code)
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='comboCurso']/option[2]")))

    def collect_data(self) -> Tuple[List[Unidade], List[Curso], Dict[str, Disciplina]]:
        """Orquestra o processo completo de coleta de dados."""
        unidades_db: List[Unidade] = []
        cursos_db: List[Curso] = []
        disciplinas_db: Dict[str, Disciplina] = {}

        try:
            self.driver.get(self.BASE_URL)
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#comboUnidade option[value]:not([value=''])")))

            unit_select = Select(self.driver.find_element(By.ID, "comboUnidade"))
            units = [{'codigo': opt.get_attribute('value'), 'nome': opt.text.strip()} for opt in unit_select.options[1:]]
            units_to_process = units[:self.max_units] if self.max_units else units

            for unit_data in units_to_process:
                try:
                    print(f"\nProcessando Unidade: {unit_data['nome']}...")
                    Select(self.driver.find_element(By.ID, "comboUnidade")).select_by_value(unit_data['codigo'])
                    self.wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='comboCurso']/option[2]")))
                    
                    course_select = Select(self.driver.find_element(By.ID, "comboCurso"))
                    courses = [{'codigo': opt.get_attribute('value'), 'nome': opt.text.strip()} for opt in course_select.options[1:]]
                    print(f"Encontrados {len(courses)} cursos.")

                    unidade_obj = Unidade(unit_data['nome'])
                    unidades_db.append(unidade_obj)

                    for i, course_data in enumerate(courses):
                        print(f"  - Coletando dados do curso {i+1}/{len(courses)}: {course_data['nome']}")
                        
                        self._navigate_to_curriculum(course_data['codigo'])
                        
                        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                        parsed_data = self._extract_course_data(soup, disciplinas_db)

                        if parsed_data:
                            curso_obj = Curso(parsed_data['nome'], unit_data['nome'])
                            curso_obj.duracao_ideal = parsed_data['duracao_ideal']
                            curso_obj.duracao_minima = parsed_data['duracao_minima']
                            curso_obj.duracao_maxima = parsed_data['duracao_maxima']
                            
                            for disc_type in ['obrigatorias', 'optativas_livres', 'optativas_eletivas']:
                                for disc_obj in parsed_data[disc_type]:
                                    getattr(curso_obj, disc_type).append(disc_obj)
                                    disc_obj.cursos.add(curso_obj.nome)
                            
                            unidade_obj.cursos.append(curso_obj)
                            cursos_db.append(curso_obj)
                        
                        self._return_to_search_form(unit_data['codigo'])

                except Exception as e:
                    print(f"    ERRO inesperado ao processar a unidade {unit_data['nome']}: {e}")
                    print("    Abandonando esta unidade e continuando para a próxima.")
                    self.driver.get(self.BASE_URL)
                    self.wait.until(EC.presence_of_element_located((By.ID, "comboUnidade")))
                    continue
        
        finally:
            self.driver.quit()
            print("\nNavegador fechado.")
        
        return unidades_db, cursos_db, disciplinas_db