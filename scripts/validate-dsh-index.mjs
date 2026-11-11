#!/usr/bin/env node
/** Validate the published DSH custom-index contract without installing plugins. */
import fs from 'node:fs'
import path from 'node:path'

const root = path.resolve(import.meta.dirname, '..')
const catalog = JSON.parse(fs.readFileSync(path.join(root, 'catalog.json'), 'utf8'))
const index = JSON.parse(fs.readFileSync(path.join(root, 'dsh/index.json'), 'utf8'))
const expected = [...(catalog.plugins ?? []), ...(catalog.candidatePlugins ?? [])]
  .filter((entry) => entry.status !== 'local_candidate')
const errors = []
if (index.format !== 1 || !index.title || !Array.isArray(index.plugins)) {
  errors.push('index must use DSH format 1 with a title and plugins array')
}
const seenNames = new Set()
const seenRepos = new Map()
for (const plugin of index.plugins ?? []) {
  if (!plugin.name || seenNames.has(plugin.name)) errors.push(`duplicate or missing package name: ${plugin.name}`)
  seenNames.add(plugin.name)
  const repo = plugin.repository?.url
  if (!repo || seenRepos.has(repo)) errors.push(`duplicate or missing repository: ${repo}`)
  seenRepos.set(repo, plugin)
  if (plugin.icon && !/^https:\/\//.test(plugin.icon) && !/^data:image\//.test(plugin.icon)) {
    errors.push(`icon must use HTTPS or an inline image: ${plugin.name}`)
  }
  if (!Array.isArray(plugin.versions) || plugin.versions.length === 0) {
    errors.push(`missing version: ${plugin.name}`)
    continue
  }
  for (const version of plugin.versions) {
    if (!/^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$/.test(version.version ?? '')) {
      errors.push(`invalid SemVer: ${plugin.name}`)
    }
    const source = version.source
    if (source?.type !== 'git' || source.url !== repo || !/^[0-9a-f]{40}$/.test(source.commit ?? '') || source.path) {
      errors.push(`invalid repository-root Git source: ${plugin.name}`)
    }
    if (!Number.isInteger(version.publishTimestamp) || version.publishTimestamp <= 0) {
      errors.push(`invalid publish time: ${plugin.name}`)
    }
  }
}
for (const entry of expected) {
  const repo = `https://github.com/${entry.repository}`
  const plugin = seenRepos.get(repo)
  if (!plugin) errors.push(`missing catalog entry: ${entry.id}`)
  else if (!plugin.versions.some((version) => version.version === entry.version)) {
    errors.push(`version mismatch: ${entry.id}`)
  }
}
if (seenRepos.size !== expected.length) errors.push(`entry count ${seenRepos.size} != ${expected.length}`)
if (errors.length) {
  for (const error of errors) console.error(error)
  process.exit(1)
}
console.log(`DSH index valid: ${expected.length} plugins`)
