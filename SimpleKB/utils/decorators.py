from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def athenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_groups(allowed_roles=[]):
    """allowed_groups

    Args:
        allowed_groups(['group1', 'group2'...]): Verifies if the user is
        in one of the groups in the list provided. If not raises a PermissionDenied error.
        Defaults to set().
    """
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            IsAllowed = request.user.groups.filter(name__in=allowed_roles).exists()

            if IsAllowed:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator


def allowed_permissions(allowed_permissions=set()):
    """allowed_permissions

    Args:
        allowed_permissions(set('perm1', 'perm2'...)): Verifies if the user has one
        of the permissions in the set provided. If not raises a PermissionDenied error.
        Defaults to set().
    """
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            IsAllowed = any(perm in request.user.get_group_permissions(obj=None)
                            for perm in allowed_permissions)

            if IsAllowed:
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied

        return wrapper_func
    return decorator
