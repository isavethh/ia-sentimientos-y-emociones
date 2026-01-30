"""
🧠 ANALIZADOR INTELIGENTE DE EMOCIONES Y SENTIMIENTOS
=====================================================
Versión optimizada que funciona sin descargas externas
Usa algoritmos de NLP puros para análisis de emociones
"""

from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
import re
from collections import Counter

app = Flask(__name__)

print("🚀 Iniciando Sistema de Análisis de Emociones...")

# ============================================================
# DICCIONARIOS DE EMOCIONES EN ESPAÑOL (Base de conocimiento)
# ============================================================

EMOTION_LEXICON = {
    'alegria': {
        'palabras': ['feliz', 'contento', 'alegre', 'genial', 'maravilloso', 'excelente', 
                    'increíble', 'fantástico', 'perfecto', 'amor', 'amo', 'encanta', 
                    'disfruto', 'emocionado', 'entusiasmado', 'dichoso', 'radiante',
                    'orgulloso', 'satisfecho', 'agradecido', 'bendecido', 'afortunado',
                    'celebrar', 'victoria', 'éxito', 'logro', 'triunfo', 'ganar',
                    'reír', 'sonreír', 'brillar', 'esperanza', 'ilusión', 'sueño',
                    'mejor', 'bueno', 'bien', 'positivo', 'hermoso', 'lindo', 'bonito'],
        'peso': 1.0,
        'emoji': '😊',
        'color': '#10b981'
    },
    'tristeza': {
        'palabras': ['triste', 'llorar', 'deprimido', 'solo', 'soledad', 'dolor', 
                    'pérdida', 'melancolía', 'sufrir', 'vacío', 'abandonado', 'lloro',
                    'lágrimas', 'pena', 'angustia', 'desolado', 'afligido', 'abatido',
                    'desesperanza', 'luto', 'extraño', 'nostalgia', 'añoranza',
                    'fracaso', 'perdido', 'roto', 'destrozado', 'herido', 'morir',
                    'muerte', 'perdí', 'falleció', 'ausencia', 'vacío', 'desconsuelo',
                    'depresión', 'depresivo', 'desánimo', 'desanimado', 'desmotivado',
                    'desmotivación', 'cansado', 'cansancio', 'agotado', 'agotamiento',
                    'exhausto', 'sin fuerzas', 'sin ganas', 'sin energía', 'apagado',
                    'gris', 'oscuro', 'oscuridad', 'negro', 'hundido', 'hundirme',
                    'caer', 'cayendo', 'pozo', 'abismo', 'fondo', 'bajo', 'decaído'],
        'peso': 1.0,
        'emoji': '😢',
        'color': '#3b82f6'
    },
    'enojo': {
        'palabras': ['furioso', 'enojado', 'rabia', 'molesto', 'irritado', 'frustrado', 
                    'odio', 'injusto', 'indignado', 'harto', 'enfadado', 'cabreado',
                    'iracundo', 'furia', 'cólera', 'resentido', 'venganza', 'maldito',
                    'estúpido', 'idiota', 'imbécil', 'inútil', 'incompetente',
                    'inaceptable', 'intolerable', 'insoportable', 'asqueroso',
                    'mierda', 'carajo', 'demonios', 'puñeta', 'bronca', 'coraje'],
        'peso': 1.2,
        'emoji': '😠',
        'color': '#ef4444'
    },
    'miedo': {
        'palabras': ['asustado', 'miedo', 'terror', 'pánico', 'ansioso', 'preocupado', 
                    'nervioso', 'aterrado', 'temeroso', 'angustia', 'fobia', 'horror',
                    'espanto', 'pavor', 'amenaza', 'peligro', 'riesgo', 'inseguro',
                    'vulnerable', 'indefenso', 'paralizado', 'temblar', 'tiemblo',
                    'ansiedad', 'incertidumbre', 'duda', 'susto', 'espantoso',
                    'presión', 'pecho', 'miran', 'observan', 'juzgan', 'entiendo',
                    'confundido', 'confusión', 'perdido', 'atrapado', 'ahogo', 'ahogando',
                    'respirar', 'respiro', 'asfixia', 'asfixiando', 'agobio', 'agobiado',
                    'abrumado', 'abrumar', 'sofocado', 'sofocar', 'oprimir', 'oprimido',
                    'inquieto', 'inquietud', 'intranquilo', 'desespero', 'desesperado',
                    'angustiado', 'angustiante', 'agonía', 'tortura', 'tormento',
                    'palpitaciones', 'taquicardia', 'sudor', 'sudo', 'sudando', 'temblor',
                    'mareo', 'mareado', 'vértigo', 'náuseas', 'escalofríos', 'frío',
                    'caliente', 'hormigueo', 'adormecido', 'débil', 'desvanecerme',
                    'desmayo', 'desmayar', 'morir', 'morirme', 'loco', 'loca', 'locura',
                    'control', 'descontrol', 'perder', 'perdiendo', 'escapar', 'huir',
                    'encerrado', 'atrapada', 'atrapado', 'claustrofobia', 'agorafobia',
                    'social', 'gente', 'público', 'expuesto', 'expuesta', 'vergüenza',
                    'ridículo', 'ridícula', 'juzgado', 'juzgada', 'criticado', 'criticada',
                    'rechazado', 'rechazada', 'inadecuado', 'inadecuada', 'inferior',
                    'incapaz', 'incompetente', 'inútil', 'fracasado', 'fracasada',
                    'pasa', 'pasando', 'conmigo', 'mal', 'fatal', 'terrible', 'horrible',
                    'soporto', 'aguanto', 'puedo', 'entender', 'comprender', 'sé', 'idea'],
        'peso': 1.3,
        'emoji': '😨',
        'color': '#8b5cf6'
    },
    'sorpresa': {
        'palabras': ['sorprendido', 'impactado', 'asombrado', 'increíble', 'inesperado', 
                    'wow', 'guau', 'impresionante', 'extraordinario', 'alucinante',
                    'flipar', 'atónito', 'perplejo', 'desconcertado', 'estupefacto',
                    'inaudito', 'insólito', 'chocante', 'pasmado', 'shock'],
        'peso': 0.9,
        'emoji': '😲',
        'color': '#f59e0b'
    },
    'amor': {
        'palabras': ['amor', 'amar', 'querer', 'querido', 'cariño', 'adorar', 'enamorado',
                    'corazón', 'pasión', 'romance', 'romántico', 'besar', 'abrazo',
                    'ternura', 'afecto', 'devoción', 'aprecio', 'estimar', 'tesoro',
                    'alma', 'vida', 'siempre', 'juntos', 'pareja', 'novio', 'novia',
                    'esposo', 'esposa', 'amado', 'amada', 'te amo', 'te quiero'],
        'peso': 1.0,
        'emoji': '❤️',
        'color': '#ec4899'
    },
    'disgusto': {
        'palabras': ['asco', 'repugnante', 'asqueroso', 'nauseabundo', 'vomitar',
                    'desagradable', 'repulsivo', 'horrible', 'grotesco', 'inmundo',
                    'sucio', 'podrido', 'pútrido', 'hediondo', 'pestilente', 'feo'],
        'peso': 1.0,
        'emoji': '🤢',
        'color': '#84cc16'
    }
}

# Palabras intensificadoras
INTENSIFIERS = {
    'muy': 1.5, 'mucho': 1.4, 'muchísimo': 2.0, 'demasiado': 1.6,
    'extremadamente': 2.0, 'totalmente': 1.8, 'completamente': 1.8,
    'absolutamente': 2.0, 'increíblemente': 1.9, 'súper': 1.7,
    'mega': 1.8, 'ultra': 1.9, 'hiper': 1.8, 'bastante': 1.3,
    'realmente': 1.4, 'verdaderamente': 1.5, 'profundamente': 1.7,
    'inmensamente': 1.8, 'enormemente': 1.7, 'terriblemente': 1.6
}

# Negadores
NEGATORS = ['no', 'nunca', 'jamás', 'tampoco', 'ni', 'sin', 'nada', 'nadie', 'ningún', 'ninguno']

# Recomendaciones por emoción
RECOMMENDATIONS = {
    'alegria': [
        "🌟 ¡Tu energía positiva es contagiosa! Sigue cultivando estos momentos.",
        "📝 Considera escribir un diario de gratitud para preservar estos sentimientos.",
        "🤝 Comparte esta alegría con quienes te rodean.",
        "🎯 Aprovecha esta motivación para emprender nuevos proyectos."
    ],
    'tristeza': [
        "💙 Es válido sentirse triste. Permítete procesar tus emociones.",
        "🚶 Una caminata al aire libre puede ayudar a despejar la mente.",
        "📞 Hablar con alguien de confianza puede ser muy reconfortante.",
        "🎵 La música puede ser terapéutica en estos momentos.",
        "🌅 Recuerda: después de la tormenta siempre sale el sol."
    ],
    'enojo': [
        "🧘 Técnicas de respiración profunda: inhala 4 seg, mantén 4 seg, exhala 4 seg.",
        "✍️ Escribir tus pensamientos puede ser liberador y clarificador.",
        "⏸️ Tómate un momento antes de actuar o responder.",
        "🏃 El ejercicio físico es excelente para canalizar esta energía.",
        "🌊 El enojo es temporal, no tomes decisiones permanentes basadas en él."
    ],
    'miedo': [
        "🌬️ RESPIRA: Inhala 4 segundos, mantén 4 segundos, exhala 6 segundos. Repite 5 veces.",
        "🫂 Lo que sientes es real pero temporal. La ansiedad pasa, siempre pasa.",
        "👁️ Si sientes que te miran: la mayoría de personas están enfocadas en sí mismas, no en ti.",
        "💓 La presión en el pecho es ansiedad, no es peligroso. Tu cuerpo está a salvo.",
        "🧊 Técnica 5-4-3-2-1: Nombra 5 cosas que ves, 4 que tocas, 3 que oyes, 2 que hueles, 1 que saboreas.",
        "📱 Si esto es frecuente, considera hablar con un profesional de salud mental. No estás solo/a.",
        "🚶 Sal a caminar, el movimiento ayuda a liberar la tensión acumulada.",
        "💭 Los pensamientos no son hechos. Solo porque lo pienses no significa que sea verdad."
    ],
    'sorpresa': [
        "✨ Las sorpresas nos mantienen alertas y curiosos ante la vida.",
        "📓 Reflexiona sobre cómo este evento inesperado puede ser una oportunidad.",
        "🎯 Mantén la mente abierta a nuevas posibilidades.",
        "🔄 La adaptabilidad es una de las mejores habilidades que puedes desarrollar."
    ],
    'amor': [
        "💕 El amor es una de las emociones más poderosas y transformadoras.",
        "📖 Expresa tus sentimientos, no dejes palabras importantes sin decir.",
        "🌹 Cuida y nutre las relaciones que valoras.",
        "❤️ El amor propio es la base de todo amor saludable."
    ],
    'disgusto': [
        "🔄 Es válido establecer límites ante lo que te desagrada.",
        "🌿 Enfócate en lo que sí te genera bienestar.",
        "🎯 Identifica si puedes cambiar la situación o necesitas aceptarla."
    ],
    'neutral': [
        "🧘 Un estado neutral es ideal para la reflexión y planificación.",
        "📚 Buen momento para actividades que requieren concentración.",
        "🎯 Aprovecha esta calma para organizar tus prioridades.",
        "🌱 La calma es el espacio donde crecen las mejores ideas."
    ]
}


class EmotionAnalyzerAI:
    """Motor de Inteligencia Artificial para análisis de emociones"""
    
    def __init__(self):
        self.emotion_lexicon = EMOTION_LEXICON
        self.intensifiers = INTENSIFIERS
        self.negators = NEGATORS
        print("✅ Motor de IA inicializado correctamente")
    
    def analyze(self, text):
        """Análisis completo del texto"""
        # Preprocesamiento
        text_lower = text.lower()
        words = self._tokenize(text_lower)
        
        # Análisis de emociones
        emotions = self._detect_emotions(text_lower, words)
        
        # Análisis de sentimiento
        sentiment = self._analyze_sentiment(text, emotions)
        
        # Calcular intensidad
        intensity = self._calculate_intensity(text, words)
        
        # Extraer palabras clave
        keywords = self._extract_keywords(words)
        
        # Determinar emoción dominante
        dominant = emotions[0]['name'] if emotions else 'neutral'
        
        # Obtener recomendaciones
        recommendations = RECOMMENDATIONS.get(dominant, RECOMMENDATIONS['neutral'])
        
        return {
            'original_text': text,
            'word_count': len(words),
            'char_count': len(text),
            'sentiment': sentiment,
            'emotions': emotions,
            'intensity': intensity,
            'keywords': keywords,
            'dominant_emotion': dominant,
            'recommendations': recommendations,
            'spanish_emotions': self._get_found_words(text_lower)
        }
    
    def _tokenize(self, text):
        """Tokeniza el texto en palabras"""
        return re.findall(r'\b[a-záéíóúüñ]+\b', text.lower())
    
    def _detect_emotions(self, text_lower, words):
        """Detecta emociones usando el lexicón y análisis contextual"""
        emotion_scores = {}
        
        for emotion, data in self.emotion_lexicon.items():
            score = 0
            found_words = []
            
            for word in data['palabras']:
                if word in text_lower:
                    # Contar ocurrencias
                    count = text_lower.count(word)
                    word_score = count * data['peso']
                    
                    # Verificar intensificadores cercanos
                    for intensifier, multiplier in self.intensifiers.items():
                        pattern = f'{intensifier}\\s+\\w*{word}|{word}\\s+\\w*{intensifier}'
                        if re.search(pattern, text_lower):
                            word_score *= multiplier
                    
                    # Verificar negación
                    for negator in self.negators:
                        pattern = f'{negator}\\s+\\w*\\s*{word}'
                        if re.search(pattern, text_lower):
                            word_score *= -0.5
                    
                    score += word_score
                    found_words.append(word)
            
            if score > 0:
                emotion_scores[emotion] = {
                    'score': score,
                    'words': found_words,
                    'emoji': data['emoji'],
                    'color': data['color']
                }
        
        # Normalizar scores
        total = sum(e['score'] for e in emotion_scores.values()) or 1
        
        emotions = []
        for name, data in emotion_scores.items():
            normalized = (data['score'] / total) * 100
            emotions.append({
                'name': name,
                'emotion': name,
                'emotion_es': f"{data['emoji']} {name.capitalize()}",
                'score': round(normalized, 2),
                'percentage': f"{round(normalized, 1)}%",
                'color': data['color'],
                'found_words': data['words']
            })
        
        # Ordenar por score
        emotions.sort(key=lambda x: x['score'], reverse=True)
        
        # Si no hay emociones, agregar neutral
        if not emotions:
            emotions = [{
                'name': 'neutral',
                'emotion': 'neutral',
                'emotion_es': '😐 Neutral',
                'score': 100,
                'percentage': '100%',
                'color': '#6b7280',
                'found_words': []
            }]
        
        return emotions
    
    def _analyze_sentiment(self, text, emotions):
        """Analiza el sentimiento general"""
        # Usar TextBlob para polaridad base
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        # Ajustar con emociones detectadas
        positive_emotions = {'alegria', 'amor', 'sorpresa'}
        negative_emotions = {'tristeza', 'enojo', 'miedo', 'disgusto'}
        
        emotion_adjustment = 0
        for em in emotions[:3]:
            if em['name'] in positive_emotions:
                emotion_adjustment += em['score'] / 200
            elif em['name'] in negative_emotions:
                emotion_adjustment -= em['score'] / 200
        
        final_polarity = polarity + emotion_adjustment
        final_polarity = max(-1, min(1, final_polarity))
        
        # Determinar etiqueta y estrellas
        if final_polarity > 0.2:
            label = 'Positivo'
            color = '#10b981'
            stars = 4 if final_polarity < 0.5 else 5
        elif final_polarity < -0.2:
            label = 'Negativo'
            color = '#ef4444'
            stars = 2 if final_polarity > -0.5 else 1
        else:
            label = 'Neutral'
            color = '#f59e0b'
            stars = 3
        
        return {
            'label': label,
            'score': abs(final_polarity),
            'polarity': final_polarity,
            'stars': stars,
            'color': color
        }
    
    def _calculate_intensity(self, text, words):
        """Calcula la intensidad emocional"""
        # Factores de intensidad
        exclamations = text.count('!')
        questions = text.count('?')
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        caps_words = len(re.findall(r'\b[A-ZÁÉÍÓÚÑ]{2,}\b', text))
        
        # Contar intensificadores
        intensifier_count = sum(1 for word in words if word in self.intensifiers)
        
        # Repetición de caracteres (ej: "holaaa", "sííí")
        repetitions = len(re.findall(r'(.)\1{2,}', text))
        
        # Calcular score (0-100)
        score = min(100, (
            exclamations * 12 +
            caps_words * 8 +
            caps_ratio * 50 +
            intensifier_count * 15 +
            questions * 5 +
            repetitions * 10
        ))
        
        # Determinar nivel
        if score >= 70:
            level = 'Alta'
            color = '#ef4444'
            description = 'Expresión muy intensa'
        elif score >= 40:
            level = 'Media'
            color = '#f59e0b'
            description = 'Expresión moderada'
        else:
            level = 'Baja'
            color = '#10b981'
            description = 'Expresión calmada'
        
        return {
            'score': round(score),
            'level': level,
            'color': color,
            'description': description,
            'details': {
                'exclamaciones': exclamations,
                'preguntas': questions,
                'mayúsculas': caps_words,
                'intensificadores': intensifier_count,
                'repeticiones': repetitions
            }
        }
    
    def _extract_keywords(self, words):
        """Extrae palabras clave relevantes"""
        stopwords = {
            'el', 'la', 'los', 'las', 'un', 'una', 'de', 'del', 'en', 'y', 'a',
            'que', 'es', 'por', 'con', 'para', 'se', 'su', 'al', 'lo', 'como',
            'más', 'pero', 'sus', 'le', 'ya', 'o', 'este', 'sí', 'porque',
            'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre', 'también', 'me',
            'hasta', 'hay', 'donde', 'quien', 'desde', 'todo', 'nos', 'durante',
            'todos', 'uno', 'les', 'ni', 'contra', 'otros', 'ese', 'eso', 'ante',
            'ellos', 'esto', 'mí', 'antes', 'algunos', 'qué', 'unos', 'yo',
            'otro', 'otras', 'otra', 'él', 'tanto', 'esa', 'estos', 'mucho',
            'nada', 'muchos', 'cual', 'poco', 'ella', 'estar', 'estas', 'algunas',
            'algo', 'nosotros', 'mi', 'mis', 'tú', 'te', 'ti', 'tu', 'tus',
            'he', 'ha', 'han', 'hemos', 'sido', 'ser', 'fue', 'son', 'estoy',
            'está', 'están', 'tengo', 'tiene', 'tienen', 'voy', 'va', 'vas'
        }
        
        filtered = [w for w in words if w not in stopwords and len(w) > 2]
        word_freq = Counter(filtered)
        
        return word_freq.most_common(10)
    
    def _get_found_words(self, text_lower):
        """Obtiene las palabras emocionales encontradas por categoría"""
        found = {}
        for emotion, data in self.emotion_lexicon.items():
            words_found = [w for w in data['palabras'] if w in text_lower]
            if words_found:
                found[emotion] = {
                    'count': len(words_found),
                    'words_found': words_found
                }
        return found


# Instancia global del analizador
analyzer = EmotionAnalyzerAI()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text', '')
    
    if not text.strip():
        return jsonify({'error': 'Por favor, ingresa un texto para analizar'}), 400
    
    try:
        results = analyzer.analyze(text)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': f'Error en el análisis: {str(e)}'}), 500


@app.route('/batch', methods=['POST'])
def batch_analyze():
    data = request.get_json()
    texts = data.get('texts', [])
    
    results = []
    for text in texts:
        if text.strip():
            results.append(analyzer.analyze(text))
    
    return jsonify({'results': results, 'count': len(results)})


@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'engine': 'EmotionAnalyzerAI',
        'version': '2.0'
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🧠 SISTEMA DE ANÁLISIS DE EMOCIONES CON IA")
    print("="*60)
    print("🌐 Accede a: http://localhost:5000")
    print("📊 API: http://localhost:5000/analyze")
    print("💚 Health: http://localhost:5000/health")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
