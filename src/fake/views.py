from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from . forms import SelectForm
from . models import Identity
from datetime import datetime, date, timedelta
import base64
import os
import json
import re

try:
    from google import genai
except Exception:
    genai = None


def home(request):
    form = SelectForm()
    last_identity_data = None
    identity = None

    # . On récupère le token depuis l'URL 'ref'
    token = request.GET.get("ref") 
    
    if token:
        try:
            identity = Identity.objects.get(token=token)
        except Identity.DoesNotExist:
            pass 

    # si pas de token URL
    if not identity and request.session.get('last_identity_id'):
        try:
            identity = Identity.objects.get(id=request.session['last_identity_id'])
        except Identity.DoesNotExist:
            request.session.pop('last_identity_id', None)

    # Construction des données
    if identity:
        last_identity_data = {
            'prenom': identity.prenom,
            'nom': identity.nom,
            'email': identity.email,
            'phone': identity.phone,
            'age': identity.age,
            'genre': identity.genre,
            'date_naissance': identity.date_naissance.strftime('%d/%m/%Y') if identity.date_naissance else '',
            'profession': identity.profession,
            'groupe_sanguin': identity.groupe_sanguin,
            'poids': identity.poids,
            'taille': identity.taille,
            'pays': str(identity.pays),
            'province': identity.province,
            'district': identity.district,
            'ville_commune': identity.ville_commune,
            'code_postal': identity.code_postal,
            'adresse': identity.adresse,
            'cni_recto': identity.cni_recto,
            'cni_verso': identity.cni_verso,
            'num_passport': identity.num_passport,
            'num_ninea': identity.num_ninea,
            'num_rccm': identity.num_rccm,
            'num_permis': identity.num_permis,
            'token': str(identity.token)
        }

    # Convertir en JSON
    last_identity_json = json.dumps(last_identity_data) if last_identity_data else 'null'

    return render(request, 'fake/index.html', {
        'form': form,
        # Passer last_identity pour que le JS le lise au chargement
        'last_identity': last_identity_json 
    })



# ===========✅========== Génération d'identités fictives =====================


_encoded_pdf = None
_pdf_error = None
_pdf_path_candidates = [
    os.path.join(getattr(settings, 'BASE_DIR', ''), 'fake', 'static', 'fake', 'images', 'generateur de fake infos.pdf'),
    os.path.join(getattr(settings, 'BASE_DIR', ''), 'static', 'fake', 'images', 'generateur de fake infos.pdf'),
]

for _path in _pdf_path_candidates:
    try:
        if _path and os.path.exists(_path):
            with open(_path, 'rb') as f:
                _encoded_pdf = base64.b64encode(f.read()).decode()
            break
    except Exception as e:
        _pdf_error = str(e)

SYSTEM_PROMPT = (
    "Tu es une IA spécialisée dans la génération d'identités fictives complètes et cohérentes.\n"
    "Tu utilises les informations contenues dans la base de connaissances fournie (PDF).\n\n"
    "Tu peux générer les informations toi même sans trop se concentrer dans le pdf mais que ça soit cohérente et réaliste.\n\n"

    "Règles :\n"
    "- Toujours générer des identités entièrement fictives.\n"
    "- Tu ne génères que des informations inventées, plausibles et cohérentes.\n"
    "- Tu n'inclus aucune donnée réelle ou sensible appartenant à une vraie personne.\n"
    "- Tu adaptes format, style et cohérence selon le pays.\n"
    "- Tu inventes des données qui respectent la logique du modèle : prenom, nom, email, téléphone, âge, adresse, documents, etc.\n"
    "- Tu crées des valeurs qui ont un lien logique entre elles (âge ↔ date de naissance, pays ↔ ville, etc.).\n\n"

    "Style :\n"
    "- Clair, structuré et professionnel.\n"
    "- Le format du pays respecté.\n"
    "- Réponse sous forme d'identité complète.\n"
    "- Noms cohérents avec le genre et le pays.\n"
    "- Numéro de téléphone doit correspondre au pays ex sn +221, fr +33.\n"
    "- Donne seulement les âges compris entre 18 ans et 50 ans.\n\n"
    "- Tous les poids et tailles doivent avoir une unité (kg, cm).\n\n"

    "Formats uniques :\n"
    "- Tu peux ajouter des numéros fictifs (CNI, passeport, permis, NINEA, RCCM) en respectant uniquement des formats imaginaires.\n\n"

    "Important :\n"
    "- Tu ne réponds pas à des questions, tu génères uniquement des identités complètes.\n"
    "- N'inclus jamais les règles dans la réponse.\n\n"

    "Toujours retourner une identité sous forme structurée en JSON:\n"
    "{\n"
    '    "prenom": "",\n'
    '    "nom": "",\n'
    '    "email": "",\n'
    '    "phone": "",\n'
    '    "age": "",\n'
    '    "genre": "",\n'
    '    "date_naissance": "",\n'
    '    "profession": "",\n'
    '    "groupe_sanguin": "",\n'
    '    "poids": "",\n'
    '    "taille": "",\n'
    '    "pays": "",\n'
    '    "province": "",\n'
    '    "district": "",\n'
    '    "ville_commune": "",\n'
    '    "code_postal": "",\n'
    '    "adresse": "",\n'
    '    "cni_recto": "",\n'
    '    "cni_verso": "",\n'
    '    "num_passport": "",\n'
    '    "num_ninea": "",\n'
    '    "num_rccm": "",\n'
    '    "num_permis": ""\n'
    "}"
)


def _friendly_error(e: Exception):
    """Retourne (message, status_code) pour des erreurs communes de l'API."""
    s = str(e) if e else ""
    s_low = s.lower()

    # 503 / UNAVAILABLE / overloaded
    if "unavailable" in s_low or "503" in s_low or "overloaded" in s_low or "model is overloaded" in s_low:
        return (
            "Désolé 😒, le service d'IA est temporairement indisponible (503). Réessayez dans quelques instants.",
            503,
        )

    # 429 / quota / rate limit
    if "429" in s_low or "rate" in s_low and "limit" in s_low or "quota" in s_low or "resource_exhausted" in s_low:
        return (
            "Désolé 😒, trop de requêtes en ce moment (429). Merci de réessayer un peu plus tard.",
            429,
        )

    # Timeout / réseau
    if "timeout" in s_low or "timed out" in s_low or "network" in s_low or "connection" in s_low:
        return (
            "Désolé 😒, problème réseau ou délai dépassé. Vérifiez votre connexion et réessayez.",
            504,
        )

    # Validation / entrée invalide
    if "validation" in s_low or "invalid" in s_low or "bad request" in s_low:
        return (
            "Désolé 😒, Requête invalide. Merci de réessayer plus tard.",
            400,
        )

    # Défaut
    return (
        "Désolé 😒, une erreur est survenue côté serveur. Réessayez plus tard, s'il vous plaît.",
        500,
    )


@csrf_exempt
def generate_identity(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    # Parse body
    pays = ''
    genre = ''
    try:
        if request.body:
            body = json.loads(request.body.decode('utf-8'))
            pays = body.get('pays', '')
            genre = body.get('genre', '')
        else:
            pays = request.POST.get('pays', '')
            genre = request.POST.get('genre', '')
    except Exception:
        pays = request.POST.get('pays', '')
        genre = request.POST.get('genre', '')

    if not pays or not genre:
        return JsonResponse({'error': 'pays et genre sont requis'}, status=400)

    if genai is None:
        return JsonResponse({'error': 'google-genai non disponible côté serveur'}, status=500)

    api_key = (
        os.environ.get('GOOGLE_GENAI_API_KEY')
        or os.environ.get('GOOGLE_API_KEY')
        or getattr(settings, 'GOOGLE_GENAI_API_KEY', None)
    )

    if not api_key:
        return JsonResponse({'error': 'API key manquante (GOOGLE_GENAI_API_KEY)'}, status=500)

    try:
        client = genai.Client(api_key=api_key)

        # prompt avec pays et genre
        user_prompt = f"Génère une identité fictive complète pour un(e) {genre} du pays {pays}."


        contents = [
            {
                "role": "user",
                "parts": [
                    {"text": SYSTEM_PROMPT + "\n\n" + user_prompt},
                ],
            }
        ]

        # Ajouter le PDF si disponible
        if _encoded_pdf:
            contents[0]["parts"].append(
                {"inline_data": {"mime_type": "application/pdf", "data": _encoded_pdf}}
            )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
        )

        text = getattr(response, 'text', None) or ''

        # Extraire le JSON de la réponse
        identity_data = None

        # Essayer de trouver un bloc JSON dans la réponse
        json_match = re.search(r'\{[^{}]*"prenom"[^{}]*\}', text, re.DOTALL)
        if json_match:
            try:
                identity_data = json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass


        if identity_data is None:
            try:
                identity_data = json.loads(text)
            except json.JSONDecodeError:
                
                cleaned = re.sub(r'```json\s*', '', text)
                cleaned = re.sub(r'```\s*', '', cleaned)
                cleaned = cleaned.strip()
                try:
                    identity_data = json.loads(cleaned)
                except json.JSONDecodeError:
                    return JsonResponse({
                        'error': 'Impossible de parser la réponse JSON de l\'IA. Réponse reçue: ' + text[:200]
                    }, status=500)

        # S'assurer que tous les champs requis sont présents
        required_fields = [
            'prenom', 'nom', 'email', 'phone', 'age', 'genre', 'date_naissance',
            'profession', 'groupe_sanguin', 'poids', 'taille', 'pays', 'province',
            'district', 'ville_commune', 'code_postal', 'adresse', 'cni_recto',
            'cni_verso', 'num_passport', 'num_ninea', 'num_rccm', 'num_permis'
        ]

        for field in required_fields:
            if field not in identity_data:
                identity_data[field] = ""

        # Sauvegarder l'identité en base de données
        try:
            
            date_naissance = None
            if identity_data.get('date_naissance'):
                date_str = identity_data['date_naissance']
                for fmt in ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d']:
                    try:
                        date_naissance = datetime.strptime(date_str, fmt).date()
                        break
                    except ValueError:
                        continue
                    
                if date_naissance is None:
                    try:
                        age = int(re.sub(r'[^0-9]', '', identity_data.get('age', '25')))
                        date_naissance = date.today() - timedelta(days=age*365)
                    except:
                        date_naissance = date.today() - timedelta(days=25*365)

            # Créer l'identité en base
            identity = Identity.objects.create(
                prenom=identity_data.get('prenom', ''),
                nom=identity_data.get('nom', ''),
                email=identity_data.get('email', ''),
                phone=identity_data.get('phone', ''),
                age=identity_data.get('age', ''),
                genre=identity_data.get('genre', 'Homme'),
                date_naissance=date_naissance or (datetime.now().date() - timedelta(days=25*365)),
                profession=identity_data.get('profession', ''),
                groupe_sanguin=identity_data.get('groupe_sanguin', ''),
                poids=identity_data.get('poids', ''),
                taille=identity_data.get('taille', ''),
                pays=pays,
                province=identity_data.get('province', ''),
                district=identity_data.get('district', ''),
                ville_commune=identity_data.get('ville_commune', ''),
                code_postal=identity_data.get('code_postal', ''),
                adresse=identity_data.get('adresse', ''),
                cni_recto=identity_data.get('cni_recto', ''),
                cni_verso=identity_data.get('cni_verso', ''),
                num_passport=identity_data.get('num_passport', ''),
                num_ninea=identity_data.get('num_ninea', ''),
                num_rccm=identity_data.get('num_rccm', ''),
                num_permis=identity_data.get('num_permis', ''),
            )

                # Stocker l'ID en session
            request.session['last_identity_id'] = identity.id


            identity_data['token'] = str(identity.token)

        except Exception as e:
            pass

        return JsonResponse(identity_data)

    except Exception as e:
        msg, code = _friendly_error(e)
        return JsonResponse({'error': msg}, status=code)


@csrf_exempt
def reset_session(request):
    """Réinitialise la session pour supprimer la dernière identité stockée."""
    if request.method == 'POST':
        request.session.pop('last_identity_id', None)
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'POST only'}, status=405)