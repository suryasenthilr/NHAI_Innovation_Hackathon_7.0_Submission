const fs = require('fs');
const path = require('path');

const SRC_DIR = path.join(__dirname, '../dist');
const DEST_DIR = path.join(__dirname, '../android/app/src/main/assets/web');

function copyRecursiveSync(src, dest) {
  const exists = fs.existsSync(src);
  const stats = exists && fs.statSync(src);
  const isDirectory = exists && stats.isDirectory();
  
  if (isDirectory) {
    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }
    fs.readdirSync(src).forEach((childItemName) => {
      copyRecursiveSync(
        path.join(src, childItemName),
        path.join(dest, childItemName)
      );
    });
  } else {
    fs.copyFileSync(src, dest);
  }
}

function cleanDir(dir) {
  if (fs.existsSync(dir)) {
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

try {
  console.log('Cleaning destination directory...');
  cleanDir(DEST_DIR);
  
  console.log('Copying assets from dist/ to android assets...');
  copyRecursiveSync(SRC_DIR, DEST_DIR);
  
  console.log('Assets successfully copied to android/app/src/main/assets/web!');
} catch (err) {
  console.error('Error copying assets:', err);
  process.exit(1);
}
