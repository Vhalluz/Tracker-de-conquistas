import requests
import json
import time
import os

STEAM_API_KEY = "SUA API DA STEAM"
STEAM_ID_64 = "SEU ID DA STEAM"
GAME_APP_ID = "ID DO SEU JOGO"

OUTPUT_FILE_PATH = os.path.join(os.path.dirname(__file__), "conquistas_steam.txt")

UPDATE_INTERVAL_SECONDS = 30

def get_achievement_data(api_key, steam_id, app_id):

    url = f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key={api_key}&steamid={steam_id}&l=brazilian"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('playerstats')
    except requests.exceptions.RequestException as e:
        print(f"[{time.strftime('%H:%M:%S')}] ERRO: Não foi possível consultar a API da Steam: {e}")
        return None
    except json.JSONDecodeError:
        print(f"[{time.strftime('%H:%M:%S')}] ERRO: Resposta inválida da API (não é JSON).")
        return None

def write_to_file(content, file_path):
    """
    Escreve o conteúdo no arquivo especificado.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    except IOError as e:
        print(f"[{time.strftime('%H:%M:%S')}] ERRO: Não foi possível escrever no arquivo '{file_path}': {e}")

def main():
    """
    Função principal que busca e atualiza o contador de conquistas.
    """
    print(f"[{time.strftime('%H:%M:%S')}] Iniciando monitoramento de conquistas para o App ID: {GAME_APP_ID} | Steam ID: {STEAM_ID_64}")
    print(f"[{time.strftime('%H:%M:%S')}] Contador será salvo em: {OUTPUT_FILE_PATH}")

    if not all([STEAM_API_KEY, STEAM_ID_64, GAME_APP_ID]):
        print(f"[{time.strftime('%H:%M:%S')}] ERRO: Por favor, preencha STEAM_API_KEY, STEAM_ID_64 e GAME_APP_ID no script.")
        input("Pressione Enter para sair...")
        return

    while True:
        player_stats = get_achievement_data(STEAM_API_KEY, STEAM_ID_64, GAME_APP_ID)

        if player_stats and 'achievements' in player_stats:
            unlocked_achievements = 0
            
            if player_stats['achievements'] is not None:
                for achievement in player_stats['achievements']:
                    if achievement.get('achieved') == 1:
                        unlocked_achievements += 1
                total_achievements = len(player_stats['achievements'])
            else:
                unlocked_achievements = 0
                total_achievements = 0
                print(f"[{time.strftime('%H:%M:%S')}] Aviso: O jogo (App ID: {GAME_APP_ID}) pode não ter conquistas ou não foi possível obter os dados.")


            display_text = f"Conquistas: {unlocked_achievements}/{total_achievements}"
            print(f"[{time.strftime('%H:%M:%S')}] {display_text}")
            write_to_file(display_text, OUTPUT_FILE_PATH)
        else:
            print(f"[{time.strftime('%H:%M:%S')}] Aviso: Não foi possível obter os dados de conquistas. Verifique seu Steam ID, App ID ou a chave da API. Tentando novamente...")
            write_to_file("Conquistas: ERRO", OUTPUT_FILE_PATH)

        time.sleep(UPDATE_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()