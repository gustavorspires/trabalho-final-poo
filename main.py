import argparse
from scraper import USPDataCollector
from utils import save_data_to_json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Coletor de dados de cursos da USP.')
    parser.add_argument(
        'num_unidades',
        type=int,
        nargs='?',
        default=None,
        help='Número de unidades a serem processadas (opcional, processa todas se omitido).'
    )
    args = parser.parse_args()

    num_str = args.num_unidades or "todas as"
    print(f"Iniciando coleta de dados para {num_str} unidades...")
    
    collector = USPDataCollector(max_units=args.num_unidades)
    
    try:
        unidades, cursos, disciplinas = collector.collect_data()
        
        print("\n--- Resumo da Coleta ---")
        print(f"Unidades processadas: {len(unidades)}")
        print(f"Total de cursos encontrados: {len(cursos)}")
        print(f"Total de disciplinas únicas: {len(disciplinas)}")
        
        if unidades:
            save_data_to_json(unidades, cursos, disciplinas)
            
    except Exception as e:
        print(f"\nOcorreu um erro fatal durante a execução: {e}")
        print("A coleta foi interrompida.")

    print("\nExecução concluída.")