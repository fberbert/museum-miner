#!/usr/bin/env python3

import sys
import subprocess
from subprocess import check_output
import time
import re
from playsound import playsound

# -----------------------------------------------------
# CONFIGURATION SECTION

# importante: diretório onde você instalou o repositório
lib_dir = '/home/fabio/python/museum-miner/'
cmd_procurar = lib_dir + 'search-image.py'
cmd_celscreen = lib_dir + 'celscreen.py'

# caminho do comando tesseract no sistema operacional
cmd_tesseract = '/usr/bin/tesseract'

# quantidade mínima de itens premium no artefato, descartar quem tem menos
min_premium = 5

# tipos de artefato que você deseja farmar
# lista dos disponiveis:
#    'equipamento-guerra-ataque',
#    'equipamento-guerra-defesa',
#    'blindagem-guerra-ataque',
#    'blindagem-guerra-defesa',
#    'arma-guerra-ataque',
#    'arma-guerra-defesa'
#
tipos_habilitados = [
    'equipamento-guerra-ataque',
    #  'equipamento-guerra-defesa',
    'blindagem-guerra-ataque',
    #  'blindagem-guerra-defesa',
    'arma-guerra-ataque',
    #  'arma-guerra-defesa'
]

# armazenar artefatos 3 estrelas? True ou False
salvar_3_estrelas = False

# -----------------------------------------------------

if len(sys.argv) != 3:
    print("""
-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
Use: {} <id> <numero de vezes>

Exemplo:
    {} asus 10
-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
""".format(sys.argv[0], sys.argv[0]))
    sys.exit()

phone_id = sys.argv[1]
quantity = sys.argv[2]
action = 'museu'
snd_minerou = lib_dir + 'sound/cash.wav'
temp_file = 'print-temp-{}.png'.format(phone_id)
temp_text = 'items-{}'.format(phone_id)

# tela inicial
cinco_artefatos = lib_dir + 'img/5-artifacts.png'
tres_estrelas = lib_dir + 'img/3-estrelas.png'

# identificação de artefatos
tipo_artefato = {
    'equipamento-guerra-ataque': lib_dir + 'img/label-war-equip.png',
    'equipamento-guerra-defesa': lib_dir + 'img/label-war-equip.png',
    'blindagem-guerra-ataque': lib_dir + 'img/label-war-armor.png',
    'blindagem-guerra-defesa': lib_dir + 'img/label-war-armor.png',
    'arma-guerra-ataque': lib_dir + 'img/label-war-weapon.png',
    'arma-guerra-defesa': lib_dir + 'img/label-war-weapon.png'
}

item_premium = {
    'equipamento-guerra-ataque': [
        'Gen.*Damage:2',
        'Enemy Defender Spawn Time:1',
        'All Enemy Defensive Towers Hitpoints:1',
        'All Enemy Defensive Towers Damage:1'
    ],
    'equipamento-guerra-defesa': [
        'Pontos de vida dos generais i:1',
        'Tempo de geração do defensor:1',
        'Tempo de geragao do defensor:1',
        'Tempo de geracao do defensor:1',
        'Pontos de vida de todas as torres defensivas:1',
        'Danos de todas as torres defensivas:1'
    ],

    'blindagem-guerra-ataque': [
        'Gen.*points:2',
        'Heavy Tank Hitpoints:2',
        'Fighter Hitpoints:1',
    #    'Pontos de vida do paraquedista:1',
    #    'Pontos de vida do bombardeiro:1'
    ],
    'blindagem-guerra-defesa': [
        'Fighter Damage:1',
        'Heavy Tank Damage:1',
        'Danos do paraquedista i:1',
        'Danos do bombardeiro i:1'
        'Danos dos generais i:1'
    ],

    'arma-guerra-ataque': [
        'Fighter Damage:1',
        'Heavy Tank.*:2'
    ],
    'arma-guerra-defesa': [
        'Pontos de vida do caca i:1',
        'Pontos de vida do caga i:1',
        'Pontos de vida do caça i:1',
        'Pontos de vida do tanque pesado i:1',
        #  'Pontos de vida do paraquedista i:1',
        #  'Pontos de vida do bombardeiro i:1'
    ]
}


def print_tela(cmd_celscreen, phone_id, temp_file, color=0):
    command = '{} {} {}'.format(cmd_celscreen, phone_id, temp_file)
    subprocess.run(command.split(), stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
    if color == 0:
        command = 'convert -grayscale Rec709Luminance -brightness-contrast 40,40 {} {}'.format(temp_file, temp_file)
        subprocess.run(command.split(), stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)


# verificar se está na tela certa
print_tela(cmd_celscreen, phone_id, temp_file, 1)

# procurar tela inicial de construção no print
command = '{} {} {}'.format(cmd_procurar, temp_file, cinco_artefatos)
out = check_output(command.split())
if int(out) == 0:
    print('Você precisa estar na tela de construção de artefatos!' + str(out))
    sys.exit()

# coordenadas de cliques no museu
# será necessário criar uma matriz para cada dispositivo
# devido as diferenças no tamanho de tela
coordinates = {
    "museu": {
        "asus": [
            '1650:750:2:tap::',
            '1300:500:1:tap::',
            '1300:500:1:tap::',

            '1020:970:2:tap::check',
            '1400:700:1:tap::',
            '1300:500:1:tap::',
            '1300:500:1:tap::',


            '1020:970:2:tap::check',
            '1400:700:1:tap::',
            '1300:500:1:tap::',
            '1300:500:1:tap::',

            '1020:970:2:tap::check',
            '1400:700:1:tap::',
            '1300:500:1:tap::',
            '1300:500:1:tap::',

            '1020:970:2:tap::check',
            '1400:700:1:tap::',
            '1300:500:1:tap::',
            '1300:500:1:tap::',

            '1020:970:2:tap::check',
            '1400:700:1:tap::',
            '1300:500:1:tap::',
            '1300:500:1:tap::',
        ],
        "note8": [
            '1700:750:2:tap::',
            '1300:500:1:tap::',
            '1300:500:1:tap::',

            '1000:970:2:tap::check',
            '1425:700:1:tap::',
            '1300:500:1:tap::',
            '1300:500:1:tap::',

            '1000:970:2:tap::check',
            '1425:700:1:tap::',
            '1300:500:1:tap::',
            '1300:500:1:tap::',

            '1000:970:2:tap::check',
            '1425:700:1:tap::',
            '1300:500:1:tap::',
            '1300:500:1:tap::',

            '1000:970:2:tap::check',
            '1425:700:1:tap::',
            '1300:500:1:tap::',
            '1300:500:1:tap::',

            '1000:970:2:tap::check',
            '1425:700:1:tap::',
            '1300:500:1:tap::',
            '1300:500:1:tap::',
        ]
    }
}

artefatos = 0
job = 1
while artefatos < int(quantity) and job <= 120:
    print('Loop {}, minerei {}...'.format(job, artefatos))
    for click in coordinates[action][phone_id]:
        x, y, tempo, tipo, x2, y2 = click.split(':')

        premium_count = 0
        is_estrelas = False
        if y2 == 'check':
            print('checar artefato...')
            print_tela(cmd_celscreen, phone_id, temp_file, 1)

            # verificar se artefato é 3 estrelas
            #
            if salvar_3_estrelas:
                command = '{} {} {}'.format(cmd_procurar, temp_file, tres_estrelas)
                out = check_output(command.split())
                if int(out) > 20:
                    is_estrelas = True
                    print('artefato 3 estrelas, vamos guardar!')

            for artefato in tipo_artefato:
                if artefato not in tipos_habilitados:
                    continue

                if is_estrelas:
                    continue

                premium_count = 0

                command = '{} {} {}'.format(cmd_procurar, temp_file, tipo_artefato[artefato])
                out = check_output(command.split())

                if int(out) > 0:
                    print('É {}...'.format(artefato))
                    # contabilizar itens premium 

                    for lista_item in item_premium[artefato]:
                        item, peso = lista_item.split(':')
                        #  print('verificar para {}: {}'.format(artefato, item))
                        command = '/usr/bin/tesseract {} {} --dpi 300'.format(temp_file, temp_text)
                        subprocess.run(command.split(), stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

                        f = open(temp_text + '.txt')
                        for line in f:
                            line = line.strip()
                            if re.search('[a-zA-Z]', line, re.IGNORECASE):
                                #  print('Temos: ' + line)
                                if re.search(item, line):
                                    premium_count = premium_count + int(peso)
                                    print('*********** Encontrei ' + item)
                        # descomentar caso queira um tempo para depurar a tela
                        #  time.sleep(5)


                    print('quantidade de itens premium: {}\n\n'.format(premium_count))
                    #  time.sleep(5)

                if premium_count >= min_premium:
                    x = 1400
                    artefatos += 1
                    #  playsound(snd_minerou)
                    subprocess.run(['play', snd_minerou], stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
                    break


        if is_estrelas:
            x = 1400
            artefatos += 1
            #  playsound(snd_minerou)
            subprocess.run(['play', snd_minerou], stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

        if tipo == 'tap':
            command = 'adb -s {} shell input tap {} {}'.format(phone_id, x, y).split(' ')
        else:
            command = 'adb -s {} shell input swipe {} {} {} {}'.format(phone_id, x, y, x2, y2).split(' ')
        subprocess.run(command)
        time.sleep(int(tempo))
    job += 1

subprocess.run(['play', snd_minerou], stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
