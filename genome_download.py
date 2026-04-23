import os
import json
import glob
import argparse
import requests
import gzip
import shutil
from joblib import Parallel, delayed

parse = argparse.ArgumentParser()
parse.add_argument("-t", "--threads", help="number of threads to use", required=False)
args = parse.parse_args()

threads = int(args.threads) if args.threads else 1

os.makedirs("genomes", exist_ok=True)

def genome_download(species, genome):
    print(species)

    ID = genome.split('.')[0].split('_')[1]
    ID1 = ID[:3]
    ID2 = ID[3:6]
    ID3 = ID[6:9]

    assembly_name = species_assembly_name[species]

    url = f"https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/{ID1}/{ID2}/{ID3}/{genome}_{assembly_name}/{genome}_{assembly_name}_genomic.fna.gz"

    gz_path = f"genomes/{genome}_{assembly_name}_genomic.fna.gz"
    fasta_path = f"genomes/{species}-{genome}_{assembly_name}_genomic.fasta"

    try:
        r = requests.get(url, stream=True, timeout=60)

        if r.status_code != 200:
            print(f"Oops, {species} genome not available")
            print(f"URL attempted: {url}")
            return

        with open(gz_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        # decompress
        with gzip.open(gz_path, 'rb') as f_in:
            with open(fasta_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        os.remove(gz_path)

        print(f"Downloaded: {fasta_path}")

    except Exception as e:
        print(f"Failed for {species}")
        print(url)
        print(e)


species_genomeID = {}
species_assembly_name = {}

with open("genomes.csv") as f:
    for line in f:
        species, GCA, assemb_name = line.strip().split(",")
        species_genomeID[species] = GCA
        species_assembly_name[species] = assemb_name

Parallel(n_jobs=threads)(
    delayed(genome_download)(k, v) for k, v in species_genomeID.items()
)