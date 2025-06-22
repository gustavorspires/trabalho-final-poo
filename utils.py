import json
import os
from typing import List, Dict, Tuple
from data_models import Unidade, Curso, Disciplina

def save_data_to_json(
    unidades: List[Unidade],
    cursos: List[Curso],
    disciplinas: Dict[str, Disciplina],
    filename: str = 'usp_data.json'
):
    print(f"\nSalvando dados em '{filename}'...")
    data = {
        'unidades': [u.to_dict() for u in unidades],
        'cursos': [c.to_dict() for c in cursos],
        'disciplinas': {cod: d.to_dict() for cod, d in disciplinas.items()}
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Dados salvos com sucesso!")


def load_data_from_json(filename: str = 'usp_data.json') -> Tuple[List[Unidade], List[Curso], Dict[str, Disciplina]]:
    if not os.path.exists(filename):
        return [], [], {}

    print(f"Carregando dados existentes de '{filename}'...")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("ERRO: O arquivo 'usp_data.json' está corrompido ou vazio. Por favor, remova-o e execute o scrape novamente.")
        return [], [], {}

    disciplinas_db = {}
    for cod, disc_data in data.get('disciplinas', {}).items():
        disciplina = Disciplina(cod, disc_data['nome'])
        disciplina.creditos_aula = disc_data.get('creditos_aula', 0)
        disciplina.creditos_trabalho = disc_data.get('creditos_trabalho', 0)
        disciplina.carga_horaria = disc_data.get('carga_horaria', 0)
        disciplina.cursos = set(disc_data.get('cursos', []))
        disciplinas_db[cod] = disciplina

    cursos_db = []
    cursos_map = {}
    for curso_data in data.get('cursos', []):
        curso = Curso(curso_data['nome'], curso_data['unidade'])
        curso.duracao_ideal = curso_data.get('duracao_ideal', 0)
        curso.duracao_minima = curso_data.get('duracao_minima', 0)
        curso.duracao_maxima = curso_data.get('duracao_maxima', 0)
        
        curso.obrigatorias = [disciplinas_db[cod] for cod in curso_data.get('obrigatorias', []) if cod in disciplinas_db]
        curso.optativas_livres = [disciplinas_db[cod] for cod in curso_data.get('optativas_livres', []) if cod in disciplinas_db]
        curso.optativas_eletivas = [disciplinas_db[cod] for cod in curso_data.get('optativas_eletivas', []) if cod in disciplinas_db]
        
        cursos_db.append(curso)
        cursos_map[curso.nome] = curso

    unidades_db = []
    for unidade_data in data.get('unidades', []):
        unidade = Unidade(unidade_data['nome'])
        unidade.cursos = [cursos_map[nome] for nome in unidade_data.get('cursos', []) if nome in cursos_map]
        unidades_db.append(unidade)
        
    if unidades_db or cursos_db or disciplinas_db:
        print("Dados carregados com sucesso!")
    else:
        print("Aviso: O arquivo de dados foi encontrado, mas estava vazio ou mal formatado. Execute o scrape novamente.")

    return unidades_db, cursos_db, disciplinas_db