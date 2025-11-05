AUXÍLIO NA COMISSÃO PARA GERAR EDITAL E CONCLUSAO A PARTIR DE UMA PLANILHA PREENCHIDA COM DADOS DOS PROJETOS DE LEI



Como instalar os requisitos:

python -m venv venv

python.exe -m pip install --upgrade pip

pip freeze > requirements.txt

pip install -r requirements.txt


----------------------------

Estou usando (tentando) o pacote "proposicoes_bd"

# Gera o executável incluindo manualmente o pacote
pyinstaller --onefile --hidden-import=proposicoes_bd gera_edital.py



