// SPDX-License-Identifier: MIT
// Copyright (c) 2026 Nunzio Raciti
// Start of a program without pages in the browser: MicroPython in WebAssembly, LVGL on the canvas,
// the keys of the page as the board's serial port. The page says where things are:
// <main data-flash="flash/" data-width="1024" data-height="600" data-board="…" data-entry="shell.py">
import "./micropython.mjs";

const SYSTEM = ["display_driver.py", "lms_sandbox.py", "lms_web_boot.py"];
const runtime = new URL(".", import.meta.url);
const main = document.querySelector("main[data-flash]");
const status = document.getElementById("status");
const canvas = document.getElementById("canvas");
const typing = document.getElementById("typing");
let keys = "";
// For whoever tests the page from outside: the last lines printed, and whether it runs.
window.lms = { running: false, output: [] };
window.lmsTake = () => {
    const taken = keys;
    keys = "";
    return taken;
};
window.lmsType = (text) => { keys += text; }; // for tests

function show(text, failed = false) {
    status.textContent = text;
    status.classList.toggle("failed", failed);
}

const SPECIAL = {
    ArrowUp: "\x1b[A", ArrowDown: "\x1b[B", ArrowRight: "\x1b[C", ArrowLeft: "\x1b[D",
    Home: "\x1b[H", End: "\x1b[F", Insert: "\x1b[2~", Delete: "\x1b[3~", PageUp: "\x1b[5~", PageDown: "\x1b[6~",
    Enter: "\r", Backspace: "\x7f", Tab: "\t", Escape: "\x1b",
    F1: "\x1bOP", F2: "\x1bOQ", F3: "\x1bOR", F4: "\x1bOS",
};
const CONTROL = { "[": "\x1b", "\\": "\x1c", "]": "\x1d", " ": "\x00" };

// The bytes xterm sends for a key, as the IDE's terminal: Ctrl-C and the others go to the program.
function keyBytes(event) {
    if (event.key === "Tab" && event.shiftKey) return "\x1b[Z";
    if (event.key in SPECIAL) return SPECIAL[event.key];
    if (event.ctrlKey && !event.altKey && event.key.length === 1) {
        const letter = event.key.toUpperCase();
        if (letter >= "A" && letter <= "Z") return String.fromCharCode(letter.charCodeAt(0) - 64);
        if (event.key in CONTROL) return CONTROL[event.key];
    }
    if (!event.ctrlKey && !event.metaKey && event.key.length === 1) return (event.altKey ? "\x1b" : "") + event.key;
    return "";
}

document.addEventListener("keydown", (event) => {
    if (!window.lms.running || event.isComposing) return;
    if (event.ctrlKey && event.shiftKey && (event.key === "V" || event.key === "C")) return; // paste and copy of the browser
    const data = keyBytes(event);
    if (data) {
        keys += data;
        event.preventDefault();
    }
});
document.addEventListener("paste", (event) => {
    if (!window.lms.running) return;
    keys += event.clipboardData.getData("text").replace(/\r?\n/g, "\r");
    event.preventDefault();
});
// Phones show a keyboard only for a text field: a touch on the screen focuses a hidden one.
canvas.addEventListener("pointerdown", () => typing.focus({ preventScroll: true }));
typing.addEventListener("input", () => {
    if (window.lms.running && typing.value) keys += typing.value;
    typing.value = "";
});

function output(line) {
    window.lms.output.push(line);
    window.lms.output.splice(0, window.lms.output.length - 200);
    console.log(line);
}

async function fetchBytes(url) {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`${url}: ${response.status}`);
    return new Uint8Array(await response.arrayBuffer());
}

function makeFolders(FS, path) {
    let current = "";
    for (const part of path.split("/").slice(0, -1).filter(Boolean)) {
        current += "/" + part;
        try { FS.mkdir(current); } catch (error) { /* already there */ }
    }
}

async function run(code, Module) {
    const length = Module.lengthBytesUTF8(code);
    const source = Module._malloc(length + 1);
    Module.stringToUTF8(code, source, length + 1);
    const result = Module._malloc(3 * 4);
    // async: the program waits for keys, and while it waits the browser runs (Asyncify).
    await Module.ccall("mp_js_do_exec", "number", ["pointer", "number", "pointer"], [source, length, result], { async: true });
}

async function start() {
    show("Loading…");
    const mp = await loadMicroPython({ pystack: 64 * 1024, heapsize: 32 * 1024 * 1024, stdout: output, stderr: output });
    const Module = mp._module;
    Module.canvas = canvas;
    for (const name of SYSTEM) {
        mp.FS.writeFile("/" + name, await fetchBytes(new URL("system/" + name, runtime)));
    }
    const { width, height, board, entry, flash } = main.dataset;
    mp.FS.writeFile("/lms_board.py", `WIDTH = ${Number(width)}\nHEIGHT = ${Number(height)}\nBOARD = ${JSON.stringify(board)}\nENTRY = ${JSON.stringify(entry)}\n`);
    mp.FS.mkdir("/flash");
    const files = await (await fetch(flash + "files.json")).json();
    for (const name of files) {
        makeFolders(mp.FS, "/flash/" + name);
        mp.FS.writeFile("/flash/" + name, await fetchBytes(flash + name));
    }
    show("Type on the keyboard; on a phone, touch the screen first.");
    window.lms.running = true;
    // The boot runs a REPL after the program, so it ends only on an error, which Python prints.
    await run("try:\n import lms_web_boot\nexcept BaseException as e:\n import sys\n sys.print_exception(e)\n", Module);
    window.lms.running = false;
    show("The program stopped: see the browser console.", true);
}

start().catch((error) => {
    window.lms.running = false;
    console.error(error);
    show(String(error.message || error).split("\n").slice(-3).join("\n"), true);
});
