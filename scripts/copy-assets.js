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

function processAssetsRecursively(dir) {
  if (!fs.existsSync(dir)) return;
  const items = fs.readdirSync(dir);
  items.forEach((item) => {
    const fullPath = path.join(dir, item);
    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) {
      processAssetsRecursively(fullPath);
    } else {
      const ext = path.extname(item).toLowerCase();
      if (ext === '.html' || ext === '.js') {
        console.log(`Processing file: ${fullPath}`);
        try {
          const content = fs.readFileSync(fullPath, 'utf8');
          // Replace absolute paths starting with /_expo, /assets, /models, or /favicon.ico with relative paths
          // Matches: "/_expo", "/assets", "/models", "/favicon.ico" inside double or single quotes
          const updatedContent = content.replace(/(["'])\/(_expo|assets|models|favicon\.ico)/g, '$1./$2');
          
          if (content !== updatedContent) {
            fs.writeFileSync(fullPath, updatedContent, 'utf8');
            console.log(`  Updated absolute paths in ${item}`);
          }
        } catch (e) {
          console.error(`  Error processing ${item}:`, e.message);
        }
      }
    }
  });
}

try {
  console.log('Cleaning destination directory...');
  cleanDir(DEST_DIR);
  
  console.log('Copying assets from dist/ to android assets...');
  copyRecursiveSync(SRC_DIR, DEST_DIR);
  
  console.log('Post-processing assets to resolve absolute paths...');
  processAssetsRecursively(DEST_DIR);
  
  console.log('Assets successfully copied and processed in android/app/src/main/assets/web!');
} catch (err) {
  console.error('Error copying assets:', err);
  process.exit(1);
}
