import secrets, redis, pickle
from djoser.utils import login_user, logout_user, settings
from eshop.wallet.wallet import CoinWallet
from eshop.models import Message
from django.core.mail import EmailMultiAlternatives, send_mail
from loguru import logger
from django.contrib.auth.tokens import default_token_generator

cw = CoinWallet

def getCookies(request, key):
    try:
        from http.cookies import SimpleCookie
    except ImportError:
        from Cookie import SimpleCookie # type: ignore
    cookies = SimpleCookie(request.headers.get('set-cookie'))
    value = request.COOKIES.get(key) if request.COOKIES.get(key) else cookies.get(key).value if cookies.get(key) else None
    return value

def logfn1(name,path='logs/'):
    logger.add(f"{path}{name}.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == name)
    return logger.bind(name=name)

class Authent:
    
    def __init__(self, request=None, vars=None) -> None:
        from eshop.models import User, Customer
        self.User = User
        self.Customer = Customer
        self.request = request
        self.vars = vars
        self.redis = redis.Redis(host='localhost', port=6379, decode_responses=False)
        
    def getOrCreateUser(self):
        user, create = self.User.objects.get_or_create(
        email=self.vars.get('email'),
        defaults={
                    'username':self.vars.get('email'),
                }
        )
        customer, create2 = self.Customer.objects.get_or_create(
            user=user,
            defaults={
                'rolle':'new',
                'status':'Unverified',
                }
        )
   
        return user
    
    
    def sendUrl(self):
        print(self.vars)
        fprint = getCookies(self.request, '_polz')
        user = self.getOrCreateUser()
        email = user.email
        r = self.redis
        urltoken = default_token_generator.make_token(user)
        urltoken = urltoken
        dd = {'email':email, 'fprint':fprint, 'pathname':self.vars.get('pathname')}
        if self.vars.get('calledfrom'):
            dd.update({'calledfrom':self.vars.get('calledfrom')})
        g = r.set(urltoken, pickle.dumps(dd),ex=3*60)
        
        with open('api/emailtemplates/login_url_token_send.html', 'r') as file:
            content = file.read()
        res = content.replace('$login_url', f'{self.request.build_absolute_uri("/login/")+urltoken}')
            
        html_email = res
        message = html_email
        subject, from_email, to = f"Login to your account", '"DIGICOD" <support@digicod.eu>', email
        text_content = f'Login to your account {self.request.build_absolute_uri("/login/")+urltoken}'
        html_content = message
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        res = msg.send()
        
        if res == 1:
            return {'type':'success', 'message': 'An email was sent successfully. Please follow the instructions in the email.'}
        else:
            return {'type':'error','message': 'Something went wrong. Pleace try again.'}
        
    def authenticate(self):
        fprint = getCookies(self.request, '_polz')
        r = self.redis
        userdata = r.get(self.vars.get('urltoken'))
        if not userdata:
            return {'type':'error','message': 'The link is invalid or has expired.'}
        udata = pickle.loads(userdata)
        email = udata.get('email')
        calledfrom = udata.get('calledfrom')
        
        if fprint != udata.get('fprint'):
            return {'type':'error','message': 'For security reasons, your login was declined. Please try again later.'}
        # logfn1('authenticate').info(email)
        user = self.User.objects.filter(email=email).first()
        
        qs = cw.objects.filter(user__email=email).first()
        # if not qs:
        #     cw().create_user_wallet(user=user)
        
        settings.TOKEN_MODEL.objects.filter(user=user).delete()
        token = login_user(request=self.request, user=user)
        auth_token = token.key
        token.save(fprint)
        pathname = udata.get('pathname') if (udata.get('pathname') == "/checkout?r=sendorder") else '/'
        data = {'type':'success', 'pathname':pathname,'auth_token':auth_token}
        if calledfrom:
            data.update({'calledfrom':calledfrom})
        r.delete(self.vars.get('urltoken'))
        return data
    
    def logout(self):
        logout_user(self.request)
        return {'message':'Logout successful','type':'success'}
    
    
# a = Authent()

# print(a.sendUrl())

