import json
import os
import re
import subprocess
from datetime import datetime
import pytz
import unicodedata
import yaml
from pathlib import Path

def read_existing_titles():
    """Lit tous les titres d'articles existants dans le dossier _posts."""
    existing_titles = set()
    posts_dir = Path("_posts")
    if posts_dir.exists():
        for post_file in posts_dir.glob("*.md"):
            content = post_file.read_text(encoding="utf-8")
            if content.startswith("---"):
                _, front_matter, _ = content.split("---", 2)
                try:
                    meta = yaml.safe_load(front_matter)
                    if "title" in meta:
                        existing_titles.add(meta["title"])
                except yaml.YAMLError:
                    continue
    return existing_titles

def generate_slug(title):
    """Génère un slug URL-friendly à partir du titre."""
    # Convertir en minuscules et remplacer les accents
    text = unicodedata.normalize('NFKD', title).encode('ASCII', 'ignore').decode('utf-8')
    # Convertir en minuscules et remplacer espaces/apostrophes par des tirets
    text = text.lower().replace(" ", "-").replace("'", "-").replace("'", "-")
    # Supprimer tous les caractères non alphanumériques sauf tirets et underscores
    text = re.sub(r'[^\w\-]', '', text)
    # Supprimer les tirets multiples consécutifs
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

def get_paris_datetime():
    """Obtient la date et l'heure actuelles à Paris."""
    paris_tz = pytz.timezone('Europe/Paris')
    now = datetime.now(paris_tz)
    return {
        'iso': now.strftime('%Y-%m-%d %H:%M:%S +0200'),
        'date': now.strftime('%Y-%m-%d'),
        'readable': now.strftime('%d %B %Y')
    }

def get_copilot_suggestion(prompt):
    """Obtient une suggestion de GitHub Copilot via CLI."""
    try:
        result = subprocess.run(
            ["gh", "copilot", "suggest", "--target", "shell"],
            input=prompt.encode('utf-8'),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur Copilot CLI : {e}")
        print(f"Sortie d'erreur : {e.stderr}")
        raise

def generate_article_metadata():
    """Génère les métadonnées de l'article avec Copilot."""
    existing_titles = read_existing_titles()
    titles_list = "\n".join(f"- {title}" for title in existing_titles)

    prompt = f"""
    Contexte : AthenaPro = service de création de landing pages & portfolios pro HTML/CSS/Tailwind 
    pour freelances, indépendants, jeunes diplômés.

    Titres existants :
    {titles_list}

    Génère un JSON avec :
    {{
        "title": "Nouveau titre inédit et accrocheur",
        "category": "Conseils, Tutoriel, ou Astuces",
        "excerpt": "Description courte et persuasive",
        "image_url": "URL d'une image pertinente sur postimg.cc",
        "keywords": ["mot-clé1", "mot-clé2", "mot-clé3"]
    }}
    """

    response = get_copilot_suggestion(prompt)
    try:
        # Extraire le JSON de la réponse
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if not json_match:
            raise ValueError("Pas de JSON trouvé dans la réponse")
        return json.loads(json_match.group())
    except (json.JSONDecodeError, ValueError) as e:
        print(f"❌ Erreur parsing JSON : {e}")
        raise

def generate_article_content(metadata, datetime_info):
    """Génère le contenu complet de l'article avec Copilot."""
    prompt = f"""
    Génère un article en Markdown pour AthenaPro avec ce front-matter :
    ---
    layout: post
    title: "{metadata['title']}"
    date: {datetime_info['iso']}
    category: "{metadata['category']}"
    excerpt: "{metadata['excerpt']}"
    image: "{metadata['image_url']}"
    ---

    L'article doit :
    1. Suivre la structure HTML/Tailwind fournie
    2. Inclure un sommaire avec ancres
    3. Avoir au moins 5 sections avec texte, images, listes, citations
    4. Finir par une conclusion et CTA vers AthenaPro
    5. Être pertinent pour les freelances et indépendants
    """

    article_content = get_copilot_suggestion(prompt)
    return article_content

def main():
    # Créer le dossier _posts s'il n'existe pas
    os.makedirs("_posts", exist_ok=True)

    # Obtenir date/heure Paris
    datetime_info = get_paris_datetime()

    try:
        # Générer métadonnées
        metadata = generate_article_metadata()

        # Générer contenu
        article_content = generate_article_content(metadata, datetime_info)

        # Créer nom fichier
        slug = generate_slug(metadata['title'])
        filename = f"_posts/{datetime_info['date']}-{slug}.md"

        # Écrire article
        with open(filename, "w", encoding="utf-8") as f:
            f.write(article_content)

        print(f"✅ Nouvel article généré : {filename}")

    except Exception as e:
        print(f"❌ Erreur lors de la génération : {str(e)}")
        raise

if __name__ == "__main__":
    main()
