import json
from typing import List, Dict
from data_models import Unidade, Curso, Disciplina

def save_data_to_json(
    unidades: List[Unidade],
    cursos: List[Curso],
    disciplinas: Dict[str, Disciplina],
    filename: str = 'usp_data.json'
):
    """Salva os dados coletados em um arquivo JSON."""
    print(f"\nSalvando dados em '{filename}'...")
    data = {
        'unidades': [u.to_dict() for u in unidades],
        'cursos': [c.to_dict() for c in cursos],
        'disciplinas': {cod: d.to_dict() for cod, d in disciplinas.items()}
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Dados salvos com sucesso!")