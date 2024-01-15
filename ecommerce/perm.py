from rest_framework.permissions import DjangoModelPermissions, AllowAny


class HasGroupPermission(DjangoModelPermissions):
    '''Allows User actions that belongs to his/her group'''
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        if getattr(view, '_ignore_model_permissions', False):
            return True

        if not request.user or (
           not request.user.is_authenticated and self.authenticated_users_only):
            return False

        queryset = self._queryset(view)
        perms = self.get_required_permissions(request.method, queryset.model)

        # print((str(perms)+'\n')*100)
        # print(request.user.get_group_permissions())
        # print('if perms=', bool(perms))
        if perms:
            # print('perms[0] in request.user.get_group_permissions()', perms[0] in request.user.get_group_permissions())
            return (perms[0] in request.user.get_group_permissions()) or request.user.has_perms(perms)
        return False


# uncomment this to grant all users including anonymous users all required privileges
# class HasGroupPermission(AllowAny):
#     pass