from models.Cliente import Cliente, ClienteDAO
from models.Servico import Servico, ServicoDAO

class View:
    def cliente_listar():
        return ClienteDAO.listar()
    def cliente_inserir(nome, email, fone):
        cliente = Cliente(0, nome, email, fone)
        ClienteDAO.inserir(cliente)

    def cliente_atualizar(id, nome, email, fone):
        cliente = Cliente(id, nome, email, fone)
        ClienteDAO.atualizar(cliente)

    def cliente_excluir(id):
        cliente = Cliente(id, "", "", "")
        ClienteDAO.excluir(cliente)

    @staticmethod
    def Servico_inserir(descricao, valor):
        servico = Servico(0, descricao, valor) 
        ServicoDAO.inserir(servico)

    @staticmethod
    def servicos_listar():
        return ServicoDAO.listar()
    
    @staticmethod
    def servico_atualizar(id, descricao, valor):
        servico = Servico(id, descricao, valor)
        ServicoDAO.atualizar(servico)

    @staticmethod
    def Servico_excluir(id):
        servico = ServicoDAO.listar_id(id)
        if servico:
            ServicoDAO.excluir(servico)
