import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = relative => JSON.parse(fs.readFileSync(path.join(root, relative), 'utf8'));
const retained = ['effectcraft', 'figcraft', 'filmcraft', 'lightcraft'];
const moved = ['cadcraft', 'deckcraft', 'designcraft', 'gridcraft', 'pdfcraft', 'photocraft', 'soundcraft', 'vectorcraft', 'wordcraft'];

test('AIGC market retains four remote Craft candidates and excludes nine office Craft entries', () => {
  const catalog = read('catalog.json');
  const releases = read('docs/craft-marketplace-candidate-releases.json');
  for (const id of moved) assert.ok(!catalog.candidatePlugins.some(plugin => plugin.id === id), id);
  for (const id of retained) {
    const plugin = catalog.candidatePlugins.find(candidate => candidate.id === id);
    assert.equal(plugin.status, 'release_candidate_installable');
    assert.equal(plugin.codexSourcePath, undefined);
    const release = releases.find(entry => entry.plugin === id && entry.version === plugin.version);
    assert.ok(release, `${id}: missing release`);
    for (const prefix of ['', 'candidate-marketplace/']) {
      const card = read(`${prefix}.agents/plugins/marketplace.json`).plugins.find(entry => entry.name === id);
      assert.deepEqual(card.source, { source: 'url', url: `https://github.com/${plugin.repository}.git`, ref: `v${plugin.version}` });
      const zcode = read(`${prefix}marketplace.json`).plugins.find(entry => entry.name === id);
      if (release.maximumZipEntryBytes > 50 * 1024 * 1024) {
        assert.deepEqual(zcode.source, { source: 'github', repo: plugin.repository, ref: `v${plugin.version}` });
      } else {
        assert.equal(zcode.source.sha256, release.archiveSha256);
      }
    }
    assert.ok(!fs.existsSync(path.join(root, 'plugins', `${id}-plugin`)));
  }
  for (const file of ['.agents/plugins/marketplace.json', 'marketplace.json', 'kimi-marketplace.json']) {
    const entries = read(file).plugins;
    for (const id of moved) assert.ok(!entries.some(entry => (entry.name ?? entry.id) === id), `${file}: ${id}`);
  }
});

test('local ZCode distribution contains published packages and keeps Craft downloads remote', () => {
  const distribution = read('dist/local-marketplace/marketplace.json');
  const catalog = read('catalog.json');
  for (const plugin of catalog.plugins) {
    const entry = distribution.plugins.find(item => item.name === plugin.id);
    assert.equal(entry.source, `./plugins/${plugin.id}`);
    assert.ok(fs.existsSync(path.join(root, 'dist/local-marketplace/plugins', plugin.id, 'plugin.json')));
  }
  for (const plugin of catalog.candidatePlugins.filter(item => item.id.endsWith('craft'))) {
    const entry = distribution.plugins.find(item => item.name === plugin.id);
    assert.notEqual(typeof entry.source, 'string');
    assert.ok(!fs.existsSync(path.join(root, 'dist/local-marketplace/plugins', plugin.id)));
  }
});
