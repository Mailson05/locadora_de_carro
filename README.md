# Sistema de Aluguel de Carros - Testes Unitários

## 📋 Descrição do Projeto

Este é um projeto educacional para demonstrar **testes unitários em Python** usando pytest. O projeto implementa um **sistema simples de aluguel de carros** onde é possível cadastrar carros, alugá-los, devolvê-los e calcular o valor do aluguel com descontos automáticos.

## 🎯 Regras de Negócio

### 1. **Cadastro de Carros**
- Todo carro tem: placa, modelo e valor da diária
- Placa não pode estar vazia
- Modelo não pode estar vazio
- Valor da diária não pode ser negativo
- Carros iniciam como disponíveis para aluguel

### 2. **Aluguel de Carros**
- Um carro disponível pode ser alugado através da sua placa
- Um carro alugado não pode ser alugado novamente
- Um carro deve estar alugado para ser devolvido

### 3. **Cálculo do Valor**
O valor do aluguel é calculado com desconto progressivo:

- **1 a 6 dias**: Sem desconto
  - Valor = preço diária × dias

- **7 a 29 dias**: 10% de desconto
  - Desconto = valor bruto × 0.10

- **30 dias ou mais**: 20% de desconto
  - Desconto = valor bruto × 0.20

**Fórmula**: `total = valor_bruto - desconto`

### 4. **Operações do Sistema**
- Adicionar carros ao sistema
- Listar carros disponíveis
- Alugar carro por placa
- Devolver carro por placa
- Calcular valor de aluguel

## 📁 Estrutura do Projeto

```
unitario/
├── app/
│   ├── __init__.py          # Arquivo de inicialização
│   └── rental.py            # Classes Carro e SistemaAluguel
├── tests/
│   ├── __init__.py          # Arquivo de inicialização
│   └── test_rental.py       # Suite de testes
├── requirements.txt         # Dependências do projeto
└── README.md               # Este arquivo
```

## 🔧 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes)

### Passos

1. **Acesse o diretório do projeto**
   ```bash
   cd c:\Users\Mailson\Desktop\unitario
   ```

2. **Crie um ambiente virtual (recomendado)**
   ```bash
   python -m venv venv
   ```

3. **Ative o ambiente virtual**

   **Windows (PowerShell):**
   ```bash
   .\venv\Scripts\Activate.ps1
   ```

   **Windows (CMD):**
   ```bash
   .\venv\Scripts\activate.bat
   ```

   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Como Executar os Testes

### Executar todos os testes
```bash
pytest
```

### Executar com mais detalhes
```bash
pytest -v
```

### Executar com cobertura de código
```bash
pytest --cov=app tests/
```

### Executar uma classe de testes específica
```bash
pytest tests/test_rental.py::TestCarro -v
```

### Executar um teste específico
```bash
pytest tests/test_rental.py::TestCarro::test_criar_carro -v
```

### Parar no primeiro erro
```bash
pytest -x
```

### Modo verbose com output
```bash
pytest -v -s
```

## 📊 Cobertura de Testes

O projeto possui **24 testes unitários** organizados em **3 classes**:

| Classe de Teste | Testes | Cobertura |
|---|---|---|
| TestCarro | 8 | Criação, aluguel e devolução de carros |
| TestSistemaAluguel | 8 | Gerenciamento de carros no sistema |
| TestCalcularValor | 8 | Cálculo de valores e descontos |

**Total: 24 testes** cobrindo casos de sucesso e erro.

## 💡 Exemplos de Uso

### Exemplo 1: Aluguel Simples (1 dia)

```python
from app.rental import Carro, SistemaAluguel

# Criar sistema
sistema = SistemaAluguel()

# Adicionar carro: Toyota, R$ 120/dia
toyota = Carro("ABC-1234", "Toyota Corolla", 120.00)
sistema.adicionar_carro(toyota)

# Calcular aluguel por 1 dia
resultado = sistema.calcular_valor("ABC-1234", 1)
print(f"Valor bruto: R$ {resultado['valor_bruto']}")
print(f"Desconto: R$ {resultado['desconto']}")
print(f"Total: R$ {resultado['total']}")
```

**Saída:**
```
Valor bruto: R$ 120.00
Desconto: R$ 0.00
Total: R$ 120.00
```

### Exemplo 2: Aluguel com Desconto de 10% (7 dias)

```python
from app.rental import Carro, SistemaAluguel

sistema = SistemaAluguel()
fiat = Carro("XYZ-5678", "Fiat Uno", 100.00)
sistema.adicionar_carro(fiat)

# Calcular aluguel por 7 dias (aplica 10% de desconto)
resultado = sistema.calcular_valor("XYZ-5678", 7)
print(f"Valor bruto: R$ {resultado['valor_bruto']}")
print(f"Desconto (10%): R$ {resultado['desconto']}")
print(f"Total: R$ {resultado['total']}")
```

**Saída:**
```
Valor bruto: R$ 700.00
Desconto (10%): R$ 70.00
Total: R$ 630.00
```

### Exemplo 3: Aluguel com Desconto de 20% (30 dias)

```python
from app.rental import Carro, SistemaAluguel

sistema = SistemaAluguel()
honda = Carro("JKL-2020", "Honda City", 150.00)
sistema.adicionar_carro(honda)

# Calcular aluguel por 30 dias (aplica 20% de desconto)
resultado = sistema.calcular_valor("JKL-2020", 30)
print(f"Valor bruto: R$ {resultado['valor_bruto']}")
print(f"Desconto (20%): R$ {resultado['desconto']}")
print(f"Total: R$ {resultado['total']}")
```

**Saída:**
```
Valor bruto: R$ 4500.00
Desconto (20%): R$ 900.00
Total: R$ 3600.00
```

### Exemplo 4: Fluxo Completo de Aluguel

```python
from app.rental import Carro, SistemaAluguel

sistema = SistemaAluguel()

# Adicionar carros
c1 = Carro("ABC-1111", "Toyota", 120.00)
c2 = Carro("ABC-2222", "Fiat", 100.00)
sistema.adicionar_carro(c1)
sistema.adicionar_carro(c2)

# Listar carros disponíveis
disponiveis = sistema.listar_carros_disponiveis()
print(f"Carros disponíveis: {len(disponiveis)}")

# Alugar carro
sistema.alugar_carro("ABC-1111")
print("Toyota alugada!")

# Listar novamente
disponiveis = sistema.listar_carros_disponiveis()
print(f"Carros disponíveis agora: {len(disponiveis)}")

# Devolver carro
sistema.devolver_carro("ABC-1111")
print("Toyota devolvida!")

# Calcular valor
resultado = sistema.calcular_valor("ABC-1111", 15)
print(f"Aluguel para 15 dias: R$ {resultado['total']}")
```

**Saída:**
```
Carros disponíveis: 2
Toyota alugada!
Carros disponíveis agora: 1
Toyota devolvida!
Aluguel para 15 dias: R$ 1620.00
```

## 🧪 Padrões de Teste Utilizados

1. **Arrange-Act-Assert (AAA)**
   - Preparação → Execução → Validação

2. **Testes Positivos**
   - Verificam comportamento esperado em condições normais

3. **Testes Negativos**
   - Validam tratamento correto de erros e exceções

4. **Testes de Valores Limites**
   - Testam comportamento em casos extremos (dias 6, 7, 29, 30, etc)

5. **Organização por Classe**
   - Testes agrupados por funcionalidade

## 📝 Tabela de Descontos

| Período | Desconto | Exemplo (R$ 100/dia) |
|---|---|---|
| 1-6 dias | 0% | 6 dias = R$ 600 |
| 7-29 dias | 10% | 7 dias = R$ 630 (10% desc) |
| 30+ dias | 20% | 30 dias = R$ 2.400 (20% desc) |

## 🐛 Troubleshooting

### Erro: "pytest não encontrado"
```bash
pip install -r requirements.txt
```

### Erro: "ModuleNotFoundError"
Certifique-se de estar no diretório correto antes de executar pytest:
```bash
cd c:\Users\Mailson\Desktop\unitario
pytest
```

### Testes não encontrados
Verifique que os arquivos estão em `tests/test_rental.py`:
```bash
pytest tests/test_rental.py -v
```

## 📚 Referências

- [Documentação do Pytest](https://docs.pytest.org/)
- [Python Unittest Docs](https://docs.python.org/3/library/unittest.html)
- [Test-Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)

---

**Desenvolvido para aprendizado de Testes Unitários em Python** 🎓
