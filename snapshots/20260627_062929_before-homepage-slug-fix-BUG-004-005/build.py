#!/usr/bin/env python3
import json, os, shutil, sys

def build():
    pages_path = 'data/pages.json'
    if not os.path.exists(pages_path):
        print("ERROR: pages.json not found")
        sys.exit(1)
    with open(pages_path, 'r') as f:
        pages = json.load(f)
    with open('theme/base.html', 'r') as f:
        template = f.read()
    if os.path.exists('build'):
        shutil.rmtree('build')
    os.makedirs('build')
    for page in pages:
        slug = page['slug']
        content = page.get('body_content', '')
        title = page.get('title') or 'Nidd Valley BP'
        og_title = page.get('og_title') or title
        meta_description = page.get('meta_description', '')
        canonical_url = page.get('canonical_url') or (f"https://niddvalleybp.co.uk/{slug}/" if slug else "https://niddvalleybp.co.uk/")
        location_name = page.get('location_name') or 'Yorkshire'
        html = template
        html = html.replace('{{ title }}', title)
        html = html.replace('{{ og_title }}', og_title)
        html = html.replace('{{ meta_description }}', meta_description)
        html = html.replace('{{ canonical_url }}', canonical_url)
        html = html.replace('{{ location_name }}', location_name)
        html = html.replace('{{ content }}', content)
        out_dir = os.path.join('build', slug) if slug else 'build'
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, 'index.html'), 'w') as f:
            f.write(html)
    if os.path.exists('assets'):
        shutil.copytree('assets', 'build/assets', dirs_exist_ok=True)
    print(f"Built {len(pages)} pages")

if __name__ == '__main__':
    build()
