// 仅调用固定 Web 页面已公开的 API，不假定 Web 与原生 CLI 的能力相同。
export async function discover(api = globalThis.effectcraft) {
  if (!api || typeof api.info !== 'function' || typeof api.commands !== 'function') {
    throw new Error('effectcraft_web_not_ready');
  }
  const info = await api.info();
  const commands = await api.commands();
  if (info?.load?.error) throw new Error('effectcraft_web_load_failed');
  return {schema: 'effectcraft-web-capabilities/v1', info, commands,
    acceptance: 'NOT_RUN', managedEditing: 'NOT_RUN'};
}

export async function inspect(api = globalThis.effectcraft) {
  await discover(api);
  return await api.inspect();
}

export async function readArtifact(path, api = globalThis.effectcraft) {
  if (typeof path !== 'string' || !path || path.includes('..')) throw new Error('invalid_artifact_path');
  await discover(api);
  const bytes = new Uint8Array(await api.readFile(path));
  if (!bytes.byteLength) throw new Error('empty_artifact');
  const hash = new Uint8Array(await crypto.subtle.digest('SHA-256', bytes));
  return {path, bytes, sha256: Array.from(hash, x => x.toString(16).padStart(2, '0')).join(''),
    technicalAcceptance: 'NOT_RUN'};
}
