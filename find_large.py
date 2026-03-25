import os
import subprocess

def main():
    objects = {}
    with open('objects.txt', 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            parts = line.strip().split(' ', 1)
            if len(parts) == 2:
                objects[parts[0]] = parts[1]

    pack_dir = '.git/objects/pack'
    pack_files = [f for f in os.listdir(pack_dir) if f.endswith('.idx')]
    if not pack_files:
        print("No pack files found.")
        return

    pack_path = os.path.join(pack_dir, pack_files[0])
    print(f"Reading pack file: {pack_path}")
    
    vpack = subprocess.check_output(f'git verify-pack -v {pack_path}', shell=True, text=True, errors='ignore')
    
    pack_sizes = []
    for line in vpack.strip().split('\n'):
        parts = line.split()
        if len(parts) >= 3 and parts[1] in ('blob', 'tree', 'commit', 'tag'):
            size = int(parts[2])
            pack_sizes.append((parts[0], size))
    
    pack_sizes.sort(key=lambda x: x[1], reverse=True)
    
    print("\nLargest 30 objects:")
    total_large_size = 0
    for sha, size in pack_sizes[:30]:
        name = objects.get(sha, "Unknown")
        mb_size = size / (1024*1024)
        total_large_size += mb_size
        print(f"{mb_size:.2f} MB - {name} ({sha})")
    
    print(f"\nTotal size of these top 30 objects: {total_large_size:.2f} MB")

if __name__ == '__main__':
    main()
