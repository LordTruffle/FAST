import os
import json
import gzip
import requests
import uuid
from io import BytesIO

# --- CONFIGURAZIONE ---
OUTPUT_DIR = "playlists"
REGIONS = ['it', 'us', 'gb', 'de', 'es', 'fr', 'at', 'ch', 'ca', 'all'] 

SOURCES = {
    'samsung': 'https://i.mjh.nz/SamsungTVPlus/.channels.json.gz',
    'pluto': 'https://i.mjh.nz/PlutoTV/.channels.json.gz',
    'rakuten': 'https://i.mjh.nz/RakutenTV/.channels.json.gz',
    'plex': 'https://i.mjh.nz/Plex/.channels.json.gz',
    'roku': 'https://i.mjh.nz/Roku/.channels.json.gz'
}

def fetch_data(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    with gzip.GzipFile(fileobj=BytesIO(response.content)) as gz:
        return json.load(gz)

def run():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_channels_m3u = ['#EXTM3U']
    
    for service, url in SOURCES.items():
        print(f"--- Elaborazione {service.upper()} ---")
        try:
            data = fetch_data(url)
            # Controlliamo quali regioni sono effettivamente presenti nel file del servizio
            available_regions = data.get('regions', {}).keys()
            
            for region in REGIONS:
                if region not in available_regions:
                    continue
                
                print(f"Generando {service} per {region}...")
                channels = data['regions'][region].get('channels', {})
                region_m3u = [f'#EXTM3U url-tvg="https://i.mjh.nz/{service.capitalize()}/{region}.xml.gz"']
                
                for c_id, ch in channels.items():
                    if service == 'pluto':
                        stream_url = f"https://service-stitcher.clusters.pluto.tv/stitch/hls/channel/{c_id}/master.m3u8?advertisingId=&appName=web&appVersion=9.1.2&deviceDNT=0&deviceId={uuid.uuid4()}&deviceMake=Chrome&deviceModel=web&deviceType=web&deviceVersion=126.0.0&sid={uuid.uuid4()}&serverSideAds=true"
                    elif service == 'samsung':
                        slug = data.get('slug', '{id}').format(id=c_id)
                        stream_url = f"https://jmp2.uk/{slug}"
                    elif service == 'rakuten':
                        stream_url = f"https://jmp2.uk/rak-{c_id}.m3u8"
                    elif service == 'plex':
                        stream_url = f"https://jmp2.uk/plex-{c_id}.m3u8"
                    elif service == 'roku':
                        stream_url = f"https://jmp2.uk/roku-{c_id}.m3u8"
                    
                    group = f"{service.upper()} {region.upper()}"
                    extinf = f'#EXTINF:-1 tvg-id="{c_id}" tvg-logo="{ch["logo"]}" group-title="{group}",{ch["name"]}'
                    
                    region_m3u.append(extinf)
                    region_m3u.append(stream_url)
                    all_channels_m3u.append(extinf)
                    all_channels_m3u.append(stream_url)
                
                if len(region_m3u) > 1:
                    filename = f"{service}_{region}.m3u"
                    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
                        f.write("\n".join(region_m3u))
                    
        except Exception as e:
            print(f"Errore su {service}: {e}")

    with open(os.path.join(OUTPUT_DIR, "all_channels.m3u"), "w", encoding="utf-8") as f:
        f.write("\n".join(all_channels_m3u))

if __name__ == "__main__":
    run()
