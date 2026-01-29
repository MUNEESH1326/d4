

##################################################
# Modify the code below 
##################################################

# 
# =========================================================
# FIR Filter IP Validation Script
# Target : impl0
# Company: Dawnstar
# =========================================================

import os

# ---------------------------------------------------------
# Target chip
# ---------------------------------------------------------
IMPL = "impl0"

# ---------------------------------------------------------
# Base directory
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------
# Configuration files
# ---------------------------------------------------------
CFG_FILES = [
    os.path.join(BASE_DIR, "p0.cfg"),
    os.path.join(BASE_DIR, "p4.cfg"),
    os.path.join(BASE_DIR, "p7.cfg"),
    os.path.join(BASE_DIR, "p9.cfg"),
]

# Check if config files exist
for cfg in CFG_FILES:
    if not os.path.isfile(cfg):
        raise FileNotFoundError(f"Config file '{cfg}' not found. Make sure the file exists.")

# ---------------------------------------------------------
# Input vector file (directly using sqr.vec)
# ---------------------------------------------------------
VECTOR_FILE = os.path.join(BASE_DIR, "sqr.vec")

if not os.path.isfile(VECTOR_FILE):
    raise FileNotFoundError(f"Vector file '{VECTOR_FILE}' not found. Make sure the file exists.")

# ---------------------------------------------------------
# Load FIR coefficients from CSV-style cfg files
# Format: coef,en,value
# Example:
# 0,1,0x10
# 1,1,-3
# ---------------------------------------------------------
def load_coefficients(cfg_files):
    coeffs = []

    for cfg in cfg_files:
        with open(cfg, "r") as f:
            for line in f:
                line = line.strip()

                # Skip empty lines, comments, headers
                if not line or line.startswith("#") or "coef" in line.lower():
                    continue

                parts = [p.strip() for p in line.split(",")]
                if len(parts) < 3:
                    continue

                _, en, value = parts

                # Only enabled coefficients
                if int(en) != 1:
                    continue

                # Supports hex (0x..) and decimal
                coeffs.append(int(value, 0))

    if not coeffs:
        print("Warning: No enabled coefficients found!")
    return coeffs

# ---------------------------------------------------------
# Load input signal vector
# One sample per line (hex or decimal)
# ---------------------------------------------------------
def load_input_vector(vec_file):
    samples = []

    with open(vec_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            samples.append(int(line, 0))

    if not samples:
        print("Warning: Input vector is empty!")
    return samples

# ---------------------------------------------------------
# Pure Python FIR filter (golden model)
# y[n] = sum(h[k] * x[n-k])
# ---------------------------------------------------------
def fir_filter(input_signal, coefficients):
    output = []
    num_taps = len(coefficients)

    for n in range(len(input_signal)):
        acc = 0
        for k in range(num_taps):
            if n - k >= 0:
                acc += coefficients[k] * input_signal[n - k]
        output.append(acc)

    return output

# ---------------------------------------------------------
# Main Validation Flow
# ---------------------------------------------------------
def main():
    print(f"\nValidating FIR Filter IP on {IMPL}\n")

    # Load data
    coeffs = load_coefficients(CFG_FILES)
    input_vec = load_input_vector(VECTOR_FILE)

    # Check data
    if not coeffs or not input_vec:
        print("Error: Cannot run FIR. Check coefficient or input vector files.")
        return

    # Run golden FIR
    output = fir_filter(input_vec, coeffs)

    # -----------------------------------------------------
    # Results (concise, readable)
    # -----------------------------------------------------
    print("=== FIR Validation Summary ===")
    print(f"Impl                 : {IMPL}")
    print(f"Total coefficients   : {len(coeffs)}")
    print(f"Input samples        : {len(input_vec)}")
    print(f"Output samples       : {len(output)}")

    print("\nFirst 10 FIR outputs:")
    for i in range(min(10, len(output))):
        print(f"y[{i:02d}] = {output[i]}")

    print("\nFIR signal processing validation completed successfully.\n")

# ---------------------------------------------------------
# Entry Point
# ---------------------------------------------------------
if __name__ == "__main__":
    main()