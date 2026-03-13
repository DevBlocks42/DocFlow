# DocFlow

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Django](https://img.shields.io/badge/Django-Framework-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-Educational-lightgrey)

**DocFlow** est un **Document Management System (DMS)** développé avec **Django** permettant de gérer le cycle de vie des documents dans une organisation : création, validation, consultation et suivi de l’historique.

Ce projet met l'accent sur :

- une **architecture propre**
- la **séparation de la logique métier**
- un **workflow de validation**
- la **traçabilité des actions**
- une **interface ergonomique avec tri, filtrage et pagination**

---

# Fonctionnalités

## Gestion des documents

- upload sécurisé de fichiers
- création et modification des métadonnées
- téléchargement de documents
- gestion des statuts

Exemples de statuts :

- Draft / Brouillon
- Pending / En validation
- Approved / Approuvé
- Archived / Archivé

---

## Workflow de validation

Les documents suivent un processus de validation.

```
Draft → Pending → Approved
                 ↘ Archived
```

Les managers peuvent :

- approuver un document
- rejeter un document
- consulter l’historique

---

# Historique des documents

Chaque document possède un historique retraçant :

- les changements de statut
- les validations
- les utilisateurs ayant effectué les actions

Cela permet d'assurer la **traçabilité complète du cycle de vie d’un document**.

---

# Gestion des utilisateurs

Le système distingue plusieurs rôles :

| Rôle | Permissions |
|-----|-----|
| Employe | Création et consultation de ses documents |
| Manager | Validation ou rejet |
| Admin | Gestion complète |

Les permissions sont appliquées via :

- filtres de queryset
- logique métier dans les services
- contrôles dans les vues

---

# Recherche et navigation

L’interface permet une navigation efficace :

- tri par colonne
- filtres dynamiques
- pagination

Les filtres s’adaptent au type de champ :

- champ texte → recherche libre
- `ChoiceField` → menu déroulant

---

# Architecture du projet

Le projet suit une architecture visant à **séparer la logique métier de la couche web**.

```
apps/
 ├── documents/
 │
 │   ├── models.py
 │   ├── views.py
 │   ├── forms.py
 │   ├── services/
 │   │     └── document_service.py
 │   ├── templates/
 │   ├── tests/
 │   └── urls.py
 ├── workflows/
 ├── users/
```

---

# Architecture applicative

```
Client
  │
  ▼
Django Views
  │
  ▼
Services (Logique métier)
  │
  ▼
Models
  │
  ▼
Database
```

### Principe

- **Views** : gestion des requêtes HTTP & contrôles d'accès
- **Services** : logique métier
- **Models** : accès aux données

Exemple :

```python
document = document_service.create_document(request.user, form)
```

---

# Technologies

| Technologie | Rôle |
|-----|-----|
| Python | langage principal |
| Django | framework web |
| Bootstrap | interface utilisateur |
| PostgreSQL | base de données |

---

# Installation

## Cloner le projet

```bash
git clone https://github.com/devblocks42/DocFlow.git
cd DocFlow
```

---

## Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate
```

---

## Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## Appliquer les migrations

```bash
python manage.py migrate
```

---

## Lancer le serveur

```bash
python manage.py runserver
```

Application disponible sur :

```
http://127.0.0.1:8000
```

---

# Tests

Lancer les tests :

```bash
python manage.py test
```

Les tests couvrent notamment :

- l'authentification
- les filtres de documents

---

# Sécurité

Mesures mises en place :

- validation des formulaires
- contrôles d'accès selon les rôles
- gestion sécurisée des fichiers uploadés (CDR pour images & pdf)

---

# Objectif du projet

Ce projet a été développé afin de :

- approfondir **Django**
- pratiquer la **séparation des responsabilités**
- implémenter un **workflow de validation**
- concevoir une **application web maintenable**

---

# Licence

Projet à but pédagogique.