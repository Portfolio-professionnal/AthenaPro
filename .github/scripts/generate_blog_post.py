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
    text = unicodedata.normalize('NFKD', title).encode('ASCII', 'ignore').decode('utf-8')
    text = text.lower().replace(" ", "-").replace("'", "-").replace("'", "-")
    text = re.sub(r'[^\w\-]', '', text)
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
        # Modification ici pour corriger le problème d'encodage
        if isinstance(prompt, bytes):
            prompt = prompt.decode('utf-8')
        
        result = subprocess.run(
            ["gh", "copilot", "suggest"],
            input=prompt.encode('utf-8') if isinstance(prompt, str) else prompt,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur Copilot CLI : {e}")
        print(f"Sortie d'erreur : {e.stderr}")
        raise

def extract_json_from_response(response):
    """Extraire JSON de la réponse de Copilot."""
    try:
        if isinstance(response, bytes):
            response = response.decode('utf-8')
            
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if not json_match:
            raise ValueError("Aucun JSON trouvé dans la réponse de Copilot")
        return json.loads(json_match.group())
    except (json.JSONDecodeError, ValueError) as e:
        print(f"❌ Erreur lors du parsing JSON : {e}")
        print(f"Réponse reçue : {response}")
        raise

def generate_article_metadata():
    """Génère les métadonnées de l'article avec Copilot."""
    existing_titles = read_existing_titles()
    titles_list = "\n".join(f"- {title}" for title in existing_titles)

    prompt = f"""
    Contexte : AthenaPro est un service de création de landing pages et portfolios professionnels 
    en HTML/CSS/Tailwind, destiné aux freelances, indépendants et jeunes diplômés.

    Titres existants :
    {titles_list}

    Instructions : Génère un nouvel article sur un sujet pertinent pour mon audience.
    Retourne uniquement un objet JSON au format suivant :
    {{
        "title": "Titre inédit et accrocheur",
        "category": "Conseils",
        "excerpt": "Description courte et persuasive",
        "image_url": "https://i.postimg.cc/URL-de-image",
        "keywords": ["mot-clé1", "mot-clé2", "mot-clé3"]
    }}
    """

    response = get_copilot_suggestion(prompt)
    return extract_json_from_response(response)

def generate_article_content(metadata, datetime_info):
    """Génère le contenu complet de l'article avec Copilot."""
    prompt = f"""
    Génère un article complet en Markdown pour mon blog AthenaPro.
    
    Front-matter requis :
    ---
    layout: post
    title: "{metadata['title']}"
    date: {datetime_info['iso']}
    category: "{metadata['category']}"
    excerpt: "{metadata['excerpt']}"
    image: "{metadata['image_url']}"
    ---

    Structure requise :
    1. Une introduction accrocheuse
    2. Un sommaire avec ancres vers les sections
    3. Au moins 5 sections avec du contenu riche (texte, listes, citations, images)
    4. Une conclusion avec un appel à l'action vers AthenaPro
    5. Une note de mise à jour

    Le contenu doit être utile pour les freelances, indépendants et jeunes diplômés.
    """

    return get_copilot_suggestion(prompt)

def main():
    try:
        # Créer le dossier _posts s'il n'existe pas
        os.makedirs("_posts", exist_ok=True)

        # Obtenir date/heure Paris
        datetime_info = get_paris_datetime()

        # Générer métadonnées
        print("📝 Génération des métadonnées de l'article...")
        metadata = generate_article_metadata()
        print(f"✅ Métadonnées générées : {metadata['title']}")

        # Générer contenu
        print("📝 Génération du contenu de l'article...")
        article_content = generate_article_content(metadata, datetime_info)
        print("✅ Contenu généré")

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
