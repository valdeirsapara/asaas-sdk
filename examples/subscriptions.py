"""Examples for managing subscriptions."""

from asaas import Asaas

client = Asaas(api_key="your_api_key_here", sandbox=True)

CUSTOMER_ID = "cus_000005401844"

# -- Create a monthly subscription with boleto --
subscription = client.subscriptions.create(
    customer=CUSTOMER_ID,
    billing_type="BOLETO",
    value=99.90,
    next_due_date="2025-02-15",
    cycle="MONTHLY",
    description="Monthly SaaS plan",
    max_payments=12,
    discount={"value": 5.00, "dueDateLimitDays": 3, "type": "FIXED"},
    fine={"value": 1.0},
    interest={"value": 2.0},
)
print(f"Subscription created: {subscription['id']}")
print(f"Status: {subscription['status']}")
print(f"Next due date: {subscription['nextDueDate']}")

# -- Create a credit card subscription --
cc_subscription = client.subscriptions.create(
    customer=CUSTOMER_ID,
    billing_type="CREDIT_CARD",
    value=49.90,
    next_due_date="2025-02-15",
    cycle="MONTHLY",
    description="Premium plan",
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
        "phone": "4738010919",
    },
)
print(f"CC Subscription: {cc_subscription['id']}")

# -- List all active subscriptions --
page = client.subscriptions.list(status="ACTIVE", limit=20)
for sub in page.data:
    print(f"  {sub['id']} - R${sub['value']} - {sub['cycle']}")

# -- Get subscription payments --
payments = client.subscriptions.list_payments(subscription["id"])
for p in payments.get("data", []):
    print(f"  Payment {p['id']} - {p['status']} - Due: {p.get('dueDate')}")

# -- Update subscription value --
updated = client.subscriptions.update(
    subscription["id"],
    value=119.90,
    description="Updated monthly plan",
)
print(f"Updated value: R${updated['value']}")

# -- Cancel a subscription --
# client.subscriptions.delete(subscription["id"])

client.close()
