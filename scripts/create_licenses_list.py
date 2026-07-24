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
    """Download SPDX license and exception lists from GitHub."""
    licenses_url = "https://raw.githubusercontent.com/spdx/license-list-data/main/json/licenses.json"
    exceptions_url = "https://raw.githubusercontent.com/spdx/license-list-data/main/json/exceptions.json"

    # Create cfg directory, in case it does not exist
    cfg_dir = Path(__file__).parent.parent / "cfg"
    cfg_dir.mkdir(exist_ok=True)

    # Download the latest public SPDX license list
    print("Downloading SPDX license list...")
    with urllib.request.urlopen(licenses_url) as response:
        licenses_data = json.loads(response.read().decode('utf-8'))

    # Download the latest public SPDX license exception list
    print("Downloading SPDX license exceptions...")
    with urllib.request.urlopen(exceptions_url) as response:
        exceptions_data = json.loads(response.read().decode('utf-8'))

    # Extract only the name and licenseId fields from each license
    combined_list = []
    for item in licenses_data.get('licenses', []):
        combined_list.append({
            "name": item.get('name') or 'Unknown',
            "licenseId": item.get('licenseId') or ''
        })

    # Extract only the name and licenseExceptionId (mapped to licenseId) from each exception
    for item in exceptions_data.get('exceptions', []):
        combined_list.append({
            "name": item.get('name') or 'Unknown',
            "licenseId": item.get('licenseExceptionId') or ''
        })

    # Sort by licenseId for consistent ordering
    combined_list.sort(key=lambda x: x.get('licenseId', ''))

    # Add custom license types at the end
    combined_list.append({
        "name": "Proprietary",
        "licenseId": "Proprietary"
    })
    combined_list.append({
        "name": "Others",
        "licenseId": "Others"
    })
    combined_list.append({
        "name": "NVIDIA Open NVDLA License and Agreement v1.0",
        "licenseId": "LicenseRef-NVIDIA-Open-NVDLA-1.0"
    })
    combined_list.append({
        "name": "INRIA Non-Commercial License Agreement",
        "licenseId": "inria-compcert"
    })
    combined_list.append({
        "name": "NXP SOFTWARE LICENSE AGREEMENT",
        "licenseId": "LA_OPT_NXP_Software_License"
    })

    # Save to cfg/licenses.json
    output_path = cfg_dir / "licenses.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(combined_list, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(combined_list)} licenses/exceptions to {output_path}")
    return len(combined_list)


if __name__ == "__main__":
    download_spdx_licenses()
