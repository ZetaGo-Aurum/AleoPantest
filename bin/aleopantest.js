#!/usr/bin/env node

/**
 * AleoPantest NPX/NPM Bootstrap Toolkit
 *
 * Installs the AleoPantest Python package into an isolated virtualenv
 * located at ~/.aleopantest/venv (or $ALEOPANTEST_HOME/venv). This avoids:
 *   - PEP 668 "externally-managed-environment" errors
 *   - system-wide pip permission issues
 *   - the need to run pip with --break-system-packages
 *
 * The wrapper works the same on Linux, macOS, Windows, Termux and WSL.
 */

const { execSync } = require("child_process");
const os = require("os");
const fs = require("fs");
const path = require("path");

const c = {
  cyan: (s) => `\x1b[36m${s}\x1b[0m`,
  yellow: (s) => `\x1b[33m${s}\x1b[0m`,
  green: (s) => `\x1b[32m${s}\x1b[0m`,
  red: (s) => `\x1b[31m${s}\x1b[0m`,
  dim: (s) => `\x1b[2m${s}\x1b[0m`,
};

function log(msg, color = "cyan") {
  console.log(c[color](msg));
}

function findPython() {
  const candidates = ["python3", "python3.13", "python3.12", "python3.11", "python3.10", "python3.9", "python"];
  for (const cmd of candidates) {
    try {
      execSync(`${cmd} --version`, { stdio: "ignore" });
      return cmd;
    } catch (e) {
      /* try next */
    }
  }
  return null;
}

function getVenvDir() {
  if (process.env.ALEOPANTEST_HOME) {
    return path.join(process.env.ALEOPANTEST_HOME, "venv");
  }
  return path.join(os.homedir(), ".aleopantest", "venv");
}

function getBinDir(venv) {
  return process.platform === "win32" ? path.join(venv, "Scripts") : path.join(venv, "bin");
}

function getExe(name, binDir) {
  return path.join(binDir, name + (process.platform === "win32" ? ".exe" : ""));
}

function run(cmd, opts = {}) {
  return execSync(cmd, Object.assign({ stdio: "inherit" }, opts));
}

function runQuiet(cmd) {
  try {
    return execSync(cmd, { stdio: "ignore" });
  } catch (e) {
    return null;
  }
}

function venvUsable(venv) {
  const binDir = getBinDir(venv);
  return fs.existsSync(getExe("alpnts", binDir)) && fs.existsSync(getExe("python", binDir));
}

function setupVenv(python, venv, pkgSource) {
  const binDir = getBinDir(venv);
  log(`[*] Creating isolated virtual environment at: ${venv}`, "yellow");
  fs.mkdirSync(path.dirname(venv), { recursive: true });

  try {
    run(`"${python}" -m venv "${venv}"`);
  } catch (e) {
    // Some systems (Debian/Ubuntu) require python3-venv; try ensuring it.
    log(`[!] venv module unavailable, attempting to install python3-venv...`, "yellow");
    runQuiet("sudo apt-get update -qq");
    runQuiet("sudo apt-get install -y python3-venv python3-full");
    run(`"${python}" -m venv "${venv}"`);
  }

  const pip = getExe("pip", binDir);
  log(`[*] Upgrading pip inside the virtual environment...`, "yellow");
  runQuiet(`"${pip}" install --upgrade pip setuptools wheel`);

  log(`[*] Installing AleoPantest into the virtual environment...`, "yellow");
  if (pkgSource && fs.existsSync(path.join(pkgSource, "setup.py"))) {
    // Install from the local package (used when bundled with the npm package).
    log(`[*] Source detected at ${pkgSource} - installing locally.`, "yellow");
    run(`"${pip}" install --no-cache-dir "${pkgSource}"`);
  } else {
    // Fall back to installing the latest release from the official repository.
    log(`[*] Installing from https://github.com/ZetaGo-Aurum/AleoPantest.git`, "yellow");
    run(`"${pip}" install --no-cache-dir git+https://github.com/ZetaGo-Aurum/AleoPantest.git`);
  }
  log(`[+] AleoPantest installed successfully inside the virtual environment.`, "green");
}

/**
 * Make `alpnts` and `aleopantest` available as standalone commands by symlinking
 * the venv executables into a directory that is (or will be) on the user's PATH.
 * This is what lets `alpnts --help` work after `npx @zetagoaurum-dev/aleopantest`.
 */
function createCommandSymlinks(binDir) {
  const targets = ["alpnts", "aleopantest"];
  const pathDirs = (process.env.PATH || "")
    .split(path.delimiter)
    .filter((d) => d && fs.existsSync(d));

  // Prefer an existing, writable directory already on PATH.
  const candidates = [
    path.join(os.homedir(), ".local", "bin"),
    path.join(os.homedir(), "bin"),
    ...pathDirs,
  ];

  let chosen = null;
  for (const d of candidates) {
    try {
      if (fs.existsSync(d) && fs.accessSync(d, fs.constants.W_OK)) {
        chosen = d;
        break;
      }
    } catch (e) {
      /* not writable, try next */
    }
  }

  // Fall back to creating ~/.local/bin.
  if (!chosen) {
    chosen = path.join(os.homedir(), ".local", "bin");
    fs.mkdirSync(chosen, { recursive: true });
  }

  const linked = [];
  for (const t of targets) {
    const src = getExe(t, binDir);
    if (!fs.existsSync(src)) continue;
    const link = path.join(chosen, t);
    try {
      if (fs.existsSync(link) || isSymlink(link)) fs.unlinkSync(link);
      fs.symlinkSync(src, link);
      linked.push(t);
    } catch (e) {
      // Could be a permissions issue on a system dir - skip silently.
    }
  }

  if (linked.length > 0) {
    log(`[+] Linked command(s) ${linked.join(", ")} -> ${chosen}`, "green");
    if (!pathDirs.includes(chosen)) {
      log(
        `    Add to PATH once: export PATH="${chosen}:$PATH"  (and append it to ~/.bashrc)`,
        "yellow",
      );
    } else {
      log(`    You can now run '${linked[0]} --help' from anywhere.`, "cyan");
    }
  } else {
    log(
      `    Could not create a PATH symlink automatically. Run the venv binary directly:`,
      "yellow",
    );
    log(`    "${getExe("alpnts", binDir)}" --help`, "yellow");
  }
}

function isSymlink(p) {
  try {
    return fs.lstatSync(p).isSymbolicLink();
  } catch (e) {
    return false;
  }
}

// Bump this whenever a new npm release should force a Python package upgrade.
const BOOTSTRAP_VERSION = "4.0.5";

function readMarker(p) {
  try {
    return fs.readFileSync(p, "utf8").trim();
  } catch (e) {
    return "";
  }
}

function main() {
  log("[+] AleoPantest NPX/NPM Bootstrap Toolkit");

  const python = findPython();
  if (!python) {
    log("[-] Python 3 was not found on this system.", "red");
    log("    Please install Python 3.9+ and make sure 'python3' is on your PATH, then try again.", "yellow");
    process.exit(1);
  }
  log(`[*] Using Python interpreter: ${python}`, "yellow");

  const venv = getVenvDir();
  const binDir = getBinDir(venv);
  const alpnts = getExe("alpnts", binDir);
  const marker = path.join(venv, ".aleopantest_bootstrap");

  // Install (or upgrade) whenever the venv is missing or older than this bootstrap.
  if (venvUsable(venv) && readMarker(marker) === BOOTSTRAP_VERSION) {
    log("[+] AleoPantest is already installed (venv ready).", "green");
  } else {
    if (venvUsable(venv)) {
      log(`[*] A newer AleoPantest is available - upgrading virtual environment...`, "yellow");
    }
    // The npm package may ship the Python sources alongside this script.
    const pkgRoot = path.resolve(__dirname, "..");
    setupVenv(python, venv, pkgRoot);
    try {
      fs.writeFileSync(marker, BOOTSTRAP_VERSION);
    } catch (e) {
      /* best effort */
    }
  }

  // Expose alpnts/aleopantest on PATH so the command works standalone.
  createCommandSymlinks(binDir);

  const args = process.argv.slice(2);
  if (args.length === 0) {
    log("\n[+] Installation complete! AleoPantest lives in an isolated virtual environment.", "green");
    log("    Run it with:  alpnts --help", "cyan");
    log("    Or simply:    aleopantest --help", "cyan");
    return;
  }

  log(`[+] Executing: alpnts ${args.join(" ")}`, "cyan");
  try {
    run(`"${alpnts}" ${args.map((a) => JSON.stringify(a)).join(" ")}`);
  } catch (err) {
    // Surface non-zero exit codes from the underlying tool.
    process.exit(typeof err.status === "number" ? err.status : 1);
  }
}

try {
  main();
} catch (err) {
  log("[-] An error occurred during execution:", "red");
  console.error(err.message || err);
  process.exit(1);
}
