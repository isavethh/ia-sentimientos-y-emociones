import requests

texto = "no se que pasa conmigo en serio, siento una fuerte presion en mi pecho siento que todos me miran y no entiendo nada"

r = requests.post('http://localhost:5000/analyze', json={'text': texto})
d = r.json()

print("="*60)
print("TU TEXTO:")
print(f'"{texto}"')
print("="*60)

print(f"\nSENTIMIENTO: {d['sentiment']['label']} {'★' * d['sentiment']['stars']}")

print("\nEMOCIONES DETECTADAS:")
for e in d['emotions'][:5]:
    print(f"  {e['emotion_es']}: {e['percentage']}")

print(f"\nINTENSIDAD: {d['intensity']['level']} ({d['intensity']['score']}%)")

print("\nPALABRAS EMOCIONALES ENCONTRADAS:")
for emo, data in d.get('spanish_emotions', {}).items():
    print(f"  {emo}: {', '.join(data['words_found'])}")

print("\nRECOMENDACIONES PARA TI:")
for rec in d['recommendations'][:4]:
    print(f"  {rec}")
