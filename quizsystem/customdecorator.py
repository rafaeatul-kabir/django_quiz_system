from functools import wraps
from django.shortcuts import redirect

def not_logged_in_redirect(to):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(to)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
