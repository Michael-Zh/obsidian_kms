#!/bin/bash
#
# run_brief.sh — 每天 16:00 由 launchd 触发，无头运行 investment-brief 技能，
# 把简报写到 Brief/YYYY-MM-DD.md。只读账户、只写 vault，绝不下单。
#
# 依赖：claude CLI（已认证）、trading212 MCP、网络（WebSearch/WebFetch）。
# MCP 由 claude 从默认位置自动发现，不显式传 --mcp-config。

set -euo pipefail

CLAUDE_BIN="/Users/michael_zhang/.local/bin/claude"
VAULT="/Users/michael_zhang/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS"
BRIEF_DIR="$VAULT/04_project/Road_to_2040_Investment_Blueprint/Brief"
LOG_DIR="$BRIEF_DIR/.logs"

mkdir -p "$BRIEF_DIR" "$LOG_DIR"

TODAY="$(date +%Y-%m-%d)"
OUT_FILE="$BRIEF_DIR/$TODAY.md"
LOG_FILE="$LOG_DIR/run_$TODAY.log"

# 只放行「读账户 + 搜行情 + 写文件」所需的最小权限集合。
# 刻意不包含任何下单工具，也不给通用 Bash。
ALLOWED_TOOLS="Read Write WebSearch WebFetch \
mcp__trading212__fetch_account_info \
mcp__trading212__fetch_account_cash \
mcp__trading212__fetch_portfolio_summary \
mcp__trading212__fetch_portfolio_performance \
mcp__trading212__fetch_all_open_positions \
mcp__trading212__search_instrument \
mcp__trading212__search_specific_position_by_ticker \
mcp__trading212__fetch_dividend_summary \
mcp__trading212__fetch_paid_out_dividends"

# 提示词用单引号拼接变量，避免反引号/中文标点引发变量名错乱。
TITLE="投资简报 $TODAY"
PROMPT='使用 investment-brief 技能生成今日投资简报，然后把完整报告原文（含数据源声明与全部 8 段）写入这个文件：'"$OUT_FILE"'。文件第一行加一行标题：'"$TITLE"'。只读账户与行情数据，绝不下单。'

echo "=== run_brief start $(date '+%F %T') ===" >> "$LOG_FILE"

cd "$VAULT"

"$CLAUDE_BIN" -p "$PROMPT" \
  --permission-mode auto \
  --allowed-tools "$ALLOWED_TOOLS" \
  >> "$LOG_FILE" 2>&1

status=$?
echo "=== run_brief end $(date '+%F %T') status=$status ===" >> "$LOG_FILE"

if [ ! -s "$OUT_FILE" ]; then
  echo "WARN: output file empty or missing: $OUT_FILE" >> "$LOG_FILE"
  exit 1
fi

exit 0
