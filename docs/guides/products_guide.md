# Products

Products represents the itens consumed by a cliend and used on sale carts.
Every product will have a `category`, `purchase_price` and `sale_price`.

**Categories can be created by a adminuser**
**The prices will be used on relatories**

## How to use

The easiest form to use is with postman (see `unsing_postman.md` guide for more information).

### Getting product QRCode

To get a product QRCode you will need to retrieve the product `id` first (You can use the list enpoint to get it). Then just put in your navigator `{{host}}/api/v1/products/{{uuid}}/qrcode`.
