from datetime import datetime
import json
class Servico:
    def __init__(self, id, descricao, valor):
        self.set_id(id)
        self.set_descricao(descricao)
        self.set_valor(valor)

    def set_id(self, id):
        if id < 0: raise ValueError('Id inválido')
        self.__id = id
    def get_id(self):
        return self.__id
    
    def set_descricao(self, descricao):
        if id == ' ': raise ValueError('Descrição inválida')
        self.__descricao = descricao
    def get_descricao(self):
        return self.__descricao

    def set_valor(self, valor):
        if valor == 0: raise ValueError('Valor inválido')
        self.__valor = valor
    def get_valor(self):
        return self.__valor
    
    def __str__(self):
        return f'ID - {self.__id} | DESCRIÇÃO - {self.__descricao} | VALOR - {self.__valor}'
    
    def to_json(self):
        dic = {
            'id':self.__id,
            'descricao':self.__descricao,
            'valor':self.__valor,
        }
        return dic
    
    @staticmethod
    def from_json(dic):
        return Servico(
            dic['id'],
            dic['descricao'],
            dic['valor'],
        )
    

class ServicoDAO:
    __objetos = []

    @classmethod
    def inserir (cls, obj):
        cls.abrir()
        id = 0
        for aux in cls.__objetos:
            if aux.get_id() > id: 
                id = aux.get_id()
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
            with open("servico.json", mode="r") as arquivo:
                list_dic = json.load(arquivo)
                for dic in list_dic:
                    obj = Servico.from_json(dic)
                    cls.__objetos.append(obj)
        except FileNotFoundError:
            pass
    
    @classmethod
    def salvar(cls):
        with open("servico.json", mode="w") as arquivo:
            json.dump(cls.__objetos, arquivo, default = Servico.to_json)