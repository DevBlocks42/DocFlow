# FR-fr

# Gestionnaire de documents & workflows internes pour PME

## Concept 

Une application qui permet aux petites entreprises ou équipes de gérer leurs documents internes, suivre leur validation, et garder un historique.

# Fonctionnalités principales 

- Gestion des utilisateurs avec rôles (employé, manager, admin)

- Upload de documents (PDF, Word, Excel…) avec catégorisation

- Workflows : création → validation → archivage

- Historique des modifications et notifications internes

- Recherche et filtrage avancé

- Tableau de bord pour managers : documents en attente, statistiques

# Entités principales

- Utilisateur

    - username (string)

    - email (string, unique)

    - password (hashed)

    - role (enum : employé, manager, admin)

    - date_joined

    - avatar 
    
    - service/département

- Document

    - title (string)

    - description (text)

    - file (fichier uploadé, PDF/Word/Excel…)

    - category (ex : contrat, procédure, rapport…)

    - created_by (FK → Utilisateur)

    - created_at, updated_at

    - status (enum : brouillon, en validation, validé, archivé)

    - assigned_to (FK → Utilisateur, pour validation)

- Workflow / Validation

    - document (FK → Document)

    - action (enum : soumis, approuvé, rejeté)

    - performed_by (FK → Utilisateur)

    - performed_at (datetime)

    - comment (text, optionnel)

- Catégorie

    - name (string)

    - description (string, optionnel)

# Relations principales

- Un utilisateur peut créer plusieurs documents → OneToMany

- Un document peut avoir plusieurs étapes de validation → OneToMany

- Une catégorie peut regrouper plusieurs documents → OneToMany

# Fonctionnalités clés

- CRUD complet pour Documents et Catégories

- Upload / téléchargement des fichiers

- Workflow de validation : un document passe par les étapes brouillon → en validation → validé ou rejeté

- Permissions :

    - Employé : peut créer ses documents, voir ses documents

    - Manager : peut valider/rejeter les documents assignés à son équipe

    - Admin : gestion complète (utilisateurs, catégories, documents)

- Dashboard / statistiques : documents en attente, documents validés, activité récente

- Notifications : email ou notifications internes quand un document est assigné ou validé


# EN-en

# Document & worflow management for small/medium companies

## Concept 

An application allowing companies or teams to manage their internal documents, follow their validation and keep an history of changes.

# Main features 

- User management with roles (employee, manager, admin)

- Document upload (PDF, Word, Excel...) with categories

- Workflows : creation -> validation -> archiving

- Modification history and internal notifications

- Search and advances filtering

- Manager's dashboard : pending documents, stats