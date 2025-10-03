import os

# Liste des extensions vectorielles acceptées
vector_extensions = ['.ai', '.svg', '.eps']

# 🔧 Modifie ici le nom du fichier à analyser
file_name = 'ton_fichier.svg'  # Exemple : 'logo.ai', 'design.eps'

# Extraire l'extension du fichier
_, extension = os.path.splitext(file_name)

# Vérifier si l'extension est un format vectoriel
if extension.lower() in vector_extensions:
    print(f"✅ Le fichier '{file_name}' est au format vectoriel ({extension}).")
else:
    print(f"❌ Le fichier '{file_name}' n'est pas un format vectoriel ({extension}).")
