# THE WORLD — Sunday 22 November 2026

[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/c/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/airdropgodx24/news-image-20261122/rank.svg)](https://make.fun/c/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/airdropgodx24/news-image-20261122/reward.svg)](https://make.fun/c/news-image-20261122)

A newspaper front page that sums up the world news of Sunday 22 November 2026 in a single image. The masthead names the day, "SUNDAY 22 NOVEMBER 2026", and the page leads with the COP31 climate talks closing in on a final deal and the ballistic missile strike on Zelenskyy's hometown in Ukraine, followed by stories from every continent: Nigeria, Brazil, Peru, the US and Canada, France, Belgium, Nvidia, the Rohingya verdict, the Houthi strikes on Riyadh, Iran, the G20 opening in Johannesburg, Taiwan, North Korea, India, South Korea, Meta in India, Wildberries, and the US Senate.

## How it works

`main.py` draws every pixel itself with only the Python standard library: its own 5x7 bitmap letterforms, its own drawing helpers (rectangles, lines, circles, ellipses), and its own PNG encoder built on `zlib` and `struct`. No image files are shipped, nothing is downloaded, and the program never touches the network. The output is deterministic: two runs write byte-identical files.

## How to run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png` (1024x1024, well under 1 MiB). Without `MAKEFUN_OUTPUT_DIR` set, it writes to `/output/entry.png`.
