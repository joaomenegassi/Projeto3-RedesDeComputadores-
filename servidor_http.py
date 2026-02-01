import socket
import threading
import os

# Configurações do Servidor
HOST = '127.0.0.1'
PORTA = 8080 
PASTA_SITE = "site_arquivos" # Pasta onde ficarão os HTML e imagens

def obter_content_type(nome_arquivo):
    """Retorna o tipo MIME baseado na extensão do arquivo."""
    if nome_arquivo.endswith(".html") or nome_arquivo.endswith(".htm"):
        return "text/html"
    elif nome_arquivo.endswith(".jpg") or nome_arquivo.endswith(".jpeg"):
        return "image/jpeg"
    elif nome_arquivo.endswith(".png"):
        return "image/png"
    else:
        return "application/octet-stream"

def lidar_com_cliente_http(conn, addr):
    print(f"[NOVA CONEXÃO] {addr} conectado.")
    
    try:
        requisicao = conn.recv(4096).decode('utf-8')
        
        if not requisicao:
            return

        primeira_linha = requisicao.split('\n')[0]
        print(f"[{addr}] Requisitou: {primeira_linha}")
        
        try:
            metodo, caminho, versao = primeira_linha.split()
        except ValueError:
            return 

        if metodo != 'GET':
            return

        if caminho == '/':
            caminho = '/index.html'

        caminho_arquivo = caminho.lstrip('/')
        
        path_completo = os.path.join(PASTA_SITE, caminho_arquivo)

        if os.path.exists(path_completo) and os.path.isfile(path_completo):
            with open(path_completo, 'rb') as f:
                conteudo = f.read()
            
            tipo_arquivo = obter_content_type(path_completo)
            tamanho = len(conteudo)

            cabecalho = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: {tipo_arquivo}\r\n"
                f"Content-Length: {tamanho}\r\n"
                f"Connection: close\r\n"
                f"\r\n" 
            )
            
            conn.sendall(cabecalho.encode('utf-8') + conteudo)
            print(f"[{addr}] Enviado 200 OK para {caminho}")

        else:
            conteudo_erro = "<h1>404 - Arquivo Nao Encontrado</h1><p>O recurso solicitado nao existe no servidor.</p>"
            cabecalho = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(conteudo_erro)}\r\n"
                "Connection: close\r\n"
                "\r\n"
            )
            conn.sendall(cabecalho.encode('utf-8') + conteudo_erro.encode('utf-8'))
            print(f"[{addr}] Enviado 404 Not Found para {caminho}")

    except Exception as e:
        print(f"[ERRO] {addr}: {e}")
    finally:
        conn.close()

def iniciar_servidor():
    if not os.path.exists(PASTA_SITE):
        os.makedirs(PASTA_SITE)
        print(f"[INFO] Pasta '{PASTA_SITE}' criada. Coloque seus HTMLs e JPEGs lá.")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORTA))
        server_socket.listen(5) # Número de conexões na fila de espera
        print(f"[SERVIDOR HTTP] Rodando em http://{HOST}:{PORTA}")
        print(f"[DIRETÓRIO] Servindo arquivos da pasta: {PASTA_SITE}")

        while True:
            conn, addr = server_socket.accept()
            # Multithreading: cria uma thread para cada requisição (aba do navegador)
            thread = threading.Thread(target=lidar_com_cliente_http, args=(conn, addr))
            thread.start()
            
    except KeyboardInterrupt:
        print("\n[PARANDO] Servidor encerrado.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    iniciar_servidor()