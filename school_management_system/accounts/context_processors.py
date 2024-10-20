from .models import User

def user_role(request):
    context = {}
    if request.user.is_authenticated:
        context = {
            'is_librarian': request.user.role == 'Librarian',
            'is_office_staff': request.user.role == 'Office Staff',
        }
    else:
        context = {
            'is_librarian': False,
            'is_office_staff': False,
        }
    return context