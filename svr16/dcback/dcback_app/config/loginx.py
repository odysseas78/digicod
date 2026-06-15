from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from loguru import logger
from eshop_api.utils import create_login_stat
from config import settings


logger.add("logs/user_logger.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "user_logger")
user_logger = logger.bind(name="user_logger")

def clogst(request, username, result):
    try:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    except:
        ip = request.META['REMOTE_ADDR']
    create_login_stat(username=username,
        ip="94.131.159.9",
        result=result, 
        useragent=request.META.get('HTTP_USER_AGENT'),
        device=request.META.get('HTTP_SEC_CH_UA_PLATFORM'),
        meta=request.META)
    

def getuserdata(request):
    try:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    except:
        ip = request.META['REMOTE_ADDR']
        
    return f"ip: {ip} - device: {request.META.get('HTTP_SEC_CH_UA_PLATFORM')}"

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    clogst(request, user.username, 'Login')
    """ log user login to user log """
    user_logger.info(f'%s login successful: {user.username}, {getuserdata(request)}')


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, user=None, **kwargs):
    clogst(request, credentials.get('username'), 'Failed')
    """ log user login to user log """
    if user:
        user_logger.info('%s login failed', user)
    else:
        user_logger.error(f'login failed: {credentials}, {getuserdata(request)}')


@receiver(user_logged_out)
def log_user_logout(sender, user, request, **kwargs):
    clogst(request, user.username, 'Logout')
    """ log user logout to user log """
    user_logger.info(f'%s log out successful: {user.username}, {getuserdata(request)}')