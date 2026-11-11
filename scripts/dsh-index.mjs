#!/usr/bin/env node
/**
 * Generate the DSH custom index from immutable independent-repository tags.
 * The install source is the repository root: the DSH adapter needs the skills
 * and scripts next to it, which a package taken only from dsh/ would omit.
 */
import fs from 'node:fs'
import path from 'node:path'
import os from 'node:os'
import { execFileSync } from 'node:child_process'

const root = path.resolve(import.meta.dirname, '..')
const catalog = JSON.parse(fs.readFileSync(path.join(root, 'catalog.json'), 'utf8'))
const entries = [...(catalog.plugins ?? []), ...(catalog.candidatePlugins ?? [])]
const plugins = []

function git(dir, ...args) {
  return execFileSync('git', ['-C', dir, ...args], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim()
}

for (const entry of entries) {
  if (entry.status === 'local_candidate') continue
  const url = `https://github.com/${entry.repository}`
  const ref = `v${entry.version}`
  let repoDir = path.resolve(root, '..', `${entry.repository.split('/')[0]}-repositories`, entry.localDirectory)
  let temporary
  try {
    try {
      git(repoDir, 'rev-parse', '--verify', `${ref}^{commit}`)
    } catch {
      temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'dsh-market-release-'))
      execFileSync('git', ['clone', '--quiet', '--depth', '1', '--branch', ref, `${url}.git`, temporary], { stdio: 'ignore' })
      repoDir = temporary
    }
    const pkg = JSON.parse(git(repoDir, 'show', `${ref}:package.json`))
    if (pkg.version !== entry.version || pkg.dsh?.bundle?.patch !== './dsh/cordis.patch.yml') {
      throw new Error(`root DSH bundle/version mismatch at ${ref}`)
    }
    git(repoDir, 'cat-file', '-e', `${ref}:dsh/lib/index.js`)
    const commit = git(repoDir, 'rev-parse', `${ref}^{commit}`)
    const timestamp = Number(git(repoDir, 'show', '-s', '--format=%ct', commit))
    const logo = typeof entry.logo === 'string' ? entry.logo.replace(/^\.\//, '') : undefined
    const author = entry.author?.name ?? entry.author
    plugins.push({
      name: pkg.name,
      title: entry.displayName ?? entry.id,
      description: entry.description ?? '',
      ...(logo ? { icon: `https://cdn.jsdelivr.net/gh/${entry.repository}@${ref}/${logo}` } : {}),
      ...(typeof author === 'string' ? { author } : {}),
      homepage: url,
      repository: { url },
      versions: [{
        version: pkg.version,
        publishTimestamp: timestamp,
        source: { type: 'git', url, commit },
      }],
    })
  } catch (error) {
    console.warn(`skip ${entry.id}: ${error.message}`)
  } finally {
    if (temporary) fs.rmSync(temporary, { recursive: true, force: true })
  }
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
