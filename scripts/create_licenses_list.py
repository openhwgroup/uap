#!/usr/bin/env python3

# -----------------------------------------------------------------------------
#  Copyright (C) 2026 Eclipse Foundation
#  
#  This program and the accompanying materials are made
#  available under the terms of the Eclipse Public License 2.0
#  which is available at https://www.eclipse.org/legal/epl-2.0/
#  
#  SPDX-License-Identifier: EPL-2.0
# -----------------------------------------------------------------------------
#
# create_licenses_list.py

"""
Script to create the list of valid licenses, saved at cfg/licenses.json.
It obtains the latest official SPDX, from its GitHub repo, removing non 
essential information, and adding custom licenses at the end of the file.
"""

import json
import urllib.request
from pathlib import Path


def download_spdx_licenses():
    """Download SPDX license list from GitHub."""
    url = "https://raw.githubusercontent.com/spdx/license-list-data/main/json/licenses.json"
    
    # Create cfg directory, in case it does not exist
    cfg_dir = Path(__file__).parent.parent / "cfg"
    cfg_dir.mkdir(exist_ok=True)
    
    # Download the latest public SPDX license list
    print("Downloading SPDX license list...")
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))
    
    # Extract only the name and licenseId fields from each license
    licenses = []
    for item in data.get('licenses', []):
        filtered_item = {
            "name": item.get('name'),
            "licenseId": item.get('licenseId')
        }
        licenses.append(filtered_item)
    
    # Sort by licenseId for consistent ordering
    licenses.sort(key=lambda x: x.get('licenseId', ''))
    
    # Add custom license types at the end
    licenses.append({
        "name": "Proprietary",
        "licenseId": "Proprietary"
    })
    licenses.append({
        "name": "Others",
        "licenseId": "Others"
    })

    # Save to cfg/licenses.json
    output_path = cfg_dir / "licenses.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(licenses, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(licenses)} licenses to {output_path}")
    return len(licenses)


if __name__ == "__main__":
    download_spdx_licenses()
