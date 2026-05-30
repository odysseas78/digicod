import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from eshop.models import Customer


#,"coxah@web.de", "m.odysseas78@gmail.com", "o.martasidis@yahoo.de"
def kunden_email():

    users = Customer.objects.all().exclude(user__last_login=None).exclude(user__id=1).exclude(user__username='coxah')
    for user in users:
        html_email = f'''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
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
                          <a href="https://digicod.eu" style="text-decoration: none;"><img src="https://staging.giftcoins.io/media/logo.png" alt="giftcoins_logo" class="header_logo" style="outline: none;-ms-interpolation-mode: bicubic;display: block;margin: 0;padding: 0;width: 150px;"></a>
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
                          <h3 class="h3" style="margin-top: 15px;margin-left: 15px;margin-right: 15px;margin-bottom: 15px;text-align: center;">The new digicod.eu website.</h3>
                          <tr>
                          <td style="background: #FAFAFA;border-radius: 15px;padding-left: 15px;padding-top: 15px;padding-right: 15px;padding-bottom: 15px;margin-top: 15px;margin-bottom: 15px;margin-left: 15px;margin-right: 15px; ">
                            <table width='100%'>
                              <tbody>
                                <tr>
                                  <td>
                                    <p>Hello {user.user.username}!</p>
                                    <p>The service will be closed from around the evening of March 19, 2022 until around the end of the month.</p>
                                    <p>Please understand and thank you for your trust.</p>
                                  </td>
                                </tr>
                              </tbody>
                            </table>
                          </td>
                        </tr>
                          <tr>
                          <td style="border-radius: 15px;padding-left: 10px;padding-top: 10px;padding-right: 10px;padding-bottom: 10px;">

                          </td>
                        </tr>
                        </td>
                      </tr>
                      <tr>
                        <td class="td_card_table" style="padding: 0;margin: 0;font-family: Arial, Verdana, sans-serif;">

                          <table align="center" valign="middle" class="warning_info_table" cellspacing="0" cellpadding="0" border="0" style="max-width: 600px;min-width: 350px;width: 100%;border-spacing: 0;padding: 5px 17px 5px 0px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-family: Arial, Verdana, sans-serif;font-size: 15px;padding-bottom: 10px;">
                            <tbody>
                              <tr>
                                <td align="left" style="padding: 5px;margin: 0;font-family: Arial, Verdana, sans-serif;">
                                  Thank you for using <a href='hhtps://digicod.eu'>digicod.eu</a>!
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
        </html>
        '''
        # message = html_email
        # subject, from_email, to = f"The new digicod.eu website", '"DIGICOD" <support@digicod.eu>', user.user.email
        # text_content = f'The new digicod.eu website'
        # html_content = message
        # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()

        print(user.user.email)
        print(users.count())
if __name__ == "__main__":
    kunden_email()
# users = Customer.objects.all().exclude(user__last_login=None).exclude(user__id=1).exclude(user__username='coxah')

