const fs = require('fs');
const path = require('path');

const MODELS_DIR = path.join(__dirname, '../public/models');
const OUTPUT_FILE = path.join(__dirname, '../src/services/faceModelsData.js');

const filesToInline = [
  'ssd_mobilenetv1_model-weights_manifest.json',
  'ssd_mobilenetv1_model.bin',
  'face_landmark_68_model-weights_manifest.json',
  'face_landmark_68_model.bin',
  'face_recognition_model-weights_manifest.json',
  'face_recognition_model.bin'
];

try {
  console.log('Generating inline base64 model data...');
  let jsContent = '/* Generated file - do not edit directly */\n';
  jsContent += 'export const faceModelsData = {\n';

  filesToInline.forEach((filename) => {
    const filepath = path.join(MODELS_DIR, filename);
    if (!fs.existsSync(filepath)) {
      throw new Error(`Model file not found: ${filepath}`);
    }
    const data = fs.readFileSync(filepath);
    const base64 = data.toString('base64');
    const isJson = filename.endsWith('.json');
    const mimeType = isJson ? 'application/json' : 'application/octet-stream';
    
    jsContent += `  "${filename}": "data:${mimeType};base64,${base64}",\n`;
    console.log(`  Processed ${filename} (${base64.length} base64 chars)`);
  });

  jsContent += '};\n';
  
  fs.writeFileSync(OUTPUT_FILE, jsContent, 'utf8');
  console.log(`Successfully generated faceModelsData.js at: ${OUTPUT_FILE}`);
} catch (e) {
  console.error('Failed to generate inline models:', e);
  process.exit(1);
}
