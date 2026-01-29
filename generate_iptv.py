import os
import json
import gzip
import requests
import uuid
from io import BytesIO

# --- CONFIGURAZIONE ---
OUTPUT_DIR = "playlists"
REGIONS = ['it', 'us', 'gb', 'de', 'es', 'fr']
# Sorgenti MJH (le più affidabili)
SOURCES = {
    'samsung': 'https://i.mjh.nz/SamsungTVPlus/.channels.json.gz',
    'pluto': 'https://i.mjh.nz/PlutoTV/.channels.json.gz',
    'rakuten': 'https://i.mjh.nz/RakutenTV/.channels.json.gz'
}

def fetch_data(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    with gzip.GzipFile(fileobj=BytesIO(response.content)) as gz:
        return json.load(gz)

def run():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    for service, url in SOURCES.items():
        print(f"--- Elaborazione {service.upper()} ---")
        try:
            data = fetch_data(url)
            for region in REGIONS:
                if region not in data['regions']:
                    continue
                
                print(f"Generando {service} per {region}...")
                channels = data['regions'][region].get('channels', {})
                m3u_content = [f'#EXTM3U url-tvg="https://i.mjh.nz/{service.capitalize()}/{region}.xml.gz"']
                
                for c_id, ch in channels.items():
                    # --- LOGICA LINK PER SERVIZIO ---
                    
                    if service == 'pluto':
                        # Link ottimizzato per Pluto con parametri di sessione
                        stream_url = f"https://service-stitcher.clusters.pluto.tv/stitch/hls/channel/{c_id}/master.m3u8?advertisingId=&appName=web&appVersion=9.1.2&deviceDNT=0&deviceId={uuid.uuid4()}&deviceMake=Chrome&deviceModel=web&deviceType=web&deviceVersion=126.0.0&sid={uuid.uuid4()}&serverSideAds=true"
                    
                    elif service == 'samsung':
                        # Redirect stabile per Samsung
                        slug = data.get('slug', '{id}').format(id=c_id)
                        stream_url = f"https://jmp2.uk/{slug}"
                    
                    else: # rakuten
                        # Link diretto per Rakuten (più stabile per i flussi m3u8)
                        stream_url = f"https://i.mjh.nz/RakutenTV/{region}/{c_id}.m3u8"
                    
                    # Costruzione tag EXTINF
                    group = f"{service.upper()} {region.upper()}"
                    extinf = f'#EXTINF:-1 tvg-id="{c_id}" tvg-logo="{ch["logo"]}" group-title="{group}",{ch["name"]}'
                    
                    m3u_content.append(extinf)
                    m3u_content.append(stream_url)
                
                # Salvataggio file
                filename = f"{service_{region}.m3u"
                with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
                    f.write("\n".join(m3u_content))
                    
        except Exception as e:
            print(f"Errore su {service}: {e}")

if __name__ == "__main__":
    run()
