from models.Cliente import Cliente, ClienteDAO
from models.Servico import Servico, ServicoDAO
from models.Horario import Horario, HorarioDAO
from models.Profissional import Profissional, ProfissionalDAO
from datetime import datetime 

class View:   
    @classmethod
    def _validar_email(cls, email):
        for c in View.cliente_listar():
            raise ValueError("Esse e-mail já foi cadastrado")
        for p in View.profissional_listar():
            raise ValueError("Esse e-mail já foi cadastrado")
        if email == "admin":
            raise ValueError ("Esse e-mail já foi cadastrado")


    def cliente_listar():
        return ClienteDAO.listar()
    
    def cliente_listar_id(id):
        return ClienteDAO.listar_id(id)
    
    def cliente_inserir(nome, email, fone, senha):
        cliente = Cliente(0, nome, email, fone, senha) 
        View._validar_email(email) 
        
        ClienteDAO.inserir(cliente)

    def cliente_atualizar(id, nome, email, fone, senha):
        cliente = Cliente(id, nome, email, fone, senha)
        View._validar_email(email, id, 'cliente') 
        ClienteDAO.atualizar(cliente)
        
    def cliente_excluir(id):
        cliente = View.cliente_listar_id(id)
        if cliente and cliente.get_email() == "admin":
            raise ValueError ("O admin não pode ser excluído")
        for h in View.horario_listar():
            if h.get_id_cliente() == id:
                raise ValueError("Não é possivél excluir um cliente com horário agendado")
        ClienteDAO.excluir(id)

    def servico_listar():
        return ServicoDAO.listar()
    
    def servico_listar_id(id):
        return ServicoDAO.listar_id(id)

    def servico_inserir(descricao, valor):
        servico = Servico(0, descricao, valor)
        ServicoDAO.inserir(servico)

    def servico_atualizar(id, descricao, valor):
        servico = Servico(id, descricao, valor)
        ServicoDAO.atualizar(servico)
        
    def servico_excluir(id):
        servico = Servico(id, "0", 1)
        ServicoDAO.excluir(servico)

    def horario_inserir(data, confirmado, id_cliente, id_servico, id_profissional):
        c = Horario(0, data)
        c.set_confirmado(confirmado)
        c.set_id_cliente(id_cliente)
        c.set_id_servico(id_servico)
        c.set_id_profissional(id_profissional)
        HorarioDAO.inserir(c)

    def horario_listar():
        return HorarioDAO.listar()

    def horario_atualizar(id, data, confirmado, id_cliente, id_servico, id_profissional):
        c = Horario(id, data)
        c.set_confirmado(confirmado)
        c.set_id_cliente(id_cliente)
        c.set_id_servico(id_servico)
        c.set_id_profissional(id_profissional)
        HorarioDAO.atualizar(c)

    def horario_excluir(id):
        c = Horario(id, None)
        HorarioDAO.excluir(c)

    def horario_filtrar_profissional(id_profissional):
        r=[]
        for h in View.horario_listar():
            if h.get_id_profissional() == id_profissional: 
                r.append(h)
        return r
    
    def horario_filtrar_cliente(id_cliente):
        r=[]
        for h in View.horario_listar():
            if h.get_id_cliente() == id_cliente:
                r.append(h)
        return r

    def horario_agendar_horario(id_profissional):
        r=[]
        agora = datetime.now()
        for h in View.horario_listar():
            if (h.get_data() >= agora and 
                h.get_confirmado() == False and 
                h.get_id_cliente() in (None, 0) and 
                h.get_id_profissional() == id_profissional):
                r.append(h)
        r.sort(key= lambda h :h.get_data())
        return r
    
    def horario_listar_nao_confirmados(id_profissional):
        r = []
        agora = datetime.now() 
        for h in View.horario_listar():
            if (h.get_id_profissional() == id_profissional and 
                h.get_id_cliente() not in (None, 0) and 
                h.get_confirmado() == False): 
                r.append(h)
        r.sort(key=lambda x: x.get_data())
        return r

    def profissional_listar():
        return ProfissionalDAO.listar()
    
    def profissional_listar_id(id):
        return ProfissionalDAO.listar_id(id)
    
    def profissional_inserir(nome, especialidade, conselho, email, senha):
        profissional = Profissional(0, nome, especialidade, conselho, email, senha)
        View._validar_email(email)
        ProfissionalDAO.inserir(profissional)

    def profissional_atualizar(id, nome, especialidade, conselho, email, senha):
        profissional = Profissional(id, nome, especialidade, conselho, email, senha)
        View._validar_email(email, id, 'profissional')
        ProfissionalDAO.atualizar(profissional)
        
    def profissional_excluir(id):
        horarios = View.horario_filtrar_profissional(id)
        if len(horarios) > 0:
            raise ValueError("Não é possível excluir um profissional que possui horários cadastrados na agenda")
            
        profissional = Profissional(id, "", "", "", "", "")
        ProfissionalDAO.excluir(profissional)
    
    def cliente_criar_admin():
        try:
            for c in View.cliente_listar():
                if c.get_email() == "admin": return 
            admin = Cliente(0, "admin", "admin", "fone", "1234")
            ClienteDAO.inserir(admin) 
        except ValueError:
            pass 
            
    def cliente_autenticar (email, senha):
        for c in View.cliente_listar():
            if c.get_email() == email and c.get_senha() == senha:
                return {"id": c.get_id(), "nome": c.get_nome()}
        return None
    
    def profissional_autenticar(email, senha):
        for c in View.profissional_listar():
            if c.get_email() == email and c.get_senha() == senha:
                return{"id": c.get_id(), "nome": c.get_nome()}
        return None