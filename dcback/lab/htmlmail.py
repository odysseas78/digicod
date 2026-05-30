import os
import django
import os
from eshop.pdf.createpdf import create_invoice
import django
import decimal

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from eshop.models import Order
from django.core.mail import EmailMultiAlternatives



html_email = """
<table width="100%" border="0" cellspacing="0" cellpadding="0" class="iosfix">
  <tbody><tr> 
  <td align="center">

  
  <img alt="Embedded SVG Fox" width="100" id="svgimglayer" src="https://digicod.eu/media/logo.svg">


  </td>
</tr>
<tr>
  <td align="center" style="font-size:4px;line-height:4px;color:#308972">
  	<unsubscribe style="font-size:4px;line-height:4px;color:#308972;text-decoration:none">click here if you are stupid</unsubscribe>
  </td>  
</tr>
</tbody></table>"""



# message = html_email
# subject, from_email, to = f"Thank you for your order ", '"DIGICOD" <support@digicod.eu>', ['m.odysseas78@gmail.com']
# text_content = f'Your order at digicod.eu'
# html_content = message
# msg = EmailMultiAlternatives(subject, text_content, from_email, [*to])
# msg.attach_alternative(html_content, "text/html")
# msg.send()

