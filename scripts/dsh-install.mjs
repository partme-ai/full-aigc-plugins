#!/usr/bin/env node
/**
 * Install plugins from this catalog's DSH index, individually or all at once.
 *
 *   node scripts/dsh-install.mjs --list
 *   node scripts/dsh-install.mjs --profile desktop --only codegraph,gitflow
 *   node scripts/dsh-install.mjs --profile desktop --all
 *   node scripts/dsh-install.mjs --profile desktop --all --dry-run
 *
 * Each plugin is installed as its own package (git + path:/dsh), so it can be
 * removed or updated independently afterwards. `DSH_CLI` overrides the dsh
 * executable; `DSH_HOME` is inherited by the child process.
 */
import fs from 'node:fs'
import path from 'node:path'
import { execFileSync } from 'node:child_process'

const root = path.resolve(import.meta.dirname, '..')
const index = JSON.parse(fs.readFileSync(path.join(root, 'dsh/index.json'), 'utf8'))
const argv = process.argv.slice(2)
const has = (name) => argv.includes(name)
const value = (name, fallback) => {
  const i = argv.indexOf(name)
  if (i < 0) return fallback
  const next = argv[i + 1]
  return next && !next.startsWith('--') ? next : true
}

const profile = String(value('--profile', 'desktop'))
const dryRun = has('--dry-run')
const all = has('--all')
const migrate = has('--migrate')
const onlyArg = value('--only', undefined)
const only = new Set(
  onlyArg && onlyArg !== true
    ? String(onlyArg).split(',').map((s) => s.trim()).filter(Boolean)
    : [],
)

if (has('--list')) {
  for (const plugin of index.plugins) {
    const v = plugin.versions[0]
    console.log(`${plugin.name.replace('@partme-dsh/', '').padEnd(22)} ${v.version}  ${plugin.title?.en ?? plugin.title}`)
  }
  process.exit(0)
}

if (!all && only.size === 0) {
  console.error('Pass --all or --only <slug[,slug]>; --list shows the catalog.')
  process.exit(2)
}

const dsh = process.env.DSH_CLI || (process.platform === 'win32' ? 'dsh.cmd' : 'dsh')
const win = process.platform === 'win32'
const runDsh = (args) => {
  if (win) {
    const command = `"${dsh}" ${args.map((arg) => `"${arg}"`).join(' ')}`
    execFileSync(process.env.ComSpec || 'cmd.exe', ['/d', '/s', '/c', command], { stdio: 'inherit' })
  } else {
    execFileSync(dsh, args, { stdio: 'inherit' })
  }
}
const specs = []
for (const plugin of index.plugins) {
  const slug = plugin.name.split('/').pop()
  if (!all && !only.has(slug)) continue
  const version = plugin.versions[0]
  if (version.source.type === 'npm') {
    specs.push({ slug, spec: `${plugin.name}@${version.version}` })
  } else {
    const url = version.source.url.endsWith('.git') ? version.source.url : `${version.source.url}.git`
    const pathPart = version.source.path ? `&path:/${version.source.path}` : ''
    specs.push({ slug, spec: `git+${url}#${version.source.commit}${pathPart}` })
  }
}

if (migrate) {
  for (const { slug } of specs) {
    const legacy = slug === 'codereview' ? '@partme-dsh/codereview-plugin' : `@partme-dsh/${slug}`
    try {
      console.log(`\n→ removing legacy ${legacy}`)
      runDsh(['plugin', '--profile', profile, 'remove', legacy])
    } catch {
      // Not installed under the legacy scoped name.
    }
  }
}

console.log(`profile: ${profile}`)
console.log(`plugins: ${specs.length}${all ? ' (all)' : ` (${[...only].join(', ')})`}`)
for (const { slug, spec } of specs) {
  console.log(`\n→ ${slug}\n  ${spec}`)
  if (dryRun) continue
  runDsh(['plugin', '--profile', profile, 'add', spec])
}
console.log(dryRun ? '\ndry run: nothing installed' : '\ndone')
