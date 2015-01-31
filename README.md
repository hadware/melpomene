voxpopuli
=========

Un synthétiseur de dialogues basé sur le service web de Voxygen (et sur son petit reverse opéré par [tibounise](https://github.com/tibounise/PHP-Voxygen) sur Github et [mGeek](http://mgeek.fr/) sur la toile). Le fonctionnement est simple: on donne en entrée un dialogue dans lequel plusieurs voix "parlent", et le programme transforme ce dialogue textuel en dialogue audio en utilisant le service de Voxygen (et bientôt d'Acapela).

## Dépendances

Pydub : il suffit de l'installer avec pydub avec:

    sudo pip install pydub

Pydub nécessite ffmpeg (ou avconv pour ceux qui sont dans le vent). On l'installe avec:

    # libav
    sudo apt-get install libav-tools libavcodec-extra-53
    # OU
    # ffmpeg
    sudo apt-get install ffmpeg libavcodec-extra-53

## Fonctionnement

On utilise le script en CLI ou avec une GUI GTK3+, les paramètres sont le texte d'entrée (un dialogue), et le nom du fichier de sortie.
La commande est donc de la forme

    ./voxpopuli.py FILE [OUTPUT FILE] | --voices
    ./gui.py

Soit donc par exemple

    ./voxpopuli texte.txt rendu.ogg

Notes:
 * Le rendu sonore est pour l'instant uniquement exportable en OGG avec codec vorbis.
 * Si le fichier de sortie n'est pas spécifié, c'est un fichier avec un nom en hash MD5 qui est copié.
 * l'option --voices (passée seule en paramètre) permet de voir les voix disponibles
 * L'interface graphique nécessite GTK3+ et Gstreamer1.0. A priori pour un ubuntu ou un environnement gnome assez récent, ça devrait déjà être là. Pour le reste, inch'allah.

Si vous avez lu jusqu'ici, c'est probablement que vous voulez savoir comment on formatte un dialogue pour le programme. C'est très simple: on spécifie une voix, puis la ligne qu'elle devra "lire". Par exemple:

    JeanJean : Eh bien, il fait sacrament froid ici!

Un dialogue est une suite de "répliques" des voix. Tant qu'une voix ne termine pas sa réplique, *il ne faut pas* sauter de ligne (au risque de voir le parser un peu simplet du script péter les plombs). Inutile aussi de mettre des guillemets pour signifier le début et fin d'une réplique!
Aller, un petit exemple de dialogue pour voir:

    Loic : Salut toto!
    Robot : Salut tata!
    Yeti : Salut titi!
    Zozo : Mais fermez vos putains de gueule bordel

(Notez que certains mots sont censurés par le service, mais que je ne tarderai pas à implémenter le fameux Grommofilter de tibounise)

## Notes Légales (lol)
L'utilisation de voxpopuli doit se faire uniquement dans le but d'évaluer les services proposés par [Voxygen SAS](http://voxygen.fr), conformément aux [mentions légales](http://voxygen.fr/fr/content/mentions-legales) du démonstrateur de Voxygen.

Les fichiers audio produits par Voxygen SAS sont protégés par le droit d'auteur, et ne doivent pas être diffusés sans l'autorisation de Voxygen SAS.

Voxpopuli a été développé en toute indépendance de Voxygen SAS, et n'est pas affilié à Voxygen SAS.

*Toutes ressemblances de ces notes à celles de PHP-voxygen sont fortuites.*

