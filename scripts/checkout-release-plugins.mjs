// Read-only checkout of selected published versions for isolated CI validation.
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const catalog = JSON.parse(fs.readFileSync(path.join(root, 'catalog.json'), 'utf8'));
const selected = new Set(process.argv.filter(arg => arg.startsWith('--plugin=')).map(arg => arg.slice(9)));
if (process.argv.includes('--all')) for (const plugin of catalog.plugins) selected.add(plugin.id);
if (!selected.size) throw new Error('Select explicit --plugin ids to avoid unrelated checkouts.');
for (const id of selected) {
  const plugin = catalog.plugins.find(entry => entry.id === id);
  if (!plugin || !/^[a-z0-9-]+$/.test(plugin.localDirectory) || !/^[\w-]+\/[\w-]+$/.test(plugin.repository)) throw new Error(`Invalid plugin: ${id}`);
  const destination = path.resolve(root, '../full-aigc-plugins-repositories', plugin.localDirectory);
  if (fs.existsSync(destination)) throw new Error(`Existing checkout preserved: ${destination}`);
  execFileSync('git', ['-c', 'core.autocrlf=false', 'clone', '--depth', '1', '--branch', `v${plugin.version}`, `https://github.com/${plugin.repository}.git`, destination], { stdio: 'inherit' });
}
