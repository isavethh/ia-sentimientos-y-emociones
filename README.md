# 🧠 Analizador de Emociones con Inteligencia Artificial

Un sistema completo de análisis de sentimientos y emociones impulsado por modelos de IA de última generación.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![Transformers](https://img.shields.io/badge/Transformers-4.36-orange.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

## ✨ Características

### 🔍 Análisis Completo
- **Detección de Sentimientos**: Positivo, Negativo, Neutral con puntuación de confianza
- **Análisis de Emociones**: Alegría, Tristeza, Enojo, Miedo, Sorpresa, Disgusto
- **Intensidad Emocional**: Medición de la fuerza expresiva del texto
- **Palabras Clave**: Extracción automática de términos relevantes
- **Análisis en Español**: Detección de palabras emocionales en español

### 🤖 Modelos de IA Utilizados
- **DistilRoBERTa** para clasificación de emociones
- **BERT Multilingüe** para análisis de sentimientos
- **TextBlob** como fallback para análisis básico

### 💡 Recomendaciones Inteligentes
El sistema proporciona recomendaciones personalizadas basadas en las emociones detectadas para ayudar al usuario.

## 🚀 Instalación

### Requisitos Previos
- Python 3.9 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
```bash
cd c:\Users\Personal\Downloads\ia
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación**
```bash
python app.py
```

5. **Abrir en el navegador**
```
http://localhost:5000
```

## 📖 Uso

### Interfaz Web
1. Escribe o pega el texto que deseas analizar
2. Haz clic en "Analizar con IA"
3. Observa los resultados detallados:
   - Sentimiento general con estrellas
   - Gráfico de emociones detectadas
   - Medidor de intensidad emocional
   - Palabras clave extraídas
   - Recomendaciones personalizadas

### API REST

#### Analizar texto
```bash
POST /analyze
Content-Type: application/json

{
    "text": "Estoy muy feliz hoy, todo salió perfecto!"
}
```

#### Respuesta
```json
{
    "original_text": "Estoy muy feliz hoy, todo salió perfecto!",
    "word_count": 7,
    "sentiment": {
        "label": "Positivo",
        "score": 0.95,
        "stars": 5,
        "color": "#4CAF50"
    },
    "emotions": [
        {"emotion": "joy", "emotion_es": "😊 Alegría", "score": 85.5}
    ],
    "intensity": {
        "score": 35,
        "level": "Baja"
    },
    "keywords": [["feliz", 1], ["perfecto", 1]],
    "recommendations": ["🌟 ¡Excelente! Tu energía positiva es contagiosa."]
}
```

#### Análisis por lotes
```bash
POST /batch
Content-Type: application/json

{
    "texts": ["Texto 1", "Texto 2", "Texto 3"]
}
```

## 🏗️ Arquitectura

```
ia/
├── app.py              # Aplicación principal Flask + Modelos IA
├── requirements.txt    # Dependencias del proyecto
├── README.md          # Documentación
└── templates/
    └── index.html     # Interfaz web interactiva
```

## 🧪 Ejemplos de Uso

### Alegría
```
"¡Hoy fue el mejor día de mi vida! Me siento increíblemente feliz y agradecido."
```

### Tristeza
```
"Me siento muy triste y solo. Extraño mucho a mi familia."
```

### Enojo
```
"¡Estoy FURIOSO! No puedo creer la injusticia que acabo de presenciar."
```

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
FLASK_ENV=development   # Modo desarrollo
FLASK_DEBUG=1          # Debug activado
PORT=5000              # Puerto del servidor
```

### Modelos Personalizados
Puedes cambiar los modelos de IA en `app.py`:
```python
emotion_classifier = pipeline(
    "text-classification", 
    model="tu-modelo-personalizado"
)
```

## 📊 Tecnologías Utilizadas

| Tecnología | Uso |
|------------|-----|
| Python 3.9+ | Lenguaje principal |
| Flask | Framework web |
| Transformers | Modelos de IA |
| PyTorch | Backend de ML |
| NLTK | Procesamiento de lenguaje |
| TextBlob | Análisis de sentimientos |
| HTML/CSS/JS | Interfaz web |

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -m 'Añadir nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👤 Autor

Desarrollado con ❤️ por GitHub Copilot

---

⭐ Si este proyecto te fue útil, ¡dale una estrella!
