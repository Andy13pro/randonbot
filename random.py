from telethon import TelegramClient, events
import random
from PIL import Image, ImageDraw, ImageFont
import requests
import io
import asyncio

# Configuración del cliente
api_id = '24128308'
api_hash = 'e1d006e1aede7e1159b55148232780d7'
bot_token = '7665971523:AAEXoSlHWnzST6aCcMpdvSQlJHz4Z6Em7hU'
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Listas de frases y comandos divertidos
frases_random = [
    "¿Sabías que las tortugas pueden respirar por su trasero?",
    "Si te ríes ahora, es porque estás pensando en cosas tontas.",
    "[@username], te declaramos el más cool del grupo por 5 minutos.",
    "Hoy es un buen día para comer pizza, ¿no crees?",
    "[@username], recuerda que eres especial, como un WiFi sin contraseña.",
    "Si los unicornios existieran, seguramente serían programadores.",
    "[@username], ¿sabías que los koalas duermen 22 horas al día? ¡Como tú en cuarentena!",
    "Hoy es un buen día para cometer errores, aprender y luego culpar al bot. 😏",
    "[@username], si no te han llamado genio hoy, aquí estoy para hacerlo. ¡Eres genial!",
    "La vida es demasiado corta para tener chats aburridos, así que aquí estoy. 🤖"
]

preguntas_trivia = [
    {
        "pregunta": "¿Cuántos corazones tiene un pulpo?",
        "opciones": ["1", "2", "3", "4"],
        "respuesta": "3"
    },
    {
        "pregunta": "¿Cuál es el país más grande del mundo?",
        "opciones": ["Rusia", "Canadá", "China", "EE.UU."],
        "respuesta": "Rusia"
    },
    {
        "pregunta": "¿En qué año llegó el hombre a la Luna?",
        "opciones": ["1965", "1969", "1971", "1975"],
        "respuesta": "1969"
    },
    {
        "pregunta": "¿Cuál es el océano más grande del mundo?",
        "opciones": ["Atlántico", "Pacífico", "Índico", "Ártico"],
        "respuesta": "Pacífico"
    },
    {
        "pregunta": "¿Qué animal es conocido por cambiar de color?",
        "opciones": ["Camaleón", "Pulpo", "Pez Payaso", "Serpiente"],
        "respuesta": "Camaleón"
    }
]

stickers_random = [
    "CAADBAADGgADX2HhGQABkpzFP1HWPwI",  # Ejemplo de ID de sticker
    "CAADBAADHgADX2HhGQABlUzP-Ssd9AI",
    "CAADBAADIgADX2HhGQABJgHHm9JwfgI",
    "CAADBAADJgADX2HhGQABt5Z6YZkJpAI",
    "CAADBAADKgADX2HhGQAB6SRzLtG6RgI"
]

# Función para obtener un chiste de una API
async def obtener_chiste():
    try:
        response = requests.get("https://v2.jokeapi.dev/joke/Any?type=single")
        if response.status_code == 200:
            data = response.json()
            return data.get("joke", "No encontré chistes esta vez. 😢")
    except Exception as e:
        return "Parece que mi humor está roto. 😅"

# Comando de chistes
@client.on(events.NewMessage(pattern='/chiste'))
async def enviar_chiste(event):
    chiste = await obtener_chiste()
    await event.reply(chiste)

# Comando para saber "qué tan gey" o "qué tan hetero" eres
@client.on(events.NewMessage(pattern='/gey'))
async def geyometer(event):
    porcentaje = random.randint(0, 100)
    await event.reply(f"Eres un {porcentaje}% gey 🌈")

@client.on(events.NewMessage(pattern='/hetero'))
async def heterometer(event):
    porcentaje = random.randint(0, 100)
    await event.reply(f"Eres un {porcentaje}% hetero 💼")

# Comando para editar una imagen
@client.on(events.NewMessage(pattern='/dibujame'))
async def editar_imagen(event):
    if event.file:
        img_data = await event.download_media()
        with Image.open(io.BytesIO(img_data)) as img:
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("arial.ttf", size=40)
            draw.text((10, 10), "¡Random art! 🎨", fill="red", font=font)
            img_byte_array = io.BytesIO()
            img.save(img_byte_array, format='PNG')
            img_byte_array.seek(0)
        await client.send_file(event.chat_id, img_byte_array, caption="¡Aquí está tu arte random!")
    else:
        await event.reply("Por favor, envíame una imagen junto con el comando.")

# Mensaje random con menciones
@client.on(events.NewMessage(pattern='/randomuser'))
async def mencionar_usuario(event):
    participantes = await client.get_participants(event.chat_id)
    if participantes:
        usuario_random = random.choice(participantes)
        frase = random.choice(frases_random).replace("[@username]", f"@{usuario_random.username}")
        await event.reply(frase)

# Comando de trivia
@client.on(events.NewMessage(pattern='/trivia'))
async def trivia_game(event):
    trivia = random.choice(preguntas_trivia)
    opciones = "\n".join([f"{i+1}. {opcion}" for i, opcion in enumerate(trivia["opciones"])]);
    pregunta = f"{trivia['pregunta']}\n{opciones}"
    await event.reply(pregunta)

    @client.on(events.NewMessage(pattern='^[1-4]$'))
    async def check_respuesta(resp_event):
        if resp_event.sender_id == event.sender_id:
            respuesta_correcta = trivia['opciones'].index(trivia['respuesta']) + 1
            if int(resp_event.text) == respuesta_correcta:
                await resp_event.reply("¡Correcto! 🎉")
            else:
                await resp_event.reply(f"Incorrecto. La respuesta correcta era: {trivia['respuesta']}.")

# Ruleta de stickers
@client.on(events.NewMessage(pattern='/ruleta'))
async def ruleta_sticker(event):
    sticker = random.choice(stickers_random)
    await client.send_file(event.chat_id, sticker)

# Comando para lanzar un dado
@client.on(events.NewMessage(pattern='/dado'))
async def lanzar_dado(event):
    resultado = random.randint(1, 6)
    await event.reply(f"🎲 Has lanzado el dado y salió: {resultado}.")

# Comando de frases inspiradoras
@client.on(events.NewMessage(pattern='/frase'))
async def frase_inspiradora(event):
    frases_inspiradoras = [
        "La vida es 10% lo que nos pasa y 90% cómo reaccionamos a ello.",
        "El único lugar donde el éxito viene antes que el trabajo es en el diccionario.",
        "No esperes. Nunca habrá un momento perfecto.",
        "La mejor forma de predecir el futuro es creándolo."
    ]
    await event.reply(random.choice(frases_inspiradoras))

# Mensaje periódico con mención aleatoria
async def mensaje_aleatorio_periodico():
    while True:
        await asyncio.sleep(random.randint(1800, 3600))  # Entre 30 minutos y 1 hora
        async for dialog in client.iter_dialogs():
            if dialog.is_group:
                participantes = await client.get_participants(dialog)
                if participantes:
                    usuario_random = random.choice(participantes)
                    frase = random.choice(frases_random).replace("[@username]", f"@{usuario_random.username}")
                    await client.send_message(dialog.id, frase)

# Frase motivadora diaria
@client.on(events.NewMessage(pattern='/motivate'))
async def motivacion(event):
    frases_motivadoras = [
        "¡Hoy es el día perfecto para empezar algo increíble!",
        "Recuerda, lo único imposible es aquello que no intentas.",
        "Tu esfuerzo de hoy será tu éxito de mañana. 💪",
        "Nunca subestimes el poder de tus sueños. ¡Persíguelos!"
    ]
    await event.reply(random.choice(frases_motivadoras))

# Ejecutar cliente
with client:
    client.loop.create_task(mensaje_aleatorio_periodico())
    client.run_until_disconnected()
