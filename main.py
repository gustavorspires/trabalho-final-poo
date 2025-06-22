import argparse
import os
from scraper import USPDataCollector
from utils import save_data_to_json, load_data_from_json
from menu import MenuHandler

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Coletor e visualizador de dados de cursos da USP.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'num_unidades',
        type=int,
        nargs='?',
        default=None,
        help='Número de unidades a serem processadas (opcional, processa todas se omitido).'
    )
    parser.add_argument(
        '--force-scrape',
        action='store_true',
        help='Força a coleta de dados mesmo que um arquivo salvo exista.'
    )
    args = parser.parse_args()

    DATA_FILE = 'usp_data.json'
    unidades, cursos, disciplinas = [], [], {}
    
    data_loaded_from_file = not args.force_scrape and os.path.exists(DATA_FILE)

    if not data_loaded_from_file:
        num_str = args.num_unidades or "todas as"
        print(f"Iniciando coleta de dados para {num_str} unidades. Isso pode levar vários minutos...")
        
        collector = USPDataCollector(max_units=args.num_unidades)
        try:
            unidades, cursos, disciplinas = collector.collect_data()
            if unidades:
                save_data_to_json(unidades, cursos, disciplinas, DATA_FILE)
        except Exception as e:
            print(f"\nOcorreu um erro fatal durante a coleta: {e}")
    else:
        unidades, cursos, disciplinas = load_data_from_json(DATA_FILE)

    if data_loaded_from_file and args.num_unidades is not None and args.num_unidades > 0:
        print(f"\nFiltrando dados para exibir apenas as primeiras {args.num_unidades} unidades...")

        unidades_filtradas = unidades[:args.num_unidades]
        nomes_unidades_filtradas = {u.nome for u in unidades_filtradas}

        cursos_filtrados = [c for c in cursos if c.unidade in nomes_unidades_filtradas]
        nomes_cursos_filtrados = {c.nome for c in cursos_filtrados}

        disciplinas_filtradas = {}
        for codigo, disciplina in disciplinas.items():
            disciplina.cursos.intersection_update(nomes_cursos_filtrados)
            if disciplina.cursos:
                disciplinas_filtradas[codigo] = disciplina
        
        unidades = unidades_filtradas
        cursos = cursos_filtrados
        disciplinas = disciplinas_filtradas

    print("\n--- Resumo dos Dados ---")
    print(f"Total de Unidades: {len(unidades)}")
    print(f"Total de Cursos: {len(cursos)}")
    print(f"Total de Disciplinas Únicas: {len(disciplinas)}")

    if not unidades:
        print("\nNenhum dado para consultar. Execute o programa sem a flag '--force-scrape' para coletar os dados.")
    else:
        menu = MenuHandler(unidades, cursos, disciplinas)
        menu.run()

    print("\nExecução concluída.")