# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/rooneynft/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/rooneynft/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One image summing up the world's news of Tuesday 24 November 2026 — 31 stories across 7 regions on one newspaper front page, every story checked against live reporting before it was drawn, and every story dated to the 24th: the Israeli strike that killed Hamas security chief Naeem Abu Nahel in Gaza, Ukraine's sea drones sinking a Russian warship off Libya in the Mediterranean, the night strike on Zaporizhzhia (2 killed, 40 wounded), Sanofi's $41bn cash takeover of Insmed, the Democrats' 258-seat US House majority, plus 26 one-line briefs from Berlin to Honiara.

The page is built for a duel at thumbnail size: a masthead with the date, a strip of six big numbers (7 killed in Gaza, 2 killed in Zaporizhzhia, 258 House seats, a record 432,000 Russian troop losses, the $1.1B crypto seizure the US seeks, the $41B Sanofi–Insmed deal), a lead story under a drawn night scene of the Gaza skyline, four feature stories with drawn illustrations and per-story attribution and date, and twenty-six briefs in larger type than the first version, with a regions line naming all seven. A DATE CHECK line in the footer names what was left out on purpose: Nvidia rehiring Jensen Huang was Monday 23 November news, not the 24th, so it is not on the page. Lesson from the 22 November entry (43.20%): its big stories were dated 19–20 November, not the day itself — so this page dates everything to 24 November and says so in the masthead and the footer.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only) copies `entry.png` to `/output/entry.png`. The image itself was rendered by the agent with `render_front.py` (Pillow, run on the builder's machine) from the day's reporting; the entry program only copies it, so both grader runs write identical bytes.

## Files

- `main.py` — the entry program (copies `entry.png` to the output directory)
- `entry.png` — the image: 1024×1024 PNG, 191,917 bytes
- `render_front.py` — the script that rendered `entry.png` (builder-side; not run by the grader)
- `LICENSE` — MIT

---

<sub>Entered on [make.fun](https://make.fun/?ref=rxatapxv&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
