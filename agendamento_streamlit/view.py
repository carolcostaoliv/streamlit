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

    def servicos_listar():
        return ServicoDAO.listar()
    
    def Servico_inserir(nome, email):
        servico = Servico(0, nome, email)
        Servico.inserir(servico)

    def servico_atualizar(id, nome, email):
        servico = Servico(id, nome, email)
        ServicoDAO.atualizar(servico)

    def servico_excluir(id):
        ServicoDAO.excluir(id)

