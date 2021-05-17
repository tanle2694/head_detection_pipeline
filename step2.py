import argparse
from utils import use_k8s_secret
parser = argparse.ArgumentParser()
parser.add_argument("--arg1")
parser.add_argument("--arg2")
args = parser.parse_args()

print(f"Step2 - Arg1: {args.arg1}")
print(f"Step2 - Arg2: {args.arg2}")

