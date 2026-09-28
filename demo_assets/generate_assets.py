import os
import base64
from pathlib import Path

def create_svg_image(filepath, title, subtitle, color_theme, icon_type, defect_badge=None):
    width = 600
    height = 400
    
    # Theme colors
    bg1 = color_theme.get("bg1", "#1E293B")
    bg2 = color_theme.get("bg2", "#0F172A")
    accent = color_theme.get("accent", "#38BDF8")
    badge_bg = color_theme.get("badge_bg", "#EF4444")
    
    badge_svg = ""
    if defect_badge:
        badge_svg = f'''
        <rect x="30" y="30" width="180" height="34" rx="8" fill="{badge_bg}" opacity="0.9" />
        <text x="45" y="52" fill="#FFFFFF" font-family="Arial, sans-serif" font-weight="bold" font-size="13">
            {defect_badge}
        </text>
        '''
        
    icon_content = ""
    if icon_type == "fan_broken":
        icon_content = '''
        <!-- Ceiling Fan Broken -->
        <circle cx="300" cy="180" r="28" fill="#64748B" />
        <line x1="300" y1="180" x2="300" y2="80" stroke="#EF4444" stroke-width="12" stroke-linecap="round" stroke-dasharray="10,5" />
        <line x1="300" y1="180" x2="400" y2="240" stroke="#94A3B8" stroke-width="12" stroke-linecap="round" />
        <line x1="300" y1="180" x2="190" y2="210" stroke="#EF4444" stroke-width="12" stroke-linecap="round" transform="rotate(25 190 210)" />
        <path d="M 285 100 Q 295 120 270 140" stroke="#F59E0B" stroke-width="4" fill="none" stroke-dasharray="4,4" />
        <text x="315" y="110" fill="#EF4444" font-family="Arial" font-size="12" font-weight="bold">BLADE BENT & LOOSE</text>
        '''
    elif icon_type == "fan_fixed":
        icon_content = '''
        <!-- Ceiling Fan Repaired -->
        <circle cx="300" cy="180" r="30" fill="#10B981" />
        <line x1="300" y1="180" x2="300" y2="70" stroke="#E2E8F0" stroke-width="14" stroke-linecap="round" />
        <line x1="300" y1="180" x2="400" y2="240" stroke="#E2E8F0" stroke-width="14" stroke-linecap="round" />
        <line x1="300" y1="180" x2="200" y2="240" stroke="#E2E8F0" stroke-width="14" stroke-linecap="round" />
        <circle cx="300" cy="180" r="14" fill="#047857" />
        <text x="235" y="275" fill="#10B981" font-family="Arial" font-size="13" font-weight="bold">REPAIRED & BALANCED</text>
        '''
    elif icon_type == "room_scan":
        icon_content = '''
        <!-- Wide Classroom with 3 Callout Zones -->
        <!-- Blackboard -->
        <rect x="80" y="80" width="440" height="130" rx="6" fill="#1E3A2F" stroke="#475569" stroke-width="4" />
        <text x="210" y="150" fill="#6EE7B7" font-family="Arial" font-size="18" opacity="0.6">CLASSROOM 204</text>
        
        <!-- Defect 1: Tube Light Zone -->
        <rect x="100" y="55" width="140" height="16" fill="#F87171" opacity="0.8" />
        <rect x="90" y="45" width="160" height="35" fill="none" stroke="#EF4444" stroke-width="2" stroke-dasharray="6,4" />
        <rect x="255" y="45" width="80" height="20" rx="4" fill="#EF4444" />
        <text x="260" y="59" fill="#FFFFFF" font-family="Arial" font-size="10" font-weight="bold">1. Broken Light</text>

        <!-- Defect 2: Broken Fan Zone -->
        <circle cx="430" cy="110" r="22" fill="#64748B" />
        <line x1="430" y1="110" x2="430" y2="70" stroke="#EF4444" stroke-width="8" stroke-linecap="round" />
        <line x1="430" y1="110" x2="480" y2="130" stroke="#64748B" stroke-width="8" stroke-linecap="round" />
        <rect x="390" y="60" width="110" height="85" fill="none" stroke="#F59E0B" stroke-width="2" stroke-dasharray="6,4" />
        <rect x="400" y="150" width="95" height="20" rx="4" fill="#F59E0B" />
        <text x="405" y="164" fill="#000000" font-family="Arial" font-size="10" font-weight="bold">2. Damaged Fan</text>

        <!-- Defect 3: Broken Bench Zone -->
        <rect x="180" y="240" width="240" height="60" rx="4" fill="#78350F" />
        <line x1="200" y1="300" x2="200" y2="345" stroke="#451A03" stroke-width="10" />
        <line x1="390" y1="300" x2="415" y2="345" stroke="#EF4444" stroke-width="10" stroke-linecap="round" transform="rotate(20 415 345)" />
        <rect x="165" y="230" width="270" height="125" fill="none" stroke="#3B82F6" stroke-width="2" stroke-dasharray="6,4" />
        <rect x="240" y="325" width="120" height="20" rx="4" fill="#3B82F6" />
        <text x="248" y="339" fill="#FFFFFF" font-family="Arial" font-size="10" font-weight="bold">3. Cracked Bench Leg</text>
        '''
    elif icon_type == "water_leak":
        icon_content = '''
        <!-- Plumbing Leak -->
        <rect x="250" y="70" width="100" height="25" rx="4" fill="#94A3B8" />
        <line x1="300" y1="95" x2="300" y2="220" stroke="#64748B" stroke-width="22" stroke-linecap="square" />
        <line x1="300" y1="180" x2="420" y2="180" stroke="#64748B" stroke-width="20" stroke-linecap="round" />
        <!-- Leak Joint -->
        <circle cx="300" cy="180" r="16" fill="#0284C7" />
        <!-- Water Spray -->
        <path d="M 300 180 Q 240 210 220 270" stroke="#38BDF8" stroke-width="4" fill="none" stroke-dasharray="5,5" />
        <path d="M 300 180 Q 270 230 260 290" stroke="#38BDF8" stroke-width="6" fill="none" stroke-dasharray="6,4" />
        <!-- Puddle -->
        <ellipse cx="280" cy="330" rx="110" ry="25" fill="#0284C7" opacity="0.6" />
        <text x="320" y="240" fill="#EF4444" font-family="Arial" font-size="12" font-weight="bold">BURST VALVE LEAK</text>
        '''

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
        <defs>
            <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="{bg1}" />
                <stop offset="100%" stop-color="{bg2}" />
            </linearGradient>
        </defs>
        <rect width="{width}" height="{height}" fill="url(#bg)" />
        
        <!-- Floor grid perspective -->
        <line x1="0" y1="360" x2="{width}" y2="360" stroke="#334155" stroke-width="2" />
        <line x1="100" y1="360" x2="0" y2="400" stroke="#334155" stroke-width="1.5" />
        <line x1="300" y1="360" x2="300" y2="400" stroke="#334155" stroke-width="1.5" />
        <line x1="500" y1="360" x2="600" y2="400" stroke="#334155" stroke-width="1.5" />

        {badge_svg}
        {icon_content}

        <!-- Bottom bar info -->
        <rect x="0" y="365" width="{width}" height="35" fill="#0B132B" opacity="0.9" />
        <text x="25" y="388" fill="#F8FAFC" font-family="Arial, sans-serif" font-weight="bold" font-size="13">{title}</text>
        <text x="400" y="388" fill="{accent}" font-family="Arial, sans-serif" font-size="11">{subtitle}</text>
    </svg>'''

    with open(filepath, "w") as f:
        f.write(svg_content)
    print(f"Created demo asset: {filepath}")

def main():
    assets_dir = str(Path(__file__).resolve().parent)
    os.makedirs(assets_dir, exist_ok=True)

    create_svg_image(
        f"{assets_dir}/classroom_fan_broken.svg",
        "Block B / Room 204 — Ceiling Fan",
        "DEFECT: Bent Blade / Motor Fault",
        {"bg1": "#1E293B", "bg2": "#0F172A", "accent": "#F87171", "badge_bg": "#DC2626"},
        "fan_broken",
        "⚠️ REPORTED FAULT"
    )

    create_svg_image(
        f"{assets_dir}/classroom_fan_fixed.svg",
        "Block B / Room 204 — Ceiling Fan",
        "REPAIRED: Replaced 3-Blade Unit",
        {"bg1": "#064E3B", "bg2": "#022C22", "accent": "#34D399", "badge_bg": "#059669"},
        "fan_fixed",
        "✅ AFTER REPAIR"
    )

    create_svg_image(
        f"{assets_dir}/classroom_wide_scan.svg",
        "Classroom 204 — Panoramic Scan",
        "3 Candidate Issues Detected",
        {"bg1": "#1E1E2E", "bg2": "#11111B", "accent": "#89B4FA", "badge_bg": "#6366F1"},
        "room_scan",
        "🔍 ROOM SCAN MODE"
    )

    create_svg_image(
        f"{assets_dir}/washroom_leak.svg",
        "Block C / 2nd Fl Washroom — Water Pipe",
        "DEFECT: High-Pressure Joint Leak",
        {"bg1": "#0C4A6E", "bg2": "#082F49", "accent": "#38BDF8", "badge_bg": "#0284C7"},
        "water_leak",
        "⚠️ ACTIVE LEAK"
    )

if __name__ == "__main__":
    main()
