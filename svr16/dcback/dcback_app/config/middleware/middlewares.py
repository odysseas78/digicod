# from random import randrange
from datetime import datetime, timedelta
from pprint import pprint
# import time
import jsons, json
# from django.conf import settings
from django.contrib.auth import get_user_model
# from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
# from django.shortcuts import render
# from django.utils.deprecation import MiddlewareMixin
from django.utils.deprecation import MiddlewareMixin
from ipaddress import ip_address, ip_network
from loguru import logger
from django.utils import timezone
from lib.utils.cryptograph import decrypt_with_private_key
# from channels.db import database_sync_to_async
# from rest_framework.authtoken.models import Token




User = get_user_model()

def logfn1(name,path='logs/'):
    logger.add(f"{path}/{name}.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == name)
    return logger.bind(name=name)

class SetAuthorizationHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path_info.startswith(('/static/', '/media/')):
            return self.get_response(request)
        
        from apps.shop.services import get_or_create_cart
        from eshop.models import FingPrint
        # if request.user.is_authenticated and request.user.customer.basket.filter(in_order=False):
        #     get_or_create_cart(request, )
        
        ccc = request.COOKIES.get('_ccc')
        polz = request.COOKIES.get('_polz')
        # if not (ccc and polz):
        #     get_or_create_cart(request)
        # print(f'''
        #       _polz: {request.COOKIES.get('_polz')}
        #       HTTP_HOST: {request.META.get('HTTP_HOST')}
        #       REMOTE_HOST: {request.META.get('REMOTE_HOST')}
        #       PATH_INFO: {request.META.get('PATH_INFO')}
        #       _ccc: {request.COOKIES.get('_ccc')} _usr: {request.COOKIES.get('_usr')}
        #       auth_token: {request.COOKIES.get('auth_token')}
        #       REMOTE_ADDR: {request.META.get('REMOTE_ADDR')}
        #       HTTP_X_FORWARDED_FOR: {request.META.get('HTTP_X_FORWARDED_FOR')}
        #       HTTP_AUTHORIZATION: {request.META.get('HTTP_AUTHORIZATION')}
        #       HTTP_USER_AGENT: {request.META.get('HTTP_USER_AGENT')}
        #       ''')
        # autheader.info(request.COOKIES.get('auth_token'))
        # autheader.info(request.META.get('HTTP_AUTHORIZATION'))
        # print('##############################################################')
        # pprint(request.META)
        # print('##############################################################')
        # if request.META.get('HTTP_USER_AGENT') == 'axios/1.11.0':
        # logfn1('SetAuthorizationHeaderMiddleware').info(f"HTTP_USER_AGENT: {request.META.get('HTTP_USER_AGENT')}")
        # logfn1('SetAuthorizationHeaderMiddleware').info(f"REMOTE_ADDR: {request.META.get('REMOTE_ADDR')}")
        # logfn1('SetAuthorizationHeaderMiddleware').info(f"HTTP_X_FORWARDED_FOR: {request.META.get('HTTP_X_FORWARDED_FOR')}")
        # logfn1('SetAuthorizationHeaderMiddleware').info(f"HTTP_RESPONSE_XXXXCODES: {request.META.get('HTTP_RESPONSE_XXXXCODES')}")
        if polz:
            try:
                fp, created = FingPrint.objects.get_or_create(fingeprint=polz, defaults={})
                fingPrint = fp or created
                fingPrint.save()
            except Exception as e:
                if str(e) == "get() returned more than one FingPrint -- it returned 2!":
                    FingPrint.objects.filter(fingeprint=polz).delete()
        
            
        # if request.META.get('PATH_INFO')[:8] == '/adminka'  or request.COOKIES.get('_token'):
        #     if request.COOKIES.get('_token'):
        #         request.META['HTTP_AUTHORIZATION'] = 'Token {}'.format(request.COOKIES.get('_token'))
        #         response = self.get_response(request)
        #         if response.status_code == 401 or response.status_code == 403 or request.path == '/api/auth/token/logout/':
        #             # login.info(request.path)
        #             response.delete_cookie(key='_token', domain=request.META.get('SERVER_NAME'))
        #             response.set_cookie(key='__auch__', value='401', path='/', max_age=120, expires=None)
        #             return response
        #         return response
        response = self.get_response(request)
        # logfn1('SetAuthorizationHeaderMiddleware').info(response.data.get('basket').get('id'))
        if response.status_code == 401 and request.COOKIES.get('auth_token'):
            expire_date = timezone.now() - timedelta(hours=1)
            print(f'delete authtoken: {request.COOKIES.get("auth_token")}')
            # res = response.delete_cookie('auth_token', path="/")
            response.set_cookie(
            "auth_token",
            "",
            path="/",
            samesite="Lax",
            expires=expire_date
            )
        
        if hasattr(response, 'data') and type(response.data) == dict and response.data.get('cart'):
            # logfn1('SetAuthorizationHeaderMiddleware').info(response.data.get('basket').get('id'))
            response.set_cookie('_ccc', str(response.data.get('cart').get('id')), 
                        max_age=None, expires=None, path='/', domain=None, secure=False, httponly=True, samesite='Lax')
        
        if hasattr(response, 'data') and type(response.data) == dict and response.data.get('auth_token'):
            # logfn1('SetAuthorizationHeaderMiddleware').info(response.data.get('auth_token'))
            # logfn1('SetAuthorizationHeaderMiddleware').info(request.search_params)
            # logfn1('SetAuthorizationHeaderMiddleware').info(request.url)
            response.set_cookie(
            "auth_token",
            f"{response.data.get('auth_token')}",
            httponly=True,
            secure=True,
            samesite="Lax",
            # max_age=(15 * 60)
            max_age=(2 * 24 * 60 * 60),  # 2 days
            )
            # response.set_cookie(
            # "_usr",
            # 'True',
            # httponly=True,
            # secure=True,
            # samesite="Lax",
            # max_age=(15 * 60)
            # # max_age=(2 * 24 * 60 * 60),  # 2 days
            # )
        else:
            # expire_date = timezone.now() - timedelta(hours=2)
            response.set_cookie(
            "_usr",
            f"{request.user.is_authenticated}",
            path='/',
            httponly=True,
            secure=True,
            samesite="Lax",
            # expires=expire_date
            max_age=(3 * 60 * 60)
            # max_age=(2 * 24 * 60 * 60),  # 2 days
            )
        if request.user.is_authenticated and not request.user.is_superuser:
            expire_date = timezone.now() - timedelta(hours=2)
            from eshop.models import CustomToken
            fp = CustomToken.objects.filter(user=request.user).first()
            # print(f'kkk - {(fp.fingeprint == request.COOKIES.get("_polz"))}')
            if fp and not (fp.fingeprint == request.COOKIES.get("_polz")):
                fp.delete()
                response.set_cookie(
                "auth_token",
                "",
                path='/',
                httponly=True,
                secure=True,
                samesite="Lax",
                expires=expire_date
                )
                
            # 
            # print(request.COOKIES.get('_polz'))
            # expire_date = timezone.now() - timedelta(hours=1)
            # response.set_cookie(
            # "_Kokoraki",
            # "m12345678",
            # httponly=True,
            # secure=True,
            # samesite="Lax",
            # expires=expire_date
            # max_age=(60 * 60),
            # max_age=(2 * 24 * 60 * 60),  # 2 days
            # )
            # response.set_cookie('auth_token', response.data.get('auth_token'), 
            #             max_age=None, expires=None, path='/', domain=None, secure=True, httponly=True, samesite=None)
        # response.set_cookie('_usr', "True", 
        #             max_age=None, expires=None, path='/', domain=None, secure=False, httponly=True, samesite=None)
        # else:
            # logfn1('SetAuthorizationHeaderMiddleware').info(f"111: {request.user.is_authenticated}")
            # response.set_cookie('_usr', f'{request.user.is_authenticated}')
        # logfn1('SetAuthorizationHeaderMiddleware').info(f"222: {request.user.is_authenticated}")
        
        # logfn1('SetAuthorizationHeaderMiddleware').info(f"response: {request.headers.get('set-cookie')}")
        return response
        
        3736588
class RealIPFromForwardedFor(MiddlewareMixin):
    """
    Nimm die erste Adresse aus X-Forwarded-For als Client-IP.
    Platziere diese Middleware *vor* CsrfViewMiddleware.
    """
    def process_request(self, request):
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            request.META["REMOTE_ADDR"] = xff.split(",")[0].strip()

# class CsrfBypassForInternal(MiddlewareMixin):
#     """
#     Deaktiviert CSRF-Checks für interne Netze.
#     """
#     def process_request(self, request):
#         try:
#             rip = ip_address(request.META.get("REMOTE_ADDR", "0.0.0.0"))
#             if any(rip in ip_network(net) for net in INTERNAL_CSRF_EXEMPT):
#                 setattr(request, "_dont_enforce_csrf_checks", True)
#         except ValueError:
#             pass


# class TokenAuthMiddleware:
#     """
#     Middleware für die WebSocket-Authentifizierung über TokenAuth.
#     """
#     def __init__(self, inner):
#         self.inner = inner

#     async def __call__(self, scope, receive, send):
#         from rest_framework.authtoken.models import Token
#         from asgiref.sync import sync_to_async
#         from urllib.parse import parse_qs
#         # Token aus der Query-String abrufen
#         query_string = scope.get("query_string", b"").decode()
#         query_params = parse_qs(query_string)
#         token_key = query_params.get("token", [None])[0]

#         # Benutzer authentifizieren
#         if token_key:
#             try:
#                 # Token und Benutzer asynchron abrufen
#                 token = await sync_to_async(Token.objects.get)(key=token_key)
#                 user = await sync_to_async(lambda: token.user)()
#                 scope["user"] = user
#             except Token.DoesNotExist:
#                 scope["user"] = AnonymousUser()
#         else:
#             scope["user"] = AnonymousUser()

#         # Die Verbindung an den nächsten Layer weitergeben
#         inner = self.inner(scope)
#         return await super().__call__(scope, receive, send)




class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        from rest_framework.authtoken.models import Token
        from django.contrib.auth.models import AnonymousUser
        from asgiref.sync import sync_to_async
        from urllib.parse import parse_qs
        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        token_key = query_params.get("token", [None])[0]
        # print(f'''TokenAuthMiddleware - token_key: {token_key}''')
        if token_key:
            try:
                # Token & User direkt laden
                token_obj = await sync_to_async(
                    lambda: Token.objects.select_related("user").get(key=token_key)
                )()
                scope["user"] = token_obj.user
            except Token.DoesNotExist:
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)


# class TokenAuthMiddleware:
#     """
#     Middleware für die WebSocket-Authentifizierung über TokenAuth.
#     """
#     def __init__(self, inner):
#         self.inner = inner

#     def __call__(self, scope):
#         return TokenAuthMiddlewareInstance(scope, self.inner)

# class TokenAuthMiddlewareInstance:
#     def __init__(self, scope, inner):
#         self.scope = scope
#         self.inner = inner

#     async def __call__(self, receive, send):
#         # Token aus der Query-String abrufen
#         query_string = self.scope.get("query_string", b"").decode()
#         query_params = parse_qs(query_string)
#         token_key = query_params.get("token", [None])[0]

#         # Benutzer anhand des Tokens authentifizieren
#         if token_key:
#             try:
#                 token = Token.objects.get(key=token_key)
#                 self.scope["user"] = token.user
#             except Token.DoesNotExist:
#                 self.scope["user"] = AnonymousUser()
#         else:
#             self.scope["user"] = AnonymousUser()

#         # Die Verbindung an den nächsten Layer weitergeben
#         inner = self.inner(self.scope)
#         return await inner(receive, send)


# def imprt(d):
#     from config.urls import adminpaths, sd
#     if d==0:
#         if len(sd) > 1:
#             for ad in adminpaths:
#                 sd.remove(ad)
#                 if len(sd) == 1:
#                     break
#         data = json_read('jjss.json')
#         data.update({"SD000_"+str(datetime.now().timestamp()):str(sd)})
#         json_save(data, 'jjss.json')
#         return sd
#     elif d==1 and len(sd) < 2:
#         sd += adminpaths
#         data = json_read('jjss.json')
#         data.update({"Sd111_"+str(datetime.now().timestamp()):str(sd)})
#         json_save(data, 'jjss.json')
#         return sd
    # return [adminpaths, sd]

# logger.add("out.log", backtrace=True, diagnose=True)
# class CsrfDisableCheckMiddleware(MiddlewareMixin):

#     def process_request(self, request, *args, **kwargs):
#         if not getattr(request, '_dont_enforce_csrf_checks', False):
#             # Mechanism to turn off CSRF checks for test suite.
#             # It comes after the creation of CSRF cookies, so that
#             # everything else continues to work exactly the same
#             # (e.g. cookies are sent, etc.), but before any
#             # branches that call reject().
#             setattr(request, '_dont_enforce_csrf_checks', True)


class PolzovMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.add("logs/PolzovMiddleware.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "PolzovMiddleware")
        polzovMidlog = logger.bind(name="PolzovMiddleware")
        from eshop.models import Polzov, Jsonfile
        from eshop.Utilss.utils import listUniq
        from rest_framework.authtoken.models import Token
        
        fingerprint = request.COOKIES.get('_polz')
        if fingerprint:
            obj, create = Polzov.objects.get_or_create(
                fingeprint=fingerprint,
                defaults={
                "json":{
                    "userlist":[],
                    "ips":[],
                    "useragents":[],
                    "tokens":[]
                    }
            }
            )
            if request.META.get('HTTP_AUTHORIZATION'):
                auth = request.META.get('HTTP_AUTHORIZATION')
                token1 = auth.split(' ')[1]
                token = Token.objects.filter(key=token1).first()
                if token and token.user.username:
                    username = token.user.username
                    lst = obj.json.get('userlist')
                    lst.append(username)
                    obj.json['userlist'] = list(set(lst))
                    obj.save()
                    lst = obj.json.get('tokens')
                    lst.append(token.key)
                    obj.json['tokens'] = list(set(lst))
                    obj.save()
                ip = request.META.get('HTTP_X_FORWARDED_FOR')
                lst = obj.json.get('ips')
                lst.append(ip)
                obj.json['ips'] = list(set(lst))
                obj.save()
                useragent = request.META.get('HTTP_USER_AGENT')
                lst = obj.json.get('useragents')
                lst.append(useragent)
                obj.json['useragents'] = list(set(lst))
                obj.save()
        else:
            jobj, create = Jsonfile.objects.get_or_create(
                name='HeaderStat',
                defaults={
                    "json":[]
                }
            )
            hd = request.META.copy()
            hd = dict(hd)
            jsn = jobj.json
            jsn.append({
                'ip':request.META.get('HTTP_X_FORWARDED_FOR'), 
                'useragent':request.META.get('HTTP_USER_AGENT'),
                # 'cookies':request.META.get('HTTP_COOKIE')
                })
            jobj.json = listUniq(jsn)
            jobj.save()
            
            # polzovMidlog.info(request.META)
            # polzovMidlog.info(request.headers)
            # polzovMidlog.info(request.COOKIES)
            # polzovMidlog.info('#################################################################################################################')
        
        response = self.get_response(request)
        return response


# class JWTUserTokenAuthorizationMiddleware(MiddlewareMixin):

#     def process_request(self, request):
#         if request.path.find('admin') != -1:
#             return super(AuthenticationMiddleware).process_request(request)
#         auth_header = request.META.get('HTTP_AUTHORIZATION')
#         if auth_header:
#             try:
#                 token = auth_header.split(' ')[-1]
#                 data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
#                 request.user = User.objects.get(id=int(data['user_id']))
#             except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
#                 request.user = AnonymousUser()
#         else:
#             request.user = AnonymousUser()


# class UnderConstructionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#     def __call__(self, request):
        
        # if request.META.get('PATH_INFO')[:8] == '/adminka':
        #     if request.COOKIES.get('_token'):
        #         from rest_framework.authtoken.models import Token
        #         token = Token.objects.filter(key=request.COOKIES.get('_token')).first()
        #         if token and token.user.is_superuser:
        #             imprt(d=1)
        #         else:
        #             imprt(d=0)
        #     else:
        #         imprt(d=0)
        # else:
        #     imprt(d=0)

        # data = Jsonfile.objects.filter(name='Shopsettings').first().json
        # if data.get('Maintenance').get('maintenance'):
        #     # print(request.META.get('PATH_INFO')[:7])
        #     if not request.user.is_superuser and data.get('Maintenance').get('ips').count(request.META.get
        #             ('HTTP_X_FORWARDED_FOR')) == 0 and request.META.get('REQUEST_METHOD') == 'GET'\
        #             and request.META.get('PATH_INFO')[:7] != '/media/' and request.META.get('PATH_INFO')[:14] != '/administracia':
        #         if request.META.get('PATH_INFO')[:5] == '/api/':
        #             return HttpResponse('under_construction')
        #         qs = Brand.objects.all().exclude(image='').order_by('?')
        #         brands = qs
        #         i = 1
        #         for item in brands:
        #             item.index = i
        #             item.rand100 = randrange(1, 90)
        #             item.randsec = randrange(0, 300)
        #             i+=1


        #         return render(request, 'uconst.html', {'brands': brands, 'jsondata': jsons.dumps({'date': data['Maintenance']['date']})})
        # return self.get_response(request)




