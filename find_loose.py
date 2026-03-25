import os
import zlib

def main():
    objects_dir = '.git/objects'
    loose_objects = []
    
    for root, dirs, files in os.walk(objects_dir):
        # Skip info and pack directories
        if os.path.basename(root) in ['info', 'pack']:
            continue
            
        for file in files:
            filepath = os.path.join(root, file)
            # Skip non-object files
            if len(file) != 38 or len(os.path.basename(root)) != 2:
                continue
                
            try:
                size = os.path.getsize(filepath)
                sha = os.path.basename(root) + file
                loose_objects.append((sha, size, filepath))
            except Exception:
                pass

    loose_objects.sort(key=lambda x: x[1], reverse=True)
    
    print(f"Total loose objects found: {len(loose_objects)}")
    if not loose_objects:
        return

    objects_map = {}
    if os.path.exists('objects.txt'):
        with open('objects.txt', 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                parts = line.strip().split(' ', 1)
                if len(parts) == 2:
                    objects_map[parts[0]] = parts[1]

    print("\nLargest 30 loose objects:")
    total_large_size = 0
    for sha, size, filepath in loose_objects[:30]:
        name = objects_map.get(sha, "Unknown Object")
        mb_size = size / (1024*1024)
        total_large_size += mb_size
        print(f"{mb_size:.2f} MB - {name} ({sha})")
    
    print(f"\nTotal size of these top 30 loose objects: {total_large_size:.2f} MB")

if __name__ == '__main__':
    main()
