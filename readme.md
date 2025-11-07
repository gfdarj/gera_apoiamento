# AUXÍLIO PARA GERAR EDITAL E CONCLUSAO A PARTIR DE UMA PLANILHA PREENCHIDA COM DADOS DOS PROJETOS DE LEI


* Requisitos

    Como instalar:

        python -m venv venv

        python.exe -m pip install --upgrade pip

        pip freeze > requirements.txt

        pip install -r requirements.txt


* Estou usando (tentando) o pacote "proposicoes_bd"


* Gera o executável incluindo manualmente o pacote

        pyinstaller --onefile --hidden-import=proposicoes_bd gera_edital.py

* Está no mesmo nivel da pasta que o projeto

      pyinstaller --onefile --hidden-import=proposicoes_bd --paths=../proposicoes_bd gera_edital.py


* Gerei a interface gráfica sem o console aparecendo e incluindo a subpasta "modelos"
     
      pyinstaller --onefile --noconsole --hidden-import=proposicoes_bd --paths=../proposicoes_bd  --add-data "modelos;modelos" tk.py


