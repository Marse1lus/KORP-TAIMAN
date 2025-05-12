from rest_framework.permissions import BasePermission

class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        print("=== IsAuthor Permission Check ===")
        print("Method:", request.method)
        print("User:", request.user)
        print("Is authenticated:", request.user.is_authenticated)
        

        if request.method == 'GET':
            return True
            

        if request.user and request.user.is_authenticated:
            is_author = request.user.groups.filter(name='Authors').exists()
            print("Is in Authors group:", is_author)
            return is_author
            
        print("Not authenticated")
        return False
