"""Validate manifest mappings, image decoding and the untouched supplier artwork.
Optional: python3 background-tests/verify_assets.py /path/to/supplied.zip
"""
import hashlib, json, sys, zipfile
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'data/backgrounds.json').read_text())
entries=[entry for entry in manifest['backgrounds'] if entry['src'] and entry['thumbnail'] and entry['status']!='excluded']
assert len(entries)==110 and len({entry['id'] for entry in entries})==110
assert len(manifest['categories'])==9
assert 'BG014' not in {entry['id'] for entry in entries}
assert sum(entry['status']=='review' for entry in entries)==7
for category in manifest['categories']:
 assert sum(entry['category']==category['name'] for entry in entries)==category['count']
checksums={}
for entry in entries:
 for key in ['src','thumbnail']:
  path=ROOT/'public'/entry[key].lstrip('/');Image.open(path).verify()
  checksums[entry[key]]=hashlib.sha256(path.read_bytes()).hexdigest()
if len(sys.argv)>1:
 with zipfile.ZipFile(sys.argv[1]) as archive:
  assert (ROOT/'data/backgrounds.json').read_bytes()==archive.read('manifest.json')
  for path,checksum in checksums.items(): assert hashlib.sha256(archive.read(path.lstrip('/'))).hexdigest()==checksum,path
report={'originals':len(entries),'thumbnails':len(entries),'categories':9,'reviewEntriesRetained':7,'BG014':'excluded','allImagesDecode':True,'sourceZipByteComparison':len(sys.argv)>1,'sha256':checksums}
(ROOT/'artifacts/backgrounds/asset-report.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: 110 originals, 110 thumbnails, 9 category assignments; all images decode; BG014 excluded; 7 review entries retained.' + (' All files match the source ZIP byte for byte.' if len(sys.argv)>1 else ''))
