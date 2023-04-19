# MVP-PUCRJ-backend
Backend do projeto 'Controle de Estacionamento'

# API Controle de estacionamento

Esta API realiza o controle de entrada e saída de veículos em um estacionamento.

O usuário deverá preencher todos os dados para registrar o tempo de permanência de um veículo no estacionamento.

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório meu_app_api, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).


```
(env)$ python -m venv venv
```
Este comando prepara o ambiente virtual

```
(env)$ venv/scripts/Activate.ps1
```
Este comando ativa o ambiente virtual

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
