# Asaas Python SDK

SDK Python completo para a API v3 da plataforma de pagamentos [Asaas](https://www.asaas.com/).

## Instalação

```bash
pip install asaas-sdk
```

Ou instale a partir do código fonte:

```bash
pip install -e .
```

## Início Rápido

```python
from asaas import Asaas

# Inicializar cliente (sandbox para testes)
client = Asaas(api_key="sua_api_key", sandbox=True)

# Criar cliente
customer = client.customers.create(
    name="João Silva",
    cpf_cnpj="24971563792",
    email="joao@example.com",
)

# Criar cobrança via boleto
payment = client.payments.create(
    customer=customer["id"],
    billing_type="BOLETO",
    value=100.50,
    due_date="2025-12-31",
)

# Obter linha digitável do boleto
boleto = client.payments.get_identification_field(payment["id"])
print(boleto["identificationField"])

# Criar cobrança via PIX
pix_payment = client.payments.create(
    customer=customer["id"],
    billing_type="PIX",
    value=75.00,
    due_date="2025-12-31",
)
qr = client.payments.get_pix_qr_code(pix_payment["id"])
print(qr["payload"])
```

## Configuração

```python
client = Asaas(
    api_key="sua_api_key",
    sandbox=True,          # False para produção
    timeout=30,            # Timeout em segundos
    max_retries=3,         # Tentativas em caso de erro 5xx
    backoff_factor=0.5,    # Fator de backoff exponencial
)

# Ou use como context manager
with Asaas(api_key="sua_api_key", sandbox=True) as client:
    balance = client.finance.get_balance()
```

### Ambientes

| Ambiente   | URL Base                         |
|------------|----------------------------------|
| Produção   | `https://api.asaas.com`          |
| Sandbox    | `https://sandbox.asaas.com/api`  |

## Recursos Disponíveis

| Recurso | Acesso | Descrição |
|---------|--------|-----------|
| `client.customers` | Clientes | CRUD de clientes |
| `client.payments` | Cobranças | Boleto, PIX, Cartão de crédito |
| `client.subscriptions` | Assinaturas | Cobranças recorrentes |
| `client.installments` | Parcelamentos | Parcelamento com cartão |
| `client.pix` | PIX | Chaves, QR codes, transações |
| `client.accounts` | Subcontas | Gestão de subcontas |
| `client.transfers` | Transferências | Transferências entre contas |
| `client.webhooks` | Webhooks | Notificações de eventos |
| `client.invoices` | Notas Fiscais | Emissão de NFS-e |
| `client.finance` | Financeiro | Saldo e estatísticas |
| `client.bill` | Pagamento de Contas | Pagamento de boletos |
| `client.chargebacks` | Chargebacks | Disputas de estorno |
| `client.checkouts` | Checkouts | Links de checkout |
| `client.payment_links` | Links de Pagamento | Criação de links |
| `client.payment_dunnings` | Negativação | Negativação de devedores |
| `client.anticipations` | Antecipações | Antecipação de recebíveis |
| `client.credit_card` | Cartão de Crédito | Tokenização |
| `client.credit_bureau_report` | Consulta Serasa | Consultas de crédito |
| `client.fiscal_info` | Info Fiscal | Configurações fiscais |
| `client.financial_transactions` | Extrato | Extrato financeiro |
| `client.my_account` | Minha Conta | Configurações da conta |
| `client.notifications` | Notificações | Configuração de notificações |
| `client.lean` | Lean Payments | Cobranças com dados resumidos |
| `client.mobile_phone_recharges` | Recarga Celular | Recargas de celular |
| `client.escrow` | Conta Escrow | Garantias |
| `client.wallets` | Wallets | Identificação de carteiras |
| `client.sandbox_utils` | Sandbox | Utilitários de teste |

## Exemplos de Uso

### Clientes

```python
# Criar
customer = client.customers.create(
    name="Maria Santos",
    cpf_cnpj="12345678901",
    email="maria@example.com",
    mobile_phone="11999999999",
)

# Listar com filtros
page = client.customers.list(name="Maria", limit=20)
for c in page.data:
    print(c["name"], c["id"])

# Paginação automática
for c in client.customers.list_all(max_items=500):
    print(c["name"])

# Atualizar
client.customers.update(customer["id"], name="Maria S. Santos")

# Remover e restaurar
client.customers.delete(customer["id"])
client.customers.restore(customer["id"])
```

### Cobranças

```python
# Boleto
payment = client.payments.create(
    customer="cus_xxx",
    billing_type="BOLETO",
    value=199.90,
    due_date="2025-12-31",
    description="Mensalidade",
    discount={"value": 10.00, "dueDateLimitDays": 5, "type": "FIXED"},
    fine={"value": 1.0},
    interest={"value": 2.0},
)

# Cartão de crédito
cc_payment = client.payments.create(
    customer="cus_xxx",
    billing_type="CREDIT_CARD",
    value=99.90,
    due_date="2025-12-31",
    credit_card={
        "holderName": "john doe",
        "number": "5162306219378829",
        "expiryMonth": "05",
        "expiryYear": "2028",
        "ccv": "318",
    },
    credit_card_holder_info={
        "name": "John Doe",
        "email": "john@example.com",
        "cpfCnpj": "24971563792",
        "postalCode": "89223005",
        "phone": "4738010919",
    },
)

# Estorno
client.payments.refund("pay_xxx")
client.payments.refund("pay_xxx", value=50.0)  # Estorno parcial

# Status e info
status = client.payments.get_status("pay_xxx")
qr = client.payments.get_pix_qr_code("pay_xxx")
boleto = client.payments.get_identification_field("pay_xxx")
```

### Assinaturas

```python
subscription = client.subscriptions.create(
    customer="cus_xxx",
    billing_type="CREDIT_CARD",
    value=49.90,
    next_due_date="2025-03-01",
    cycle="MONTHLY",
    description="Plano Premium",
    credit_card_token="token_xxx",
)

# Listar pagamentos da assinatura
payments = client.subscriptions.list_payments(subscription["id"])

# Atualizar valor
client.subscriptions.update(subscription["id"], value=59.90)

# Cancelar
client.subscriptions.delete(subscription["id"])
```

### Saldo e Extrato

```python
balance = client.finance.get_balance()
print(f"Saldo: R$ {balance['balance']:.2f}")

stats = client.finance.get_payment_statistics()
print(f"Estatísticas: {stats}")

# Extrato
page = client.financial_transactions.list(
    start_date="2025-01-01",
    finish_date="2025-01-31",
)
for tx in page.data:
    print(f"{tx['date']} - R${tx['value']} - {tx['description']}")
```

### Webhooks

```python
webhook = client.webhooks.create(
    url="https://seusite.com/webhook",
    email="admin@seusite.com",
    events=["PAYMENT_CONFIRMED", "PAYMENT_OVERDUE", "PAYMENT_REFUNDED"],
)
```

## Paginação

Todos os endpoints de listagem retornam um `PaginatedResponse`:

```python
page = client.payments.list(limit=10)
print(page.total_count)  # Total de registros
print(page.has_more)     # Há mais páginas?
print(page.data)         # Lista de registros
print(page.offset)       # Offset atual
print(page.limit)        # Limite por página
```

Para paginar automaticamente, use os métodos `list_all()`:

```python
# Itera por TODOS os registros automaticamente
for payment in client.payments.list_all():
    print(payment["id"])

# Limitar a quantidade total
for payment in client.payments.list_all(max_items=200):
    print(payment["id"])
```

## Tratamento de Erros

```python
from asaas import (
    AsaasError,
    AsaasAPIError,
    AsaasValidationError,
    AsaasAuthenticationError,
    AsaasNotFoundError,
    AsaasRateLimitError,
    AsaasTimeoutError,
    AsaasConnectionError,
)

try:
    client.payments.create(...)
except AsaasValidationError as e:
    # 400 - Erro de validação
    print(f"Validação: {e.message}")
    for error in e.errors:
        print(f"  [{error['code']}] {error['description']}")
except AsaasAuthenticationError:
    # 401 - API key inválida
    print("Verifique sua API key")
except AsaasNotFoundError:
    # 404 - Recurso não encontrado
    print("Registro não encontrado")
except AsaasRateLimitError:
    # 429 - Rate limit excedido
    print("Aguarde antes de tentar novamente")
except AsaasTimeoutError:
    # Timeout de conexão
    print("Timeout na requisição")
except AsaasConnectionError:
    # Erro de conexão
    print("Erro de conexão com a API")
except AsaasAPIError as e:
    # Qualquer outro erro da API
    print(f"Erro {e.status_code}: {e.message}")
```

## Logging

O SDK usa o módulo `logging` padrão do Python:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("asaas")
logger.setLevel(logging.DEBUG)
```

## Sandbox

Utilitários disponíveis apenas no ambiente sandbox:

```python
client = Asaas(api_key="sandbox_key", sandbox=True)

# Simular confirmação de pagamento
client.sandbox_utils.confirm_payment("pay_xxx")

# Forçar vencimento de uma cobrança
client.sandbox_utils.force_overdue("pay_xxx")
```

## Desenvolvimento

```bash
# Instalar dependências de desenvolvimento
pip install -e ".[dev]"

# Executar testes
pytest

# Executar testes com cobertura
pytest --cov=asaas

# Linting
ruff check src/

# Type checking
mypy src/asaas/
```

## Requisitos

- Python 3.8+
- `requests` >= 2.28.0

## Links

- [Documentação oficial da API Asaas](https://docs.asaas.com)
- [Painel Sandbox](https://sandbox.asaas.com)

## Licença

MIT
