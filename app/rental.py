
class Carro:
    
    def __init__(self, placa, modelo, valor_diaria):
        """
        Cria um carro
        
        Args:
            placa (str): Placa do carro (ex: ABC-1234)
            modelo (str): Modelo do carro
            valor_diaria (float): Valor da diária em reais
        """
        if not placa or not isinstance(placa, str):
            raise ValueError("Placa inválida")
        if not modelo or not isinstance(modelo, str):
            raise ValueError("Modelo inválido")
        if valor_diaria < 0:
            raise ValueError("Valor da diária não pode ser negativo")
        
        self.placa = placa
        self.modelo = modelo
        self.valor_diaria = valor_diaria
        self.alugado = False
    
    def alugar(self):
        if self.alugado:
            raise ValueError("Carro já está alugado")
        self.alugado = True
    
    def devolver(self):
        if not self.alugado:
            raise ValueError("Carro não está alugado")
        self.alugado = False


class SistemaAluguel:
    
    DESCONTO_SETE_DIAS = 0.10  
    DESCONTO_TRINTA_DIAS = 0.20 
    
    def __init__(self):
        self.carros = []
    
    def adicionar_carro(self, carro):
        
        if not isinstance(carro, Carro):
            raise ValueError("Deve ser um objeto Carro")
        self.carros.append(carro)
    
    def listar_carros_disponiveis(self):
        
        return [c for c in self.carros if not c.alugado]
    
    def alugar_carro(self, placa):
        
        for carro in self.carros:
            if carro.placa == placa:
                carro.alugar()
                return
        raise ValueError(f"Carro com placa {placa} não encontrado")
    
    def devolver_carro(self, placa):
        
        for carro in self.carros:
            if carro.placa == placa:
                carro.devolver()
                return
        raise ValueError(f"Carro com placa {placa} não encontrado")
    
    def calcular_valor(self, placa, dias):
        
        if dias <= 0:
            raise ValueError("Número de dias deve ser maior que zero")
        
        # Encontra o carro
        carro = None
        for c in self.carros:
            if c.placa == placa:
                carro = c
                break
        
        if not carro:
            raise ValueError(f"Carro com placa {placa} não encontrado")
        
        valor_bruto = carro.valor_diaria * dias
        
        desconto = 0
        if dias >= 30:
            desconto = valor_bruto * self.DESCONTO_TRINTA_DIAS
        elif dias >= 7:
            desconto = valor_bruto * self.DESCONTO_SETE_DIAS
        
        total = valor_bruto - desconto
        
        return {
            "valor_bruto": round(valor_bruto, 2),
            "desconto": round(desconto, 2),
            "total": round(total, 2)
        }
