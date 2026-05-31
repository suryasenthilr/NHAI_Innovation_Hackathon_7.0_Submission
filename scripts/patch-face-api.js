const fs = require('fs');
const path = require('path');

const files = [
  path.join(__dirname, '../node_modules/@vladmandic/face-api/dist/tfjs.esm.js'),
  path.join(__dirname, '../node_modules/@vladmandic/face-api/dist/face-api.esm.js'),
  path.join(__dirname, '../node_modules/@vladmandic/face-api/dist/face-api.js')
];

console.log('Running BharatVerify Biometrics Compatibility Patch...');

files.forEach(file => {
  if (fs.existsSync(file)) {
    try {
      let content = fs.readFileSync(file, 'utf8');
      
      // Patch TextEncoder constructor lookup
      if (content.includes('new this.util.TextEncoder')) {
        content = content.replace(
          /new this\.util\.TextEncoder/g,
          'new (typeof TextEncoder !== "undefined" ? TextEncoder : this.util.TextEncoder)'
        );
        console.log(`- Patched TextEncoder in: ${path.basename(file)}`);
      }
      
      // Patch TextDecoder constructor lookup
      if (content.includes('new this.util.TextDecoder')) {
        content = content.replace(
          /new this\.util\.TextDecoder/g,
          'new (typeof TextDecoder !== "undefined" ? TextDecoder : this.util.TextDecoder)'
        );
        console.log(`- Patched TextDecoder in: ${path.basename(file)}`);
      }
      
      fs.writeFileSync(file, content, 'utf8');
    } catch (e) {
      console.error(`- Failed to patch file: ${file}`, e.message);
    }
  } else {
    console.log(`- File not found (skipping): ${path.basename(file)}`);
  }
});

console.log('Compatibility patch completed successfully.');
