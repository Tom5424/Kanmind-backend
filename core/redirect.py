from django.shortcuts import redirect


def redirect_to_admin_panel(request):
    return redirect("admin/")