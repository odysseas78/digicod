from django.contrib.auth import get_user_model
import django, os, sys
sys.path.insert(0, '/home/dcback')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

# User = get_user_model()
# user = User.objects.get(id=97)
# from sesame.utils import get_token, renew_token
# # renew_token('AAAAYQlYlRvkhgjufX6y87W5')
# print(get_token(user))
# print(renew_token('AAAAYQlYlRvkhgjufX6y87W5'))