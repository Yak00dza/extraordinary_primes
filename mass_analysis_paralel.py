import os
import subprocess
import tempfile
from pathlib import Path

INPUT = "curves_noniso_l.txt"
N_PROCESSES = 11

def main():
    with open(INPUT, "r") as f:
        curves = f.readlines()

    chunks = [
        curves[i::N_PROCESSES]
        for i in range(N_PROCESSES)
    ]

    processes = []

    for i, chunk in enumerate(chunks):
        tmp = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".txt",
            delete=False
        )
        tmp.writelines(chunk)
        tmp.close()

        log = open(f"worker_{i}.log", "w")

        p = subprocess.Popen(
            ["python", "-u", "mass_analysis.py", tmp.name],
            stdout=log,
            stderr=subprocess.STDOUT
        )

        processes.append((p, tmp.name, log))

    # Wait for all workers
    for p, tmp, log in processes:
        p.wait()
        log.close()
        os.remove(tmp)

if __name__ == "__main__":
    main()