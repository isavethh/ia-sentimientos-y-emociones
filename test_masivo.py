"""
🧪 ALIMENTACIÓN MASIVA DEL ANALIZADOR DE EMOCIONES
Múltiples escenarios y casos de prueba
"""

import requests
import time

API_URL = "http://localhost:5000/analyze"

# TEXTOS EXTENSOS Y VARIADOS
TEXTOS_MASIVOS = [
    # ============ ALEGRÍA Y FELICIDAD ============
    ("😊 Alegría por logro profesional", 
     "¡¡¡LO LOGRÉ!!! Después de 5 años de esfuerzo, finalmente me ascendieron a gerente. No puedo creer que todo mi trabajo duro haya valido la pena. Estoy SÚPER feliz, emocionado y agradecido. ¡Este es el mejor día de mi carrera!"),
    
    ("😊 Felicidad familiar",
     "Hoy nació mi primera hija y es el momento más hermoso de mi vida. Verla por primera vez me llenó de una alegría inmensa. Soy el padre más afortunado del mundo. Mi corazón está lleno de amor y felicidad."),
    
    ("😊 Celebración de cumpleaños",
     "¡Qué fiesta tan increíble! Todos mis amigos vinieron a celebrar mi cumpleaños. Hubo música, baile, risas y muchos abrazos. Me siento muy querido y bendecido por tener personas tan maravillosas en mi vida."),
    
    ("😊 Victoria deportiva",
     "¡¡¡GANAMOS EL CAMPEONATO!!! No puedo dejar de gritar de emoción. Todo el equipo jugó increíblemente bien. Somos los mejores, lo logramos juntos. ¡Qué orgullo tan grande! ¡CAMPEONES!"),

    # ============ TRISTEZA PROFUNDA ============
    ("😢 Pérdida de mascota",
     "Hoy tuve que despedirme de mi perrito que me acompañó 15 años. El vacío que siento es inmenso. Lloro cada vez que veo su plato de comida vacío. Era mi mejor amigo, mi compañero fiel. Lo extraño muchísimo."),
    
    ("😢 Ruptura amorosa",
     "Terminamos después de 7 años juntos. Me siento completamente destrozado y solo. No sé cómo seguir adelante sin ella. Las noches son eternas y el dolor no para. Mi corazón está hecho pedazos."),
    
    ("😢 Nostalgia del pasado",
     "Encontré las fotos de mi infancia y la melancolía me invadió. Extraño esos tiempos simples cuando todo era más fácil. La inocencia perdida, los amigos que ya no están, los abuelos que partieron. Qué tristeza."),
    
    ("😢 Fracaso importante",
     "Reprobé el examen más importante de mi carrera. Estudié durante meses y aún así fallé. Me siento un completo fracaso, incapaz e inútil. No sé si tengo la fuerza para intentarlo de nuevo."),

    # ============ ENOJO INTENSO ============
    ("😠 Injusticia laboral",
     "¡¡¡ME TIENEN HARTO!!! Trabajo el doble que todos y el ascenso se lo dieron al sobrino del jefe. ¡ES UNA MALDITA INJUSTICIA! Estoy FURIOSO. Años de esfuerzo para NADA. ¡Esto es INACEPTABLE!"),
    
    ("😠 Estafa económica",
     "¡¡¡MALDITOS LADRONES!!! Me estafaron con todos mis ahorros. ¡Son unos CRIMINALES desgraciados! La rabia que siento es indescriptible. Quiero que paguen por lo que hicieron. ¡ODIO a esa gente!"),
    
    ("😠 Traición de amigo",
     "¡NO PUEDO CREER QUE ME TRAICIONARAS ASÍ! Después de todo lo que hice por ti, me apuñalas por la espalda. Eres un hipócrita, un falso, un miserable. ¡NUNCA te lo voy a perdonar! Estoy INDIGNADO."),
    
    ("😠 Mal servicio",
     "¡INCOMPETENTES! Llevo HORAS esperando y nadie resuelve nada. Es la peor empresa del mundo. ¡Quiero hablar con el gerente AHORA! Esto es una falta de respeto total. ¡EXIJO una solución!"),

    # ============ MIEDO Y ANSIEDAD ============
    ("😨 Ansiedad por salud",
     "Los resultados del examen médico salen mañana y no puedo dormir. Tengo mucho miedo de que sea algo grave. Mi corazón late muy rápido y las manos me tiemblan. La incertidumbre me está matando."),
    
    ("😨 Pánico escénico",
     "Mañana tengo que hablar frente a 500 personas y estoy aterrorizado. Solo de pensarlo me paralizo del terror. ¿Y si me equivoco? ¿Y si se ríen de mí? Tengo pánico, estoy muy nervioso y asustado."),
    
    ("😨 Preocupación financiera",
     "No sé cómo voy a pagar las deudas este mes. La angustia me consume. Tengo miedo de perder mi casa, de no poder alimentar a mi familia. La ansiedad no me deja pensar con claridad."),
    
    ("😨 Fobia específica",
     "Vi una araña ENORME en mi cuarto y casi me desmayo del terror. Estoy temblando, mi corazón va a explotar. No puedo entrar ahí, tengo demasiado miedo. El pánico me paraliza completamente."),

    # ============ AMOR Y ROMANCE ============
    ("❤️ Declaración de amor",
     "Te amo con toda mi alma. Eres la razón por la que sonrío cada día. Mi corazón te pertenece completamente. Quiero pasar cada momento de mi vida a tu lado. Eres mi todo, mi amor eterno."),
    
    ("❤️ Amor de pareja estable",
     "Llevamos 20 años casados y cada día te amo más. Eres mi mejor amigo, mi confidente, mi compañero de vida. Gracias por amarme, por cuidarme, por estar siempre. Te adoro infinitamente."),
    
    ("❤️ Amor maternal",
     "Ver a mis hijos crecer es el mayor regalo. Los amo con locura, son mi razón de ser. Cada abrazo suyo llena mi corazón de ternura. Haría cualquier cosa por su felicidad. Son mi vida entera."),
    
    ("❤️ Primer amor",
     "Creo que me estoy enamorando. Cada vez que la veo mi corazón late más rápido. Pienso en ella todo el día. Sus ojos, su sonrisa, su voz... me tiene cautivado. Nunca había sentido algo así."),

    # ============ SORPRESA ============
    ("😲 Sorpresa positiva",
     "¡¡¡NO ME LO ESPERABA!!! ¿En serio me regalaron un viaje a París? ¡GUAU! Estoy en shock total. ¡Esto es increíble, impresionante, alucinante! ¡No puedo creerlo! ¡¡¡WOW!!!"),
    
    ("😲 Noticia inesperada",
     "¡¿QUÉ?! ¿Mi hermano se va a casar la próxima semana? ¡Pero si ni sabía que tenía novia! Estoy completamente atónito y desconcertado. ¡Esto es totalmente inesperado! ¡No lo puedo creer!"),
    
    ("😲 Encuentro sorpresivo",
     "¡INCREÍBLE! Me encontré con mi amigo de la infancia después de 25 años. ¡No lo podía creer cuando lo vi! ¡Qué impacto! El mundo es un pañuelo. Estoy asombrado de esta coincidencia."),

    # ============ EMOCIONES MIXTAS ============
    ("🎭 Graduación agridulce",
     "Por fin me gradué y estoy muy feliz y orgulloso de mi logro. Pero también siento tristeza porque mis amigos de la universidad tomarán caminos diferentes. Alegría y nostalgia mezcladas."),
    
    ("🎭 Mudanza a otra ciudad",
     "Conseguí el trabajo de mis sueños pero tengo que mudarme lejos de mi familia. Estoy emocionado por la oportunidad pero triste por dejar todo atrás. Es confuso sentir alegría y dolor al mismo tiempo."),
    
    ("🎭 Nuevo bebé en tiempos difíciles",
     "Mi bebé nació en medio de problemas económicos. El amor que siento es inmenso, pero también hay preocupación y miedo por el futuro. Felicidad y ansiedad conviviendo en mi corazón."),

    # ============ MOTIVACIÓN Y DETERMINACIÓN ============
    ("💪 Superar adversidad",
     "¡¡¡NO ME VOY A RENDIR!!! Caí 100 veces pero me levantaré 101. Soy más fuerte que mis problemas. ¡VOY A TRIUNFAR! Nada ni nadie me va a detener. ¡A POR TODAS! ¡SÍ SE PUEDE!"),
    
    ("💪 Inicio de proyecto",
     "¡HOY COMIENZO MI EMPRESA! Años de preparación para este momento. Estoy listo, decidido, enfocado. El éxito me espera. ¡Voy a darlo TODO! ¡Este es MI momento! ¡ARRIBA!"),
    
    ("💪 Recuperación personal",
     "Después de tocar fondo, hoy empiezo de nuevo. Soy capaz, soy valiente, soy imparable. Cada día es una nueva oportunidad. ¡VAMOS! No hay obstáculo que no pueda superar."),

    # ============ GRATITUD ============
    ("🙏 Agradecimiento profundo",
     "Gracias, gracias, GRACIAS por todo lo que hiciste por mí. Tu apoyo me salvó la vida. Estoy eternamente agradecido. Eres un ángel. Que Dios te bendiga siempre. No tengo palabras suficientes."),
    
    ("🙏 Gratitud por la vida",
     "Hoy desperté agradecido por todo lo que tengo. Salud, familia, techo, comida. Soy muy afortunado. Doy gracias a la vida por cada bendición. Mi corazón está lleno de gratitud."),

    # ============ FRUSTRACIÓN ============
    ("😤 Frustración tecnológica",
     "¡¡¡Esta computadora de PORQUERÍA!!! Llevo horas intentando que funcione y NADA. ¡Me tiene HARTO! ¿Por qué todo es tan complicado? ¡AAAAAARGH! Estoy a punto de lanzarla por la ventana."),
    
    ("😤 Frustración de tráfico",
     "¡¡¡OTRA VEZ ATASCADOS!!! Llevamos UNA HORA sin movernos. ¡Es insoportable! Todos los días lo mismo. ¡Estoy DESESPERADO! ¿Por qué no hacen algo las autoridades? ¡BASTA YA!"),

    # ============ TEXTOS NEUTRALES ============
    ("😐 Día ordinario",
     "Me levanté a las siete, desayuné cereal con leche, fui al trabajo en autobús, almorcé un sandwich y regresé a casa. Un día normal, sin novedades particulares."),
    
    ("😐 Descripción factual",
     "La reunión comenzó a las tres de la tarde. Se discutieron los presupuestos del próximo trimestre. El gerente presentó los números y se asignaron las tareas correspondientes."),
    
    ("😐 Información técnica",
     "El sistema operativo requiere 4GB de RAM y 20GB de espacio en disco. La instalación toma aproximadamente 30 minutos. Se recomienda hacer una copia de seguridad previa."),

    # ============ CASOS ESPECIALES ============
    ("🔥 Texto con muchas exclamaciones",
     "¡¡¡ESTO ES INCREÍBLE!!! ¡¡¡NO PUEDO MÁS!!! ¡¡¡AAAAAAH!!! ¡¡¡SÍ!!! ¡¡¡LO LOGRAMOS!!! ¡¡¡VAMOS!!! ¡¡¡GENIAL!!! ¡¡¡WOW!!!"),
    
    ("📢 Texto EN MAYÚSCULAS",
     "ESTOY MUY EMOCIONADO PORQUE HOY ES UN DÍA ESPECIAL. TODO SALIÓ PERFECTO Y NO PUEDO ESTAR MÁS FELIZ. ES EL MEJOR MOMENTO DE MI VIDA."),
    
    ("🔄 Repetición emocional",
     "Triste triste triste. Me siento muy triste. Tristeza infinita. Solo tristeza. Nada más que tristeza. Tristeza total."),
    
    ("❓ Solo preguntas",
     "¿Por qué me siento así? ¿Qué me está pasando? ¿Cuándo terminará esto? ¿Hay esperanza? ¿Alguien me entiende? ¿Qué hago?"),

    # ============ REDES SOCIALES ============
    ("📱 Tweet feliz",
     "Mejores vacaciones de mi vidaaaa 🌴🌊 Sol, playa y buena compañía. Living my best life! Súper feliz ✨💕 #blessed #vacation #happy"),
    
    ("📱 Desahogo en redes",
     "Ya no puedo más con este mundo. Todo está mal. La gente es horrible. Nadie te ayuda. Estoy cansado de todo. 😔💔 Solo quiero paz."),
    
    ("📱 Emoción por concierto",
     "OMG OMG OMG!!! Conseguí boletos para ver a mi artista favorito!!! Voy a LLORAR de la emoción!!! No puedo esperar!!! 😭🎉🎶 AAAAH!!!"),
]

def analizar_texto(texto):
    try:
        response = requests.post(API_URL, json={"text": texto}, timeout=30)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def mostrar_resultado(categoria, resultado):
    print("\n" + "━"*70)
    print(f"📝 {categoria}")
    print("━"*70)
    
    if "error" in resultado:
        print(f"❌ Error: {resultado['error']}")
        return False
    
    # Sentimiento con barra visual
    sent = resultado.get('sentiment', {})
    stars = sent.get('stars', 0)
    stars_visual = '★' * stars + '☆' * (5-stars)
    print(f"\n🎯 SENTIMIENTO: {sent.get('label', 'N/A')} {stars_visual}")
    
    # Emociones con barras
    print(f"\n🎭 EMOCIONES:")
    for em in resultado.get('emotions', [])[:4]:
        score = em['score']
        bar = "█" * int(score / 5) + "░" * (20 - int(score / 5))
        print(f"   {em['emotion_es']:15} [{bar}] {em['percentage']}")
    
    # Intensidad con indicador visual
    intensity = resultado.get('intensity', {})
    level = intensity.get('level', 'Baja')
    score = intensity.get('score', 0)
    indicator = "🟢" if level == "Baja" else "🟡" if level == "Media" else "🔴"
    print(f"\n⚡ INTENSIDAD: {indicator} {level} ({score}%)")
    
    # Palabras clave
    keywords = resultado.get('keywords', [])[:5]
    if keywords:
        kw_str = " | ".join([f"{w[0]}" for w in keywords])
        print(f"\n🏷️  KEYWORDS: {kw_str}")
    
    # Emociones españolas encontradas
    spanish = resultado.get('spanish_emotions', {})
    if spanish:
        for emo, data in spanish.items():
            words = ", ".join(data['words_found'][:3])
            print(f"\n🇪🇸 {emo.upper()}: {words}")
    
    return True

def main():
    print("\n" + "🧠"*35)
    print("   ALIMENTACIÓN MASIVA DE LA IA")
    print("🧠"*35)
    
    print(f"\n📊 Preparando {len(TEXTOS_MASIVOS)} textos de prueba...")
    print("⏳ Verificando conexión...")
    
    # Esperar servidor
    intentos = 0
    while intentos < 15:
        try:
            r = requests.get("http://localhost:5000/health", timeout=2)
            if r.status_code == 200:
                break
        except:
            pass
        intentos += 1
        time.sleep(1)
    
    if intentos >= 15:
        print("❌ No se pudo conectar con el servidor")
        return
    
    print("✅ ¡Servidor conectado!")
    print(f"\n{'='*70}")
    print(f"🚀 INICIANDO ANÁLISIS MASIVO DE {len(TEXTOS_MASIVOS)} TEXTOS")
    print(f"{'='*70}")
    
    # Estadísticas
    exitosos = 0
    por_sentimiento = {'Positivo': 0, 'Negativo': 0, 'Neutral': 0}
    por_intensidad = {'Alta': 0, 'Media': 0, 'Baja': 0}
    emociones_detectadas = {}
    
    for i, (categoria, texto) in enumerate(TEXTOS_MASIVOS, 1):
        print(f"\n[{i}/{len(TEXTOS_MASIVOS)}]", end="")
        resultado = analizar_texto(texto)
        
        if mostrar_resultado(categoria, resultado):
            exitosos += 1
            
            # Recopilar estadísticas
            sent = resultado.get('sentiment', {}).get('label', 'Neutral')
            por_sentimiento[sent] = por_sentimiento.get(sent, 0) + 1
            
            intensity = resultado.get('intensity', {}).get('level', 'Baja')
            por_intensidad[intensity] = por_intensidad.get(intensity, 0) + 1
            
            for em in resultado.get('emotions', []):
                name = em.get('name', 'neutral')
                emociones_detectadas[name] = emociones_detectadas.get(name, 0) + 1
        
        time.sleep(0.3)
    
    # RESUMEN FINAL
    print("\n\n" + "="*70)
    print("📈 RESUMEN DE ALIMENTACIÓN MASIVA")
    print("="*70)
    print(f"\n✅ Análisis exitosos: {exitosos}/{len(TEXTOS_MASIVOS)}")
    
    print(f"\n📊 POR SENTIMIENTO:")
    for sent, count in por_sentimiento.items():
        bar = "█" * count + "░" * (len(TEXTOS_MASIVOS) - count)
        print(f"   {sent:10}: [{bar[:20]}] {count}")
    
    print(f"\n⚡ POR INTENSIDAD:")
    for level, count in por_intensidad.items():
        indicator = "🟢" if level == "Baja" else "🟡" if level == "Media" else "🔴"
        print(f"   {indicator} {level:6}: {count} textos")
    
    print(f"\n🎭 EMOCIONES MÁS FRECUENTES:")
    sorted_emotions = sorted(emociones_detectadas.items(), key=lambda x: x[1], reverse=True)
    for emo, count in sorted_emotions[:7]:
        print(f"   • {emo.capitalize()}: {count} veces")
    
    print("\n" + "="*70)
    print("🧠 ¡ALIMENTACIÓN COMPLETA!")
    print("="*70)

if __name__ == "__main__":
    main()
