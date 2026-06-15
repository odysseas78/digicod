import pdfkit
from eshop.pdf.invoicehtml import invtemplate
from datetime import datetime, timedelta, date
from decimal import Decimal



def create_invoice(order):
        # order = Order.objects.filter(id=862682).first()
    if order.cart.currency.shortname == 'USDT':
            tofx = 4
    elif order.cart.currency.type == 'crypto':
        tofx = 8
    else:
        tofx = 2

    prodlist = ''''''
    for product in order.cart.products.all():
        # print(product.product.title)
        prodlist += f'''<tr>
                    <td style="padding: 15px;">{product.qty}</td>
                    <td style="padding: 15px;">{product.product.title}</td>
                    <td style="padding: 15px;">{round(product.final_price/product.qty*order.cart.currency.price, tofx)} {order.cart.currency.sign}</td>
                    <td style="padding: 15px;">0 {order.cart.currency.sign}</td>
                    <td style="padding: 15px;">0 %</td>
                    <td style="text-align: right; padding: 15px;" >{round(product.final_price*order.cart.currency.price, tofx)} {order.cart.currency.sign}</td>
                </tr>'''
    invnr = str(date.today()).replace('-','')[2:]+str(order.id)
    a = invtemplate.format(
        order.customer.user.email, 
        invnr,
        order.created_at.strftime("%d.%m.%Y %H:%M"),
        order.id,
        prodlist,
        round(order.pay_amount, tofx),
        order.pay_currency.sign,
        order.pay_currency.sign,
        round(order.pay_amount, tofx),
        order.pay_currency.sign,
        order.del_email
        )
    with open(f'/home/dcback/eshop/pdf/invoices/invoice_{invnr}.html', 'w') as f:
        f.write(a)
        f.close()

    pdfkit.from_file(f'/home/dcback/eshop/pdf/invoices/invoice_{invnr}.html', 
                     output_path=f'/home/dcback/eshop/pdf/invoices/invoice_{invnr}.pdf')
    
    return invnr