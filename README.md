# Gestion de configuration avec ansible

Ce document est accompagné d'un atelier qui est disponible sur coursenligne [https://coursenligne.parisnanterre.fr/course/view.php?id=8175#section-0](https://coursenligne.parisnanterre.fr/course/view.php?id=8175#section-5)

## Configurations nécessaires pour les exercices

Il est nécessaire, sur le système d'exploitation que vous utilisez, que soit installé:

- vagrant [https://www.vagrantup.com/](https://www.vagrantup.com/)
- ansible [https://docs.ansible.com/](https://docs.ansible.com/). Il faudra aussi installer le module docker afin de construire et déployer des conteneurs sur la machine invitée. Voici la commande pour le faire: `ansible-galaxy collection install community.docker:2.7.9`
- virtualbox [https://www.virtualbox.org/](https://www.virtualbox.org/)

Vous pouvez télécharger sur coursenligne les dépendances nécessaire pour réaliser les exercices ou récupérer ces dépendances depuis le dépot disponible sur github. Ces dépendances contiennent notamment:

- un fichier `Vagrantfile` qui servira à déployer la machine virtuelle
- un fichier `hosts` qui permettra à ansible d'accéder à la machine à configurer (la machine virtuelle déployée avec vagrant)
- un fichier `ansible.cfg` qui indiquera la clef privée permettant à ansible de ssh dans la machine virtuelle déployée avec vagrant
- un fichier `install_docker_podman.yaml` qui est un "playbook" ansible afin d'installer les dépendances nécessaires pour utiliser des conteneurs (docker, podman)

### Si vous travaillez dans une machine virtuelle déployée avec Virtualbox

Référez-vous au TP chroot pour le partage de dossier, la sélection de l'iso et la redirection de ports. Il faudra notamment rediriger le 22 de l'invité vers le port 2222 de l'hôte.

Voici les commandes à exécuter dans la machine virtuelle déployée avec virtualbox (et non vagrant):
```bash
sudo su
cd ~/

# Si vous souhaitez configurer un répertoire partagé, cf. tp chroot
mkdir -p partage && sudo mount -t vboxsf partage partage
sudo chmod 600 partage
cd partage

# Il faudra placer les fichiers hosts, ansible.cfg et install_docker_podman.yml dans le dossier playbooks
mkdir playbooks

# Installation des dépendances
sudo apt update
sudo apt install vagrant virtualbox ansible ansible-lint
```

### Vagrant

Pour permettre à ansible d'exécuter des tâches dans la machine virtuelle déployée avec vagrant, il faudra récupérer le chemin du fichier de la clef privée utilisée pour ssh dans la machine:
```bash
# A exécuter une fois que la machine virtuelle est en cours d'exécution
vagrant ssh-config # regarder le champ IdentityFile pour récupérer la clef ssh qu'il faudra copier dans le fichier ansible.cfg (private_key_file)

chmod -R 600 .vagrant # pour éviter les problèmes de droits avec ansible
```

### Ansible, installation des dépendances

Pour construire et exécuter des conteneurs sur la machine virtuelle déployée avec vagrant, vous diposez d'un "playbook" `install_docker_podman.yml`. Vous pouvez exécuter celui-ci avec la commande suivante:

```bash
ansible-playbook -i hosts install_docker_podman.yml
```

## Préambule aux exercices

Vous devez faire un fork du répertoire qui est herbégée sur github à l'adresse suivante: [https://github.com/vbouquetnanterre/IVC_TP_ansible](https://github.com/vbouquetnanterre/IVC_TP_ansible)

Vous devez ensuite mettre votre répertoire en privé.

## Exercice 1:

Créer un `playbook` afin d'enregistrer le nom d'utilisateur github et le mot de passe sur la machine virtuelle déployée avec vagrant. Pour le mot de passe, vous devez générer un token depuis le site github. Voici un lien de la documentation expliquant la procédure afin de générer un token [https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

Pour enregistrer le nom d'utilisateur et le token vous pouvez configurer un fichier .gitconfig et .git-credentials qui doit être placé dans le home. Pour générer ces fichiers, utilisez le `prompt` d'ansible, le module de `copy` et le module de `template` (utilisant jinja). Voici le lien de la documentation sur le stockage des données d'authentification avec git: [https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage](https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage)

## Exercice 2

Créer un `playbook afin de cloner ou de mettre à jour votre dépôt privé sur la machine virtuelle déployée avec vagrant.

## Exercice 3

Parcourez l'application et identifiez les différents services. Proposez une solution pour découpler les services que vous avez identifiés afin de les exécuter dans différents conteneurs. Donnez ensuite les fichiers nécessaires à la construction des images qui permettront d'exécuter les services sur des conteneurs.

## Exercice 4

Créer un `playbook` afin de construire les images des conteneurs. Note: selon les versions d'ansible, il est possible que le module `community.docker`ne fonctionne pas correctement. Dans ce cas, vous pouvez utilisez le module `ansible.builtin.shell` afin d'exécuter directement les commandes avec le docker client.

## Exercice 5

Créer un `playbook` afin d'exécuter les conteneurs. Vérifiez ensuite que l'application fonctionne correctement en accédant à l'url localhost:PORT (selon le port que vous avez choisi, par défaut celui-ci est 5000 pour flask).

## Exercice 6

Proposez une solution afin de rendre la base de données persistante et modifier les fichiers nécessaires. Créer ensuite un `playbook` afin de sauvegarder la base de données toutes les heures. Pour cela, vous pouvez utiliser le module `ansible.builtin.cron`.

## Exercice 7

Créer un `playbook` afin d'installer nginx pour servir des pages statiques (html, css, png, pdf, etc.) qui seront présents dans le dossier `/www/data` à l'url `localhost:8081`. Vous pourrez ajouter les fichiers que vous souhaitez dans ce dossier.

## Exercice 8

Créer un ou plusieurs `playbooks` afin d'exécuter les services comme si l'application était en production. Cela comprend l'utilisation de `tls/ssl` pour le chiffrement afin de pouvoir utiliser `https` mais aussi la sécurisation des informations d'authentification des différents services.

## Exercice 9

Déployez l'application en developpement et l'application en production sur deux machines virtuelles différentes en utilisant vagrant.

