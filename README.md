# 📺 LordTruffle FAST - Global Playlists

Benvenuto nel mio repository di automazione FAST. Qui trovi le playlist per **Samsung TV Plus**, **Pluto TV** e **Rakuten TV** aggiornate automaticamente ogni 12 ore.

## 🚀 Come usare su TiviMate / Sparkle

1. Vai su **Impostazioni** -> **Playlist** nel tuo player.
2. Copia il link **M3U (Raw)** della regione che ti interessa dalla tabella qui sotto.
3. Inserisci il link **EPG** corrispondente per avere la guida TV.

### 🇮🇹 Italia
| Servizio | Playlist M3U (Link Raw) | Guida TV (EPG) |
| :--- | :--- | :--- |
| **Samsung** | `https://raw.githubusercontent.com/LordTruffle/FAST/main/playlists/samsung_it.m3u` | `https://i.mjh.nz/SamsungTVPlus/it.xml.gz` |
| **Pluto TV** | `https://raw.githubusercontent.com/LordTruffle/FAST/main/playlists/pluto_it.m3u` | `https://i.mjh.nz/PlutoTV/it.xml.gz` |
| **Rakuten** | `https://raw.githubusercontent.com/LordTruffle/FAST/main/playlists/rakuten_it.m3u` | `https://i.mjh.nz/RakutenTV/it.xml.gz` |

### 🇺🇸 United States
| Servizio | Playlist M3U (Link Raw) | Guida TV (EPG) |
| :--- | :--- | :--- |
| **Samsung** | `https://raw.githubusercontent.com/LordTruffle/FAST/main/playlists/samsung_us.m3u` | `https://i.mjh.nz/SamsungTVPlus/us.xml.gz` |
| **Pluto TV** | `https://raw.githubusercontent.com/LordTruffle/FAST/main/playlists/pluto_us.m3u` | `https://i.mjh.nz/PlutoTV/us.xml.gz` |

---

## ⚙️ Dettagli Tecnici
- **Aggiornamento:** Automatico ogni 12 ore via GitHub Actions.
- **Sorgenti:** Database MJH (Samsung, Pluto, Rakuten).
- **Formato:** M3U Plus con tag `tvg-id`, `tvg-logo` e `group-title`.

## ⚠️ Note
I canali che richiedono **DRM** sono inclusi. Per una visione ottimale, assicurati che il tuo dispositivo e il tuo player supportino i flussi Widevine/DASH.
