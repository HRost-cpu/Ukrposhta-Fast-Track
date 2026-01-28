import os
import asyncio
import httpx
from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__)

# API Укрпошти 2026
BASE_URL = "https://www.ukrposhta.ua/ecom/0.0.1"

async def call_api(method, endpoint, token, data=None, stream=False):
    """Універсальний асинхронний виклик API через HTTPX"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    # Використовуємо context manager для клієнта
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        url = f"{BASE_URL}/{endpoint}"
        if method == "POST":
            response = await client.post(url, json=data, headers=headers)
        else:
            response = await client.get(url, headers=headers)
        
        if stream:
            return response
        return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
async def generate_label():
    """Асинхронна обробка запиту (вимагає flask[async])"""
    try:
        user_data = request.json
        token = user_data.get('token')
        
        if not token:
            return jsonify({"error": "Bearer Token відсутній"}), 400

        # 1. Створення адрес паралельно
        sender_addr_task = call_api("POST", "addresses", token, {
            "postcode": user_data.get('sender_postcode', '01001'),
            "country": "UA",
            "city": user_data.get('sender_city', 'Київ'),
            "street": user_data.get('sender_street', 'Хрещатик'),
            "houseNumber": user_data.get('sender_house', '1')
        })
        
        recipient_addr_task = call_api("POST", "addresses", token, {
            "postcode": user_data.get('recipient_postcode', '79000'),
            "country": "UA",
            "city": user_data.get('recipient_city', 'Львів'),
            "street": user_data.get('recipient_street', 'Площа Ринок'),
            "houseNumber": user_data.get('recipient_house', '1')
        })

        sender_addr, recipient_addr = await asyncio.gather(sender_addr_task, recipient_addr_task)

        if 'id' not in sender_addr or 'id' not in recipient_addr:
            return jsonify({"error": "Помилка адрес", "details": sender_addr}), 400

        # 2. Створення клієнтів паралельно
        sender_client_task = call_api("POST", f"clients?token={token}", token, {
            "name": user_data.get('sender_name', 'Відправник'),
            "phoneNumber": "0500000000",
            "addressId": sender_addr['id']
        })

        recipient_client_task = call_api("POST", f"clients?token={token}", token, {
            "name": user_data.get('recipient_name', 'Отримувач'),
            "phoneNumber": "0990000000",
            "addressId": recipient_addr['id']
        })

        sender_client, recipient_client = await asyncio.gather(sender_client_task, recipient_client_task)

        if 'uuid' not in sender_client or 'uuid' not in recipient_client:
            return jsonify({"error": "Помилка реєстрації клієнтів"}), 400

        # 3. Створення відправлення
        shipment = await call_api("POST", f"shipments?token={token}", token, {
            "sender": { "uuid": sender_client['uuid'] },
            "recipient": { "uuid": recipient_client['uuid'] },
            "senderAddressId": sender_addr['id'],
            "deliveryType": "W2W",
            "parcels": [{"weight": 1000, "length": 30}]
        })

        if 'uuid' not in shipment:
            return jsonify({"error": "API Error", "details": shipment}), 400

        return jsonify({
            "status": "success",
            "barcode": shipment.get('barcode'),
            "uuid": shipment.get('uuid')
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_sticker/<uuid>/<token>')
async def get_sticker(uuid, token):
    try:
        response = await call_api("GET", f"shipments/{uuid}/sticker?token={token}", token, stream=True)
        if response.status_code == 200:
            return Response(response.content, mimetype='application/pdf')
        return f"Помилка завантаження: {response.status_code}", 400
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # Налаштування для локального запуску
    app.run(debug=False, host='0.0.0.0', port=5000)