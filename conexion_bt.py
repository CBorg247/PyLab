from flask import Flask, render_template, request, jsonify
from bleak import BleakScanner, BleakClient
import asyncio

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Bluet.html')

@app.route('/scan', methods=['GET'])
def scan_devices():
    async def scan():
        try:
            devices = await BleakScanner.discover(timeout=5.0)
            return [{"name": d.name or "Desconocido", "address": d.address} for d in devices]
        except Exception as e:
            print("[ERROR SCAN]", str(e))
            return []
        

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(scan())
    return jsonify(result)

@app.route('/connect', methods=['POST'])
def connect_device():
    data = request.get_json()
    address = data.get("address")

    async def connect():
        client = BleakClient(address)
        try:
            await client.connect()
            connected = client.is_connected
            await client.disconnect()
            return {"connected": connected}
        except Exception as e:
            return {"connected": False, "error": str(e)}

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(connect())
    print(f"[DEBUG] Resultado conexión: {result}")
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)