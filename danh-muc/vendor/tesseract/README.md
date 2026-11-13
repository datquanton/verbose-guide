On-device text recognition for the screenshot intake. Self-hosted so a visitor's image triggers no third-party request.

- tesseract.js 5.1.1 (`tesseract.min.js`, `worker.min.js`), Apache-2.0
- tesseract.js-core 5.1.1 (`tesseract-core-*-lstm.wasm.js`), Apache-2.0
- @tesseract.js-data/eng 1.0.0, `4.0.0_best_int` (`eng.traineddata.gz`), Apache-2.0 data, MIT package

Copied unmodified from the npm packages. Loaded only when a visitor chooses a screenshot.
