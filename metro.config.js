const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

// Ensure 'web' is registered as a valid platform for extension resolution (.web.tsx)
if (!config.resolver.platforms.includes('web')) {
  config.resolver.platforms.push('web');
}

// Custom resolver to handle Node.js SSR builds of face-api
config.resolver.resolveRequest = (context, moduleName, platform) => {
  // Redirect @tensorflow/tfjs-node to empty module during bundling
  if (moduleName === '@tensorflow/tfjs-node') {
    return {
      type: 'empty',
    };
  }

  // Force all face-api imports to use the ESM browser bundle (which contains its own CPU/WebGL tfjs engine)
  if (moduleName === '@vladmandic/face-api' || moduleName.endsWith('face-api.node.js')) {
    return context.resolveRequest(
      context,
      '@vladmandic/face-api/dist/face-api.esm.js',
      platform
    );
  }

  // Fallback to default resolver
  return context.resolveRequest(context, moduleName, platform);
};

module.exports = config;
