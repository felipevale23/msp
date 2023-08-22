# Método da Soma de Potência
Algorítimo em Python para o Método da Soma de Potência na distribuição de energia elétrica.

Para criar um ambiente virtual, vá para o diretório do seu projeto e execute:

No Unix:

``` shell
    $ python3 -m venv msp
```
No Windows:

Primeiro habilitando scripts de terceiros.

Poweshell:
``` shell
    > Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
Powershell

``` shell
    > py -m venv msp
```

> Note que você deve excluir seu diretório de ambiente virtual de seu sistema de controle de versão usando .gitignore ou similar.

Para começar a usar o ambiente no console, você deve ativá-lo

No Unix:

``` shell
	$ source msp/bin/activate
```

On Windows:

```shell
	> .\msp\Scripts\activate
```

Veja a parte de como você verifica se está no ambiente (usando which (linux, unix) ou where (windows)!

**Para desativar**  basta rodar:

```shell
	$ deactivate
```

## Dependências

[Documentação do Pip](https://pip.pypa.io/en/latest/user_guide/#requirements-files)

> “Requirements files” are files containing a list of dependencies to be installed using pip install like so

(**How to Install requirements files**)

```shell
	$ pip3 install -r requirements.txt
```

> Requirements files are used to hold the result from pip freeze for the purpose of achieving repeatable installations. In this case, your requirement file  **contains a pinned version of everything that was installed**  when  **pip freeze**  was  **run**.

```shell
	$ python3 -m pip3 freeze > requirements.txt
	$ python3 -m pip3 install -r requirements.txt
```
