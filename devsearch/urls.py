from django.contrib import admin
from django.urls import path, include
# for MEDIA_ROOT / MEDIA_URL
from django.conf import settings
# importing static function/file
from django.conf.urls.static import static
# authentication for passsword reset
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('project.urls')),
    path('', include('users.urls')),
    path('api/', include('api.urls')),

    # built in class based views
    # class based views instead of function they are classes
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html"),
         name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view
         (template_name="reset_password_complete.html"), name='password_reset_complete'),

]

# we need to add path to find images
# connect MEDIA_ROOT and MEDIA_URL
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# same for static files coz after deployment it doesn't work
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
