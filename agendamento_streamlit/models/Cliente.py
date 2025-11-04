import json
from models.dao import DAO

class Cliente:

    def __init__(self, id, nome, email, fone, senha, observacoes=""):
        self.__id = id
        self.__nome = nome
        self.__email = email
        self.__fone = fone
        self.__observacoes = observacoes  
        self.set_senha(senha)

    def get_senha(self): return self.__senha
    def set_senha(self, senha): self.__senha = senha

    def set_id(self, id):
        if id < 0: raise ValueError ("ID inválido")
        self.__id = id
    def get_id(self):
        return self.__id

    def set_nome(self, nome):
        if nome == "": raise ValueError ("Nome inválido")
        self.__nome = nome
    def get_nome(self):
        return self.__nome

    def set_email(self, email):
        if email =="": raise ValueError ("E-mail inválido")
        self.__email = email
    def get_email(self):
        return self.__email

    def set_fone(self, fone):
        if fone == "": raise ValueError ("Telefone inválido")
        self.__fone = fone
    def get_fone(self):
        return self.__fone


    def set_observacoes(self, observacoes):
        self.__observacoes = observacoes
    def get_observacoes(self):
        return self.__observacoes

    def __str__(self):
        return f"{self.__id} - {self.__nome} | {self.__email} | {self.__fone}"

    def to_json(self):
        dic = {
            "id": self.__id, 
            "nome": self.__nome,
            "email": self.__email, 
            "fone": self.__fone, 
            "senha": self.__senha,
            "observacoes": self.__observacoes  
        }
        return dic

    @staticmethod
    def from_json(dic):
        observacoes = dic.get("observacoes", "") 
        return Cliente(
            dic["id"], dic["nome"], dic["email"], 
            dic["fone"], dic["senha"], observacoes 
        )

class ClienteDAO(DAO):  
    @classmethod
    def abrir(cls):
        cls._objetos = []
        try:
            with open("clientes.json", mode ="r") as arquivo: 
                list_dic = json.load(arquivo)
                for dic in list_dic:
                    obj = Cliente.from_json(dic) 
                    cls._objetos.append(obj)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError: 
            pass

    @classmethod
    def salvar(cls):
        with open("clientes.json", mode ="w") as arquivo:
            json.dump(cls._objetos, arquivo, default = Cliente.to_json, indent=4) 