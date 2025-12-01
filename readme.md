# AUXÍLIO PARA GERAR EDITAL E CONCLUSAO A PARTIR DE UMA PLANILHA PREENCHIDA COM DADOS DOS PROJETOS DE LEI


* Requisitos

    Como instalar:

        python -m venv venv

        python -m pip install --upgrade pip

        pip freeze > requirements.txt

        pip install -r requirements.txt


* Estou usando (tentando) o pacote "proposicoes_bd"


* Gera o executável incluindo manualmente o pacote

        pyinstaller --onefile --hidden-import=proposicoes_bd gera_edital.py

* Está no mesmo nivel da pasta que o projeto

      pyinstaller --onefile --hidden-import=proposicoes_bd --paths=../proposicoes_bd gera_edital.py


* Gerei a interface gráfica sem o console aparecendo e incluindo a subpasta "modelos"
     
      pyinstaller --onefile --noconsole --hidden-import=proposicoes_bd --paths=../proposicoes_bd  --add-data "modelos;modelos" tk.py


# Usando PyEnv (Linux)

1) Instalar dependências necessárias

        sudo apt update
        sudo apt install -y make build-essential libssl-dev zlib1g-dev \
          libbz2-dev libreadline-dev libsqlite3-dev curl \
          llvm libncursesw5-dev xz-utils tk-dev libxml2-dev \
          libxmlsec1-dev libffi-dev liblzma-dev

    Essas libs são obrigatórias para compilar Python 3.14.


2) Instalar o Pyenv

        curl https://pyenv.run | bash

Isso instala:
- pyenv
- pyenv-virtualenv
- pyenv-update
- pyenv-doctor

3) Ativar o Pyenv no seu shell

    Como você usa o Linux Mint Cinnamon, está usando o bash.

    Adicione isso ao final do ~/.bashrc:

        export PATH="$HOME/.pyenv/bin:$PATH"
        eval "$(pyenv init -)"
        eval "$(pyenv virtualenv-init -)"

    Depois recarregue o shell:

        source ~/.bashrc

    Testar:

        pyenv --version

4) Instalar o Python 3.14 pelo Pyenv

        pyenv install 3.14.0

    (ou execute pyenv install --list para ver todas as versões)

    Obs.: se ainda não saiu a final, pode instalar a versão beta/rc:

    pyenv install 3.14.0b2 por exemplo.


5) Escolher como usar o Python 3.14

    ✔️ Usar globalmente (para você, sem afetar o sistema):

        pyenv global 3.14.0

    ✔️ Usar por projeto (o mais recomendado):

        cd /pasta_do_seu_projeto
        pyenv local 3.14.0

    Isso cria um .python-version na pasta e ativa automaticamente quando você entrar nela.


6) Criar ambientes virtuais com Pyenv + Pyenv-Virtualenv

        pyenv virtualenv 3.14.0 venv314
        pyenv activate venv314

    Ativar:

        pyenv activate venv314

    Desativar:

        pyenv deactivate

