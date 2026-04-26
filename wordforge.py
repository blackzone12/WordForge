#!/usr/bin/env python3
"""
WordForge: Custom Wordlist Generator for Pentesting
Usage: python wordforge.py
Cross-platform: Kali, Windows, Android Termux
"""

import argparse
import itertools
import os
import sys
from pathlib import Path

def get_user_input():
    print("\n🛠️  WordForge - Custom Wordlist Generator")
    print("------------------------------------------")
    print("Leave blank if unknown\n")
    
    details = {
        'name': input("Full name (e.g., John Doe): ").strip().lower(),
        'nickname': input("Nickname/Handle: ").strip().lower(),
        'birth_year': input("Birth year (e.g., 1990): ").strip(),
        'pet': input("Pet name: ").strip().lower(),
        'company': input("Company/School: ").strip().lower(),
        'partner': input("Partner's name: ").strip().lower(),
        'parents': input("Parents' names (comma sep): ").strip().lower().split(','),
        'children': input("Children's names (comma sep): ").strip().lower().split(','),
        'relatives': input("Relatives/Friends (comma sep): ").strip().lower().split(','),
        'past_city': input("Previous City/Town: ").strip().lower(),
        'school': input("School/University: ").strip().lower(),
        'team': input("Favorite Sports Team: ").strip().lower(),
        'anniversary': input("Important Year (e.g. Anniversary): ").strip(),
        'hobbies': input("Hobbies/Sports (comma sep): ").strip().lower().split(','),
        'city': input("Current City/Town: ").strip().lower(),
        'phone_prefix': input("Phone prefix (e.g., 123): ").strip(),
        'others': input("Other keywords (comma sep): ").strip().lower().split(','),
    }
    
    # Process lists to remove empty strings
    for key in ['parents', 'children', 'relatives', 'hobbies', 'others']:
        details[key] = [w.strip() for w in details[key] if w.strip()]
        
    # Extra keywords from full name
    name_parts = details['name'].split()
    details['name_parts'] = name_parts
    
    # Collective bases for permutation
    details['raw_bases'] = [] # will be filled in generate
    return details

def leet_transform(word):
    # Expanded leet combinations
    transformations = {
        'a': ['4', '@'],
        'e': ['3'],
        'i': ['1', '!'],
        'o': ['0'],
        's': ['5', '$'],
        't': ['7'],
        'l': ['1'],
        'g': ['9'],
        'b': ['8']
    }
    
    variants = {word}
    
    # Simple full transformations
    variants.add(word.translate(str.maketrans('aeiosltg', '43105719')))
    variants.add(word.translate(str.maketrans('aeiosltg', '@3!0$716')))
    
    # Capitalization variants often used in leet
    variants.add(word.capitalize().translate(str.maketrans('aeiosltg', '43105719')))
    
    return [v for v in variants if v != word]

def generate_permutations(details, count_limit=1000000):
    passwords = set()
    
    # Base words collection
    raw_bases = []
    if details['name']: raw_bases.append(details['name'])
    if details['nickname']: raw_bases.append(details['nickname'])
    if details['pet']: raw_bases.append(details['pet'])
    if details['company']: raw_bases.append(details['company'])
    if details['partner']: raw_bases.append(details['partner'])
    if details.get('city'): raw_bases.append(details['city'])
    if details.get('past_city'): raw_bases.append(details['past_city'])
    if details.get('school'): raw_bases.append(details['school'])
    if details.get('team'): raw_bases.append(details['team'])
    
    raw_bases.extend(details['name_parts'])
    raw_bases.extend(details['parents'])
    raw_bases.extend(details['children'])
    raw_bases.extend(details['relatives'])
    raw_bases.extend(details['hobbies'])
    raw_bases.extend(details['others'])
    
    raw_bases = list(set([b for b in raw_bases if b]))
    
    # Formatting variants for bases
    all_bases = set()
    for b in raw_bases:
        all_bases.add(b)
        all_bases.add(b.capitalize())
        all_bases.add(b.upper())
        if len(b) > 3:
            # First letter capitalized, last letter capitalized
            all_bases.add(b[:-1] + b[-1].upper())
        
        # Add leet variants
        for l in leet_transform(b):
            all_bases.add(l)
    
    # Date/Number components
    years = []
    if details['birth_year']:
        years.append(details['birth_year'])
        if len(details['birth_year']) == 4:
            years.append(details['birth_year'][2:])
    
    if details.get('anniversary'):
        years.append(details['anniversary'])
        if len(details['anniversary']) == 4:
            years.append(details['anniversary'][2:])
    
    numbers = ['123', '1234', '12345', '123456', '0', '1', '12', '123456789', '2023', '2024', '2025', '2026', '111', '777', '888', '69', '420']
    if details['phone_prefix']:
        numbers.append(details['phone_prefix'])
    
    symbols = ['!', '@', '#', '$', '?', '_', '.', '*', '%', '&']
    
    # 1. Base Variants (Direct)
    for b in all_bases:
        passwords.add(b)
        if len(passwords) >= count_limit: break

    # 2. Base + Numbers/Years
    if len(passwords) < count_limit:
        for b in all_bases:
            for n in numbers + years:
                passwords.add(b + n)
                passwords.add(n + b)
                if len(passwords) >= count_limit: break
            if len(passwords) >= count_limit: break

    # 3. Base + Symbols
    if len(passwords) < count_limit:
        for b in all_bases:
            for s in symbols:
                passwords.add(b + s)
                passwords.add(s + b)
                if len(passwords) >= count_limit: break
            if len(passwords) >= count_limit: break

    # 4. Double Base Combinations
    if len(passwords) < count_limit:
        # Cross join raw bases to keep it manageable
        for b1, b2 in itertools.permutations(raw_bases[:15], 2):
            combos = [
                b1 + b2,
                b1.capitalize() + b2,
                b1 + b2.capitalize(),
                b1.capitalize() + b2.capitalize(),
                b1 + '_' + b2,
                b1 + '.' + b2
            ]
            for c in combos:
                passwords.add(c)
                if len(passwords) >= count_limit: break
            if len(passwords) >= count_limit: break

    # 5. Base + Number + Symbol (High Priority)
    if len(passwords) < count_limit:
        for b in all_bases:
            for n in numbers[:8]:
                for s in symbols[:5]:
                    passwords.add(b + n + s)
                    passwords.add(b + s + n)
                    passwords.add(s + b + n)
                    if len(passwords) >= count_limit: break
                if len(passwords) >= count_limit: break
            if len(passwords) >= count_limit: break

    # 6. More complex patterns: Year + Base + Symbol
    if len(passwords) < count_limit and years:
        for y in years:
            for b in all_bases:
                for s in symbols[:5]:
                    passwords.add(y + b + s)
                    passwords.add(b + y + s)
                    if len(passwords) >= count_limit: break
                if len(passwords) >= count_limit: break

    # 8. Date Formats (DDMM, MMDD)
    if len(passwords) < count_limit:
        day_month = []
        for d in range(1, 32):
            for m in range(1, 13):
                day_month.append(f"{d:02d}{m:02d}")
                day_month.append(f"{m:02d}{d:02d}")
        
        for b in raw_bases[:5]: # limited to top bases
            for dm in day_month:
                passwords.add(b + dm)
                if len(passwords) >= count_limit: break
            if len(passwords) >= count_limit: break

    # 9. Triple Combinations (Very Aggressive)
    if len(passwords) < count_limit:
        for b in raw_bases[:10]:
            for n in numbers[:5]:
                for s in symbols[:3]:
                    for y in years[:1]:
                        passwords.add(b + n + s + y)
                        passwords.add(b + y + n + s)
                        if len(passwords) >= count_limit: break

    return sorted(list(passwords))[:count_limit]

def save_wordlist(passwords, filename):
    try:
        path = Path(filename)
        # Create directory if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            for pw in passwords:
                f.write(pw + '\n')
        print(f"💾 Saved {len(passwords):,} passwords to {path.absolute()}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")

def main():
    parser = argparse.ArgumentParser(description="WordForge: Custom Wordlist Generator")
    parser.add_argument('-o', '--output', default='custom_wordlist.txt', help='Output file')
    parser.add_argument('-l', '--limit', type=int, default=1000000, help='Max number of passwords (default 1M)')
    parser.add_argument('--non-interactive', action='store_true', help='Use example data (debugging)')
    
    # Specific fields for CLI usage
    parser.add_argument('--name', help='Full name')
    parser.add_argument('--year', help='Birth year')
    
    args = parser.parse_args()
    
    if args.name or args.year:
        # Simple CLI mode
        details = {
            'name': (args.name or "").lower(),
            'nickname': '',
            'birth_year': args.year or "",
            'pet': '',
            'company': '',
            'partner': '',
            'parents': [],
            'children': [],
            'relatives': [],
            'hobbies': [],
            'city': '',
            'phone_prefix': '',
            'others': [],
            'name_parts': (args.name or "").lower().split()
        }
    elif args.non_interactive:
        details = {
            'name': 'john doe',
            'nickname': 'johny',
            'birth_year': '1990',
            'pet': 'max',
            'company': 'techcorp',
            'partner': 'jane',
            'parents': ['will', 'mary'],
            'children': ['billy'],
            'relatives': ['bob'],
            'hobbies': ['football'],
            'city': 'london',
            'past_city': 'manchester',
            'school': 'oxford',
            'team': 'united',
            'anniversary': '2015',
            'phone_prefix': '123',
            'others': ['secret'],
            'name_parts': ['john', 'doe']
        }
    else:
        details = get_user_input()
    
    print("\n⚙️  Forging passwords...")
    passwords = generate_permutations(details, count_limit=args.limit)
    
    output_path = args.output
    # If using default filename and we have a target name, use results/{name}.txt
    if output_path == 'custom_wordlist.txt':
        target_name = details.get('name', 'unknown').replace(' ', '_')
        if not target_name: target_name = 'unknown'
        output_path = os.path.join('results', f"{target_name}.txt")

    save_wordlist(passwords, output_path)
    
    print(f"\n📊 Generated {len(passwords):,} targeted passwords")
    print(f"🎯 Ready for ripcrack: ./ripcrack crack {output_path}")

if __name__ == "__main__":
    main()
