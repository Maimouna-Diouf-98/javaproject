# Generated by Django 5.1.2 on 2024-11-19 14:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fichier_csv', '0004_remove_fichier_projet_fichier_site'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='fichiers/')),
                ('nom', models.CharField(max_length=255)),
                ('niveau_tension', models.CharField(max_length=50)),
                ('categorie_tarifaire', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('site', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='fichiers', to='sites.sites')),
            ],
        ),
        migrations.CreateModel(
            name='DonneesAnnuelles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annee', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donnees_annuelles', to='fichier_csv.client')),
            ],
        ),
        migrations.CreateModel(
            name='DonneesMensuelles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mois', models.CharField(max_length=20)),
                ('puissance_souscrite', models.FloatField()),
                ('k1', models.FloatField(verbose_name='K1 (kWh)')),
                ('k2', models.FloatField(verbose_name='K2 (kWh)')),
                ('ma', models.FloatField(verbose_name='Ma')),
                ('energie_reactive', models.FloatField(verbose_name='Energie Réactive (kWh)')),
                ('puissance_max_releve', models.FloatField(verbose_name='Puissance max relevée (kWh)')),
                ('nombre_de_jours_facture', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('donnees_annuelles', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donnees_mensuelles', to='fichier_csv.donneesannuelles')),
            ],
        ),
        migrations.DeleteModel(
            name='Fichier',
        ),
    ]
