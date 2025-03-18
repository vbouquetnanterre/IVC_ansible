# Gestion de configuration avec ansible

Ce document est accompagné d'un atelier qui est disponible sur coursenligne [https://coursenligne.parisnanterre.fr/course/view.php?id=8175#section-5](https://coursenligne.parisnanterre.fr/course/view.php?id=8175#section-5)

## Configurations nécessaires pour les exercices

Il est nécessaire, sur le système d'exploitation que vous utilisez, que soit installé:

<!-- - vagrant [https://www.vagrantup.com/](https://www.vagrantup.com/) -->
- ansible [https://docs.ansible.com/](https://docs.ansible.com/). Nous vous recommandons d'installer aussi `ansible-lint` permettant l'analyse statique de fichier de configuration ansible. Voici la commande pour l'installer: `pip3 install ansible-lint`. Si vous utilisez vscode, vous pouvez installer l'extension "ansible" de Red Hat afin de permettre le support du language utilisé dans les fichiers de configuration ansible. Il est aussi possible d'installer le module docker afin de construire et déployer des conteneurs sur la machine invitée. Voici la commande pour le faire: `ansible-galaxy collection install community.docker:2.7.9`
- virtualbox [https://www.virtualbox.org/](https://www.virtualbox.org/)

Vous pouvez télécharger sur coursenligne les dépendances nécessaire pour réaliser les exercices ou récupérer ces dépendances depuis le dépot disponible sur github. Ces dépendances contiennent notamment:

<!-- - un fichier `Vagrantfile` qui servira à déployer la machine virtuelle -->
- un fichier `hosts` qui permettra à ansible d'accéder à la machine à configurer (la machine virtuelle Virtualbox)
- un fichier `ansible.cfg` qui indiquera, notamment, l'utilisateur et sa clef privée permettant à ansible de se connecter à la machine virtuelle avec ssh
- un fichier `install_docker_podman.yaml` qui est un "playbook" ansible afin d'installer les dépendances nécessaires pour utiliser des conteneurs (docker, podman)

### Si vous travaillez dans une machine virtuelle déployée avec Virtualbox

Référez-vous au TP chroot pour le partage de dossier (si vous en avez besoin), la sélection de l'iso et la redirection de ports. Il faudra notamment rediriger le 22 de l'invité vers le port 2222 de l'hôte.

Voici les commandes à exécuter dans la machine virtuelle déployée avec virtualbox:
```bash
sudo su
cd /mnt/
# Si vous souhaitez configurer un répertoire partagé, cf. tp chroot
mkdir -p partage && sudo mount -t vboxsf partage partage
```

### Configuration de ssh et du root
Pour permettre à ansible d'exécuter des tâches dans la machine virtuelle, nous devons configurer l'accès à ssh. Pour cela, nous allons: générer une clef publique et une clef privée afin de permettre la connexion à ssh sans saisir un mot de passe. Pour cela, nous devons enregistrer la clef publique dans la fichier de configuration ssh de l'utilisateur de la machine virtuelle.

```bash
# Génération de la clef publique et de la clef publique
# Note: la phrase secrète est vide, ceci n'est pas recommandé pour la mise en production mais facilite la configuration pour ce TP
# Terminal hôte (votre machine):
cd /home/<utilisateur_hote>/.ssh/
ssh-keygen -t rsa -b 4096 -f id_rsa_ansible -N ""

# Vérifier que vous avez bien deux fichiers "id_rsa_ansible" et id_rsa_ansible.pub contenant, respectivement, la clef privée et la clef publique

# Copie de la clef ssh publique dans la machine virtuelle
# Terminal hôte
ssh-copy-id -i id_rsa_ansible.pub -p 2222 <utilisateur_vm>@localhost

# Hote: vérifions que ça fonctionne, normalement aucun mot de passe ne vous sera demandé
ssh -p 2222 <utilisateur_vm>@localhost

# Ajouter le chemin du la clef privé au fichier ansible.fg
# private_key_file = /home/<utilisateur_hote>/.ssh/id_rsa_ansible # chemin de la clef privée sur votre machine:

# Tester ansible depuis le répertoire playbooks du dépôt git
ansible -i hosts serveurs -m ping
# Affichage attendu:
# vm_virtualbox | SUCCESS => {
#     "ansible_facts" : {
#         "discovered_interpreter_python": "/usr/bin/python3"
#     },
#     "changed": false,
#     "ping": "pong"
# }
```

Il sera aussi nécessaire pour ce TP de permettre à ansible d'exécuter des commandes en tant que root sur la machine invitée. Puisqu'elle se connecter avec l'utilisateur <utilisateur_vm>, il faut que celui-ci est les droits.

```bash
# Vérifier si votre utilisateur a les droits sudo
# Machine invitée
sudo -l -U <utilisateur_vm>
# Vous devirez voir afficher: (ALL) ALL à la fin du retour de la commande

# Si l'utilisateur n'a pas les droits sudo
groups <utilisateur_vm>
sudo usermod -aG Wheel <utilisateur_vm>
# Se déconnecter et se reconnecter
```

Afin qu'ansible n'est pas à saisir de mot de passe pour exécuter des commandes en tant que sudo:

```bash
# Machine invitée
sudo visudo

# Ajouter la ligne suivant à la fin du fichier
# <utilisateur_vm> ALL=(ALL) NOPASSWD: ALL

# L'éditeur est vim. Vous savez normalement comment sauvegarder un fichier et quitter l'éditeur
```

### Ansible, installation des dépendances

Pour construire et exécuter des conteneurs sur la machine virtuelle déployée avec vagrant, vous diposez d'un "playbook" `install_docker_podman.yml`. Vous pouvez exécuter celui-ci avec la commande suivante:

```bash
ansible-playbook -i hosts install_docker_podman.yml
```

## Préambule aux exercices

Vous devez faire un fork du dépôt qui est herbégée sur github à l'adresse suivante: [https://github.com/vbouquetnanterre/IVC_ansible](https://github.com/vbouquetnanterre/IVC_ansible)

Vous devez ensuite mettre votre dépôt en privé.

## Exercice 1:

Créez un `playbook` afin d'enregistrer le nom d'utilisateur github et le mot de passe sur la machine virtuelle déployée avec vagrant. Pour le mot de passe, vous devez générer un token depuis le site github. Voici un lien de la documentation expliquant la procédure afin de générer un token [https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

Pour enregistrer le nom d'utilisateur et le token vous pouvez configurer un fichier .gitconfig et .git-credentials qui doit être placé dans le home. Pour générer ces fichiers, utilisez le `prompt` d'ansible, le module de `copy` et le module de `template` (utilisant jinja). Voici le lien de la documentation sur le stockage des données d'authentification avec git: [https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage](https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage)

## Exercice 2

Créez un `playbook` afin de cloner ou de mettre à jour votre dépôt privé sur la machine virtuelle.

## Exercice 3

Parcourez l'application (dans le dossier app) et identifiez les différents services. Proposez une solution pour découpler les services que vous avez identifiés afin de les exécuter dans différents conteneurs. Donnez ensuite les fichiers nécessaires à la construction des images qui permettront d'exécuter les services sur des conteneurs.

## Exercice 4

Créez un `playbook` afin de construire les images des conteneurs.Vous pouvez utilisez le module `ansible.builtin.shell` afin d'exécuter directement les commandes avec le client du conteneur (docker ou podman). Vous pouvez aussi utilisez les modules communautaires de docker ou de podman.

## Exercice 5

Créez un `playbook` afin d'exécuter les conteneurs. Vérifiez ensuite que l'application fonctionne correctement en accédant à l'url localhost:PORT (selon le port que vous avez choisi, par défaut, celui-ci est 5000 pour flask). Vérifier que le port 5000 est correctement redirigé avec virtualbox.

## Exercice 6

Proposez une solution afin de rendre la base de données persistante et modifiez les fichiers nécessaires. Créez ensuite un `playbook` afin de sauvegarder la base de données toutes les heures. Pour cela, vous pouvez utiliser le module `ansible.builtin.cron`.

## Exercice 7

Créez un `playbook` afin d'installer nginx pour servir des pages statiques (html, css, png, pdf, etc.) qui seront présents dans le dossier `/www/data` à l'url `localhost:8081`. Vous pourrez ajouter les fichiers que vous souhaitez dans ce dossier. Essayez d'accéder à vos fichiers depuis le navigateur avec l'adresse `localhost:8081/nom_dun_fichier.ext`.

## Exercice Bonus 1

Créez un ou plusieurs `playbooks` afin d'exécuter les services comme si l'application était en production. Cela comprend l'utilisation de `tls/ssl` pour le chiffrement afin de pouvoir utiliser `https` mais aussi la sécurisation des informations d'authentification des différents services.

## Exercice Bonus 2

Déployez l'application en developpement et l'application en production sur deux machines virtuelles différentes en utilisant vagrant.
