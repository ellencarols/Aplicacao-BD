from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from bson.objectid import ObjectId
from datetime import datetime

def conectar_ao_mongo():
    print("Conectando ao banco de dados MongoDB...")
    MONGO_URI = "mongodb+srv://gustavo:gustavo@clustertestebd.tj8a3w4.mongodb.net/?retryWrites=true&w=majority&appName=ClusterTesteBd"
    DB_NAME = "biblioteca_db_nosql"

    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("Conexao bem-sucedida!")
        db = client[DB_NAME]
        return db
    except ConnectionFailure as e:
        print(f"ERRO FATAL: Nao foi possivel conectar ao MongoDB. {e}")
        return None

def criar_aluno(db, matricula, nome, cpf, status):
    print(f"\n--- Tentando criar aluno: {nome} ---")
    try:
        if db.Aluno.find_one({"matricula": matricula}):
            print(f"ERRO: A matrícula '{matricula}' já está em uso.")
            return None
        if db.Aluno.find_one({"usuario.cpf": cpf}):
            print(f"ERRO: O CPF '{cpf}' já está em uso.")
            return None

        documento = {
            "matricula": matricula,
            "status": status,
            "usuario": {
                "cpf": cpf,
                "nome": nome
            }
        }
        resultado = db.Aluno.insert_one(documento)
        aluno_id = resultado.inserted_id
        print(f"SUCESSO: Aluno criado com ID: {aluno_id}.")
        return aluno_id
    except OperationFailure as e:
        print(f"ERRO ao criar aluno: {e}")
        return None

def ler_todos_alunos(db):
    print("\n--- Consultando todos os alunos ---")
    try:
        alunos = db.Aluno.find({}, {"matricula": 1, "status": 1, "usuario.nome": 1}).sort("usuario.nome", 1)
        lista_alunos = list(alunos)
        if not lista_alunos:
            print("Nenhum aluno encontrado.")
        else:
            for aluno in lista_alunos:
                nome_aluno = aluno.get('usuario', {}).get('nome', 'Nome não informado')
                print(f" 	-> ID: {aluno['_id']}, Matrícula: {aluno['matricula']}, Nome: {nome_aluno}, Status: {aluno['status']}")
    except OperationFailure as e:
        print(f"ERRO ao ler alunos: {e}")

def atualizar_status_aluno(db, id_aluno_str, novo_status):
    print(f"\n--- Tentando atualizar status do aluno ID: {id_aluno_str} ---")
    
    status_validos = ["ATIVO", "TRANCADO", "CONCLUIDO", "CANCELADO"]
    if novo_status not in status_validos:
        print(f"ERRO: Status '{novo_status}' é inválido. Use um de: {', '.join(status_validos)}")
        return

    try:
        filtro = {'_id': ObjectId(id_aluno_str)}
        novos_dados = {'$set': {'status': novo_status}}
        resultado = db.Aluno.update_one(filtro, novos_dados)
        if resultado.matched_count == 0:
            print("AVISO: Nenhum aluno encontrado com o ID fornecido.")
        else:
            print(f"SUCESSO: Aluno atualizado. ({resultado.modified_count} campo(s) modificado(s)).")
    except Exception as e:
        print(f"ERRO ao atualizar aluno: {e}")

def deletar_aluno(db, id_aluno_str):
    print(f"\n--- Tentando deletar aluno ID: {id_aluno_str} ---")
    try:
        resultado = db.Aluno.delete_one({'_id': ObjectId(id_aluno_str)})
        if resultado.deleted_count > 0:
            print(f"SUCESSO: Aluno deletado.")
        else:
            print("AVISO: Nenhum aluno encontrado para deletar.")
    except Exception as e:
        print(f"ERRO ao deletar aluno: {e}")

def criar_secao(db, nome, descricao):
    print(f"\n--- Tentando criar secao: {nome} ---")
    try:
        documento = {"nome": nome, "descricao": descricao}
        resultado = db.Secao.insert_one(documento)
        secao_id = resultado.inserted_id
        print(f"SUCESSO: Secao criada com ID: {secao_id}.")
        return secao_id
    except OperationFailure as e:
        print(f"ERRO ao criar secao: {e}")
        return None

def ler_todas_secoes(db):
    print("\n--- Consultando todas as secoes ---")
    try:
        secoes = db.Secao.find().sort("nome", 1)
        lista_secoes = list(secoes)
        if not lista_secoes:
            print("Nenhuma secao encontrada.")
        else:
            for secao in lista_secoes:
                print(f" 	-> ID: {secao['_id']}, Nome: {secao['nome']}, Descricao: '{secao.get('descricao', '')}'")
    except OperationFailure as e:
        print(f"ERRO ao ler secoes: {e}")

def atualizar_secao(db, id_secao_str, novo_nome, nova_descricao):
    print(f"\n--- Tentando atualizar secao ID: {id_secao_str} ---")
    try:
        filtro = {'_id': ObjectId(id_secao_str)}
        novos_dados = {'$set': {'nome': novo_nome, 'descricao': nova_descricao}}
        resultado = db.Secao.update_one(filtro, novos_dados)
        if resultado.matched_count == 0:
            print("AVISO: Nenhuma secao encontrada com o ID fornecido.")
        else:
            print(f"SUCESSO: Secao atualizada. ({resultado.modified_count} campo(s) modificado(s)).")
    except Exception as e:
        print(f"ERRO ao atualizar secao: {e}")

def deletar_secao(db, id_secao_str):
    print(f"\n--- Tentando deletar secao ID: {id_secao_str} ---")
    try:
        resultado = db.Secao.delete_one({'_id': ObjectId(id_secao_str)})
        if resultado.deleted_count > 0:
            print(f"SUCESSO: Secao deletada.")
        else:
            print("AVISO: Nenhuma secao encontrada para deletar.")
    except Exception as e:
        print(f"ERRO ao deletar secao: {e}")

def criar_titulo_livro(db, nome, idioma, paginas, edicao, editora, isbn, autores_str):
    print(f"\n--- Tentando criar titulo (Livro): {nome} ---")
    try:
        documento = {
            "nome": nome,
            "idioma": idioma,
            "data": datetime.now(),
            "paginas": paginas,
            "edicao": edicao,
            "editora": editora,
            "ISBN": isbn,
            "autores": autores_str,
            "secoes": [],
            "exemplares": [],
            "reservas": []
        }
        resultado = db.Livro.insert_one(documento)
        titulo_id = resultado.inserted_id
        print(f"SUCESSO: Titulo (Livro) criado com ID: {titulo_id}.")
        return titulo_id
    except OperationFailure as e:
        print(f"ERRO ao criar titulo: {e}")
        return None

def ler_todos_titulos(db):
    print("\n--- Consultando todos os titulos ---")
    try:
        titulos = db.Livro.find({}, {"nome": 1, "autores": 1, "edicao": 1}).sort("nome", 1)
        lista_titulos = list(titulos)
        if not lista_titulos:
            print("Nenhum titulo encontrado.")
        else:
            for titulo in lista_titulos:
                autores = titulo.get('autores', 'N/A')
                print(f" 	-> ID: {titulo['_id']}, Nome: {titulo['nome']}, "
                      f"Autores: {autores}, Edicao: {titulo.get('edicao')}")
    except OperationFailure as e:
        print(f"ERRO ao ler titulos: {e}")

def atualizar_titulo(db, id_titulo_str, novos_dados):
    print(f"\n--- Tentando atualizar titulo ID: {id_titulo_str} ---")
    
    if not novos_dados:
        print("Nenhuma alteração fornecida.")
        return

    try:
        filtro = {'_id': ObjectId(id_titulo_str)}
        operacao_update = {'$set': novos_dados}
        
        resultado = db.Livro.update_one(filtro, operacao_update)
        
        if resultado.matched_count == 0:
            print("AVISO: Nenhum titulo encontrado com o ID fornecido.")
        else:
            if resultado.modified_count > 0:
                print(f"SUCESSO: Titulo atualizado. ({resultado.modified_count} campo(s) modificado(s)).")
            else:
                print("AVISO: Nenhuma alteração foi realizada (os dados fornecidos podem ser iguais aos existentes).")
    except Exception as e:
        print(f"ERRO ao atualizar titulo: {e}")

def deletar_titulo(db, id_titulo_str):
    print(f"\n--- Tentando deletar titulo ID: {id_titulo_str} ---")
    try:
        resultado = db.Livro.delete_one({'_id': ObjectId(id_titulo_str)})
        if resultado.deleted_count > 0:
            print(f"SUCESSO: Titulo deletado.")
        else:
            print("AVISO: Nenhum titulo encontrado para deletar.")
    except Exception as e:
        print(f"ERRO ao deletar titulo: {e}")

def menu_principal():
    print("\n==================== MENU PRINCIPAL (NoSQL) ====================")
    print("1. Gerenciar Alunos")
    print("2. Gerenciar Secoes")
    print("3. Gerenciar Titulos ")
    print("0. Sair")
    return input("Escolha uma opcao: ")

def gerenciar_alunos(db):
    while True:
        print("\n--- Gerenciar Alunos ---")
        print("1. Criar novo aluno")
        print("2. Listar todos os alunos")
        print("3. Atualizar status de um aluno")
        print("4. Deletar um aluno")
        print("9. Voltar ao menu principal")
        opcao = input("Escolha uma opcao: ")

        try:
            if opcao == '1':
                matricula = input("Matrícula do aluno: ")
                nome = input("Nome completo do aluno: ")
                cpf = input("CPF do aluno (11 digitos, sem pontos): ")
                status = input("Status do aluno (ATIVO, TRANCADO, CONCLUIDO, CANCELADO): ").upper()
                criar_aluno(db, matricula, nome, cpf, status)
            elif opcao == '2':
                ler_todos_alunos(db)
            elif opcao == '3':
                id_aluno = input("ID do aluno a ser atualizado: ")
                novo_status = input("Novo status (ATIVO, TRANCADO, CONCLUIDO, CANCELADO): ").upper()
                atualizar_status_aluno(db, id_aluno, novo_status)
            elif opcao == '4':
                id_aluno = input("ID do aluno a ser deletado: ")
                deletar_aluno(db, id_aluno)
            elif opcao == '9':
                break
            else:
                print("Opcao invalida. Tente novamente.")
        except ValueError:
            print("ERRO: Entrada invalida.")
        except Exception as e:
            print(f"Um erro inesperado ocorreu: {e}")

def gerenciar_secoes(db):
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
                descricao = input("Descricao da secao: ")
                criar_secao(db, nome, descricao)
            elif opcao == '2':
                ler_todas_secoes(db)
            elif opcao == '3':
                id_secao = input("ID da secao a ser atualizada: ")
                novo_nome = input("Novo nome da secao: ")
                nova_descricao = input("Nova descricao da secao: ")
                atualizar_secao(db, id_secao, novo_nome, nova_descricao)
            elif opcao == '4':
                id_secao = input("ID da secao a ser deletada: ")
                deletar_secao(db, id_secao)
            elif opcao == '9':
                break
            else:
                print("Opcao invalida. Tente novamente.")
        except Exception as e:
            print(f"Um erro inesperado ocorreu: {e}")

def gerenciar_titulos(db):
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
                autores_str = input("Autor(es) (pode ser mais de um, separado por vírgula): ")
                idioma = input("Idioma: ")
                paginas = int(input("Numero de paginas: "))
                edicao = int(input("Edicao: "))
                editora = input("Editora: ")
                isbn = input("ISBN (13 digitos): ")
                criar_titulo_livro(db, nome, idioma, paginas, edicao, editora, isbn, autores_str)
            
            elif opcao == '2':
                ler_todos_titulos(db)
            
            elif opcao == '3':
                id_titulo = input("ID do titulo a ser atualizado: ")
                
                try:
                    livro_atual = db.Livro.find_one({'_id': ObjectId(id_titulo)})
                except Exception:
                    livro_atual = None

                if not livro_atual:
                    print("ERRO: Livro não encontrado com o ID fornecido.")
                    continue

                print("\n--- Editando o Livro: '{}' ---".format(livro_atual.get('nome')))
                print("(Pressione Enter para manter a informação atual)")

                novo_nome = input(f"Nome atual: [{livro_atual.get('nome', '')}] -> Novo nome: ")
                novos_autores = input(f"Autores atuais: [{livro_atual.get('autores', '')}] -> Novos autores: ")
                novo_idioma = input(f"Idioma atual: [{livro_atual.get('idioma', '')}] -> Novo idioma: ")
                novas_paginas_str = input(f"Páginas atuais: [{livro_atual.get('paginas', '')}] -> Novas páginas: ")
                nova_edicao_str = input(f"Edição atual: [{livro_atual.get('edicao', '')}] -> Nova edição: ")
                nova_editora = input(f"Editora atual: [{livro_atual.get('editora', '')}] -> Nova editora: ")
                novo_isbn = input(f"ISBN atual: [{livro_atual.get('ISBN', '')}] -> Novo ISBN: ")
                
                dados_para_atualizar = {}
                if novo_nome:
                    dados_para_atualizar['nome'] = novo_nome
                if novos_autores:
                    dados_para_atualizar['autores'] = novos_autores
                if novo_idioma:
                    dados_para_atualizar['idioma'] = novo_idioma
                if novas_paginas_str:
                    dados_para_atualizar['paginas'] = int(novas_paginas_str)
                if nova_edicao_str:
                    dados_para_atualizar['edicao'] = int(nova_edicao_str)
                if nova_editora:
                    dados_para_atualizar['editora'] = nova_editora
                if novo_isbn:
                    dados_para_atualizar['ISBN'] = novo_isbn

                atualizar_titulo(db, id_titulo, dados_para_atualizar)

            elif opcao == '4':
                id_titulo = input("ID do titulo a ser deletado: ")
                deletar_titulo(db, id_titulo)
            
            elif opcao == '9':
                break
            
            else:
                print("Opcao invalida. Tente novamente.")
        except ValueError:
            print("ERRO: Entrada invalida. Por favor, insira numeros onde for solicitado (páginas, edição).")
        except Exception as e:
            print(f"Um erro inesperado ocorreu: {e}")

def main():
    db = conectar_ao_mongo()
    
    if db is None:
        print("\nNao foi possivel estabelecer conexao com o banco de dados. O programa sera encerrado.")
        return 

    while True:
        opcao = menu_principal()
        if opcao == '1':
            gerenciar_alunos(db)
        elif opcao == '2':
            gerenciar_secoes(db)
        elif opcao == '3':
            gerenciar_titulos(db)
        elif opcao == '0':
            print("Saindo do programa...")
            break
        else:
            print("Opcao invalida. Tente novamente.")

    if db and db.client:
        db.client.close()
        print("\nConexao com o MongoDB foi fechada.")


if __name__ == "__main__":
    main()
