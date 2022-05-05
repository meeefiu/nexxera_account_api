## Descrição 

Esta API dispõe das seguintes operações:

- Criar contas virtuais;
- Listar todas as contas virtuais;
- Criar transações para um conta virtual;
- Extrato de uma conta virtual;

A descrição completa de cada endpoint pode ser vista no link abaixo.

https://documenter.getpostman.com/view/249665/UyxbrVou

## Execução do projeto

Após clonar este repositório, crie um virtual env e ative-o logo em seguida.

Faça a instalação das dependências com o pip:
`pip install -r requirements.txt`

Rode as migrations com o comando:
`python manage.py migrate`

*\* Este projeto utiliza o banco de dados sqlite, então não precisar fazer nenhum tipo de configuração de banco de dados.*

Rode o projeto com o comando abaixo e pronto!
`python manage.py startserver`

#### Execução dos testes

Este projeto faz uso da biblioteca unittest. Faz uso também da biblioteca coverage para geração das estatísticas de cobertura. 

Rode o comando abaixo para a execução os testes e a geração das estatísticas de cobertura:

`coverage run --source='.' manage.py test core`

Após isso, execute o comando abaixo para visualizar estas estatísticas
`coverage report`