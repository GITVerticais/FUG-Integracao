const fs = require("fs");
const path = require("path");

const dest = path.join("public", "downloads");
fs.rmSync(dest, { recursive: true, force: true });
fs.cpSync("downloads", dest, { recursive: true });
