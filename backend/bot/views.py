from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from .models import User
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import time
import cloudscraper
from django.core.cache import cache
from urllib.parse import unquote
import os
import signal
import threading
import subprocess
import yagmail
from twilio.rest import Client
from datetime import datetime
from pinax.referrals.models import Referral
import datetime as time1
import warnings
from decimal import Decimal
from itertools import chain
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, RedirectView, TemplateView, View
from django.views.generic.detail import (
    DetailView,
    SingleObjectMixin,
    SingleObjectTemplateResponseMixin,
)
from django.views.generic.edit import (
    DeleteView,
    FormView,
    ModelFormMixin,
    ProcessFormView,
)
from django.views.generic.list import ListView
from next_url_mixin.mixin import NextUrlMixin

from plans.base.models import (
    AbstractBillingInfo,
    AbstractInvoice,
    AbstractOrder,
    AbstractPlan,
    AbstractPlanPricing,
    AbstractQuota,
    AbstractUserPlan,
)
from plans.forms import BillingInfoForm, CreateOrderForm, FakePaymentsForm
from plans.importer import import_name
from plans.mixins import LoginRequired
from plans.signals import order_started
from plans.utils import get_currency
from plans.validators import plan_validation
from plans.plan_change import get_change_price
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.utils.translation import gettext_lazy as _
import six
from django.utils import timezone
from django.db.models import Count 
from plans.models import Plan, UserPlan, PlanPricing, Pricing, Quota, PlanQuota
from pinax.referrals.models import Referral
from django.db.models import Count
from pinax.referrals.models import ReferralResponse
from django.core.cache import cache
from django.views.decorators.cache import never_cache
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render
from django.conf import settings
# Django view to reset the password
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
import requests
from django.http import JsonResponse
from .models import Zone
from django.shortcuts import render
from .models import Zone
import uuid
from django.db.models import Prefetch
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from plans.models import Plan, PlanPricing
from plans_payments.models import Payment
from django.urls import reverse

stripe.api_key = settings.STRIPE_LIVE_SECRET_KEY

import json
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from plans.models import Plan, UserPlan
from django.utils import timezone

# Stripe Webhook Secret (from the Stripe Dashboard)
STRIPE_WEBHOOK_SECRET = settings.STRIPE_WEBHOOK_SECRET

from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from plans.models import BillingInfo, Order, Invoice, Plan, PlanPricing, Pricing, UserPlan, RecurringUserPlan
from django.conf import settings
from sequences import get_next_value

import threading
import time
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
import asyncio
from asgiref.sync import sync_to_async
import os
import psutil
import resource
soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))
# Global dictionary to store flags and threads for each user
user_threads = {}



@csrf_exempt  # Disable CSRF for this view (or use token-based CSRF protection)
def send_support_email(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data sent from the React frontend
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            query = data.get('query')

            # Create the email subject and message
            subject = f"Support Query from {name}"
            message = f"Name: {name}\nEmail: {email}\n\nQuery:\n{query}"
            #from_email = 'grabbereat@gmail.com'  # Sender's email (e.g., support@example.com)
            recipient_list = ['grabbereat@gmail.com']  # List of recipients
                
            gmail_user = 'grabbereat@gmail.com'
            gmail_password = 'qquc rlcn yesb wuje'

            yag = yagmail.SMTP(gmail_user, gmail_password)

            #to = [email]

            yag.send(recipient_list, subject = subject, contents = message)

            # Return a success response
            return JsonResponse({'message': 'Email sent successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def get_referral_counts(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        referrer_user = User.objects.get(id=username)  # Fetch by username
        plan_name_premium = 'PREMIUM'
        plan_name_basic = 'BASIC'

        # Get weekly and monthly pricing IDs for each plan
        basic_weekly_pricing_id = 1
        basic_monthly_pricing_id = 2
        premium_weekly_pricing_id = 1
        premium_monthly_pricing_id = 2

        data = {
            "basic_weekly": get_referral_counts_total(referrer_user, plan_name_basic, basic_weekly_pricing_id),
            "basic_monthly": get_referral_counts_total(referrer_user, plan_name_basic, basic_monthly_pricing_id),
            "premium_weekly": get_referral_counts_total(referrer_user, plan_name_premium, premium_weekly_pricing_id),
            "premium_monthly": get_referral_counts_total(referrer_user, plan_name_premium, premium_monthly_pricing_id),
        }

        return JsonResponse(data, status=200, safe=False)

    except User.DoesNotExist:
        return JsonResponse({"error": "Referrer user does not exist"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

from django.db.models import Count

def get_referral_counts_total(referrer_user, plan_name, pricing_id):


    # Step 1: Get all users who were referred by the referrer_user (using referred_by field)
    referred_users = User.objects.filter(referred_by=referrer_user)

    # Step 2: Get the Plan object that matches the provided plan name (e.g., 'PREMIUM')
    plan = Plan.objects.get(name=plan_name)

    # Step 3: Filter the UserPlan entries for these referred users with the correct plan
    # We join UserPlan with RecurringUserPlan to filter by the pricing_id from RecurringUserPlan
    active_users_with_plan = (
        UserPlan.objects.filter(
            user__in=referred_users,  # The user must be one of the referred users
            plan=plan,                 # The plan must match the provided plan
            active=True            # Only active plans
        )
        .filter(
            recurring__pricing__id=pricing_id  # Filtering by pricing_id in the RecurringUserPlan
        )
    ).values('user__username').annotate(count=Count('user'))

    # Step 4: Count how many referred users have the active plan/price combination
    #count = active_users_with_plan.count()

    return list(active_users_with_plan)

def get_referral_counts_total_claim(referrer, plan_name, pricing_id):
    awarded_plans = {}
    referral_counts = (
        ReferralResponse.objects.filter(
            referral__user__referred_by=referrer,
            referral__user__userplan__plan__name=plan_name,
            referral__user__userplan__plan__planpricing__id=pricing_id,  # Adding the pricing ID check
            action="SIGNUP"
        )
        .count()
    )
    # Award free plan for every 2 referrals 
    free_plans_to_award = referral_counts
    awarded_plans = { 'plan_name': plan_name, 'pricing_id': pricing_id, 'free_plans_to_award': free_plans_to_award }
    return awarded_plans


@csrf_exempt
def get_awarded_plans(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        referrer_user = User.objects.get(id=int(username))  # Fetch by username
        plan_name_premium = "PREMIUM"
        plan_name_basic = "BASIC"

        # Get weekly and monthly pricing IDs for each plan
        basic_weekly_pricing_id = 1
        basic_monthly_pricing_id = 2
        premium_weekly_pricing_id = 1
        premium_monthly_pricing_id = 2

        data = {"awarded_plans" : {
            0: count_active_referrals_with_plan(referrer_user, plan_name_basic, basic_weekly_pricing_id),
            1: count_active_referrals_with_plan(referrer_user, plan_name_basic, basic_monthly_pricing_id),
            2: count_active_referrals_with_plan(referrer_user, plan_name_premium, premium_weekly_pricing_id),
            3: count_active_referrals_with_plan(referrer_user, plan_name_premium, premium_monthly_pricing_id),
        }}

        return JsonResponse(data, status=200)

    except User.DoesNotExist:
        return JsonResponse({"error": "Referrer user does not exist"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def count_active_referrals_with_plan(referrer_user, plan_name, pricing_id):
    """
    Count the number of users referred by a specific referrer
    that have an active recurring plan/price combination, using django-plans models.

    :param referrer_user: The user who referred others.
    :param plan_name: The name of the plan to check for (e.g., 'PREMIUM').
    :param pricing_id: The ID of the pricing plan to check (e.g., 1 for Weekly, 2 for Monthly).
    :return: The count of referred users with an active plan and pricing combination.
    """

    # Step 1: Get all users who were referred by the referrer_user (using referred_by field)
    referred_users = User.objects.filter(referred_by=referrer_user)

    # Step 2: Get the Plan object that matches the provided plan name (e.g., 'PREMIUM')
    plan = Plan.objects.get(name=plan_name)

    # Step 3: Filter the UserPlan entries for these referred users with the correct plan
    # We join UserPlan with RecurringUserPlan to filter by the pricing_id from RecurringUserPlan
    active_users_with_plan = (
        UserPlan.objects.filter(
            user__in=referred_users,  # The user must be one of the referred users
            plan=plan,                 # The plan must match the provided plan
            active=True            # Only active plans
        )
        .filter(
            recurring__pricing__id=pricing_id  # Filtering by pricing_id in the RecurringUserPlan
        )
    )

    # Step 4: Count how many referred users have the active plan/price combination
    count = active_users_with_plan.count()
    
    if plan_name == 'BASIC' and pricing_id == 1:
        claimed_count = referrer_user.bw_count
    elif plan_name == 'BASIC' and pricing_id == 2:
        claimed_count = referrer_user.bm_count
    elif plan_name == 'PREMIUM' and pricing_id == 1:
        claimed_count = referrer_user.pw_count
    else:
        claimed_count = referrer_user.pm_count
    awarded_plans = { 'plan_name': plan_name, 'pricing_id': pricing_id, 'free_plans_to_award': count, 'claimed_count': claimed_count }
    return awarded_plans

@csrf_exempt
def claim_plan(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        plan_name = data.get('plan_name')
        pricing_id = data.get('pricing_id')

        user = User.objects.get(id=int(username))
        plan_pricing = PlanPricing.objects.get(plan__name=plan_name, pricing_id=pricing_id)
        pricing = Pricing.objects.get(id=pricing_id)

        if pricing_id==1:
            tenure = 7
        else:
            tenure = 30
        # Add the free plan to the user's account
        try:
            user_plan = UserPlan.objects.get(user=user)
            user_plan.plan=plan_pricing.plan
            user_plan.pricing=plan_pricing
            user_plan.active=True
            user_plan.updated_at=timezone.now()
            user_plan.expire= datetime.combine(user_plan.expire, datetime.min.time()).astimezone() + timedelta(days=tenure)
            user_plan.save()
            if plan_name == 'BASIC' and pricing_id == 1:
                user.bw_count += 1
                user.save()
            elif plan_name == 'BASIC' and pricing_id == 2:
                user.bm_count += 1
                user.save()
            elif plan_name == 'PREMIUM' and pricing_id == 1:
                user.pw_count += 1
                user.save()
            else:
                user.pm_count += 1
                user.save()
            

        except UserPlan.DoesNotExist:
            UserPlan.objects.create(user=user, plan=plan_pricing.plan, pricing=plan_pricing, active=True, created=timezone.now(), updated_at=timezone.now(), expires=timezone.now() + timedelta(days=tenure) )
        
        try:
            recurring_plan = RecurringUserPlan.objects.get(pricing=pricing, user_plan=user_plan)
            recurring_plan.amount = 0.00
            recurring_plan.tax = 0
            recurring_plan.currency='GBP'
            recurring_plan.has_automatic_renewal=False 
            recurring_plan.token=''
            recurring_plan.token_verified=False
            recurring_plan.created=timezone.now()
            recurring_plan.updated_at=timezone.now()
            recurring_plan.renewal_triggered_by=1 
            recurring_plan.payment_provider='stripe'
            recurring_plan.save()
        except RecurringUserPlan.DoesNotExist:
            #RecurringUserPlan.objects.create( pricing=pricing, user_plan=user_plan, amount=invoice['amount_due'], tax=0, currency='GBP', has_automatic_renewal=True, token=invoice['subscription'], token_verified=True, created=timezone.now(), updated_at=timezone.now(), renewal_triggered_by='stripe', payment_provider='stripe')
        # Optionally, create a RecurringUserPlan entry if required
            RecurringUserPlan.objects.create( pricing=pricing, user_plan=user_plan, amount=0.00, tax=0, currency='GBP', has_automatic_renewal=False, token='', token_verified=False, created=timezone.now(), updated_at=timezone.now(), renewal_triggered_by=1, payment_provider='stripe')


        return JsonResponse({'status': 'success'}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=404)
    except PlanPricing.DoesNotExist:
        return JsonResponse({'error': 'Plan pricing not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def save_toggle_values(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        open_run_toggle = data.get('open_run_toggle')
        overflows_toggle = data.get('overflows_toggle')

        user = User.objects.get(id=username)  # Fetch by username

        if open_run_toggle is not None:
            user.open_runs_toggle = open_run_toggle
        if overflows_toggle is not None:
            user.overflows_toggle = overflows_toggle

        user.save()

        return JsonResponse({"success": True}, status=200)
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def get_toggle_values(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        user = User.objects.get(id=username)  # Fetch by username

        toggle_settings = {
            "open_run_toggle": user.open_runs_toggle,
            "overflows_toggle": user.overflows_toggle,
        }
        return JsonResponse(toggle_settings, status=200)
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def assign_trial_plan(instance, created):
    """
    Automatically assigns a trial plan to a new user after registration.
    """
    if created:
        # Find the trial plan (you can adjust this to your needs)
        trial_plan = Plan.objects.filter(name="TRIAL").first()

        if trial_plan:
            #print(instance.id)
            # Create a subscription for the user to the trial plan
                try:
                    instance.userplan.initialize()
                    instance.userplan.expire = timezone.now() + timedelta(days=3)
                    instance.userplan.save()
                except UserPlan.DoesNotExist:
                    return


@csrf_exempt
def record_signup(request):
        # Parse the request body
        try:
            data = json.loads(request.body)
            referral_code = data.get('referral_code')
            session_key = data.get('session_key')
            user_ip = data.get('user_ip')
            username = data.get('username')

            # Validate that we have necessary data
            if not referral_code or not session_key or not user_ip:
                return JsonResponse({"error": "Missing referral_code, session_key, or user_ip"}, status=400)

            # Try to get the referral object from the referral code
            try:
                referral = Referral.objects.get(code=referral_code)
            except Referral.DoesNotExist:
                return JsonResponse({"error": "Referral code not valid or not found"}, status=404)

            # Retrieve the user by username (or email or whatever you use)
            user = User.objects.filter(username=username).first()  # Adjust this to your logic if needed
            referrer = User.objects.get(pk=referral.user_id)

            if user:
                # Create a referral record, associate the user with the referral (manually add the referrer)
                user.referred_by = referrer  # Assuming the referrer field is set
                user.save()

                # Optionally, create a log entry for the session and IP address

                referral_response = ReferralResponse.objects.create(referral=referral, action="SIGNUP", session_key=session_key, ip_address=user_ip, user=user)
                referral_response_old = ReferralResponse.objects.filter(referral=referral, action="RESPONDED", session_key=session_key, ip_address=user_ip).first()
                referral_response_old.user = user
                referral_response_old.save()

                return JsonResponse({"message": "Referral signup recorded successfully"}, status=200)

            return JsonResponse({"error": "User not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt  # Disable CSRF for simplicity in testing (better handle CSRF in production)
def submit_referral(request):
    try:
        # Parse the incoming JSON body to get the referral code
        data = json.loads(request.body)
        #print(data)
        referral_code = data.get('referral_code')
        session_key = data.get('session_key')
        user_ip = data.get('user_ip')




        if not referral_code:
            return JsonResponse({'status': 'error', 'message': 'Referral code is missing.'})

        # Find the referral by code
        referral = Referral.objects.get(code=referral_code)

        # Create a referral response for this referral (you can customize this logic as needed)
        referral_response = ReferralResponse.objects.create(referral=referral, action="RESPONDED", session_key=session_key, ip_address=user_ip)

        return JsonResponse({'status': 'success', 'message': 'Referral recorded successfully!', 'referral_response': {'status': 'success'}})

    except Referral.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid referral code.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
def referral_list(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('username')
        user = User.objects.get(pk=int(user_id))
        # Fetch all referrals and their responses for the logged-in user
        referrals = Referral.objects.filter(user=user)
        referral_data = []
        
        for referral in referrals:
            responses = ReferralResponse.objects.filter(referral=referral)
            response_data = [
                {
                    "response_message": response.action,
                    "status": response.referral_id,
                    "created_at": response.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
                for response in responses
            ]
            
            referral_data.append({
                "referral_code": referral.code,
                "referred_email": user.referred_by.email if user.referred_by else None,
                "created_at": referral.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "responses": response_data
            })
        
        return JsonResponse({"referrals": referral_data}, status=200)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt 
def current_plan(user_id):
    # Get the current active user plan (subscription)
    #print(data.get('username'))

    try:
        user = User.objects.get(pk=int(user_id))
        user_plan = UserPlan.objects.get(user=user, active=True)

        # Get the associated plan and expiry date
        plan = user_plan.plan
        expiry_date = datetime.combine(user_plan.expire, datetime.min.time()).astimezone()  # Assuming the end date is stored here

        # Format the expiry date
        expiry_str = expiry_date.strftime('%Y-%m-%d')

        # Check if the subscription has expired
        is_expired = expiry_date < timezone.now()

        # Prepare context for rendering the template
        context = {
            'plan_name': plan.name,  # Plan name
            'expiry_date': expiry_str,  # Expiry date
            'is_expired': is_expired,  # Check if expired
        }

        return context
    
    except UserPlan.DoesNotExist:
        # If no active subscription exists
        contextnil =  {
            'plan_name': "No Active Plan",  # Plan name
            'expiry_date': "Expired",  # Expiry date
            'is_expired': True,  # Check if expired
        }
        return contextnil


@csrf_exempt
def stripe_webhook(request):
    payload = request.body.decode('utf-8')
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    if event['type'] == 'invoice.payment_succeeded':
        invoice = event['data']['object']

        stripe_customer_id = invoice['customer']
        try:
            user = User.objects.get(stripe_customer_id=stripe_customer_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        price_id = invoice['lines']['data'][0]['price']['id']
                # Ensure that the pricing is recurring
        if price_id == 'price_1QOGy3Rvd2TmzN7sVRrtYCWU':
            plan_id = 2 
            pricing_id = 1
        elif price_id == 'price_1QOGyjRvd2TmzN7svhnHEHvU':
            plan_id = 2 
            pricing_id = 2
        if price_id == 'price_1QOGzKRvd2TmzN7s1gV9OSgp':
            plan_id = 3 
            pricing_id = 1
        if price_id ==  "price_1QQ669Rvd2TmzN7sYRv7DtP3":
            plan_id = 3
            pricing_id = 2
            #price_id = 'price_1QOGzqRvd2TmzN7s76nvZsjk'  # Use the Stripe price ID saved in your pricing model
            #price_id = "price_1QPH6kRvd2TmzN7s4KTG58LR"
        try:
            plan_pricing = PlanPricing.objects.get(plan_id=plan_id, pricing_id=pricing_id)
            plan = plan_pricing.plan  # Get the related plan
        except PlanPricing.DoesNotExist:
            return JsonResponse({'error': 'Plan pricing not found'}, status=404)

        # Check if the UserPlan already exists for this user
        user_plan, created = UserPlan.objects.get_or_create(user=user)

        pricing = Pricing.objects.get(id=plan_pricing.pricing_id)

        # Update the UserPlan details
        user_plan.plan = plan
        user_plan.active = 1
        user_plan.expire = timezone.now() + timezone.timedelta(days=pricing.period)
        user_plan.save()

        # Update the Order status
        Order.objects.filter(user=user, plan=plan).update(status=2)
        order = Order.objects.filter(user=user, plan=plan)
        invoice_number = get_next_value('invoice_number')

        # Create a new Invoice record
        Invoice.objects.create(
            order=Order.objects.filter(user=user, plan=plan).first(),
            user=user,
            total_net=plan_pricing.price,
            unit_price_net=plan_pricing.price,  # Set the unit_price_net field
            tax_total=0,  # Set the tax_total field
            total=plan_pricing.price,
            currency='GBP',  # Adjust as needed
            item_description=f'Subscription to {plan.name} plan',
            number=invoice_number,
            issued=timezone.now(),  # Ensure the issued field is set
            payment_date=timezone.now() + timezone.timedelta(days=pricing.period)  # Adjust as needed
        )
        
        # Create a new RecurringUserPlan entry
        
        try:
            recurring_plan = RecurringUserPlan.objects.get(pricing=pricing, user_plan=user_plan)
            recurring_plan.amount = invoice['amount_due']
            recurring_plan.tax = 0
            recurring_plan.currency='GBP'
            recurring_plan.has_automatic_renewal=True 
            recurring_plan.token=invoice['subscription'] 
            recurring_plan.token_verified=True
            recurring_plan.created=timezone.now()
            recurring_plan.updated_at=timezone.now()
            recurring_plan.renewal_triggered_by=1 
            recurring_plan.payment_provider='stripe'
            recurring_plan.save()
        except RecurringUserPlan.DoesNotExist:
            RecurringUserPlan.objects.create( pricing=pricing, user_plan=user_plan, amount=invoice['amount_due'], tax=0, currency='GBP', has_automatic_renewal=True, token=invoice['subscription'], token_verified=True, created=timezone.now(), updated_at=timezone.now(), renewal_triggered_by=1, payment_provider='stripe')
        return JsonResponse({'status': 'success'}, status=200)

    elif event['type'] == 'invoice.payment_failed':
        invoice = event['data']['object']
        stripe_customer_id = invoice['customer']
        try:
            user = User.objects.get(stripe_customer_id=stripe_customer_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        user_plan = UserPlan.objects.filter(user=user).first()
        if user_plan:
            user_plan.status = 'inactive'
            user_plan.save()

        return JsonResponse({'status': 'failed'}, status=200)

    return JsonResponse({'error': 'Unhandled event type'}, status=400)


"""
@csrf_exempt
def create_stripe_session(request):
    data = json.loads(request.body)
    plan_id = data.get('plan_id')
    pricing_id = data.get('pricing_id')

    # Fetch the Plan and Pricing from your database (replace with your actual model logic)
    plan = Plan.objects.get(id=plan_id)
    pricing = PlanPricing.objects.get(id=pricing_id)

# Ensure that the pricing is recurring
    if plan_id == 2 and pricing_id == 1:
        #price_id = 'price_1QOGy3Rvd2TmzN7sVRrtYCWU'  # Use the Stripe price ID saved in your pricing model
        price_id = "price_1QPH55Rvd2TmzN7spjv1NCet"
    elif plan_id == 2 and pricing_id == 2:
        price_id = "price_1QPH5aRvd2TmzN7s27NIgpXU"
        #price_id = 'price_1QOGyjRvd2TmzN7svhnHEHvU'  # Use the Stripe price ID saved in your pricing model
    if plan_id == 3 and pricing_id == 1:
        price_id = "price_1QPH6GRvd2TmzN7sD2bv3Vhk"
        #price_id = 'price_1QOGzKRvd2TmzN7s1gV9OSgp'  # Use the Stripe price ID saved in your pricing model
    if plan_id == 3 and pricing_id == 2:
        #price_id = 'price_1QOGzqRvd2TmzN7s76nvZsjk'  # Use the Stripe price ID saved in your pricing model
        price_id = "price_1QPH6kRvd2TmzN7s4KTG58LR"
    try:
        # Create a Checkout Session in Stripe
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,  # Use the price ID from the PlanPricing
                'quantity': 1,      # Adjust quantity if needed
            }],
            mode='subscription',  # Use 'subscription' mode for recurring payments
            success_url='https://grabbereat.com/success',  # Your success URL after payment
            cancel_url='https://grabbereat.com/cancel',    # Your cancel URL if the user cancels
        )

        return JsonResponse({'session_url': session.url})

    except stripe.error.StripeError as e:
        return JsonResponse({'error': str(e)}, status=400)
"""
from django.core.cache import cache
@csrf_exempt
def create_stripe_session(request):
    data = json.loads(request.body)
    username = data.get('username')
    plan_id = data.get('plan_id')
    pricing_id = data.get('pricing_id')

    # Fetch the User, Plan, PlanPricing, and Pricing from your database
    user = User.objects.get(id=username)
    plan = Plan.objects.get(pk=plan_id)
    plan_pricing = PlanPricing.objects.get(plan=plan, pricing_id=pricing_id)
    print(plan_pricing)
    pricing = Pricing.objects.get(pk=pricing_id)  # Fetch the correct Pricing instance

    # Check if the user has billing info
    try:
        billing_info = BillingInfo.objects.get(user=user)
    except BillingInfo.DoesNotExist:
        billing_info, created = BillingInfo.objects.create(user=user)
        billing_info.tax_number = 'ABC'
        billing_info.name = 'ZUBAIR EJAZ'
        billing_info.street = '12 BRISTOL LANE'
        billing_info.zipcode = 'AB1BH6'
        billing_info.city = 'LONDON'
        billing_info.country = 'GB'
        billing_info.save()

    try:
        # Create a new order
        order = Order.objects.create(
            user=user,
            plan=plan,
            pricing=pricing,  # Use the correct Pricing instance
            amount=plan_pricing.price,
            tax=0,
            currency='GBP'  # Adjust as needed
        )

        # Generate a unique invoice number using django-sequences
        invoice_number = get_next_value('invoice_number')

        # Create a new invoice
        """
        invoice = Invoice.objects.create(
            order=order,
            user=user,
            total_net=plan_pricing.price,
            unit_price_net=plan_pricing.price,  # Set the unit_price_net field
            tax_total=0,  # Set the tax_total field
            total=plan_pricing.price,
            currency='GBP',  # Adjust as needed
            item_description=f'Subscription to {plan.name} plan',
            number=invoice_number,
            issued=timezone.now(),  # Ensure the issued field is set
            payment_date=timezone.now() + timezone.timedelta(days=30)  # Adjust as needed
        )
        """
        # Check if the user already has a Stripe customer ID
        if not user.stripe_customer_id:
            # Create a Stripe customer
            customer = stripe.Customer.create(
                email=user.email,
                name=user.get_full_name(),
            )
            # Save the Stripe customer ID to the user
            user.stripe_customer_id = customer.id
            user.save()


        # Ensure that the pricing is recurring
        if plan_id == 2 and pricing_id == 1:
            price_id = 'price_1QOGy3Rvd2TmzN7sVRrtYCWU'  # Use the Stripe price ID saved in your pricing model
            #price_id = "price_1QPH55Rvd2TmzN7spjv1NCet"
        elif plan_id == 2 and pricing_id == 2:
            price_id = 'price_1QOGyjRvd2TmzN7svhnHEHvU'  # Use the Stripe price ID saved in your pricing model
            #price_id = "price_1QPH5aRvd2TmzN7s27NIgpXU"
        if plan_id == 3 and pricing_id == 1:
            price_id = 'price_1QOGzKRvd2TmzN7s1gV9OSgp'  # Use the Stripe price ID saved in your pricing model
            #price_id = "price_1QPH6GRvd2TmzN7sD2bv3Vhk"
        if plan_id == 3 and pricing_id == 2:
            #price_id = 'price_1QOGzqRvd2TmzN7s76nvZsjk'  # Use the Stripe price ID saved in your pricing model
            #price_id = "price_1QPH6kRvd2TmzN7s4KTG58LR"``
            price_id =  "price_1QQ669Rvd2TmzN7sYRv7DtP3"
            # Create a Checkout Session in Stripe
        session = stripe.checkout.Session.create(
            customer=user.stripe_customer_id,  # Use the Stripe customer ID
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,  # Use the stripe_price_id from the PlanPricing
                'quantity': 1,      # Adjust quantity if needed
            }],
            mode='subscription',  # Use 'subscription' mode for recurring payments
            success_url='https://grabbereat.com/success',  # Your success URL after payment
            cancel_url='https://grabbereat.com/cancel',    # Your cancel URL if the user cancels
        )

        return JsonResponse({'session_url': session.url})

    except stripe.error.StripeError as e:
        return JsonResponse({'error': str(e)}, status=400)


from plans.models import BillingInfo
from asgiref.sync import sync_to_async

@csrf_exempt
def save_billing_info(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('username')
        user = User.objects.get(id=user_id)

        billing_info, created = BillingInfo.objects.get_or_create(user=user)
        billing_info.tax_number = data.get('tax_number', billing_info.tax_number)
        billing_info.name = data.get('name', billing_info.name)
        billing_info.street = data.get('street', billing_info.street)
        billing_info.zipcode = data.get('zipcode', billing_info.zipcode)
        billing_info.city = data.get('city', billing_info.city)
        billing_info.country = data.get('country', billing_info.country)
        billing_info.shipping_name = data.get('shipping_name', billing_info.shipping_name)
        billing_info.shipping_street = data.get('shipping_street', billing_info.shipping_street)
        billing_info.shipping_zipcode = data.get('shipping_zipcode', billing_info.shipping_zipcode)
        billing_info.shipping_city = data.get('shipping_city', billing_info.shipping_city)
        billing_info.save()

        return JsonResponse({'status': 'success', 'billing_info': billing_info.id})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def get_plans(request):
    try:
        # Fetch all plans
        plans = Plan.objects.all().filter(visible=True)

        # Prepare the list to hold serialized plan data
        plans_data = []

        for plan in plans:
            # Prefetch related PlanQuota and Quota data
            plan_quotas = PlanQuota.objects.filter(plan=plan).select_related('quota')
            
            # Initialize the list for quotas data
            quotas_data = []
            for plan_quota in plan_quotas:
                quotas_data.append({
                    'quota_id': plan_quota.quota.id,
                    'quota_name': plan_quota.quota.name,
                    'quota_codename': plan_quota.quota.codename,
                    'quota_unit': plan_quota.quota.unit,
                    'quota_description': plan_quota.quota.description,
                    'quota_is_boolean': plan_quota.quota.is_boolean,
                    'quota_url': plan_quota.quota.url,
                    'quota_value': plan_quota.value,  # The value of the quota for this plan
                    'created': plan_quota.created,
                    'updated_at': plan_quota.updated_at,
                })

            # Fetch pricing details for the plan
            plan_pricing = PlanPricing.objects.filter(plan=plan).select_related('pricing')

            pricing_data = []
            for pricing in plan_pricing:
                pricing_data.append({
                    'pricing_id': pricing.pricing.id,
                    'pricing_name': pricing.pricing.name,
                    'pricing_period': pricing.pricing.period,
                    'price': str(pricing.price),  # Convert Decimal to string
                    'has_automatic_renewal': pricing.has_automatic_renewal,
                    'order': pricing.order,
                    'visible': pricing.visible,
                    'url': pricing.pricing.url,
                    'created': pricing.created,
                    'updated_at': pricing.updated_at,
                })

            # Append the plan details along with pricing and quotas data separately
            plans_data.append({
                'plan_id': plan.id,
                'plan_name': plan.name,
                'plan_description': plan.description,
                'quotas': quotas_data,  # Only quotas are here
                'pricing': pricing_data,  # Pricing details here
            })

        return JsonResponse({'plans': plans_data})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def save_zone(request):
    # Ensure the request method is POST
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)

            username = data.get('username')
            zones_data = data.get('zones')
            user = User.objects.get(pk=int(username))
            
            if not zones_data:
                return JsonResponse({'error': 'Zones data is missing'}, status=400)

            # Loop through the zones data and update/create each zone
            for zone in zones_data:
                zone_id = zone.get('id')
                zone_name = zone.get('name')
                active_status = zone.get('active')

                # Check for missing zone details
                if not zone_id or not zone_name or active_status is None:
                    return JsonResponse({'error': 'Missing zone details'}, status=400)

                # Check if the zone exists in the database for the given user
                try:
                    existing_zone = Zone.objects.get(zone_id=zone_id, user=user)
                    # If it exists, update the zone details
                    existing_zone.zone_name = zone_name
                    existing_zone.zone_toggle = active_status
                    existing_zone.save()
                except Zone.DoesNotExist:
                    # If the zone doesn't exist, create a new one
                    Zone.objects.create(
                        zone_id=zone_id,
                        user=user,
                        zone_name=zone_name,
                        zone_toggle=active_status
                    )
            updated_zones = Zone.objects.filter(user=user)

            zones_data_to_return = [
                {
                'id': zone.zone_id,
                'name': zone.zone_name,
                'active': zone.zone_toggle
                }
                for zone in updated_zones
            ]

            return JsonResponse({'message': 'Zones data saved successfully', 'zones': zones_data_to_return})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)




@csrf_exempt
def reset_password(request):
    if request.method == "POST":
        try:
            # Decode the raw body as UTF-8 (ensure it's valid UTF-8)
            body = request.body.decode('utf-8')  # Decode as UTF-8
            data = json.loads(body)  # Parse the JSON

            uid = data.get('uid')
            token = data.get('token')
            new_password = data.get('new_password')

            if not token or not new_password:
                return JsonResponse({"error": "Token and new_password are required."}, status=400)

            # Process the password reset logic here
            user = User.objects.get(pk=int(uid))
            user.set_password(new_password)
            user.save()

            return JsonResponse({"message": "Password reset successfully."}, status=200)

        except UnicodeDecodeError as e:
            return JsonResponse({"error": f"Unicode decode error: {str(e)}"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    
# Password reset request
@csrf_exempt
def forgot_password(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        email = body.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)

            # Send reset email with token
            reset_link = f"https://grabbereat.com/reset-password/{user.id}/{token}/"
            subject = 'Password Reset'
            email_body = 'Click the link to reset your password: ' + reset_link
                
            gmail_user = 'grabbereat@gmail.com'
            gmail_password = 'qquc rlcn yesb wuje'

            yag = yagmail.SMTP(gmail_user, gmail_password)

            to = [email]

            yag.send(to, subject = subject, contents = email_body)

            return JsonResponse({'message': 'Password reset link sent to your email.'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User with that email not found.'}, status=400)
    
    return JsonResponse({'message': 'Invalid request method.'}, status=405)

UserPlan = AbstractUserPlan.get_concrete_model()
PlanPricing = AbstractPlanPricing.get_concrete_model()
Plan = AbstractPlan.get_concrete_model()
Order = AbstractOrder.get_concrete_model()
BillingInfo = AbstractBillingInfo.get_concrete_model()
Quota = AbstractQuota.get_concrete_model()
Invoice = AbstractInvoice.get_concrete_model()

@csrf_exempt
def zones(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))  # Decode bytes to string
        username = body.get('username')
        user = User.objects.get(pk=int(username))
        zones = get_preferred_zones_data(request, user.justeatemail, user.justeatpw, user.email, username )
        return JsonResponse({"message":"zones retrieved", "zones": zones}, status = 200)


def get_preferred_zones_data(request, just_eat_email, just_eat_password, email, userid):

    # Plan Details



    # Proxy configuration with login and password
    
    proxy_host = 'gw.dataimpulse.com'
    proxy_port = '823'
    proxy_login = 'd824909e4ba7ceff05a7'
    proxy_password = '902ee652f9a28a99'
    proxy = f'http://{proxy_login}:{proxy_password}@{proxy_host}:{proxy_port}'
    proxy1 = f'https://{proxy_login}:{proxy_password}@{proxy_host}:{proxy_port}'

    proxies = {
        'http': proxy,
        'https': proxy1
    }
    
    url = "https://api-courier-produk.skipthedishes.com/v4/couriers/two-fa-login"
    headers = {
            "app-token": "31983a5d-37b1-4390-bd1c-8184e855e5da",
            "accept": "application/json",
            "User-Agent":"PostmanRuntime7.29.0",
            "Cache-Control":"no-cache",
            "Pragma": "no-cache",
            "Set-Cookie":"__cf_bm=kIVHRvBfvHN86XaDlB2qzKGhbnmVqooUPKAwDhCAvKI-1729788425-1.0.1.1-x7xp7JPAbkvQwK.NePd4Vf5Rl3qyQQD04B6nLBdcB7jgs0U1__REn1uXiMPTXBanfMTEPfFoUHvbtXuTowSajA; path=/; expires=Thu, 24-Oct-24 17:17:05 GMT; domain=.skipthedishes.com; HttpOnly; Secure; SameSite=None",
            "authority":"orion-http.gw.postman.co",
            "method":"POST",
            "accept":"*/*",
            "accept-encoding":"gzip, deflate, br, zstd",
            "accept-language":"en-US,en;q=0.9,hi;q=0.8",
            "content-type":"text/plain;charset=UTF-8",
            "origin":"https://web.postman.co",
            "User-Agent":"PostmanRuntime/7.42.0", "Cache-Control":"no-cache", "Postman-Token":"n01e31729-a412-411e-8296-0b94fe535d4f", "Host":"api-courier-produk.skipthedishes.com", "Accept-Encoding":"gzip%2C deflate%2C br", "Connection":"keep-alive",
            "rejectUnauthorized":"false",
            "referer":"https://web.postman.co/workspace/My-Workspace~23e9bd30-dd6d-4f5b-8e27-a270e9519610/request/create?requestId=efec554b-86fa-40f3-82fd-9db3c2fb197e",
            "sec-ch-ua-platform":"Windows","sec-fetch-des":"empty","sec-fetch-mode":"cors","sec-fetch-site":"same-site","user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        
    }
    data = {
            "email": just_eat_email,
            "password": just_eat_password
            
        }
    
    # Convert data to JSON string
    body = json.dumps(data)
    try:
        zones = []
        scraper = cloudscraper.CloudScraper()
        response = scraper.post(url, headers=headers, proxies=proxies, data=body).text
        if response:
            response_data = json.loads(response)
            #print(response_data)
        else:
            return zones
        #return response_data
        # returns a CloudScraper instance
        # Extract relevant data from the response
        user_id = response_data.get('id')
        user_token = response_data.get('token')
        # Make the GET request to the new URL
        get_url = 'https://api-courier-produk.skipthedishes.com/v4/couriers/'+user_id+'/preferred-zones-max-courier-hours'
        #print(get_url, user_token, user_id) 

        get_headers = {
                "accept":"application/json",
                "Accept-Encoding":"gzip",
                "app-build":"231",
                "app-token": "31983a5d-37b1-4390-bd1c-8184e855e5da",
                "app-version":"5.2.1 - 231",
                "Cache-Control":"no-cache",
                "Connection":"Keep-Alive",
                "Content-Length":"0",
                "Cookie":"__cf_bm=rGXwJsR50ygqOQPXSAo_I5Vvq0dp2YQZDWyMrtkcmes-1730356103-1.0.1.1-IAHS6AijB2lAEMxQ0ZqlY7WCdLlmAXczc8xEqYIgrg0WcMExF_aztpKymfu7mN.CqnAxWO_sPPV4VCy5_TGslQ",
                "device-id":"156cd6b1a5acdb2c",
                "Host":"api-courier-produk.skipthedishes.com",
                "model":"SM-A715F",
                "platform":"Android",
                "platform-version":"13",
                "tenant-id":"uk",
                "user-agent":"SkipTheDishes-COURAPP-Just Eat / (Android - 5.2.1 - 231)",
                "user-token": user_token
            }
        scraper2 = cloudscraper.CloudScraper()
        get_response = scraper2.get(url=get_url, proxies=proxies, headers=get_headers).text 
        #get_response = requests.get(get_url, headers=get_headers, params=params)
        #get_response_data = get_response.json()
        get_response_data = json.loads(get_response)

        #logic for parsing through a json response and creating a json object to send to react frontend

        assignable_zones = get_response_data.get('assignableZones', [])
        #print(get_response_data)

        # Creating a new dictionary to hold the zones in a specific format
        zones = []
        user = User.objects.get(pk=int(userid))
        #print(userid)

        for zone in assignable_zones:
            try:
                existing_zone = Zone.objects.get(user=user, zone_id=zone.get('id'))
                print(zone.get('id'))
                
                zones.append({
                    'id': zone.get('id'),  # Zone ID
                    'name': zone.get('name'),  # Zone name
                    'description': zone.get('groupId'),  # Zone description
                    'active': existing_zone.zone_toggle,  # Zone toggle (active or inactive)
                })
            except Exception as e: # Handle any exception 
                print(f"An error occurred: {e}")                
                zones.append({
                    'id': zone.get('id'),  # Zone ID
                    'name': zone.get('name'),  # Zone name
                    'description': zone.get('groupId'),  # Zone description
                    'active': True,  # Zone toggle (active or inactive)
                })
            #existing_zone = Zone.objects.get(zone_id=zone.get('id'), user=user)

        # Now `zones` is a dictionary with both preferred and assignable zones
        # You can send this `zones` dictionary as the response to the frontend

        response_data_z = zones  # Wrap the data into a response object for the frontend


        # Return this response as a JSON object
        return response_data_z
    except:
        print("ERROR")

def savezones(request):
    return HttpResponse('{"success":"Zones Preferences Saved"}')

def referralsfront(request):
    try:
        code = Referral.objects.get(user=request.user)
        referrer_user = User.objects.get(username=request.user.username)
        # Referral Count
        plan_name_premium = 'PREMIUM'
        plan_name_basic = 'BASIC'
        pricing_value_weekly = 1
        pricing_value_monthly = 2
        referral_counts_basic_weekly = get_referral_counts(referrer_user, plan_name_basic, pricing_value_weekly)
        referral_counts_basic_monthly = get_referral_counts(referrer_user, plan_name_basic, pricing_value_monthly)
        referral_counts_premium_weekly = get_referral_counts(referrer_user, plan_name_premium, pricing_value_weekly)
        referral_counts_premium_monthly = get_referral_counts(referrer_user, plan_name_premium, pricing_value_monthly)

    except Referral.DoesNotExist:
        code = None
        referrer_user = None
    return render(request, "referralsfront.html", {"referral_code":code, "referrer_user": referrer_user})

def convert_on_off(value):
  if value == 'on' or value == True:
    return True
  elif value == 'off' or value == False:
    return False
  else:
    raise ValueError("Invalid value: {}".format(value))

def send_email(user, recipient, subject, body, user_whatsapp_number):
    whatsapp_validator = WhatsAppValidator()
    email_validator = EmailValidator()

    if email_validator.validate(user) and user.email_notif_toggle:

        gmail_user = 'grabbereat@gmail.com'
        gmail_password = 'qquc rlcn yesb wuje'
        shift_from_t = body.get('shiftTime').get('start')/1000
        shift_to_t = body.get('shiftTime').get('end')/1000
        dt_object_1 = datetime.fromtimestamp(shift_from_t)
        dt_object_2 = datetime.fromtimestamp(shift_to_t)

        date = dt_object_1.strftime("%d/%m/%Y")
        timefrom =  dt_object_1.strftime("%H:%M")
        timeto =  dt_object_2.strftime("%H:%M")

        newbody = "A new shift has been arranged for you. Check out the details: \n Date: "+date+" \n Time : "+timefrom+" - "+timeto+" \n Area: "+body.get('location')

        yag = yagmail.SMTP(gmail_user, gmail_password)

        sent_from = gmail_user
        to = [recipient]

        email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, to, subject, newbody)
        yag.send(to, subject = subject, contents = newbody)
    if whatsapp_validator.validate(user) and user.mobile_notif_toggle:
        client = Client('', '')

        message = client.messages.create(
            content_sid= "",
            content_variables=json.dumps({"1":date, "2":timefrom + " - " + timeto, "3": body.get('location')}),
            from_='whatsapp:+18509612448',
            messaging_service_sid= "",
            to='whatsapp:{}'.format(user_whatsapp_number),
        )
        #print(user_whatsapp_number)
        #print(message.sid)
        #print('Great! Expect a message...')

def find_string_and_read_line(file_path, search_string):
    logs = []
    logs_line = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            if search_string in line:
                logs_line.append(line_number)
                logs.append(previous_line)
            previous_line = line
        file.close()
        return logs_line, logs

    return None, None

def get_logs(user_id):

    file_path = 'logs/'+str(user_id)+'.txt'  # Replace with your file path
    search_string = 'available_shifts_accepted'  # Replace with the string you want to find


    line_number, line_content = find_string_and_read_line(file_path, search_string)

    if line_number:
        logs = line_content
    else:
        return ('nothing found')
    return logs

@csrf_exempt
def logs(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))  # Decode bytes to string
            username = body.get('username')
            #print(username)
            logs = get_logs(username)
            newbody = []

            for body in logs:
                
                body = eval(body)
                bod = json.dumps(body)
                bod = json.loads(bod)
                
                shift_from_t = bod.get('shiftTime').get('start')/1000
                shift_to_t = bod.get('shiftTime').get('end')/1000
                dt_object_1 = datetime.fromtimestamp(shift_from_t)
                dt_object_2 = datetime.fromtimestamp(shift_to_t)

                date = dt_object_1.strftime("%d/%m/%Y")
                timefrom =  dt_object_1.strftime("%H:%M")
                timeto =  dt_object_2.strftime("%H:%M")

                newbody.append({"date": date, "time": timefrom + '-' + timeto, "Zone" : bod.get('location'), "message" : "A new shift has been arranged for you." })


            if logs:
                return JsonResponse({'message': 'Log Query Successful', 'logs' : newbody }, status=200)
            else:
                return JsonResponse({'message': 'Log Query Unsuccessful'}, status=400)
        except:
            return JsonResponse({'message': 'Log Query Unsuccessful'}, status=400)
    
def epoch_conv(epoch):
    epoch = epoch / 1000.0
    str_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime(epoch))
    return str_time

@csrf_exempt  # Use this decorator if you want to disable CSRF protection for this view (useful for testing purposes)
def index(request):
    if  request.user.is_authenticated:
        
        whatsapp_validator = WhatsAppValidator()

        email_validator = EmailValidator()

        return render(request, "start.html")
    else:
        return render(request, "index.html")

def contact(request):
    return render(request, "contact.html")

@csrf_exempt
def notifications(request):

    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))  # Decode bytes to string
            username = body.get('username')
            #print(username)
            
            user = User.objects.get(pk=int(username))
            return JsonResponse({ "message":"Successfully retrieved schedule", "user_id": user.id, "email": user.email_notif , "whatsapp": user.mobile_notif , "emailNotifications": user.email_notif_toggle , "whatsappNotifications" : user.mobile_notif_toggle } , status=200)
        except:
            return JsonResponse({ "message":"Error retrieving schedule" }, status=400)

def profile(request):
    return render(request, "profile.html")

@csrf_exempt
@never_cache
def schedule(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))  # Decode bytes to string
            username = body.get('username')
            #print(username)
            
            user = User.objects.get(pk=int(username))
            mon_time_from = user.mon_time_from;
            mon_time_to = user.mon_time_to;
            tue_time_from = user.tue_time_from;
            tue_time_to = user.tue_time_to;
            wed_time_from = user.wed_time_from;
            wed_time_to = user.wed_time_to;
            thu_time_from = user.thu_time_from;
            thu_time_to = user.thu_time_to;
            fri_time_from = user.fri_time_from;
            fri_time_to = user.fri_time_to;
            sat_time_from = user.sat_time_from;
            sat_time_to = user.sat_time_to;
            sun_time_from = user.sun_time_from;
            sun_time_to = user.sun_time_to;
            if(mon_time_from==time1.time(23,59)):
                mon_time_from="24"
            else:
                mon_time_from=user.mon_time_from.strftime("%H")
            
            if(mon_time_to==time1.time(23,59)):
                mon_time_to="24"
            else:
                mon_time_to=user.mon_time_to.strftime("%H")
            if(tue_time_from==time1.time(23,59)):
                tue_time_from="24"
            else:
                tue_time_from=user.tue_time_from.strftime("%H")
            if(tue_time_to==time1.time(23,59)):
                tue_time_to="24"
            else:
                tue_time_to=user.tue_time_to.strftime("%H")
            if(wed_time_from==time1.time(23,59)):
                wed_time_from="24"
            else:
                wed_time_from=user.wed_time_from.strftime("%H")
            if(wed_time_to==time1.time(23,59)):
                wed_time_to="24"
            else:
                wed_time_to=user.wed_time_to.strftime("%H")
            if(thu_time_from==time1.time(23,59)):
                thu_time_from="24"
            else:
                thu_time_from=user.thu_time_from.strftime("%H")
            if(thu_time_to==time1.time(23,59)):
                thu_time_to="24"
            else:
                thu_time_to=user.thu_time_to.strftime("%H")
            if(fri_time_from==time1.time(23,59)):
                fri_time_from="24"
            else:
                fri_time_from=user.fri_time_from.strftime("%H")
            if(fri_time_to==time1.time(23,59)):
                fri_time_to="24"
            else:
                fri_time_to=user.fri_time_to.strftime("%H")
            if(sat_time_from==time1.time(23,59)):
                sat_time_from="24"
            else:
                sat_time_from=user.sat_time_from.strftime("%H")
            if(sat_time_to==time1.time(23,59)):
                sat_time_to="24"
            else:
                sat_time_to=user.sat_time_to.strftime("%H")
            if(sun_time_from==time1.time(23,59)):
                sun_time_from="24"
            else:
                sun_time_from=user.sun_time_from.strftime("%H")            
            if(sun_time_to==time1.time(23,59)):
                sun_time_to="24"
            else:
                sun_time_to=user.sun_time_to.strftime("%H")
            return JsonResponse({ "message":"Successfully retrieved schedule", "user_id": user.id, "Monday": { "range": [int(mon_time_from), int(mon_time_to)], "enabled": user.mon_time_toggle } , "Tuesday": { "range": [int(tue_time_from), int(tue_time_to)], "enabled": user.tue_time_toggle } , "Wednesday": { "range": [int(wed_time_from), int(wed_time_to)], "enabled": user.wed_time_toggle } , "Thursday": { "range": [int(thu_time_from), int(thu_time_to)], "enabled": user.thu_time_toggle } , "Friday": { "range": [int(fri_time_from), int(fri_time_to)], "enabled": user.fri_time_toggle } , "Saturday": { "range": [int(sat_time_from), int(sat_time_to)], "enabled": user.sat_time_toggle } , "Sunday": { "range": [int(sun_time_from), int(sun_time_to)], "enabled": user.sun_time_toggle }  }, status=200)
        except:
            return JsonResponse({ "message":"Error retrieving schedule" }, status=400)
        
@csrf_exempt
def saveprofile(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))  # Decode bytes to string
            #print(body)
            username = body.get('username')
            #print(username)
            
            user = User.objects.get(pk=int(username))    
            current_password  = body.get('currentPassword');
            new_password  = body.get('newPassword');
            new_password_confirm  = body.get('newPassword');
            # Ensure password matches confirmation
            if new_password != new_password_confirm:
                JsonResponse({"message":"Passwords Must Match"}, status=400)
                
            if(user.check_password(current_password)):
                user.set_password(new_password)
                user.save()
                return JsonResponse({"message":"Save Password Success"}, status=200)
            else:
                return JsonResponse({"message":"Wrong Current Password"}, status=400)
        except:
            return JsonResponse({"message":"Save Password Failed"}, status=400)

@csrf_exempt
def savenotifications(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))  # Decode bytes to string
            body = body.get('settings')
            user_id = body.get('user_id');
            email_notif = body.get('email');
            mobile_notif = body.get('whatsapp');
            email_notif_toggle = body.get('emailNotifications');
            mobile_notif_toggle = body.get('whatsappNotifications');
            user = User.objects.get(pk=int(user_id))
            user.email_notif = email_notif
            user.mobile_notif = mobile_notif 
            user.email_notif_toggle = email_notif_toggle
            user.mobile_notif_toggle = mobile_notif_toggle
            user.save()
            return JsonResponse({
                "message": "Success:  Notification Preferences Saved"
            }, status=200)
        except:
            return JsonResponse({
                "message": "Error:  Notification Preferences Not Saved"
            }, status=400)

@csrf_exempt
@never_cache
def saveschedule(request):

    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))  # Decode bytes to string
            #print(body)
            user_id = body.get('user_id')
            mon_time = body.get('Monday').get('range');
            tue_time = body.get('Tuesday').get('range');
            wed_time = body.get('Wednesday').get('range');
            thu_time = body.get('Thursday').get('range');
            fri_time = body.get('Friday').get('range');
            sat_time = body.get('Saturday').get('range');
            sun_time = body.get('Sunday').get('range');
            mon_time_toggle = body.get('Monday').get('enabled');
            tue_time_toggle = body.get('Tuesday').get('enabled');
            wed_time_toggle = body.get('Wednesday').get('enabled');
            thu_time_toggle = body.get('Thursday').get('enabled');
            fri_time_toggle = body.get('Friday').get('enabled');
            sat_time_toggle = body.get('Saturday').get('enabled');
            sun_time_toggle = body.get('Sunday').get('enabled');
            user = User.objects.get(pk=user_id)
            user.mon_time_from = time1.time(int(mon_time[0]), 0)
            if(int(mon_time[1])==24):
                user.mon_time_to = time1.time(23, 59)
            else:
                user.mon_time_to = time1.time(int(mon_time[1]), 0)
            user.tue_time_from = time1.time(int(tue_time[0]), 0)
            if(int(tue_time[1])==24):
                user.tue_time_to = time1.time(23, 59)
            else:
                user.tue_time_to = time1.time(int(tue_time[1]), 0)
            user.wed_time_from = time1.time(int(wed_time[0]), 0)
            if(int(wed_time[1])==24):
                user.wed_time_to = time1.time(23, 59)
            else:
                user.wed_time_to = time1.time(int(wed_time[1]), 0)
            user.thu_time_from = time1.time(int(thu_time[0]), 0)
            if(int(thu_time[1])==24):
                user.thu_time_to = time1.time(23, 59)
            else:
                user.thu_time_to = time1.time(int(thu_time[1]), 0)
            user.fri_time_from = time1.time(int(fri_time[0]), 0)
            if(int(fri_time[1])==24):
                user.fri_time_to = time1.time(23, 59)
            else:
                user.fri_time_to = time1.time(int(fri_time[1]), 0)
            user.sat_time_from = time1.time(int(sat_time[0]), 0)
            if(int(sat_time[1])==24):
                user.sat_time_to = time1.time(23, 59)
            else:
                user.sat_time_to = time1.time(int(sat_time[1]), 0)
            user.sun_time_from = time1.time(int(sun_time[0]), 0)
            if(int(sun_time[1])==24):
                user.sun_time_to = time1.time(23, 59)
            else:
                user.sun_time_to = time1.time(int(sun_time[1]), 0)
            user.mon_time_toggle = mon_time_toggle
            user.tue_time_toggle = tue_time_toggle
            user.wed_time_toggle = wed_time_toggle
            user.thu_time_toggle = thu_time_toggle
            user.fri_time_toggle = fri_time_toggle
            user.sat_time_toggle = sat_time_toggle
            user.sun_time_toggle = sun_time_toggle
            user.save()
            return JsonResponse({'message':'Saved Successfully'},status=200)
        except:
            return JsonResponse({'message':'Not Saved'},status=400)

import asyncio
import traceback
from datetime import datetime
async def safe_sleep(duration, flag, user_id):
    """Break sleep into smaller chunks with protection"""
    chunks = int(duration)
    for i in range(chunks):
        if not flag.is_set():
            #print(f"[User {user_id}] Flag cleared during sleep chunk {i}")
            return False
            
        try:
            # Shield the sleep to prevent cancellation
            await asyncio.shield(asyncio.sleep(1))
            #print(f"[User {user_id}] Completed sleep chunk {i+1}/{chunks}")
        except asyncio.CancelledError:
            #print(f"[User {user_id}] Sleep cancelled in chunk {i+1}")
            if not flag.is_set():
                return False
            raise
    return True


# In your User model or a utility file
async def async_save(instance):
    await sync_to_async(instance.save)()


async def startgrabbing(flag, user, email, user_whatsapp_number, justeatemail, justeatpw, user_id):
    try:
        while flag.is_set():
            try:
                #print(f"[User {user_id}] Starting iteration")
                
                # Use sync_to_async for any synchronous database operations
                from asgiref.sync import sync_to_async
                check_plan_expiry_sync = sync_to_async(check_plan_expiry)
                is_expired, expiry_date = await check_plan_expiry_sync(user_id)
                if not is_expired:
                    try:

                        await asyncio.sleep(1)
                    except asyncio.CancelledError:
                        if not flag.is_set():
                            #print(f"[User {user_id}] Flag cleared during sleep")
                            break
                        raise
                    # Make sure get_data is properly async
                    get_response_data = await get_data(user, justeatemail, justeatpw, 
                                                    email, user_whatsapp_number, user_id)
                else:
                    #print(f"[User {user_id}] Plan expired. Stopping task.")
                    break       
            except asyncio.CancelledError:
                #print(f"[User {user_id}] Task cancelled")
                raise
            except Exception as e:
                #print(f"[User {user_id}] Error: {str(e)}")
                #traceback.print_exc()
                if not flag.is_set():
                    break
                await asyncio.sleep(1)
                
    finally:
        #print(f"[User {user_id}] Starting cleanup")
        try:
            # Use sync_to_async if user.save() is synchronous
            user.thread_toggle = False
            await async_save(user)  # Make sure this is truly async
            #print(f"[User {user_id}] User saved")
        except Exception as e:
            #print(f"[User {user_id}] Cleanup error: {str(e)}")
            traceback.print_exc()
        
        if user_id in user_threads:
            del user_threads[user_id]
            #print(f"[User {user_id}] Removed from user_threads")


# Modify startprocess to add more logging
@csrf_exempt
async def startprocess(request):
    try:
        body = json.loads(request.body)
        user_id = str(body.get('username'))
        #print(f"[User {user_id}] Start request received")
        log_open_files()
        
        # Make sure to use the async version of get()
        user = await User.objects.aget(pk=int(user_id))
        email = user.email
        user_whatsapp_number = user.mobile_notif
        justeatemail = user.justeatemail
        justeatpw = user.justeatpw
        
        if user_id in user_threads:
            #print(f"[User {user_id}] Thread already exists")
            return JsonResponse({"message": "Thread already running"}, status=400)
        
        execution_flag = asyncio.Event()
        execution_flag.set()
        
        task = asyncio.create_task(
            startgrabbing(execution_flag, user, email, user_whatsapp_number, 
                         justeatemail, justeatpw, user_id)
        )
        task.set_name(f"task_user_{user_id}")
        
        def task_done_callback(task):
            #try:
            print(f"[User {user_id}] Task completed")
                #if task.exception():
                    #print(f"[User {user_id}] Task error: {task.exception()}")
            #except Exception as e:
                #print(f"[User {user_id}] Callback error: {str(e)}")

        task.add_done_callback(task_done_callback)
        user_threads[user_id] = (task, execution_flag)
        
        return JsonResponse({"message": "Thread started"}, status=200)
        
    except Exception as e:
        print(f"[User {user_id}] Error in startprocess: {str(e)}")
        traceback.print_exc()
        return JsonResponse({"message": "Error starting process"}, status=500)

@csrf_exempt
async def stopprocess(request):
    body = json.loads(request.body)
    user_id = str(body.get('username'))
    
    if user_id in user_threads:
        task, execution_flag = user_threads[user_id]
        #print(f"[User {user_id}] Stop process initiated")
        
        # First clear the flag
        execution_flag.clear()
        #print(f"[User {user_id}] Flag cleared")
        
        try:
            # Give the task time to clean up gracefully
            await asyncio.wait_for(task, timeout=2.0)
            #print(f"[User {user_id}] Task completed gracefully")
        except asyncio.TimeoutError:
            print(f"[User {user_id}] Graceful shutdown timed out, forcing cancel")
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                print(f"[User {user_id}] Task cancelled successfully")
        
        if user_id in user_threads:
            del user_threads[user_id]
        
        return JsonResponse({"message": "Thread stopped"}, status=200)
    else:
        return JsonResponse({"message": "No thread found"}, status=400)

def log_open_files():
    process = psutil.Process(os.getpid())
    open_files = process.open_files()
    print(f"Number of open files: {len(open_files)}")
    return open_files

@csrf_exempt
async def check_execution_status(request):
    user_id = request.GET.get('username')
    user = await User.objects.aget(pk=int(user_id))
    # Ensure the user_id is always treated as a string 
    user_id = str(user_id)
    
    # Check if user has an active thread in user_threads dictionary
    #if user_id in user_threads and user.thread_toggle:
    if user_id in user_threads:
        return JsonResponse({"execution_status": "running"}, status=200) 
    else:
        return JsonResponse({"execution_status": "stopped"}, status=200)

def check_plan_expiry(user_id):
    # Get the current active user plan (subscription)
    try:
        user = User.objects.get(pk=int(user_id))
        user_plan = UserPlan.objects.get(user=user, active=True)

        # Get the associated plan and expiry date
        plan = user_plan.plan
        expiry_date = datetime.combine(user_plan.expire, datetime.min.time()).astimezone()  # Assuming the end date is stored here

        # Check if the subscription has expired
        is_expired = expiry_date < timezone.now()

        return is_expired, expiry_date
    
    except UserPlan.DoesNotExist:
        return True, None  # Plan expired or user does not have a plan

async def get_data(user, just_eat_email, just_eat_password, email, user_whatsapp_number, user_id):
    # Proxy configuration with login and password
    

    file_path = 'logs/'+str(user_id)+'.txt'  # Replace with your file path
    # Open file for writing
    try:


        proxy_host = 'gw.dataimpulse.com'
        proxy_port = '823'
        proxy_login = 'd824909e4ba7ceff05a7'
        proxy_password = '902ee652f9a28a99'
        proxy = f'http://{proxy_login}:{proxy_password}@{proxy_host}:{proxy_port}'
        proxy1 = f'https://{proxy_login}:{proxy_password}@{proxy_host}:{proxy_port}'

        proxies = {
            'http': proxy,
            'https': proxy1
        }
        
        url = "https://api-courier-produk.skipthedishes.com/v4/couriers/two-fa-login"
        headers = {
                "app-token": "31983a5d-37b1-4390-bd1c-8184e855e5da",
                "accept": "application/json",
                "User-Agent":"PostmanRuntime7.29.0",
                "Cache-Control":"no-cache", 
                "Pragma": "no-cache",
                "Set-Cookie":"__cf_bm=kIVHRvBfvHN86XaDlB2qzKGhbnmVqooUPKAwDhCAvKI-1729788425-1.0.1.1-x7xp7JPAbkvQwK.NePd4Vf5Rl3qyQQD04B6nLBdcB7jgs0U1__REn1uXiMPTXBanfMTEPfFoUHvbtXuTowSajA; path=/; expires=Thu, 24-Oct-24 17:17:05 GMT; domain=.skipthedishes.com; HttpOnly; Secure; SameSite=None",
                "authority":"orion-http.gw.postman.co",
                "method":"POST",
                "accept":"*/*",
                "accept-encoding":"gzip, deflate, br, zstd",
                "accept-language":"en-US,en;q=0.9,hi;q=0.8",
                "content-type":"text/plain;charset=UTF-8",
                "origin":"https://web.postman.co",
                "User-Agent":"PostmanRuntime/7.42.0", "Cache-Control":"no-cache", "Postman-Token":"n01e31729-a412-411e-8296-0b94fe535d4f", "Host":"api-courier-produk.skipthedishes.com", "Accept-Encoding":"gzip%2C deflate%2C br", "Connection":"keep-alive",
                "rejectUnauthorized":"false",
                "referer":"https://web.postman.co/workspace/My-Workspace~23e9bd30-dd6d-4f5b-8e27-a270e9519610/request/create?requestId=efec554b-86fa-40f3-82fd-9db3c2fb197e",
                "sec-ch-ua-platform":"Windows","sec-fetch-des":"empty","sec-fetch-mode":"cors","sec-fetch-site":"same-site","user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
            
        }
        data = {
                "email": just_eat_email,
                "password": just_eat_password
                
            }
        

        # Convert data to JSON string
        body = json.dumps(data)
        try:
            # Create a regular CloudScraper instance
            scraper = cloudscraper.create_scraper()
            # Convert synchronous requests to async
            async_post = sync_to_async(scraper.post)
            async_get = sync_to_async(scraper.get)
            response = scraper.post(url, headers=headers, proxies=proxies, data=body)
            response_text = response.text

            if response_text:
                response_data = json.loads(response_text)
                #print(response_data)
            else:
                return "{'scheduledShifts': [], 'availableShifts': []}"

            user_id = response_data.get('id')
            user_token = response_data.get('token')
            
            get_url = "https://api-courier-produk.skipthedishes.com/v2/couriers/"+user_id+"/shifts/scheduled?includeAvailable=true&timezoneEurope%2FLondon&hasCourierRefreshedOpenShifts=true"

            get_headers = { 
                    "accept":"application/json",
                    "Accept-Encoding":"gzip",
                    "app-build":"231",
                    "app-token": "31983a5d-37b1-4390-bd1c-8184e855e5da",
                    "app-version":"5.2.1 - 231",
                    "Cache-Control":"no-cache",
                    "Connection":"Keep-Alive",
                    "Content-Length":"0",
                    "Cookie":"__cf_bm=rGXwJsR50ygqOQPXSAo_I5Vvq0dp2YQZDWyMrtkcmes-1730356103-1.0.1.1-IAHS6AijB2lAEMxQ0ZqlY7WCdLlmAXczc8xEqYIgrg0WcMExF_aztpKymfu7mN.CqnAxWO_sPPV4VCy5_TGslQ",
                    "device-id":"156cd6b1a5acdb2c",
                    "Host":"api-courier-produk.skipthedishes.com",
                    "model":"SM-A715F",
                    "platform":"Android",
                    "platform-version":"13",
                    "tenant-id":"uk",
                    "user-agent":"SkipTheDishes-COURAPP-Just Eat / (Android - 5.2.1 - 231)",
                    "user-token": user_token
                }
            scraper2 = cloudscraper.create_scraper() # Convert synchronous requests to async
            async_post2 = sync_to_async(scraper2.post)
            async_get2 = sync_to_async(scraper2.get)
            get_response = scraper2.get(url=get_url, proxies=proxies, headers=get_headers)
            get_response_text = get_response.text
            get_response_data = json.loads(get_response_text)
            #print(get_response_data)

            now = timezone.now()
            timenow = now.time()

            day_of_week_number = now.weekday()
            
            days = ["mon_", "tue_", "wed_", "thu_", "fri_", "sat_", "sun_"]
            day_of_week_name = days[day_of_week_number]

            schednamefrom = day_of_week_name + "time_from"
            schednameto = day_of_week_name + "time_to"
            togglename = day_of_week_name + "time_toggle" 
            schedtimefrom = getattr(user, schednamefrom, None)
            schedtimeto = getattr(user, schednameto, None)
            toggle = getattr(user, togglename, None)

            if get_response_data.get('availableShifts'): 
                for indx in get_response_data.get('availableShifts'):
                    if is_time_in_range(schedtimefrom, schedtimeto, timenow) and toggle:
                        with open(file_path, 'a+') as f:
                            print(indx, file=f)                
                            shift_id = indx['id']
                            post_url = "https://api-courier-produk.skipthedishes.com/v2/couriers/"+user_id+"/shifts/"+shift_id+"/confirm"
            
                            post_headers = {
                                "accept":"application/json",
                                "Accept-Encoding":"gzip",
                                "app-build":"231",
                                "app-token": "31983a5d-37b1-4390-bd1c-8184e855e5da",
                                "app-version":"5.2.1 - 231",
                                "Cache-Control":"no-cache",
                                "Connection":"Keep-Alive",
                                "Content-Length":"0",
                                "Cookie":"__cf_bm=rGXwJsR50ygqOQPXSAo_I5Vvq0dp2YQZDWyMrtkcmes-1730356103-1.0.1.1-IAHS6AijB2lAEMxQ0ZqlY7WCdLlmAXczc8xEqYIgrg0WcMExF_aztpKymfu7mN.CqnAxWO_sPPV4VCy5_TGslQ",
                                "device-id":"156cd6b1a5acdb2c",
                                "Host":"api-courier-produk.skipthedishes.com",
                                "model":"SM-A715F",
                                "platform":"Android",
                                "platform-version":"13",
                                "tenant-id":"uk",
                                "user-agent":"SkipTheDishes-COURAPP-Just Eat / (Android - 5.2.1 - 231)",
                                "user-token": user_token
                            }
                            scraper3 = cloudscraper.create_scraper()
                            # Convert synchronous requests to async
                            async_post3 = sync_to_async(scraper3.post)
                            async_get3 = sync_to_async(scraper3.get)
                            post_response = scraper3.post(url=post_url, proxies=proxies, headers=post_headers)
                            post_response_text = post_response.text
                            post_response_data = json.loads(post_response_text)

                            if(post_response_data.get('status') == 'SUCCESS_SHIFT_CONFIRMED'):
                                print("available_shifts_accepted:", file=f)
                                print(post_response_data, file=f)
                                send_email_sync = sync_to_async(send_email)
                                await send_email_sync(user, user.email_notif, "Notification Email", indx, user.mobile_notif)
                            else:
                                print("available_shifts_error:", file=f)
                                print(post_response_data, file=f)
                            #f.close()

                    else:
                        with open(file_path, 'a+') as f:
                            print("available_shifts_rejected:", file=f)
                            #f.close()

                
        except requests.RequestException as e:
            get_response_data = {"error": str(e)}

    except Exception as e:
        get_response_data = {"error": str(e)}
        
        # Then restore the original stdout
    return get_response_data
def is_time_in_range(start_time, end_time, check_time):
    """Checks if a given time is within a specified range."""
    if start_time <= end_time:
        return start_time <= check_time <= end_time
    else:  # Time range crosses midnight
        return check_time >= start_time or check_time <= end_time

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
import json

def request_to_dict(request):
    # Initialize an empty dictionary
    data = {}

    data = {
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'mobile': request.user.mobile,
        'open_runs_toggle': request.user.open_runs_toggle,
        'overflows_toggle': request.user.overflows_toggle,
        'justEatCredentials': {'username' : request.user.justeatemail, 'password' : request.user.justeatpw},
        'currentPlan' : current_plan(request.user.id)
        }

    data['method'] = request.method
    data['path'] = request.path
    data['user_agent'] = request.META.get('HTTP_USER_AGENT')
    data['ip_address'] = request.META.get('REMOTE_ADDR')
    return data


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))  # Decode bytes to string
            #print(body)
            username = body.get('username')
            password = body.get('password')

            if not username or not password:
                return JsonResponse({'error': 'Please provide both username and password'}, status=400)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                user_data = {
                    'username': request.user.username,
                    'email': request.user.email,
                    # Add other relevant user data as needed
                }
                return JsonResponse({'message': 'Login successful', 'userAuthenticated' : request.user.is_authenticated, 'request' : request_to_dict(request)  })
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# CSRF Token view


"""
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST.get('username')
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            #login(request, user)        
            data = { 'method': request.method, 'path': request.path, 'status': 'success', 'username': username}
            return JsonResponse(data=data, safe=False)
        else:
            data = { 'method': request.method, 'path': request.path, 'status': 'error', 'username': username}
            return JsonResponse(data=data, safe=False)
    else:
        data = { 'method': request.method, 'path': request.path}
        return JsonResponse(data=data, safe=False)
"""

def logout_view(request):
    logout(request)
    return redirect(reverse("index"))

@csrf_exempt
def save_justeat_credentials(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode('utf-8'))  # Decode bytes to string
            #print(body)
            username = body.get("username")
            justeatemail = body.get("justeatemail")
            justeatpw = body.get("justeatpw")


            proxy_host = 'gw.dataimpulse.com'
            proxy_port = '823'
            proxy_login = 'd824909e4ba7ceff05a7'
            proxy_password = '902ee652f9a28a99'
            proxy = f'http://{proxy_login}:{proxy_password}@{proxy_host}:{proxy_port}'
            proxy1 = f'https://{proxy_login}:{proxy_password}@{proxy_host}:{proxy_port}'

            proxies = {
                'http': proxy,
                'https': proxy1
            }
            
            url = "https://api-courier-produk.skipthedishes.com/v4/couriers/login"
            headers = {
                    "app-token": "31983a5d-37b1-4390-bd1c-8184e855e5da",
                    "accept": "application/json",
                    "User-Agent":"PostmanRuntime7.29.0",
                    "Cache-Control":"no-cache",
                    "Pragma": "no-cache",
                    "Set-Cookie":"__cf_bm=kIVHRvBfvHN86XaDlB2qzKGhbnmVqooUPKAwDhCAvKI-1729788425-1.0.1.1-x7xp7JPAbkvQwK.NePd4Vf5Rl3qyQQD04B6nLBdcB7jgs0U1__REn1uXiMPTXBanfMTEPfFoUHvbtXuTowSajA; path=/; expires=Thu, 24-Oct-24 17:17:05 GMT; domain=.skipthedishes.com; HttpOnly; Secure; SameSite=None",
                    "authority":"orion-http.gw.postman.co",
                    "method":"POST",
                    "accept":"*/*",
                    "accept-encoding":"gzip, deflate, br, zstd",
                    "accept-language":"en-US,en;q=0.9,hi;q=0.8",
                    "content-type":"text/plain;charset=UTF-8",
                    "origin":"https://web.postman.co",
                    "User-Agent":"PostmanRuntime/7.42.0", "Cache-Control":"no-cache", "Postman-Token":"n01e31729-a412-411e-8296-0b94fe535d4f", "Host":"api-courier-produk.skipthedishes.com", "Accept-Encoding":"gzip%2C deflate%2C br", "Connection":"keep-alive",
                    "rejectUnauthorized":"false",
                    "referer":"https://web.postman.co/workspace/My-Workspace~23e9bd30-dd6d-4f5b-8e27-a270e9519610/request/create?requestId=efec554b-86fa-40f3-82fd-9db3c2fb197e",
                    "sec-ch-ua-platform":"Windows","sec-fetch-des":"empty","sec-fetch-mode":"cors","sec-fetch-site":"same-site","user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
                
            }
            data = {
                    "email": justeatemail,
                    "password": justeatpw
                    
                }
            
            # Convert data to JSON string
            body = json.dumps(data)
            
        
            try:
                scraper = cloudscraper.CloudScraper()
                response = scraper.post(url, headers=headers, proxies=proxies, data=body).text
                if response:
                    response_data = json.loads(response)
                    print(response_data) 
                if response_data.get('id') and response_data.get('token'):
                    user = User.objects.get(id=username)
                    user.justeatemail = justeatemail
                    user.justeatpw = justeatpw
                    user.save()
                    user_exists = User.objects.filter(justeatemail=justeatemail).first()
                    if not user_exists:
                        assign_trial_plan(user, user.id)
                    return JsonResponse({"success":"Success: Credentials Saved"}, status=200)
                else:
                    return JsonResponse({"message":"Error Registering JustEat Credentials"}, status=400)
            except:
                return JsonResponse({"message":"Error Saving JustEat Credentials"}, status=400)
        except:
            return JsonResponse({"message":"Error contacting JustEat Server"}, status=400)
@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode('utf-8'))  # Decode bytes to string
            #print(body)
            username = body.get("email")
            email = body.get("email")
            mobile = body.get("mobile")
            name = body.get("username")
            first_name = body.get("username")
            last_name = ""

            # Ensure password matches confirmation
            password = body.get("password")
            confirmation = body.get("confirmation")
            
            if password != confirmation:
                return JsonResponse({"message":"Error: Passwords do not match"}, status=400)
            try:
                user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name, mobile = mobile, email_notif = email, mobile_notif = mobile)
                user.save()
                referral = Referral.create(user=user, redirect_to='/signup', label=request.POST.get("label", ""), target=None) 
                #user.referral_code = referral.code 
                #user.save()
                return JsonResponse({"message":"Registered Successfully"}, status=200)
            except IntegrityError:
                return JsonResponse({"message":"Error: Email already registered"}, status=400)
            # Proxy configuration with login and password

            action = Referral.record_response(request, "USER_SIGNUP")
            if action is not None:
                referral = Referral.objects.get(id=action.referral.id)
                user.referral_code = Referral.objects.get(id=action.referral.code)
                user.referred_by = User.objects.get(id=referral.user.id)
                user.save()
                # Attempt to create new user
                #login(request, user)
            return JsonResponse({"message":"Registered Successfully"}, status=200)
        except:
            return JsonResponse({"message":"Failed"}, status=400)


class AccountActivationView(LoginRequired, TemplateView):
    template_name = "plans/account_activation.html"

    def get_context_data(self, **kwargs):
        if (
            self.request.user.userplan.active is True
            or self.request.user.userplan.is_expired()
        ):
            raise Http404()

        context = super(AccountActivationView, self).get_context_data(**kwargs)
        errors = self.request.user.userplan.clean_activation()

        if errors["required_to_activate"]:
            context["SUCCESSFUL"] = False
        else:
            context["SUCCESSFUL"] = True
            messages.success(self.request, _("Your account is now active"))

        for error in errors["required_to_activate"]:
            messages.error(self.request, error)
        for error in errors["other"]:
            messages.warning(self.request, error)

        return context


class PlanTableMixin(object):
    def get_plan_table(self, plan_list):
        """
        This method return a list in following order:
        [
            ( Quota1, [ Plan1Quota1, Plan2Quota1, ... , PlanNQuota1] ),
            ( Quota2, [ Plan1Quota2, Plan2Quota2, ... , PlanNQuota2] ),
            ...
            ( QuotaM, [ Plan1QuotaM, Plan2QuotaM, ... , PlanNQuotaM] ),
        ]

        This can be very easily printed as an HTML table element with quotas by row.

        Quotas are calculated based on ``plan_list``. These are all available quotas that are
        used by given plans. If any ``Plan`` does not have any of ``PlanQuota`` then value ``None``
        will be propagated to the data structure.

        """

        # Retrieve all quotas that are used by any ``Plan`` in ``plan_list``
        quota_list = (
            Quota.objects.all().filter(planquota__plan__in=plan_list).distinct()
        )

        # Create random access dict that for every ``Plan`` map ``Quota`` -> ``PlanQuota``
        plan_quotas_dic = {}
        for plan in plan_list:
            plan_quotas_dic[plan] = {}
            for plan_quota in plan.planquota_set.all():
                plan_quotas_dic[plan][plan_quota.quota] = plan_quota

        # Generate data structure described in method docstring, propagate ``None`` whenever
        # ``PlanQuota`` is not available for given ``Plan`` and ``Quota``
        return map(
            lambda quota: (
                quota,
                map(lambda plan: plan_quotas_dic[plan].get(quota, None), plan_list),
            ),
            quota_list,
        )


class PlanTableViewBase(PlanTableMixin, ListView):
    model = Plan
    context_object_name = "plan_list"

    def get_queryset(self):
        queryset = (
            super(PlanTableViewBase, self)
            .get_queryset()
            .prefetch_related("planpricing_set__pricing", "planquota_set__quota")
        )
        if self.request.user.is_authenticated:
            queryset = queryset.filter(
                Q(available=True, visible=True)
                & (Q(customized=self.request.user) | Q(customized__isnull=True))
            )
        else:
            queryset = queryset.filter(
                Q(available=True, visible=True) & Q(customized__isnull=True)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PlanTableViewBase, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            try:
                self.userplan = UserPlan.objects.select_related("plan").get(
                    user=self.request.user
                )
            except UserPlan.DoesNotExist:
                self.userplan = None

            context["userplan"] = self.userplan

            try:
                context["current_userplan_index"] = list(self.object_list).index(
                    self.userplan.plan
                )
            except (ValueError, AttributeError):
                pass

        context["plan_table"] = self.get_plan_table(self.object_list)
        context["CURRENCY"] = settings.PLANS_CURRENCY

        return context


class CurrentPlanView(LoginRequired, PlanTableViewBase):
    template_name = "plans/current.html"

    def get_queryset(self):
        return Plan.objects.filter(userplan__user=self.request.user).prefetch_related(
            "planpricing_set__pricing", "planquota_set__quota"
        )


class UpgradePlanView(LoginRequired, PlanTableViewBase):
    template_name = "plans/upgrade.html"


class PricingView(PlanTableViewBase):
    template_name = "plans/pricing.html"


class ChangePlanView(LoginRequired, View):
    """
    A view for instant changing user plan when it does not require additional payment.
    Plan can be changed without payment when:
    * user can enable this plan (it is available & visible and if it is customized it is for him,
    * plan is different from the current one that user have,
    * within current change plan policy this does not require any additional payment (None)

    It always redirects to ``upgrade_plan`` url as this is a potential only one place from
    where change plan could be invoked.
    """

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse("upgrade_plan"))

    def post(self, request, *args, **kwargs):
        plan = get_object_or_404(
            Plan,
            Q(pk=kwargs["pk"])
            & Q(available=True, visible=True)
            & (Q(customized=request.user) | Q(customized__isnull=True)),
        )
        if request.user.userplan.plan != plan:
            policy = import_name(
                getattr(
                    settings,
                    "PLANS_CHANGE_POLICY",
                    "plans.plan_change.StandardPlanChangePolicy",
                )
            )()

            period = request.user.userplan.days_left()
            price = policy.get_change_price(request.user.userplan.plan, plan, period)

            if price is None:
                request.user.userplan.extend_account(plan, None)
                messages.success(request, _("Your plan has been successfully changed"))
            else:
                return HttpResponseForbidden()
        return HttpResponseRedirect(reverse("upgrade_plan"))


class CreateOrderView(LoginRequired, CreateView):
    template_name = "plans/create_order.html"
    form_class = CreateOrderForm

    def recalculate(self, amount, billing_info):
        """
        Calculates and return pre-filled Order
        """
        order = Order(pk=-1)
        order.recalculate(amount, billing_info, self.request)
        return order

    def validate_plan(self, plan):
        validation_errors = plan_validation(self.request.user, plan)
        if validation_errors["required_to_activate"] or validation_errors["other"]:
            messages.error(
                self.request,
                _(
                    "The selected plan is insufficient for your account. "
                    "Your account will not be activated or will not work fully after completing this order."
                    "<br><br>Following limits will be exceeded: <ul><li>%(reasons)s</ul>"
                )
                % {
                    "reasons": "<li>".join(
                        chain(
                            validation_errors["required_to_activate"],
                            validation_errors["other"],
                        )
                    ),
                },
            )

    def get_all_context(self):
        """
        Retrieves Plan and Pricing for current order creation
        """
        self.plan_pricing = get_object_or_404(
            PlanPricing.objects.all().select_related("plan", "pricing"),
            Q(pk=self.kwargs["pk"])
            & Q(plan__available=True)
            & (
                Q(plan__customized=self.request.user) | Q(plan__customized__isnull=True)
            ),
        )

        # User is not allowed to create new order for Plan when he has different Plan
        # unless it's a free plan. Otherwise, the should use Plan Change View for this
        # kind of action
        if (
            not self.request.user.userplan.is_expired()
            and not self.request.user.userplan.plan.is_free()
            and self.request.user.userplan.plan != self.plan_pricing.plan
        ):
            raise Http404

        self.plan = self.plan_pricing.plan
        self.pricing = self.plan_pricing.pricing

    def get_billing_info(self):
        try:
            return self.request.user.billinginfo
        except BillingInfo.DoesNotExist:
            return None

    def get_price(self):
        return self.plan_pricing.price

    def get_context_data(self, **kwargs):
        context = super(CreateOrderView, self).get_context_data(**kwargs)
        self.get_all_context()
        context["billing_info"] = self.get_billing_info()

        order = self.recalculate(
            self.get_price() or Decimal("0.0"), context["billing_info"]
        )
        order.plan = self.plan_pricing.plan
        order.pricing = self.plan_pricing.pricing
        order.currency = get_currency()
        order.user = self.request.user
        context["object"] = order

        self.validate_plan(order.plan)
        return context

    def form_valid(self, form):
        self.get_all_context()
        order = self.recalculate(
            self.get_price() or Decimal("0.0"), self.get_billing_info()
        )

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.plan = self.plan
        self.object.pricing = self.pricing
        self.object.amount = order.amount
        self.object.tax = order.tax
        self.object.currency = order.currency
        self.object.save()
        order_started.send(sender=self.object)
        return super(ModelFormMixin, self).form_valid(form)


class CreateOrderPlanChangeView(CreateOrderView):
    template_name = "plans/create_order.html"
    form_class = CreateOrderForm

    def get_all_context(self):
        self.plan = get_object_or_404(
            Plan,
            Q(pk=self.kwargs["pk"])
            & Q(available=True, visible=True)
            & (Q(customized=self.request.user) | Q(customized__isnull=True)),
        )
        self.pricing = None

    def get_price(self):
        return get_change_price(self.request.user.userplan, self.plan)

    def get_context_data(self, **kwargs):
        context = super(CreateOrderView, self).get_context_data(**kwargs)
        self.get_all_context()

        price = self.get_price()
        context["plan"] = self.plan
        context["billing_info"] = self.get_billing_info()
        if price is None:
            context["FREE_ORDER"] = True
            price = 0
        order = self.recalculate(price, context["billing_info"])
        order.pricing = None
        order.plan = self.plan
        order.user = self.request.user
        context["billing_info"] = context["billing_info"]
        context["object"] = order
        self.validate_plan(order.plan)
        return context


class OrderView(LoginRequired, DetailView):
    model = Order

    def get_queryset(self):
        return (
            super(OrderView, self)
            .get_queryset()
            .filter(user=self.request.user)
            .select_related(
                "plan",
                "pricing",
            )
        )


class OrderListView(LoginRequired, ListView):
    model = Order
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        self.CURRENCY = getattr(settings, "PLANS_CURRENCY", None)
        if len(self.CURRENCY) != 3:
            raise ImproperlyConfigured(
                "PLANS_CURRENCY should be configured as 3-letter currency code."
            )
        context["CURRENCY"] = self.CURRENCY
        return context

    def get_queryset(self):
        return (
            super(OrderListView, self)
            .get_queryset()
            .filter(user=self.request.user)
            .select_related(
                "plan",
                "pricing",
            )
        )


class OrderPaymentReturnView(LoginRequired, DetailView):
    """
    This view is a fallback from any payments processor. It allows just to set additional message
    context and redirect to Order view itself.
    """

    model = Order
    status = None

    def render_to_response(self, context, **response_kwargs):
        if self.status == "success":
            messages.success(
                self.request,
                _(
                    "Thank you for placing a payment. It will be processed as soon as possible."
                ),
            )
        elif self.status == "failure":
            messages.error(
                self.request,
                _(
                    "Payment was not completed correctly. Please repeat payment process."
                ),
            )

        return HttpResponseRedirect(self.object.get_absolute_url())

    def get_queryset(self):
        return (
            super(OrderPaymentReturnView, self)
            .get_queryset()
            .filter(user=self.request.user)
        )


class SuccessUrlMixin:
    def get_success_url(self):
        messages.success(self.request, _("Billing info has been updated successfuly."))
        return reverse("billing_info")


class CreateOrUpdateView(
    SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView
):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class BillingInfoCreateOrUpdateView(
    NextUrlMixin, SuccessUrlMixin, LoginRequired, CreateOrUpdateView
):
    form_class = BillingInfoForm
    template_name = "plans/billing_info_create_or_update.html"

    def get_object(self):
        try:
            return self.request.user.billinginfo
        except (AttributeError, BillingInfo.DoesNotExist):
            return None

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(request=self.request)
        return kwargs


class RedirectToBilling(RedirectView):
    url = reverse_lazy("billing_info")
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        warnings.warn(
            "This view URL is deprecated. Use plain billing_info instead.",
            DeprecationWarning,
        )
        return super().get_redirect_url(*args, **kwargs)


class BillingInfoDeleteView(LoginRequired, DeleteView):
    """
    Deletes billing data for user
    """

    template_name = "plans/billing_info_delete.html"

    def get_object(self):
        try:
            return self.request.user.billinginfo
        except BillingInfo.DoesNotExist:
            raise Http404

    def get_success_url(self):
        messages.success(self.request, _("Billing info has been deleted."))
        return reverse("billing_info")


class InvoiceDetailView(LoginRequired, DetailView):
    model = Invoice

    def get_template_names(self):
        return getattr(settings, "PLANS_INVOICE_TEMPLATE", "plans/invoices/PL_EN.html")

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        context["logo_url"] = getattr(settings, "PLANS_INVOICE_LOGO_URL", None)
        context["auto_print"] = True
        return context

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super(InvoiceDetailView, self).get_queryset().select_related("order")
        else:
            return (
                super(InvoiceDetailView, self)
                .get_queryset()
                .filter(user=self.request.user)
                .select_related("order")
            )


class FakePaymentsView(LoginRequired, SingleObjectMixin, FormView):
    form_class = FakePaymentsForm
    model = Order
    template_name = "plans/fake_payments.html"

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_queryset(self):
        return (
            super(FakePaymentsView, self).get_queryset().filter(user=self.request.user)
        )

    def dispatch(self, *args, **kwargs):
        if not getattr(settings, "DEBUG", False):
            return HttpResponseForbidden("This view is accessible only in debug mode.")
        self.object = self.get_object()
        return super(FakePaymentsView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if int(form["status"].value()) == Order.STATUS.COMPLETED:
            self.object.complete_order()
            return HttpResponseRedirect(
                reverse("order_payment_success", kwargs={"pk": self.object.pk})
            )
        else:
            self.object.status = form["status"].value()
            self.object.save()
            return HttpResponseRedirect(
                reverse("order_payment_failure", kwargs={"pk": self.object.pk})
            )


class QuotaValidator(object):
    """
    Base class for all Quota validators needed for account activation
    """

    required_to_activate = True
    default_quota_value = None

    @property
    def code(self):
        raise ImproperlyConfigured('Quota code name is not provided for validator')

    """
    def get_quota_value(self, user, quota_dict=None):
        
        Returns quota value for a given user
        
        if quota_dict is None:
            quota_dict = get_user_quota(user)

        return quota_dict.get(self.code, self.default_quota_value)
    """

    def get_error_message(self, quota_value, **kwargs):
        return u'Plan validation error'


    def __call__(self, user, quota_dict=None, **kwargs):
        """
        Performs validation of quota limit for a user account
        """
        #print("Hi");
        raise NotImplementedError('Please implement specific QuotaValidator')

    def on_activation(self, user, quota_dict=None, **kwargs):
        """
        Hook for any action that validator needs to do while successful activation of the plan
        Most useful for validators not required to activate, e.g. some "option" is turned ON for user
        but when user downgrade plan this option should be turned OFF automatically rather than
        stops account activation
        """
        pass

class ModelCountValidator(QuotaValidator):
    """
    Validator that checks if there is no more than quota number of objects given model
    """

    @property
    def model(self):
        raise ImproperlyConfigured('ModelCountValidator requires model name')

    def get_queryset(self, user):
        return self.model.objects.all()


    def get_error_message(self, quota_value, **kwargs):
        return _('Limit of %(model_name_plural)s exceeded. The limit is %(quota)s items.') % {
            'model_name_plural': self.model._meta.verbose_name_plural.title().lower(),
            'quota': quota_value,
        }


    def __call__(self, user, quota_dict=None, **kwargs):
        quota = self.get_quota_value(user, quota_dict)
        total_count = self.get_queryset(user).count() + kwargs.get('add', 0)
        if not quota is None and total_count > quota:
            raise ValidationError(self.get_error_message(quota))



class ModelAttributeValidator(ModelCountValidator):
    """
    Validator checks if every obj.attribute value for a given model satisfy condition
    provided in check_attribute_value() method.

    .. warning::
        ModelAttributeValidator requires `get_absolute_url()` method on provided model.
    """

    @property
    def attribute(self):
        raise ImproperlyConfigured('ModelAttributeValidator requires defining attribute name')

    def check_attribute_value(self, attribute_value, quota_value):
        # default is to value is <= limit
        return attribute_value <= quota_value


    def get_error_message(self, quota_value, **kwargs):
        return _('Following %(model_name_plural)s are not in limits: %(objects)s') % {
            'model_name_plural': self.model._meta.verbose_name_plural.title().lower(),
            'objects': u', '.join(map(lambda o: u'<a href="%s">%s</a>' % (o.get_absolute_url(), six.u(o)),
                                      kwargs['not_valid_objects'])),
        }


    def __call__(self, user, quota_dict=None, **kwargs):
        quota_value = self.get_quota_value(user, quota_dict)
        not_valid_objects = []
        if not quota_value is None:
            for obj in self.get_queryset(user):
                if not self.check_attribute_value(getattr(obj, self.attribute), quota_value):
                    not_valid_objects.append(obj)
        if not_valid_objects:
            raise ValidationError(
                self.get_error_message(quota_value, not_valid_objects=not_valid_objects)
            )
 


def plan_validation(user, plan=None, on_activation=False):
    """
    Validates validator that represents quotas in a given system
    :param user:
    :param plan:
    :return:
    """
    if plan is None:
        # if plan is not given, the default is to use current plan of the user
        plan = user.userplan.plan
    quota_dict = plan.get_quota_dict()
    validators = getattr(settings, 'PLANS_VALIDATORS', {})
    errors = {
        'required_to_activate': [],
        'other': [],
    }

    for quota in validators:
        validator = import_name(validators[quota])

        if on_activation:
            validator.on_activation(user, quota_dict)
        else:
            try:
                validator(user, quota_dict)
            except ValidationError as e:
                if validator.required_to_activate:
                    errors['required_to_activate'].extend(e.messages)
                else:
                    errors['other'].extend(e.messages)
    return errors


class WhatsAppValidator(QuotaValidator):
    code = 'whatsappnotif'
    verbose_name = "WhatsApp Notifications"
    default_limit = 1  # Adjust as needed

    def validate(self, user):
        try:
            user_plan = UserPlan.objects.get(user=user)
            # Check if the plan has a quota with the given codename and a boolean value set to True
            has_whatsapp_quota = Quota.objects.filter(plan=user_plan.plan, codename=self.code).exists()
            return has_whatsapp_quota
        except UserPlan.DoesNotExist:
            return False

class EmailValidator(QuotaValidator):
    code = 'emailnotif'
    verbose_name = "Email Notifications"
    default_limit = 1  # Adjust as needed

    def validate(self, user):
        try:
            user_plan = UserPlan.objects.get(user=user)
            # Check if the plan has a quota with the given codename and a boolean value set to True
            has_email_quota = Quota.objects.filter(plan=user_plan.plan, codename=self.code).exists()
            return has_email_quota
        except UserPlan.DoesNotExist:
            return False