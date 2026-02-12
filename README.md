# Projet-NSI
README fait avec ChatGPT !!! Mais correspond au projet


---

## 📌 Présentation

**API Studio** est une application desktop développée en **Python avec Tkinter** permettant :

* d’envoyer des requêtes HTTP (GET, POST, PUT, DELETE)
* de gérer dynamiquement les paramètres (Query, Headers, Body)
* d’analyser les réponses serveur
* d’automatiser des tests via un module de bruteforce

L’objectif du projet est de reproduire certaines fonctionnalités d’outils comme **Postman** ou **Burp Suite**, tout en gardant une architecture simple et pédagogique.

---

# ⚙️ Fonctionnement Général

L’application repose sur :

* 🖥 **Interface graphique Tkinter**
* 🌐 **Backend HTTP personnalisé (`ApiClient`)**
* 📦 Gestion dynamique des paramètres
* 🎨 Affichage formaté et coloré du HTML
* 🤖 Module d’automatisation pour tests de sécurité

---

# 🔹 1. Module Requêtes HTTP

L’utilisateur peut :

* Choisir la méthode HTTP : `GET`, `POST`, `PUT`, `DELETE`
* Saisir une URL cible
* Ajouter dynamiquement :

  * Query parameters
  * Headers
  * Body (données envoyées)

### 🔄 Gestion des paramètres

Les paramètres sont stockés sous forme de dictionnaires :

```python
self.params = {
    "query": {},
    "headers": {},
    "body": {}
}
```

Lorsqu’un type de paramètre est sélectionné, l’interface sauvegarde automatiquement l’ancien et charge le nouveau.

Cela permet une gestion propre et flexible des données envoyées.

---

# 🔹 2. Envoi des Requêtes

Les requêtes sont exécutées via un objet `ApiClient`.

Pour éviter le blocage de l’interface graphique :

* L’exécution se fait dans un **thread secondaire**
* L’interface est mise à jour via `root.after()`

Cela garantit une application fluide même lors de requêtes longues.

---

# 🔹 3. Analyse et Affichage de la Réponse

Après réception de la réponse :

* Le code HTTP est affiché
* Le contenu HTML est formaté avec `BeautifulSoup`
* Une coloration syntaxique est appliquée via le widget `Text` de Tkinter

Les éléments colorés :

* Balises HTML
* Attributs
* Valeurs
* Commentaires

Cela améliore considérablement la lisibilité.

---

# 🔹 4. Visualisation de la Page

Un bouton permet d’ouvrir le HTML reçu :

* Le contenu est écrit dans un fichier temporaire
* Il est ensuite ouvert dans le navigateur par défaut

Cela permet de voir le rendu réel de la page.

---

# 🔹 5. Module Automatisation (Bruteforce)

L’application intègre une fenêtre dédiée à l’automatisation.

## 🎯 Objectif

Tester une liste de mots de passe contre une cible HTTP.

## ⚠️ Principe de fonctionnement

Ce bruteforce repose sur une technique d’analyse par **différence de longueur de réponse**.

Il fonctionne uniquement lorsque :

> Le message d’erreur change lorsque le bon identifiant est trouvé.

Cela provoque généralement une différence dans la taille (longueur) de la réponse HTTP.

L’outil affiche donc dans la console :

```
motdepasse_testé -> longueur: XXX
```

L’utilisateur peut alors identifier une variation suspecte.

## 🔧 Paramètres du bruteforce

* URL cible
* Clé principale (ex: password)
* Clé secondaire optionnelle
* Valeur personnalisée pour la seconde clé
* Liste de mots de passe

Les résultats sont affichés dans la console.

---

# 🏗 Architecture Simplifiée

```
App (Tkinter UI)
│
├── ApiClient (gestion HTTP)
├── ScrollableKeyValueFrame (gestion dynamique des paramètres)
├── parse_html (formatage + coloration HTML)
└── Module Bruteforce
```

---


