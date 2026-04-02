#!/usr/bin/env python3
"""Extract text and images from a .docx file.

Usage:
    python extract_docx.py <docx_path> <image_output_dir>

Outputs:
    - Images extracted to <image_output_dir>/
    - Text + image markers printed to stdout (one paragraph per line,
      [IMAGE:<filename>] markers where images appear)
"""

import os
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def get_image_rels(z):
    """Build rId -> media filename mapping from document.xml.rels."""
    rels = {}
    try:
        with z.open("word/_rels/document.xml.rels") as f:
            tree = ET.parse(f)
        for rel in tree.getroot():
            rid = rel.get("Id")
            target = rel.get("Target", "")
            if "media/" in target:
                rels[rid] = os.path.basename(target)
    except KeyError:
        pass
    return rels


def extract(docx_path, image_dir):
    os.makedirs(image_dir, exist_ok=True)

    with zipfile.ZipFile(docx_path) as z:
        media_files = [n for n in z.namelist() if n.startswith("word/media/")]
        for name in media_files:
            fname = os.path.basename(name)
            with z.open(name) as src, open(os.path.join(image_dir, fname), "wb") as dst:
                dst.write(src.read())

        rels = get_image_rels(z)

        with z.open("word/document.xml") as f:
            tree = ET.parse(f)

    body = tree.getroot().find(".//w:body", NS)
    img_counter = 0

    for para in body.findall(".//w:p", NS):
        texts = []
        for r in para.findall(".//w:r", NS):
            for t in r.findall("w:t", NS):
                if t.text:
                    texts.append(t.text)

        images_in_para = []
        for drawing in para.findall(".//" + "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}drawing"):
            blips = drawing.findall(".//{http://schemas.openxmlformats.org/drawingml/2006/main}blip")
            for blip in blips:
                embed = blip.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
                if embed and embed in rels:
                    images_in_para.append(rels[embed])

        for alt in para.findall(".//{http://schemas.openxmlformats.org/markup-compatibility/2006}AlternateContent"):
            blips = alt.findall(".//{http://schemas.openxmlformats.org/drawingml/2006/main}blip")
            for blip in blips:
                embed = blip.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
                if embed and embed in rels:
                    images_in_para.append(rels[embed])

        line = "".join(texts).strip()
        if line:
            print(line)
        for img in images_in_para:
            img_counter += 1
            print(f"[IMAGE:{img}]")

    if not media_files:
        print("[NO_IMAGES]", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <docx_path> <image_output_dir>", file=sys.stderr)
        sys.exit(1)
    extract(sys.argv[1], sys.argv[2])
