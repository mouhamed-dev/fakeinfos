from django.db import models
from django_countries.fields import CountryField
import uuid
class Identity(models.Model):

    GENRE = [
        ('Homme', 'Masculin'),
        ('Femme', 'Féminin'),
    ]

    prenom = models.CharField(max_length=60)
    nom = models.CharField(max_length=60)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    age = models.CharField(max_length=12)
    genre = models.CharField(max_length=30, choices=GENRE, default='Homme')
    date_naissance = models.DateField()
    profession = models.CharField(max_length=100)
    groupe_sanguin = models.CharField(max_length=12)
    poids = models.CharField(max_length=12)
    taille = models.CharField(max_length=12)

    pays = CountryField(default='SN')
    province = models.CharField(max_length=60)
    district = models.CharField(max_length=60)
    ville_commune = models.CharField(max_length=60)
    code_postal = models.CharField(max_length=10)
    adresse = models.CharField(max_length=100)

    cni_recto = models.CharField(max_length=30)
    cni_verso = models.CharField(max_length=30)
    num_passport = models.CharField(max_length=30)
    num_ninea = models.CharField(max_length=30)
    num_rccm = models.CharField(max_length=30)
    num_permis = models.CharField(max_length=30)

    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.prenom} - {self.nom}"

    class Meta:
        verbose_name = 'Personne'
        verbose_name_plural = 'Personnes'
        ordering = ['-date']