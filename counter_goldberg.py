import time
import os
import json 

# Coloque entre ''
PASTA_GOLDBERG = r'CAMINHO ONDE O GOLDBERG CRIA O ARQUIVO DE CONQUISTA EX:c:\Users\User\AppData\Roaming\GSE Saves\ID DO JOGO' 

# Nome do arquivo que o Goldberg cria, não precisa mudar esse
ARQUIVO_CONQUISTAS = 'achievements.json' 

# Cria o arquivo que deve ser carregado no Obs na fonte de texto
ARQUIVO_SAIDA_OBS = r'CAMINHO ONDE O OBS VAI CRIAR O ARQUIVO PARA EXECUTAR NO OBS'

# Número de conquistas do jogo em qustão
TOTAL_CONQUISTAS = 00

INTERVALO_ATUALIZACAO = 5 

def contar_conquistas():
    caminho_completo_conquistas = os.path.join(PASTA_GOLDBERG, ARQUIVO_CONQUISTAS)
    conquistas_desbloqueadas = 0

    if not os.path.exists(caminho_completo_conquistas):
        print(f"Erro: Arquivo de conquistas não encontrado em {caminho_completo_conquistas}")
        return f"Erro: Arquivo não encontrado!"

    try:
        with open(caminho_completo_conquistas, 'r', encoding='utf-8') as f:
            dados_json = json.load(f)
            
            for detalhes_conquista in dados_json.values():
                if 'earned' in detalhes_conquista and detalhes_conquista['earned'] == True:
                    conquistas_desbloqueadas += 1

    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{ARQUIVO_CONQUISTAS}' não é um JSON válido.")
        return f"Erro: Formato de arquivo inválido!"
    except Exception as e:
        print(f"Erro inesperado ao ler o arquivo de conquistas: {e}")
        return f"Erro ao ler conquistas!"
    
    return f"{conquistas_desbloqueadas}/{TOTAL_CONQUISTAS} Conquistas"

print(f"Iniciando contador de conquistas. Arquivo de saída: {ARQUIVO_SAIDA_OBS}")
print(f"Verificando a cada {INTERVALO_ATUALIZACAO} segundos...")

while True:
    texto_para_obs = contar_conquistas()
    try:
        with open(ARQUIVO_SAIDA_OBS, 'w', encoding='utf-8') as f:
            f.write(texto_para_obs)
    except Exception as e:
        print(f"Erro ao escrever no arquivo de saída para OBS: {e}")
        
    time.sleep(INTERVALO_ATUALIZACAO)