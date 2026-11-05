# Research: travel router with VPN for hotels, 2026-11-05 (Fable agent)

Reddit was read through snapshots (reddit.sentinel-team.org), plus the GL.iNet forum and Amazon.

## Pain points
1. The hotel captive portal won't load (7 threads, every brand: GL.iNet, UniFi, TP-Link). Examples: r/digitalnomad
   Beryl AX failed in 2 hotels; GL.iNet forum, Slate 7 at Shangri-La Fiji; r/Ubiquiti UTR portals "never loaded".
2. VPN speed (5): usually the hotel uplink, the VPN server's upload or the MTU, not the box (MTU 1380 fixed a Slate AX).
3. A work laptop breaks with the router's VPN on: corporate VPN or Zscaler double-tunnel (3).
4. Reaching home over Tailscale/WireGuard (4).
5. Cruise ships ban routers: Carnival (Sep 2024), Royal Caribbean (Dec 2024), MSC (4).

## Honest winner (GL.iNet is ours, Awin 80509)
- **Beryl AX (GL-MT3000), $98.99**: WireGuard 300 Mbps / OpenVPN 150 Mbps (GL.iNet lab), 4.5★ on 5,493 Amazon
  reviews. GL.iNet firmware 4.6+ has "Auto-Enable Login Mode for Public Hotspots" and one-click MAC clone; the
  documented fallback is asking the desk to whitelist the MAC (GL.iNet captive-portal FAQ). Hotel Wi-Fi rarely
  exceeds 100–200 Mbps, so 300 Mbps isn't the bottleneck.
- **Beryl 7 (GL-MT3600BE), $129.99**: 1,100 Mbps WireGuard, the pick for home-tunnel users; newer (4.2★ on 654).
- Slate 7 (GL-BE3600), $159.99: 490 Mbps WireGuard, touchscreen; not the pick. Slate AX (GL-AXT1800), $119.99: EAP
  enterprise Wi-Fi, 3 Ethernet ports. Opal (GL-SFT1200), $39.99: 65 Mbps WireGuard, no Tailscale; budget only.

## Facts (gl-inet.com US, 2026-11-05)
All have a 2-year warranty, 30-day money back and free US shipping. No code is printed (the "GET 10% OFF" banner has
none).

| Model | URL | Price | WG / OpenVPN | Wi-Fi | Ports | Power | Size / weight | Amazon ASIN |
|---|---|---|---|---|---|---|---|---|
| Beryl AX GL-MT3000 | https://www.gl-inet.com/en-us/products/gl-mt3000 | $98.99 | 300 / 150 | AX3000 | 2.5G WAN, 1G LAN, USB 3.0 | USB-C 5V/3A | 120×83×34 mm, 196 g | B0BPSGJN7T |
| Beryl 7 GL-MT3600BE | https://www.gl-inet.com/en-us/products/gl-mt3600be | $129.99 | 1,100 / 1,000 | BE3600 | 2× 2.5G, USB 3.0 | USB-C PD | 205 g | B0GF1J99S4 |
| Slate 7 GL-BE3600 | https://www.gl-inet.com/en-us/products/gl-be3600 | $159.99 | 490 / 385 | BE3600 | 2× 2.5G, touchscreen | USB-C PD | 295 g | B0F2MR53D6 |
| Slate AX GL-AXT1800 | https://www.gl-inet.com/en-us/products/gl-axt1800 | $119.99 | 550 / 560 | AX1800 | 1 WAN + 2 LAN, microSD | USB-C 5V/4A | 245 g | B0B2J7WSDK |
| Opal GL-SFT1200 | https://www.gl-inet.com/en-us/products/gl-sft1200 | $39.99 | 65 / 12 | AC1200 | 1 WAN + 2 LAN | USB-C | 145 g | – |

## Field (Amazon, 2026-11-05)
- TP-Link Roam 6 TL-WR1502X: $39.99, 3.9★ (1.4K); no VPN throughput published.
- TP-Link Roam 7 TL-WR3602BE: $87.99, 4.3★ (429); no published VPN number, no Tailscale.
- ASUS RT-AX57 Go: $99.00, 4.0★ (175); WireGuard 300 Mbps (ASUS), the same as Beryl AX.
- ASUS RT-BE58 Go: $136.86.

## Unverified
Independent WireGuard measurements (use GL.iNet's figures); captive-portal success rates are anecdotal.
