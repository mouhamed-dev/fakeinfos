# --- Imports à ajouter en haut de views.py ---
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from . models import Identity

# --- Nouvelle fonction à la fin de views.py ---
def download_pdf(request):
    """Génère un PDF avec les informations de la dernière identité."""
    
     # 1. On cherche d'abord le token dans l'URL (C'est ça qui va sauver la prod)
    token = request.GET.get('ref')
    identity = None

    if token:
        try:
            identity = Identity.objects.get(token=token)
        except Identity.DoesNotExist:
            pass
    
    # 2. Si pas de token, on essaie l'ancienne méthode (Session)
    if not identity:
        identity_id = request.session.get('last_identity_id')
        if identity_id:
            try:
                identity = Identity.objects.get(id=identity_id)
            except Identity.DoesNotExist:
                pass

    if not identity:
        return HttpResponse("Identité introuvable ou expirée.", status=404)


    # 2. Préparer la réponse HTTP (type fichier PDF)
    response = HttpResponse(content_type='application/pdf')
    filename = f"Identite_{identity.prenom}_{identity.nom}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # 3. Création du Canvas (le document PDF)
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 2 * cm  # Position verticale de départ (haut de page)

    p.setTitle(f"Fiche d'Identité - {identity.prenom} {identity.nom}")
    p.setAuthor("MouhaTech")
    p.setSubject("Générateur de fausses informations")
    p.setCreator("MouhaTech Generator")
    p.setProducer("MouhaTech Generator")

    # --- Titre ---
    p.setFont("Helvetica-Bold", 20)
    p.setFillColor(colors.darkslateblue)
    p.drawString(2 * cm, y, "Fiche d'Identité Fictive")
    y -= 1.5 * cm

    # Fonction utilitaire pour écrire une ligne
    def draw_line(label, value):
        nonlocal y
        p.setFont("Helvetica-Bold", 12)
        p.setFillColor(colors.black)
        p.drawString(2 * cm, y, f"{label} :")
        
        p.setFont("Helvetica", 12)
        p.setFillColor(colors.darkslategray)
        # On décale la valeur vers la droite
        p.drawString(7 * cm, y, str(value) if value else "-")
        y -= 0.8 * cm # Espace entre les lignes
        
        # Saut de page si on arrive en bas
        if y < 2 * cm:
            p.showPage()
            y = height - 2 * cm

    # --- Section 1 : Infos Personnelles ---
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(colors.gray)
    p.drawString(2 * cm, y, "INFORMATIONS PERSONNELLES")
    # Ligne de séparation
    p.setStrokeColor(colors.lightgrey)
    p.line(2 * cm, y - 0.2*cm, width - 2*cm, y - 0.2*cm)
    y -= 1 * cm

    draw_line("Prénom", identity.prenom)
    draw_line("Nom", identity.nom)
    draw_line("Genre", identity.genre)
    draw_line("Né(e) le", identity.date_naissance.strftime('%d/%m/%Y') if identity.date_naissance else "-")
    draw_line("Âge", f"{identity.age} ans" if identity.age else "-")
    draw_line("Email", identity.email)
    draw_line("Téléphone", identity.phone)
    draw_line("Profession", identity.profession)
    draw_line("Gr. Sanguin", identity.groupe_sanguin)
    draw_line("Taille / Poids", f"{identity.taille} / {identity.poids}")

    y -= 0.5 * cm # Espacement supplémentaire

    # --- Section 2 : Coordonnées géographiques ---
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(colors.gray)
    p.drawString(2 * cm, y, "Coordonnées géographiques")
    p.line(2 * cm, y - 0.2*cm, width - 2*cm, y - 0.2*cm)
    y -= 1 * cm

    draw_line("Pays", identity.pays)
    draw_line("Région/Province", identity.province)
    draw_line("District", identity.district)
    draw_line("Ville/Commune", identity.ville_commune)
    draw_line("Adresse", identity.adresse)
    draw_line("Code Postal", identity.code_postal)

    y -= 0.5 * cm

    # --- Section 3 : Informations d'identification ---
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(colors.gray)
    p.drawString(2 * cm, y, "Informations d'identification")
    p.line(2 * cm, y - 0.2*cm, width - 2*cm, y - 0.2*cm)
    y -= 1 * cm

    draw_line("CNI (Recto)", identity.cni_recto)
    draw_line("CNI (Verso)", identity.cni_verso)
    draw_line("Passeport", identity.num_passport)
    draw_line("NINEA", identity.num_ninea)
    draw_line("RCCM", identity.num_rccm)
    draw_line("Permis", identity.num_permis)


    # --- Footer ---
    name = "https://mouhatech.com"
    footer_text = f"Généré par {name} - Document Fictif"
    site_url = "https://mouhatech.com"

    # 1. Augmentation de la taille de police (de 8 à 10)
    p.setFont("Helvetica-Oblique", 10)
    p.setFillColor(colors.gray)

    # 2. Calcul pour centrer le texte parfaitement
    text_width = p.stringWidth(footer_text, "Helvetica-Oblique", 10)
    x_pos = (width - text_width) / 2
    y_pos = 1 * cm

    # 3. Dessiner le texte
    p.drawString(x_pos, y_pos, footer_text)

    # 4. Créer la zone cliquable (Lien) par-dessus le texte
    # Format du rectangle : (x1, y1, x2, y2) -> (gauche, bas, droite, haut)
    p.linkURL(site_url, (x_pos, y_pos - 2, x_pos + text_width, y_pos + 10), relative=1)

    # 4. Fermeture et envoi
    p.showPage()
    p.save()
    return response