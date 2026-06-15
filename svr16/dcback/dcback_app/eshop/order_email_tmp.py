import os, sys
sys.path.insert(0, '/home/dcback')
import django
import os
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
          <td style="background: #FAFAFA; border: 5px solid #E7E7E7; border-radius: 15px; padding-left:12px; padding-right:12px; padding-top:12px; padding-bottom:12px;">
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
    
    tmplt = '''
    <!doctype html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">

<head>
  <title>
  </title>
  <!--[if !mso]><!-->
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <!--<![endif]-->
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style type="text/css">
    #outlook a {
      padding: 0;
    }

    body {
      margin: 0;
      padding: 0;
      -webkit-text-size-adjust: 100%;
      -ms-text-size-adjust: 100%;
    }

    table,
    td {
      border-collapse: collapse;
      mso-table-lspace: 0pt;
      mso-table-rspace: 0pt;
    }

    img {
      border: 0;
      height: auto;
      line-height: 100%;
      outline: none;
      text-decoration: none;
      -ms-interpolation-mode: bicubic;
    }

    p {
      display: block;
      margin: 13px 0;
    }
  </style>
  <!--[if mso]>
        <noscript>
        <xml>
        <o:OfficeDocumentSettings>
          <o:AllowPNG/>
          <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
        </xml>
        </noscript>
        <![endif]-->
  <!--[if lte mso 11]>
        <style type="text/css">
          .mj-outlook-group-fix { width:100% !important; }
        </style>
        <![endif]-->
  <!--[if !mso]><!-->
  <link href="https://fonts.googleapis.com/css?family=Ubuntu:300,400,500,700" rel="stylesheet" type="text/css">
  <style type="text/css">
    @import url(https://fonts.googleapis.com/css?family=Ubuntu:300,400,500,700);
  </style>
  <!--<![endif]-->
  <style type="text/css">
    @media only screen and (min-width:480px) {
      .mj-column-per-100 {
        width: 100% !important;
        max-width: 100%;
      }

      .mj-column-per-50 {
        width: 50% !important;
        max-width: 50%;
      }

      .mj-column-per-25 {
        width: 25% !important;
        max-width: 25%;
      }

      .mj-column-per-75 {
        width: 75% !important;
        max-width: 75%;
      }

      .mj-column-per-33-333333333333336 {
        width: 33.333333333333336% !important;
        max-width: 33.333333333333336%;
      }
    }
  </style>
  <style media="screen and (min-width:480px)">
    .moz-text-html .mj-column-per-100 {
      width: 100% !important;
      max-width: 100%;
    }

    .moz-text-html .mj-column-per-50 {
      width: 50% !important;
      max-width: 50%;
    }

    .moz-text-html .mj-column-per-25 {
      width: 25% !important;
      max-width: 25%;
    }

    .moz-text-html .mj-column-per-75 {
      width: 75% !important;
      max-width: 75%;
    }

    .moz-text-html .mj-column-per-33-333333333333336 {
      width: 33.333333333333336% !important;
      max-width: 33.333333333333336%;
    }
  </style>
  <style type="text/css">
    @media only screen and (max-width:480px) {
      table.mj-full-width-mobile {
        width: 100% !important;
      }

      td.mj-full-width-mobile {
        width: auto !important;
      }
    }
  </style>
</head>

<body style="word-spacing:normal;background-color:#ffffff;">
  <div style="background-color:#ffffff;">
    <!--[if mso | IE]><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
    <div style="margin:0px auto;max-width:600px;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
        <tbody>
          <tr>
            <td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:20px;padding-top:20px;text-align:center;">
              <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="" style="width:600px;" ><![endif]-->
              <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0;line-height:0;text-align:left;display:inline-block;width:100%;direction:ltr;">
                <!--[if mso | IE]><table border="0" cellpadding="0" cellspacing="0" role="presentation" ><tr><td style="vertical-align:top;width:300px;" ><![endif]-->
                <div class="mj-column-per-50 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:50%;">
                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                    <tbody>
                      <tr>
                        <td align="left" style="font-size:0px;padding:10px 25px;padding-right:25px;padding-left:25px;word-break:break-word;">
                          <div style="font-family:Ubuntu, Helvetica, Arial, sans-serif;font-size:11px;line-height:1;text-align:left;color:#000000;">[[HEADLINE]]</div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <!--[if mso | IE]></td><td style="vertical-align:top;width:300px;" ><![endif]-->
                <div class="mj-column-per-50 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:50%;">
                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                    <tbody>
                      <tr>
                        <td align="right" style="font-size:0px;padding:10px 25px;padding-right:25px;padding-left:25px;word-break:break-word;">
                          <div style="font-family:Ubuntu, Helvetica, Arial, sans-serif;font-size:11px;line-height:1;text-align:right;color:#000000;">[PERMALINK_LABEL]]</div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <!--[if mso | IE]></td></tr></table><![endif]-->
              </div>
              <!--[if mso | IE]></td></tr></table><![endif]-->
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!--[if mso | IE]></td></tr></table><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
    <div style="margin:0px auto;max-width:600px;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
        <tbody>
          <tr>
            <td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:0px;padding-top:0;text-align:center;">
              <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="" style="vertical-align:top;width:150px;" ><![endif]-->
              <div class="mj-column-per-25 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                  <tbody>
                    <tr>
                      <td align="center" style="font-size:0px;padding:0px;word-break:break-word;">
                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                          <tbody>
                            <tr>
                              <td style="width:147px;">
                                <a href="https://mjml.io" target="_blank" style="text-decoration: none;">
                                  <img alt height="auto" src="http://191n.mj.am/img/191n/3s/xm0.png" style="border:0;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:13px;" width="147">
                                </a>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!--[if mso | IE]></td><td class="" style="vertical-align:top;width:450px;" ><![endif]-->
              <div class="mj-column-per-75 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                  <tbody>
                    <tr>
                      <td align="left" style="font-size:0px;padding:0 25px;word-break:break-word;">
                        <div style="font-family:Ubuntu, Helvetica, Arial, sans-serif;font-size:19px;font-weight:bold;line-height:1;text-align:left;color:#000000;">Special pre sale information</div>
                      </td>
                    </tr>
                    <tr>
                      <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                        <div style="font-family:Ubuntu, Helvetica, Arial, sans-serif;font-size:11px;line-height:1;text-align:left;color:#000000;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin rutrum enim eget magna efficitur, eu semper augue semper. Aliquam erat volutpat. Proin rutrum enim eget magna efficitur.</div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!--[if mso | IE]></td></tr></table><![endif]-->
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!--[if mso | IE]></td></tr></table><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" bgcolor="#fcc245" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
    <div style="background:#fcc245;background-color:#fcc245;margin:0px auto;max-width:600px;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#fcc245;background-color:#fcc245;width:100%;">
        <tbody>
          <tr>
            <td style="direction:ltr;font-size:0px;padding:20px 0;text-align:center;">
              <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="" style="vertical-align:top;width:600px;" ><![endif]-->
              <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                  <tbody>
                    <tr>
                      <td align="center" style="font-size:0px;padding:0 25px;word-break:break-word;">
                        <div style="font-family:Ubuntu, Helvetica, Arial, sans-serif;font-size:20px;line-height:1;text-align:center;color:#000000;"><span style="color: rgb(89, 89, 89);">PRE SALE BEGINS TODAY</span> AT 9 AM</div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!--[if mso | IE]></td></tr></table><![endif]-->
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!--[if mso | IE]></td></tr></table><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" bgcolor="#ffffff" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><v:rect style="width:600px;" xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false"><v:fill origin="0.5, 0" position="0.5, 0" src="http://191n.mj.am/img/191n/3s/xl9.jpg" color="#ffffff" type="tile" size="1,1" aspect="atleast" /><v:textbox style="mso-fit-shape-to-text:true" inset="0,0,0,0"><![endif]-->
    <div style="background:#ffffff url(http://191n.mj.am/img/191n/3s/xl9.jpg) center top / cover repeat;background-position:center top;background-repeat:repeat;background-size:cover;margin:0px auto;max-width:600px;">
      <div style="line-height:0;font-size:0;">
        <table align="center" background="http://191n.mj.am/img/191n/3s/xl9.jpg" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#ffffff url(http://191n.mj.am/img/191n/3s/xl9.jpg) center top / cover repeat;background-position:center top;background-repeat:repeat;background-size:cover;width:100%;">
          <tbody>
            <tr>
              <td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:20px;padding-top:20px;text-align:center;">
                <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="" style="vertical-align:top;width:600px;" ><![endif]-->
                <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                    <tbody>
                      <tr>
                        <td align="center" vertical-align="middle" style="font-size:0px;padding:305px 25px 0;word-break:break-word;">
                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:separate;line-height:100%;">
                            <tr>
                              <td align="center" bgcolor="#fcc245" role="presentation" style="border:none;border-radius:3px;cursor:auto;mso-padding-alt:10px 25px;background:#fcc245;" valign="middle">
                                <a href="https://mjml.io" style="display: inline-block; background: #fcc245; color: #000000; font-family: Ubuntu, Helvetica, Arial, sans-serif; font-size: 18px; font-weight: normal; line-height: 120%; margin: 0; text-transform: none; padding: 10px 25px; mso-padding-alt: 0px; border-radius: 3px; text-decoration: none;" target="_blank"> BUY TICKETS </a>
                              </td>
                            </tr>
                          </table>
                        </td>
                      </tr>
                      <tr>
                        <td align="center" style="font-size:0px;padding:10px 25px;padding-top:10px;padding-right:25px;padding-bottom:10px;padding-left:25px;word-break:break-word;">
                          <div style="font-family:Ubuntu, Helvetica, Arial, sans-serif;font-size:13px;line-height:1;text-align:center;color:#000000;"><span style="color: rgb(255, 255, 255);">PASSWORD : YULAN03</span></div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <!--[if mso | IE]></td></tr></table><![endif]-->
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <!--[if mso | IE]></v:textbox></v:rect></td></tr></table><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
    <div style="margin:0px auto;max-width:600px;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
        <tbody>
          <tr>
            <td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:20px;padding-top:20px;text-align:center;">
              <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="" style="vertical-align:middle;width:150px;" ><![endif]-->
              <div class="mj-column-per-25 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:middle;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:middle;" width="100%">
                  <tbody>
                    <tr>
                      <td align="center" style="font-size:0px;padding:0px;word-break:break-word;">
                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                          <tbody>
                            <tr>
                              <td style="width:147px;">
                                <img alt="CD" height="auto" src="http://191n.mj.am/img/191n/3s/xmw.jpg" style="border:0;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:13px;" width="147">
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!--[if mso | IE]></td><td class="" style="vertical-align:middle;width:150px;" ><![endif]-->
              <div class="mj-column-per-25 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:middle;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:middle;" width="100%">
                  <tbody>
                    <tr>
                      <td align="center" style="font-size:0px;padding:0 25px;word-break:break-word;">
                        <div style="font-family:Ubuntu, Helvetica, Arial, sans-serif;font-size:16px;line-height:1;text-align:center;color:#000000;">LAST ALBUM AVAILABLE <span style="font-weight: bold;">12,99&#x20AC;</span></div>
                      </td>
                    </tr>
                    <tr>
                      <td align="center" vertical-align="middle" style="font-size:0px;padding:10px 0;word-break:break-word;">
                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:separate;line-height:100%;">
                          <tr>
                            <td align="center" bgcolor="#fcc245" role="presentation" style="border:none;border-radius:3px;cursor:auto;mso-padding-alt:10px 25px;background:#fcc245;" valign="middle">
                              <a href="https://mjml.io" style="display: inline-block; background: #fcc245; color: #000000; font-family: Ubuntu, Helvetica, Arial, sans-serif; font-size: 17px; font-weight: normal; line-height: 120%; margin: 0; text-transform: none; padding: 10px 25px; mso-padding-alt: 0px; border-radius: 3px; text-decoration: none;" target="_blank"> BUY IT ! </a>
                            </td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!--[if mso | IE]></td><td class="" style="vertical-align:top;width:300px;" ><![endif]-->
              <div class="mj-column-per-50 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                  <tbody>
                    <tr>
                      <td align="center" style="font-size:0px;padding:0px;word-break:break-word;">
                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                          <tbody>
                            <tr>
                              <td style="width:290px;">
                                <a href="https://mjml.io" target="_blank" style="text-decoration: none;">
                                  <img alt="Play now and win your vip pass" height="auto" src="http://191n.mj.am/img/191n/3s/xmx.jpg" style="border:0;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:13px;" width="290">
                                </a>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!--[if mso | IE]></td></tr></table><![endif]-->
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!--[if mso | IE]></td></tr></table><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
    <div style="margin:0px auto;max-width:600px;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
        <tbody>
          <tr>
            <td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:20px;padding-top:20px;text-align:center;">
              <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="" style="vertical-align:top;width:600px;" ><![endif]-->
              <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                  <tbody>
                    <tr>
                      <td align="center" vertical-align="middle" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:separate;line-height:100%;">
                          <tr>
                            <td align="center" bgcolor="#000000" role="presentation" style="border:none;border-radius:0px;cursor:auto;mso-padding-alt:10px 25px;background:#000000;" valign="middle">
                              <a href="https://mjml.io" style="display: inline-block; background: #000000; color: #fcc245; font-family: Ubuntu, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: normal; line-height: 120%; margin: 0; text-transform: none; padding: 10px 25px; mso-padding-alt: 0px; border-radius: 0px; text-decoration: none;" target="_blank"> OUR PARTNERS </a>
                            </td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!--[if mso | IE]></td></tr></table><![endif]-->
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!--[if mso | IE]></td></tr></table><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
    <div style="margin:0px auto;max-width:600px;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
        <tbody>
          <tr>
            <td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:20px;padding-top:0;text-align:center;">
              <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="" style="vertical-align:top;width:150px;" ><![endif]-->
              <div class="mj-column-per-25 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                  <tbody>
                    <tr>
                      <td align="center" style="font-size:0px;padding:0 0 10px 0;word-break:break-word;">
                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                          <tbody>
                            <tr>
                              <td style="width:95px;">
                                <a href="https://mjml.io" target="_blank" style="text-decoration: none;">
                                  <img alt="Partner logo" height="auto" src="http://191n.mj.am/img/191n/3s/y2.jpg" style="border:0;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:13px;" width="95">
                                </a>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!--[if mso | IE]></td><td class="" style="vertical-align:top;width:150px;" ><![endif]-->
              <div class="mj-column-per-25 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                  <tbody>
                    <tr>
                      <td align="center" style="font-size:0px;padding:0 0 10px 0;word-break:break-word;">
                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                          <tbody>
                            <tr>
                              <td style="width:95px;">
                                <a href="https://mjml.io" target="_blank" style="text-decoration: none;">
                                  <img alt="Partner logo" height="auto" src="http://191n.mj.am/img/191n/3s/y2.jpg" style="border:0;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:13px;" width="95">
                                </a>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!--[if mso | IE]></td><td class="" style="vertical-align:top;width:150px;" ><![endif]-->
              <div class="mj-column-per-25 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                  <tbody>
                    <tr>
                      <td align="center" style="font-size:0px;padding:0 0 10px 0;word-break:break-word;">
                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                          <tbody>
                            <tr>
                              <td style="width:95px;">
                                <a href="https://mjml.io" target="_blank" style="text-decoration: none;">
                                  <img alt="Partner logo" height="auto" src="http://191n.mj.am/img/191n/3s/y2.jpg" style="border:0;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:13px;" width="95">
                                </a>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!--[if mso | IE]></td><td class="" style="vertical-align:top;width:150px;" ><![endif]-->
              <div class="mj-column-per-25 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                  <tbody>
                    <tr>
                      <td align="center" style="font-size:0px;padding:0 0 10px 0;word-break:break-word;">
                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                          <tbody>
                            <tr>
                              <td style="width:95px;">
                                <a href="https://mjml.io" target="_blank" style="text-decoration: none;">
                                  <img alt="Partner logo" height="auto" src="http://191n.mj.am/img/191n/3s/y2.jpg" style="border:0;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:13px;" width="95">
                                </a>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!--[if mso | IE]></td></tr></table><![endif]-->
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!--[if mso | IE]></td></tr></table><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
    <div style="margin:0px auto;max-width:600px;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
        <tbody>
          <tr>
            <td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:20px;padding-top:20px;text-align:center;">
              <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="" style="vertical-align:top;width:600px;" ><![endif]-->
              <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                  <tbody>
                    <tr>
                      <td align="center" style="font-size:0px;padding:0 25px;word-break:break-word;">
                        <div style="font-family:Ubuntu, Helvetica, Arial, sans-serif;font-size:13px;font-weight:bold;line-height:1;text-align:center;color:#000000;">Terms and conditions:</div>
                      </td>
                    </tr>
                    <tr>
                      <td align="center" style="font-size:0px;padding:0 25px 10px 25px;word-break:break-word;">
                        <div style="font-family:Ubuntu, Helvetica, Arial, sans-serif;font-size:13px;line-height:1;text-align:center;color:#000000;">
                          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin rutrum enim eget magna efficitur, eu semper augue semper. Aliquam erat volutpat. Cras id dui lectus. Vestibulum sed finibus lectus, sit amet suscipit nibh. Proin nec commodo purus. Sed eget nulla elit. Nulla aliquet mollis faucibus.</p>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!--[if mso | IE]></td></tr></table><![endif]-->
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!--[if mso | IE]></td></tr></table><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" bgcolor="#fcc245" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
    <div style="background:#fcc245;background-color:#fcc245;margin:0px auto;max-width:600px;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#fcc245;background-color:#fcc245;width:100%;">
        <tbody>
          <tr>
            <td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:0px;padding-top:0;text-align:center;">
              <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="" style="vertical-align:middle;width:200px;" ><![endif]-->
              <div class="mj-column-per-33-333333333333336 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:middle;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:middle;" width="100%">
                  <tbody>
                    <tr>
                      <td align="center" style="font-size:0px;padding:0 25px;word-break:break-word;">
                        <div style="font-family:Ubuntu, Helvetica, Arial, sans-serif;font-size:20px;font-weight:bold;line-height:1;text-align:center;color:#000000;">
                          <p>0800 123 456</p>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td align="center" style="font-size:0px;padding:0 25px;word-break:break-word;">
                        <div style="font-family:Ubuntu, Helvetica, Arial, sans-serif;font-size:13px;line-height:1;text-align:center;color:#FFFFFF;">
                          <p>Privacy policy</p>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!--[if mso | IE]></td><td class="" style="vertical-align:middle;width:200px;" ><![endif]-->
              <div class="mj-column-per-33-333333333333336 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:middle;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:middle;" width="100%">
                  <tbody>
                    <tr>
                      <td align="center" style="font-size:0px;padding:0px;word-break:break-word;">
                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                          <tbody>
                            <tr>
                              <td style="width:133px;">
                                <a href="https://mjml.io" target="_blank" style="text-decoration: none;">
                                  <img alt="Logo yellow" height="auto" src="http://191n.mj.am/img/191n/3s/yp.jpg" style="border:0;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:13px;" width="133">
                                </a>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!--[if mso | IE]></td><td class="" style="vertical-align:middle;width:200px;" ><![endif]-->
              <div class="mj-column-per-33-333333333333336 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:middle;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:middle;" width="100%">
                  <tbody>
                    <tr>
                      <td align="center" style="font-size:0px;padding:30px;word-break:break-word;">
                        <!--[if mso | IE]><table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" ><tr><td><![endif]-->
                        <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="float:none;display:inline-table;">
                          <tr>
                            <td style="padding:4px;vertical-align:middle;">
                              <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#3b5998;border-radius:3px;width:20px;">
                                <tr>
                                  <td style="font-size:0;height:20px;vertical-align:middle;width:20px;">
                                    <a href="https://www.facebook.com/sharer/sharer.php?u=[[SHORT_PERMALINK]]" target="_blank" style="text-decoration: none;">
                                      <img height="20" src="https://www.mailjet.com/images/theme/v1/icons/ico-social/facebook.png" style="border-radius:3px;display:block;" width="20">
                                    </a>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </table>
                        <!--[if mso | IE]></td><td><![endif]-->
                        <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="float:none;display:inline-table;">
                          <tr>
                            <td style="padding:4px;vertical-align:middle;">
                              <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#55acee;border-radius:3px;width:20px;">
                                <tr>
                                  <td style="font-size:0;height:20px;vertical-align:middle;width:20px;">
                                    <a href="https://twitter.com/intent/tweet?url=[[SHORT_PERMALINK]]" target="_blank" style="text-decoration: none;">
                                      <img height="20" src="https://www.mailjet.com/images/theme/v1/icons/ico-social/twitter.png" style="border-radius:3px;display:block;" width="20">
                                    </a>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </table>
                        <!--[if mso | IE]></td><td><![endif]-->
                        <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="float:none;display:inline-table;">
                          <tr>
                            <td style="padding:4px;vertical-align:middle;">
                              <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#dc4e41;border-radius:3px;width:20px;">
                                <tr>
                                  <td style="font-size:0;height:20px;vertical-align:middle;width:20px;">
                                    <a href="https://plus.google.com/share?url=[[SHORT_PERMALINK]]" target="_blank" style="text-decoration: none;">
                                      <img height="20" src="https://www.mailjet.com/images/theme/v1/icons/ico-social/google-plus.png" style="border-radius:3px;display:block;" width="20">
                                    </a>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </table>
                        <!--[if mso | IE]></td></tr></table><![endif]-->
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!--[if mso | IE]></td></tr></table><![endif]-->
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!--[if mso | IE]></td></tr></table><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
    <div style="margin:0px auto;max-width:600px;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
        <tbody>
          <tr>
            <td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:20px;padding-top:20px;text-align:center;">
              <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="" style="vertical-align:top;width:600px;" ><![endif]-->
              <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                  <tbody>
                    <tr>
                      <td align="center" style="font-size:0px;padding:0 25px;word-break:break-word;">
                        <div style="font-family:Ubuntu, Helvetica, Arial, sans-serif;font-size:11px;line-height:1;text-align:center;color:#000000;">
                          <p>[[DELIVERY_INFO]]</p>
                          <p>[[POSTAL_ADDRESS]]</p>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!--[if mso | IE]></td></tr></table><![endif]-->
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!--[if mso | IE]></td></tr></table><![endif]-->
  </div>
</body>

</html>'''
    
    message = tmplt
    subject, from_email, to = f"Thank you for your order #{order.id}", '"DIGICOD" <support@digicod.eu>', ['m.odysseas78@gmail.com', 'coxah@web.de']
    text_content = f'Your order at digicod.eu'
    html_content = message
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    # msg.content_subtype = 'html'  # Main content is text/html
    msg.mixed_subtype = 'related'  # This is critical, otherwise images will be displayed as attachments!
    for item in imageslist.copy():
        msg.attach(item)
    msg.attach_alternative(html_content, "text/html")
    msg.attach_file(f'/home/dcback/eshop/pdf/invoices/invoice_{invnr}.pdf')
    msg.send()

  
    subject, from_email, to = f"Thank you for your order #{order.id} - {order.del_email}", '"DIGICOD" <support@digicod.eu>', ['o.martasidis@yahoo.de']
    text_content = f'Your order at digicod.eu'
    html_content = message
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    # msg.content_subtype = 'html'  # Main content is text/html
    msg.mixed_subtype = 'related'  # This is critical, otherwise images will be displayed as attachments!

    for item in imageslist.copy():
        msg.attach(item)
    msg.attach_alternative(html_content, "text/html")
    msg.attach_file(f'/home/dcback/eshop/pdf/invoices/invoice_{invnr}.pdf')
    msg.send()

# orderemail(872990)