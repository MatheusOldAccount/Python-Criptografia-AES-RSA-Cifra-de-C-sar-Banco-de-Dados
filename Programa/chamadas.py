import Programa.functions_rsa
from Programa.functions_cipher_cesar import decrypt, encrypt
from Programa.sustentabilidade import menu, menu2
import Programa.functions_aes
import time
import os
import pymysql.cursors


def processamento():
    conexao = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='Criptografia',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with conexao.cursor() as banco:
            banco.execute('select * from senha')
            resultado = banco.fetchall()
    except:
        print('\033[31mNão foi possível acessar o banco de dados\033[m')
        exit()
    else:
        continuar = False
        key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
        obj = Programa.functions_aes.Criptografia(key)
        if len(resultado) != 0:
            while True:
                senha = menu()
                if resultado[0]['senha'] == senha:
                    continuar = True
                    break
                else:
                    print('\033[31mSenha incorreta.\033[m')
        else:
            Programa.functions_aes.limpa_tela()
            senha = menu2()
            try:
                with conexao.cursor() as banco:
                    banco.execute(f'insert into senha (senha) values ("{senha}")')
                    conexao.commit()
            except:
                print('\033[31mNão foi possível acessar o banco de dados\033[m')
                exit()
            else:
                print("Por favor, reinicie o programa para concluir a confirmação dos dados.")
                time.sleep(15)
                exit()
        if continuar:
            while True:
                try:
                    tipocript = int(input('Deseja utilizar a Cifra de César (1), o RSA (2) ou o AES (3)? '))
                except (ValueError, TypeError):
                    print('\033[31mTipo de dados digitados errados ! Esperava-se um tipo inteiro digitado. \033[m')
                except KeyboardInterrupt:
                    print('\033[31mUsuário preferiu não informar os dados !\033[m')
                    exit()
                except Exception as motivo_erro:
                    print(f'\033[31mErro: {motivo_erro} \033[m')
                else:
                    if tipocript == 1 or tipocript == 2 or tipocript == 3:
                        break
                    else:
                        print('\033[31mOpção Inválida !\033[m')
            if tipocript == 1:
                while True:
                    try:
                        option = str(input('Deseja criptografar ou decriptografar uma mensagem? [C/D] ')).strip().upper()[0]
                        if option in 'CD':
                            break
                        else:
                            print('\033[31mOpção escolhida inválida! Escolha a opção correta, digitando [C/D]\033[m')
                    except:
                        print('\033[31mOpção escolhida inválida! Por favor, escolha a opção correta, digitando [C/D]\033[m')
                try:
                    rot = int(input('Em quantas casas deseja rotacionar a criptografia? '))
                    message = str(input('Mensagem: ')).strip()
                except (ValueError, TypeError):
                    print('\033[31mForam encontrados erros com os tipos de dados digitados!\033[m')
                except KeyboardInterrupt:
                    print('\033[31mUsuário preferiu não informar os dados! \033[m')
                except Exception as error:
                    print(f'\033[31mO erro encontrado foi \'{error}\'\033[m')
                else:
                    arq = open('cifra_de_cesar.txt', 'w')
                    if option == 'C':
                        arq.write(f'Cifragem de \'{message}\' rotacionando {rot} casas é \'{encrypt(message, rot)}\'')
                    else:
                        arq.write(f'Decifragem de \'{message}\' rotacionando {rot} casas é \'{decrypt(message, rot)}\'')
                    arq.close()
                    print('\033[35mResultado adicionado ao arquivo!\033[m')
            elif tipocript == 2:
                while True:
                    try:
                        opc = str(input('Deseja Criptografar ou Decriptografar uma mensagem? [C/D]: ')).strip().upper()[0]
                        if opc == 'C' or opc == 'D':
                            break
                        else:
                            print(f'\033[31mOpção Inválida! Por favor, escolha novamente.\033[m')
                    except IndexError:
                        print(f'\033[31mErro: Texto vazio ! Por favor, escolha uma opção.\033[m')
                    except Exception as erro:
                        print(f'\033[31mErro: {erro}\033[m')
                Programa.functions_rsa.escolha(opc)
            else:
                Programa.functions_aes.menu(key)
