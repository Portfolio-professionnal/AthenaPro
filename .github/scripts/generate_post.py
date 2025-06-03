import os
import glob
from datetime import datetime
import random
from pathlib import Path

def get_existing_topics():
    """Récupère les sujets déjà traités"""
    posts_dir = Path('_posts')
    existing_topics = []
    
    if posts_dir.exists():
        for post in posts_dir.glob('*.md'):
            with open(post, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extrait le titre du frontmatter
                if 'title: "' in content:
                    title = content.split('title: "')[1].split('"')[0]
                    existing_topics.append(title.lower())
    
    return existing_topics

def generate_new_topic():
    """Génère un nouveau sujet non traité"""
    existing = get_existing_topics()
    base_topics = [
        "portfolio", "landing page", "UX/UI", "web design", 
        "conversion", "personal branding", "analytics"
    ]
    
    topic_templates = [
        "Comment optimiser votre {topic} en 2025",
        "Les meilleures pratiques {topic} pour freelances",
        "Guide complet : {topic} qui convertit",
        "5 techniques avancées de {topic}",
        "L'art du {topic} professionnel",
    ]
    
    while True:
        topic = random.choice(base_topics)
        template = random.choice(topic_templates)
        title = template.format(topic=topic)
        if title.lower() not in existing:
            return title

def generate_article_content(title):
    """Génère le contenu de l'article"""
    sections = [
        {
            "title": "Introduction",
            "content": f"Dans le monde digital en constante évolution, la maîtrise du {title.split(':')[-1].strip()} est devenue cruciale."
        },
        {
            "title": "Les fondamentaux",
            "content": "Comprendre les bases est essentiel pour construire une stratégie efficace."
        },
        {
            "title": "Stratégies avancées",
            "content": "Découvrez les techniques qui font la différence entre un projet ordinaire et un projet exceptionnel."
        },
        {
            "title": "Mise en pratique",
            "content": "Appliquez ces concepts à travers des exemples concrets et des cas d'études."
        },
        {
            "title": "Conclusion",
            "content": "En suivant ces conseils, vous pourrez significativement améliorer vos résultats."
        }
    ]
    
    return {
        "title": title,
        "category": random.choice(["Design", "Marketing", "Développement", "Stratégie"]),
        "excerpt": f"Découvrez comment optimiser votre présence en ligne grâce à nos conseils experts sur {title.lower()}",
        "image": "https://i.postimg.cc/W3THdGdS/PORTFOLIO.webp",
        "sections": sections
    }

def main():
    try:
        # Génère un nouveau sujet
        title = generate_new_topic()
        article = generate_article_content(title)
        
        # Crée le nom du fichier
        date = datetime.now()
        filename = f"{date.strftime('%Y-%m-%d')}-{title.lower().replace(' ', '-')}.md"
        
        # Assure que le dossier _posts existe
        os.makedirs('_posts', exist_ok=True)
        
        # Génère le contenu avec le template HTML
        content = f"""---
layout: post
title: "{article['title']}"
date: {date.strftime('%Y-%m-%d %H:%M:%S +0100')}
category: "{article['category']}"
excerpt: "{article['excerpt']}"
image: "{article['image']}"
---

<main class="pt-24 pb-16 bg-[#0A0118] text-white font-serif">
  <div class="container mx-auto px-4 max-w-4xl">
    <div class="mb-10 rounded-xl overflow-hidden shadow-lg">
      <img 
        src="{{{{ page.image }}}}" 
        alt="{{{{ page.title }}}}" 
        loading="lazy"
        class="w-full h-72 object-cover object-center transition-transform duration-500 hover:scale-105"
      />
    </div>

    <article class="max-w-none">
      <h1 class="text-4xl font-bold mb-6 neon-text">{{{{ page.title }}}}</h1>
      
      <div class="flex items-center mb-8">
        <span class="text-sm text-gray-400">{{{{ page.date | date: "%d %B %Y" }}}}</span>
        <span class="mx-2 text-gray-500">•</span>
        <span class="text-sm text-[#FF61D2]">{{{{ page.category }}}}</span>
      </div>

      <!-- Contenu de l'article -->
      {{% for section in article['sections'] %}}
      <h2 class="text-3xl font-bold mt-8 neon-text">{{{{ section['title'] }}}}</h2>
      <p class="mt-4 leading-relaxed text-gray-300">{{{{ section['content'] }}}}</p>
      {{% endfor %}}

      <!-- Call-to-action -->
      <div class="mt-12 p-6 bg-[#1A1128] rounded-xl border border-[#FF61D2]">
        <h3 class="text-2xl font-bold mb-4">Besoin d'aide pour votre projet ?</h3>
        <p class="mb-4 text-gray-300">Je peux vous aider à créer une landing page ou un portfolio qui convertit.</p>
        <a href="https://athenapro.ovh/Contact.html" class="inline-block bg-[#FF61D2] text-white font-bold py-3 px-6 rounded-full hover:scale-105 transition-transform">
          Contactez-moi
        </a>
      </div>
    </article>
  </div>
</main>"""
        
        # Sauvegarde l'article
        filepath = os.path.join('_posts', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Article créé avec succès : {filepath}")
        
    except Exception as e:
        print(f"Erreur lors de la création de l'article : {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()