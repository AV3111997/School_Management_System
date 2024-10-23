from .models import User

def user_role(request):
    context = {}
    if request.user.is_authenticated:
        context = {
            'is_librarian': request.user.role == 'librarian',
            'is_office_staff': request.user.role == 'office_staff',
        }
    else:
        context = {
            'is_librarian': False,
            'is_office_staff': False,
        }
    return context