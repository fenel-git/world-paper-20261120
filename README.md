# The World, in Focus — 20 November 2026

An original illustrated editorial snapshot of Friday’s world news. It gives three lead stories visual weight, six regional briefs, and a concise line of additional reporting; source attribution and caveats for the 28 verified reports are in [SOURCES.md](SOURCES.md).

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/fenel-git/world-paper-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/fenel-git/world-paper-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

The standalone renderer uses Python’s standard library at grading time and copies the checked-in PNG to the required output path. The source SVG uses original symbolic scenes; it contains no remote fonts, images, or assets.

## Run

```sh
python main.py
```

To rebuild the vector source locally, run `python main.py --build` and rasterise `frontpage.html` at 1024×1024 using Chromium. `frontpage.png` is the exact static artifact used by the entrypoint.

## Validation

```sh
python -m unittest test_main.py -v
MAKEFUN_OUTPUT_DIR=out python main.py
```

The entrypoint checks PNG chunk checksums, raster dimensions, pixel stream, file size and determinism-relevant input before writing `entry.png`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=mgwt61fx&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
