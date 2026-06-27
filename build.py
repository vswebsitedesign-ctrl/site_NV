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
    canonical_urls = []
    for page in pages:
        slug = page['slug']
        content = page.get('body_content', '')
        title = page.get('title') or 'Nidd Valley BP'
        og_title = page.get('og_title') or title
        meta_description = page.get('meta_description', '')
        canonical_url = page.get('canonical_url') or ("https://niddvalleybp.co.uk/" if slug in ('', 'index') else f"https://niddvalleybp.co.uk/{slug}/")
        location_name = page.get('location_name') or 'Yorkshire'
        canonical_urls.append(canonical_url)
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
    # LOCATION PAGES — generated from data/locations.json + theme/location.html
    if os.path.exists('data/locations.json') and os.path.exists('theme/location.html'):
        with open('data/locations.json') as f:
            locations = json.load(f)
        with open('theme/location.html') as f:
            loc_template = f.read()
        loc_count = 0
        for loc in locations:
            slug = loc['slug']
            ln = loc['location_name']
            blurbs = loc.get('service_blurbs', {})
            nearby_pills = ''.join(f'<span class="location-pill">{n}</span>\n      ' for n in loc.get('nearby', []))
            canonical_url = f"https://niddvalleybp.co.uk/{slug}/"
            loc_html = loc_template
            loc_html = loc_html.replace('{{ location_name }}', ln)
            loc_html = loc_html.replace('{{ intro_para_1 }}', loc.get('intro_para_1', ''))
            loc_html = loc_html.replace('{{ intro_para_2 }}', loc.get('intro_para_2', ''))
            loc_html = loc_html.replace('{{ blurb_repointing }}', blurbs.get('repointing', ''))
            loc_html = loc_html.replace('{{ blurb_masonry_repairs }}', blurbs.get('masonry_repairs', ''))
            loc_html = loc_html.replace('{{ blurb_stonework }}', blurbs.get('stonework', ''))
            loc_html = loc_html.replace('{{ blurb_chimney_repairs }}', blurbs.get('chimney_repairs', ''))
            loc_html = loc_html.replace('{{ blurb_wall_restoration }}', blurbs.get('wall_restoration', ''))
            loc_html = loc_html.replace('{{ blurb_damp_repairs }}', blurbs.get('damp_repairs', ''))
            loc_html = loc_html.replace('{{ blurb_pointing_styles }}', blurbs.get('pointing_styles', ''))
            loc_html = loc_html.replace('{{ blurb_mortar_lime }}', blurbs.get('mortar_lime', ''))
            loc_html = loc_html.replace('{{ blurb_commercial }}', blurbs.get('commercial', ''))
            loc_html = loc_html.replace('{{ nearby_pills }}', nearby_pills)
            # wrap in base.html
            title = loc.get('title') or f"Repointing & Brickwork in {ln} | Nidd Valley BP"
            page_html = template
            page_html = page_html.replace('{{ title }}', title)
            page_html = page_html.replace('{{ og_title }}', f"Repointing & Brickwork in {ln}")
            page_html = page_html.replace('{{ meta_description }}', loc.get('meta_description', f"Expert repointing and brickwork services in {ln}, Yorkshire. Free no-obligation quotes from Darren at Nidd Valley Building Preservation."))
            page_html = page_html.replace('{{ canonical_url }}', canonical_url)
            page_html = page_html.replace('{{ location_name }}', ln)
            page_html = page_html.replace('{{ content }}', loc_html)
            out_dir = os.path.join('build', slug)
            os.makedirs(out_dir, exist_ok=True)
            with open(os.path.join(out_dir, 'index.html'), 'w') as f:
                f.write(page_html)
            canonical_urls.append(canonical_url)
            loc_count += 1
        print(f"Built {loc_count} location pages from locations.json")

    if os.path.exists('assets'):
        shutil.copytree('assets', 'build/assets', dirs_exist_ok=True)
    # Homepage fix: engine writes 'index' slug to build/index/index.html
    # but site root must serve build/index.html — copy automatically per
    # Master Report known_issues.homepage_slug rule, every build.
    index_src = os.path.join('build', 'index', 'index.html')
    if os.path.exists(index_src):
        shutil.copy(index_src, os.path.join('build', 'index.html'))
        print("Homepage: copied build/index/index.html -> build/index.html")
    # BUG-007: sitemap.xml generated from same canonical_urls collected above
    sitemap_urls = ''.join(f'  <url><loc>{u}</loc></url>\n' for u in sorted(set(canonical_urls)))
    sitemap_xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap_urls}</urlset>\n'
    with open(os.path.join('build', 'sitemap.xml'), 'w') as f:
        f.write(sitemap_xml)
    # BUG-008: robots.txt referencing the sitemap
    robots_txt = "User-agent: *\nAllow: /\n\nSitemap: https://niddvalleybp.co.uk/sitemap.xml\n"
    with open(os.path.join('build', 'robots.txt'), 'w') as f:
        f.write(robots_txt)
    print(f"Built {len(pages)} pages, sitemap.xml ({len(set(canonical_urls))} URLs), robots.txt")

if __name__ == '__main__':
    build()
