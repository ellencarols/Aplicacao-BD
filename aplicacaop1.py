import psycopg2
from datetime import date

# 1. CONFIGURACAO DA CONEXAO
def conectar_ao_banco():
    """Conecta ao banco de dados PostgreSQL e retorna o objeto de conexao."""
    print("Conectando ao banco de dados...")
    try:
        conn = psycopg2.connect(
            host='banco-da-ellen.csoujpxglswu.us-east-1.rds.amazonaws.com',
            port='5432',
            dbname='biblioteca_db',
            user='professor',
            password='professor'
        )
        print("Conexao bem-sucedida!")
        return conn
    except psycopg2.OperationalError as e:
        print(f"ERRO FATAL: Nao foi possivel conectar. {e}")
        return None

# --- FUNCOES CRUD PARA A TABELA 'Autor' ---
def criar_autor(conn, nome_completo, ano_nascimento, pais):
    """Insere um novo autor e retorna o ID gerado."""
    print(f"\n--- Tentando criar autor: {nome_completo} ---")
    autor_id = None
    try:
        with conn.cursor() as cur:
            query = 'INSERT INTO "Biblioteca".Autor (nome_completo, ano_de_nascimento, pais) VALUES (%s, %s, %s) RETURNING idAutor;'
            cur.execute(query, (nome_completo, ano_nascimento, pais))
            autor_id = cur.fetchone()[0]
        conn.commit()
        print(f"SUCESSO: Autor criado com ID: {autor_id}.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"ERRO ao criar autor: {e}")
    return autor_id

def ler_todos_autores(conn):
    """Le e exibe todos os autores da tabela."""
    print("\n--- Consultando todos os autores ---")
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT idAutor, nome_completo, pais FROM "Biblioteca".Autor ORDER BY nome_completo;')
            resultados = cur.fetchall()
            if not resultados:
                print("Nenhum autor encontrado.")
            else:
                for row in resultados:
                    print(f"  -> ID: {row[0]}, Nome: {row[1]}, Pais: {row[2]}")
    except psycopg2.Error as e:
        print(f"ERRO ao ler autores: {e}")

def atualizar_autor(conn, id_autor, novo_nome, novo_pais):
    """(UPDATE) Atualiza o nome e o pais de um autor especifico."""
    print(f"\n--- Tentando atualizar autor ID: {id_autor} ---")
    try:
        with conn.cursor() as cur:
            query = 'UPDATE "Biblioteca".Autor SET nome_completo = %s, pais = %s WHERE idAutor = %s;'
            cur.execute(query, (novo_nome, novo_pais, id_autor))
        conn.commit()
        if cur.rowcount == 0:
            print("AVISO: Nenhum autor encontrado com o ID fornecido.")
        else:
            print(f"SUCESSO: Autor atualizado.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"ERRO ao atualizar autor: {e}")

def deletar_autor(conn, id_autor):
    """Deleta um autor especifico pelo ID."""
    print(f"\n--- Tentando deletar autor ID: {id_autor} ---")
    try:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM "Biblioteca".Autor WHERE idAutor = %s;', (id_autor,))
        conn.commit()
        if cur.rowcount > 0:
            print(f"SUCESSO: Autor deletado.")
        else:
            print("AVISO: Nenhum autor encontrado para deletar.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"ERRO ao deletar autor: {e}")

# --- FUNCOES CRUD PARA A TABELA 'Secao' ---
def criar_secao(conn, nome, descricao):
    """Insere uma nova secao e retorna o ID gerado."""
    print(f"\n--- Tentando criar secao: {nome} ---")
    secao_id = None
    try:
        with conn.cursor() as cur:
            query = 'INSERT INTO "Biblioteca".Secao (nome, descricao) VALUES (%s, %s) RETURNING idSecao;'
            cur.execute(query, (nome, descricao))
            secao_id = cur.fetchone()[0]
        conn.commit()
        print(f"SUCESSO: Secao criada com ID: {secao_id}.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"ERRO ao criar secao: {e}")
    return secao_id

def ler_todas_secoes(conn):
    """Le e exibe todas as secoes da tabela."""
    print("\n--- Consultando todas as secoes ---")
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT idSecao, nome, descricao FROM "Biblioteca".Secao ORDER BY nome;')
            resultados = cur.fetchall()
            if not resultados:
                print("Nenhuma secao encontrada.")
            else:
                for row in resultados:
                    print(f"  -> ID: {row[0]}, Nome: {row[1]}, Descricao: '{row[2]}'")
    except psycopg2.Error as e:
        print(f"ERRO ao ler secoes: {e}")

def atualizar_secao(conn, id_secao, novo_nome, nova_descricao):
    """(UPDATE) Atualiza o nome e a descricao de uma secao especifica."""
    print(f"\n--- Tentando atualizar secao ID: {id_secao} ---")
    try:
        with conn.cursor() as cur:
            query = 'UPDATE "Biblioteca".Secao SET nome = %s, descricao = %s WHERE idSecao = %s;'
            cur.execute(query, (novo_nome, nova_descricao, id_secao))
        conn.commit()
        if cur.rowcount == 0:
            print("AVISO: Nenhuma secao encontrada com o ID fornecido.")
        else:
            print(f"SUCESSO: Secao atualizada.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"ERRO ao atualizar secao: {e}")

def deletar_secao(conn, id_secao):
    """Deleta uma secao especifica pelo ID."""
    print(f"\n--- Tentando deletar secao ID: {id_secao} ---")
    try:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM "Biblioteca".Secao WHERE idSecao = %s;', (id_secao,))
        conn.commit()
        if cur.rowcount > 0:
            print(f"SUCESSO: Secao deletada.")
        else:
            print("AVISO: Nenhuma secao encontrada para deletar.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"ERRO ao deletar secao: {e}")

# --- FUNCOES CRUD PARA A TABELA 'Titulo' ---
def criar_titulo(conn, nome, idioma, paginas, edicao):
    """Insere um novo titulo e retorna o ID gerado."""
    print(f"\n--- Tentando criar titulo: {nome} ---")
    titulo_id = None
    try:
        with conn.cursor() as cur:
            query = "INSERT INTO \"Biblioteca\".Titulo (nome, idioma, data, paginas, edicao) VALUES (%s, %s, %s, %s, %s) RETURNING idTitulo;"
            cur.execute(query, (nome, idioma, date.today(), paginas, edicao))
            titulo_id = cur.fetchone()[0]
        conn.commit()
        print(f"SUCESSO: Titulo criado com ID: {titulo_id}.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"ERRO ao criar titulo: {e}")
    return titulo_id

def ler_todos_titulos(conn):
    """Le e exibe todos os titulos da tabela."""
    print("\n--- Consultando todos os titulos ---")
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT idTitulo, nome, paginas, edicao, volume FROM "Biblioteca".Titulo ORDER BY nome;')
            resultados = cur.fetchall()
            if not resultados:
                print("Nenhum titulo encontrado.")
            else:
                for row in resultados:
                    print(f"  -> ID: {row[0]}, Nome: {row[1]}, Paginas: {row[2]}, Edicao: {row[3]}, Volume: {row[4]}")
    except psycopg2.Error as e:
        print(f"ERRO ao ler titulos: {e}")

def atualizar_titulo(conn, id_titulo, nova_edicao, novo_volume):
    """(UPDATE) Atualiza a edicao e o volume de um titulo especifico."""
    print(f"\n--- Tentando atualizar titulo ID: {id_titulo} ---")
    try:
        with conn.cursor() as cur:
            query = 'UPDATE "Biblioteca".Titulo SET edicao = %s, volume = %s WHERE idTitulo = %s;'
            cur.execute(query, (nova_edicao, novo_volume, id_titulo))
        conn.commit()
        if cur.rowcount == 0:
            print("AVISO: Nenhum titulo encontrado com o ID fornecido.")
        else:
            print(f"SUCESSO: Titulo atualizado.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"ERRO ao atualizar titulo: {e}")

def deletar_titulo(conn, id_titulo):
    """Deleta um titulo especifico pelo ID."""
    print(f"\n--- Tentando deletar titulo ID: {id_titulo} ---")
    try:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM "Biblioteca".Titulo WHERE idTitulo = %s;', (id_titulo,))
        conn.commit()
        if cur.rowcount > 0:
            print(f"SUCESSO: Titulo deletado.")
        else:
             print("AVISO: Nenhum titulo encontrado para deletar.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"ERRO ao deletar titulo: {e}")
        
# --- FUNCOES CRUD PARA A TABELA 'Escreve' ---
def criar_associacao_autor_titulo(conn, id_autor, id_titulo):
    """Cria uma associacao entre um autor e um titulo."""
    print(f"\n--- Tentando associar Autor ID {id_autor} com Titulo ID {id_titulo} ---")
    try:
        with conn.cursor() as cur:
            query = 'INSERT INTO "Biblioteca".Escreve (Autor_idAutor, Titulo_idTitulo) VALUES (%s, %s);'
            cur.execute(query, (id_autor, id_titulo))
        conn.commit()
        print("SUCESSO: Associacao criada.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"ERRO ao criar associacao: {e}")

def ler_associacoes(conn):
    """Le e exibe todas as associacoes 'Autor escreve Titulo'."""
    print("\n--- Consultando associacoes ---")
    try:
        with conn.cursor() as cur:
            query = """
                SELECT a.idAutor, a.nome_completo, t.idTitulo, t.nome FROM "Biblioteca".Escreve AS e
                JOIN "Biblioteca".Autor AS a ON e.Autor_idAutor = a.idAutor
                JOIN "Biblioteca".Titulo AS t ON e.Titulo_idTitulo = t.idTitulo;
            """
            cur.execute(query)
            resultados = cur.fetchall()
            if not resultados:
                print("Nenhuma associacao encontrada.")
            else:
                for row in resultados:
                    print(f"  -> [Autor ID: {row[0]}] {row[1]} <-> [Titulo ID: {row[2]}] {row[3]}")
    except psycopg2.Error as e:
        print(f"ERRO ao ler associacoes: {e}")

def deletar_associacao_autor_titulo(conn, id_autor, id_titulo):
    """Deleta uma associacao especifica."""
    print(f"\n--- Tentando deletar associacao entre Autor ID {id_autor} e Titulo ID {id_titulo} ---")
    try:
        with conn.cursor() as cur:
            query = 'DELETE FROM "Biblioteca".Escreve WHERE Autor_idAutor = %s AND Titulo_idTitulo = %s;'
            cur.execute(query, (id_autor, id_titulo))
        conn.commit()
        if cur.rowcount > 0:
            print("SUCESSO: Associacao deletada.")
        else:
            print("AVISO: Nenhuma associacao encontrada para deletar.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"ERRO ao deletar associacao: {e}")

# --- FUNCOES DE INTERFACE E MENUS ---
def menu_principal():
    print("\n==================== MENU PRINCIPAL ====================")
    print("1. Gerenciar Autores")
    print("2. Gerenciar Secoes")
    print("3. Gerenciar Titulos")
    print("4. Gerenciar Associacoes (Autor-Titulo)")
    print("0. Sair")
    return input("Escolha uma opcao: ")

def gerenciar_autores(conn):
    while True:
        print("\n--- Gerenciar Autores ---")
        print("1. Criar novo autor")
        print("2. Listar todos os autores")
        print("3. Atualizar um autor")
        print("4. Deletar um autor")
        print("9. Voltar ao menu principal")
        opcao = input("Escolha uma opcao: ")

        try:
            if opcao == '1':
                nome = input("Nome completo do autor: ")
                ano = int(input("Ano de nascimento: "))
                pais = input("Pais de origem: ")
                criar_autor(conn, nome, ano, pais)
            elif opcao == '2':
                ler_todos_autores(conn)
            elif opcao == '3':
                id_autor = int(input("ID do autor a ser atualizado: "))
                nome = input("Novo nome completo: ")
                pais = input("Novo pais de origem: ")
                atualizar_autor(conn, id_autor, nome, pais)
            elif opcao == '4':
                id_autor = int(input("ID do autor a ser deletado: "))
                deletar_autor(conn, id_autor)
            elif opcao == '9':
                break
            else:
                print("Opcao invalida. Tente novamente.")
        except ValueError:
            print("ERRO: Entrada invalida. Por favor, insira um numero para IDs e anos.")

def gerenciar_secoes(conn):
    while True:
        print("\n--- Gerenciar Secoes ---")
        print("1. Criar nova secao")
        print("2. Listar todas as secoes")
        print("3. Atualizar uma secao")
        print("4. Deletar uma secao")
        print("9. Voltar ao menu principal")
        opcao = input("Escolha uma opcao: ")

        try:
            if opcao == '1':
                nome = input("Nome da secao: ")
                desc = input("Descricao da secao: ")
                criar_secao(conn, nome, desc)
            elif opcao == '2':
                ler_todas_secoes(conn)
            elif opcao == '3':
                id_secao = int(input("ID da secao a ser atualizada: "))
                nome = input("Novo nome: ")
                desc = input("Nova descricao: ")
                atualizar_secao(conn, id_secao, nome, desc)
            elif opcao == '4':
                id_secao = int(input("ID da secao a ser deletada: "))
                deletar_secao(conn, id_secao)
            elif opcao == '9':
                break
            else:
                print("Opcao invalida. Tente novamente.")
        except ValueError:
            print("ERRO: Entrada invalida. Por favor, insira um numero para IDs.")

def gerenciar_titulos(conn):
    while True:
        print("\n--- Gerenciar Titulos ---")
        print("1. Criar novo titulo")
        print("2. Listar todos os titulos")
        print("3. Atualizar um titulo")
        print("4. Deletar um titulo")
        print("9. Voltar ao menu principal")
        opcao = input("Escolha uma opcao: ")

        try:
            if opcao == '1':
                nome = input("Nome do titulo: ")
                idioma = input("Idioma: ")
                paginas = int(input("Numero de paginas: "))
                edicao = int(input("Edicao: "))
                criar_titulo(conn, nome, idioma, paginas, edicao)
            elif opcao == '2':
                ler_todos_titulos(conn)
            elif opcao == '3':
                id_titulo = int(input("ID do titulo a ser atualizado: "))
                edicao = int(input("Nova edicao: "))
                volume = int(input("Novo volume: "))
                atualizar_titulo(conn, id_titulo, edicao, volume)
            elif opcao == '4':
                id_titulo = int(input("ID do titulo a ser deletado: "))
                deletar_titulo(conn, id_titulo)
            elif opcao == '9':
                break
            else:
                print("Opcao invalida. Tente novamente.")
        except ValueError:
            print("ERRO: Entrada invalida. Por favor, insira numeros onde for solicitado.")

def gerenciar_associacoes(conn):
    while True:
        print("\n--- Gerenciar Associacoes (Autor escreve Titulo) ---")
        print("1. Criar nova associacao")
        print("2. Listar todas as associacoes")
        print("3. Deletar uma associacao")
        print("9. Voltar ao menu principal")
        opcao = input("Escolha uma opcao: ")

        try:
            if opcao == '1':
                ler_todos_autores(conn)
                id_autor = int(input("ID do Autor para associar: "))
                ler_todos_titulos(conn)
                id_titulo = int(input("ID do Titulo para associar: "))
                criar_associacao_autor_titulo(conn, id_autor, id_titulo)
            elif opcao == '2':
                ler_associacoes(conn)
            elif opcao == '3':
                ler_associacoes(conn)
                id_autor = int(input("ID do Autor da associacao a deletar: "))
                id_titulo = int(input("ID do Titulo da associacao a deletar: "))
                deletar_associacao_autor_titulo(conn, id_autor, id_titulo)
            elif opcao == '9':
                break
            else:
                print("Opcao invalida. Tente novamente.")
        except ValueError:
            print("ERRO: Entrada invalida. Por favor, insira um numero para IDs.")

# --- BLOCO DE EXECUCAO PRINCIPAL ---
def main():
    conexao = conectar_ao_banco()
    if not conexao:
        return

    while True:
        opcao = menu_principal()
        if opcao == '1':
            gerenciar_autores(conexao)
        elif opcao == '2':
            gerenciar_secoes(conexao)
        elif opcao == '3':
            gerenciar_titulos(conexao)
        elif opcao == '4':
            gerenciar_associacoes(conexao)
        elif opcao == '0':
            print("Saindo do programa...")
            break
        else:
            print("Opcao invalida. Tente novamente.")

    conexao.close()
    print("\nConexao com o PostgreSQL foi fechada.")

if __name__ == "__main__":
    main()

