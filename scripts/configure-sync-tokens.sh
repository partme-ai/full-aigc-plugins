#!/usr/bin/env bash
# 统一使用一把 SKILLS_SYNC_TOKEN：写入全部技能仓与插件仓，并清理两个已废弃的令牌名。
#
# 用法：
#   SKILLS_SYNC_TOKEN='xxx' bash scripts/configure-sync-tokens.sh
#   SKILLS_SYNC_TOKEN='xxx' bash scripts/configure-sync-tokens.sh --dry-run
#   SKILLS_SYNC_TOKEN='xxx' bash scripts/configure-sync-tokens.sh --orgs full-aigc-skills,full-aigc-plugins
#   SKILLS_SYNC_TOKEN='xxx' bash scripts/configure-sync-tokens.sh --repos full-aigc-skills/jianying-skills,full-aigc-plugins/jianying-draft-plugin
#   bash scripts/configure-sync-tokens.sh --verify        # 只读巡检，不需要令牌
#
# 设计要点（都是踩过坑换来的）：
#   1. 预检：令牌必须真的能 dispatch，预检不过就一个仓都不写。
#      2026-09-21 一次无差别覆盖把当时唯一可用的令牌冲掉，分发现场由 success 变 failure。
#   2. 清理 FULL_STACK_SKILLS_SYNC_TOKEN / FULL_AIGC_SKILLS_SYNC_TOKEN：
#      这两个名字是历史遗留，留着会在 `A || B` 表达式里抢在 SKILLS_SYNC_TOKEN 前面被命中。
#   3. 仓库清单不再手写：仓库改名（jianying-cli → jianying-draft、
#      jianying-edit-plugin → jianying-draft-plugin）和 craft 系列扩张让手写清单必然过期。
#      默认自动发现；改名后的 301 由 gh 跟随，写入的是当前 full_name。
#   4. 令牌能力要求：Fine-grained PAT 必须勾选目标仓库并授予 Contents: Read and write
#      （repository_dispatch 需要写权限）；classic PAT 需要 repo scope。
set -uo pipefail

ORGS_DEFAULT="full-aigc-skills,full-aigc-plugins,full-stack-skills,full-stack-plugins"
LEGACY_SECRETS=(FULL_STACK_SKILLS_SYNC_TOKEN FULL_AIGC_SKILLS_SYNC_TOKEN)
# 预检目标：一个技能仓 + 一个插件仓，覆盖令牌两个方向的使用场景。
PROBE_REPOS=(
  full-aigc-plugins/video-factory-plugin
  full-aigc-plugins/jianying-draft-plugin
  full-aigc-skills/jianying-skills
  full-stack-plugins/codeguard-plugin
)

mode=set
orgs_csv="$ORGS_DEFAULT"
explicit_repos=()

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) mode=dry ;;
    --verify) mode=verify ;;
    --probe) mode=probe ;;
    --orgs) orgs_csv="${2:-}"; shift ;;
    --repos)
      IFS=',' read -r -a extra <<<"${2:-}"
      explicit_repos+=("${extra[@]}")
      shift
      ;;
    -h | --help)
      sed -n '2,22p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "未知参数: $1" >&2
      exit 2
      ;;
  esac
  shift
done

command -v gh >/dev/null 2>&1 || { echo "缺少 gh CLI" >&2; exit 2; }

# 打印待处理仓库的当前 full_name（去重、去空）。
discover() {
  local org name
  for org in ${orgs_csv//,/ }; do
    while IFS= read -r name; do
      [ -n "$name" ] && printf '%s/%s\n' "$org" "$name"
    done < <(gh repo list "$org" --limit 300 --json name,isArchived \
      --jq '.[] | select(.isArchived | not) | .name' 2>/dev/null)
  done
}

resolve_full_name() {
  gh api "repos/$1" --jq '.full_name' 2>/dev/null | tr -d '\r'
}

# ── 只读巡检 ────────────────────────────────────────────────────────────────
if [ "$mode" = "verify" ]; then
  total=0 missing=0 legacy=0 noperm=0
  printf '%-56s %-18s %-8s %s\n' "REPOSITORY" "SKILLS_SYNC_TOKEN" "LEGACY" "NOTE"
  printf '%-56s %-18s %-8s %s\n' "----------" "-----------------" "------" "----"
  while IFS= read -r repo; do
    [ -n "$repo" ] || continue
    total=$((total + 1))
    current="$(resolve_full_name "$repo")"
    current="${current:-$repo}"
    names="$(gh api "repos/${current}/actions/secrets" --jq '.secrets[].name' 2>/dev/null)"
    if [ -z "$names" ]; then
      printf '%-56s %-18s %-8s %s\n' "$current" "-" "-" "no admin"
      noperm=$((noperm + 1))
      continue
    fi
    state=MISSING
    if printf '%s\n' "$names" | grep -qx SKILLS_SYNC_TOKEN; then state=present; else missing=$((missing + 1)); fi
    legacy_state=clean
    for legacy_name in "${LEGACY_SECRETS[@]}"; do
      if printf '%s\n' "$names" | grep -qx "$legacy_name"; then
        legacy_state=stale
        legacy=$((legacy + 1))
      fi
    done
    printf '%-56s %-18s %-8s %s\n' "$current" "$state" "$legacy_state" ""
  done < <(if [ ${#explicit_repos[@]} -gt 0 ]; then printf '%s\n' "${explicit_repos[@]}"; else discover; fi)
  echo
  echo "共 $total 个仓库：缺 SKILLS_SYNC_TOKEN $missing，残留废弃令牌 $legacy，无 admin 权限 $noperm"
  exit 0
fi

SKILLS_SYNC_TOKEN="${SKILLS_SYNC_TOKEN:?请先设置 SKILLS_SYNC_TOKEN}"

# ── 预检：令牌必须真的能 dispatch，否则一个仓都不写 ──────────────────────────
if [ "$mode" = "set" ]; then
  for probe in "${PROBE_REPOS[@]}"; do
    if GH_TOKEN="$SKILLS_SYNC_TOKEN" gh api --method POST "repos/$probe/dispatches" \
      -f event_type=token-preflight >/dev/null 2>&1; then
      echo "预检通过：$probe"
    else
      echo "❌ 预检失败：令牌无法 dispatch 到 ${probe}（缺 Contents 写权限）。" >&2
      echo "   未写入任何仓。请修好令牌后重跑。" >&2
      exit 3
    fi
  done
  echo
fi

# ── 可见性探测：用令牌逐仓发 GET，看谁在 PAT 的可见范围内 ─────────────
if [ "$mode" = "probe" ]; then
  probe_token="${SKILLS_SYNC_TOKEN:?--probe 需要 SKILLS_SYNC_TOKEN}"
  visible=0 invisible=0 unreadable=()
  while IFS= read -r repo; do
    [ -n "$repo" ] || continue
    if GH_TOKEN="$probe_token" gh api "repos/$repo" >/dev/null 2>&1; then
      visible=$((visible + 1))
    else
      invisible=$((invisible + 1))
      unreadable+=("$repo")
    fi
  done < <(if [ ${#explicit_repos[@]} -gt 0 ]; then printf '%s\n' "${explicit_repos[@]}"; else discover; fi)
  echo
  echo "可见 $visible，不可见 $invisible"
  if [ "$invisible" -gt 0 ]; then
    echo "以下仓在令牌可见范围外（dispatch 会拿到 404）："
    printf '  - %s\n' "${unreadable[@]}"
    exit 1
  fi
  exit 0
fi

# ── 写入 ────────────────────────────────────────────────────────────────────
ok=0 failed=0 skipped=0
failures=()

while IFS= read -r repo; do
  [ -n "$repo" ] || continue
  current="$(resolve_full_name "$repo")"
  if [ -z "$current" ]; then
    echo "→ $repo  (仓库不存在，跳过)"
    skipped=$((skipped + 1))
    continue
  fi
  echo "→ $current"

  if [ "$mode" = "dry" ]; then
    echo "   would set SKILLS_SYNC_TOKEN (len ${#SKILLS_SYNC_TOKEN})"
    for legacy_name in "${LEGACY_SECRETS[@]}"; do
      echo "   would delete $legacy_name (if present)"
    done
    skipped=$((skipped + 1))
    continue
  fi

  if gh secret set SKILLS_SYNC_TOKEN --repo "$current" --body "$SKILLS_SYNC_TOKEN" >/dev/null 2>&1; then
    ok=$((ok + 1))
    echo "   SKILLS_SYNC_TOKEN set"
  else
    failed=$((failed + 1))
    failures+=("$current: SKILLS_SYNC_TOKEN set failed (need admin?)")
    echo "   ❌ SKILLS_SYNC_TOKEN set failed"
  fi

  for legacy_name in "${LEGACY_SECRETS[@]}"; do
    # 不存在时 gh 返回非零，忽略即可；可反复执行。
    gh secret delete "$legacy_name" --repo "$current" >/dev/null 2>&1 \
      && echo "   deleted legacy $legacy_name"
  done
done < <(if [ ${#explicit_repos[@]} -gt 0 ]; then printf '%s\n' "${explicit_repos[@]}"; else discover; fi)

echo
if [ "$mode" = "dry" ]; then
  echo "dry-run 完成：$skipped 个仓库，未写入任何 secret"
  exit 0
fi

echo "成功 $ok，失败 $failed，跳过 $skipped"
if [ $failed -gt 0 ]; then
  echo "失败项：" >&2
  printf '  - %s\n' "${failures[@]}" >&2
  exit 1
fi
