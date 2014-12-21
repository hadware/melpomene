voxpopuli
=========

Un synthétiseur de texte basé sur le service web de Voxygen (et sur son petit reverse opéré par [tibounise](https://github.com/tibounise/PHP-Voxygen) sur Github et [mGeek](http://mgeek.fr/) sur la toile).

Dépendances
===

Pydub : il suffit de l'installer avec pydub avec:

    pip install pydub

Pydub nécessite ffmpeg (ou avconv pour ceux qui sont dans le vent). On l'installe avec:

    # libav
    apt-get install libav-tools libavcodec-extra-53
    # OU
    # ffmpeg
    apt-get install ffmpeg libavcodec-extra-53

Fonctionnement
===

On utilise le script en CLI, les paramètres sont le texte d'entrée (un dialogue), et le nom du fichier de sortie.
La commande est donc de la forme
    ./voxpopuli FILE [OUTPUT FILE] | --voices
Soit donc par exemple
    ./voxpopuli texte.txt rendu.ogg

Nota Bene:
 * Le rendu sonore est pour l'instant uniquement exportable en OGG avec codec vorbis.
 * Si le fichier de sortie n'est pas spécifié, c'est un fichier avec un hash MD5 qui est copié.
 * l'option --voices (passée seule en paramètre) permet de voir les voix disponibles

Si vous avez lu jusqu'ici, c'est probablement que vous voulez savoir comment on formate un dialogue pour le programme. C'est très simple: on spécifie une voix, puis la ligne qu'elle devra "lire". Par exemple:
    JeanJean : Eh bien, il fait sacrament froid ici!

Un dialogue est une suite de "répliques" des voix. Tant qu'une voix ne termine pas sa réplique, *il ne faut pas* sauter de ligne (au risque de voir le parser un peu simplet du script péter les plombs). Inutile aussi de mettre des guillemets pour signifier le début et fin d'une réplique!
Aller, un petit exemple de dialogue pour voir:

    Loic : Salut toto!
    Robot : Salut tata!
    Yeti : Salut titi!
    Zozo : Mais fermez vos putains de gueule bordel

(Notez que certains mots sont censurés par le service, mais que je ne tarderai pas à implémenter le fameux Grommofilter de tibounise)