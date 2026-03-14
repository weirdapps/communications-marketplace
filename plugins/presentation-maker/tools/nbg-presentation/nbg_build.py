#!/usr/bin/env python3
"""
NBG Presentation Builder - McKinsey Quality Version

Creates NBG-formatted presentations from YAML storylines following McKinsey standards:
- Pyramid Principle: Lead with the answer
- SCQA Framework: Situation, Complication, Question, Answer
- Action Titles: Full sentences that tell the story
- One Message Per Slide

Supports two input formats:
1. Simple format (slides array at root)
2. McKinsey format (presentation object with slides)

Usage:
    python nbg_build.py storyline.yaml output.pptx
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

import yaml

# Register namespaces to preserve them in output
ET.register_namespace('a', 'http://schemas.openxmlformats.org/drawingml/2006/main')
ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
ET.register_namespace('p', 'http://schemas.openxmlformats.org/presentationml/2006/main')

# Paths
SCRIPT_DIR = Path(__file__).parent
ASSETS_DIR = SCRIPT_DIR.parent.parent / 'assets'
CATALOG_PATH = ASSETS_DIR / 'slide-catalog.yaml'
TEMPLATES_DIR = ASSETS_DIR / 'templates'
def rearrange_slides(template_path, output_path, indices):
    """Extract specific slides from template PPTX by index (1-based).

    Creates a new PPTX containing only the slides at the given indices,
    preserving layouts, masters, and relationships.
    """
    ns_map = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'rel': 'http://schemas.openxmlformats.org/package/2006/relationships',
        'ct': 'http://schemas.openxmlformats.org/package/2006/content-types',
    }
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        src = tmp / 'src'
        with zipfile.ZipFile(template_path, 'r') as zf:
            zf.extractall(src)

        slides_dir = src / 'ppt' / 'slides'
        rels_dir = slides_dir / '_rels'

        # Parse presentation.xml to get slide order
        pres_path = src / 'ppt' / 'presentation.xml'
        pres_tree = ET.parse(pres_path)
        pres_root = pres_tree.getroot()
        sld_id_lst = pres_root.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}sldIdLst')
        if sld_id_lst is None:
            raise RuntimeError("No sldIdLst found in presentation.xml")

        sld_ids = list(sld_id_lst)

        # Parse presentation.xml.rels to map rIds to slide files
        pres_rels_path = src / 'ppt' / '_rels' / 'presentation.xml.rels'
        pres_rels_tree = ET.parse(pres_rels_path)
        rid_to_target = {}
        for rel in pres_rels_tree.getroot():
            rid = rel.get('Id')
            target = rel.get('Target')
            if target and 'slides/slide' in target:
                rid_to_target[rid] = target

        # Build ordered list of slide files from presentation
        ordered_slides = []
        for sld_id in sld_ids:
            rid = sld_id.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
            if rid and rid in rid_to_target:
                ordered_slides.append(rid_to_target[rid])

        # Select slides by 1-based index
        keep_targets = set()
        for idx in indices:
            if 1 <= idx <= len(ordered_slides):
                keep_targets.add(ordered_slides[idx - 1])

        # Remove slides not in keep list
        remove_targets = set()
        for sld_id in list(sld_id_lst):
            rid = sld_id.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
            if rid and rid in rid_to_target:
                target = rid_to_target[rid]
                if target not in keep_targets:
                    remove_targets.add(target)
                    sld_id_lst.remove(sld_id)

        # Reorder kept slides to match requested order
        remaining = list(sld_id_lst)
        for item in remaining:
            sld_id_lst.remove(item)
        for idx in indices:
            target = ordered_slides[idx - 1] if 1 <= idx <= len(ordered_slides) else None
            if target:
                for item in remaining:
                    rid = item.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
                    if rid and rid_to_target.get(rid) == target:
                        sld_id_lst.append(item)
                        break

        pres_tree.write(pres_path, xml_declaration=True, encoding='UTF-8')

        # Delete removed slide files and their rels
        for target in remove_targets:
            slide_file = src / 'ppt' / target
            if slide_file.exists():
                slide_file.unlink()
            rels_file = slides_dir / '_rels' / (Path(target).name + '.rels')
            if rels_file.exists():
                rels_file.unlink()

        # Clean up [Content_Types].xml — remove overrides for deleted slides
        ct_path = src / '[Content_Types].xml'
        if ct_path.exists():
            ct_tree = ET.parse(ct_path)
            ct_root = ct_tree.getroot()
            ct_ns = 'http://schemas.openxmlformats.org/package/2006/content-types'
            keep_slide_names = set()
            for target in keep_targets:
                keep_slide_names.add(Path(target).name)
            for override in list(ct_root):
                part = override.get('PartName', '')
                if '/ppt/slides/slide' in part:
                    slide_name = part.split('/')[-1]
                    if slide_name not in keep_slide_names:
                        ct_root.remove(override)
            ct_tree.write(ct_path, xml_declaration=True, encoding='UTF-8')

        # Remove presentation.xml.rels entries for deleted slides
        for rel in list(pres_rels_tree.getroot()):
            target = rel.get('Target', '')
            if target in remove_targets:
                pres_rels_tree.getroot().remove(rel)
        pres_rels_tree.write(pres_rels_path, xml_declaration=True, encoding='UTF-8')

        # Repack
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for fp in src.rglob('*'):
                if fp.is_file():
                    zf.write(fp, fp.relative_to(src))


def extract_inventory(pptx_path):
    """Extract text shape inventory from PPTX.

    Returns dict: {"slide-0": {"Shape Name": {top, left, width, height, ...}}, ...}
    """
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    }
    EMU_TO_INCHES = 914400

    inventory = {}
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            zf.extractall(tmp)

        slides_dir = tmp / 'ppt' / 'slides'
        slide_files = sorted(slides_dir.glob('slide*.xml'),
                             key=lambda f: int(re.search(r'(\d+)', f.name).group()))

        for slide_idx, slide_file in enumerate(slide_files):
            slide_key = f"slide-{slide_idx}"
            inventory[slide_key] = {}

            tree = ET.parse(slide_file)
            root = tree.getroot()

            for sp in root.findall('.//p:sp', ns):
                # Get shape name
                nvSpPr = sp.find('.//p:nvSpPr/p:cNvPr', ns)
                if nvSpPr is None:
                    continue
                name = nvSpPr.get('name', '')

                # Get position/size
                xfrm = sp.find('.//p:spPr/a:xfrm', ns)
                if xfrm is None:
                    xfrm = sp.find('.//a:xfrm', ns)

                top = left = width = height = 0
                if xfrm is not None:
                    off = xfrm.find('a:off', ns)
                    ext = xfrm.find('a:ext', ns)
                    if off is not None:
                        left = int(off.get('x', 0)) / EMU_TO_INCHES
                        top = int(off.get('y', 0)) / EMU_TO_INCHES
                    if ext is not None:
                        width = int(ext.get('cx', 0)) / EMU_TO_INCHES
                        height = int(ext.get('cy', 0)) / EMU_TO_INCHES

                # Get placeholder type
                nvPr = sp.find('.//p:nvSpPr/p:nvPr', ns)
                ph_type = ''
                if nvPr is not None:
                    ph = nvPr.find('p:ph', ns)
                    if ph is not None:
                        ph_type = ph.get('type', '')

                # Check for text body
                txBody = sp.find('.//p:txBody', ns)
                if txBody is None:
                    txBody = sp.find('.//a:txBody', ns)
                if txBody is None:
                    continue

                # Extract paragraphs info
                paras = []
                default_font_size = 11
                for para in txBody.findall('a:p', ns):
                    text_parts = []
                    for r_elem in para.findall('a:r', ns):
                        t = r_elem.find('a:t', ns)
                        if t is not None and t.text:
                            text_parts.append(t.text)
                        rPr = r_elem.find('a:rPr', ns)
                        if rPr is not None:
                            sz = rPr.get('sz')
                            if sz:
                                default_font_size = int(sz) / 100
                    paras.append({'text': ''.join(text_parts)})

                inventory[slide_key][name] = {
                    'top': round(top, 2),
                    'left': round(left, 2),
                    'width': round(width, 2),
                    'height': round(height, 2),
                    'placeholder_type': ph_type,
                    'default_font_size': default_font_size,
                    'paragraphs': paras,
                }

    return inventory


def apply_replacements(pptx_path, replacements, output_path):
    """Apply text replacements to PPTX shapes.

    replacements: {"slide-0": {"Shape Name": {"paragraphs": [{"text": "...", ...}]}}}
    """
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    }

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            zf.extractall(tmp)

        slides_dir = tmp / 'ppt' / 'slides'
        slide_files = sorted(slides_dir.glob('slide*.xml'),
                             key=lambda f: int(re.search(r'(\d+)', f.name).group()))

        for slide_idx, slide_file in enumerate(slide_files):
            slide_key = f"slide-{slide_idx}"
            if slide_key not in replacements:
                continue

            tree = ET.parse(slide_file)
            root = tree.getroot()
            modified = False

            for sp in root.findall('.//p:sp', ns):
                nvSpPr = sp.find('.//p:nvSpPr/p:cNvPr', ns)
                if nvSpPr is None:
                    continue
                name = nvSpPr.get('name', '')

                if name not in replacements[slide_key]:
                    continue

                repl = replacements[slide_key][name]
                new_paras = repl.get('paragraphs', [])

                txBody = sp.find('.//p:txBody', ns)
                if txBody is None:
                    txBody = sp.find('.//a:txBody', ns)
                if txBody is None:
                    continue

                # Remove existing paragraphs
                for p_elem in txBody.findall('a:p', ns):
                    txBody.remove(p_elem)

                # Add new paragraphs
                if not new_paras:
                    # Empty paragraph to keep valid XML
                    p_elem = ET.SubElement(txBody, '{http://schemas.openxmlformats.org/drawingml/2006/main}p')
                    ET.SubElement(p_elem, '{http://schemas.openxmlformats.org/drawingml/2006/main}endParaRPr')
                else:
                    for para_spec in new_paras:
                        p_elem = ET.SubElement(txBody, '{http://schemas.openxmlformats.org/drawingml/2006/main}p')

                        # Paragraph properties (bullets, spacing)
                        if para_spec.get('bullet') or para_spec.get('space_before'):
                            pPr = ET.SubElement(p_elem, '{http://schemas.openxmlformats.org/drawingml/2006/main}pPr')
                            if para_spec.get('bullet'):
                                level = para_spec.get('level', 0)
                                pPr.set('lvl', str(level))
                                # NBG bullet: • in Arial, Bright Cyan #00DFF8
                                buFont = ET.SubElement(pPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}buFont')
                                buFont.set('typeface', para_spec.get('bullet_font', 'Arial'))
                                buClr = ET.SubElement(pPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}buClr')
                                buSrgb = ET.SubElement(buClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
                                buSrgb.set('val', para_spec.get('bullet_color', '00DFF8'))
                                buChar = ET.SubElement(pPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}buChar')
                                buChar.set('char', '\u2022')
                            if para_spec.get('space_before'):
                                spcBef = ET.SubElement(pPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}spcBef')
                                spcPts = ET.SubElement(spcBef, '{http://schemas.openxmlformats.org/drawingml/2006/main}spcPts')
                                spcPts.set('val', str(int(para_spec['space_before'] * 100)))

                        # Run with text
                        r_elem = ET.SubElement(p_elem, '{http://schemas.openxmlformats.org/drawingml/2006/main}r')

                        # Run properties
                        rPr = ET.SubElement(r_elem, '{http://schemas.openxmlformats.org/drawingml/2006/main}rPr')
                        rPr.set('lang', 'el-GR')
                        rPr.set('dirty', '0')
                        if para_spec.get('bold'):
                            rPr.set('b', '1')
                        if para_spec.get('font_size'):
                            rPr.set('sz', str(int(para_spec['font_size'] * 100)))
                        if para_spec.get('font_name'):
                            latin = ET.SubElement(rPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}latin')
                            latin.set('typeface', para_spec['font_name'])
                        if para_spec.get('color'):
                            solidFill = ET.SubElement(rPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}solidFill')
                            srgbClr = ET.SubElement(solidFill, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
                            srgbClr.set('val', para_spec['color'])

                        # Text
                        t = ET.SubElement(r_elem, '{http://schemas.openxmlformats.org/drawingml/2006/main}t')
                        t.text = para_spec.get('text', '')

                modified = True

            if modified:
                tree.write(slide_file, xml_declaration=True, encoding='UTF-8')

        # Repack
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for fp in tmp.rglob('*'):
                if fp.is_file():
                    zf.write(fp, fp.relative_to(tmp))


def load_catalog():
    """Load the slide catalog."""
    with open(CATALOG_PATH, 'r') as f:
        return yaml.safe_load(f)


def resolve_slide_index(catalog, template, slide_type):
    """Resolve a slide type path (e.g., 'covers/simple_white') to template index."""
    parts = slide_type.split('/')
    slides = catalog['templates'][template]['slides']

    current = slides
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            raise ValueError(f"Unknown slide type: {slide_type}")

    if isinstance(current, int):
        return current
    raise ValueError(f"Slide type {slide_type} does not resolve to an index")


def get_template_path(template):
    """Get template file path."""
    return TEMPLATES_DIR / f'NBG-Template-{template}.pptx'


def normalize_slide_type(slide_type, recommended_visual=None):
    """Convert McKinsey slide types to catalog paths.

    Handles both:
    - Simple: "covers/simple_white" (passes through)
    - McKinsey: "cover", "content", "divider", "back_cover"

    Uses recommended_visual hint when available for smarter selection.
    """
    # If it already has a slash, it's a catalog path
    if '/' in slide_type:
        return slide_type

    # Visual-based mapping for content slides (McKinsey format)
    # Using simpler layouts to avoid decorative elements (ellipses, triangles)
    visual_mapping = {
        'bar_chart': 'charts/bar_single',
        'pie_chart': 'charts/pie_single',
        'line_chart': 'charts/line_single',
        'waterfall_chart': 'charts/bar_single',  # Use bar_single to avoid decorative triangles
        'comparison_chart': 'charts/bar_dual',
        'kpi_dashboard': 'content/text_only',                 # Clean layout, no decorative elements
        'numbered_infographic': 'content/text_only',         # Clean layout, no decorative elements
        'timeline': 'content/text_only',                     # Clean layout, no decorative elements
        'process': 'content/text_only',                      # Clean layout, no decorative elements
        'funnel': 'content/text_only',                       # Clean layout, no decorative elements
        'table': 'tables/half_page',
        'comparison_table': 'tables/comparison',
        'icons': 'content/text_only',                         # Clean layout, no decorative elements
        'none': 'content/text_only',
    }

    # If recommended_visual is provided and matches, use it
    if recommended_visual and recommended_visual in visual_mapping:
        return visual_mapping[recommended_visual]

    # Map base McKinsey types to catalog paths
    # Using "quiet" variants by default - cleaner designs without decorative elements
    type_mapping = {
        'cover': 'covers/quiet',              # Minimal cover (slide 21)
        'divider': 'dividers/quiet_white',    # Clean divider with simple rect (slide 72)
        'content': 'content/text_only',
        'chart': 'charts/bar_dual',
        'infographic': 'infographics/numbered_6',
        'table': 'tables/half_page',
        'thankyou': 'back_covers/quiet',      # Truly empty slide (slide 190)
        'back_cover': 'back_covers/quiet',    # Truly empty slide (slide 190)
        'summary': 'content/text_with_bullets',
    }

    return type_mapping.get(slide_type, 'content/text_only')


def clean_template_artifacts(pptx_path):
    """Remove template artifacts that violate NBG guidelines.

    1. Strip decorative shapes (triangles, ellipses) that aren't content
    2. Remove orphaned chart files not referenced by kept slides
    3. Set text box margins to 0 (NBG requirement)
    """
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    }

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            zf.extractall(tmp)

        slides_dir = tmp / 'ppt' / 'slides'
        rels_dir = slides_dir / '_rels'

        # Collect all chart/media references from kept slides
        referenced_charts = set()
        for slide_file in slides_dir.glob('slide*.xml'):
            rels_file = rels_dir / (slide_file.name + '.rels')
            if rels_file.exists():
                rels_tree = ET.parse(rels_file)
                for rel in rels_tree.getroot():
                    target = rel.get('Target', '')
                    if 'chart' in target:
                        referenced_charts.add(target.split('/')[-1])

        # Remove orphaned chart files
        charts_dir = tmp / 'ppt' / 'charts'
        if charts_dir.exists():
            for chart_file in charts_dir.glob('chart*.xml'):
                if chart_file.name not in referenced_charts:
                    chart_file.unlink()
                    # Also remove chart rels
                    chart_rels = charts_dir / '_rels' / (chart_file.name + '.rels')
                    if chart_rels.exists():
                        chart_rels.unlink()

        # Process each slide
        for slide_file in slides_dir.glob('slide*.xml'):
            tree = ET.parse(slide_file)
            root = tree.getroot()
            modified = False

            sp_tree = root.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}spTree')
            if sp_tree is None:
                continue

            # Remove decorative shapes (triangles, rounded rects with no text)
            # Check both direct sp children AND group shapes (grpSp)
            decorative_geoms = ('triangle', 'rtTriangle', 'ellipse', 'roundRect')
            for child in list(sp_tree):
                tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag

                if tag == 'grpSp':
                    # Group shape — check if it contains only decorative elements
                    geoms = [g.get('prst', '') for g in child.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}prstGeom')]
                    texts = [t.text for t in child.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}t') if t.text and t.text.strip()]
                    if geoms and all(g in decorative_geoms for g in geoms) and not texts:
                        sp_tree.remove(child)
                        modified = True
                        continue

                if tag != 'sp':
                    continue

                # Check if shape is a decorative element
                prstGeom = child.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}prstGeom')
                if prstGeom is not None:
                    prst = prstGeom.get('prst', '')
                    if prst in decorative_geoms:
                        texts = [t.text for t in child.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}t') if t.text and t.text.strip()]
                        if not texts:
                            sp_tree.remove(child)
                            modified = True
                            continue

                # Set text box margins to 0 (NBG requirement: margin: 0 always)
                # Must explicitly set all four — OOXML defaults are non-zero
                for bodyPr in child.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}bodyPr'):
                    for attr in ('lIns', 'tIns', 'rIns', 'bIns'):
                        bodyPr.set(attr, '0')
                    modified = True

            if modified:
                tree.write(slide_file, xml_declaration=True, encoding='UTF-8')

        # Clean up content types for orphaned charts
        ct_path = tmp / '[Content_Types].xml'
        if ct_path.exists():
            ct_tree = ET.parse(ct_path)
            ct_root = ct_tree.getroot()
            for override in list(ct_root):
                part = override.get('PartName', '')
                if '/ppt/charts/chart' in part:
                    chart_name = part.split('/')[-1]
                    if chart_name not in referenced_charts:
                        ct_root.remove(override)
            ct_tree.write(ct_path, xml_declaration=True, encoding='UTF-8')

        # Repack
        with zipfile.ZipFile(pptx_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for fp in tmp.rglob('*'):
                if fp.is_file():
                    zf.write(fp, fp.relative_to(tmp))


def clear_slide_numbers(pptx_path):
    """Clear static slide number text from all slides.

    NBG template slides have hardcoded slide numbers (e.g., "93" on slide 93).
    This function clears those placeholders to avoid showing incorrect numbers.
    """
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    }

    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        unpacked = temp / 'unpacked'

        # Unpack
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            zf.extractall(unpacked)

        slides_dir = unpacked / 'ppt' / 'slides'
        modified = False

        for slide_file in sorted(slides_dir.glob('slide*.xml')):
            tree = ET.parse(slide_file)
            root = tree.getroot()

            # Find all shapes
            for sp in root.findall('.//p:sp', ns):
                # Check if this is a slide number placeholder
                nvPr = sp.find('.//p:nvSpPr/p:nvPr', ns)
                if nvPr is not None:
                    ph = nvPr.find('p:ph', ns)
                    if ph is not None and ph.get('type') == 'sldNum':
                        # Clear all text in this shape
                        for t in sp.findall('.//a:t', ns):
                            if t.text and t.text.strip().isdigit():
                                t.text = ''
                                modified = True

            if modified:
                tree.write(slide_file, xml_declaration=True, encoding='UTF-8')

        if modified:
            # Repack
            with zipfile.ZipFile(pptx_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for file_path in unpacked.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(unpacked)
                        zf.write(file_path, arcname)


def build_presentation(outline_path, output_path):
    """Build NBG presentation from outline.

    Supports two formats:
    1. Simple: { template: GR, slides: [...] }
    2. McKinsey: { presentation: { slides: [...] }, template: GR }
    """
    outline_path = Path(outline_path).expanduser().resolve()
    output_path = Path(output_path).expanduser().resolve()

    # Load outline
    with open(outline_path, 'r') as f:
        outline = yaml.safe_load(f)

    # Support both simple and McKinsey formats
    if 'presentation' in outline:
        # McKinsey format
        presentation = outline['presentation']
        slides = presentation.get('slides', [])
        template = outline.get('template', 'GR')
        print(f"\n[McKinsey Quality] Using Pyramid Principle structure")
        if presentation.get('main_recommendation'):
            print(f"  Main recommendation: {presentation['main_recommendation'][:60]}...")
    else:
        # Simple format
        template = outline.get('template', 'GR')
        slides = outline.get('slides', [])

    if not slides:
        raise ValueError("No slides defined in outline")

    template_path = get_template_path(template)
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    catalog = load_catalog()

    print(f"\nNBG Presentation Builder")
    print(f"{'='*50}")
    print(f"Template: {template}")
    print(f"Slides: {len(slides)}")
    print(f"Output: {output_path}")
    print(f"{'='*50}\n")

    # Get slide indices and resolved types - handle both simple and McKinsey types
    indices = []
    resolved_types = []  # Track resolved catalog paths for each slide
    for slide in slides:
        raw_type = slide.get('type', 'content')
        # McKinsey format may have recommended_visual hint
        recommended_visual = slide.get('recommended_visual')
        normalized_type = normalize_slide_type(raw_type, recommended_visual)
        idx = resolve_slide_index(catalog, template, normalized_type)
        indices.append(idx)
        resolved_types.append(normalized_type)
        if recommended_visual:
            print(f"  {raw_type} (visual: {recommended_visual}) -> {normalized_type} -> slide {idx}")
        elif raw_type != normalized_type:
            print(f"  {raw_type} -> {normalized_type} -> slide {idx}")
        else:
            print(f"  {raw_type} -> slide {idx}")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        working = temp / 'working.pptx'

        # Step 1: Rearrange slides
        print(f"\n[1/4] Extracting slides from template...")
        rearrange_slides(template_path, working, indices)
        print(f"  Extracted {len(indices)} slides")

        # Step 2: Extract inventory
        print(f"\n[2/4] Analyzing slide structure...")
        inventory = extract_inventory(working)
        print(f"  Found shapes in {len(inventory)} slides")

        # Step 3: Build smart replacements
        print(f"\n[3/4] Preparing content...")
        replacements = build_smart_replacements(slides, inventory, resolved_types)

        # Step 4: Apply replacements
        print(f"\n[4/4] Applying content...")
        final = temp / 'final.pptx'
        apply_replacements(working, replacements, final)

        # Use the best available output
        if final.exists():
            shutil.copy(final, output_path)
        else:
            shutil.copy(working, output_path)
            print("  Using template (text replacement skipped)")

    # Clean template artifacts (decorative shapes, orphaned charts, margins)
    print("\n[5/6] Cleaning template artifacts...")
    try:
        clean_template_artifacts(output_path)
        print("  Removed decorative shapes, orphaned charts, fixed margins")
    except Exception as e:
        print(f"  Warning: Could not clean artifacts: {e}")

    # Clear static slide numbers from template
    print("\n[6/6] Cleaning up slide numbers...")
    try:
        clear_slide_numbers(output_path)
        print("  Cleared static slide numbers")
    except Exception as e:
        print(f"  Warning: Could not clear slide numbers: {e}")

    print(f"\n{'='*50}")
    print(f"Created: {output_path}")
    print(f"{'='*50}\n")

    # Validate
    print("Validating...")
    cmd = ['python', str(SCRIPT_DIR / 'nbg_validate.py'), str(output_path)]
    subprocess.run(cmd)


def build_smart_replacements(slides, inventory, resolved_types=None):
    """Build replacement JSON with smart content mapping.

    Uses a simple positional approach: shapes are sorted top-to-bottom,
    and content is assigned in order. This works reliably with NBG templates.
    All text uses Aptos font to match NBG brand guidelines.

    Accessibility: Automatically selects font colors based on background:
    - Light backgrounds: Dark Teal (#003841) for titles, Dark Text (#202020) for body
    - Dark backgrounds: White (#FFFFFF) for all text

    Args:
        slides: List of slide definitions from YAML
        inventory: Shape inventory from the working presentation
        resolved_types: List of resolved catalog paths for each slide (for smarter detection)
    """
    NBG_FONT = "Aptos"  # NBG brand font

    # Accessibility: Color settings for different backgrounds
    COLORS_LIGHT_BG = {
        'title': '003841',    # Dark Teal
        'body': '202020',     # Dark Text
        'number': '007B85',   # NBG Teal
    }
    COLORS_DARK_BG = {
        'title': 'FFFFFF',    # White
        'body': 'FFFFFF',     # White
        'number': 'FFFFFF',   # White
    }

    # Slide types that use dark backgrounds
    DARK_BG_TYPES = ['covers/simple_dark', 'dividers/section_dark', 'dividers/quiet_dark',
                     'back_covers/plain_dark']

    replacements = {}

    for slide_idx, slide in enumerate(slides):
        slide_key = f"slide-{slide_idx}"
        content = slide.get('content', {})
        raw_type = slide.get('type', '')

        # Use resolved type if available for better category detection
        resolved_type = resolved_types[slide_idx] if resolved_types else raw_type

        # Accessibility: Select colors based on background
        is_dark_bg = resolved_type in DARK_BG_TYPES
        colors = COLORS_DARK_BG if is_dark_bg else COLORS_LIGHT_BG

        if slide_key not in inventory:
            continue

        shapes = inventory[slide_key]
        replacements[slide_key] = {}

        # Sort shapes by position (top to bottom, left to right)
        sorted_shapes = sorted(
            shapes.items(),
            key=lambda x: (x[1].get('top', 0), x[1].get('left', 0))
        )

        # Determine slide category based on resolved catalog path (not raw_type)
        # resolved_type is the definitive type after visual recommendations are applied
        is_cover = 'cover' in resolved_type and 'back_cover' not in resolved_type
        is_back_cover = 'back_cover' in resolved_type
        is_divider = 'divider' in resolved_type
        is_chart = 'chart' in resolved_type
        is_infographic = 'infographic' in resolved_type
        is_timeline = 'timeline' in resolved_type
        is_table = 'table' in resolved_type
        # Content only if resolved path is content/ AND not a visual type
        is_content = 'content/' in resolved_type and not (is_chart or is_infographic or is_timeline or is_table)

        if is_back_cover:
            # Back cover: clear all text
            for shape_name, shape_info in sorted_shapes:
                replacements[slide_key][shape_name] = {"paragraphs": []}
            continue

        if is_divider:
            # Section divider: number and title
            # Find shapes - typically one for number, one for title
            number_shape = None
            title_shape = None

            for shape_name, shape_info in sorted_shapes:
                font_size = shape_info.get('default_font_size', 11)
                width = shape_info.get('width', 5)

                # Number is typically in a narrow shape or has large font
                if width < 2 and number_shape is None:
                    number_shape = shape_name
                elif title_shape is None:
                    title_shape = shape_name

            for shape_name, shape_info in sorted_shapes:
                if shape_name == number_shape and 'number' in content:
                    replacements[slide_key][shape_name] = {
                        "paragraphs": [{"text": content['number'], "font_name": NBG_FONT, "font_size": 60, "color": colors['number']}]
                    }
                elif shape_name == title_shape and 'title' in content:
                    replacements[slide_key][shape_name] = {
                        "paragraphs": [{"text": content['title'], "font_name": NBG_FONT, "font_size": 48, "color": colors['title']}]
                    }
                else:
                    replacements[slide_key][shape_name] = {"paragraphs": []}
            continue

        if is_chart:
            # Chart slides: set title and description, leave chart placeholders
            # Use accessible colors based on background
            title_set = False
            desc_set = False

            for shape_name, shape_info in sorted_shapes:
                height = shape_info.get('height', 1)
                placeholder = shape_info.get('placeholder_type', '')

                # Skip chart/picture placeholders
                if placeholder in ('OBJECT', 'CHART', 'PICTURE'):
                    continue

                if not title_set and 'title' in content and height < 1:
                    replacements[slide_key][shape_name] = {
                        "paragraphs": [{"text": content['title'], "font_name": NBG_FONT, "bold": True, "color": colors['title']}]
                    }
                    title_set = True
                elif not desc_set and 'description' in content:
                    replacements[slide_key][shape_name] = {
                        "paragraphs": [{"text": content['description'], "font_name": NBG_FONT, "color": colors['body']}]
                    }
                    desc_set = True
                else:
                    replacements[slide_key][shape_name] = {"paragraphs": []}
            continue

        if is_cover:
            # Cover slides: NBG typography hierarchy
            # Title: 48pt, Dark Teal #003841, Regular weight
            # Subtitle: 36pt, NBG Teal #007B85
            # Location: 14pt, Dark Teal #003841
            # Date: 14pt, Medium Gray #939793
            content_items = []
            if 'title' in content:
                content_items.append({'text': content['title'], 'font_name': NBG_FONT, 'font_size': 48, 'color': colors['title']})
            if 'subtitle' in content:
                content_items.append({'text': content['subtitle'], 'font_name': NBG_FONT, 'font_size': 36, 'color': '007B85'})
            if 'location' in content:
                content_items.append({'text': content['location'], 'font_name': NBG_FONT, 'font_size': 14, 'color': colors['title']})
            if 'date' in content:
                content_items.append({'text': content['date'], 'font_name': NBG_FONT, 'font_size': 14, 'color': '939793'})

            for i, (shape_name, shape_info) in enumerate(sorted_shapes):
                if i < len(content_items):
                    replacements[slide_key][shape_name] = {
                        "paragraphs": [content_items[i]]
                    }
                else:
                    replacements[slide_key][shape_name] = {"paragraphs": []}
            continue

        if is_content:
            # Content slides: McKinsey format support
            # - 'points' (McKinsey) or 'paragraphs' (legacy) for body content
            # - 'title' is action title (full sentence for McKinsey)
            # - 'hyper_title' or 'bumper' for section tag above title

            # Find shapes by their likely purpose
            hyper_title_shape = None
            title_shape = None
            body_shape = None

            for shape_name, shape_info in sorted_shapes:
                height = shape_info.get('height', 1)

                if height < 0.5 and hyper_title_shape is None:
                    hyper_title_shape = shape_name
                elif height < 1.0 and title_shape is None and shape_name != hyper_title_shape:
                    title_shape = shape_name
                elif height > 1.0 and body_shape is None:
                    body_shape = shape_name

            # If we didn't find by height, use position
            if title_shape is None and len(sorted_shapes) >= 2:
                title_shape = sorted_shapes[1][0] if sorted_shapes[0][0] == hyper_title_shape else sorted_shapes[0][0]
            if body_shape is None and len(sorted_shapes) >= 2:
                # Use the largest shape
                body_shape = max(sorted_shapes, key=lambda x: x[1].get('height', 0) * x[1].get('width', 0))[0]

            # Get body content - support both McKinsey 'points' and legacy 'paragraphs'
            body_content = content.get('points') or content.get('paragraphs') or []

            # Get hyper title - support both 'bumper' (McKinsey) and 'hyper_title' (legacy)
            hyper_text = content.get('bumper') or content.get('hyper_title')

            # Build replacements with NBG typography hierarchy
            # Content title: 24pt, Dark Teal, Regular weight (NOT bold)
            # Bumper: 12pt, NBG Teal #007B85
            # Body bullets: 14pt L1, spacing before 14pt, bullet in Arial Bright Cyan
            for shape_name, shape_info in sorted_shapes:
                if shape_name == hyper_title_shape and hyper_text:
                    replacements[slide_key][shape_name] = {
                        "paragraphs": [{"text": hyper_text, "font_name": NBG_FONT, "font_size": 12, "color": colors['number']}]
                    }
                elif shape_name == title_shape and 'title' in content:
                    replacements[slide_key][shape_name] = {
                        "paragraphs": [{"text": content['title'], "font_name": NBG_FONT, "font_size": 24, "color": colors['title']}]
                    }
                elif shape_name == body_shape and body_content:
                    paras = []
                    for p in body_content:
                        if isinstance(p, dict):
                            para = {'text': p.get('text', ''), 'font_name': NBG_FONT, 'font_size': 14, 'color': colors['body']}
                            if p.get('bullet'):
                                para['bullet'] = True
                                para['level'] = 0
                                para['space_before'] = 14
                            paras.append(para)
                        else:
                            # McKinsey points are strings - convert to bullet points
                            paras.append({'text': str(p), 'font_name': NBG_FONT, 'font_size': 14, 'bullet': True, 'level': 0, 'color': colors['body'], 'space_before': 14})
                    replacements[slide_key][shape_name] = {"paragraphs": paras}
                else:
                    # Clear other shapes
                    replacements[slide_key][shape_name] = {"paragraphs": []}
            continue

        # Handle infographic slides specially (numbered items in grid)
        if is_infographic:
            body_content = content.get('points') or content.get('items') or []
            title_text = content.get('title', '')

            # Find title shape (first shape at top with short height)
            title_shape = None
            number_shapes = []  # Shapes with single numbers (1, 2, 3...)
            text_shapes = []    # Text shapes next to numbers

            for shape_name, shape_info in sorted_shapes:
                height = shape_info.get('height', 1)
                width = shape_info.get('width', 1)
                top = shape_info.get('top', 5)
                paras = shape_info.get('paragraphs', [])
                first_text = paras[0].get('text', '') if paras else ''

                # Title is at top with short height
                if top < 1.2 and height < 0.5 and title_shape is None:
                    title_shape = shape_name
                # Number shapes are small squares with single digit
                elif width < 1.5 and height > 0.8 and first_text.isdigit():
                    number_shapes.append((shape_name, int(first_text)))
                # Text shapes are wider boxes next to numbers
                elif width > 2.5 and height > 0.8:
                    text_shapes.append(shape_name)

            # Sort number shapes by their number value
            number_shapes.sort(key=lambda x: x[1])

            # Apply replacements with accessible colors
            for shape_name, shape_info in sorted_shapes:
                if shape_name == title_shape and title_text:
                    replacements[slide_key][shape_name] = {
                        "paragraphs": [{"text": title_text, "font_name": NBG_FONT, "bold": True, "color": colors['title']}]
                    }
                elif shape_name in [ns[0] for ns in number_shapes]:
                    # Keep the numbers as-is (they're part of the visual design)
                    pass
                elif shape_name in text_shapes and body_content:
                    # Map content items to text shapes
                    idx = text_shapes.index(shape_name)
                    if idx < len(body_content):
                        item = body_content[idx]
                        text = item.get('text', item.get('title', '')) if isinstance(item, dict) else str(item)
                        replacements[slide_key][shape_name] = {
                            "paragraphs": [{"text": text, "font_name": NBG_FONT, "color": colors['body']}]
                        }
                    else:
                        # Clear unused text shapes
                        replacements[slide_key][shape_name] = {"paragraphs": []}
                else:
                    # Clear other shapes (like description text)
                    replacements[slide_key][shape_name] = {"paragraphs": []}
            continue

        # Handle chart and timeline slides
        # These have visual elements we want to preserve - only update title
        if is_chart or is_timeline or is_table:
            title_text = content.get('title', '')

            # Find title shape (first shape at top with short height)
            title_shape = None
            for shape_name, shape_info in sorted_shapes:
                height = shape_info.get('height', 1)
                top = shape_info.get('top', 5)
                if top < 1.2 and height < 0.5 and title_shape is None:
                    title_shape = shape_name
                    break

            # Apply replacements - only update title, preserve other content
            for shape_name, shape_info in sorted_shapes:
                if shape_name == title_shape and title_text:
                    replacements[slide_key][shape_name] = {
                        "paragraphs": [{"text": title_text, "font_name": NBG_FONT, "bold": True, "color": colors['title']}]
                    }
                # Preserve other shapes - don't add to replacements
            continue

        # Default: for unknown slide types, preserve template content
        # This handles edge cases where slide type isn't recognized
        for shape_name, shape_info in sorted_shapes:
            # Only set title if we have one
            if 'title' in content and shape_info.get('top', 5) < 1.5 and shape_info.get('height', 1) < 0.5:
                replacements[slide_key][shape_name] = {
                    "paragraphs": [{"text": content['title'], "font_name": NBG_FONT, "bold": True, "color": colors['title']}]
                }
                break

    return replacements


def main():
    if len(sys.argv) < 3:
        print("NBG Presentation Builder")
        print("=" * 40)
        print("\nUsage: python nbg_build.py <outline.yaml> <output.pptx>")
        print("\nExample outline.yaml:")
        print("""
template: GR

slides:
  - type: covers/simple_white
    content:
      title: "Presentation Title"
      subtitle: "Subtitle"
      date: "February 2026"

  - type: content/text_with_bullets
    content:
      title: "Section Title"
      paragraphs:
        - text: "First bullet point"
          bullet: true
        - text: "Second bullet point"
          bullet: true

  - type: back_covers/plain_logo
""")
        sys.exit(1)

    try:
        build_presentation(sys.argv[1], sys.argv[2])
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
