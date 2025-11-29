def calculate_financials(stock_items, allowance_deductions, payments):
    gross_total = sum(
        float(item.weight or 0) * float(item.rate or 0)
        for item in stock_items if item
    )

    net_total = gross_total
    for entry in allowance_deductions:
        amount = round(float(entry.allowance_deduction_amount or 0))
        if entry.is_allowance:
            net_total += amount
        else:
            net_total -= amount

    total_payments = sum(
        round(float(p.payment_amount or 0)) for p in payments
    )

    remaining_payment = net_total - total_payments

    if total_payments >= net_total:
        payment_status = "PAID"
    elif 0 < total_payments < net_total:
        payment_status = "PARTIALLY PAID"
    else:
        payment_status = "UNPAID"

    return net_total, payment_status, remaining_payment
