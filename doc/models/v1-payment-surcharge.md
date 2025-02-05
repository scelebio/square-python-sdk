
# V1 Payment Surcharge

V1PaymentSurcharge

## Structure

`V1 Payment Surcharge`

## Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `name` | `str` | Optional | The name of the surcharge. |
| `applied_money` | [`V1 Money`](../../doc/models/v1-money.md) | Optional | - |
| `rate` | `str` | Optional | The amount of the surcharge as a percentage. The percentage is provided as a string representing the decimal equivalent of the percentage. For example, "0.7" corresponds to a 7% surcharge. Exactly one of rate or amount_money should be set. |
| `amount_money` | [`V1 Money`](../../doc/models/v1-money.md) | Optional | - |
| `type` | [`str (V1 Payment Surcharge Type)`](../../doc/models/v1-payment-surcharge-type.md) | Optional | - |
| `taxable` | `bool` | Optional | Indicates whether the surcharge is taxable. |
| `taxes` | [`List V1 Payment Tax`](../../doc/models/v1-payment-tax.md) | Optional | The list of taxes that should be applied to the surcharge. |
| `surcharge_id` | `str` | Optional | A Square-issued unique identifier associated with the surcharge. |

## Example (as JSON)

```json
{
  "name": "name6",
  "applied_money": {
    "amount": 196,
    "currency_code": "IQD"
  },
  "rate": "rate4",
  "amount_money": {
    "amount": 186,
    "currency_code": "UZS"
  },
  "type": "AUTO_GRATUITY"
}
```

