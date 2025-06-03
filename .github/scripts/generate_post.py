import os
from datetime import datetime
import random
from pathlib import Path

def get_todays_topic():
    """Génère un sujet pertinent pour AthenaPro"""
    topics = [
        "Portfolio", "Landing Page", "UX/UI", "Conversion",
        "Personal Branding", "Web Design", "Analytics"
    ]
    
    templates = [
        "Comment optimiser votre {topic} en 2025",
        "Les meilleures pratiques {topic} pour freelances",
        "Guide complet : {topic} qui convertit",
        "5 techniques avancées de {topic}",
        "L'art du {topic} professionnel"
    ]
    
    topic = random.choice(topics)
    template = random.choice(templates)
    return template.format(topic=topic.lower())

def main():
    try:
        # Création du dossier _posts si nécessaire
        os.makedirs('_posts', exist_ok=True)
        
        # Génération du titre
        title = get_todays_topic()
        date = datetime.now()
        
        # Création du nom de fichier
        filename = f"{date.strftime('%Y-%m-%d')}-{title.lower().replace(' ', '-')}.md"
        filepath = os.path.join('_posts', filename)
        
        # Génération du contenu
        content = f"""---
layout: post
title: "{title}"
date: {date.strftime('%Y-%m-%d %H:%M:%S +0100')}
category: "Design"
excerpt: "Découvrez les meilleures pratiques et techniques avancées pour améliorer votre présence en ligne"
image: "https://i.postimg.cc/W3THdGdS/PORTFOLIO.webp"
---

<main class="pt-24 pb-16 bg-[#0A0118] text-white font-serif">
  <div class="container mx-auto px-4 max-w-4xl">
    <div class="mb-10 rounded-xl overflow-hidden shadow-lg">
      <img src="{{{{ page.image }}}}" alt="{{{{ page.title }}}}" loading="lazy" class="w-full h-72 object-cover"/>
    </div>
    <article class="max-w-none">
      <h1 class="text-4xl font-bold mb-6 neon-text">{{{{ page.title }}}}</h1>
      <!-- Contenu généré par GitHub Copilot -->
    </article>
  </div>
</main>"""
        
        # Sauvegarde du fichier
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Article créé : {filepath}")
        
    except Exception as e:
        print(f"Erreur : {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()