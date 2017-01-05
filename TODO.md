## Intégrer un support pour d'autres sources de TTS en ligne

 * NeoSpeech
 * iVona
 * Acapela
 * AT&T Natural voices
 * CereProc Voices

## Paralléliser la récupération de l'audio en passant en multithread/sur async
Le problème étant la cohabitation entre l'eventloop de GTKLib et celle de python...

## Intégrer une sauvegarde en .zip du fichier sonore
Nécessitera aussi probablement d'arrêter de sauvergarder directement le MP3 lors de sa réception, et de le manipuler en mémoire comme un objet byte
