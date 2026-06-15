import os, sys
import django
sys.path.insert(0, '/home/dcback')
from eshop.Utilss.utils import random_code
from eshop.pdf.createpdf import create_invoice
import django
import decimal


os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from eshop.models import Order
from django.core.mail import EmailMultiAlternatives

def qr_code_mime(data, name):
    import qrcode
    import io
    from email.mime.image import MIMEImage
    qr = qrcode.QRCode(version = 1,
                   box_size = 3,
                   border = 0)
    qr.add_data(data)
    qr.make(fit = True)
    img = qr.make_image(fill_color = 'green',
                        back_color = 'white')
    buf = io.BytesIO()
    img.save(buf, format='PNG', name={name})
    byte_im = buf.getvalue()
    image = MIMEImage(byte_im)
    return image

#,"coxah@web.de", "m.odysseas78@gmail.com", "o.martasidis@yahoo.de"
def orderemail(ordernr):
    
    order = Order.objects.filter(id=ordernr).first()
    # codes = ProductCode.objects.get(ct_product=order.cart.products)
    invnr = create_invoice(order)
    if order.cart.currency.shortname == 'USDT':
        tofx = 4
    elif order.cart.currency.type == 'crypto':
        tofx = 8
    else:
        tofx = 2
    product = ''
    imageslist = []
    for item in order.cart.products.all():
        codes = ''
        i=1
        for code in item.product_codes.all():
            border = 'border-bottom: 1px solid gray;' if i!=len(item.product_codes.all()) else ''
            imgname = random_code(16, True, True, True, False)
            qrcode = f'<img src="cid:{imgname}.png" alt="QR-CODE">' if code.code[:6] != 'Sorry,' else ''
            if code.serial:
                serial = f"""
                <div><i> Serial: {code.serial}</i></div>
              """
            else:
                serial = ''
            cod1 = f'''
                <td style="padding-bottom: 10px; padding-top: 13px;">
                    {qrcode}
                </td>
                <td style="padding-bottom: 10px; padding-top: 13px;">
                    <div>Code: <b>{code.code}</b></div>
                    {serial}
                </td>
                                '''
            cod2 = f'''
                <td style="padding-bottom: 10px; padding-top: 13px;">
                    <div>Code: <b>{code.code}</b></div>
                    {serial}
                </td>
                <td style="padding-bottom: 10px; padding-top: 13px;">
                    {qrcode}
                </td>
                                '''
            cod = cod2 if (i % 2) == 0 else cod1
            
            codes += f'''
             <tr>
                <td colspan={2} style="{border}">
                    <table align="center">
                        <tbody>
                            <tr>
                                {cod}
                            </tr>
                        </tbody>
                    </table>
                </td>
            </tr>
            '''
            image = qr_code_mime(code.code, imgname+'.png')
            image.add_header('Content-ID', '<{}.png>'.format(imgname))
            image.add_header('Content-Disposition', 'inline; filename="{}.png"'.format(imgname))
        
            imageslist.append(image)
            i+=1
            
        imgsrc = f'https://digicod.eu{item.product.brand.image}'
        if item.product.brand.image[0:4] == 'http':
            imgsrc = item.product.brand.image
        product += f'''
        <tr>
          <td style="background: #FAFAFA; border: 5px solid #E7E7E7; border-radius: 15px; padding-left:15px; padding-right:15px; padding-top:15px; padding-bottom:15px;">
            <table width='100%'>
              <tbody>
                <tr>
                  <td>
                    <img style="border-radius: 10px" src={imgsrc} width='70px' height='70px' alt="">
                  </td>
                   <td align='center'>
                    {item.product.title} x{item.qty}
                  </td>
                   <td align='right' style="min-width: 50px">
                    {round(item.final_price * decimal.Decimal(order.json.get('curprice')),tofx)} {order.cart.currency.sign}
                  </td>
                </tr>
              </tbody>
            </table>
            <table  align="center">
              <tbody>
                {codes}
              </tbody>
            </table>
          </td>
        </tr>
        '''
    wallet_payment = ''
    if order.cart.wallet_payment > 0:
        wallet_payment = f'''
        <tr>
                        <td align="right" style="padding: 5px;margin: 0;font-family: Arial, Verdana, sans-serif;">
                         Paid with Wallet: {round(order.cart.wallet_payment * decimal.Decimal(order.json.get('curprice')),tofx)} {order.cart.currency.sign}
                        </td>
                      </tr>
        '''
    trans_cost = ''
    if order.cart.process_fee > 0:
        trans_cost = F'''
         <tr>
                        <td align="right" style="padding: 5px;margin: 0;font-family: Arial, Verdana, sans-serif;">
                         Transactions cost: {round(order.cart.process_fee * decimal.Decimal(order.json.get('curprice')),tofx)} {order.cart.currency.sign}
                        </td>
                      </tr>
        '''
    paymentmethod = ''
    if order.cart.payment_method_payment > 0:
        paymentmethod = f'''
         <tr>
                        <td align="right" style="padding: 5px;margin: 0;font-family: Arial, Verdana, sans-serif;">
                          Paid with {order.cart.payment_method.name}: {round(order.cart.payment_method_payment * decimal.Decimal(order.json.get('curprice')),tofx)} {order.cart.currency.sign}
                        </td>
                      </tr>
        '''
    html_email = f'''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="en">
<head>
  <meta http-equiv="content-type" content="text/html" charset="UTF-8">
  
</head>
<body style="background-color: #ffffff;padding: 20px 0;margin: 0 auto;font-family: Arial, Verdana, sans-serif;">
  <table border="0" class="wrap_table" align="center" valign="middle" cellspacing="0" cellpadding="0" style="max-width: 600px;min-width: 350px;width: 100%;border-spacing: 0;padding: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-family: Arial, Verdana, sans-serif;background-color: #E7E7E7;">
    <tbody>
      <tr>
        <td class="td_wrap_header" style="padding: 0;margin: 0;font-family: Arial, Verdana, sans-serif;">
          <table bgcolor="#373836" cellpadding="0" align="center" valign="middle" class="table_header" border="0" style="max-width: 600px;min-width: 350px;width: 100%;border-spacing: 0;padding: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-family: Arial, Verdana, sans-serif;background-color: #fff;">
            <tbody>
              <tr>
                <td class="td_header" align="center" style="padding: 7px;margin: 0;font-family: Arial, Verdana, sans-serif;">
                  <a href="https://digicod.eu" style="text-decoration: none;">
                  <img src="https://digicod.eu/media/logo.png" alt="digicod" class="header_logo" style="outline: none;-ms-interpolation-mode: bicubic;display: block;margin: 0;padding: 0;width: 150px;">
                  </a>
                </td>
              </tr>
            </tbody>
          </table>
        </td>
      </tr>
      <tr>
        <td class="td_wrap_content" style="padding: 0;margin: 0;font-family: Arial, Verdana, sans-serif;">
          <table class="table_content" align="center" valign="middle" cellpadding="0" bgcolor="#FAFAFA" border="0" cellspacing="0" style="max-width: 600px;min-width: 350px;width: 100%;border-spacing: 0;padding: 0px 15px 0px 15px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-family: Arial, Verdana, sans-serif;background-color: #E7E7E7;">
            <tbody>
              <tr>
                <td style="padding: 0;margin: 0;font-family: Arial, Verdana, sans-serif;">
                  <h3 class="h3" style="margin-top: 15px;margin-left: 15px;margin-right: 15px;margin-bottom: 15px;text-align: center;">Your order</h3>
                  {product}
                </td>
              </tr>
              <tr>
                <td class="td_card_table" style="padding: 0;margin: 0;font-family: Arial, Verdana, sans-serif;">
                 
                  <table align="center" valign="middle" class="warning_info_table" cellspacing="0" cellpadding="0" border="0" style="max-width: 600px;min-width: 350px;width: 100%;border-spacing: 0;padding: 5px 17px 5px 0px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-family: Arial, Verdana, sans-serif;font-size: 15px;padding-bottom: 10px;">
                    <tbody>
                      <tr>
                        <td align="right" style="padding: 5px;margin: 0;font-family: Arial, Verdana, sans-serif;">
                          Subtotal: {round(order.cart.final_price * decimal.Decimal(order.json.get('curprice')),tofx)} {order.cart.currency.sign}
                        </td>
                      </tr>
                       {wallet_payment}
                        {trans_cost}
                        {paymentmethod}
                       <tr>
                        <td align="right" style="padding: 5px;margin: 0;font-family: Arial, Verdana, sans-serif;">
                         Total: {round(order.cart.order_final_price * decimal.Decimal(order.json.get('curprice')),tofx)} {order.cart.currency.sign}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </td>
              </tr>
            </tbody>
          </table>
        </td>
      </tr>
      <tr>
        <td class="td_wrap_footer" style="padding: 0;margin: 0;font-family: Arial, Verdana, sans-serif;">
          <table class="table_footer" width="100%" align="center" valign="middle" bgcolor="#FAFAFA" cellspacing="0" cellpadding="0" border="0" style="max-width: 600px;min-width: 350px;width: 100%;border-spacing: 0;padding: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-family: Arial, Verdana, sans-serif;background-color: #E7E7E7;">
            <tbody>
              <tr>
                <td align="center" class="td_footer" style="padding: 0;margin: 0;font-family: Arial, Verdana, sans-serif;border-top: 1px solid #373836;font-size: 11px;color: grey;line-height: 15px;padding-top: 10px;padding-bottom: 10px;">
                  Copyright © 2021 DIGIDAG LTD, All rights reserved. <br>
                  <a href="https://www.digicod.eu" style="text-decoration: none;">www.digicod.eu</a> |
                  <a href="mailto:support@digicod.eu" style="text-decoration: none;">support@digicod.eu</a>
                </td>
              </tr>
            </tbody>
          </table>
        </td>
      </tr>
    </tbody>
  </table>
</body>
</html>'''
    
    
    message = html_email
    subject, from_email, to = f"Thank you for your order #{order.id}", '"DIGICOD" <support@digicod.eu>', order.del_email
    text_content = f'Your order at digicod.eu'
    html_content = message
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # msg.content_subtype = 'html'  # Main content is text/html
    msg.mixed_subtype = 'related'  # This is critical, otherwise images will be displayed as attachments!
    for item in imageslist.copy():
        msg.attach(item)
    msg.attach_alternative(html_content, "text/html")
    msg.attach_file(f'/home/dcback/eshop/pdf/invoices/invoice_{invnr}.pdf')
    r = msg.send()

  
    subject, from_email, to = f"Thank you for your order #{order.id} - {order.del_email}", '"DIGICOD" <support@digicod.eu>', 'order@digicod.eu'
    text_content = f'Your order at digicod.eu'
    html_content = message
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # msg.content_subtype = 'html'  # Main content is text/html
    msg.mixed_subtype = 'related'  # This is critical, otherwise images will be displayed as attachments!

    for item in imageslist.copy():
        msg.attach(item)
    msg.attach_alternative(html_content, "text/html")
    msg.attach_file(f'/home/dcback/eshop/pdf/invoices/invoice_{invnr}.pdf')
    msg.send()
    return r
# orderemail(876430)