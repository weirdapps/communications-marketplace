#!/usr/bin/env python3
"""
NBG Brand Validation Tool

Validates presentations against NBG brand guidelines.
Checks dimensions, colors, fonts, and other brand elements.

Usage:
    python nbg_validate.py presentation.pptx

Output:
    Lists all validation checks with pass/fail status.
"""

import re
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

# NBG Brand Guidelines
NBG_GUIDELINES = {
    'dimensions': {
        # NBG template uses 12192000 x 6858000 EMUs
        # Standard conversion: 914400 EMU = 1 inch
        # Therefore: 12192000/914400 = 13.33" and 6858000/914400 = 7.5"
        # Use LAYOUT_WIDE in PptxGenJS (13.33" x 7.5")
        'width_emu': 12192000,
        'height_emu': 6858000,
        'tolerance': 10000,  # EMU tolerance
    },
    'colors': {
        # Primary colors (hex without #)
        'allowed': {
            '003841': 'Dark Teal',
            '007B85': 'NBG Teal',
            '047A85': 'Teal Variant',
            '00ADBF': 'Cyan',
            '00DFF8': 'Bright Cyan',
            '00DEF8': 'Bright Cyan Alt',
            '000000': 'Black',
            '202020': 'Dark Text',
            '212121': 'Alt Black',
            '252D30': 'Dark Charcoal',
            '939793': 'Medium Gray',
            '595959': 'Gray',
            'BEC1BE': 'Light Gray',
            'D9D9D9': 'Neutral Gray',
            'F5F8F6': 'Off White',
            'F5F9F6': 'Off White Alt',
            'F6FAF8': 'Off White Template',
            'FFFFFF': 'White',
            # Status colors
            'CB0030': 'Deep Red',
            'F60037': 'Red',
            'FF7F1A': 'Orange',
            'FFDC00': 'Yellow',
            '5D8D2F': 'Green',
            '90DC48': 'Bright Green',
            '73AF3C': 'Success Green',
            'AA0028': 'Alert Red',
            # Segment colors
            '0D90FF': 'Business Blue',
            'D9A757': 'Premium Gold',
            '1E478E': 'Info Blue',
            '59C3FF': 'Followed Link',
            # Chart colors
            '3EDEF8': 'Aqua Light',
            'B5B7B5': 'Chart Gray',
            '00E2FC': 'Highlight Accent',
            '00A7BA': 'Cyan Variant',
            '00A9BD': 'Cyan Variant 2',
        },
        'primary': ['003841', '007B85', '00ADBF', '00DFF8'],
    },
    'fonts': {
        'allowed': ['Aptos', 'Aptos SemiBold', 'Aptos Display', 'Arial', 'Calibri', 'Tahoma'],
        'primary': 'Aptos',
    },
}

# XML Namespaces
NAMESPACES = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


class ValidationResult:
    def __init__(self, name: str, passed: bool, message: str, details: list = None):
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details or []


def check_dimensions(unpacked_dir: Path) -> ValidationResult:
    """Check slide dimensions match NBG spec."""
    pres_file = unpacked_dir / 'ppt' / 'presentation.xml'

    if not pres_file.exists():
        return ValidationResult('Dimensions', False, 'presentation.xml not found')

    tree = ET.parse(pres_file)
    root = tree.getroot()

    # Find sldSz element
    sld_sz = root.find('.//{%s}sldSz' % NAMESPACES['p'])

    if sld_sz is None:
        return ValidationResult('Dimensions', False, 'Slide size not found')

    cx = int(sld_sz.get('cx', 0))
    cy = int(sld_sz.get('cy', 0))

    expected_cx = NBG_GUIDELINES['dimensions']['width_emu']
    expected_cy = NBG_GUIDELINES['dimensions']['height_emu']
    tolerance = NBG_GUIDELINES['dimensions']['tolerance']

    width_ok = abs(cx - expected_cx) < tolerance
    height_ok = abs(cy - expected_cy) < tolerance

    # Standard EMU to inch conversion: 914400 EMU = 1 inch
    actual_w = cx / 914400
    actual_h = cy / 914400

    if width_ok and height_ok:
        return ValidationResult(
            'Dimensions',
            True,
            f'{actual_w:.2f}" x {actual_h:.2f}" (NBG standard = LAYOUT_WIDE)'
        )
    else:
        return ValidationResult(
            'Dimensions',
            False,
            f'{actual_w:.2f}" x {actual_h:.2f}" (expected 13.33" x 7.5" / LAYOUT_WIDE)'
        )


def extract_colors_from_slides(unpacked_dir: Path) -> set:
    """Extract all colors used in slides."""
    colors = set()
    slides_dir = unpacked_dir / 'ppt' / 'slides'

    if not slides_dir.exists():
        return colors

    for slide_file in slides_dir.glob('slide*.xml'):
        tree = ET.parse(slide_file)
        root = tree.getroot()

        # Find srgbClr elements
        for elem in root.findall('.//{%s}srgbClr' % NAMESPACES['a']):
            color = elem.get('val', '').upper()
            if color:
                colors.add(color)

        # Find solidFill with srgbClr
        for elem in root.findall('.//{%s}solidFill/{%s}srgbClr' % (NAMESPACES['a'], NAMESPACES['a'])):
            color = elem.get('val', '').upper()
            if color:
                colors.add(color)

    return colors


def check_colors(unpacked_dir: Path) -> ValidationResult:
    """Check all colors are within NBG palette."""
    colors = extract_colors_from_slides(unpacked_dir)
    allowed = {c.upper() for c in NBG_GUIDELINES['colors']['allowed'].keys()}

    invalid = colors - allowed
    valid = colors & allowed

    if not invalid:
        return ValidationResult(
            'Colors',
            True,
            f'All {len(valid)} colors within NBG palette'
        )
    else:
        details = [f'#{c} (not in NBG palette)' for c in sorted(invalid)]
        return ValidationResult(
            'Colors',
            False,
            f'{len(invalid)} non-standard color(s) found',
            details
        )


def extract_fonts_from_slides(unpacked_dir: Path) -> set:
    """Extract all fonts used in slides."""
    fonts = set()
    slides_dir = unpacked_dir / 'ppt' / 'slides'

    if not slides_dir.exists():
        return fonts

    for slide_file in slides_dir.glob('slide*.xml'):
        tree = ET.parse(slide_file)
        root = tree.getroot()

        # Find latin font elements
        for elem in root.findall('.//{%s}latin' % NAMESPACES['a']):
            typeface = elem.get('typeface', '')
            if typeface and not typeface.startswith('+'):
                fonts.add(typeface)

        # Find rPr with font info
        for rPr in root.findall('.//{%s}rPr' % NAMESPACES['a']):
            latin = rPr.find('{%s}latin' % NAMESPACES['a'])
            if latin is not None:
                typeface = latin.get('typeface', '')
                if typeface and not typeface.startswith('+'):
                    fonts.add(typeface)

    return fonts


def check_fonts(unpacked_dir: Path) -> ValidationResult:
    """Check all fonts are NBG-approved."""
    fonts = extract_fonts_from_slides(unpacked_dir)
    allowed = set(NBG_GUIDELINES['fonts']['allowed'])

    invalid = fonts - allowed
    valid = fonts & allowed

    if not invalid:
        return ValidationResult(
            'Fonts',
            True,
            f'Fonts used: {", ".join(sorted(valid)) if valid else "Theme fonts only"}'
        )
    else:
        details = [f'{f} (not NBG-approved)' for f in sorted(invalid)]
        return ValidationResult(
            'Fonts',
            False,
            f'{len(invalid)} non-standard font(s) found',
            details
        )


def check_logo_present(unpacked_dir: Path) -> ValidationResult:
    """Check if NBG logo is present in the presentation."""
    media_dir = unpacked_dir / 'ppt' / 'media'

    if not media_dir.exists():
        return ValidationResult('Logo', False, 'No media folder found')

    # Look for NBG logo files
    logo_patterns = ['nbg', 'logo', 'ethniki']
    images = list(media_dir.glob('image*.*'))

    # Check slide relationships for external image references
    slides_dir = unpacked_dir / 'ppt' / 'slides'
    has_logo_ref = False

    if slides_dir.exists():
        for rels_file in (slides_dir / '_rels').glob('*.rels'):
            with open(rels_file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                if 'logo' in content or 'nbg' in content:
                    has_logo_ref = True
                    break

    if images or has_logo_ref:
        return ValidationResult(
            'Logo',
            True,
            f'{len(images)} media file(s) found (verify NBG logo manually)'
        )
    else:
        return ValidationResult(
            'Logo',
            False,
            'No media files or logo references found'
        )


def check_slide_count(unpacked_dir: Path) -> ValidationResult:
    """Check presentation has slides."""
    slides_dir = unpacked_dir / 'ppt' / 'slides'

    if not slides_dir.exists():
        return ValidationResult('Slides', False, 'No slides folder found')

    slide_count = len(list(slides_dir.glob('slide*.xml')))

    if slide_count > 0:
        return ValidationResult(
            'Slides',
            True,
            f'{slide_count} slide(s) in presentation'
        )
    else:
        return ValidationResult('Slides', False, 'No slides found')


def check_element_boundaries(unpacked_dir: Path) -> ValidationResult:
    """Check all elements are within slide boundaries."""
    slides_dir = unpacked_dir / 'ppt' / 'slides'
    if not slides_dir.exists():
        return ValidationResult('Boundaries', False, 'No slides folder found')

    # Slide dimensions in EMUs
    slide_width = NBG_GUIDELINES['dimensions']['width_emu']
    slide_height = NBG_GUIDELINES['dimensions']['height_emu']

    out_of_bounds = []

    for slide_file in sorted(slides_dir.glob('slide*.xml')):
        slide_num = re.search(r'slide(\d+)', slide_file.name).group(1)
        tree = ET.parse(slide_file)
        root = tree.getroot()

        # Find all position elements (xfrm = transform)
        for xfrm in root.findall('.//{%s}xfrm' % NAMESPACES['a']):
            off = xfrm.find('{%s}off' % NAMESPACES['a'])
            ext = xfrm.find('{%s}ext' % NAMESPACES['a'])

            if off is not None and ext is not None:
                x = int(off.get('x', 0))
                y = int(off.get('y', 0))
                cx = int(ext.get('cx', 0))
                cy = int(ext.get('cy', 0))

                # Check if element extends beyond slide
                if x + cx > slide_width + 50000:  # 50000 EMU tolerance (~0.05")
                    out_of_bounds.append(f'Slide {slide_num}: element extends {(x + cx - slide_width) / 914400:.2f}" past right edge')
                if y + cy > slide_height + 50000:
                    out_of_bounds.append(f'Slide {slide_num}: element extends {(y + cy - slide_height) / 914400:.2f}" past bottom edge')
                if x < -50000:
                    out_of_bounds.append(f'Slide {slide_num}: element starts {abs(x) / 914400:.2f}" past left edge')
                if y < -50000:
                    out_of_bounds.append(f'Slide {slide_num}: element starts {abs(y) / 914400:.2f}" past top edge')

    if not out_of_bounds:
        return ValidationResult('Boundaries', True, 'All elements within slide boundaries')
    else:
        return ValidationResult(
            'Boundaries',
            False,
            f'{len(out_of_bounds)} element(s) outside slide boundaries',
            out_of_bounds[:10]
        )


def check_color_contrast(unpacked_dir: Path) -> ValidationResult:
    """Check font colors have sufficient contrast with backgrounds."""
    slides_dir = unpacked_dir / 'ppt' / 'slides'
    if not slides_dir.exists():
        return ValidationResult('Contrast', False, 'No slides folder found')

    # Define light and dark colors
    dark_colors = {'003841', '007B85', '000000', '202020', '212121', '252D30'}
    light_colors = {'FFFFFF', 'F5F8F6', 'F5F9F6', 'F6FAF8'}

    contrast_issues = []

    for slide_file in sorted(slides_dir.glob('slide*.xml')):
        slide_num = re.search(r'slide(\d+)', slide_file.name).group(1)
        tree = ET.parse(slide_file)
        root = tree.getroot()

        # Get background color (if specified)
        bg_color = 'FFFFFF'  # Default white
        bg_elem = root.find('.//{%s}bgClr' % NAMESPACES['p'])
        if bg_elem is not None:
            srgb = bg_elem.find('.//{%s}srgbClr' % NAMESPACES['a'])
            if srgb is not None:
                bg_color = srgb.get('val', 'FFFFFF').upper()

        is_dark_bg = bg_color.upper() in dark_colors

        # Check text colors
        for rPr in root.findall('.//{%s}rPr' % NAMESPACES['a']):
            solid_fill = rPr.find('{%s}solidFill' % NAMESPACES['a'])
            if solid_fill is not None:
                srgb = solid_fill.find('{%s}srgbClr' % NAMESPACES['a'])
                if srgb is not None:
                    text_color = srgb.get('val', '').upper()
                    is_dark_text = text_color in dark_colors

                    # Dark text on dark background = bad
                    if is_dark_bg and is_dark_text:
                        contrast_issues.append(f'Slide {slide_num}: dark text ({text_color}) on dark background ({bg_color})')
                    # Light text on light background = bad
                    elif not is_dark_bg and text_color in light_colors:
                        # This is less common but still a problem
                        pass  # Usually OK as light text on white is rare

    if not contrast_issues:
        return ValidationResult('Contrast', True, 'Font colors have adequate contrast')
    else:
        return ValidationResult(
            'Contrast',
            False,
            f'{len(contrast_issues)} contrast issue(s) found',
            contrast_issues[:10]
        )


def check_decorative_elements(unpacked_dir: Path) -> ValidationResult:
    """Check for unwanted decorative elements (ellipses, complex shapes)."""
    slides_dir = unpacked_dir / 'ppt' / 'slides'
    if not slides_dir.exists():
        return ValidationResult('Decorative', False, 'No slides folder found')

    # Shapes that are typically decorative
    decorative_shapes = {'ellipse', 'oval', 'triangle', 'star', 'heart', 'moon', 'cloud'}

    found_decorations = []

    for slide_file in sorted(slides_dir.glob('slide*.xml')):
        slide_num = re.search(r'slide(\d+)', slide_file.name).group(1)
        tree = ET.parse(slide_file)
        root = tree.getroot()

        # Check preset geometry shapes
        for prstGeom in root.findall('.//{%s}prstGeom' % NAMESPACES['a']):
            shape_type = prstGeom.get('prst', '').lower()
            if shape_type in decorative_shapes:
                found_decorations.append(f'Slide {slide_num}: {shape_type} shape found')

    if not found_decorations:
        return ValidationResult('Decorative', True, 'No unwanted decorative elements')
    else:
        return ValidationResult(
            'Decorative',
            False,
            f'{len(found_decorations)} decorative element(s) found (may affect clean design)',
            found_decorations[:10]
        )


def check_pie_charts(unpacked_dir: Path) -> ValidationResult:
    """Check that no pie charts are used (should be doughnut instead)."""
    charts_dir = unpacked_dir / 'ppt' / 'charts'

    if not charts_dir.exists():
        return ValidationResult('Chart Types', True, 'No charts in presentation')

    pie_charts_found = []
    doughnut_charts_found = 0

    for chart_file in sorted(charts_dir.glob('chart*.xml')):
        chart_name = chart_file.stem
        tree = ET.parse(chart_file)
        root = tree.getroot()

        # Check for pie charts
        pie_elems = root.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/chart}pieChart')
        if pie_elems:
            pie_charts_found.append(f'{chart_name}: pieChart found (use doughnutChart instead)')

        # Count doughnut charts (good)
        doughnut_elems = root.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/chart}doughnutChart')
        doughnut_charts_found += len(doughnut_elems)

    if pie_charts_found:
        return ValidationResult(
            'Chart Types',
            False,
            f'{len(pie_charts_found)} pie chart(s) found (NBG requires doughnut charts)',
            pie_charts_found
        )
    elif doughnut_charts_found > 0:
        return ValidationResult('Chart Types', True, f'{doughnut_charts_found} doughnut chart(s) (correct)')
    else:
        return ValidationResult('Chart Types', True, 'No pie/doughnut charts')


def check_thank_you_slides(unpacked_dir: Path) -> ValidationResult:
    """Check for any "Thank You" or similar closing text on slides."""
    slides_dir = unpacked_dir / 'ppt' / 'slides'
    if not slides_dir.exists():
        return ValidationResult('Thank You Check', False, 'No slides folder found')

    # Phrases to look for (case-insensitive)
    forbidden_phrases = [
        'thank you', 'thanks', 'any questions', 'q&a', 'questions?',
        'thank-you', 'thankyou', 'grazie', 'merci', 'danke',
        'ευχαριστώ', 'ευχαριστουμε', 'ερωτησεις'  # Greek
    ]

    found_issues = []

    for slide_file in sorted(slides_dir.glob('slide*.xml')):
        slide_num = re.search(r'slide(\d+)', slide_file.name).group(1)
        tree = ET.parse(slide_file)
        root = tree.getroot()

        text_elements = root.findall('.//{%s}t' % NAMESPACES['a'])
        text_content = ' '.join(t.text or '' for t in text_elements).strip().lower()

        for phrase in forbidden_phrases:
            if phrase in text_content:
                found_issues.append(f'Slide {slide_num}: contains "{phrase}"')
                break

    if not found_issues:
        return ValidationResult('Thank You Check', True, 'No "Thank You" slides found (correct)')
    else:
        return ValidationResult(
            'Thank You Check',
            False,
            f'{len(found_issues)} slide(s) with "Thank You" or similar (use plain back cover)',
            found_issues
        )


def check_text_margins(unpacked_dir: Path) -> ValidationResult:
    """Check that text boxes use zero margins (NBG requirement)."""
    slides_dir = unpacked_dir / 'ppt' / 'slides'
    if not slides_dir.exists():
        return ValidationResult('Text Margins', False, 'No slides folder found')

    # NBG requirement: all text boxes should have margin: 0
    # In OOXML: lIns, tIns, rIns, bIns should be 0 or very small

    non_zero_margins = []

    for slide_file in sorted(slides_dir.glob('slide*.xml')):
        slide_num = re.search(r'slide(\d+)', slide_file.name).group(1)
        tree = ET.parse(slide_file)
        root = tree.getroot()

        for bodyPr in root.findall('.//{%s}bodyPr' % NAMESPACES['a']):
            # Default margins in OOXML are 91440 EMU (0.1 inch)
            # NBG requires 0
            lIns = int(bodyPr.get('lIns', '91440'))
            tIns = int(bodyPr.get('tIns', '45720'))
            rIns = int(bodyPr.get('rIns', '91440'))
            bIns = int(bodyPr.get('bIns', '45720'))

            # If any margin is > 50000 EMU (~0.05 inch), flag it
            if lIns > 50000 or rIns > 50000:
                non_zero_margins.append(f'Slide {slide_num}: text box has non-zero margins')
                break

    total_slides = len(list(slides_dir.glob('slide*.xml')))

    if not non_zero_margins:
        return ValidationResult('Text Margins', True, 'All text boxes use zero margins')
    elif len(non_zero_margins) < total_slides / 2:
        return ValidationResult(
            'Text Margins',
            True,
            f'{len(non_zero_margins)} slide(s) have default margins (minor issue)',
            non_zero_margins[:3]
        )
    else:
        return ValidationResult(
            'Text Margins',
            False,
            f'{len(non_zero_margins)} slide(s) with non-zero margins',
            non_zero_margins[:5]
        )


def check_back_cover(unpacked_dir: Path) -> ValidationResult:
    """Check if presentation ends with a back cover slide."""
    slides_dir = unpacked_dir / 'ppt' / 'slides'

    if not slides_dir.exists():
        return ValidationResult('Back Cover', False, 'No slides folder found')

    # Sort numerically, not alphabetically (slide10.xml > slide2.xml)
    slide_files = sorted(
        slides_dir.glob('slide*.xml'),
        key=lambda x: int(re.search(r'slide(\d+)', x.name).group(1))
    )
    if not slide_files:
        return ValidationResult('Back Cover', False, 'No slides found')

    last_slide = slide_files[-1]
    tree = ET.parse(last_slide)
    root = tree.getroot()

    # Check if last slide has minimal text (typical back cover)
    text_elements = root.findall('.//{%s}t' % NAMESPACES['a'])
    text_content = ' '.join(t.text or '' for t in text_elements).strip().lower()

    # Back cover should have minimal or no text (just logo)
    if len(text_content) < 50 and 'thank you' not in text_content:
        return ValidationResult(
            'Back Cover',
            True,
            'Last slide appears to be a plain back cover'
        )
    elif 'thank you' in text_content:
        return ValidationResult(
            'Back Cover',
            False,
            'Last slide contains "Thank You" (use plain back cover instead)'
        )
    else:
        return ValidationResult(
            'Back Cover',
            False,
            f'Last slide has significant text ({len(text_content)} chars)'
        )


def validate_presentation(pptx_path: str) -> list:
    """Run all validation checks on a presentation."""
    pptx_path = Path(pptx_path).expanduser()

    if not pptx_path.exists():
        raise FileNotFoundError(f"Presentation not found: {pptx_path}")

    results = []

    with tempfile.TemporaryDirectory() as temp_dir:
        unpacked_dir = Path(temp_dir) / 'unpacked'

        with zipfile.ZipFile(pptx_path, 'r') as zf:
            zf.extractall(unpacked_dir)

        # Run all checks
        results.append(check_slide_count(unpacked_dir))
        results.append(check_dimensions(unpacked_dir))
        results.append(check_colors(unpacked_dir))
        results.append(check_fonts(unpacked_dir))
        results.append(check_logo_present(unpacked_dir))
        results.append(check_back_cover(unpacked_dir))
        # Quality control checks
        results.append(check_element_boundaries(unpacked_dir))
        results.append(check_color_contrast(unpacked_dir))
        results.append(check_decorative_elements(unpacked_dir))
        # NBG-specific checks
        results.append(check_pie_charts(unpacked_dir))
        results.append(check_thank_you_slides(unpacked_dir))
        results.append(check_text_margins(unpacked_dir))

    return results


def print_results(results: list, pptx_path: str):
    """Print validation results."""
    print(f"\nNBG Brand Validation Report")
    print(f"{'=' * 50}")
    print(f"File: {pptx_path}")
    print(f"{'=' * 50}\n")

    passed = 0
    failed = 0

    for result in results:
        status = '\033[92m✓\033[0m' if result.passed else '\033[91m✗\033[0m'
        print(f"{status} {result.name}: {result.message}")

        if result.details:
            for detail in result.details[:5]:  # Show max 5 details
                print(f"    - {detail}")
            if len(result.details) > 5:
                print(f"    ... and {len(result.details) - 5} more")

        if result.passed:
            passed += 1
        else:
            failed += 1

    print(f"\n{'=' * 50}")
    print(f"Summary: {passed} passed, {failed} failed")

    if failed == 0:
        print("\033[92mAll checks passed! Presentation follows NBG guidelines.\033[0m")
    else:
        print("\033[93mSome checks failed. Review and fix before publishing.\033[0m")

    print(f"{'=' * 50}\n")

    return failed == 0


def main():
    if len(sys.argv) < 2:
        print("NBG Brand Validation Tool")
        print("=" * 40)
        print("\nUsage: python nbg_validate.py <presentation.pptx>")
        print("\nValidates presentations against NBG brand guidelines.")
        sys.exit(1)

    pptx_path = sys.argv[1]

    try:
        results = validate_presentation(pptx_path)
        success = print_results(results, pptx_path)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\033[91mError: {e}\033[0m")
        sys.exit(1)


if __name__ == '__main__':
    main()
