import mysql.connector
import paho.mqtt.client as mqtt
from datetime import datetime

# Callback saat terhubung ke broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("scoring")

# Callback saat pesan diterima
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode()))

    # Koneksi ke database MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="lombok",
        port=8889
    )
    cursor = conn.cursor()

    # Tentukan nilai ref_penilaian_tandings_id berdasarkan data yang diterima
    ref_penilaian_tandings_id = 1 if msg.payload.decode() == "TANGAN" else 3

    # Waktu sekarang untuk created_at dan updated_at
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Query SQL untuk memasukkan data
    sql = """
    INSERT INTO sensor_juri (arena_code, corner, censor_code, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (ref_penilaian_tandings_id, 'blue',1 ,now, now)

    # Eksekusi query dan commit perubahan
    cursor.execute(sql, values)
    conn.commit()

    # Tutup koneksi
    cursor.close()
    conn.close()

# Inisialisasi MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Hubungkan ke broker MQTT
client.connect("192.168.202.3", 1883, 60)

# Jalankan loop MQTT
client.loop_forever()
