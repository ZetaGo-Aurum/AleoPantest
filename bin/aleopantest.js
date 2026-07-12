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

  if (venvUsable(venv)) {
    log("[+] AleoPantest is already installed (venv ready).", "green");
  } else {
    // The npm package may ship the Python sources alongside this script.
    const pkgRoot = path.resolve(__dirname, "..");
    setupVenv(python, venv, pkgRoot);
  }

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
