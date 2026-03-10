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
PPTX_SCRIPTS = Path.home() / '.claude/plugins/cache/anthropic-agent-skills/document-skills/c74d647e56e6/document-skills/pptx/scripts'


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
        'kpi_dashboard': 'content/text_with_bullets',      # Simpler than infographic
        'numbered_infographic': 'content/text_with_bullets', # Simpler than infographic
        'timeline': 'content/text_with_bullets',            # Simpler than infographic
        'process': 'content/text_with_bullets',             # Simpler than infographic
        'funnel': 'content/text_with_bullets',              # Simpler than infographic
        'table': 'tables/half_page',
        'comparison_table': 'tables/comparison',
        'icons': 'content/text_with_bullets',               # Simpler than infographic
        'none': 'content/text_with_bullets',
    }

    # If recommended_visual is provided and matches, use it
    if recommended_visual and recommended_visual in visual_mapping:
        return visual_mapping[recommended_visual]

    # Map base McKinsey types to catalog paths
    # Using "quiet" variants by default - cleaner designs without decorative elements
    type_mapping = {
        'cover': 'covers/quiet',              # Minimal cover (slide 21)
        'divider': 'dividers/quiet_white',    # Clean divider with simple rect (slide 72)
        'content': 'content/text_with_bullets',
        'chart': 'charts/bar_dual',
        'infographic': 'infographics/numbered_6',
        'table': 'tables/half_page',
        'thankyou': 'back_covers/quiet',      # Truly empty slide (slide 190)
        'back_cover': 'back_covers/quiet',    # Truly empty slide (slide 190)
        'summary': 'content/text_with_bullets',
    }

    return type_mapping.get(slide_type, 'content/text_with_bullets')


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"  {description}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"    Warning: {result.stderr.split(chr(10))[0]}")
        return False
    return True


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
        cmd = [
            'python', str(PPTX_SCRIPTS / 'rearrange.py'),
            str(template_path), str(working),
            ','.join(str(i) for i in indices)
        ]
        if not run_command(cmd, "Rearranging"):
            raise RuntimeError("Failed to rearrange slides")

        # Step 2: Extract inventory
        print(f"\n[2/4] Analyzing slide structure...")
        inventory_file = temp / 'inventory.json'
        cmd = [
            'python', str(PPTX_SCRIPTS / 'inventory.py'),
            str(working), str(inventory_file)
        ]
        run_command(cmd, "Extracting inventory")

        with open(inventory_file, 'r') as f:
            inventory = json.load(f)

        # Step 3: Build smart replacements
        print(f"\n[3/4] Preparing content...")
        replacements = build_smart_replacements(slides, inventory, resolved_types)

        replacements_file = temp / 'replacements.json'
        with open(replacements_file, 'w') as f:
            json.dump(replacements, f, indent=2)

        # Step 4: Apply replacements
        print(f"\n[4/4] Applying content...")
        final = temp / 'final.pptx'
        cmd = [
            'python', str(PPTX_SCRIPTS / 'replace.py'),
            str(working), str(replacements_file), str(final)
        ]

        success = run_command(cmd, "Replacing text")

        # Use the best available output
        if final.exists():
            shutil.copy(final, output_path)
        else:
            shutil.copy(working, output_path)
            print("  Using template (text replacement skipped)")

    # Clear static slide numbers from template
    print("\n[5/5] Cleaning up slide numbers...")
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
                        "paragraphs": [{"text": content['number'], "font_name": NBG_FONT, "bold": True, "color": colors['number']}]
                    }
                elif shape_name == title_shape and 'title' in content:
                    replacements[slide_key][shape_name] = {
                        "paragraphs": [{"text": content['title'], "font_name": NBG_FONT, "bold": True, "color": colors['title']}]
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
            # Cover slides: map title, subtitle, location, date to shapes in order
            # Use accessible colors based on background
            content_items = []
            if 'title' in content:
                content_items.append({'text': content['title'], 'font_name': NBG_FONT, 'bold': True, 'color': colors['title']})
            if 'subtitle' in content:
                content_items.append({'text': content['subtitle'], 'font_name': NBG_FONT, 'color': colors['body']})
            if 'location' in content:
                content_items.append({'text': content['location'], 'font_name': NBG_FONT, 'color': colors['body']})
            if 'date' in content:
                content_items.append({'text': content['date'], 'font_name': NBG_FONT, 'color': colors['body']})

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

            # Build replacements with Aptos font and accessible colors
            for shape_name, shape_info in sorted_shapes:
                if shape_name == hyper_title_shape and hyper_text:
                    replacements[slide_key][shape_name] = {
                        "paragraphs": [{"text": hyper_text, "font_name": NBG_FONT, "color": colors['number']}]
                    }
                elif shape_name == title_shape and 'title' in content:
                    replacements[slide_key][shape_name] = {
                        "paragraphs": [{"text": content['title'], "font_name": NBG_FONT, "bold": True, "color": colors['title']}]
                    }
                elif shape_name == body_shape and body_content:
                    paras = []
                    for p in body_content:
                        if isinstance(p, dict):
                            para = {'text': p.get('text', ''), 'font_name': NBG_FONT, 'color': colors['body']}
                            if p.get('bullet'):
                                para['bullet'] = True
                                para['level'] = 0
                            paras.append(para)
                        else:
                            # McKinsey points are strings - convert to bullet points
                            paras.append({'text': str(p), 'font_name': NBG_FONT, 'bullet': True, 'level': 0, 'color': colors['body']})
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
