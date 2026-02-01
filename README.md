# Projeto 3: Servidor Web HTTP Multithread com Sockets TCP

Este projeto consiste na implementação de um servidor web básico desenvolvido em **Python**, utilizando a biblioteca `socket` para comunicação em rede e `threading` para suportar múltiplas conexões simultâneas. O servidor é capaz de processar requisições HTTP GET, servir arquivos estáticos (HTML e Imagens) e gerenciar erros de recurso não encontrado (404).

## Funcionalidades

* **Comunicação TCP:** Utiliza sockets AF_INET e SOCK_STREAM para garantir a entrega confiável dos dados.
* **Protocolo HTTP:** Processamento manual de cabeçalhos HTTP/1.1.
* **Multithreading:** Capacidade de atender múltiplos clientes (abas do navegador) simultaneamente através de threads independentes.
* **Suporte a Tipos MIME:** Identificação automática de arquivos `.html`, `.jpg`, `.jpeg` e `.png`.
* **Tratamento de Erros:** Resposta customizada para erro 404 (Not Found).

## Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Bibliotecas Nativas:** `socket`, `threading`, `os`
* **Frontend:** HTML5 básico para testes de renderização.
