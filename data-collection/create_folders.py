import os
import sys

 
if len(sys.argv) < 2:
    print("Usage: python3 file.py <command>")
    sys.exit(1)
    
PID = sys.argv[1]

print(f"creating folders for PID {PID}")
base_dir = f"FD-data/{PID}"

folders = {
    "ADLs": ["LOB1", "LOB2", "RS", "SBS", "SIT", "SSS1", "SSS2", "SSW", "SWW1", "SWW2", "TWC1", "TWC2", "WAT", "WSS1", "WSS2"],
    "Falls": ["FFAS", "FFTSIT2", "FFT1", "FFT2", "FFTSIT1", "FHO1", "FHO2", "FWW", "FFSIT1", "FFSIT2"]
}

for category, subfolders in folders.items():
    category_path = os.path.join(base_dir, category)
    os.makedirs(category_path, exist_ok=True)
    for subfolder in subfolders:
        subfolder_path = os.path.join(category_path, subfolder)
        os.makedirs(subfolder_path, exist_ok=True)

