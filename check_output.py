import os

content_dir = 'content'
for fname in sorted(os.listdir(content_dir)):
    if fname.endswith('.js'):
        fpath = os.path.join(content_dir, fname)
        size = os.path.getsize(fpath)
        with open(fpath, 'r', encoding='utf-8') as f:
            first_200 = f.read(200)
        print(f"{fname}: {size:,} bytes")
