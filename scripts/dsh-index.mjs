#!/usr/bin/env node
/**
 * Generate `dsh/index.json` — a DeepSeek Harness format-1 plugin market index —
 * from this catalog's plugins and their sibling repositories' `dsh/` packages.
 *
 *   node scripts/dsh-index.mjs
 *
 * Each entry installs from the plugin repository at the current commit, with
 * `path: dsh`; no package is copied into this catalog.
 */
import fs from 'node:fs'
import path from 'node:path'
import { execFileSync } from 'node:child_process'

const root = path.resolve(import.meta.dirname, '..')
const catalog = JSON.parse(fs.readFileSync(path.join(root, 'catalog.json'), 'utf8'))
const repos = path.resolve(root, '..', `${catalog.name}-repositories`)
const entries = [...(catalog.plugins ?? []), ...(catalog.candidatePlugins ?? [])]
const plugins = []
for (const entry of entries) {
  const repoDir = path.join(repos, entry.localDirectory)
  const pkgFile = path.join(repoDir, 'dsh/package.json')
  if (!fs.existsSync(pkgFile)) {
    console.warn(`skip ${entry.id}: no dsh/package.json`)
    continue
  }
  const pkg = JSON.parse(fs.readFileSync(pkgFile, 'utf8'))
  const commit = execFileSync('git', ['-C', repoDir, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim()
  const timestamp = Number(execFileSync('git', ['-C', repoDir, 'show', '-s', '--format=%ct', 'HEAD'], { encoding: 'utf8' }).trim())
  const logo = typeof entry.logo === 'string' ? entry.logo.replace(/^\.\//, '') : undefined
  plugins.push({
    name: pkg.name,
    title: entry.displayName ?? entry.id,
    description: entry.description ?? '',
    ...(logo ? { icon: `https://cdn.jsdelivr.net/gh/${entry.repository}@v${pkg.version}/${logo}` } : {}),
    repository: { url: `https://github.com/${entry.repository}` },
    versions: [{
      version: pkg.version,
      publishTimestamp: timestamp,
      source: { type: 'git', url: `https://github.com/${entry.repository}`, commit, path: 'dsh' },
    }],
  })
}
const index = {
  format: 1,
  title: catalog.displayName ?? catalog.name,
  ...(catalog.description ? { description: catalog.description } : {}),
  metadata: {},
  plugins,
}
const out = path.join(root, 'dsh/index.json')
fs.mkdirSync(path.dirname(out), { recursive: true })
fs.writeFileSync(out, JSON.stringify(index, null, 2) + '\n')
console.log(`${catalog.name}: ${plugins.length} plugins -> ${out}`)
