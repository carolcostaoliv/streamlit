import json

class Cliente:

    def __init__(self, id, nome, email, fone, senha):
        self.__id = id
        self.__nome = nome
        self.__email = email
        self.__fone = fone
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


    def __str__(self):
        return f"{self.__id} - {self.__nome} | {self.__email} | {self.__fone}"

    def to_json(self):
        dic = {"id":self.__id, "nome":self.__nome,"email":self.__email, "fone":self.__fone, "senha": self.__senha}
        return dic

    @staticmethod
    def from_json(dic):
        return Cliente(dic["id"], dic["nome"], dic["email"], dic["fone"], dic["senha"])

import json

class ClienteDAO:
    __objetos = []
    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        id = 0

        for aux in cls.__objetos:
            if aux.get_id() > id: id = aux.get_id()
        obj.set_id(id + 1)

        cls.__objetos.append(obj)
        cls.salvar()
    @classmethod
    def listar(cls):
        cls.abrir()
        return cls.__objetos

    @classmethod
    def listar_id(cls, id):
        cls.abrir()
        for obj in cls.__objetos:
            if obj.get_id() == id: return obj
        return None

    @classmethod
    def atualizar(cls, obj):
        aux = cls.listar_id(obj.get_id())
        if aux != None:
            cls.__objetos.remove(aux)
            cls.__objetos.append(obj)
            cls.salvar()

    @classmethod
    def excluir(cls, obj):
        aux = cls.listar_id(obj.get_id())
        if aux != None:
            cls.__objetos.remove(aux)
            cls.salvar()

    @classmethod
    def abrir(cls):
        cls.__objetos = []
        try: 
            with open("clientes.json", mode="r") as arquivo: 
                list_dic = json.load(arquivo)
                for dic in list_dic:
                    obj = Cliente.from_json(dic)
                    cls.__objetos.append(obj)
        except FileNotFoundError:
            pass

    @classmethod
    def salvar(cls):
        with open("clientes.json", mode="w") as arquivo:
            json.dump(cls.__objetos, arquivo, default = Cliente.to_json)