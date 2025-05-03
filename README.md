# ReconApp

O ReconApp é uma ferramenta de reconhecimento baseado em terminal que permite realizar escaneamento de portas, consulta Whois, enumeração DNS, Scan WhatWeb, escaneamento de subdomínios e Scan Wapiti em um domínio alvo.

## Requisitos

Na raiz do repositório, execute o comando abaixo para instalar as bibliotecas utilizadas:

```
pip install -r requirements
```

Além das bibliotecas, caso deseje utilizar as funções de Scan WhatWeb ou Scan Wapiti, eles precisam estar instalados na sua máquina (ou disponíveis via WSL):

```
sudo apt install whatweb
sudo apt install wapiti
```

## Utilização

Clone o repositório, acesse a pasta raiz e execute o arquivo main.py:

```
python main.py
```

Feito isso, você está livre para explorar e utilizar as ferramentas disponíveis no ReconApp.

## Estrutura

```
ReconApp/
│
├── main.py               # Menu principal
├── requirements.txt      # Bibliotecas necessárias
├── modules/              # Módulos com ferramentas
│   ├── auxx/             # Objetos auxiliares (cores, dicionários, etc.)
│   ├── portscanner.py
│   ├── whoislookup.py
│   ├── dnsenumeration.py
│   ├── wapiti.py
│   ├── subdomainscan.py
│   └── whatweb.py
└── outputs/              # Relatórios (Wapiti)
    └── README.md         # Informações sobre a pasta
```