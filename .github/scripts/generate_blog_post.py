def get_copilot_suggestion(prompt):
    """Obtient une suggestion de GitHub Copilot via CLI."""
    try:
        # Ajout d'un délai pour s'assurer que Copilot est prêt
        import time
        time.sleep(2)
        
        result = subprocess.run(
            ['gh', 'copilot', 'suggest', '--timeout', '30'],
            input=prompt.encode('utf-8'),
            capture_output=True,
            text=True
        )
        
        # Si la commande échoue mais produit une sortie, on utilise quand même la sortie
        if result.stdout:
            return result.stdout.strip()
        
        # Si pas de sortie mais une erreur, on lève l'erreur
        if result.returncode != 0:
            print(f"Sortie d'erreur : {result.stderr}")
            result.check_returncode()
            
        return ""
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur Copilot CLI : {e}")
        print(f"Sortie d'erreur : {e.stderr}")
        raise

def generate_article_metadata():
    """Génère les métadonnées de l'article avec Copilot."""
    existing_titles = read_existing_titles()
    titles_list = "\n".join(f"- {title}" for title in existing_titles)

    prompt = f"""
    Generate a new blog post metadata for AthenaPro website.
    Context: AthenaPro is a service for creating professional landing pages and portfolios
    using HTML, CSS, and Tailwind, targeting freelancers and young graduates.

    Existing titles:
    {titles_list}

    Return ONLY a JSON object with the following structure:
    {{
        "title": "A catchy and unique title",
        "category": "Tips",
        "excerpt": "A persuasive short description",
        "image_url": "https://i.postimg.cc/relevant-image-url",
        "keywords": ["keyword1", "keyword2", "keyword3"]
    }}
    """

    for attempt in range(3):  # Tentatives multiples
        try:
            response = get_copilot_suggestion(prompt)
            if response:
                return extract_json_from_response(response)
        except Exception as e:
            print(f"Tentative {attempt + 1} échouée : {e}")
            if attempt == 2:  # Dernière tentative
                raise
            time.sleep(2)  # Attente entre les tentatives

    raise Exception("Impossible d'obtenir une réponse valide de Copilot après 3 tentatives")
