const fs = require('fs');
const path = require('path');

const SRC_DIR = path.join(__dirname, '../dist');
const DEST_DIR = path.join(__dirname, '../android/app/src/main/assets/web');
const MODELS_SRC_DIR = path.join(__dirname, '../public/models');

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

function generateBase64ModelsFile(destDir) {
  const filesToInline = [
    'ssd_mobilenetv1_model-weights_manifest.json',
    'ssd_mobilenetv1_model.bin',
    'face_landmark_68_model-weights_manifest.json',
    'face_landmark_68_model.bin',
    'face_recognition_model-weights_manifest.json',
    'face_recognition_model.bin'
  ];

  console.log('Generating inline base64 models-data.js inside assets web directory...');
  let jsContent = '/* Generated file - containing base64 face models data */\n';
  jsContent += 'window.faceModelsData = {\n';

  filesToInline.forEach((filename) => {
    const filepath = path.join(MODELS_SRC_DIR, filename);
    if (!fs.existsSync(filepath)) {
      throw new Error(`Model file not found in public/models: ${filepath}`);
    }
    const data = fs.readFileSync(filepath);
    const base64 = data.toString('base64');
    const isJson = filename.endsWith('.json');
    const mimeType = isJson ? 'application/json' : 'application/octet-stream';
    
    jsContent += `  "${filename}": "data:${mimeType};base64,${base64}",\n`;
  });

  jsContent += '};\n';
  
  const outputPath = path.join(destDir, 'models-data.js');
  fs.writeFileSync(outputPath, jsContent, 'utf8');
  console.log(`Generated models-data.js at: ${outputPath}`);
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
          let content = fs.readFileSync(fullPath, 'utf8');
          
          // 1. Replace absolute paths with relative paths
          let updatedContent = content.replace(/(["'])\/(_expo|assets|models|favicon\.ico)/g, '$1./$2');
          
          // 2. Inject models-data.js script into HTML files
          if (ext === '.html') {
            if (!updatedContent.includes('models-data.js')) {
              updatedContent = updatedContent.replace('</head>', '<script src="./models-data.js"></script></head>');
              console.log(`  Injected models-data.js script into ${item}`);
            }
          }
          
          if (content !== updatedContent) {
            fs.writeFileSync(fullPath, updatedContent, 'utf8');
            console.log(`  Updated file content for ${item}`);
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
  
  console.log('Generating base64 models data...');
  generateBase64ModelsFile(DEST_DIR);
  
  console.log('Post-processing assets to resolve absolute paths and inject script tags...');
  processAssetsRecursively(DEST_DIR);
  
  console.log('Assets successfully copied and processed in android/app/src/main/assets/web!');
} catch (err) {
  console.error('Error copying assets:', err);
  process.exit(1);
}
