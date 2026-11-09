import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = relative => JSON.parse(fs.readFileSync(path.join(root, relative), 'utf8'));
const moved = ['cadcraft', 'deckcraft', 'designcraft', 'effectcraft', 'figcraft', 'filmcraft', 'gridcraft', 'lightcraft', 'pdfcraft', 'photocraft', 'soundcraft', 'vectorcraft', 'wordcraft'];

test('AIGC market excludes all 13 Craft entries now owned by the office market', () => {
  const catalog = read('catalog.json');
  for (const id of moved) assert.ok(!catalog.candidatePlugins.some(plugin => plugin.id === id), id);
  for (const file of ['.agents/plugins/marketplace.json', 'marketplace.json', 'kimi-marketplace.json', 'candidate-marketplace/.agents/plugins/marketplace.json', 'candidate-marketplace/marketplace.json', 'candidate-marketplace/kimi-marketplace.json']) {
    const entries = read(file).plugins;
    for (const id of moved) assert.ok(!entries.some(entry => (entry.name ?? entry.id) === id), `${file}: ${id}`);
  }
  for (const id of moved) assert.ok(!fs.existsSync(path.join(root, 'plugins', `${id}-plugin`)));
});

test('local ZCode distribution contains published packages without Craft payloads', () => {
  const distribution = read('dist/local-marketplace/marketplace.json');
  const catalog = read('catalog.json');
  for (const plugin of catalog.plugins) {
    const entry = distribution.plugins.find(item => item.name === plugin.id);
    assert.equal(entry.source, `./plugins/${plugin.id}`);
    assert.ok(fs.existsSync(path.join(root, 'dist/local-marketplace/plugins', plugin.id, 'plugin.json')));
  }
  for (const id of moved) assert.ok(!fs.existsSync(path.join(root, 'dist/local-marketplace/plugins', id)));
});
