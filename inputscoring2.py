import mysql.connector
import paho.mqtt.client as mqtt
import json
from datetime import datetime

# Callback saat terhubung ke broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("scoring")

# Callback saat pesan diterima
def on_message(client, userdata, msg):
    print(f"Message received: {msg.payload.decode()}")

    try:
        # Parsing JSON dari payload
        payload = json.loads(msg.payload.decode())

        # Ambil data dari JSON
        arena_code = payload.get("arena")
        corner = payload.get("corner")
        censor_code = payload.get("fsr")

        # Periksa apakah data lengkap
        if arena_code is None or corner is None or censor_code is None:
            print("Incomplete data, skipping insert.")
            return

        # Waktu sekarang untuk kolom created_at dan updated_at
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Koneksi ke database MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="lombok",
            port=8889
        )
        cursor = conn.cursor()

        # Query SQL untuk memasukkan data
        sql = """
        INSERT INTO sensor_juris (arena_code, corner, censor_code, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (arena_code, corner, censor_code, now, now)

        # Eksekusi query dan commit perubahan
        cursor.execute(sql, values)
        conn.commit()

        print("Data inserted successfully!")

        # Tutup koneksi
        cursor.close()
        conn.close()

    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")

# Inisialisasi MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Hubungkan ke broker MQTT
client.connect("localhost", 1883, 60)

# Jalankan loop MQTT
client.loop_forever()
