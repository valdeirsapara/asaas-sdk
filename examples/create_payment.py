"""Examples for creating different types of payments."""

from asaas import Asaas

client = Asaas(api_key="your_api_key_here", sandbox=True)

CUSTOMER_ID = "cus_000005401844"

# -- Boleto --
boleto = client.payments.create(
    customer=CUSTOMER_ID,
    billing_type="BOLETO",
    value=199.90,
    due_date="2025-12-31",
    description="Invoice #12345",
    external_reference="order_12345",
    discount={"value": 10.00, "dueDateLimitDays": 5, "type": "FIXED"},
    interest={"value": 2.0},  # 2% per month
    fine={"value": 1.0},  # 1% fine
)
print(f"Boleto created: {boleto['id']}")
print(f"Invoice URL: {boleto.get('invoiceUrl')}")
print(f"Bank slip URL: {boleto.get('bankSlipUrl')}")


# -- Credit Card --
cc_payment = client.payments.create(
    customer=CUSTOMER_ID,
    billing_type="CREDIT_CARD",
    value=299.90,
    due_date="2025-12-31",
    description="Premium subscription",
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
        "postalCode": "89223-005",
        "addressNumber": "277",
        "phone": "4738010919",
    },
    remote_ip="116.213.42.532",
)
print(f"Credit card payment: {cc_payment['id']} - Status: {cc_payment['status']}")


# -- PIX --
pix = client.payments.create(
    customer=CUSTOMER_ID,
    billing_type="PIX",
    value=49.90,
    due_date="2025-12-31",
    description="Quick PIX payment",
)
qr_code = client.payments.get_pix_qr_code(pix["id"])
print(f"PIX QR Code payload: {qr_code.get('payload')}")


# -- Pre-authorized Credit Card --
preauth = client.payments.create(
    customer=CUSTOMER_ID,
    billing_type="CREDIT_CARD",
    value=500.00,
    due_date="2025-12-31",
    authorized_only=True,
    credit_card_token="your_token_here",
)
# Later, capture the authorized payment
# client.payments.capture_authorized(preauth["id"])


# -- Payment with Split --
split_payment = client.payments.create(
    customer=CUSTOMER_ID,
    billing_type="BOLETO",
    value=1000.00,
    due_date="2025-12-31",
    split=[
        {"walletId": "wallet_partner_1", "fixedValue": 200.00},
        {"walletId": "wallet_partner_2", "percentualValue": 10.0},
    ],
)
print(f"Split payment: {split_payment['id']}")

client.close()
