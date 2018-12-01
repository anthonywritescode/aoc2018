#!/usr/bin/env nodejs
fs = require('fs');

function compute(s) {
    let val = 0;
    s.match(/[^\r\n]+/g).forEach(function (s) {
        val += parseInt(s, 10);
    });
    return val
}

(function () {
    if (process.argv.length != 3) {
        console.log(`usage: ${process.argv[1]} FILENAME`);
        process.exit(1);
    }
    let contents = fs.readFileSync(process.argv[2], 'utf8');
    console.log(compute(contents));
}());
