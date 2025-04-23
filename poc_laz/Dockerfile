FROM ubuntu:22.04

# Éviter les interactions pendant l'installation
ENV DEBIAN_FRONTEND=noninteractive

# Installation des dépendances de base
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    software-properties-common \
    blender \
    ninja-build \
    cmake \
    libeigen3-dev \
    libgdal-dev \
    wget \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Ajouter le PPA UbuntuGIS
RUN add-apt-repository -y ppa:ubuntugis/ppa && apt-get update

# Installation de PDAL (vérification version récente ou installation depuis source)
RUN apt-get install -y --no-install-recommends \
        git clang && \
        git clone https://github.com/PDAL/PDAL.git /tmp/PDAL && \
        cd /tmp/PDAL && \
        git checkout 2.6.0 && \
        mkdir build && cd build && \
        cmake .. && make && make install && \
        ldconfig && \
        rm -rf /tmp/PDAL

# Installation des dépendances Python
RUN pip3 install numpy pdal
RUN pip3 install scipy

# Créer le répertoire de travail
WORKDIR /app

# Copier les scripts
COPY laz_to_fbx_converter.py .
COPY blender_script.py .

# Créer le répertoire pour les données
RUN mkdir /data

# Définir le volume pour les données
VOLUME ["/data"]
VOLUME ["/app"]

# Commande par défaut
CMD ["python3", "laz_to_fbx_converter.py"]
