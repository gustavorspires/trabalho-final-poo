# data_models.py

from typing import List, Dict, Set

class Disciplina:
    """Representa uma disciplina com seus dados e cursos associados."""
    def __init__(self, codigo: str, nome: str):
        self.codigo = codigo
        self.nome = nome
        self.creditos_aula: int = 0
        self.creditos_trabalho: int = 0
        self.carga_horaria: int = 0
        self.carga_estagio: int = 0
        self.carga_praticas: int = 0
        self.atividades_aprofundamento: int = 0
        self.cursos: Set[str] = set()

    def to_dict(self) -> Dict:
        """Converte o objeto Disciplina para um dicionário."""
        return {
            'codigo': self.codigo,
            'nome': self.nome,
            'creditos_aula': self.creditos_aula,
            'creditos_trabalho': self.creditos_trabalho,
            'carga_horaria': self.carga_horaria,
            'carga_estagio': self.carga_estagio,
            'carga_praticas': self.carga_praticas,
            'atividades_aprofundamento': self.atividades_aprofundamento,
            'cursos': sorted(list(self.cursos))
        }

class Curso:
    """Representa um curso com suas durações e listas de disciplinas."""
    def __init__(self, nome: str, unidade: str):
        self.nome = nome
        self.unidade = unidade
        self.duracao_ideal: int = 0
        self.duracao_minima: int = 0
        self.duracao_maxima: int = 0
        self.obrigatorias: List[Disciplina] = []
        self.optativas_livres: List[Disciplina] = []
        self.optativas_eletivas: List[Disciplina] = []

    def to_dict(self) -> Dict:
        """Converte o objeto Curso para um dicionário."""
        return {
            'nome': self.nome,
            'unidade': self.unidade,
            'duracao_ideal': self.duracao_ideal,
            'duracao_minima': self.duracao_minima,
            'duracao_maxima': self.duracao_maxima,
            'obrigatorias': [d.codigo for d in self.obrigatorias],
            'optativas_livres': [d.codigo for d in self.optativas_livres],
            'optativas_eletivas': [d.codigo for d in self.optativas_eletivas]
        }

class Unidade:
    """Representa uma unidade da universidade e os cursos que ela oferece."""
    def __init__(self, nome: str):
        self.nome = nome
        self.cursos: List[Curso] = []

    def to_dict(self) -> Dict:
        """Converte o objeto Unidade para um dicionário."""
        return {
            'nome': self.nome,
            'cursos': [curso.nome for curso in self.cursos]
        }