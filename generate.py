#!/usr/bin/env python3
"""Índice de HTML/PDF. Python 3.9+, sin dependencias. Ejecutar desde cualquier carpeta."""
import argparse
from collections import defaultdict
from html import escape
from pathlib import Path
import re
from urllib.parse import quote

# Personalización: se excluyen carpetas por nombre, a cualquier profundidad.
EXCLUDED_DIRS = {'tools', 'scripts', 'assets', 'static', 'images', 'img', 'css', 'js',
                 'node_modules', 'vendor', 'venv', '__pycache__', 'tests', 'test',
                 'dist', 'build', '_site', 'coverage', 'outputs', 'work'}
EXCLUDED_FILES = {'index.html', 'index.htm', '404.html', 'readme.html', 'license.html'}
EXTENSIONS = {'.html': 'App HTML', '.htm': 'App HTML', '.pdf': 'PDF'}
PREFIXES = {'cinema': 'Cinemática', 'festat': 'Estática de fluidos'}
TITLE = 'Mecánica de fluidos'


def readable(name):
    """Conserva siglas y números; separa guiones y guiones bajos."""
    text = re.sub(r'[-_]+', ' ', name).strip()
    return text[:1].upper() + text[1:]


def file_title(path):
    stem = path.stem
    for prefix, label in PREFIXES.items():
        if stem.lower().startswith(prefix + '-'):
            return label + ' · ' + readable(stem[len(prefix) + 1:])
    return readable(stem)


def scan(root):
    groups = defaultdict(list)
    for path in sorted(root.rglob('*'), key=lambda p: p.as_posix().casefold()):
        rel = path.relative_to(root)
        if any(part.startswith('.') or part.lower() in EXCLUDED_DIRS for part in rel.parts[:-1]):
            continue
        if path.is_symlink() or any((root / parent).is_symlink() for parent in rel.parents):
            continue
        if not path.is_file() or path.name.startswith('.'):
            continue
        if path.name.lower() in EXCLUDED_FILES or path.suffix.lower() not in EXTENSIONS:
            continue
        groups[rel.parent.as_posix()].append(rel)
    return groups


def generate(root):
    groups = scan(root)
    folders = sorted((p for p in groups if p != '.'), key=str.casefold)
    anchors = {folder: f'carpeta-{i}' for i, folder in enumerate(folders, 1)}
    parts = []
    if folders:
        cards = ''.join(
            f'<a class="card folder" href="#{anchors[folder]}"><span class="badge">▤ Carpeta</span>'
            f'<h3>{escape(" / ".join(readable(p) for p in folder.split("/")))}</h3>'
            f'<span class="meta">{len(groups[folder])} recursos · Ver contenido →</span></a>'
            for folder in folders)
        parts.append(f'<nav aria-label="Carpetas"><h2>Explorar carpetas</h2><div class="grid">{cards}</div></nav>')
    for folder in (['.'] if '.' in groups else []) + folders:
        label = 'Recursos' if folder == '.' else ' / '.join(readable(p) for p in folder.split('/'))
        anchor = 'recursos' if folder == '.' else anchors[folder]
        cards = []
        for rel in groups[folder]:
            kind = EXTENSIONS[rel.suffix.lower()]
            css, icon = ('pdf', '↓') if kind == 'PDF' else ('app', '↗')
            # quote evita que espacios, #, ?, acentos o comillas rompan el enlace.
            href = './' + quote(rel.as_posix(), safe='/')
            cards.append(f'<a class="card {css}" href="{escape(href, quote=True)}">'
                         f'<span class="badge">{icon} {kind}</span><h3>{escape(file_title(rel))}</h3>'
                         f'<span class="filename">{escape(rel.name)}</span>'
                         f'<span class="meta">{"Abrir documento" if css == "pdf" else "Abrir aplicación"} →</span></a>')
        parts.append(f'<section id="{anchor}" aria-labelledby="titulo-{anchor}">'
                     f'<h2 id="titulo-{anchor}">{escape(label)}</h2><div class="grid">{"".join(cards)}</div></section>')
    count = sum(map(len, groups.values()))
    if not count:
        parts.append('<p class="empty">Todavía no hay recursos. Añade archivos HTML o PDF al repositorio.</p>')
    template = Path(__file__).with_name('template.html').read_text(encoding='utf-8')
    rendered = template.replace('{{TITLE}}', escape(TITLE)).replace('{{COUNT}}', str(count)).replace('{{CONTENT}}', '\n'.join(parts))
    (root / 'index.html').write_text(rendered, encoding='utf-8')
    print(f'index.html generado: {count} recursos, {len(folders)} carpetas.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2], help='Raíz que contiene los recursos')
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error('La raíz debe ser una carpeta existente')
    generate(root)
