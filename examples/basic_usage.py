"""Basic usage examples for the Asaas SDK."""

from asaas import Asaas, AsaasValidationError

# Initialize the client (sandbox mode for testing)
client = Asaas(api_key="your_api_key_here", sandbox=True)

# -- Customers --

# Create a customer
customer = client.customers.create(
    name="João Silva",
    cpf_cnpj="24971563792",
    email="joao@example.com",
    mobile_phone="11999999999",
    postal_code="01310000",
)
print(f"Customer created: {customer['id']}")

# List customers
page = client.customers.list(limit=10)
print(f"Total customers: {page.total_count}")
for c in page.data:
    print(f"  - {c['name']} ({c['id']})")

# Auto-paginate through all customers
for c in client.customers.list_all(max_items=50):
    print(f"  - {c['name']}")

# Get a single customer
customer = client.customers.get(customer["id"])
print(f"Customer name: {customer['name']}")

# Update a customer
updated = client.customers.update(customer["id"], name="João da Silva")
print(f"Updated name: {updated['name']}")


# -- Payments --

# Create a boleto payment
payment = client.payments.create(
    customer=customer["id"],
    billing_type="BOLETO",
    value=150.00,
    due_date="2025-12-31",
    description="Monthly service fee",
)
print(f"Payment created: {payment['id']} - Status: {payment['status']}")

# Get boleto identification field (linha digitável)
boleto_info = client.payments.get_identification_field(payment["id"])
print(f"Boleto line: {boleto_info.get('identificationField')}")

# Create a PIX payment
pix_payment = client.payments.create(
    customer=customer["id"],
    billing_type="PIX",
    value=75.50,
    due_date="2025-12-31",
    description="PIX payment",
)

# Get PIX QR Code
qr = client.payments.get_pix_qr_code(pix_payment["id"])
print(f"PIX payload: {qr.get('payload')}")

# List payments with filters
page = client.payments.list(
    customer=customer["id"],
    status="PENDING",
    due_date_ge="2025-01-01",
)
print(f"Pending payments: {page.total_count}")


# -- Error Handling --

try:
    client.payments.create(
        customer="invalid_customer",
        billing_type="BOLETO",
        value=-1,
        due_date="2025-12-31",
    )
except AsaasValidationError as e:
    print(f"Validation error: {e.message}")
    for error in e.errors:
        print(f"  [{error['code']}] {error['description']}")


# -- Context Manager --

with Asaas(api_key="your_api_key_here", sandbox=True) as client:
    balance = client.finance.get_balance()
    print(f"Account balance: R$ {balance.get('balance', 0):.2f}")

# -- Cleanup --
client.close()
