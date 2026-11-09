import assert from "node:assert/strict";
import test from "node:test";

import {
  validateInstalledCapabilityManifest,
  validateSkillCapabilityContract,
} from "../scripts/release_install_canary.mjs";
import { AdapterError } from "../scripts/runtime_adapter.mjs";

const packaged = {
  schema: "jianying-capabilities/v1",
  cli_version: "1.6.0",
  contract_state: "released",
  release_ref: "v1.6.0",
  source_commit: "a".repeat(40),
  capabilities: [
    { id: "capabilities", status: "supported" },
    { id: "schema.job_v2", status: "supported" },
  ],
};

test("accepts a runtime capability handshake identical to the packaged manifest", () => {
  validateInstalledCapabilityManifest(
    { ...packaged, capabilities: [...packaged.capabilities] },
    packaged,
  );
});

test("rejects capability content drift even when release identity is unchanged", () => {
  const runtime = {
    ...packaged,
    capabilities: packaged.capabilities.map((entry) => ({ ...entry })),
  };
  runtime.capabilities[1].status = "partial";
  assert.throws(
    () => validateInstalledCapabilityManifest(runtime, packaged),
    (error) => error instanceof AdapterError
      && error.code === "release_capability_manifest_mismatch",
  );
});

test("requires every locked skill capability to be supported by the installed release", () => {
  const skillsLock = {
    version: 1,
    sources: [{
      package: "jianying-skills",
      releaseVersion: "2.0.3",
      minimumCliVersion: "1.6.0",
      minimumCapabilities: ["capabilities", "schema.job_v2"],
    }],
  };
  assert.deepEqual(validateSkillCapabilityContract(packaged, skillsLock), {
    skillsVersion: "2.0.3",
    minimumCliVersion: "1.6.0",
    requiredCapabilities: ["capabilities", "schema.job_v2"],
  });

  const partial = {
    ...packaged,
    capabilities: packaged.capabilities.map((entry) => ({ ...entry })),
  };
  partial.capabilities[1].status = "partial";
  assert.throws(
    () => validateSkillCapabilityContract(partial, skillsLock),
    (error) => error instanceof AdapterError
      && error.code === "skill_capability_contract_incomplete"
      && error.details.unsupported[0].id === "schema.job_v2"
      && error.details.unsupported[0].status === "partial",
  );
});

test("rejects a skill capability missing from the installed manifest", () => {
  const skillsLock = {
    version: 1,
    sources: [{
      package: "jianying-skills",
      releaseVersion: "2.0.3",
      minimumCliVersion: "1.6.0",
      minimumCapabilities: ["job.run"],
    }],
  };
  assert.throws(
    () => validateSkillCapabilityContract(packaged, skillsLock),
    (error) => error instanceof AdapterError
      && error.code === "skill_capability_contract_incomplete"
      && error.details.unsupported[0].status === "missing",
  );
});

test("rejects an installed CLI older than the locked Skills minimum", () => {
  const skillsLock = {
    version: 1,
    sources: [{
      package: "jianying-skills",
      releaseVersion: "2.0.3",
      minimumCliVersion: "1.7.0",
      minimumCapabilities: ["capabilities"],
    }],
  };
  assert.throws(
    () => validateSkillCapabilityContract(packaged, skillsLock),
    (error) => error instanceof AdapterError
      && error.code === "skill_capability_contract_incomplete"
      && error.details.versionCompatible === false
      && error.details.unsupported.length === 0,
  );
});

test("rejects malformed or ambiguous Skills capability locks", () => {
  const invalidLocks = [
    { version: 1, sources: [] },
    {
      version: 1,
      sources: [{
        package: "jianying-skills",
        releaseVersion: "2.0.3",
        minimumCliVersion: "1.6",
        minimumCapabilities: ["capabilities"],
      }],
    },
    {
      version: 1,
      sources: [{
        package: "jianying-skills",
        releaseVersion: "2.0.3",
        minimumCliVersion: "1.6.0",
        minimumCapabilities: ["capabilities", "capabilities"],
      }],
    },
  ];
  for (const skillsLock of invalidLocks) {
    assert.throws(
      () => validateSkillCapabilityContract(packaged, skillsLock),
      (error) => error instanceof AdapterError
        && error.code === "skill_capability_contract_invalid",
    );
  }
});
