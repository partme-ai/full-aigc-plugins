#!/bin/sh
# 返回125表示非已有任务入口；可信任务以exec接替，失败绝不回落安装当前Python。
task_entry() {
set -eu
LC_ALL=C; export LC_ALL
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
entry_fail() { printf '%s\n' "bound_entry_invalid: $1" >&2; exit 1; }
entry_hash() { if command -v sha256sum >/dev/null 2>&1; then sha256sum | awk '{print $1}'; else shasum -a 256 | awk '{print $1}'; fi; }
# 仅解析已有公开契约中的全局选项和task；所有原始参数随后仍交由管理层严格解析。
state=${CRAFT_STATE_HOME:-$HOME/.local/share/craft-tasks/effectcraft}; action=''; task=''; expect=''
for item in "$@"; do
  if [ -n "$expect" ]; then
    case "$expect" in state) state=$item;; task) [ -z "$task" ] || entry_fail duplicate_task; task=$item;; runtime) :;; esac
    expect=''; continue
  fi
  if [ -z "$action" ]; then
    case "$item" in
      --state-root) expect=state;; --state-root=*) state=${item#*=};;
      --runtime-home) expect=runtime;; --runtime-home=*) :;;
      resume|reconcile|review|revise|inspect|cancel) action=$item;; *) return 125;;
    esac
  else
    case "$item" in --task) expect=task;; --task=*) [ -z "$task" ] || entry_fail duplicate_task; task=${item#*=};; esac
  fi
done
[ -n "$action" ] || return 125
[ -z "$expect" ] && [ -n "$task" ] || entry_fail missing_task
case "$task" in *[!a-zA-Z0-9_-]*|[-_]*|'') entry_fail task_id;; esac
[ "${#task}" -le 96 ] || entry_fail task_id
case "$state" in '~/'*) state="$HOME/${state#\~/}";; esac
case "$state" in /*) ;; *) state="$PWD/$state";; esac
# 不经过符号链接选择任务或执行资源。
for path in "$state" "$state/tasks" "$state/tasks/$task" "$state/tasks/$task/state.json" "$state/tasks/$task/execution" "$state/tasks/$task/execution/identity.json" "$state/tasks/$task/execution/entry.tsv"; do
  [ ! -L "$path" ] || entry_fail symlink
 done
execution="$state/tasks/$task/execution"; identity="$execution/identity.json"; descriptor="$execution/entry.tsv"
[ -f "$identity" ] && [ -f "$descriptor" ] && [ -f "$state/tasks/$task/state.json" ] || entry_fail missing_launch_material
[ "$(wc -c < "$identity" | tr -d ' ')" -le 16777216 ] && [ "$(wc -c < "$descriptor" | tr -d ' ')" -le 16384 ] || entry_fail oversized
[ "$(wc -c < "$state/tasks/$task/state.json" | tr -d ' ')" -le 16777216 ] || entry_fail oversized
identity_sha=$(tr -d '\n' < "$identity" | entry_hash)
awk -v sha="$identity_sha" -f "$HERE/entry_identity.awk" "$identity" "$state/tasks/$task/state.json" || entry_fail identity_mismatch
entry_sha=$(entry_hash < "$descriptor")
# 该字段在v2绑定身份中；禁止从任务计划或任意环境变量选择执行路径。
awk -v token="\"entrySha256\":\"$entry_sha\"" '{ n=split($0,a,token); if(n!=2) exit 1 }' "$identity" || entry_fail descriptor_mismatch
# 固定顺序、固定字段数；不使用source/eval，不支持描述中的命令表达式。
tab=$(printf '\t')
read_field() {
  row=$1; expected_key=$2
  value=$(sed -n "${row}p" "$descriptor")
  field=${value%%"$tab"*}; [ "$field" = "$expected_key" ] && [ "$field" != "$value" ] || entry_fail descriptor_shape
  value=${value#*"$tab"}; case "$value" in *"$tab"*) entry_fail descriptor_shape;; esac
  printf '%s' "$value"
}
[ "$(wc -l < "$descriptor" | tr -d ' ')" = 11 ] || entry_fail descriptor_shape
descriptor_schema=$(read_field 1 schema) || entry_fail descriptor_shape
[ "$descriptor_schema" = effectcraft-task-entry/v1 ] || entry_fail descriptor_version
mode=$(read_field 2 mode) || entry_fail descriptor_shape; python=$(read_field 3 executable) || entry_fail descriptor_shape; python_sha=$(read_field 4 executableSha256) || entry_fail descriptor_shape
root=$(read_field 5 root) || entry_fail descriptor_shape; key=$(read_field 6 platform) || entry_fail descriptor_shape; version=$(read_field 7 version) || entry_fail descriptor_shape
manifest=$(read_field 8 manifest) || entry_fail descriptor_shape; manifest_sha=$(read_field 9 manifestSha256) || entry_fail descriptor_shape; archive_sha=$(read_field 10 archiveSha256) || entry_fail descriptor_shape; minimum=$(read_field 11 minimumSystem) || entry_fail descriptor_shape
case "$(uname -s):$(uname -m)" in Darwin:arm64|Darwin:aarch64) actual=darwin-arm64;; Darwin:x86_64) actual=darwin-x86_64;; Linux:x86_64) actual=linux-x86_64;; Linux:aarch64|Linux:arm64) actual=linux-aarch64;; *) entry_fail platform;; esac
[ "$actual" = "$key" ] || entry_fail platform
case "$python" in /*) ;; *) entry_fail python_path;; esac
[ -f "$python" ] && [ ! -L "$python" ] && [ "$(entry_hash < "$python")" = "$python_sha" ] || entry_fail python_changed
case "$mode" in
 external) [ "$root" = - ] && [ "$manifest" = - ] || entry_fail descriptor_shape;;
 locked)
  case "$root" in /*) ;; *) entry_fail root;; esac
  [ -d "$root" ] && [ ! -L "$root" ] || entry_fail root
  case "$python" in "$root/"*) ;; *) entry_fail python_path;; esac
  case "$manifest" in python-integrity/*.tsv) ;; *) entry_fail manifest_path;; esac
  case "$manifest" in *..*|*\\*) entry_fail manifest_path;; esac
  manifest="$execution/skill/scripts/$manifest"
  [ -f "$manifest" ] && [ ! -L "$manifest" ] && [ "$(entry_hash < "$manifest")" = "$manifest_sha" ] || entry_fail manifest_changed
  case "$key" in darwin-*) system=$(sw_vers -productVersion);; linux-*) system=$(getconf GNU_LIBC_VERSION 2>/dev/null | awk '$1=="glibc"{print $2}');; esac
  [ -n "$system" ] || entry_fail minimum_system
  awk -v actual="$system" -v minimum="$minimum" 'BEGIN{split(actual,a,".");split(minimum,b,".");for(i=1;i<=3;i++){if(a[i]+0>b[i]+0)exit 0;if(a[i]+0<b[i]+0)exit 1}}' || entry_fail minimum_system
  verify_receipt "$root"
  expected_count=$(wc -l < "$manifest" | tr -d ' ')
  actual_count=$(find "$root" \( -type f -o -type l \) ! -path "$root/installation.json" -print | wc -l | tr -d ' ')
  [ "$actual_count" = "$expected_count" ] || entry_fail python_inventory
  while IFS="$tab" read -r kind expected relative; do
    case "$relative" in /*|*..*|*\\*) entry_fail python_manifest;; esac
    file="$root/$relative"
    case "$kind" in
      l) [ -L "$file" ] || entry_fail python_link; target=$(readlink "$file"); sha=$(printf '%s' "$target" | entry_hash);;
      f) [ -f "$file" ] && [ ! -L "$file" ] || entry_fail python_file; sha=$(entry_hash < "$file");;
      *) entry_fail python_manifest;;
    esac
    [ "$sha" = "$expected" ] || entry_fail python_changed
  done < "$manifest"
  ;;
 *) entry_fail mode;;
esac
exec "$python" -I -B "$HERE/task_entry.py" "$@"

}
