#!/usr/bin/env node

/**
 * Aleopantest NPM Wrapper
 * This script serves as a bootstrap to install the Python package via pip.
 */

const { execSync } = require("child_process");
const os = require("os");

console.log("\x1b[36m%s\x1b[0m", "[+] AleoPantest NPX/NPM Bootstrap Toolkit");

try {
  // Check if python is available
  let pythonCmd = "python3";
  try {
    execSync("python3 --version", { stdio: "ignore" });
  } catch (e) {
    pythonCmd = "python"; // Fallback for Windows
  }

  console.log(
    "\x1b[33m%s\x1b[0m",
    `[*] Verifying Python environment (${pythonCmd})...`,
  );

  // Check if already installed
  try {
    execSync(`${pythonCmd} -c "import aleopantest"`, { stdio: "ignore" });
    console.log(
      "\x1b[32m%s\x1b[0m",
      "[+] AleoPantest Python package is already installed.",
    );
  } catch (e) {
    console.log(
      "\x1b[33m%s\x1b[0m",
      "[*] AleoPantest Python package not found. Initiating installation...",
    );
    console.log(
      "\x1b[33m%s\x1b[0m",
      "[*] Running: pip install git+https://github.com/ZetaGo-Aurum/AleoPantest.git --no-cache-dir",
    );

    execSync(
      `${pythonCmd} -m pip install git+https://github.com/ZetaGo-Aurum/AleoPantest.git --no-cache-dir`,
      {
        stdio: "inherit",
      },
    );
    console.log(
      "\x1b[32m%s\x1b[0m",
      "[+] Python package installed successfully.",
    );
  }

  const args = process.argv.slice(2).join(" ");
  if (args) {
    console.log("\x1b[36m%s\x1b[0m", `[+] Executing: alpnts ${args}`);
    execSync(`alpnts ${args}`, { stdio: "inherit" });
  } else {
    console.log(
      "\x1b[32m%s\x1b[0m",
      "\nInstallation complete! You can now use the 'alpnts' or 'aleopantest' commands anywhere.",
    );
    console.log("Try running: alpnts --help");
  }
} catch (err) {
  console.error("\x1b[31m%s\x1b[0m", "[-] An error occurred during execution:");
  console.error(err.message);
  process.exit(1);
}
