import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--arg1")
parser.add_argument("--arg2")
args = parser.parse_args()

print(f"Step1 - Arg1: {args.arg1}")
print(f"Step1 - Arg2: {args.arg2}")

