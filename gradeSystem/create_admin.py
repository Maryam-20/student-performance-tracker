from django.contrib.auth import get_user_model

User = get_user_model()

# The email of the user you want to promote
email = "yusuffalana@gmail.com"

try:
    user = User.objects.get(email=email)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f"User {email} has been successfully promoted to superuser.")
except User.DoesNotExist:
    print(f"No user found with email: {email}")
