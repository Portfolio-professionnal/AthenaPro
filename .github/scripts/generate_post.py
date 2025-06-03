import os
from datetime import datetime
import random

TOPICS = [
    {
        "title": "5 tendances portfolio pour 2025",
        "category": "Design",
        "excerpt": "Découvrez les dernières tendances en matière de design de portfolio",
        "image": "https://i.postimg.cc/W3THdGdS/PORTFOLIO.webp"
    },
    {
        "title": "Comment optimiser votre landing page",
        "category": "Marketing",
        "excerpt": "Les meilleures pratiques pour une landing page qui convertit",
        "image": "https://i.postimg.cc/J7XCT9yk/article-Athenapro.png"
    }
]

def main():
    # Créer le dossier _posts si nécessaire
    os.makedirs('_posts', exist_ok=True)
    
    # Choisir un sujet aléatoire
    topic = random.choice(TOPICS)
    
    # Créer le nom du fichier
    date = datetime.now().strftime('%Y-%m-%d')
    filename = f"{date}-{topic['title'].lower().replace(' ', '-')}.md"
    filepath = os.path.join('_posts', filename)
    
    # Créer le contenu
    content = f"""---
layout: post
title: "{topic['title']}"
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S +0100')}
category: "{topic['category']}"
excerpt: "{topic['excerpt']}"
image: "{topic['image']}"
---

<main class="pt-24 pb-16 bg-[#0A0118] text-white font-serif">
  <div class="container mx-auto px-4 max-w-4xl">
    <div class="mb-10 rounded-xl overflow-hidden shadow-lg">
      <img src="{{{{ page.image }}}}" alt="{{{{ page.title }}}}" loading="lazy" class="w-full h-72 object-cover"/>
    </div>
    <article class="max-w-none">
      <h1 class="text-4xl font-bold mb-6 neon-text">{{{{ page.title }}}}</h1>
      <!-- Contenu de l'article -->
    </article>
  </div>
</main>"""
    
    # Sauvegarder le fichier
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    main()