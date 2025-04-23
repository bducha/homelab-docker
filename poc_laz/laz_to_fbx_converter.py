import pdal
import numpy as np
import json
import os
import subprocess
from pathlib import Path

class LazToFbxConverter:
    def convert_laz_to_xyz(self, input_path: str, output_path: str):
        # Définir le pipeline PDAL pour lire le fichier LAZ
        pipeline_json = {
            "pipeline": [
                input_path,
                # {
                #     "type": "filters.decimation",
                #     "step": 10  # Réduire le nombre de points pour le prototype
                # },
                {
                    "type":"filters.range",
                    "limits":"Classification[2:2]"
                },
                {
                    "type": "writers.text",
                    "filename": output_path,
                    "write_header": False,
                    "format":"csv",
                    "order":"X,Y,Z",
                }
            ]
        }
        
        # Exécuter le pipeline
        pipeline = pdal.Pipeline(json.dumps(pipeline_json))
        pipeline.execute()

def main():
    input_file = "/data/input.laz"
    intermediate_file = "/data/points.xyz"
    output_file = "/data/output.fbx"
    
    # # Convertir LAZ en XYZ
    # converter = LazToFbxConverter()
    # print("Converting LAZ to XYZ...")
    # converter.convert_laz_to_xyz(input_file, intermediate_file)
    
    # Utiliser Blender pour convertir XYZ en FBX
    subprocess.run([
        "blender", 
        "--background",
        "--python", 
        "blender_script.py",
        "--", 
        intermediate_file,
        output_file
    ])

if __name__ == "__main__":
    main()