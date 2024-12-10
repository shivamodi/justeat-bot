from django.urls import path, include
from django.conf import settings
from . import views
from plans_payments import urls as plans_payments_urls
from payments import urls as payments_urls
import plans_payments, payments

urlpatterns = [
    path("pricing/", views.PricingView.as_view(), name="pricing"),
    path("account/", views.CurrentPlanView.as_view(), name="current_plan"),
    path(
        "account/activation/",
        views.AccountActivationView.as_view(),
        name="account_activation",
    ),
    path("upgrade/", views.UpgradePlanView.as_view(), name="upgrade_plan"),
    path(
        "order/extend/new/<int:pk>/",
        views.CreateOrderView.as_view(),
        name="create_order_plan",
    ),
    path(
        "order/upgrade/new/<int:pk>/",
        views.CreateOrderPlanChangeView.as_view(),
        name="create_order_plan_change",
    ),
    path("change/<int:pk>/", views.ChangePlanView.as_view(), name="change_plan"),
    path("order/", views.OrderListView.as_view(), name="order_list"),
    path("order/<int:pk>/", views.OrderView.as_view(), name="order"),
    path(
        "order/<int:pk>/payment/success/",
        views.OrderPaymentReturnView.as_view(status="success"),
        name="order_payment_success",
    ),
    path(
        "order/<int:pk>/payment/failure/",
        views.OrderPaymentReturnView.as_view(status="failure"),
        name="order_payment_failure",
    ),
    # Redirect for backward compatibility:
    path("billing/create/", views.RedirectToBilling.as_view(), name="billing_info_create"),
    # Redirect for backward compatibility:
    path("billing/update/", views.RedirectToBilling.as_view(), name="billing_info_update"),
    path("billing/", views.BillingInfoCreateOrUpdateView.as_view(), name="billing_info"),
    path(
        "billing/delete/", views.BillingInfoDeleteView.as_view(), name="billing_info_delete"
    ),
    path(
        "invoice/<int:pk>/preview/html/",
        views.InvoiceDetailView.as_view(),
        name="invoice_preview_html",
    ),
]

if getattr(settings, "DEBUG", False) or getattr(settings, "ENABLE_FAKE_PAYMENTS", True):
    urlpatterns += [
        path(
            "fakepayments/<int:pk>/", views.FakePaymentsView.as_view(), name="fake_payments"
        ),
    ]

urlpatterns += [
    path('', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("login_view", views.login_view, name="login_view"),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('reset_password', views.reset_password, name='reset_password'),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("startprocess", views.startprocess, name="startprocess"),
    path("stopprocess", views.stopprocess, name="stopprocess"),
    path("saveschedule", views.saveschedule, name="saveschedule"),
    path("schedule", views.schedule, name="schedule"),
    path("profile", views.profile, name="profile"),
    path("saveprofile", views.saveprofile, name="saveprofile"),
    path("notifications", views.notifications, name="notifications"),
    path("savenotifications", views.savenotifications, name="savenotifications"),
    path("zones", views.zones, name="zones"),
    path("save_zone", views.save_zone, name="save_zone"),
    path("savezones", views.savezones, name="savezones"),
    path("contact", views.contact, name="contact"),
    path("logs", views.logs, name="logs"),
    path('plans-payments/', include('plans_payments.urls')),
    path('get_plans', views.get_plans, name='get_plans'),
    path('create_stripe_session', views.create_stripe_session, name='create_stripe_session'),
    path('webhooks/stripe/', views.stripe_webhook, name='stripe-webhook'),
    path('current_plan', views.current_plan, name='current_plan'),
    path('get_referrals', views.referral_list, name='get_referrals'),
    path('submit_referral', views.submit_referral, name='submit_referral'),
    path('record_signup', views.record_signup, name='record_signup'),
    path('check_execution_status', views.check_execution_status, name='check_execution_status'),
    path('get_referral_counts', views.get_referral_counts, name='get_referral_counts'),
    path('save_billing_info', views.save_billing_info, name='save_billing_info'),
    path('get_toggle_values', views.get_toggle_values, name='get_toggle_values'),
    path('save_toggle_values', views.save_toggle_values, name='save_toggle_values'),
    path('get_awarded_plans', views.get_awarded_plans, name='get_awarded_plans'),
    path('claim_plan', views.claim_plan, name='claim_plan'),
    path('save_justeat_credentials', views.save_justeat_credentials, name='save_justeat_credentials'),
    path('send_support_email', views.send_support_email, name='send_support_email'),
    ]
urlpatterns += [
    path('payments/', include('payments.urls')),
]