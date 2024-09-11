from flask import Blueprint, request, jsonify
import stripe
from app.models import db, User
from flask_login import login_required, current_user
import os

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

stripe_routes = Blueprint('stripe', __name__)

@stripe_routes.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    data = request.get_json()
    price_id = data.get('price_id')

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=request.host_url + 'success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.host_url + 'cancel',
            customer_email=current_user.email
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403

@stripe_routes.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET')

    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        return jsonify({'error': 'Invalid signature'}), 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session(session)
    elif event['type'] == 'invoice.payment_succeeded':
        invoice = event['data']['object']
        handle_payment_succeeded(invoice)
    elif event['type'] == 'invoice.payment_failed':
        invoice = event['data']['object']
        handle_payment_failed(invoice)
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        handle_subscription_deleted(subscription)
    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        handle_subscription_updated(subscription)

    return jsonify({'status': 'success'}), 200

def handle_checkout_session(session):
    user = User.query.filter_by(email=session['customer_email']).first()
    if user:
        subscription = stripe.Subscription.retrieve(session['subscription'])
        price_id = subscription['items']['data'][0]['price']['id']
        user.stripe_customer_id = session['customer']
        user.stripe_subscription_id = subscription['id']
        if price_id == 'price_1PLVpIBIxhjYY7P2UNEsuWfr':  # Replace with your actual monthly price ID
            user.status = 'Premium Monthly'
        elif price_id == 'price_1PLVpbBIxhjYY7P2e7zv0EU2':  # Replace with your actual annual price ID
            user.status = 'Premium Annual'
        db.session.commit()

def handle_payment_succeeded(invoice):
    # You can implement any additional logic if needed for successful payments
    pass

def handle_payment_failed(invoice):
    customer_id = invoice['customer']
    user = User.query.filter_by(stripe_customer_id=customer_id).first()
    if user:
        user.status = 'Basic'
        db.session.commit()

def handle_subscription_deleted(subscription):
    customer_id = subscription['customer']
    user = User.query.filter_by(stripe_customer_id=customer_id).first()
    if user:
        user.status = 'Accepted'
        user.stripe_subscription_id = None
        db.session.commit()

def handle_subscription_updated(subscription):
    if subscription['status'] == 'canceled':
        handle_subscription_deleted(subscription)
    else:
        customer_id = subscription['customer']
        user = User.query.filter_by(stripe_customer_id=customer_id).first()
        if user:
            price_id = subscription['items']['data'][0]['price']['id']
            user.stripe_subscription_id = subscription['id']
            if price_id == 'price_1PLVpIBIxhjYY7P2UNEsuWfr':  # Replace with your actual monthly price ID
                user.status = 'Premium Monthly'
            elif price_id == 'price_1PLVpbBIxhjYY7P2e7zv0EU2':  # Replace with your actual annual price ID
                user.status = 'Premium Annual'
            db.session.commit()

@stripe_routes.route('/create-portal-session', methods=['POST'])
@login_required
def create_portal_session():
    data = request.get_json()
    customer_id = data.get('customer_id')

    try:
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=request.host_url + 'manage-subscription-return'
        )
        return jsonify({'url': session.url})
    except Exception as e:
        return jsonify(error=str(e)), 403
