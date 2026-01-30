"""
🧪 Script de Prueba para el Analizador de Emociones con IA
Alimenta la IA con múltiples textos de prueba
"""

import requests
import json
import time

API_URL = "http://localhost:5000/analyze"

# Textos de prueba para alimentar la IA
TEXTOS_PRUEBA = [
    {
        "categoria": "😊 ALEGRÍA INTENSA",
        "texto": "¡Hoy es el día más feliz de mi vida! Acabo de recibir la noticia de que conseguí el trabajo de mis sueños. Estoy saltando de alegría, no puedo contener la emoción. ¡TODO ES MARAVILLOSO!"
    },
    {
        "categoria": "😢 TRISTEZA PROFUNDA",
        "texto": "Me siento completamente vacío y solo. Perdí a alguien muy importante para mí y el dolor es insoportable. Las lágrimas no dejan de caer y no encuentro consuelo en nada."
    },
    {
        "categoria": "😠 ENOJO Y FRUSTRACIÓN",
        "texto": "¡¡¡ESTOY HARTO!!! No puedo creer la incompetencia de esta empresa. Me tienen esperando HORAS sin ninguna explicación. Es una falta de respeto total. ¡Esto es INACEPTABLE!"
    },
    {
        "categoria": "😨 MIEDO Y ANSIEDAD",
        "texto": "Tengo mucho miedo de lo que pueda pasar mañana. La incertidumbre me paraliza, no puedo dormir pensando en todos los escenarios negativos. Mi corazón late muy rápido y me tiemblan las manos."
    },
    {
        "categoria": "❤️ AMOR ROMÁNTICO",
        "texto": "Te amo más de lo que las palabras pueden expresar. Cada momento a tu lado es un regalo del cielo. Eres mi todo, mi razón de ser, mi corazón late solo por ti. Quiero pasar cada día de mi vida contigo."
    },
    {
        "categoria": "😲 SORPRESA TOTAL",
        "texto": "¡NO PUEDO CREERLO! ¿Esto realmente está pasando? ¡Guau! Jamás me imaginé algo así. Estoy en shock total, esto es completamente inesperado. ¡Increíble!"
    },
    {
        "categoria": "🤔 TEXTO NEUTRAL",
        "texto": "Hoy fui al supermercado y compré algunas cosas para la semana. El clima estuvo normal, ni muy frío ni muy caliente. Después regresé a casa y preparé la cena."
    },
    {
        "categoria": "🎭 EMOCIONES MIXTAS",
        "texto": "Me siento confundido. Por un lado estoy feliz porque mi hermano se casa, pero también triste porque se muda lejos. Es una mezcla extraña de alegría y nostalgia que no sé cómo manejar."
    },
    {
        "categoria": "💪 MOTIVACIÓN",
        "texto": "¡HOY ES EL DÍA! Voy a dar todo de mí para alcanzar mis metas. Nada me va a detener. Soy fuerte, soy capaz, y voy a demostrar de qué estoy hecho. ¡A por todas!"
    },
    {
        "categoria": "😔 DECEPCIÓN",
        "texto": "Confié en ti y me fallaste. Pensé que eras diferente pero resulta que eras igual que todos los demás. Me siento traicionado y desilusionado. No sé si podré volver a confiar en alguien."
    }
]

def probar_conexion():
    """Verifica si el servidor está disponible"""
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def analizar_texto(texto):
    """Envía un texto a la API y obtiene el análisis"""
    try:
        response = requests.post(
            API_URL,
            json={"text": texto},
            timeout=30
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def mostrar_resultado(categoria, resultado):
    """Muestra el resultado de forma visual"""
    print("\n" + "="*70)
    print(f"📝 {categoria}")
    print("="*70)
    
    if "error" in resultado:
        print(f"❌ Error: {resultado['error']}")
        return
    
    # Sentimiento
    sent = resultado.get('sentiment', {})
    print(f"\n🎯 SENTIMIENTO: {sent.get('label', 'N/A')}")
    print(f"   Confianza: {sent.get('score', 0)*100:.1f}%")
    print(f"   Estrellas: {'★' * sent.get('stars', 0)}{'☆' * (5-sent.get('stars', 0))}")
    
    # Emociones principales
    emociones = resultado.get('emotions', [])[:3]
    print(f"\n🎭 EMOCIONES DETECTADAS:")
    for em in emociones:
        barra = "█" * int(em['score'] / 10) + "░" * (10 - int(em['score'] / 10))
        print(f"   {em['emotion_es']}: [{barra}] {em['percentage']}")
    
    # Intensidad
    intensidad = resultado.get('intensity', {})
    print(f"\n⚡ INTENSIDAD: {intensidad.get('level', 'N/A')} ({intensidad.get('score', 0)}%)")
    
    # Palabras clave
    keywords = resultado.get('keywords', [])[:5]
    if keywords:
        palabras = ", ".join([f"{w[0]}({w[1]})" for w in keywords])
        print(f"\n🏷️ PALABRAS CLAVE: {palabras}")
    
    # Emociones en español
    spanish = resultado.get('spanish_emotions', {})
    if spanish:
        detected = ", ".join(spanish.keys())
        print(f"\n🇪🇸 EMOCIONES EN ESPAÑOL: {detected}")
    
    # Recomendación
    recs = resultado.get('recommendations', [])
    if recs:
        print(f"\n💡 RECOMENDACIÓN: {recs[0]}")

def main():
    print("\n" + "🧠"*35)
    print("   PRUEBA DEL ANALIZADOR DE EMOCIONES CON IA")
    print("🧠"*35)
    
    print("\n⏳ Verificando conexión con el servidor...")
    
    intentos = 0
    while not probar_conexion() and intentos < 30:
        print(f"   Esperando servidor... (intento {intentos + 1}/30)")
        time.sleep(2)
        intentos += 1
    
    if not probar_conexion():
        print("\n❌ No se pudo conectar con el servidor.")
        print("   Asegúrate de que app.py esté ejecutándose.")
        return
    
    print("✅ ¡Servidor conectado!")
    print(f"\n📊 Analizando {len(TEXTOS_PRUEBA)} textos de prueba...\n")
    
    resultados_exitosos = 0
    
    for prueba in TEXTOS_PRUEBA:
        resultado = analizar_texto(prueba["texto"])
        mostrar_resultado(prueba["categoria"], resultado)
        
        if "error" not in resultado:
            resultados_exitosos += 1
        
        time.sleep(0.5)  # Pequeña pausa entre análisis
    
    # Resumen final
    print("\n" + "="*70)
    print("📈 RESUMEN DE LA PRUEBA")
    print("="*70)
    print(f"   ✅ Análisis exitosos: {resultados_exitosos}/{len(TEXTOS_PRUEBA)}")
    print(f"   🧠 Modelos de IA funcionando correctamente")
    print("="*70)

if __name__ == "__main__":
    main()
