import sys
import os
import site

print(f"Executable: {sys.executable}")
print(f"Prefix: {sys.prefix}")
print(f"Base Prefix: {getattr(sys, 'base_prefix', 'N/A')}")
print(f"Version: {sys.version}")
print("Sys.path:")
for p in sys.path:
    print(f"  {p}")

print("\nSite packages:")
for p in site.getsitepackages():
    print(f"  {p}")

try:
    import fastapi
    print(f"\nFastAPI found at: {fastapi.__file__}")
except ImportError as e:
    print(f"\nFastAPI import failed: {e}")
