// SPDX-License-Identifier: MIT
// Copyright (c) 2026 Nunzio Raciti
// Start of an LVGL MPY Studio game in the browser: MicroPython in WebAssembly, LVGL draws on the canvas.
import "./micropython.mjs";

const TONE = "\x1bLVSIM_TONE ";
const status = document.getElementById("status");
const canvas = document.getElementById("canvas");
let audio = null;
let oscillator = null;
let stopAt = null;
// For whoever tests the page from outside, for example a test: how many tones the game asked for.
window.lms = { tones: 0, running: false };

function show(text, failed = false) {
    status.textContent = text;
    status.classList.toggle("failed", failed);
}

// The Buzzer of the game writes tone markers: here they become sound with Web Audio.
function play(frequency, milliseconds) {
    if (!audio) {
        return; // the browser allows sound only after a first touch
    }
    clearTimeout(stopAt);
    if (oscillator) {
        oscillator.stop();
        oscillator = null;
    }
    if (frequency <= 0) {
        return;
    }
    oscillator = audio.createOscillator();
    const gain = audio.createGain();
    oscillator.type = "square";
    oscillator.frequency.value = frequency;
    gain.gain.value = 0.08;
    oscillator.connect(gain).connect(audio.destination);
    oscillator.start();
    if (milliseconds > 0) {
        stopAt = setTimeout(() => play(0, 0), milliseconds);
    }
}

function output(line) {
    const start = line.indexOf(TONE);
    if (start >= 0) {
        const [frequency, milliseconds] = line.slice(start + TONE.length).split(" ").map(Number);
        window.lms.tones += 1;
        play(frequency, milliseconds);
        line = line.slice(0, start);
    }
    if (line) {
        console.log(line);
    }
}

window.addEventListener("pointerdown", () => {
    if (!audio) {
        audio = new AudioContext();
    }
}, { once: true });

async function run(code, Module) {
    const length = Module.lengthBytesUTF8(code);
    const source = Module._malloc(length + 1);
    Module.stringToUTF8(code, source, length + 1);
    const result = Module._malloc(3 * 4);
    // async: the game never ends, and between two frames it gives control back to the browser.
    await Module.ccall("mp_js_do_exec", "number", ["pointer", "number", "pointer"], [source, length, result], { async: true });
    proxy_convert_mp_to_js_obj_jsside_with_free(result); // raises the Python error, if there was one
}

async function start() {
    show("Loading…");
    const mp = await loadMicroPython({
        pystack: 64 * 1024,
        heapsize: 24 * 1024 * 1024,
        stdout: output,
        stderr: (line) => console.error(line),
    });
    const Module = mp._module;
    Module.canvas = canvas;
    const files = await (await fetch("game/files.json")).json();
    for (const name of files) {
        const response = await fetch("game/" + name);
        mp.FS.writeFile("/" + name, new Uint8Array(await response.arrayBuffer()));
    }
    show("");
    window.lms.running = true;
    await run("import main\nmain.main()\n", Module);
}

start().catch((error) => {
    console.error(error);
    show(String(error.message || error).split("\n").slice(-3).join("\n"), true);
});
