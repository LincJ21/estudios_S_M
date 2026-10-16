# -*- coding: utf-8 -*-
import os
import re
import sys

from header_title import get_header_and_title
from punto1 import get_punto1
from punto2 import get_punto2
from punto3 import get_punto3
from punto4 import get_punto4
from punto5 import get_punto5
from punto6 import get_punto6
from punto7 import get_punto7
from punto8_sintesis import get_punto8

def check_for_emojis(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U0001FA00-\U0001FA6F"  # chess symbols
        "\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-a
        "\U00002600-\U000026FF"  # miscellaneous symbols
        "]+", flags=re.UNICODE
    )
    matches = emoji_pattern.findall(text)
    return matches

def main():
    print("Iniciando ensamblado del Cuaderno de Apuntes Digital...")
    
    # Lectura de los codigos 01 y 02
    path_01 = os.path.join(os.path.dirname(__file__), "..", "01", "01.py")
    path_02 = os.path.join(os.path.dirname(__file__), "..", "02", "02.py")
    
    with open(path_01, "r", encoding="utf-8") as f:
        code_01 = f.read()
    with open(path_02, "r", encoding="utf-8") as f:
        code_02 = f.read()
        
    print(f" • 01/01.py cargado: {len(code_01.splitlines())} lineas")
    print(f" • 02/02.py cargado: {len(code_02.splitlines())} lineas")
    
    # Ensamblado modular
    partes = [
        get_header_and_title(),
        get_punto1(),
        get_punto2(),
        get_punto3(),
        get_punto4(),
        get_punto5(code_01),
        get_punto6(),
        get_punto7(code_02),
        get_punto8()
    ]
    
    documento_completo = "\n".join(partes)
    
    # Verificacion estricta de ausencia de emojis
    emojis_encontrados = check_for_emojis(documento_completo)
    if emojis_encontrados:
        print(f"ALERTA: Se encontraron emojis en el documento: {emojis_encontrados}")
        sys.exit(1)
    else:
        print(" • Comprobacion de emojis superada: CERO emojis detectados en todo el documento.")
        
    # Escritura en los dos archivos objetivo
    out_paths = [
        os.path.join(os.path.dirname(__file__), "..", "overlif.txt"),
        os.path.join(os.path.dirname(__file__), "..", "overlift.txt")
    ]
    
    for opath in out_paths:
        with open(opath, "w", encoding="utf-8") as f:
            f.write(documento_completo)
        print(f" • Archivo guardado con exito: {os.path.abspath(opath)}")
        
    lineas = len(documento_completo.splitlines())
    tam_kb = len(documento_completo.encode("utf-8")) / 1024
    print("=" * 60)
    print(f" ENSAMBLADO COMPLETADO SATISFACTORIAMENTE:")
    print(f" • Total de lineas LaTeX : {lineas}")
    print(f" • Peso del archivo      : {tam_kb:.2f} KB")
    print("=" * 60)

if __name__ == "__main__":
    main()

