#!/usr/bin/env python3
"""Pattern 4: Fine-grained progress bar with true color gradient"""

import json, sys
from datetime import datetime, timezone

data = json.load(sys.stdin)

BLOCKS = " ▏▎▍▌▋▊▉█"
R = "\033[0m"
DIM = "\033[2m"


def gradient(pct):
    return "\033[38;2;80;200;80m"


def bar(pct, width=10):
    pct = min(max(pct, 0), 100)
    filled = pct * width / 100
    full = int(filled)
    frac = int((filled - full) * 8)
    b = "█" * full
    if full < width:
        b += BLOCKS[frac]
        b += "░" * (width - full - 1)
    return b


def fmt_reset(five_data):
    remaining_sec = None

    # resets_at: Unix タイムスタンプ（秒）
    if "resets_at" in five_data:
        try:
            reset_ts = int(five_data["resets_at"])
            now_ts = int(datetime.now(timezone.utc).timestamp())
            remaining_sec = max(0, reset_ts - now_ts)
        except (ValueError, TypeError):
            pass

    if remaining_sec is None:
        return None

    h, rem = divmod(remaining_sec, 3600)
    m = rem // 60
    if h > 0:
        return f"{h}h{m:02d}m"
    else:
        return f"{m}m"


def fmt(label, pct, reset_str=None):
    p = round(pct)
    reset_part = f" {DIM}({reset_str}){R}" if reset_str else ""
    return f"{label} {gradient(pct)}{bar(pct)} {p}%{R}{reset_part}"


model = data.get("model", {}).get("display_name", "Claude")
effort = data.get("effort", {}).get("level", "None")
model += f" ({effort})"
parts = [model]

cost = data.get("cost", {}).get("total_cost_usd", 0) or 0
parts.append(f"${cost:.2f}")

ctx = data.get("context_window", {}).get("used_percentage")
if ctx is not None:
    parts.append(fmt("ctx", ctx))

five_data = data.get("rate_limits", {}).get("five_hour", {})
five = five_data.get("used_percentage")
if five is not None:
    reset_str = fmt_reset(five_data)
    parts.append(fmt("5h", five, reset_str))

week = data.get("rate_limits", {}).get("seven_day", {}).get("used_percentage")
if week is not None:
    parts.append(fmt("7d", week))

print(f"{DIM}│{R}".join(f" {p} " for p in parts), end="")
