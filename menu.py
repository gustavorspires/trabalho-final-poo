from typing import List, Dict, Optional
from data_models import Unidade, Curso, Disciplina

class MenuHandler:
    """Gerencia o menu interativo para consultar os dados da USP."""

    def __init__(self, unidades: List[Unidade], cursos: List[Curso], disciplinas: Dict[str, Disciplina]):
        self.unidades_list = sorted(unidades, key=lambda u: u.nome)
        self.cursos_list = sorted(cursos, key=lambda c: c.nome)
        self.disciplinas_db = disciplinas
        self.disciplinas_by_name_map = {d.nome.lower(): d for d in disciplinas.values()}

    def _print_help(self):
        """Imprime o menu de ajuda com as instruções de comando."""
        print("\n--- Menu de Consulta ---")
        print("Comandos de Listagem Geral:")
        print("  U                               - Lista todas as unidades.")
        print("  C                               - Lista todos os cursos, agrupados por unidade.")
        print("  D COMUM                         - Lista disciplinas que pertencem a mais de um curso.")
        print("\nComandos de Consulta Específica:")
        print("  U [sigla/nome]                  - Mostra os cursos de uma unidade específica.")
        print("  C [sigla/nome] [Nº]             - Mostra os dados de um curso específico.")
        print("  DC [sigla/nome] [Nº]            - Lista todas as disciplinas de um curso específico.")
        print("  D [código/nome]                 - Mostra os dados de uma disciplina específica.")
        print("\nComandos de Busca e Estatísticas:")
        print("  BUSCAR C [termo]                - Busca cursos que contêm o termo no nome.")
        print("  STATS                           - Mostra estatísticas gerais sobre os dados coletados.")
        print("  AJUDA                           - Mostra este menu de ajuda.")
        print("  SAIR                            - Encerra o programa.")
        print("-" * 35)

    def _find_unidade(self, query: str) -> Optional[Unidade]:
        """Encontra uma unidade por nome completo ou pela sigla entre parênteses."""
        query_lower = query.lower()
        sigla_pattern = f"( {query_lower} )"
        for unidade in self.unidades_list:
            unidade_nome_lower = unidade.nome.lower()
            if query_lower == unidade_nome_lower or sigla_pattern in unidade_nome_lower:
                return unidade
        return None

    def _display_all_unidades(self):
        print("\n--- Todas as Unidades ---")
        for i, unidade in enumerate(self.unidades_list):
            print(f"{i+1:2d}. {unidade.nome}")

    def _display_all_cursos(self):
        print("\n--- Todos os Cursos ---")
        for unidade in self.unidades_list:
            if unidade.cursos:
                print(f"\n> {unidade.nome}:")
                for curso in sorted(unidade.cursos, key=lambda c: c.nome):
                    print(f"  - {curso.nome}")

    def _display_unidade_details(self, unidade: Unidade):
        """Imprime os detalhes de uma unidade encontrada."""
        print(f"\n> Unidade: {unidade.nome}")
        if not unidade.cursos:
            print("  - Nenhum curso encontrado para esta unidade.")
            return
        print("  Cursos oferecidos:")
        for i, curso in enumerate(sorted(unidade.cursos, key=lambda c: c.nome)):
            print(f"    {i+1}. {curso.nome}")

    def _get_curso_by_number(self, unit_query: str, course_number_str: str) -> Optional[Curso]:
        """Busca um curso em uma unidade pelo seu número na lista ordenada."""
        unidade = self._find_unidade(unit_query)
        if not unidade:
            print(f"ERRO: Unidade '{unit_query}' não encontrada.")
            return None
        try:
            course_number = int(course_number_str)
            sorted_cursos = sorted(unidade.cursos, key=lambda c: c.nome)
            if 1 <= course_number <= len(sorted_cursos):
                return sorted_cursos[course_number - 1]
            else:
                print(f"ERRO: Número do curso inválido. A unidade tem apenas {len(sorted_cursos)} cursos.")
                return None
        except ValueError:
            print(f"ERRO: '{course_number_str}' não é um número de curso válido.")
            return None

    def _find_and_display_curso_details(self, curso: Curso):
        """Exibe os dados de um objeto de curso."""
        print(f"\n> Curso: {curso.nome}")
        print(f"  - Unidade: {curso.unidade}")
        print(f"  - Duração Ideal: {curso.duracao_ideal} semestres")
        print(f"  - Duração Mínima: {curso.duracao_minima} semestres")
        print(f"  - Duração Máxima: {curso.duracao_maxima} semestres")
        print("\n  Quantidade de Disciplinas:")
        print(f"    - Obrigatórias: {len(curso.obrigatorias)}")
        print(f"    - Optativas Eletivas: {len(curso.optativas_eletivas)}")
        print(f"    - Optativas Livres: {len(curso.optativas_livres)}")

    def _find_and_display_course_disciplines(self, curso: Curso):
        """Exibe as listas de disciplinas de um objeto de curso."""
        print(f"\n--- Disciplinas do Curso: {curso.nome} ---")
        
        if curso.obrigatorias:
            print("\n> Disciplinas Obrigatórias:")
            for disc in sorted(curso.obrigatorias, key=lambda d: d.nome):
                print(f"  - {disc.codigo} - {disc.nome}")
        
        if curso.optativas_eletivas:
            print("\n> Disciplinas Optativas Eletivas:")
            for disc in sorted(curso.optativas_eletivas, key=lambda d: d.nome):
                print(f"  - {disc.codigo} - {disc.nome}")
        
        if curso.optativas_livres:
            print("\n> Disciplinas Optativas Livres:")
            for disc in sorted(curso.optativas_livres, key=lambda d: d.nome):
                print(f"  - {disc.codigo} - {disc.nome}")

        if not (curso.obrigatorias or curso.optativas_eletivas or curso.optativas_livres):
            print("Nenhuma disciplina encontrada para este curso.")

    def _find_and_display_disciplina(self, query: str):
        """Encontra e exibe uma disciplina por código ou nome."""
        disciplina = self.disciplinas_db.get(query.upper()) or self.disciplinas_by_name_map.get(query.lower())
        if not disciplina:
            print(f"ERRO: Disciplina '{query}' não encontrada.")
            return
        
        print(f"\n> Disciplina: {disciplina.nome} ({disciplina.codigo})")
        print(f"  - Créditos Aula: {disciplina.creditos_aula}, Créditos Trabalho: {disciplina.creditos_trabalho}")
        print(f"  - Carga Horária Total: {disciplina.carga_horaria}h")
        if disciplina.cursos:
            print("\n  Oferecida nos seguintes cursos:")
            for i, curso_nome in enumerate(sorted(list(disciplina.cursos))):
                print(f"    {i+1}. {curso_nome}")

    def _display_common_disciplines(self):
        """Exibe disciplinas que são utilizadas em mais de um curso."""
        print("\n--- Disciplinas Comuns (em mais de um curso) ---")
        common_disciplines = [d for d in self.disciplinas_db.values() if len(d.cursos) > 1]
        if not common_disciplines:
            print("Nenhuma disciplina encontrada em mais de um curso.")
            return
        
        for disc in sorted(common_disciplines, key=lambda d: len(d.cursos), reverse=True):
            print(f"- {disc.codigo} - {disc.nome} (usada em {len(disc.cursos)} cursos)")

    def _search_courses(self, term: str):
        """Busca cursos contendo um termo no nome."""
        print(f"\n--- Buscando cursos com o termo '{term}' ---")
        term_lower = term.lower()
        found_courses = [c for c in self.cursos_list if term_lower in c.nome.lower()]
        if not found_courses:
            print("Nenhum curso encontrado.")
            return
        
        for curso in found_courses:
            print(f"- {curso.nome} ({curso.unidade})")

    def _display_stats(self):
        """Exibe estatísticas interessantes sobre os dados."""
        if not self.unidades_list:
            print("Não há dados para gerar estatísticas.")
            return

        print("\n--- Estatísticas Gerais ---")
        
        # Unidade com mais cursos
        unit_with_most_courses = max(self.unidades_list, key=lambda u: len(u.cursos))
        print(f"Unidade com mais cursos: {unit_with_most_courses.nome} ({len(unit_with_most_courses.cursos)} cursos)")

        # Curso com mais disciplinas obrigatórias
        course_with_most_mand = max(self.cursos_list, key=lambda c: len(c.obrigatorias))
        print(f"Curso com mais disciplinas obrigatórias: {course_with_most_mand.nome} ({len(course_with_most_mand.obrigatorias)} disciplinas)")

        # 5 disciplinas mais comuns
        top_5_common = sorted(self.disciplinas_db.values(), key=lambda d: len(d.cursos), reverse=True)[:5]
        print("\nTop 5 disciplinas mais comuns:")
        for i, disc in enumerate(top_5_common):
             print(f"  {i+1}. {disc.nome} ({disc.codigo}) - Usada em {len(disc.cursos)} cursos")


    def run(self):
        """Inicia o loop do menu interativo."""
        self._print_help()
        while True:
            try:
                user_input = input("\nComando > ").strip()
                if not user_input: continue

                parts = user_input.split(' ', 1)
                command = parts[0].upper()
                args = parts[1] if len(parts) > 1 else ""

                if command == "SAIR":
                    print("Encerrando..."); break
                elif command == "AJUDA":
                    self._print_help()
                elif command == 'U':
                    if args:
                        unidade = self._find_unidade(args)
                        if unidade: self._display_unidade_details(unidade)
                        else: print(f"ERRO: Unidade '{args}' não encontrada.")
                    else:
                        self._display_all_unidades()
                elif command == 'C':
                    if args:
                        split_args = args.rsplit(' ', 1)
                        if len(split_args) == 2:
                            curso = self._get_curso_by_number(split_args[0], split_args[1])
                            if curso: self._find_and_display_curso_details(curso)
                        else: print("Formato inválido. Use: C [unidade] [número]")
                    else:
                        self._display_all_cursos()
                elif command == 'DC' and args:
                    split_args = args.rsplit(' ', 1)
                    if len(split_args) == 2:
                        curso = self._get_curso_by_number(split_args[0], split_args[1])
                        if curso: self._find_and_display_course_disciplines(curso)
                    else:
                        print("Formato inválido. Use: DC [unidade] [número]")
                elif command == 'D':
                    if args == 'COMUM':
                        self._display_common_disciplines()
                    elif args:
                        self._find_and_display_disciplina(args)
                    else:
                        print("Argumento para 'D' faltando. Use D [código/nome] ou D COMUM.")
                elif command == 'BUSCAR' and args:
                    search_parts = args.split(' ', 1)
                    if len(search_parts) == 2 and search_parts[0].upper() == 'C':
                        self._search_courses(search_parts[1])
                    else:
                        print("Formato inválido. Use: BUSCAR C [termo]")
                elif command == 'STATS':
                    self._display_stats()
                else:
                    print("Comando inválido. Digite 'AJUDA' para ver as opções.")
            except (KeyboardInterrupt, EOFError):
                print("\nEncerrando por interrupção do usuário..."); break