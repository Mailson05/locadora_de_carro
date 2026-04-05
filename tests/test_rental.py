"""
Testes unitários para o sistema de aluguel de carros
"""

import pytest
from app.rental import Carro, SistemaAluguel


class TestCarro:
    """Testes da classe Carro"""
    
    def test_criar_carro(self):
        """Deve criar um carro"""
        carro = Carro("ABC-1234", "Toyota Corolla", 100.00)
        assert carro.placa == "ABC-1234"
        assert carro.modelo == "Toyota Corolla"
        assert carro.valor_diaria == 100.00
        assert carro.alugado is False
    
    def test_carro_placa_invalida(self):
        """Não deve criar carro com placa inválida"""
        with pytest.raises(ValueError, match="Placa inválida"):
            Carro("", "Modelo", 100.00)
        with pytest.raises(ValueError, match="Placa inválida"):
            Carro(None, "Modelo", 100.00)
    
    def test_carro_modelo_invalido(self):
        """Não deve criar carro com modelo inválido"""
        with pytest.raises(ValueError, match="Modelo inválido"):
            Carro("ABC-1234", "", 100.00)
        with pytest.raises(ValueError, match="Modelo inválido"):
            Carro("ABC-1234", None, 100.00)
    
    def test_carro_valor_negativo(self):
        """Não deve criar carro com valor negativo"""
        with pytest.raises(ValueError, match="Valor da diária não pode ser negativo"):
            Carro("ABC-1234", "Modelo", -50.00)
    
    def test_alugar_carro(self):
        """Deve marcar carro como alugado"""
        carro = Carro("ABC-1234", "Modelo", 100.00)
        carro.alugar()
        assert carro.alugado is True
    
    def test_alugar_carro_ja_alugado(self):
        """Não deve alugar carro que já está alugado"""
        carro = Carro("ABC-1234", "Modelo", 100.00)
        carro.alugar()
        with pytest.raises(ValueError, match="Carro já está alugado"):
            carro.alugar()
    
    def test_devolver_carro(self):
        """Deve marcar carro como disponível"""
        carro = Carro("ABC-1234", "Modelo", 100.00)
        carro.alugar()
        carro.devolver()
        assert carro.alugado is False
    
    def test_devolver_carro_nao_alugado(self):
        """Não deve devolver carro que não está alugado"""
        carro = Carro("ABC-1234", "Modelo", 100.00)
        with pytest.raises(ValueError, match="Carro não está alugado"):
            carro.devolver()


class TestSistemaAluguel:
    """Testes da classe SistemaAluguel"""
    
    def test_criar_sistema(self):
        """Deve criar um sistema vazio"""
        sistema = SistemaAluguel()
        assert len(sistema.carros) == 0
    
    def test_adicionar_carro(self):
        """Deve adicionar carro ao sistema"""
        sistema = SistemaAluguel()
        carro = Carro("ABC-1234", "Toyota", 100.00)
        sistema.adicionar_carro(carro)
        
        assert len(sistema.carros) == 1
        assert sistema.carros[0].placa == "ABC-1234"
    
    def test_adicionar_multiplos_carros(self):
        """Deve adicionar múltiplos carros"""
        sistema = SistemaAluguel()
        c1 = Carro("ABC-1234", "Toyota", 100.00)
        c2 = Carro("XYZ-9999", "Fiat", 80.00)
        
        sistema.adicionar_carro(c1)
        sistema.adicionar_carro(c2)
        
        assert len(sistema.carros) == 2
    
    def test_adicionar_objeto_invalido(self):
        """Não deve adicionar objeto que não é Carro"""
        sistema = SistemaAluguel()
        with pytest.raises(ValueError, match="Deve ser um objeto Carro"):
            sistema.adicionar_carro("Não é carro")
    
    def test_listar_carros_disponiveis(self):
        """Deve listar apenas carros disponíveis"""
        sistema = SistemaAluguel()
        c1 = Carro("ABC-1234", "Toyota", 100.00)
        c2 = Carro("XYZ-9999", "Fiat", 80.00)
        
        sistema.adicionar_carro(c1)
        sistema.adicionar_carro(c2)
        c1.alugar()
        
        disponiveis = sistema.listar_carros_disponiveis()
        assert len(disponiveis) == 1
        assert disponiveis[0].placa == "XYZ-9999"
    
    def test_listar_carros_disponiveis_vazio(self):
        """Deve retornar lista vazia se nenhum disponível"""
        sistema = SistemaAluguel()
        assert sistema.listar_carros_disponiveis() == []
    
    def test_alugar_carro_por_placa(self):
        """Deve alugar carro pela placa"""
        sistema = SistemaAluguel()
        carro = Carro("ABC-1234", "Toyota", 100.00)
        sistema.adicionar_carro(carro)
        
        sistema.alugar_carro("ABC-1234")
        assert carro.alugado is True
    
    def test_alugar_carro_inexistente(self):
        """Não deve alugar carro que não existe"""
        sistema = SistemaAluguel()
        with pytest.raises(ValueError, match="Carro com placa .* não encontrado"):
            sistema.alugar_carro("ZZZ-0000")
    
    def test_devolver_carro_por_placa(self):
        """Deve devolver carro pela placa"""
        sistema = SistemaAluguel()
        carro = Carro("ABC-1234", "Toyota", 100.00)
        sistema.adicionar_carro(carro)
        
        sistema.alugar_carro("ABC-1234")
        sistema.devolver_carro("ABC-1234")
        assert carro.alugado is False
    
    def test_devolver_carro_inexistente(self):
        """Não deve devolver carro que não existe"""
        sistema = SistemaAluguel()
        with pytest.raises(ValueError, match="Carro com placa .* não encontrado"):
            sistema.devolver_carro("ZZZ-0000")


class TestCalcularValor:
    """Testes do cálculo de valor do aluguel"""
    
    def test_calcular_valor_um_dia(self):
        """Deve calcular valor sem desconto para 1 dia"""
        sistema = SistemaAluguel()
        carro = Carro("ABC-1234", "Toyota", 100.00)
        sistema.adicionar_carro(carro)
        
        resultado = sistema.calcular_valor("ABC-1234", 1)
        assert resultado["valor_bruto"] == 100.00
        assert resultado["desconto"] == 0.00
        assert resultado["total"] == 100.00
    
    def test_calcular_valor_multiplos_dias(self):
        """Deve calcular valor para múltiplos dias"""
        sistema = SistemaAluguel()
        carro = Carro("ABC-1234", "Toyota", 100.00)
        sistema.adicionar_carro(carro)
        
        resultado = sistema.calcular_valor("ABC-1234", 5)
        assert resultado["valor_bruto"] == 500.00
        assert resultado["desconto"] == 0.00
        assert resultado["total"] == 500.00
    
    def test_calcular_valor_sete_dias_desconto(self):
        """Deve aplicar 10% de desconto a partir de 7 dias"""
        sistema = SistemaAluguel()
        carro = Carro("ABC-1234", "Toyota", 100.00)
        sistema.adicionar_carro(carro)
        
        resultado = sistema.calcular_valor("ABC-1234", 7)
        assert resultado["valor_bruto"] == 700.00
        assert resultado["desconto"] == 70.00
        assert resultado["total"] == 630.00
    
    def test_calcular_valor_dez_dias_desconto(self):
        """Deve aplicar 10% de desconto para 10 dias"""
        sistema = SistemaAluguel()
        carro = Carro("ABC-1234", "Toyota", 100.00)
        sistema.adicionar_carro(carro)
        
        resultado = sistema.calcular_valor("ABC-1234", 10)
        assert resultado["valor_bruto"] == 1000.00
        assert resultado["desconto"] == 100.00
        assert resultado["total"] == 900.00
    
    def test_calcular_valor_trinta_dias_desconto(self):
        """Deve aplicar 20% de desconto a partir de 30 dias"""
        sistema = SistemaAluguel()
        carro = Carro("ABC-1234", "Toyota", 100.00)
        sistema.adicionar_carro(carro)
        
        resultado = sistema.calcular_valor("ABC-1234", 30)
        assert resultado["valor_bruto"] == 3000.00
        assert resultado["desconto"] == 600.00
        assert resultado["total"] == 2400.00
    
    def test_calcular_valor_quarenta_cinco_dias_desconto(self):
        """Deve aplicar 20% de desconto para 45 dias"""
        sistema = SistemaAluguel()
        carro = Carro("ABC-1234", "Toyota", 100.00)
        sistema.adicionar_carro(carro)
        
        resultado = sistema.calcular_valor("ABC-1234", 45)
        assert resultado["valor_bruto"] == 4500.00
        assert resultado["desconto"] == 900.00
        assert resultado["total"] == 3600.00
    
    def test_calcular_valor_carro_inexistente(self):
        """Não deve calcular valor para carro inexistente"""
        sistema = SistemaAluguel()
        with pytest.raises(ValueError, match="Carro com placa .* não encontrado"):
            sistema.calcular_valor("ZZZ-0000", 5)
    
    def test_calcular_valor_dias_invalido(self):
        """Não deve calcular valor com dias inválido"""
        sistema = SistemaAluguel()
        carro = Carro("ABC-1234", "Toyota", 100.00)
        sistema.adicionar_carro(carro)
        
        with pytest.raises(ValueError, match="Número de dias deve ser maior que zero"):
            sistema.calcular_valor("ABC-1234", 0)
        
        with pytest.raises(ValueError, match="Número de dias deve ser maior que zero"):
            sistema.calcular_valor("ABC-1234", -5)
